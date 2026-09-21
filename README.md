# Research Workspace

> **A local-first research workspace that turns literature, knowledge, research questions, experiments, and evidence into persistent, traceable, and evolving research memory.**  
> **一个 Local-first（本地优先）的科研工作空间，将论文、知识、科研问题、实验与证据转化为可持续积累、可追踪、可演化的科研记忆。**

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

当前 v0.1 包含以下核心实体：

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
├── .agents/
│   └── skills/
│       ├── research-profile/
│       ├── paper-intake/
│       ├── paper-reader/
│       ├── research-question/
│       └── research-memory/
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

当前已经包含 5 个核心 Skill：

### `research-profile`

**English:** Maintains the researcher profile and knowledge-state context used for personalized research workflows.  
**中文：** 管理研究者背景、研究兴趣、学习进度和多维知识状态，为后续个性化科研工作流提供上下文。

### `paper-intake`

**English:** Turns a paper, DOI, URL, or PDF into structured research objects and proposals.  
**中文：** 将论文、DOI、URL 或 PDF 导入科研工作空间，并提取论文、概念、方法、任务等结构化信息。

### `paper-reader`

**English:** Provides prerequisite-aware, guided paper reading and produces reading records, claims, evidence, and knowledge-update proposals.  
**中文：** 根据研究者知识状态生成个性化论文阅读路线，并在阅读过程中提取阅读记录、主张、证据和知识更新候选。

### `research-question`

**English:** Creates and manages research questions, knowledge gaps, hypotheses, links, and next actions.  
**中文：** 管理科研问题、知识缺口、假设、关联论文、实验以及下一步行动。

### `research-memory`

**English:** Commits validated research knowledge into persistent local Markdown memory while preserving provenance.  
**中文：** 将经过人工确认的科研信息提交到本地 Markdown Research Memory，并保留来源与 provenance。

---

## Research Protocol | 科研工作协议

Every Skill follows the same boundary model:

每个 Skill 都遵循统一的权限边界：

| Capability | 中文 | 含义 |
|---|---|---|
| `Read` | 读取 | 可以读取指定研究实体 |
| `Propose` | 提议 | 可以生成 Proposal |
| `Modify` | 修改 | 只能修改明确授权的字段 |
| `Commit` | 提交 | 经过人工确认后才能进入正式 Research Memory |

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

## Current MVP | 当前 MVP

The current v0.1 implementation focuses on the foundation rather than autonomous research execution.

当前 v0.1 重点是**研究状态模型和科研记忆基础设施**，而不是追求完全自动化科研。

已实现：

- Researcher Profile / 研究者画像
- Multi-dimensional Knowledge State / 多维知识状态
- Paper Intake / 论文导入协议
- Prerequisite-aware Paper Reading / 前置知识感知的论文阅读
- Research Question model / 科研问题模型
- Claim + Evidence model / 主张与证据模型
- Long-term Research Memory / 长期科研记忆
- Markdown-first local storage / Markdown 本地存储
- Git / Obsidian compatibility / Git 与 Obsidian 兼容
- Basic validation and tests / 基础校验与自动化测试

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

### 1. 初始化科研工作空间 | Initialize a workspace

```bash
python3 scripts/init_workspace.py
```

### 2. 校验工作空间 | Validate the workspace

```bash
python3 scripts/validate_workspace.py
```

### 3. 运行自动化测试 | Run tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
```

### 4. 本地 CLI 使用 | Local CLI usage

无需安装 Python package 也可以直接运行：

```bash
PYTHONPATH=src python3 -m research_workspace.cli init ./my-research
PYTHONPATH=src python3 -m research_workspace.cli validate ./my-research
```

---

## Example | 示例

当前仓库提供了一个个性化科研画像示例：

```text
examples/personalized/researcher-profile-current.yaml
```

其中专门展示了一个关键场景：

> **Transformer：概念层面已经理解，但 PyTorch implementation 仍然是 0。**

这个例子说明 Knowledge State 并不是“学过 / 没学过”的二元标签，而是用于表达真实科研学习状态的多维模型。

---

## Roadmap | 后续路线

### Phase 1 — Foundation | 基础设施

- [x] Researcher Profile
- [x] Knowledge State
- [x] Research Protocol
- [x] Research Question model
- [x] Paper / Reading templates
- [x] Basic validation

### Phase 2 — Research Workflow | 科研工作流

- [ ] Real paper intake pipeline
- [ ] Guided reading workflow
- [ ] Concept / Method extraction
- [ ] Knowledge-state update workflow
- [ ] Research Question decomposition
- [ ] Claim / Evidence linking
- [ ] Obsidian export and wiki-link generation

### Phase 3 — Research Intelligence | 科研智能

- [ ] Research Radar
- [ ] Paper comparison
- [ ] Paper → Code mapping
- [ ] Evidence audit
- [ ] Experiment workflow
- [ ] Figure / visualization agent
- [ ] Reviewer agent
- [ ] Submission assistant

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
