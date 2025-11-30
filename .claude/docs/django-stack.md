# Django Stack Conventions

This project uses a specific Django stack and architectural patterns. Follow these conventions for consistency across all projects.

## Architecture Overview

**Hybrid Rendering Architecture:**

- Django templates for server-rendered pages
- React/Vite for interactive components
- Progressive enhancement approach

**MVT + Services Pattern:**

- Models: Data structure (Django ORM)
- Views: Request handling
- Templates: Presentation
- Services: Business logic (write operations)
- Selectors: Data retrieval (read operations)

## Core Dependencies

| Package | Purpose | When to Use |
|---------|---------|-------------|
| `django-allauth` | Authentication (email, social, MFA) | Always (for auth) |
| `django-ninja` | REST API framework | API endpoints |
| `django-guardian` | Row-level permissions | Object-level permissions |
| `django-environ` | Environment configuration | Settings management |
| `django-cotton` | HTML components | Reusable UI components |
| `celery` + `dragonfly` | Background tasks | Async operations |
| `dragonfly` (redis alternative) | Caching | Cache expensive operations |
| `nh3` | HTML sanitization | User-submitted HTML |

## Django Principles

### 1. Use Built-In Features First

Django already solved most problems. Before adding a package or writing custom code:

1. Check Django documentation
2. Check if `django.contrib` has it
3. Check if a popular, stable package exists
4. Only then consider writing custom code

```python
# GOOD: Using Django built-ins
from django.core.paginator import Paginator
from django.core.validators import EmailValidator
from django.contrib.auth.decorators import login_required

# BAD: Custom implementations
def custom_paginator():  # Django has this!
    pass

def custom_email_validator():  # Django has this!
    pass
```

### 2. Prefer Class-Based Views for Complexity

**Function-Based Views (FBVs):** Simple, straightforward views

```python
# GOOD: Simple view as FBV
@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'posts': user_posts})
```

**Class-Based Views (CBVs):** Complex views with multiple operations

```python
# GOOD: Complex view as CBV
from django.views.generic import ListView

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related('category')
```

### 3. Use the ORM

**Always prefer ORM over raw SQL.**

```python
# GOOD: Using ORM
users = User.objects.filter(
    is_active=True,
    created_at__gte=timezone.now() - timedelta(days=30)
).select_related('profile').prefetch_related('posts')

# ACCEPTABLE: Parameterized raw SQL when ORM is insufficient
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM complex_query WHERE id = %s",
        [user_id]
    )

# BAD: Raw SQL via string formatting
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # SQL injection!
```

### 4. Use the Provided User Model

**Always use the custom User model in `users/models.py`.**

```python
# GOOD: Reference custom User model
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# ALSO GOOD: Direct import in business logic
from {{ project_name }}.users.models import User

def create_user(email: str) -> User:
    return User.objects.create_user(email=email)

# BAD: Using Django's default User
from django.contrib.auth.models import User  # Don't do this!
```

### 5. Never Write Custom Auth

**Use django-allauth. It's already configured.**

```python
# GOOD: Use allauth views
from allauth.account.views import LoginView, SignupView

# GOOD: Extend allauth forms if needed
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        # Custom logic
        return user

# BAD: Custom login view
def custom_login(request):
    # Don't reimplement auth!
    pass
```

## Services Pattern

**Business logic (write operations) lives in `services.py`.**

Services are functions that:

- Create, update, or delete data
- Contain business logic
- Raise exceptions on errors
- Return model instances or primitives

```python
# users/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from {{ project_name }}.users.models import User

@transaction.atomic
def user_create(*, email: str, name: str, password: str) -> User:
    """
    Create a new user account.

    Raises:
        ValidationError: If email already exists or validation fails
    """
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already in use")

    user = User(email=email, name=name)
    user.set_password(password)
    user.full_clean()  # Validate before saving
    user.save()

    return user

@transaction.atomic
def user_update(*, user: User, name: str = None, bio: str = None) -> User:
    """Update user profile information."""
    if name is not None:
        user.name = name
    if bio is not None:
        user.bio = bio

    user.full_clean()
    user.save()

    return user
```

**Usage in views:**

