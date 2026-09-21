from __future__ import annotations
from pathlib import Path
import re

_FRONTMATTER_RE = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n", re.DOTALL)

def read_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    data = {}
    for raw_line in match.group("yaml").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, text[match.end():]
