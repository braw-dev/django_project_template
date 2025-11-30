# Template Development Guide

This guide is for working on the **Django Project Template itself**, not on projects generated from it.

## Critical: Recognize Template Context

You are working on the template if you see:

- File paths with `{{ project_name }}` template variables
- Files ending in `.py-tpl`
- The `dev/` directory exists
- `AGENTS.md` describes this as a "Django Project Template"

## Template Variable Rules

### DO NOT Replace These

Django's `startproject` command will automatically replace these during project generation:

```django
{{ project_name }}      # Will become the actual project name
{% templatetag openvariable %}   # Will render as {{
{% templatetag closevariable %}  # Will render as }}
```

**Never:**

- Replace `{{ project_name }}` with a real name like `myproject`
- "Fix" template tags that look like "syntax errors"
- Remove or modify Django template syntax

**Example of CORRECT template code:**

```python
# In project_name/project_name/settings.py-tpl
ROOT_URLCONF = '{{ project_name }}.urls'

INSTALLED_APPS = [
    '{{ project_name }}.core',
    '{{ project_name }}.users',
]
```

## File Extensions

Files that will be processed by Django's template engine:

- `.py-tpl` - Python files (renamed to `.py` during generation)
- `.yaml` - YAML files
- `.md` - Markdown files
- `.json` - JSON files
- `.toml` - TOML files
- And more (see `--extension` in README.md)

## File Structure

### Template Structure

```text
django_project_template/          # Template repository root
├── project_name/                 # Source directory (double nesting intentional!)
│   ├── project_name/             # Main Django app
│   │   ├── settings.py-tpl       # Django settings
│   │   ├── urls.py-tpl           # URL configuration
│   │   └── wsgi.py-tpl           # WSGI application
│   ├── core/                     # Core app
│   ├── users/                    # Users app
│   └── manage.py-tpl             # Django management command
├── frontend/
│   └── project_name/             # Frontend source
├── dev/                          # Template development/testing tools
│   ├── 01-test-project-template.yaml
│   └── README.md
├── .claude/                      # Claude Code instructions
├── AGENTS.md                     # AI agent guide
└── README.md                     # Template documentation
```

### Generated Project Structure

```text
myproject/                        # Generated project root
├── myproject/                    # Django source
│   ├── myproject/                # Main app
│   │   ├── settings.py           # .py-tpl → .py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/
│   ├── users/
│   └── manage.py
├── frontend/
│   └── myproject/
├── .claude/                      # Claude instructions (copied)
├── AGENTS.md                     # Updated with project name
└── README.md                     # Updated with project name
```

**Note:** The `dev/` directory is excluded during generation.

## Adding New Files to Template

### 1. Determine Location

**Python/Django files:**

- Place in `project_name/project_name/<app>/`
- Use `.py-tpl` extension for files containing template variables
- Use regular `.py` for files without template variables

**Frontend files:**

- Place in `frontend/project_name/`
- Use appropriate extensions (`.js`, `.jsx`, `.tsx`, etc.)

**Templates:**

- Place in `project_name/<app>/templates/`

**Static files:**

- Place in `project_name/static/`

### 2. Use Template Variables

If the file needs to reference the project name:

```python
# In new_app/services.py-tpl
from {{ project_name }}.core.exceptions import ServiceError
from {{ project_name }}.users.models import User

def my_service():
    # Business logic
    pass
```

### 3. Update Extension List

If adding a new file type, update the `--extension` parameter in `README.md`:

```bash
--extension 'py,yaml,md,template,dist,toml,json,css,js,dev,prod,NEW_EXT'
```

## Testing Template Changes

**ALWAYS test template changes before committing.**

### Method 1: Ansible Playbook (Recommended)

```bash
uv run ansible-playbook ./dev/01-test-project-template.yaml
```

This will:

1. Generate a test project in `./tmp/`
2. Install all dependencies
3. Run migrations
4. Run tests
5. Report any errors

### Method 2: Manual Generation

