#!/usr/bin/env bash
# Checks package interoperability after uv sync --upgrade.
# Lives in dev/ so it is excluded from generated projects.
set -euo pipefail

PASS=0
FAIL=0

check() {
    local pkg="$1"
    local version
    if version=$(uv pip show "$pkg" 2>/dev/null | awk '/^Version:/{print $2}'); then
        echo "  OK  $pkg==$version"
        PASS=$((PASS + 1))
    else
        echo "  FAIL $pkg (not installed)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== 1. Package presence ==="
PACKAGES=(
    django
    django-allauth
    django-anymail
    django-axes
    django-braces
    django-cotton
    pydantic-settings
    django-extensions
    django-filter
    django-hijack
    django-meta
    django-parler
    django-model-utils
    django-ninja
    rules
    django-structlog
    django-storages
    django-sri
    django-vite
    django-widget-tweaks
    gunicorn
    markdown
    nh3
    polar-sdk
    pillow
    typeid-python
    whitenoise
    celery
    django-celery-results
    hiredis
    httpx
    psycopg
    pydantic
    django-debug-toolbar
    factory-boy
    playwright
    ruff
    mypy
)
for pkg in "${PACKAGES[@]}"; do
    check "$pkg"
done

echo ""
echo "=== 2. Ruff lint + format ==="
if uv run ruff check --quiet && uv run ruff format --check --quiet; then
    echo "  OK  ruff"
else
    echo "  FAIL ruff"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== 3. Template generation (Ansible) ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if uv run ansible-playbook "$SCRIPT_DIR/01-test-project-template.yaml"; then
    echo "  OK  template generation"
else
    echo "  FAIL template generation"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Summary ==="
echo "  Passed: $PASS"
if [ "$FAIL" -gt 0 ]; then
    echo "  Failed: $FAIL"
    exit 1
else
    echo "  Failed: 0"
fi
