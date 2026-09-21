#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from research_workspace.validator import validate_workspace
errors = validate_workspace(ROOT)
if errors:
    print("Validation failed:")
    for e in errors:
        print(f"- {e}")
    raise SystemExit(1)
print(f"Validation passed: {ROOT}")
