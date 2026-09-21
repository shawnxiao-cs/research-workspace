from __future__ import annotations
import argparse
from pathlib import Path
from .workspace import init_workspace
from .validator import validate_workspace

def main():
    parser = argparse.ArgumentParser(prog="research-workspace")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("root", nargs="?", default=".")
    val = sub.add_parser("validate")
    val.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.command == "init":
        created = init_workspace(root)
        print(f"Initialized: {root}")
        for p in created:
            print(f"  created {p.relative_to(root)}")
        return 0
    errors = validate_workspace(root)
    if errors:
        print("Validation failed:")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"Validation passed: {root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
