# Research Workspace

> **A local-first research workspace that turns literature, knowledge, research questions, experiments, and evidence into persistent, traceable, and evolving research memory.**  
> **一个 Local-first（本地优先）的科研工作空间，将论文、知识、科研问题、实验与证据转化为可持续积累、可追踪、可演化的科研记忆。**

## Language and Documentation Policy

All code identifiers, schema keys, entity names, IDs, folder names, CLI commands, and machine-readable protocol fields stay in English. `SKILL.md` operational instructions should remain primarily in English.

User-facing responses follow the user's language: Chinese users receive Chinese responses, English users receive English responses, and mixed-language users receive the dominant language.

`README.md` is maintained as bilingual documentation: English first, followed by a complete Chinese explanation. Schema documentation may use English terminology with Chinese explanations and examples. Examples may contain Chinese natural-language research notes, but all machine-readable keys remain in English.

Learned does not imply implemented:

```yaml
Transformer:
  conceptual: 2
  implementation: 0
```

## 语言与文档政策

所有代码标识符、schema key、实体名称、ID、文件夹名称、CLI 命令以及机器可读的协议字段都保持英文。`SKILL.md` 的操作性说明应主要使用英文。

面向用户的回复遵循用户使用的语言：中文用户使用中文回复，英文用户使用英文回复，中英混合时按照主要语言回复。

`README.md` 维护为双语文档：英文在前，随后提供完整中文说明。Schema 文档可以使用英文术语，并配合中文解释和示例。示例可以包含中文自然语言科研笔记，但所有机器可读 key 必须保持英文。

Learned does not imply implemented，学过不代表已经实现：

```yaml
Transformer:
  conceptual: 2
  implementation: 0
```

## 项目简介 | Overview

**Research Workspace** is an open-source, Codex-oriented research workflow project. It is designed to help a researcher build a long-term, structured research state instead of treating each paper-reading session or AI conversation as an isolated event.

**Research Workspace** 是一个面向开源科研工作流、并针对 Codex Skill 设计的项目。它的目标不是简单地“帮你总结论文”，而是把研究者长期科研过程中产生的**论文、知识、阅读记录、研究问题、实验、证据和结论**组织起来，形成一个能够不断演化的科研状态系统。

### 我们要解决的问题 | The Problem

传统 AI 科研助手通常解决的是一个局部任务：

- 搜索论文 / Find papers
- 总结论文 / Summarize papers
- 解释论文 / Explain papers
- 生成笔记 / Generate notes
- 生成代码 / Generate code

但长期科研还存在一个更重要的问题：

> **“我作为一个研究者，现在到底知道什么、不知道什么、为什么读这篇论文、有哪些科研问题、看到过哪些证据、做过哪些实验，以及下一步为什么要做这件事？”**

Research Workspace therefore focuses on **research state and research memory** rather than only paper summarization.

因此，本项目真正关注的是：

> **研究者当前的知识状态 + 研究问题 + 证据链 + 实验状态 + 长期科研记忆。**

---

## 核心理念 | Core Philosophy

> **AI proposes. Human validates. Repository remembers.**  
> **AI 提议，人类验证，仓库记忆。**

AI-generated output is never automatically treated as verified knowledge. The workflow is:

AI 产生的内容不会自动成为“事实”或“知识”，统一经过以下流程：

```text
DISCOVER
  ↓
EXTRACT
  ↓
PROPOSE
  ↓
VALIDATE
  ↓
ACCEPT / EDIT / REJECT
  ↓
COMMIT
  ↓
RESEARCH MEMORY
```

也就是说：

```text
发现
 ↓
提取
 ↓
提出候选结论
 ↓
人工验证
 ↓
接受 / 编辑 / 拒绝
 ↓
提交到仓库
 ↓
形成长期科研记忆
```

这意味着：

- AI 可以提出 Concept / Method / Claim / Evidence / Research Question。
- 人类决定这些内容是否成立、如何修改、是否进入正式研究记录。
- Git 保留文件级历史。
- Research Memory 保留研究状态和知识演化。

---

## 核心特色 | Key Features

The following sections describe the project's design goals. Their implementation status is summarized in [Current Implementation](#current-implementation--当前实现状态); several research workflows are still plans or Skill instructions only.

