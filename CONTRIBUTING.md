# Contributing

## Development setup

Use Python 3.10 or newer, matching `pyproject.toml`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Run the checks before opening a pull request:

```bash
python -m unittest discover -s tests
python scripts/validate_workspace.py
```

The CI workflow also installs the package and runs CLI smoke checks in a temporary workspace.

## Bug reports

Include the Python version, operating system, exact command, expected result, actual result, and a minimal synthetic workspace that reproduces the issue. Remove private profiles, paper PDFs, credentials, and personal research notes before attaching files.

## Data and protocol boundaries

- Keep code identifiers, schema keys, entity names, IDs, folders, and machine-readable fields in English.
- Treat Markdown as the source of truth and preserve provenance and source locations.
- Keep proposals distinct from accepted knowledge. AI output needs human review before it becomes an accepted record.
- Do not infer implementation ability from reading or conceptual understanding.
- Never commit `.research/config/researcher-profile.yaml` or copy a real profile into `examples/`.
- Label synthetic examples clearly; do not invent scientific results or present them as verified.
- Prefer small patches. Do not overwrite accepted human notes without explicit approval.

## 贡献指南（中文）

### 环境与检查

使用 Python 3.10 或更新版本，并以 `pyproject.toml` 为准：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests
python scripts/validate_workspace.py
```

CI 还会安装项目，并在临时工作区执行 CLI 冒烟检查。

### 可复现问题报告

请提供 Python 版本、操作系统、完整命令、预期结果、实际结果，以及能够复现问题的最小合成工作区。附加文件前请移除私人画像、论文 PDF、凭据和个人研究笔记。

### 数据与协议边界

- 代码标识符、schema key、实体名、ID、文件夹名和机器可读字段使用英文。
- Markdown 是事实来源；保留 provenance 和来源位置。
- 区分待审提案与已接受知识。AI 输出须经人工审核后才能成为已接受记录。
- 不得从阅读或概念理解推断实现能力。
- 不要提交 `.research/config/researcher-profile.yaml`，也不要将真实画像复制到 `examples/`。
- 合成示例必须明确标注；不要编造科研结果或将其描述为已验证事实。
- 优先提交小改动；未经明确批准，不覆盖已接受的人工笔记。
