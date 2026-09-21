---
name: paper-reader
description: Guide a researcher through prerequisite-aware paper reading using their current knowledge state, then preserve a traceable Reading record, questions, claims, and evidence.
---

# Guided Paper Reader

Follow `.research/schema/research-protocol.md`, `.research/schema/entity-model.md`, and `.research/schema/knowledge-state.md`.

## First step: prerequisite check
Compare the paper's required concepts, methods, tasks, and mathematics with the user's Researcher Profile. Classify each as known enough, partial/review needed, or unknown/prerequisite needed.

Never equate paper reading with implementation competence.

## Stages
1. PREVIEW — title, abstract, figures, conclusion
2. STRUCTURE — problem, motivation, prior work, method, experiments, conclusion
3. DEEP_READ — section-by-section reading
4. VALIDATION — test the user's own understanding and questions
5. READING_COMMIT — persist Reading after review

## Personalization
Skip or shorten prerequisites the user already knows. Expand actual gaps. Example: conceptual Transformer understanding with no PyTorch implementation should not trigger a Transformer-from-zero lesson; implementation becomes a gap only when the target workflow needs it.

## Output
Reading record: purpose, current understanding, remaining gaps, concepts/methods, user questions, claim/evidence proposals, next actions, and knowledge-state updates.
