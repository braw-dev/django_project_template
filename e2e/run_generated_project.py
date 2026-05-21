#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

DEFAULT_PROJECT_NAME = "ci_test_project"
DEFAULT_HOST = "127.0.0.1"


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    print(f"+ {' '.join(command)}", file=sys.stderr)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def start(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.Popen[str]:
    print(f"+ {' '.join(command)}", file=sys.stderr)
    return subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        text=True,
    )


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((DEFAULT_HOST, 0))
        return int(sock.getsockname()[1])


def wait_for_http(url: str, *, timeout_seconds: int = 90) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url) as response:  # noqa: S310
                if response.status < 500:
                    return
        except Exception:
            time.sleep(0.5)
    raise RuntimeError(f"Timed out waiting for {url}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run repo-top Playwright checks against a generated project.")
    parser.add_argument("--keep-project", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    temp_root = Path(tempfile.mkdtemp(prefix="template-e2e-"))
    generated_project_root = temp_root
    django_port = get_free_port()
    base_url = f"http://{DEFAULT_HOST}:{django_port}"
    django_project_dir = generated_project_root / DEFAULT_PROJECT_NAME
    frontend_dir = generated_project_root / "frontend" / DEFAULT_PROJECT_NAME
    e2e_dir = repo_root / "e2e"
    processes: list[subprocess.Popen[str]] = []
    generated_env = {
        **os.environ,
        "CACHE_DEFAULT_URL": "locmemcache://",
        "DEBUG": "False",
    }

    try:
        run(
            [
                "python3",
                "dev/create_test_project.py",
                "--project-name",
                DEFAULT_PROJECT_NAME,
                "--output-dir",
                str(generated_project_root),
            ],
            cwd=repo_root,
        )
        run(["uv", "sync"], cwd=generated_project_root, env=generated_env)
        run(["pnpm", "install", "--frozen-lockfile"], cwd=frontend_dir)
        run(["pnpm", "build"], cwd=frontend_dir)
        run(["pnpm", "install", "--frozen-lockfile"], cwd=e2e_dir)
        run(["pnpm", "playwright", "install", "chromium"], cwd=e2e_dir)
        run(
            ["uv", "run", "python", "manage.py", "migrate", "--noinput"],
            cwd=django_project_dir,
            env=generated_env,
        )
        run(
            ["uv", "run", "python", "manage.py", "collectstatic", "--noinput"],
            cwd=django_project_dir,
            env=generated_env,
        )

        processes.append(
            start(
                ["uv", "run", "python", "manage.py", "runserver", f"{DEFAULT_HOST}:{django_port}"],
                cwd=django_project_dir,
                env=generated_env,
            )
        )

        wait_for_http(base_url)

        run(
            ["pnpm", "playwright", "test"],
            cwd=e2e_dir,
            env={**os.environ, "E2E_BASE_URL": base_url},
        )
        return 0
    finally:
        for process in reversed(processes):
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
        if args.keep_project:
            print(generated_project_root)
        else:
            shutil.rmtree(generated_project_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
