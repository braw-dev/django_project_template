# Security & Simplicity Principles

This project balances **security by default** with **radical simplicity** to enable a solo developer or small team to maintain a portfolio of SaaS projects.

## Core Philosophy

**Security is non-negotiable. Complexity is the enemy. Boring technology wins.**

Every security decision should make the system simpler, not more complex. Every simplification should maintain or improve security.

## Security Principles

### 1. Authentication & Authorization

**Use django-allauth. Period.**

- Never write custom authentication code
- MFA is enabled by default - don't disable it
- Use Django's permission system + django-guardian for row-level permissions
- Session-based auth (cookies), not tokens (unless API absolutely requires it)

```python
# GOOD: Use provided User model
from {{ project_name }}.users.models import User

def my_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('account_login')
```

```python
# BAD: Custom auth
def custom_login(request, username, password):
    # Don't do this!
    pass
```

**Human review required for:**

- Any changes to authentication/authorization logic
- Adding new login methods
- Modifying permission checks
- Changes to User model

### 2. Data Handling

Rule: **Minimize, Validate, Sanitize**

**Data Minimization:**

- Only collect data you absolutely need
- Delete data when no longer needed
- Don't log sensitive information (passwords, tokens, PII)

```python
# GOOD: Minimal data collection
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=50)

# BAD: Collecting unnecessary data
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=50)
    birth_date = models.DateField()  # Do you really need this?
    phone = models.CharField(max_length=20)  # Or this?
    address = models.TextField()  # Or this?
```

**Input Validation:**

- Validate at boundaries (forms, API endpoints)
- Use Django's built-in validators
- Trust internal code - don't over-validate between services

```python
# GOOD: Validate at boundary
class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
```

**HTML Sanitization:**