以下内容描述项目设计目标。各项能力的实现状态见[当前实现状态](#current-implementation--当前实现状态)；部分科研工作流目前仍只是计划或 Skill 指令。

### 1. Researcher Profile

建立研究者自己的科研画像，包括：

- Research background / 科研背景
- Research interests / 研究兴趣
- Research goals / 科研目标
- Learning progress / 学习进度
- Knowledge state / 知识状态
- Current research questions / 当前研究问题

系统不会假设所有研究者拥有相同基础，而是根据研究者自己的状态调整后续科研工作流。

---

### 2. Multi-dimensional Knowledge State

**“学过”不等于“掌握”。**

Research Workspace does not use a single score such as “beginner / intermediate / expert”. Instead, each concept is represented by multiple independent capability dimensions:

Research Workspace 不使用一个简单的“初级 / 中级 / 高级”分数，而是分别记录：

| Dimension | 中文 | 0–4 含义 |
|---|---|---|
| `awareness` | 接触程度 | 0 未接触 → 4 研究可用 |
| `conceptual` | 概念理解 | 0 不知道 → 4 可用于科研分析 |
| `mathematical` | 数学理解 | 0 看不懂 → 4 可进行相关数学分析 |
| `implementation` | 实现能力 | 0 未实现 → 4 可独立完成科研级实现 |
| `application` | 应用能力 | 0 未应用 → 4 可用于实际研究任务 |
| `research` | 科研能力 | 0 未使用 → 4 可围绕该知识开展研究 |

统一状态定义：

```text
0 = Unknown / 未接触
1 = Exposed / 接触、了解
2 = Understood / 已理解
3 = Proficient / 熟练使用
4 = Research-ready / 达到科研使用水平
```

注意：**0–4 不是考试分数，也不是“精通程度评分”**。它表示某一个具体能力维度当前处于什么状态。

例如，一个研究者可能：

```yaml
Transformer:
  conceptual: 2
  mathematical: 1
  implementation: 0
  application: 0
  research: 0
```

这表示：

> 已经能够理解 Transformer 的核心概念，但还没有进行 PyTorch 实现，也还没有将它真正用于实际科研任务。

因此：

> **“看懂 Transformer 论文” ≠ “会 PyTorch 实现 Transformer” ≠ “能够用 Transformer 做科研”。**

这正是本项目 Knowledge State 模型需要准确表达的区别。

---

### 3. Prerequisite-aware Guided Reading

当用户获得一篇论文时，系统不会只做“论文总结”，而会先分析这篇论文依赖哪些前置知识，再与研究者自己的 Knowledge State 对照。

For example:

```text
WAVE-MAMBA
│
├── Transformer             ✓ 已有基础
├── State Space Model       ✗ 未系统学习
├── Mamba                   ✗ 未系统学习
├── Frequency Domain        ✗ 未系统学习
├── Wavelet                 ✗ 未系统学习
└── Image Reconstruction    △ 部分了解
```

系统可以据此生成个性化阅读路线，例如：

```text
SSM
 ↓
Mamba
 ↓
Frequency Domain
 ↓
Wavelet
 ↓
WAVE-MAMBA
```

不同研究者看到同一篇论文，可以得到不同的阅读路径。

---

### 4. Research Questions as the Center

The system is **question-centered**, not paper-centered.

系统不是以“论文”作为唯一中心，而是以 **Research Question（科研问题）** 组织整个研究过程：

```text
Research Question
      │
 ┌────┼────┬─────────┐
 ↓    ↓    ↓         ↓
Paper Concept Experiment Evidence
 │     │      │          │
 └─────┴──────┴──────────┘
             ↓
           Claim
             ↓
     New Research Question
```

例如：

```text
RQ-005
Mamba + Compressed Sensing
是否能够改善遥感图像重建？
```

它可以关联：

- Concepts: Mamba, SSM, Frequency Domain
- Papers: WAVE-MAMBA, ISTA-Net
- Experiments: EXP-0017
- Evidence: EVD-0042
- Claims: CLAIM-0017
- Next Research Questions

这样，论文、知识、实验和证据最终都围绕科研问题组织起来。

---

### 5. Evidence Traceability

Research Workspace distinguishes **Claim** from **Evidence**.

项目严格区分：

- **Claim / 主张**：一个可以被支持、反驳或验证的研究陈述。
- **Evidence / 证据**：来自论文、实验或其他来源的具体证据。

例如：

```text
CLAIM-0017

在当前实验设置下，Mamba-based reconstruction
取得了更高的 PSNR。

        ↑
        │ supported by
        │
EVD-0042

Source: EXP-0017
Dataset: XXX
Metric: PSNR
Result: 32.17 → 33.02
```

论文中的：

> “Our method achieves SOTA.”

不会自动被系统写成：

> “该方法客观上就是 SOTA。”

而会先记录为**作者主张（Claim Proposal）**，并保留来源位置。

---

### 6. Long-term Research Memory

The goal is not to save chat history. The goal is to save **research state**.

目标不是保存聊天记录，而是保存：

```text
我研究什么？
我已经知道什么？
我什么时候知道的？
为什么读这篇论文？
我从论文中获得了什么？
哪些问题还没有解决？
我做过哪些实验？
哪些结论有证据支持？
下一步为什么要做？
```

例如：

```text
Mamba
│
├── Concept
├── Papers
├── Methods
├── Research Questions
├── Readings
├── Evidence
├── Experiments
└── Knowledge Evolution
```

这使 Research Workspace 更像一个长期积累的 **Research Memory / 科研记忆系统**，而不是一个临时的 AI 聊天工具。

---

## 核心数据模型 | Core Data Model

下表描述目标协议中的实体。当前可运行代码主要实现研究者画像和知识状态；Paper、Reading、Research Question 只有模板与协议模型，其他实体还没有 CRUD 工作流或跨实体校验。

The table describes entities in the target protocol. The runnable code currently focuses on researcher profiles and knowledge state. Paper, Reading, and Research Question have templates and protocol documentation only; the other entities do not yet have CRUD workflows or cross-entity validation.

| Entity | 中文 | 主要作用 |
|---|---|---|
| `Paper` | 论文 | 记录论文及其元信息 |
| `Concept` | 概念 | 记录知识概念及知识关系 |
| `Method` | 方法 | 记录算法、模型、方法 |
| `Dataset` | 数据集 | 记录实验数据来源 |
| `Task` | 任务 | 记录分类、分割、重建等研究任务 |
| `Reading` | 阅读记录 | 记录某次阅读的目的、理解和问题 |
| `ResearchQuestion` | 科研问题 | 组织整个研究状态 |
| `Claim` | 研究主张 | 记录可被验证的研究陈述 |
| `Evidence` | 证据 | 记录支持/反驳 Claim 的具体证据 |
| `Experiment` | 实验 | 记录实验配置、结果和可复现信息 |

核心关系：

```text
Paper
  ↓
Reading
  ↓
Concept / Method / Claim / Evidence

Research Question
  ↓
Experiment
  ↓
Evidence
  ↓
Claim
  ↓
New Research Question
```

---

## Repository Structure | 仓库结构

```text
research-workspace/
│
├── .agents/skills/ # Codex instruction files; most are not executable workflows
│
├── .research/
│   ├── schema/
│   │   ├── entity-model.md
│   │   ├── knowledge-state.md
│   │   ├── research-protocol.md
│   │   └── research-question.md
│   ├── indexes/
│   └── config/
│
├── papers/         # 论文
├── concepts/       # 概念
├── methods/        # 方法
├── datasets/       # 数据集
├── tasks/          # 任务
├── readings/       # 阅读记录
├── questions/      # 科研问题
├── claims/         # 研究主张
├── evidence/       # 证据
├── experiments/    # 实验
├── inbox/          # 待处理输入
│
├── templates/      # Markdown / YAML 模板
├── examples/       # 示例
├── scripts/        # 初始化和验证脚本
├── src/            # Python 基础工具
├── tests/          # 自动化测试
├── AGENTS.md       # Codex / Agent 项目级约束
├── CONTRIBUTING.md # Contributor setup and data-handling rules
└── README.md
```

### 为什么不用 `01-papers`、`02-concepts`？ | Why no numeric folders?

数字顺序只是文件展示顺序，并不是研究知识模型。

The folder structure is storage organization, while relationships are represented explicitly through IDs and links. This keeps the model stable even when the UI or folder ordering changes.

也就是说：

> **Hierarchy 解决“它属于哪里”，Graph 解决“它和什么有关”。**

---

## Markdown / Git / Obsidian

Research Workspace follows a **Markdown-first, Git-native, Obsidian-compatible** approach.

项目采用：

```text
Markdown = Source of Truth
Git      = File History / Audit Trail
Obsidian = Optional Knowledge View
```

即：

- Markdown 是核心数据载体。
- Git 保存文件级历史和变更记录。
- Obsidian 用于可视化、双向链接和知识图谱浏览。

Obsidian is a **lens**, not the database and not the protocol itself.

这意味着未来即使用户不使用 Obsidian，也可以继续使用：

```text
Markdown + Git + Codex
```

---

## Codex Skills | Codex 技能

仓库包含 6 个 Codex Skill 指令文件。它们为 Codex 提供操作约束和工作流程说明；除 `research-onboarding` 使用的画像 onboarding CLI 外，它们不是本仓库可独立执行的流水线或自动化集成。

The repository contains six Codex Skill instruction files. They describe boundaries and workflows for Codex; apart from the profile onboarding CLI used by `research-onboarding`, they are not executable pipelines or automated integrations in this project.

### `research-profile`

**English:** Maintains the researcher profile and knowledge-state context used for personalized research workflows.  
**中文：** 管理研究者背景、研究兴趣、学习进度和多维知识状态，为后续个性化科研工作流提供上下文。

Implemented locally: profile validation, interactive onboarding, and profile display. Personalized paper workflows are not implemented by the CLI.

本地已实现画像校验、交互式 onboarding 和画像展示；CLI 尚未实现个性化论文工作流。

### `paper-intake`

**English:** Turns a paper, DOI, URL, or PDF into structured research objects and proposals.  
**中文：** 将论文、DOI、URL 或 PDF 导入科研工作空间，并提取论文、概念、方法、任务等结构化信息。

Current status: instruction only; there is no paper extraction or intake command.

当前状态：只有 Skill 指令，尚无论文提取或导入命令。

### `paper-reader`

**English:** Provides prerequisite-aware, guided paper reading and produces reading records, claims, evidence, and knowledge-update proposals.  
**中文：** 根据研究者知识状态生成个性化论文阅读路线，并在阅读过程中提取阅读记录、主张、证据和知识更新候选。

Current status: instruction only; there is no guided-reading execution code.

当前状态：只有 Skill 指令，尚无可执行的引导阅读代码。

### `research-question`

**English:** Creates and manages research questions, knowledge gaps, hypotheses, links, and next actions.  
**中文：** 管理科研问题、知识缺口、假设、关联论文、实验以及下一步行动。

Current status: instruction plus a template; there is no research-question management command.

当前状态：有 Skill 指令和模板，尚无科研问题管理命令。

### `research-memory`

**English:** Commits validated research knowledge into persistent local Markdown memory while preserving provenance.  
**中文：** 将经过人工确认的科研信息提交到本地 Markdown Research Memory，并保留来源与 provenance。

Current status: instruction and protocol only; validated memory commits are a human workflow, not an implemented automation.

当前状态：只有 Skill 指令和协议；经过验证的记忆提交由人执行，尚无自动化实现。

### `research-onboarding`

**English:** Documents the human-reviewed profile onboarding flow provided by the CLI.
**中文：** 说明 CLI 提供的研究者画像交互式创建与更新流程，并要求保存前由用户审核。

---

## Research Protocol | 科研工作协议

Every Skill follows the same boundary model:

每个 Skill 都遵循统一的权限边界：

| Capability | 中文 | 含义 |
|---|---|---|
| `L0 Read` | 读取 | 读取允许访问的研究实体 |
| `L1 Propose` | 提议 | 生成待审核提案 |
| `L2 Human Commit` | 人工提交 | 人工接受或编辑后再写入记录 |
| `L3 Controlled Mutation` | 受控修改 | 仅修改明确授权的字段 |

默认流程：

```text
AI
 ↓
Proposal
 ↓
Human Review
 ├── Accept
 ├── Edit
 └── Reject
 ↓
Commit
 ↓
Research Memory
```

特别规则：

- AI-generated statement cannot become verified knowledge without human review.
- AI 生成的内容不能未经审核直接变成已验证知识。
- Stable typed IDs are identity; filenames are presentation/storage.
- 稳定的类型化 ID 才是实体身份，文件名只是展示和存储形式。
- Claims retain scope and provenance.
- Claim 必须保留适用范围和来源信息。
- Evidence should retain source location where possible.
- Evidence 尽量保留页码、章节、图、表、公式、实验记录等具体来源位置。
- Research Questions are not automatically marked answered from one paper or one model output.
- 科研问题不能因为一篇论文或一次模型输出就自动标记为“已回答”。
- Accepted human notes must not be overwritten by automation without explicit acceptance.
- 已经经过人工确认的笔记不能被自动化流程静默覆盖。

完整协议见：

```text
.research/schema/research-protocol.md
```

---

## Current Implementation | 当前实现状态

The current v0.1 package is an early local foundation, not an end-to-end research system.

当前 v0.1 是早期的本地基础工具，还不是端到端科研系统。

**Implemented / 已实现**

- Profile template, interactive onboarding with preview/confirmation, profile display, and profile validation.
- Six independent knowledge dimensions; unknown assessments can remain `null`, and implementation state is never inferred from reading.
- Workspace initialization and basic Markdown frontmatter / typed-ID checks.
- Unit tests and a repository validation script.
- Markdown files remain the source of truth and can be versioned with Git. Obsidian can open Markdown files but has no dedicated integration here.

- 提供画像模板、带预览和确认的交互式 onboarding、画像展示与画像校验。
- 六个独立知识维度；未评估项可保留为 `null`，不会根据阅读经历推断实现能力。
- 支持工作区初始化，以及基础 Markdown frontmatter 和类型化 ID 检查。
- 提供单元测试和仓库验证脚本。
- Markdown 是事实来源，可由 Git 管理；Obsidian 可以打开这些文件，但本项目没有专用集成。

**Partially implemented / 部分实现**

- Paper, Reading, and Research Question templates and protocol documentation exist, but there is no intake, guided-reading, question-management, experiment, evidence-linking, or research-memory automation.
- The workspace validator checks required frontmatter field presence and ID format/prefix. It does not validate full schemas, duplicate IDs, or cross-entity references.
- Codex Skills provide instructions; they do not implement the described workflows on their own.

- Paper、Reading 和 Research Question 有模板及协议文档，但尚无论文导入、引导阅读、问题管理、实验、证据关联或科研记忆自动化。
- 工作区验证器只检查 frontmatter 必填字段是否存在以及 ID 格式/前缀；不会校验完整 schema、重复 ID 或实体间引用。
- Codex Skills 提供操作指引；仅凭指令文件并不会实现所描述的工作流。

**Planned / 计划中**

- Stronger schema and cross-entity reference integrity.
- One end-to-end, clearly synthetic research workflow.
- Better contributor onboarding and repeatable release preparation.

- 加强 schema、ID 唯一性和实体间引用完整性。
- 提供一个明确标注为合成数据的端到端科研工作流。
- 改善新贡献者上手流程和可重复的发布准备。

暂时**不做或不默认做**：

- 自动决定研究方向
- 自动宣布科研问题已经解决
- 自动把论文作者的观点当作事实
- 自动覆盖人工确认的科研笔记
- 自动生成完整论文并当作最终稿
- 自建大型论文数据库以替代 Zotero / Elicit / ResearchRabbit 等现有工具
- 强制用户使用 Obsidian

这些边界是项目设计的一部分，而不是暂时缺少的功能。

---

## Quick Start | 快速开始

### English

```bash
python3 -m pip install -e .
research-workspace init ./my-research --language en
research-workspace onboard ./my-research --language en
research-workspace profile show --path ./my-research/.research/config/researcher-profile.yaml --language en
research-workspace validate ./my-research --language en
research-workspace validate-profile ./my-research/.research/config/researcher-profile.yaml --language en
```

CLI output defaults to Chinese; use `--language en` or `--language zh` for user-facing text. On an existing profile, choose whether to edit profile details, reassess knowledge topics, or both. Reassessment can be done without re-entering background or interests. An empty topic list preserves existing topics and assessments. Quick Reassessment asks only about conceptual understanding and implementation; it proposes `null` for other dimensions and shows those changes before saving. Detailed mode offers all six dimensions. Choose **Edit** on the preview to edit one section, or **Cancel** to leave the profile untouched. The live YAML profile at `.research/config/researcher-profile.yaml` is private, local-only, and Git-ignored. Never commit it or copy it into public examples. Conceptual understanding never implies implementation ability. “Not assessed” is stored as `null`.

### 中文

先在仓库根目录安装 CLI，再初始化并通过交互问答创建或更新画像：

```bash
python3 -m pip install -e .
research-workspace init ./my-research --language zh
research-workspace onboard ./my-research --language zh
research-workspace profile show --path ./my-research/.research/config/researcher-profile.yaml --language zh
research-workspace validate ./my-research --language zh
research-workspace validate-profile ./my-research/.research/config/researcher-profile.yaml --language zh
```

CLI 默认使用中文，也可以通过 `--language en` 切换英文。已有画像可选择只更新画像信息、只重评知识主题，或两者都更新；只重评知识时无需重新填写背景和研究兴趣。主题列表留空会保留已有主题及其评估。快速重评只询问概念理解和实现能力，并提议将其他维度设为 `null`；所有提议会在保存前显示。详细模式可评估全部六个维度。预览中的“编辑”可选择单个分区修改，“取消”会保持画像原样。实时画像 `.research/config/researcher-profile.yaml` 是私密本地数据，默认由 Git 忽略；不要提交，也不要复制到公共示例。理解概念不代表具备实现能力。“尚未评估”保存为 `null`。

初始化工作区不会覆盖已有画像。`profile show` 用语义标签显示六个维度，`--verbose` 可同时查看内部值。验证失败时先修正画像，再运行工作区验证。自动化测试和仓库脚本验证：

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_workspace.py
```

---

## Example | 示例

`examples/researcher-profile.yaml` 是不对应真实研究者的合成示例，仅展示画像字段结构。不要把真实个人画像复制到公共示例目录。

`examples/researcher-profile.yaml` is a synthetic profile that does not describe a real researcher. It demonstrates field structure only. Do not copy a real personal profile into public examples.

```text
examples/researcher-profile.yaml
```

示例展示概念理解与实现能力相互独立：

> **ExampleConcept：conceptual 为 2，implementation 为 0。**

该占位概念仅用于说明 Knowledge State 不是“学过 / 没学过”的二元标签，不代表真实科研记录。

---

## Roadmap | 后续路线

### Milestone 1 — Release readiness | 发布基础

- [x] CI for the declared minimum Python version
- [x] Accurate feature-status documentation and contributor guidance
- [x] Installed-package CLI smoke coverage

已完成：按声明的最低 Python 版本运行 CI、校准功能状态和贡献文档，并覆盖安装后 CLI 冒烟检查。

### Milestone 2 — Schema integrity | Schema 完整性

- [ ] Validate complete entity schemas, ID uniqueness, and cross-entity references.

待完成：校验实体完整 schema、ID 唯一性和实体间引用。

### Milestone 3 — Synthetic end-to-end workflow | 合成端到端工作流

- [ ] Demonstrate intake through reviewed evidence and claims using clearly synthetic data.

待完成：使用明确标注的合成数据，演示从导入到人工审核证据和主张的完整流程。

### Milestone 4 — Reproducible releases | 可复现发布

- [ ] Improve first-time contributor experience and document repeatable release preparation.

待完成：改善首次贡献体验，并记录可重复的发布准备步骤。

---

## Design Goal | 设计目标

Research Workspace is not intended to replace the researcher.

本项目不是为了替代研究者，而是为了让 AI 成为一个**有边界、有上下文、有长期记忆、能够追踪证据的科研工作伙伴**。

理想的长期闭环是：

```text
Researcher Profile
        ↓
Knowledge State
        ↓
Research Question
        ↓
Literature
        ↓
Guided Reading
        ↓
Knowledge Update
        ↓
Experiment
        ↓
Evidence
        ↓
Claim
        ↓
New Research Question
        ↓
Research Memory
        ↺
```

> **From “AI helps me read papers” to “AI helps maintain my evolving research state.”**  
> **从“AI 帮我读论文”，走向“AI 帮我维护持续演化的科研状态”。**

---

## License

See `LICENSE` for the project license.
