from __future__ import annotations
from pathlib import Path

DIRECTORIES = (
    "papers", "concepts", "methods", "datasets", "tasks", "questions", "claims",
    "evidence", "experiments", "readings", "inbox", ".research/schema",
    ".research/config", ".research/indexes",
)

def init_workspace(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    created = []
    for relative in DIRECTORIES:
        path = root / relative
        if not path.exists():
            path.mkdir(parents=True)
            created.append(path)
    return created
