from __future__ import annotations
from pathlib import Path
import shutil

DIRECTORIES = (
    "papers", "concepts", "methods", "datasets", "tasks", "questions", "claims",
    "evidence", "experiments", "readings", "inbox", ".research/schema",
    ".research/config", ".research/indexes",
)
PROFILE_TEMPLATE = Path("templates/researcher-profile.yaml")
RESEARCHER_PROFILE = Path(".research/config/researcher-profile.yaml")

def init_workspace(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    created = []
    for relative in DIRECTORIES:
        path = root / relative
        if not path.exists():
            path.mkdir(parents=True)
            created.append(path)
    profile = root / RESEARCHER_PROFILE
    template = _profile_template(root)
    if not profile.exists() and template.exists():
        shutil.copyfile(template, profile)
        created.append(profile)
    return created


def _profile_template(root: Path) -> Path:
    workspace_template = root / PROFILE_TEMPLATE
    if workspace_template.exists():
        return workspace_template
    return Path(__file__).resolve().parents[2] / PROFILE_TEMPLATE
