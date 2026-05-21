#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def run_output(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    print(f"+ {' '.join(command)}", file=sys.stderr)
    result = subprocess.run(command, cwd=cwd, env=env, check=True, capture_output=True, text=True)
    return result.stdout.strip()


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


def seed_app_shell_session(*, cwd: Path, env: dict[str, str], project_name: str) -> dict[str, str]:
    script = f"""
import json
from allauth.account.models import EmailAddress
from allauth.mfa.models import Authenticator
from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from {project_name}.tenancy import services as tenancy_services

User = get_user_model()
user = User.objects.create_user(email='e2e@example.com', password='password123!')
other_user = User.objects.create_user(email='owner2@example.com', password='password123!')
EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
Authenticator.objects.create(user=user, type=Authenticator.Type.TOTP, data=dict(secret='totp-secret'))
team = tenancy_services.create_team(name='Acme', slug='acme', owner=user)
second_team = tenancy_services.create_team(name='Beta', slug='beta', owner=other_user)
tenancy_services.add_user_to_team(actor=other_user, team=second_team, user=user, role='member')
session = SessionStore()
session[SESSION_KEY] = str(user.pk)
session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
session[HASH_SESSION_KEY] = user.get_session_auth_hash()
session.save()
print(json.dumps(dict(session_key=session.session_key, team_slug=team.slug)))
"""
    output = run_output(["uv", "run", "python", "manage.py", "shell", "-c", script], cwd=cwd, env=env)
    output_lines = [line for line in output.splitlines() if line.strip()]
    return json.loads(output_lines[-1])


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
        session_info = seed_app_shell_session(
            cwd=django_project_dir,
            env=generated_env,
            project_name=DEFAULT_PROJECT_NAME,
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
            env={
                **os.environ,
                "E2E_BASE_URL": base_url,
                "E2E_SESSION_KEY": session_info["session_key"],
                "E2E_TEAM_SLUG": session_info["team_slug"],
            },
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
