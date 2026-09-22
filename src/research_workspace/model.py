from __future__ import annotations
import re
from typing import Any

KNOWLEDGE_LEVELS = {
    0: "unknown",
    1: "exposed",
    2: "understood",
    3: "proficient",
    4: "research-ready",
}

KNOWLEDGE_DIMENSIONS = (
    "awareness",
    "conceptual",
    "mathematical",
    "implementation",
    "application",
    "research",
)

def validate_knowledge_level(value: Any) -> bool:
    return value is None or (isinstance(value, int) and 0 <= value <= 4)

def validate_typed_id(value: str) -> bool:
    return bool(re.fullmatch(r"(?:PAPER|CONCEPT|METHOD|DATASET|TASK|RQ|CLAIM|EVD|EXP|READ)-\d{4}", value))
