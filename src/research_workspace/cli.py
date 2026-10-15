from __future__ import annotations
import argparse
from pathlib import Path
from .workspace import init_workspace
from .validator import validate_workspace
from .profile import validate_researcher_profile
from .onboarding import LABELS, onboard, render_profile
from .profile import load_researcher_profile

def main():
    parser = argparse.ArgumentParser(prog="research-workspace")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("root", nargs="?", default=".")
    init.add_argument("--language", choices=("zh", "en"), default="zh")
    onboarding = sub.add_parser("onboard")
    onboarding.add_argument("root", nargs="?", default=".")
    onboarding.add_argument("--language", choices=("zh", "en"), default="zh")
    profile = sub.add_parser("profile")
    profile_sub = profile.add_subparsers(dest="profile_command", required=True)
    show = profile_sub.add_parser("show")
    show.add_argument("--path", default=".research/config/researcher-profile.yaml")
    show.add_argument("--language", choices=("zh", "en"), default="zh")
    show.add_argument("--verbose", action="store_true")
    val = sub.add_parser("validate")
    val.add_argument("root", nargs="?", default=".")
    val_profile = sub.add_parser("validate-profile")
    val_profile.add_argument("path", nargs="?", default=".research/config/researcher-profile.yaml")
    val_profile.add_argument("--language", choices=("zh", "en"), default="zh")
    val.add_argument("--language", choices=("zh", "en"), default="zh")
    args = parser.parse_args()
    if args.command == "init":
        root = Path(args.root).resolve()
        created = init_workspace(root)
        print(("工作空间已初始化" if args.language == "zh" else "Initialized workspace") + f": {root}")
        for p in created:
            verb = "已创建" if args.language == "zh" else "created"
            print(f"  {verb} {p.relative_to(root)}")
        return 0
    if args.command == "onboard":
        return onboard(Path(args.root).resolve(), args.language)
    if args.command == "profile":
        path = Path(args.path).resolve()
        if not path.exists():
            print(LABELS[args.language]["missing"])
            return 1
        errors = validate_researcher_profile(path)
        if errors:
            print("画像无效：" if args.language == "zh" else "Profile validation failed:")
            print("\n".join(f"- {e}" for e in errors)); return 1
        print(render_profile(load_researcher_profile(path).data, args.language, args.verbose))
        return 0
    if args.command == "validate-profile":
        path = Path(args.path).resolve()
        errors = validate_researcher_profile(path)
        if errors:
            print("画像校验失败：" if args.language == "zh" else "Profile validation failed:")
            print("\n".join(f"- {e}" for e in errors))
            return 1
        print(("画像校验通过" if args.language == "zh" else "Profile validation passed") + f": {path}")
        return 0
    root = Path(args.root).resolve()
    errors = validate_workspace(root)
    if errors:
        print("工作区校验失败：" if args.language == "zh" else "Validation failed:")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(("工作区校验通过" if args.language == "zh" else "Validation passed") + f": {root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
