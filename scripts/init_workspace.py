#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from research_workspace.workspace import init_workspace
created = init_workspace(ROOT)
print(f"Initialized: {ROOT}")
for p in created:
    print(f"  created {p.relative_to(ROOT)}")