```python
from {{ project_name }}.users.services import user_create

def signup_view(request):
    if request.method == 'POST':
        try:
            user = user_create(
                email=request.POST['email'],
                name=request.POST['name'],
                password=request.POST['password']
            )
            return redirect('dashboard')
        except ValidationError as e:
            return render(request, 'signup.html', {'error': str(e)})

    return render(request, 'signup.html')
```

## Selectors Pattern

**Data retrieval (read operations) lives in `selectors.py`.**

Selectors are functions that:

- Query the database
- Return QuerySets or model instances
- Don't modify data
- Encapsulate complex queries

```python
# posts/selectors.py
from django.db.models import QuerySet, Prefetch
from {{ project_name }}.posts.models import Post

def post_list(*, author_id: int = None, published_only: bool = True) -> QuerySet[Post]:
    """
    Get list of posts with optimized queries.

    Args:
        author_id: Filter by author ID
        published_only: Only return published posts

    Returns:
        QuerySet of Post objects
    """
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')

    if published_only:
        queryset = queryset.filter(status='published')

    if author_id is not None:
        queryset = queryset.filter(author_id=author_id)

    return queryset.order_by('-created_at')

def post_get_by_slug(*, slug: str) -> Post | None:
    """Get a single post by slug."""
    return Post.objects.select_related('author').filter(slug=slug).first()
```

**Usage in views:**

```python
from {{ project_name }}.posts.selectors import post_list, post_get_by_slug

def post_list_view(request):
    posts = post_list(author_id=request.user.id)
    return render(request, 'posts/list.html', {'posts': posts})

def post_detail_view(request, slug):
    post = post_get_by_slug(slug=slug)
    if post is None:
        raise Http404
    return render(request, 'posts/detail.html', {'post': post})
```

## API Endpoints (Django Ninja)

**REST APIs use Django Ninja.**

```python
# api.py
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from {{ project_name }}.posts.models import Post
from {{ project_name }}.posts.selectors import post_list
from {{ project_name }}.posts.services import post_create

api = NinjaAPI()

class PostSchema(Schema):
    id: int
    title: str
    content: str
    author_name: str

class PostCreateSchema(Schema):
    title: str
    content: str

@api.get("/posts", response=list[PostSchema])
def list_posts(request):
    posts = post_list(published_only=True)
    return [
        {
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'author_name': p.author.name
        }
        for p in posts
    ]

@api.post("/posts", response=PostSchema)
def create_post(request, payload: PostCreateSchema):
    post = post_create(
        author=request.user,
        title=payload.title,
        content=payload.content
    )
    return {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author_name': post.author.name
    }
```

## Error Handling

### In Services

Use Django exceptions for validation and business logic errors:

```python
from django.core.exceptions import ValidationError, PermissionDenied

def post_delete(*, post: Post, user: User) -> None:
    """Delete a post. Only author can delete."""
    if post.author != user:
        raise PermissionDenied("Only author can delete post")

    post.delete()
```

### In Views

Handle exceptions and show user-friendly messages:

```python
from django.contrib import messages

def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    try:
        post_delete(post=post, user=request.user)
        messages.success(request, "Post deleted successfully")
        return redirect('post_list')
    except PermissionDenied as e:
        messages.error(request, str(e))
        return redirect('post_detail', post_id=post.id)
```

## Components (django-cotton)

**Use django-cotton for reusable HTML components.**

Components live in `components/` directory.

```html
<!-- components/button.html -->
<c-vars variant="primary" size="md" />

<button class="btn btn-{{ variant }} btn-{{ size }}" {{ attrs }}>
    <c-slot />
</button>
```

**Usage in templates:**

```html
<c-button variant="primary" size="lg" type="submit">
    Save Changes
</c-button>

<c-button variant="ghost" size="sm" @click="handleCancel">
    Cancel
</c-button>
```

## Project Structure

```text
{{ project_name }}/
├── {{ project_name }}/           # Main app (settings, urls)
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Root URL configuration
│   └── wsgi.py                   # WSGI application
├── core/                         # Shared functionality
│   ├── models.py                 # Base models
│   ├── views.py                  # Generic views
│   └── utils.py                  # Utilities
├── users/                        # User management
│   ├── models.py                 # User model
│   ├── services.py               # User business logic
│   ├── selectors.py              # User queries
│   ├── views.py                  # User views
│   └── api.py                    # User API endpoints
├── posts/                        # Example app
│   ├── models.py                 # Post, Category models
│   ├── services.py               # Post CRUD logic
│   ├── selectors.py              # Post queries
│   ├── views.py                  # Post views
│   ├── api.py                    # Post API endpoints
│   └── tests/                    # Post tests
├── components/                   # django-cotton components
│   ├── button.html
│   ├── card.html
│   └── modal.html
└── templates/                    # Django templates
    ├── base.html
    ├── posts/
    └── users/
```