- Use `nh3` for user-submitted HTML
- Django auto-escapes in templates (don't disable it)
- Never use `mark_safe()` on user input

```python
# GOOD: Sanitize user HTML
import nh3

def clean_user_html(html: str) -> str:
    return nh3.clean(html)

# BAD: Marking user input as safe
from django.utils.safestring import mark_safe

def display_user_content(user_html):
    return mark_safe(user_html)  # XSS vulnerability!
```

### 3. Secret Management

**Environment variables only. Never in code.**

- Store secrets in `.env` file (not committed)
- Use `django-environ` to load them
- Provide `.env.dist` template with dummy values
- Never log secrets

```python
# GOOD: Using environment variables
import environ

env = environ.Env()
SECRET_KEY = env('SECRET_KEY')
DATABASE_PASSWORD = env('DATABASE_PASSWORD')

# BAD: Hardcoded secrets
SECRET_KEY = 'django-insecure-hardcoded-secret'  # Never do this!
```

### 4. Password Hashing

**Use Argon2id. It's configured by default.**

Don't change it unless you have a very good reason (and expert review).

```python
# Already configured in settings.py-tpl
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    # Fallbacks for legacy passwords
]
```

### 5. SQL Injection Prevention

**Use the ORM. Avoid raw SQL.**

```python
# GOOD: Using ORM
users = User.objects.filter(email=user_email)

# ACCEPTABLE: Parameterized queries when raw SQL is necessary
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE email = %s", [user_email])

# BAD: String formatting in SQL
cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")  # SQL injection!
```

### 6. Cross-Site Scripting (XSS) Prevention

**Django auto-escapes by default. Don't break it.**

```django
<!-- GOOD: Auto-escaped -->
<p>{{ user.comment }}</p>

<!-- BAD: Disabled escaping -->
<p>{{ user.comment|safe }}</p>

<!-- GOOD: Sanitized HTML -->
<p>{{ user.comment|nh3_clean }}</p>
```

### 7. CSRF Protection

**Django handles it. Don't disable it.**

```html
<!-- GOOD: CSRF token in forms -->
<form method="post">
    {% csrf_token %}
    ...
</form>
```

```python
# GOOD: CSRF exempt only for specific API endpoints with other auth
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only because we use API key auth
def webhook_endpoint(request):
    # Verify API key
    pass
```

### 8. HTTPS/TLS

**HTTPS everywhere in production.**

```python
# In production settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

## Simplicity Principles

### 1. "Does It Pay Rent?"

Every dependency, service, and abstraction must justify its existence.

**Good reasons to add a dependency:**

- Solves a complex problem we shouldn't implement ourselves (auth, payments)
- Saves significant development time (>8 hours)
- Security-critical functionality (crypto, password hashing)

**Bad reasons:**

- "It might be useful later"
- "It's more elegant"
- "It's best practice" (without specific benefit)

```python
# GOOD: django-allauth pays rent (saves weeks of auth dev)
INSTALLED_APPS = [
    'allauth',
    'allauth.account',
]

# BAD: Adding a package for one helper function
# Just write the helper function!
```

### 2. Monolithic First

**One codebase, one deployment, one database.**

Don't extract microservices until you have:

1. Proven scalability issues
2. Clear service boundaries
3. Team size that justifies the complexity (10+ people)

For a company of one, monolith is always the answer.

```python
# GOOD: Keep related features in one Django app
# apps/billing/
#   ├── models.py         # Customer, Subscription
#   ├── services.py       # Business logic
#   ├── views.py          # Billing views
#   └── api.py            # Billing API

# BAD: Separate billing service
# - billing-service/     # Separate deployment
# - main-app/            # Main deployment
# Now you have distributed system complexity!
```

### 3. Prefer Built-In Solutions

**Django already solved most problems.**

Before adding a package, check if Django has it built-in.

| Need | Django Built-In | Don't Add |
|------|----------------|-----------|
| Admin interface | `django.contrib.admin` | Custom admin framework |
| Forms | `django.forms` | Form library |
| ORM | `django.db.models` | SQLAlchemy |
| Auth | `django.contrib.auth` + `allauth` | Custom auth system |
| Validation | `django.core.validators` | Validation library |
| Email | `django.core.mail` | Email library |
| Pagination | `django.core.paginator` | Pagination library |

### 4. Standardization

**Same patterns everywhere.**

If you solve a problem once, solve it in the template. Every project should:

- Use the same tech stack
- Follow the same patterns
- Use the same `just` commands
- Have the same directory structure

```bash
# Every project has the same commands
just install-dev
just runserver
just test-unit
just test-e2e
just format
just migrate
```

This means:

- No context switching between projects
- Fixes in one project can be applied to all
- Onboarding is instant (same patterns everywhere)

### 5. Delete Code Aggressively

**The best code is no code.**

If something is unused:

- Delete it completely
- Don't comment it out
- Don't rename it to `_unused_function`
- Don't keep it "just in case"

Git keeps history. You can always get it back.

```python
# GOOD: Delete unused code
def active_function():
    pass

# BAD: Keeping dead code around
def active_function():
    pass

# def old_function():  # Commented out "for reference"
#     pass

def _unused_helper():  # Renamed but still here
    pass
```

## Security Checklist

Before completing any task, verify:

- [ ] **No hardcoded secrets** - Check for API keys, passwords, tokens
- [ ] **Input validated** - All user input validated at boundaries
- [ ] **SQL injection prevented** - Using ORM or parameterized queries
- [ ] **XSS prevented** - Django auto-escaping or explicit sanitization
- [ ] **CSRF protected** - Forms have `{% csrf_token %}`
- [ ] **Authentication enforced** - Login required where needed
- [ ] **Authorization checked** - Permission checks for sensitive operations
- [ ] **No OWASP Top 10 issues** - Review common vulnerabilities

## When to Request Human Review

**Always request review for:**

- Authentication/authorization changes
- Payment/billing logic
- PII handling
- Database migrations that modify existing data
- Cryptographic operations
- Permission system changes
- Security configuration changes

**Can proceed autonomously:**

- Bug fixes within existing patterns
- Adding features using established conventions
- Refactoring that doesn't change behavior
- UI/UX improvements
- Performance optimizations (if not security-related)

## Common Security Mistakes to Avoid

### 1. SQL Injection via f-strings

```python
# BAD
query = f"SELECT * FROM users WHERE email = '{email}'"

# GOOD
users = User.objects.filter(email=email)
```

### 2. XSS via mark_safe

```python
# BAD
return mark_safe(user_input)

# GOOD
return user_input  # Auto-escaped by Django
```

### 3. Hardcoded Secrets

```python
# BAD
API_KEY = "sk_live_abcd1234"

# GOOD
API_KEY = env('API_KEY')
```

### 4. Missing Authorization Checks

```python
# BAD
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()  # Anyone can delete any post!

# GOOD
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        raise PermissionDenied
    post.delete()
```

### 5. Information Disclosure in Errors

```python
# BAD
try:
    user = User.objects.get(email=email)
except User.DoesNotExist:
    return "User not found"  # Leaks whether email exists

# GOOD
try:
    user = User.objects.get(email=email)
except User.DoesNotExist:
    return "Invalid email or password"  # Generic message
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [The Grug Brained Developer](https://grugbrain.dev/)
- [Choose Boring Technology](https://boringtechnology.club/)
