---
name: paper-intake
description: Intake a paper from a PDF, DOI, URL, citation, or advisor assignment into a local research workspace while preserving provenance and distinguishing author claims from verified evidence.
---

# Paper Intake

Follow `.research/schema/research-protocol.md` and `.research/schema/entity-model.md`.

## Inputs
PDF, DOI/URL, BibTeX/citation, advisor assignment, or existing Paper ID.

## Read
Researcher Profile, Knowledge State, Research Questions, and existing Papers for deduplication and relevance.

## Proposals
Paper, Concept, Method, Dataset, Task, Claim, Evidence, Research Question.

All extracted statements remain proposals until review.

## Evidence
Preserve page/section/figure/table/equation where possible. Distinguish author claim, observed result, implementation detail, and interpretation. Never turn "the authors report SOTA" into an unqualified system fact.

## Mutation
Never overwrite accepted human notes. Commit only after human acceptance/editing.
