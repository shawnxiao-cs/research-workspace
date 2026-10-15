---
name: research-onboarding
description: Guide a researcher through creating or updating the local YAML profile with explicit review and confirmation.
---

# Research Onboarding

Follow `.research/schema/research-protocol.md`, `.research/schema/knowledge-state.md`, and the `research-profile` skill for profile semantics and validation.

## Responsibilities

- Collect researcher background, stage, interests, goals, learning sources, and self-assessed topic dimensions through the CLI.
- Keep the canonical YAML profile at `.research/config/researcher-profile.yaml`.
- Show a readable preview and require explicit confirmation before writing.
- Offer Quick Assessment for conceptual understanding and implementation, with an optional detailed assessment of all six dimensions.
- Confirm parsed topic names and reject topic lists entered as the academic/professional stage.
- For an existing profile, offer a knowledge-only reassessment route; an empty topic list preserves current topics and assessments.
- On preview edits, let the researcher select a single profile section to revisit.
- Preserve unrelated profile fields and prior history. Record changes only for previously assessed knowledge values, using `user_self_report` provenance.
- Never infer implementation from reading, courses, theory, or conceptual understanding.

## Workflow

Use `research-workspace onboard --language zh|en`, inspect the preview, then confirm, edit, or cancel. The profile remains local and Git-ignored by default. Refer to schema documentation for field meanings; do not duplicate the full schema here.
