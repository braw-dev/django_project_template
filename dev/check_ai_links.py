from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_SYMLINKS = {
    Path(".claude/CLAUDE.md"): Path("../ai/docs/CLAUDE.md"),
    Path(".claude/docs"): Path("../ai/docs"),
}

CURSOR_RULES = {
    "django-stack": "django-stack.md",
    "grug-brain": "grug-brain.md",
    "security-simplicity": "security-simplicity.md",
    "template-development": "template-development.md",
    "internationalisation-first": "internationalisation-first.md",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_symlink(path: Path, expected_target: Path) -> None:
    absolute_path = REPO_ROOT / path
    if not absolute_path.is_symlink():
        fail(f"{path} must be a symlink")

    target = absolute_path.readlink()
    if target != expected_target:
        fail(f"{path} must point to {expected_target}, found {target}")

    if not absolute_path.resolve().exists():
        fail(f"{path} points to a missing target")


def check_cursor_rule(name: str, canonical_doc: str) -> None:
    cursor_rule = REPO_ROOT / ".cursor" / "rules" / f"{name}.mdc"
    if not cursor_rule.is_symlink():
        fail(f"{cursor_rule.relative_to(REPO_ROOT)} must be a symlink")
    if not cursor_rule.resolve().exists():
        fail(f"{cursor_rule.relative_to(REPO_ROOT)} points to a missing target")

    ai_rule = REPO_ROOT / "ai" / "rules" / f"{name}.mdc"
    if not ai_rule.exists():
        fail(f"ai/rules/{name}.mdc is missing")

    text = ai_rule.read_text()
    required_line = f"Apply the canonical guide in `../../ai/docs/{canonical_doc}`."
    if required_line not in text:
        fail(f"ai/rules/{name}.mdc must reference ai/docs/{canonical_doc}")


def main() -> None:
    for path, target in REQUIRED_SYMLINKS.items():
        check_symlink(path, target)

    for name, canonical_doc in CURSOR_RULES.items():
        check_cursor_rule(name, canonical_doc)

    print("AI instruction links are valid.")


if __name__ == "__main__":
    main()
