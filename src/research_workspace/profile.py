from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .model import validate_knowledge_level

PROFILE_VERSION = "0.1"
CANONICAL_KNOWLEDGE_DIMENSIONS = (
    "awareness",
    "conceptual",
    "mathematical",
    "implementation",
    "application",
    "research",
)
REQUIRED_PROFILE_FIELDS = (
    "profile_version",
    "researcher",
    "learning_progress",
    "knowledge_state",
    "provenance",
)
REQUIRED_RESEARCHER_FIELDS = (
    "id",
    "stage",
    "background",
    "research_interests",
    "research_goals",
)
RESEARCHER_LIST_FIELDS = (
    "background",
    "research_interests",
    "research_goals",
)
PROVENANCE_TYPES = ("source", "generated", "human")
PROVENANCE_REVIEW_STATUSES = ("pending", "accepted", "edited", "rejected")


@dataclass(frozen=True)
class ResearcherProfile:
    path: Path
    data: dict[str, Any]

    @property
    def knowledge_state(self) -> dict[str, Any]:
        value = self.data.get("knowledge_state", {})
        return value if isinstance(value, dict) else {}

    @property
    def knowledge_state_history(self) -> Any:
        return self.data.get("knowledge_state_history")

    @property
    def provenance(self) -> dict[str, Any]:
        value = self.data.get("provenance", {})
        return value if isinstance(value, dict) else {}


@dataclass(frozen=True)
class _YamlLine:
    indent: int
    content: str


def load_researcher_profile(path: Path) -> ResearcherProfile:
    return ResearcherProfile(path=path, data=load_plain_yaml(path))


def validate_researcher_profile(path: Path) -> list[str]:
    try:
        profile = load_researcher_profile(path)
    except OSError as exc:
        return [f"{path}: unable to read researcher profile: {exc.strerror}"]
    except ValueError as exc:
        return [f"{path}: {exc}"]

    errors: list[str] = []
    data = profile.data
    if not isinstance(data, dict):
        return [f"{path}: profile must be a YAML mapping"]

    for field in REQUIRED_PROFILE_FIELDS:
        if field not in data:
            errors.append(f"{path}: missing field {field}")

    if "profile_version" in data and str(data["profile_version"]) != PROFILE_VERSION:
        errors.append(f"{path}: expected profile_version {PROFILE_VERSION}")

    if "researcher" in data:
        errors.extend(_validate_researcher(path, data["researcher"]))

    if "learning_progress" in data and not isinstance(data["learning_progress"], dict):
        errors.append(f"{path}: learning_progress must be a mapping")

    if "provenance" in data:
        errors.extend(_validate_provenance(path, data["provenance"]))

    if "knowledge_state" in data:
        errors.extend(_validate_knowledge_state(path, data["knowledge_state"]))

    return errors


def _validate_researcher(path: Path, researcher: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(researcher, dict):
        return [f"{path}: researcher must be a mapping"]

    for field in REQUIRED_RESEARCHER_FIELDS:
        if field not in researcher:
            errors.append(f"{path}: researcher.{field} is required")

    for field in ("id", "stage"):
        if field in researcher and not isinstance(researcher[field], str):
            errors.append(f"{path}: researcher.{field} must be a string")

    for field in RESEARCHER_LIST_FIELDS:
        if field in researcher and not isinstance(researcher[field], list):
            errors.append(f"{path}: researcher.{field} must be a list")

    return errors


def _validate_provenance(path: Path, provenance: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(provenance, dict):
        return [f"{path}: provenance must be a mapping"]

    if "type" not in provenance:
        errors.append(f"{path}: provenance.type is required")
    elif provenance["type"] not in PROVENANCE_TYPES:
        allowed = ", ".join(PROVENANCE_TYPES)
        errors.append(f"{path}: provenance.type must be one of: {allowed}")

    if "review_status" not in provenance:
        errors.append(f"{path}: provenance.review_status is required")
    elif provenance["review_status"] not in PROVENANCE_REVIEW_STATUSES:
        allowed = ", ".join(PROVENANCE_REVIEW_STATUSES)
        errors.append(f"{path}: provenance.review_status must be one of: {allowed}")

    if "source_refs" in provenance and not isinstance(provenance["source_refs"], list):
        errors.append(f"{path}: provenance.source_refs must be a list")

    return errors


def load_plain_yaml(path: Path) -> dict[str, Any]:
    lines = _yaml_lines(path.read_text(encoding="utf-8"))
    if not lines:
        return {}
    value, index = _parse_block(lines, 0, lines[0].indent)
    if index != len(lines):
        line = lines[index]
        raise ValueError(f"unexpected YAML content at indent {line.indent}: {line.content}")
    if not isinstance(value, dict):
        raise ValueError("profile must be a YAML mapping")
    return value


def _validate_knowledge_state(path: Path, knowledge_state: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(knowledge_state, dict):
        return [f"{path}: knowledge_state must be a mapping"]

    for concept, dimensions in knowledge_state.items():
        if not isinstance(dimensions, dict):
            errors.append(f"{path}: knowledge_state.{concept} must be a mapping")
            continue
        for dimension, level in dimensions.items():
            if dimension not in CANONICAL_KNOWLEDGE_DIMENSIONS:
                errors.append(
                    f"{path}: knowledge_state.{concept}.{dimension} is not a canonical dimension"
                )
                continue
            if not validate_knowledge_level(level):
                errors.append(
                    f"{path}: knowledge_state.{concept}.{dimension} must be null or integer 0..4"
                )
    return errors


def _yaml_lines(text: str) -> list[_YamlLine]:
    lines: list[_YamlLine] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append(_YamlLine(indent=indent, content=raw.strip()))
    return lines


def _parse_block(lines: list[_YamlLine], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    if lines[index].content.startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_mapping(lines: list[_YamlLine], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ValueError(f"unexpected indentation before {line.content}")
        if line.content.startswith("- "):
            break
        key, raw_value = _split_key_value(line.content)
        index += 1
        if raw_value:
            result[key] = _parse_scalar(raw_value)
            continue
        if index < len(lines) and lines[index].indent > indent:
            result[key], index = _parse_block(lines, index, lines[index].indent)
        else:
            result[key] = {}
    return result, index


def _parse_list(lines: list[_YamlLine], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ValueError(f"unexpected indentation before {line.content}")
        if not line.content.startswith("- "):
            break

        item = line.content[2:].strip()
        index += 1
        if not item:
            if index < len(lines) and lines[index].indent > indent:
                value, index = _parse_block(lines, index, lines[index].indent)
                result.append(value)
            else:
                result.append(None)
            continue

        if ":" in item and not _is_quoted(item):
            key, raw_value = _split_key_value(item)
            value = {key: _parse_scalar(raw_value) if raw_value else {}}
            if index < len(lines) and lines[index].indent > indent:
                child, index = _parse_block(lines, index, lines[index].indent)
                if isinstance(child, dict):
                    value.update(child)
                else:
                    value[key] = child
            result.append(value)
            continue

        result.append(_parse_scalar(item))
    return result, index


def _split_key_value(content: str) -> tuple[str, str]:
    if ":" not in content:
        raise ValueError(f"expected key/value pair: {content}")
    key, value = content.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"empty key in line: {content}")
    return key, value.strip()


def _parse_scalar(value: str) -> Any:
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if _is_quoted(value):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]") and value[1:-1].strip() == "":
        return []
    if value == "{}":
        return {}
    if value == "[]":
        return []
    if value.lstrip("-").isdigit():
        return int(value)
    return value


def _is_quoted(value: str) -> bool:
    return len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}