## Creating New Apps

Use the provided template:

```bash
just startapp my_app
```

This creates:

```text
my_app/
├── __init__.py
├── models.py
├── services.py
├── selectors.py
├── views.py
├── api.py
├── admin.py
├── urls.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_views.py
```

## Database Migrations

**Workflow:**

1. Modify models
2. Create migration: `just makemigrations`
3. Review migration file
4. Apply: `just migrate`

**Best practices:**

- Review migrations before committing
- Never edit applied migrations
- Use data migrations for data transformations
- Keep migrations small and focused

```python
# Example data migration
from django.db import migrations

def populate_slugs(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    for post in Post.objects.all():
        if not post.slug:
            post.slug = slugify(post.title)
            post.save()

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_post_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]
```

## Testing

### Unit Tests (pytest)

```python
# tests/test_services.py
import pytest
from django.core.exceptions import ValidationError
from {{ project_name }}.users.services import user_create

@pytest.mark.django_db
def test_user_create_success():
    user = user_create(
        email='test@example.com',
        name='Test User',
        password='secure_password'
    )
    assert user.email == 'test@example.com'
    assert user.name == 'Test User'

@pytest.mark.django_db
def test_user_create_duplicate_email():
    user_create(email='test@example.com', name='User 1', password='pass')

    with pytest.raises(ValidationError):
        user_create(email='test@example.com', name='User 2', password='pass')
```

### E2E Tests (Playwright)

```typescript
// tests/e2e/tests/auth.spec.ts
import { test, expect } from '@playwright/test';

test('user can sign up', async ({ page }) => {
  await page.goto('/signup');

  await page.fill('input[name="email"]', 'newuser@example.com');
  await page.fill('input[name="password"]', 'SecurePass123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
});
```

## Common Patterns

### Pagination

```python
from django.core.paginator import Paginator

def post_list_view(request):
    posts = post_list()
    paginator = Paginator(posts, 20)  # 20 posts per page
    page = request.GET.get('page', 1)
    posts_page = paginator.get_page(page)

    return render(request, 'posts/list.html', {'posts': posts_page})
```

### Search

```python
from django.db.models import Q

def post_search(*, query: str) -> QuerySet[Post]:
    return Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).distinct()
```

### Background Tasks (Celery)

```python
# tasks.py
from celery import shared_task

@shared_task
def send_welcome_email(user_id: int):
    user = User.objects.get(id=user_id)
    # Send email
    pass

# services.py
def user_create(*, email: str, name: str, password: str) -> User:
    user = User(email=email, name=name)
    user.set_password(password)
    user.save()

    # Send welcome email asynchronously
    send_welcome_email.delay(user.id)

    return user
```

## Performance Optimization

### Use select_related and prefetch_related

```python
# GOOD: Optimized queries
posts = Post.objects.select_related('author').prefetch_related('tags')

# BAD: N+1 queries
posts = Post.objects.all()  # Will cause N+1 when accessing post.author
```

### Use only() and defer() for large models

```python
# Only fetch needed fields
users = User.objects.only('id', 'email', 'name')

# Defer large fields
posts = Post.objects.defer('content')  # Skip content field
```

### Cache expensive operations

```python
from diskcache import Cache

cache = Cache('.cache')

@cache.memoize(expire=3600)
def expensive_computation(user_id: int):
    # Expensive operation
    return result
```

## Key Takeaways

1. **Use Django's built-in features** - Most problems are already solved
2. **Services for writes, Selectors for reads** - Clear separation of concerns
3. **Validate at boundaries** - Forms, API inputs
4. **Use the ORM** - Avoid raw SQL
5. **Never write custom auth** - Use django-allauth
6. **Test business logic** - Services and selectors
7. **Keep it simple** - Boring beats clever
