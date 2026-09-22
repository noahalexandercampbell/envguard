from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from envguard.loader import default_paths, load_env_files
from envguard.models import diff_env
from envguard.profile import Profile
from envguard.reporter import render_diff_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="envguard")
    subparsers = parser.add_subparsers(dest="command")

    check = subparsers.add_parser("check")
    check.add_argument("--file", default=None, type=Path)
    check.add_argument("--profile", required=True, type=Path)
    check.add_argument("--json", action="store_true")

    diff = subparsers.add_parser("diff")
    diff.add_argument("--file", default=None, type=Path)
    diff.add_argument("--profile", required=True, type=Path)
    diff.add_argument("--json", action="store_true")

    merge = subparsers.add_parser("merge")
    merge.add_argument("--base", required=True, type=Path)
    merge.add_argument("--overlay", required=True, type=Path)
    merge.add_argument("--destination", required=True, type=Path)
    merge.add_argument("--profile", required=True, type=Path)
    merge.add_argument("--json", action="store_true")

    return parser


def load_profile(path: Path) -> Profile:
    with path.open("r", encoding="utf-8") as file:
        if path.suffix.lower() in (".yml", ".yaml"):
            import yaml
            payload = yaml.safe_load(file)
        else:
            import json
            payload = json.load(file)
    return Profile.from_dict(payload)


def _resolve_file(file: Path | None) -> list[Path]:
    if file is not None:
        return [file]
    return default_paths()


def handle_check(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    env = load_env_files(_resolve_file(args.file))
    diff = diff_env(env, profile)
    if args.json:
        print(json.dumps({
            "missing": diff.missing,
            "extra": diff.extra,
            "blank": diff.blank,
        }))
    else:
        print(render_diff_table(diff))
    return 1 if (diff.missing or diff.extra or diff.blank) else 0


def handle_diff(args: argparse.Namespace) -> int:
    return handle_check(args)


def handle_merge(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    base_env = load_env_files([args.base])
    overlay_env = load_env_files([args.overlay])
    merged = {**base_env, **overlay_env}
    diff = diff_env(merged, profile)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    with args.destination.open("w", encoding="utf-8") as file:
        for key, value in merged.items():
            file.write(f"{key}={value}\n")
    if args.json:
        print(json.dumps({
            "missing": diff.missing,
            "extra": diff.extra,
            "blank": diff.blank,
            "destination": str(args.destination),
        }))
    else:
        print(render_diff_table(diff))
    return 1 if (diff.missing or diff.extra or diff.blank) else 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        return handle_check(args)
    if args.command == "diff":
        return handle_diff(args)
    if args.command == "merge":
        return handle_merge(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
