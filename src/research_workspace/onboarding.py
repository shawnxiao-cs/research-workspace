"""Interactive, local researcher profile onboarding."""
from __future__ import annotations

import json
import os
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .profile import CANONICAL_KNOWLEDGE_DIMENSIONS, load_plain_yaml, validate_researcher_profile

STAGE_CHOICES = (
    ("undergraduate", "本科生", "Undergraduate"),
    ("masters", "硕士研究生", "Master's student"),
    ("doctoral", "博士研究生 / PhD", "Doctoral student / PhD"),
    ("postdoctoral", "博士后", "Postdoctoral researcher"),
    ("faculty", "高校教师 / 研究人员", "Faculty / academic researcher"),
    ("industry", "工业界研究人员", "Industry researcher"),
    ("independent", "独立研究者", "Independent researcher"),
)

LABELS = {
    "zh": {
        "title": "研究者画像", "stage_label": "当前阶段", "background_label": "研究背景", "interests_label": "研究兴趣",
        "goals_label": "研究目标", "sources_label": "学习来源", "knowledge_label": "知识状态",
        "welcome": "研究者画像仅保存在本机，默认不纳入 Git。留空表示保留现有值或跳过。",
        "existing_mode": "画像已存在：1 更新画像信息；2 重评知识主题；3 两者都做；0 取消",
        "existing_mode_error": "请选择 1、2、3 或 0。",
        "stage_question": "你目前的学业或职业阶段是什么？请选择一项。",
        "stage_other": "其他阶段（输入文字）", "stage_keep": "保留当前阶段", "stage_error": "请输入一个选项；阶段不能填写逗号分隔的主题列表。请重试。",
        "background": "研究背景（逗号分隔）", "interests": "研究兴趣（逗号分隔）", "goals": "研究目标（逗号分隔）",
        "sources": "学习来源（逗号分隔）", "topics": "学过的技术主题。示例：CNN, RNN, Self-Attention, Transformer",
        "topics_error": "主题列表无效（主题不能为空、不能只是数字）。请重新输入。",
        "topics_confirm": "将评估以下主题", "topics_accept": "确认 [y] / 重新输入 [r]", "topics_confirm_error": "请输入 y 确认，或 r 重新输入。",
        "topics_empty": "主题列表留空：现有主题及其评估会全部保留，不会进行重评。",
        "existing_topic_note": "选择的现有主题将按你的明确选择重新评估；快速重评会提议把其他维度设为“尚未评估”，并在预览中列出。",
        "mode": "评估模式：1 快速评估（概念 + 实现，默认）；2 详细评估（六个维度）",
        "mode_error": "请选择 1（快速）或 2（详细）。",
        "assessment": "选择菜单编号（这是选项序号，不是知识等级；6 表示尚未评估）",
        "assessment_error": "请输入菜单中的 1–6 选项，或留空保留当前值。",
        "not_assessed": "尚未评估", "confirm": "确认保存 [y] / 编辑 [e] / 取消 [c]",
        "edit_menu": "选择要编辑的部分：1 背景/阶段；2 研究兴趣/目标；3 学习来源；4 知识主题与评估；5 返回预览；6 取消",
        "edit_menu_error": "请选择 1–6。", "changes_title": "本次提议的变更",
        "cancel": "已取消，画像未修改。", "interrupt": "已取消，画像未修改。", "saved": "画像已验证并保存：",
        "missing": "尚无本机画像。请先运行 init 或 onboard。", "reason": "为本次知识状态变更填写一个可选原因（留空跳过）",
        "history_provenance": "user_self_report", "yes": "y", "no": "r",
        "dimensions": {"awareness": "接触程度", "conceptual": "概念理解", "mathematical": "数学理解", "implementation": "实现能力", "application": "实际应用", "research": "科研使用"},
        "values": {
            "awareness": ["未接触该主题", "听说过或见过基本术语", "熟悉用途和基本背景", "能独立识别相关概念", "能判断其研究适用性"],
            "conceptual": ["尚未接触", "知道用途和基本术语", "理解核心概念并能跟读论文", "能独立解释、分析和比较", "能从研究角度分析局限和设计取舍"],
            "mathematical": ["尚未学习相关数学", "见过相关符号或公式", "能理解主要推导", "能独立推导并分析假设", "能从研究角度扩展或评估数学方法"],
            "implementation": ["从未实现", "跟随教程或示例实现过", "能修改现有实现", "能独立实现核心模块", "能完成可运行实现并用于实验"],
            "application": ["从未用于实际任务", "观察过相关应用", "在指导下用于基础任务", "能独立用于实际任务", "能设计并评估研究级应用"],
            "research": ["尚未用于科研分析", "观察过相关研究", "能在指导下分析研究工作", "能独立分析研究问题", "能据此设计和推进研究"],
        },
    },
    "en": {
        "title": "Researcher Profile", "stage_label": "Current stage", "background_label": "Research background", "interests_label": "Research interests",
        "goals_label": "Research goals", "sources_label": "Learning sources", "knowledge_label": "Knowledge",
        "welcome": "Your profile stays on this machine and is ignored by Git by default. Blank keeps existing values or skips a field.",
        "existing_mode": "Profile exists: 1 Edit profile details; 2 Reassess knowledge; 3 Both; 0 Cancel",
        "existing_mode_error": "Choose 1, 2, 3, or 0.",
        "stage_question": "What is your current academic or professional stage? Choose one option.",
        "stage_other": "Other stage (enter text)", "stage_keep": "Keep current stage", "stage_error": "Enter one choice; a comma-separated topic list is not a stage. Please try again.",
        "background": "Research background (comma-separated)", "interests": "Research interests (comma-separated)", "goals": "Research goals (comma-separated)",
        "sources": "Learning sources (comma-separated)", "topics": "Technical topics studied. Example: CNN, RNN, Self-Attention, Transformer",
        "topics_error": "Invalid topic list (topics cannot be empty or numeric-only). Please re-enter it.",
        "topics_confirm": "Topics to assess", "topics_accept": "Confirm [y] / Re-enter [r]", "topics_confirm_error": "Enter y to confirm or r to re-enter.",
        "topics_empty": "Empty topic list: existing topics and assessments will be preserved; nothing will be reassessed.",
        "existing_topic_note": "Selected existing topics will be reassessed as requested. Quick Reassessment proposes Not assessed for other dimensions and shows these changes in the preview.",
        "mode": "Assessment mode: 1 Quick (conceptual + implementation, default); 2 Detailed (all six dimensions)",
        "mode_error": "Choose 1 (Quick) or 2 (Detailed).",
        "assessment": "Choose a menu number (this is an option index, not a knowledge level; 6 means Not assessed)",
        "assessment_error": "Enter a menu choice from 1–6, or leave blank to keep the current value.",
        "not_assessed": "Not assessed", "confirm": "Confirm save [y] / Edit [e] / Cancel [c]",
        "edit_menu": "Choose a section: 1 Background/stage; 2 Interests/goals; 3 Learning sources; 4 Knowledge topics and assessments; 5 Return to preview; 6 Cancel",
        "edit_menu_error": "Choose 1–6.", "changes_title": "Proposed changes",
        "cancel": "Cancelled; profile was not changed.", "interrupt": "Cancelled; profile was not changed.", "saved": "Validated profile saved:",
        "missing": "No local profile found. Run init or onboard first.", "reason": "Optional reason for these knowledge changes (blank to skip)",
        "history_provenance": "user_self_report", "yes": "y", "no": "r",
        "dimensions": {"awareness": "Awareness", "conceptual": "Conceptual understanding", "mathematical": "Mathematical understanding", "implementation": "Implementation", "application": "Practical application", "research": "Research use"},
        "values": {
            "awareness": ["Never encountered the topic", "Heard of it or seen basic terms", "Know its purpose and context", "Can independently recognize related concepts", "Can judge its research relevance"],
            "conceptual": ["Not yet encountered", "Know its purpose and basic terminology", "Understand core concepts and follow papers", "Can explain, analyze, and compare independently", "Can analyze limitations and design choices for research"],
            "mathematical": ["Have not studied its mathematics", "Seen related notation or equations", "Understand main derivations", "Can derive and analyze assumptions independently", "Can extend or assess the mathematics for research"],
            "implementation": ["Never implemented", "Followed a tutorial or example", "Can modify an existing implementation", "Can independently implement core modules", "Can build a working implementation and use it in experiments"],
            "application": ["Never used in a practical task", "Observed an application", "Can use it for basic tasks with guidance", "Can independently apply it to real tasks", "Can design and evaluate research-grade applications"],
            "research": ["Not used for research analysis", "Observed related research", "Can analyze research with guidance", "Can independently analyze research questions", "Can design and advance research using it"],
        },
    },
}


