# Template E2E

Repo-top Playwright checks for the template's generated-project UI foundation.

These tests do **not** run against the template repository directly. They generate a temporary
project from the template, install its dependencies, start Django + Vite, and then run browser
checks against that generated project.

## Run

```bash
python3 e2e/run_generated_project.py
```

Keep the generated project for debugging:

```bash
python3 e2e/run_generated_project.py --keep-project
```
