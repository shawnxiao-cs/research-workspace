# Research Workspace Agent Instructions

This repository implements a local-first research workspace protocol.

## Non-negotiable rules

1. Follow `.research/schema/research-protocol.md`.
2. Treat `Markdown` as the source of truth unless a task explicitly says otherwise.
3. Never turn an AI proposal into verified research knowledge without human validation.
4. Keep user knowledge state separate from paper/method/concept facts.
5. Never collapse learning into a single score.
6. For knowledge state, distinguish `awareness`, `conceptual`, `mathematical`, `implementation`, `application`, and `research`.
7. A paper-reading event does not imply implementation skill.
8. Preserve provenance and source locations whenever possible.
9. Do not overwrite accepted human notes without explicit approval.
10. Use stable typed IDs for entities.

## Knowledge scale

```text
0 = unknown / not reached
1 = exposed / observed
2 = understood
3 = proficient / independent
4 = research-ready
```

For implementation specifically:

```text
0 = never implemented
1 = followed an implementation
2 = modified an implementation
3 = independently implemented
4 = research-ready implementation
```

## Example

A researcher can legitimately have:

```text
Transformer conceptual      = 2
Transformer implementation  = 0
```

when they can understand the paper but have not implemented Transformer in PyTorch.

## Safe workflow

```text
DISCOVER → EXTRACT → PROPOSE → VALIDATE → ACCEPT / EDIT / REJECT → COMMIT
```

Prefer small, reviewable patches over wholesale rewriting of research notes.