```bash
cd /tmp
uv run django-admin startproject \
    --template=/path/to/django_project_template \
    --extension 'py,yaml,md,template,dist,toml,json,css,js,dev,prod' \
    --name Justfile \
    --exclude '.ruff_cache' \
    --exclude '.venv' \
    --exclude 'node_modules' \
    --exclude 'dev' \
    --exclude 'tmp' \
    test_project

cd test_project
just install-dev
just test-unit
```

### What to Verify

After generation, check:

- [ ] No `{{ project_name }}` remains in generated files
- [ ] All `.py-tpl` files were renamed to `.py`
- [ ] Imports work correctly
- [ ] Tests pass
- [ ] `just runserver` starts without errors
- [ ] No template syntax errors

## Finding Hardcoded `project_name`

Use this to find `project_name` that is NOT a template variable (needs fixing):

```bash
# In template repository
rg 'project_name' | rg -v '\{\{\s*project_name\s*\}\}'
```

This finds instances where you should have used `{{ project_name }}` but didn't.

## Common Template Development Tasks

### Adding a New Django App

1. Create directory: `project_name/<app_name>/`
2. Add files with `.py-tpl` extension
3. Use `{{ project_name }}` in imports:

   ```python
   from {{ project_name }}.core.models import BaseModel
   ```

4. Update `project_name/project_name/settings.py-tpl` INSTALLED_APPS:

   ```python
   INSTALLED_APPS = [
       ...
       '{{ project_name }}.<app_name>',
   ]
   ```

5. Test generation

### Adding a New Dependency

1. Update `project_name/pyproject.toml`
2. Document why in comments (Grug brain: does it pay rent?)
3. Test generation and verify installation

### Modifying Settings

1. Edit `project_name/project_name/settings.py-tpl`
2. Consider if setting should be environment-specific
3. Update `.env.dist` if adding new environment variables
4. Test generation

### Adding Documentation

1. Template-level docs go in root directory
2. Generated project docs go in `project_name/` (will be copied)
3. Use `{{ project_name }}` in examples where appropriate

## Template Development Checklist

Before committing template changes:

- [ ] No hardcoded `project_name` (use `{{ project_name }}`)
- [ ] File extensions added to `--extension` list if needed
- [ ] Tested with Ansible playbook
- [ ] Generated project tests pass
- [ ] Documentation updated
- [ ] AGENTS.md updated if workflow changes
- [ ] .claude/ docs updated if relevant

## Excluding Files from Generation

Update `README.md` and add to `--exclude` list:

```bash
--exclude 'dev' \
--exclude 'tmp' \
--exclude '.venv' \
--exclude 'node_modules' \
--exclude '.ruff_cache'
```

## Template Variables Reference

| Variable | Usage | Example |
|----------|-------|---------|
| `{{ project_name }}` | Project name in code | `'{{ project_name }}.urls'` |
| `{% templatetag openvariable %}` | Literal `{{` in templates | For django-cotton components |
| `{% templatetag closevariable %}` | Literal `}}` in templates | For django-cotton components |

## Debugging Template Issues

### Problem: `{{ project_name }}` appears in generated project

**Solution:** File wasn't processed by Django template engine.

- Check file extension is in `--extension` list
- Verify file isn't in `--exclude` list
- Check file path doesn't contain spaces

### Problem: Import errors in generated project

**Solution:** Missing or incorrect `{{ project_name }}` variable.

- Search for hardcoded `project_name`
- Use the ripgrep command to find issues
- Fix and test again

### Problem: Template tag syntax errors

**Solution:** Don't "fix" template tags.

- `{% templatetag openvariable %}` is valid
- These render correctly in generated projects

## Best Practices

1. **Test early, test often** - Run Ansible playbook after each significant change
2. **Keep it simple** - Don't add complexity to the template
3. **Document decisions** - Explain why you added something
4. **Follow Grug brain** - If a feature doesn't clearly serve solo developers, say no
5. **Security first** - Template should generate secure projects by default
6. **Convention over configuration** - Make good defaults, minimize config needed
