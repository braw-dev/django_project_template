#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

EXTENSIONS = "py,yaml,md,template,dist,toml,json,css,js,dev,prod"
EXCLUDES = [
    ".env",
    ".env.local",
    ".ruff_cache",
    ".rumdl_cache",
    "dev",
    "dist",
    ".venv",
    "db.sqlite3",
    "node_modules",
    "tmp",
]
ENV_OVERRIDES = {
    "DEBUG": "True",
    "ENVIRONMENT": "development",
    "SEND_EMAILS": "False",
    "LOG_LEVEL": "DEBUG",
    "DB_DEFAULT_URL": "sqlite:///db.sqlite3",
}


def run(command: list[str], *, cwd: Path) -> None:
    print(f"+ {' '.join(command)}", file=sys.stderr)
    subprocess.run(command, cwd=cwd, check=True)


def replace_env_value(env_path: Path, key: str, value: str) -> None:
    lines = env_path.read_text().splitlines()
    updated_lines: list[str] = []
    replaced = False

    for line in lines:
        if line.startswith(f"{key}="):
            updated_lines.append(f"{key}={value}")
            replaced = True
        else:
            updated_lines.append(line)

    if not replaced:
        raise RuntimeError(f"Could not find {key}=... in {env_path}")

    env_path.write_text("\n".join(updated_lines) + "\n")


def build_startproject_command(
    template_root: Path, project_name: str, output_dir: Path
) -> list[str]:
    command = [
        "uv",
        "run",
        "django-admin",
        "startproject",
        f"--template={template_root}",
        "--extension",
        EXTENSIONS,
        "--name",
        "Justfile",
    ]

    for item in EXCLUDES:
        command.extend(["--exclude", item])

    command.extend([project_name, str(output_dir)])
    return command


def cleanup_generated_project(output_parent_dir: Path, generated_project_dir: Path) -> None:
    cleanup_paths = [
        output_parent_dir / "specs",
        output_parent_dir / ".specify" / "memory" / "constitution.md",
        generated_project_dir / "db.sqlite3",
    ]

    for path in cleanup_paths:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def prepare_env_file(generated_project_dir: Path) -> None:
    env_dist_path = generated_project_dir / ".env.dist"
    env_path = generated_project_dir / ".env"

    shutil.copyfile(env_dist_path, env_path)

    for key, value in ENV_OVERRIDES.items():
        replace_env_value(env_path, key, value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a disposable Django project from this template.",
    )
    parser.add_argument("--project-name", default="ci_test_project")
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    template_root = Path(__file__).resolve().parent.parent
    output_parent_dir = Path(args.output_dir).resolve()

    if output_parent_dir == template_root:
        raise RuntimeError("Refusing to write generated project into the template repository root")

    if output_parent_dir.exists() and any(output_parent_dir.iterdir()):
        raise RuntimeError(f"Output directory must be empty: {output_parent_dir}")

    output_parent_dir.mkdir(parents=True, exist_ok=True)

    run(
        build_startproject_command(template_root, args.project_name, output_parent_dir),
        cwd=template_root,
    )

    generated_project_dir = output_parent_dir / args.project_name
    cleanup_generated_project(output_parent_dir, generated_project_dir)
    prepare_env_file(generated_project_dir)

    print(output_parent_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
