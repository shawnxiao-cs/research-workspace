# Entity Model v0.1

## Knowledge objects
Paper, Concept, Method, Dataset, Task

## Inquiry objects
Research Question, Claim, Evidence

## Activity objects
Reading, Experiment

## Typed IDs
PAPER-0001, CONCEPT-0001, METHOD-0001, DATASET-0001, TASK-0001, RQ-0001, CLAIM-0001, EVD-0001, EXP-0001, READ-0001

IDs are identity; filenames are presentation/storage.

## Common metadata
id, type, status, created_at, updated_at, provenance

## Core relations

```text
Paper --proposes--> Method
Paper --uses--> Dataset
Paper --studies--> Concept
Paper --addresses--> Task
Paper --contains--> Evidence
Method --uses--> Concept
Method --applied_to--> Task
ResearchQuestion --investigates--> Method
ResearchQuestion --informed_by--> Paper
ResearchQuestion --tested_by--> Experiment
ResearchQuestion --supported_by--> Evidence
Experiment --uses--> Method
Experiment --uses--> Dataset
Experiment --produces--> Evidence
Reading --reads--> Paper
Reading --updates--> Concept
Reading --raises--> ResearchQuestion
```
