#!/usr/bin/env python3
"""Require a Krypton goal package for non-trivial code changes."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


CODE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".cts",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".json",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".mjs",
    ".mts",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".swift",
    ".ts",
    ".tsx",
    ".toml",
    ".yaml",
    ".yml",
}

CODE_FILENAMES = {
    "Dockerfile",
    "Makefile",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "requirements.txt",
    "requirements-lock.txt",
    "yarn.lock",
}

REQUIRED_FILES = ("PLAN.md", "GOAL.md", "EVIDENCE.md")

REQUIRED_PATTERNS = {
    "PLAN.md": (
        ("truth owner", re.compile(r"truth\s+owner", re.IGNORECASE)),
        ("deletion or cutover", re.compile(r"deletion|cutover|displaced\s+path", re.IGNORECASE)),
        ("evidence gate", re.compile(r"evidence\s+gate", re.IGNORECASE)),
    ),
    "GOAL.md": (
        ("truth owner/cutover instruction", re.compile(r"truth\s+owner|cutover", re.IGNORECASE)),
        ("evidence gate instruction", re.compile(r"evidence\s+gate|acceptance\s+evidence", re.IGNORECASE)),
    ),
    "EVIDENCE.md": (
        ("acceptance evidence", re.compile(r"acceptance\s+evidence", re.IGNORECASE)),
        ("verification", re.compile(r"verification|focused\s+check", re.IGNORECASE)),
    ),
}


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def changed_files(repo: Path, base_ref: str) -> list[Path]:
    output = git(repo, "diff", "--name-only", "--diff-filter=ACMR", base_ref, "HEAD")
    return [Path(line) for line in output.splitlines() if line.strip()]


def is_code_change(path: Path) -> bool:
    if not path.parts:
        return False
    if path.parts[0] == "docs":
        return False
    return path.name in CODE_FILENAMES or path.suffix in CODE_EXTENSIONS


def changed_goal_slugs(paths: list[Path], goals_dir: Path) -> list[Path]:
    slugs: set[Path] = set()
    goals_parts = goals_dir.parts
    for path in paths:
        if len(path.parts) < len(goals_parts) + 2:
            continue
        if path.parts[: len(goals_parts)] != goals_parts:
            continue
        slugs.add(Path(*path.parts[: len(goals_parts) + 1]))
    return sorted(slugs)


def validate_goal_package(repo: Path, goal_dir: Path) -> list[str]:
    errors: list[str] = []
    for filename in REQUIRED_FILES:
        path = repo / goal_dir / filename
        if not path.exists():
            errors.append(f"{goal_dir}: missing {filename}")
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in REQUIRED_PATTERNS[filename]:
            if not pattern.search(text):
                errors.append(f"{goal_dir}/{filename}: missing {label}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--goals-dir", default="docs/goals")
    parser.add_argument(
        "--require-for",
        choices=("code", "always"),
        default="code",
        help="When to require a goal package. Default: code changes only.",
    )
    args = parser.parse_args()

    repo = Path.cwd()
    goals_dir = Path(args.goals_dir)
    paths = changed_files(repo, args.base_ref)

    if not paths:
        print("No changed files.")
        return 0

    require_goal = args.require_for == "always" or any(is_code_change(path) for path in paths)
    if not require_goal:
        print("No code changes detected; Krypton goal package not required.")
        return 0

    goal_dirs = changed_goal_slugs(paths, goals_dir)
    if not goal_dirs:
        print(
            "No Krypton goal package changed. Add docs/goals/<slug>/PLAN.md, "
            "GOAL.md, and EVIDENCE.md with truth owner, deletion/cutover, "
            "and evidence gate details.",
            file=sys.stderr,
        )
        return 1

    errors: list[str] = []
    for goal_dir in goal_dirs:
        errors.extend(validate_goal_package(repo, goal_dir))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Krypton goal package validated: {', '.join(str(path) for path in goal_dirs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
