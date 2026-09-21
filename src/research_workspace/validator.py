from __future__ import annotations
from pathlib import Path
from .frontmatter import read_frontmatter
from .model import validate_typed_id

ENTITY_DIRS = {
    "papers": "PAPER", "concepts": "CONCEPT", "methods": "METHOD", "datasets": "DATASET",
    "tasks": "TASK", "questions": "RQ", "claims": "CLAIM", "evidence": "EVD",
    "experiments": "EXP", "readings": "READ",
}
REQUIRED_FIELDS = ("id", "type", "status", "created_at", "updated_at", "provenance")

def validate_workspace(root: Path):
    errors = []
    for directory, prefix in ENTITY_DIRS.items():
        base = root / directory
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            data, _ = read_frontmatter(path)
            if not data:
                errors.append(f"{path}: missing YAML frontmatter")
                continue
            for field in REQUIRED_FIELDS:
                if field not in data:
                    errors.append(f"{path}: missing field {field}")
            entity_id = data.get("id")
            if entity_id and not validate_typed_id(entity_id):
                errors.append(f"{path}: invalid typed id {entity_id}")
            if entity_id and not entity_id.startswith(prefix + "-"):
                errors.append(f"{path}: expected id prefix {prefix}")
    return errors
