---
name: research-profile
description: Initialize or update a researcher's local research profile and per-concept knowledge state. Use when the user reports what they have studied, what they can explain, what they can implement, what they have applied, or what they can use for research.
---

# Research Profile

Follow `.research/schema/research-protocol.md` and `.research/schema/knowledge-state.md`.

## Core rule
Never collapse "studied" into "mastered". Record capability dimensions independently.

## Dimensions
Track: awareness, conceptual, mathematical, implementation, application, research.
Use 0–4 and do not guess unknown values.

- 0 = unknown / not reached
- 1 = exposed / observed
- 2 = understood
- 3 = proficient / independent
- 4 = research-ready

Implementation: 0 never implemented; 1 followed an implementation; 2 modified one; 3 independently implemented; 4 research-ready implementation.

## User-state intake
If the user says "I understand the Transformer paper but have not used PyTorch", record `conceptual: 2` and `implementation: 0` as an example, subject to the user's own assessment. Do not infer mathematical, application, or research readiness without evidence.

## Mutation
Prefer proposal → human review → commit. Preserve previous state in history when updating an existing state.

`templates/researcher-profile.yaml` is the public template. The canonical live profile path is `.research/config/researcher-profile.yaml`.
The live profile may contain personal research and learning information, so it is ignored by default.
Users may intentionally remove that path from `.gitignore` if they explicitly want to version-control their profile.

## Output
Return proposed state changes, supporting evidence, unknown dimensions, and a concise next step tied to the research goal.