def parse_topics(value: str) -> list[str] | None:
    """Parse, trim and case-insensitively deduplicate a comma-separated topic list."""
    parts = [part.strip() for part in value.split(",") if part.strip()]
    if any(part.isdigit() or any(ord(ch) < 32 for ch in part) for part in parts):
        return None
    seen: set[str] = set()
    result = []
    for part in parts:
        key = part.casefold()
        if key not in seen:
            seen.add(key)
            result.append(part)
    return result


def _split(value: str) -> list[str]:
    """Parse a simple comma-separated list field, retaining its original ordering."""
    return [part.strip() for part in value.split(",") if part.strip()]


def _quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    return _quote(str(value))


def _yaml(value: Any, indent: int = 0) -> list[str]:
    pad = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{pad}{key}:")
                lines.extend(_yaml(item, indent + 2))
            elif isinstance(item, dict):
                lines.append(f"{pad}{key}: {{}}")
            elif isinstance(item, list):
                lines.append(f"{pad}{key}: []")
            else:
                lines.append(f"{pad}{key}: {_scalar(item)}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, dict):
                first = next(iter(item.items()), (None, None))
                if first[0] is None:
                    lines.append(f"{pad}- {{}}")
                    continue
                key, child = first
                if isinstance(child, (dict, list)):
                    lines.append(f"{pad}- {key}:")
                    lines.extend(_yaml(child, indent + 4))
                else:
                    lines.append(f"{pad}- {key}: {_scalar(child)}")
                for key, child in list(item.items())[1:]:
                    if isinstance(child, (dict, list)):
                        lines.append(f"{pad}  {key}:")
                        lines.extend(_yaml(child, indent + 4))
                    else:
                        lines.append(f"{pad}  {key}: {_scalar(child)}")
            else:
                lines.append(f"{pad}- {_scalar(item)}")
        return lines
    return [f"{pad}{_scalar(value)}"]


def _display_stage_choice(index: int, language: str) -> str:
    code, zh, en = STAGE_CHOICES[index]
    return zh if language == "zh" else en


def render_profile(data: dict[str, Any], language: str = "zh", verbose: bool = False) -> str:
    text = LABELS[language]
    researcher = data.get("researcher", {})
    stage = researcher.get("stage", "")
    stage_index = next((i for i, choice in enumerate(STAGE_CHOICES) if choice[0] == stage), None)
    if stage_index is not None:
        stage = _display_stage_choice(stage_index, language)
    lines = [text["title"], f"{text['stage_label']}: {stage}", "", text["background_label"]]
    lines.extend(f"- {item}" for item in researcher.get("background", []))
    lines.extend(["", text["interests_label"]])
    lines.extend(f"- {item}" for item in researcher.get("research_interests", []))
    lines.extend(["", text["goals_label"]])
    lines.extend(f"- {item}" for item in researcher.get("research_goals", []))
    lines.extend(["", text["sources_label"]])
    lines.extend(f"- {item}" for item in data.get("learning_progress", {}).get("sources", []))
    lines.extend(["", text["knowledge_label"]])
    for concept, dimensions in data.get("knowledge_state", {}).items():
        lines.append(str(concept))
        for dimension, level in dimensions.items():
            if level is None:
                label = text["not_assessed"]
            elif language == "zh" and dimension == "conceptual" and level == 2:
                label = "已理解"
            elif language == "zh" and dimension == "implementation" and level == 0:
                label = "从未实现"
            elif language == "en" and dimension == "conceptual" and level == 2:
                label = "Understood"
            elif language == "en" and dimension == "implementation" and level == 0:
                label = "Never implemented"
            else:
                label = text["values"][dimension][level]
            suffix = f" ({level if level is not None else 'null'})" if verbose else ""
            lines.append(f"  {text['dimensions'].get(dimension, dimension)}: {label}{suffix}")
    return "\n".join(lines)


def _ask_stage(input_fn: Callable[[str], str], output_fn: Callable[[str], None], profile: dict[str, Any], language: str) -> str:
    text = LABELS[language]
    while True:
        output_fn(text["stage_question"])
        output_fn(f"0. {text['stage_keep']} [{profile.get('stage', '')}]")
        for index, choice in enumerate(STAGE_CHOICES, 1):
            output_fn(f"{index}. {_display_stage_choice(index - 1, language)}")
        output_fn(f"8. {text['stage_other']}")
        raw = input_fn("Stage choice: ").strip()
        if not raw or raw == "0":
            return str(profile.get("stage", ""))
        if "," in raw:
            output_fn(text["stage_error"])
            continue
        if raw.isdigit() and 1 <= int(raw) <= len(STAGE_CHOICES):
            return STAGE_CHOICES[int(raw) - 1][0]
        if raw == "8":
            custom = input_fn(f"{text['stage_other']}: ").strip()
            if custom and "," not in custom:
                return custom
            output_fn(text["stage_error"])
            continue
        normalized = raw.casefold()
        aliases = {
            "undergraduate": 0, "本科生": 0, "bachelor": 0,
            "masters": 1, "master": 1, "硕士": 1, "硕士研究生": 1,
            "doctoral": 2, "phd": 2, "博士": 2, "博士研究生": 2,
            "postdoctoral": 3, "postdoc": 3, "博士后": 3,
            "faculty": 4, "academic researcher": 4, "高校教师": 4,
            "industry": 5, "industry researcher": 5, "工业界研究人员": 5,
            "independent": 6, "independent researcher": 6, "独立研究者": 6,
        }
        if normalized in aliases:
            return STAGE_CHOICES[aliases[normalized]][0]
        output_fn(text["stage_error"])


def _ask_topics(
    input_fn: Callable[[str], str], output_fn: Callable[[str], None], language: str,
    existing_topics: set[str] | None = None,
) -> list[str]:
    text = LABELS[language]
    existing_topics = existing_topics or set()
    while True:
        topics = parse_topics(input_fn(f"{text['topics']}: "))
        if topics is None:
            output_fn(text["topics_error"])
            continue
        if not topics:
            output_fn(text["topics_empty"])
            return []
        while True:
            output_fn(f"{text['topics_confirm']}: " + ", ".join(topics))
            if any(topic.casefold() in existing_topics for topic in topics):
                output_fn(text["existing_topic_note"])
            decision = input_fn(text["topics_accept"] + ": ").strip().lower()
            if decision in {"y", "yes", "是"}:
                return topics
            if decision in {"r", "no", "n", "否"}:
                break
            output_fn(text["topics_confirm_error"])


def _assessment_mode(
    input_fn: Callable[[str], str], output_fn: Callable[[str], None], language: str,
    reassessment: bool = False,
) -> str:
    text = LABELS[language]
    prompt = text["mode"]
    if reassessment:
        prompt = prompt.replace("Quick (", "Quick Reassessment (").replace("快速评估（", "快速重评（")
    while True:
        answer = input_fn(prompt + " ").strip() or "1"
        if answer in {"1", "2"}:
            return answer
        output_fn(text["mode_error"])


def _assess_dimension(
    input_fn: Callable[[str], str], output_fn: Callable[[str], None],
    concept: str, dimension: str, existing: Any, language: str,
) -> int | None:
    text = LABELS[language]
    output_fn(f"{concept} — {text['dimensions'][dimension]}")
    for index, description in enumerate(text["values"][dimension], 1):
        output_fn(f"  {index}. {description}")
    output_fn(f"  6. {text['not_assessed']}")
    while True:
        answer = input_fn(f"{text['assessment']} [1-6; Enter keeps current value]: ").strip()
        if not answer:
            return existing
        if answer in {"1", "2", "3", "4", "5", "6"}:
            return None if answer == "6" else int(answer) - 1
        output_fn(text["assessment_error"])


def _edit_profile_section(
    data: dict[str, Any], section: str, input_fn: Callable[[str], str],
    output_fn: Callable[[str], None], language: str,
) -> None:
    text = LABELS[language]
    researcher = data.setdefault("researcher", {})
    if section == "1":
        stage = _ask_stage(input_fn, output_fn, researcher, language)
        if stage:
            researcher["stage"] = stage
        answer = input_fn(f"{text['background']} [{', '.join(researcher.get('background', []))}]: ").strip()
        if answer:
            researcher["background"] = _split(answer)
    elif section == "2":
        for key, label in (("research_interests", "interests"), ("research_goals", "goals")):
            answer = input_fn(f"{text[label]} [{', '.join(researcher.get(key, []))}]: ").strip()
            if answer:
                researcher[key] = _split(answer)
    elif section == "3":
        learning_progress = data.setdefault("learning_progress", {})
        answer = input_fn(f"{text['sources']} [{', '.join(learning_progress.get('sources', []))}]: ").strip()
        if answer:
            learning_progress["sources"] = _split(answer)


def _assess_topics(
    data: dict[str, Any], input_fn: Callable[[str], str], output_fn: Callable[[str], None],
    language: str, reassessment: bool,
) -> None:
    text = LABELS[language]
    knowledge_state = data.setdefault("knowledge_state", {})
    existing = {name.casefold() for name in knowledge_state}
    topics = _ask_topics(input_fn, output_fn, language, existing)
    if not topics:
        return
    mode = _assessment_mode(input_fn, output_fn, language, reassessment=any(topic.casefold() in existing for topic in topics))
    dimensions_to_ask = CANONICAL_KNOWLEDGE_DIMENSIONS if mode == "2" else ("conceptual", "implementation")
    for concept in topics:
        concept_key = next((name for name in knowledge_state if name.casefold() == concept.casefold()), concept)
        previous = knowledge_state.get(concept_key, {})
        # Choosing Quick Reassessment explicitly proposes null for dimensions it does not ask.
        values = {dimension: None for dimension in CANONICAL_KNOWLEDGE_DIMENSIONS}
        for dimension in dimensions_to_ask:
            values[dimension] = _assess_dimension(input_fn, output_fn, concept_key, dimension, previous.get(dimension), language)
        knowledge_state[concept_key] = values


def _changes(original: dict[str, Any], proposed: dict[str, Any]) -> list[tuple[str, str, Any, Any]]:
    changes = []
    old_knowledge = original.get("knowledge_state", {})
    for concept, dimensions in proposed.get("knowledge_state", {}).items():
        previous = old_knowledge.get(concept)
        if not isinstance(previous, dict):
            continue
        for dimension, new_value in dimensions.items():
            old_value = previous.get(dimension)
            if old_value is not None and old_value != new_value:
                changes.append((concept, dimension, old_value, new_value))
    return changes


def _level_label(dimension: str, value: Any, language: str) -> str:
    text = LABELS[language]
    if value is None:
        return text["not_assessed"]
    if dimension == "conceptual" and value == 2:
        return "已理解" if language == "zh" else "Understood"
    if dimension == "implementation" and value == 0:
        return "从未实现" if language == "zh" else "Never implemented"
    return text["values"][dimension][value]


def render_changes(original: dict[str, Any], proposed: dict[str, Any], language: str = "zh") -> str:
    text = LABELS[language]
    lines = [text["changes_title"]]
    old_researcher = original.get("researcher", {})
    new_researcher = proposed.get("researcher", {})
    for key, label in (("stage", text["stage_label"]), ("background", text["background_label"]),
                       ("research_interests", text["interests_label"]), ("research_goals", text["goals_label"])):
        old_value, new_value = old_researcher.get(key), new_researcher.get(key)
        if old_value != new_value:
            lines.append(f"- {label}: {old_value!r} → {new_value!r}")
    old_sources = original.get("learning_progress", {}).get("sources")
    new_sources = proposed.get("learning_progress", {}).get("sources")
    if old_sources != new_sources:
        lines.append(f"- {text['sources_label']}: {old_sources!r} → {new_sources!r}")
    old_state = original.get("knowledge_state", {})
    new_state = proposed.get("knowledge_state", {})
    for concept, dimensions in new_state.items():
        before = old_state.get(concept, {})
        for dimension, value in dimensions.items():
            old_value = before.get(dimension) if isinstance(before, dict) else None
            if old_value != value:
                old_label = _level_label(dimension, old_value, language)
                new_label = _level_label(dimension, value, language)
                lines.append(f"- {concept} — {text['dimensions'][dimension]}: {old_label} → {new_label}")
        if concept not in old_state:
            lines.append(f"- {concept}: " + ("新增主题" if language == "zh" else "New topic"))
    if len(lines) == 1:
        lines.append("- " + ("没有字段变更" if language == "zh" else "No field changes"))
    return "\n".join(lines)


def _choose_edit(input_fn: Callable[[str], str], output_fn: Callable[[str], None], language: str) -> str:
    text = LABELS[language]
    while True:
        choice = input_fn(text["edit_menu"] + ": ").strip()
        if choice in {"1", "2", "3", "4", "5", "6"}:
            return choice
        output_fn(text["edit_menu_error"])


def _onboard(root: Path, language: str, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> int:
    text = LABELS[language]
    path = root / ".research/config/researcher-profile.yaml"
    output_fn(text["welcome"])
    profile_exists = path.exists()
    if not profile_exists:
        original = {
            "profile_version": "0.1",
            "researcher": {"id": "USER-0001", "stage": "", "background": [], "research_interests": [], "research_goals": []},
            "learning_progress": {"sources": []}, "knowledge_state": {},
            "provenance": {"type": "human", "review_status": "accepted", "source_refs": []},
        }
    else:
        try:
            original = load_plain_yaml(path)
        except (OSError, ValueError) as exc:
            output_fn(str(exc))
            return 1

    proposed = deepcopy(original)
    sections = {"profile": False, "knowledge": False}
    if profile_exists:
        while True:
            route = input_fn(text["existing_mode"] + ": ").strip()
            if route in {"0", "1", "2", "3"}:
                break
            output_fn(text["existing_mode_error"])
        if route == "0":
            output_fn(text["cancel"])
            return 0
        sections["profile"] = route in {"1", "3"}
        sections["knowledge"] = route in {"2", "3"}
    else:
        sections = {"profile": True, "knowledge": True}

    if sections["profile"]:
        _edit_profile_section(proposed, "1", input_fn, output_fn, language)
        _edit_profile_section(proposed, "2", input_fn, output_fn, language)
        _edit_profile_section(proposed, "3", input_fn, output_fn, language)
    if sections["knowledge"]:
        _assess_topics(proposed, input_fn, output_fn, language, reassessment=profile_exists)

    while True:
        output_fn(render_changes(original, proposed, language))
        output_fn(render_profile(proposed, language))
        decision = input_fn(text["confirm"] + ": ").strip().lower()
        if decision in {"c", "cancel", "q", "n", "取消"}:
            output_fn(text["cancel"])
            return 0
        if decision in {"e", "edit"}:
            section = _choose_edit(input_fn, output_fn, language)
            if section == "5":
                continue
            if section == "6":
                output_fn(text["cancel"])
                return 0
            if section == "4":
                _assess_topics(proposed, input_fn, output_fn, language, reassessment=True)
            else:
                _edit_profile_section(proposed, section, input_fn, output_fn, language)
            continue
        if decision not in {"y", "yes", "是", "确认"}:
            output_fn(text["cancel"])
            return 0

        changes = _changes(original, proposed)
        history = deepcopy(original.get("knowledge_state_history", []))
        if changes:
            reason = input_fn(text["reason"] + ": ").strip()
            for concept, dimension, old_value, new_value in changes:
                entry = {
                    "concept": concept, "dimension": dimension, "from": old_value, "to": new_value,
                    "timestamp": datetime.now(timezone.utc).isoformat(), "provenance": text["history_provenance"],
                }
                if reason:
                    entry["reason"] = reason
                history.append(entry)
        if history or "knowledge_state_history" in original:
            proposed["knowledge_state_history"] = history

        errors = validate_data(proposed, path)
        if errors:
            output_fn("\n".join(errors))
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        content = "\n".join(_yaml(proposed)) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        output_fn(f"{text['saved']} {path}")
        return 0


def onboard(
    root: Path, language: str = "zh", input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> int:
    try:
        return _onboard(root, language, input_fn, output_fn)
    except KeyboardInterrupt:
        output_fn(LABELS[language]["interrupt"])
        return 0


def validate_data(data: dict[str, Any], path: Path) -> list[str]:
    """Validate the exact serialized representation before committing it."""
    text = "\n".join(_yaml(data)) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as stream:
        stream.write(text)
        temp_path = Path(stream.name)
    try:
        return validate_researcher_profile(temp_path)
    finally:
        temp_path.unlink(missing_ok=True)
