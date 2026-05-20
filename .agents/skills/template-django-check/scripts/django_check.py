#!/usr/bin/env python3
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd=None, check=True, capture_output=True):
    print(f"Running: {' '.join(cmd)} (cwd: {cwd or '.'})")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        if capture_output:
            print(f"STDOUT:\n{e.stdout}")
            print(f"STDERR:\n{e.stderr}")
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-name", default="DJANGO_CHECK_PROJECT")
    parser.add_argument("--template-dir", default=".")
    args = parser.parse_args()

    template_path = Path(args.template_dir).resolve()

    with tempfile.TemporaryDirectory(prefix="django-check-") as tmpdir:
        project_path = Path(tmpdir) / args.project_name

        # 1. Generate project
        run(
            [
                "uv",
                "run",
                "django-admin",
                "startproject",
                "--template",
                str(template_path),
                "--extension",
                "py,yaml,md,template,dist,toml,json,css,js,dev,prod",
                "--name",
                "Justfile",
                "--exclude",
                ".env",
                "--exclude",
                ".env.local",
                "--exclude",
                ".ruff_cache",
                "--exclude",
                ".rumdl_cache",
                "--exclude",
                ".venv",
                "--exclude",
                "dev",
                "--exclude",
                "db.sqlite3",
                "--exclude",
                "node_modules",
                "--exclude",
                "tmp",
                args.project_name,
                tmpdir,
            ]
        )

        # Setup .env
        env_dist = project_path / ".env.dist"
        env_file = project_path / ".env"
        if env_dist.exists():
            text = env_dist.read_text()
            replacements = {
                "DEBUG=False": "DEBUG=True",
                "ENVIRONMENT=production": "ENVIRONMENT=development",
                "SEND_EMAILS=True": "SEND_EMAILS=False",
                "LOG_LEVEL=ERROR": "LOG_LEVEL=DEBUG",
            }
            # We want to force sqlite and locmem cache for the
            # check script to avoid needing real infrastructure
            import re

            text = re.sub(r"DB_DEFAULT_URL=.*", "DB_DEFAULT_URL=sqlite:///db.sqlite3", text)
            text = re.sub(r"CACHE_DEFAULT_URL=.*", "CACHE_DEFAULT_URL=locmemcache://", text)

            for old, new in replacements.items():
                text = text.replace(old, new)
            env_file.write_text(text)

        # Ensure Justfile has replacements if django-admin missed it
        justfile = project_path / "Justfile"
        if justfile.exists():
            text = justfile.read_text()
            text = text.replace("{{ project_name }}", args.project_name)
            text = text.replace("{{project_name}}", args.project_name)
            text = text.replace("{% templatetag openvariable %}", "{{")
            text = text.replace("{% templatetag closevariable %}", "}}")
            justfile.write_text(text)

        # 2. Setup project (install dependencies)
        run(["uv", "sync"], cwd=project_path)

        # 3. Run Django check
        print("\n--- Running python manage.py check ---")
        try:
            # The project_path is the root of the generated project.
            # manage.py is located in the root of the generated project (project_name/)
            # but startproject might have renamed it or kept it as manage.py
            # In our template, manage.py-tpl becomes manage.py in project_name/
            run(["uv", "run", "python", "manage.py", "check"], cwd=project_path)
            print("Django check passed.")
        except subprocess.CalledProcessError:
            print("\nDJANGO CHECK FAILED. Please fix the errors in the template.")
            sys.exit(1)

        # 4. Run Django migrate
        print("\n--- Running python manage.py migrate ---")
        try:
            run(["uv", "run", "python", "manage.py", "migrate"], cwd=project_path)
            print("Django migrate passed.")
        except subprocess.CalledProcessError:
            print("\nDJANGO MIGRATE FAILED. Please fix the migrations in the template.")
            sys.exit(1)

        print("\nAll Django checks and migrations passed successfully!")


if __name__ == "__main__":
    main()
