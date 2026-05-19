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
    parser.add_argument("--project-name", default="BACKPORT_TEST_PROJECT")
    parser.add_argument("--template-dir", default=".")
    parser.add_argument("--iterations", type=int, default=3)
    args = parser.parse_args()

    template_path = Path(args.template_dir).resolve()

    for i in range(args.iterations):
        print(f"\n--- Iteration {i + 1} ---")

        with tempfile.TemporaryDirectory(prefix="backport-") as tmpdir:
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

            # Setup .env and Justfile
            env_dist = project_path / ".env.dist"
            env_file = project_path / ".env"
            if env_dist.exists():
                text = env_dist.read_text()
                replacements = {
                    "DEBUG=False": "DEBUG=True",
                    "ENVIRONMENT=production": "ENVIRONMENT=development",
                    "SEND_EMAILS=True": "SEND_EMAILS=False",
                    "LOG_LEVEL=ERROR": "LOG_LEVEL=DEBUG",
                    "DB_DEFAULT_URL=postgis://{{ project_name }}:{{ project_name }}@localhost:5432/{{ project_name }}?pool=True&server_side_binding=True": "DB_DEFAULT_URL=sqlite:///db.sqlite3",  # noqa: E501
                }
                for old, new in replacements.items():
                    text = text.replace(old, new)
                env_file.write_text(text)

            # Ensure Justfile has replacements if django-admin missed it
            justfile = project_path / "Justfile"
            if justfile.exists():
                text = justfile.read_text()
                text = text.replace("{{ project_name }}", args.project_name)
                text = text.replace("{{project_name}}", args.project_name)
                # Also handle templatetags if they weren't processed
                text = text.replace("{% templatetag openvariable %}", "{{")
                text = text.replace("{% templatetag closevariable %}", "}}")
                justfile.write_text(text)

            # 2. Setup project
            run(["git", "init"], cwd=project_path)
            # Try to install minimal deps for ruff if needed, but ruff usually works standalone
            try:
                run(["uv", "sync"], cwd=project_path)
            except subprocess.CalledProcessError:
                print("uv sync failed, continuing anyway...")

            # 3. Check for lint/format issues
            format_diff = run(
                ["uv", "run", "ruff", "format", "--diff"], cwd=project_path, check=False
            ).stdout
            lint_diff = run(
                ["uv", "run", "ruff", "check", "--diff"], cwd=project_path, check=False
            ).stdout

            if not format_diff.strip() and "Would fix" not in lint_diff:
                print("No lint or format issues found in generated project.")
                # Run tests to be sure
                run(["just", "test-unit"], cwd=project_path)
                print("Tests passed.")
                if i == 0:
                    print("Already clean. Exiting.")
                    return
                print("Converged!")
                break

            print("Issues found. Requesting fixes via diff...")

            print("\n--- Ruff Format Diff ---")
            print(format_diff)
            print("\n--- Ruff Check Diff ---")
            print(lint_diff)

            # Instruct the agent:
            print(
                "\nAGENT ACTION REQUIRED: Map the above diffs back to the template files in the root repo."  # noqa: E501
            )
            print("Then this script will be re-run by the agent in the next iteration to verify.")

            # Exit to let agent work
            sys.exit(1)


if __name__ == "__main__":
    main()
