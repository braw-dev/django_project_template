---
description: Create a test project from the template, run linting and formatting checks, and backport the changes into the template repository. Use when you need to ensure the template generates clean, formatted code.
name: template-backport
---

## Usage

Use this skill when modifying the template files to ensure that the generated project remains
compliant with linting and formatting standards (Ruff).

1. Run the backport check script:

   ```bash
   python3 .agents/skills/template-backport/scripts/backport_check.py
   ```

2. The script will generate a project, run `ruff check` and `ruff format --check`, and output the
   diffs.
3. **Analyze the diffs**: Match the generated file paths (e.g.,
   `BACKPORT_TEST_PROJECT/app/models.py`) to their source template files (e.g.,
   `project_name/app/models.py` or `project_name/app/models.py-tpl`).
4. **Apply changes**: Manually apply the minimal equivalent changes to the template files.
   **DO NOT** replace `{{ project_name }}` or other template variables with hardcoded values.
5. **Verify**: Run the script again. It will repeat the process until no differences are found.
6. **Test**: The script runs `just test-unit` in the generated project to ensure no logic was broken
   by formatting changes.

## Core Principles

- **Template Integrity**: Never hardcode the test project name into template files.
- **Minimal Edits**: Apply only what is necessary to satisfy the linter/formatter.
- **Verification**: Always regenerate and re-check. A fix in the template might lead to new
  formatting issues or broken syntax after generation.
- **Ruff is Truth**: The generated project's `ruff` output is the source of truth for template
  correctness.
