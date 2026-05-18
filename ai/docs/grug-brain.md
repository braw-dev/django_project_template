# Grug Brain Developer Philosophy

This project follows the **Grug Brain Developer** philosophy: ruthless simplicity for a company of one.

> "Grug brain developer not so smart, but grug brain developer try make up for by no over think things."
> — [grugbrain.dev](https://grugbrain.dev/)

## Core Philosophy

**Time and cognitive load are your scarcest resources. Protect them ruthlessly.**

As a solo developer or small team building a portfolio of SaaS projects, you cannot afford:

- Complex architectures
- Learning curves for new technologies
- Debugging clever code
- Maintaining abstractions that don't pull their weight
- Context switching between different tech stacks

## The Principles

### 1. Complexity Bad

**Complexity is the enemy. Fight it always.**

- Simple code that works beats clever code that might work
- If you can't explain it simply, it's too complex
- When in doubt, choose the simpler option

```python
# GOOD: Simple and obvious
def get_active_users():
    return User.objects.filter(is_active=True)

# BAD: Clever and complex
def get_active_users():
    return User.objects.filter(
        **{f"{'is' + '_' + 'active'}": True}
    )  # Why?!
```

### 2. Say No

**Default to "no" for everything.**

**Say no to features** unless they directly serve users:

- "It would be nice to have..." → No
- "Users might want..." → No (until they ask)
- "We should add..." → No (unless critical)

**Say no to abstractions** until you need them three times:

- First time: Write it inline
- Second time: Copy and paste (yes, really)
- Third time: Extract abstraction

**Say no to dependencies** unless they save significant time:

- "This package is only 500 lines..." → Write it yourself
- "This makes the code more elegant..." → No
- "This package does X, Y, and Z..." → You only need X, write it yourself

**Say no to "what if" scenarios**:

- "What if we need to scale to 1M users?" → You have 10 users
- "What if we add more payment providers?" → You have one
- "What if we need multiple databases?" → You don't

```python
# GOOD: Solve today's problem
def send_notification(user: User, message: str):
    send_email(user.email, message)

# BAD: Solving tomorrow's problems
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, user: User, message: str): pass

class EmailNotification(NotificationStrategy):
    def send(self, user: User, message: str):
        send_email(user.email, message)

class SMSNotification(NotificationStrategy):  # Not needed yet!
    def send(self, user: User, message: str):
        send_sms(user.phone, message)

class NotificationFactory:  # Definitely not needed!
    @staticmethod
    def create(notification_type: str) -> NotificationStrategy:
        if notification_type == 'email':
            return EmailNotification()
        elif notification_type == 'sms':
            return SMSNotification()
```

### 3. Code is Liability

**Every line of code is a cost, not an asset.**

- Code must be read
- Code must be understood
- Code must be maintained
- Code can have bugs
- Code needs tests

Features are assets (maybe). Code is always a cost.

**Therefore:**

- Delete code whenever possible
- Don't comment out code (delete it, Git remembers)
- Don't keep unused functions "just in case"
- The best code is no code

```python
# GOOD: Code was deleted

# BAD: Code graveyard
# def old_implementation():  # Kept "for reference"
#     pass

def _unused_helper():  # Renamed but still here
    pass

def feature_flag_maybe_someday():  # "We might need this"
    pass
```

### 4. One Stack to Rule Them All

**Don't introduce new languages or frameworks lightly.**

You're building a portfolio of projects. Each new technology:

- Has a learning curve (time cost)
- Requires context switching (cognitive cost)
- Needs separate maintenance (ongoing cost)
- Breaks knowledge transfer between projects (opportunity cost)

**This project uses:**

- Python (Django)
- TypeScript (React)
- SQL (via ORM)
- HTML/CSS

**Don't add:**

- Go "because it's faster" (Python is fast enough)
- GraphQL "because it's better" (REST works fine)
- MongoDB "because it's flexible" (PostgreSQL/SQLite work fine)
- Next.js "because of SSR" (Django does SSR)

```bash
# GOOD: Same stack everywhere
project1/  # Django + React + SQLite
project2/  # Django + React + SQLite  
project3/  # Django + React + SQLite

# BAD: Technology buffet
project1/  # Django + React + PostgreSQL
project2/  # FastAPI + Vue + MongoDB
project3/  # Rails + Svelte + MySQL
# Now you maintain 9 technologies!
```

### 5. Ship It

**Working software beats perfect plans.**

- Done is better than perfect
- Ship, measure, iterate
- If in doubt, ship the simpler version
- You can't optimize what doesn't exist

**Grug's shipping checklist:**

- [ ] Does it work?
- [ ] Is it secure?
- [ ] Can you debug it?

If yes to all three: **ship it**.

```python
# GOOD: Ship this
def calculate_total(items):
    return sum(item.price for item in items)

# BAD: Don't wait for this
def calculate_total(items, tax_rate=0, discount=None, coupon=None, 
                   loyalty_points=0, gift_card=None, promo_code=None):
    # Handling 5 features you don't have yet
    pass
```

### 6. Debugging > Cleverness

**Write code that's easy to debug, not easy to write.**

At 3am when your site is down, you need code you can understand quickly.

**Priorities:**

1. Readable - Can you understand it?
2. Debuggable - Can you trace what's happening?
3. Explicit - No hidden magic
4. Boring - Predictable behavior

**Not priorities:**

1. Elegant
2. Clever
3. Compact
4. "Pythonic" (if it sacrifices clarity)

```python
# GOOD: Obvious and debuggable
def process_payment(user, amount):
    if user.balance < amount:
        logger.error(f"Insufficient balance: user={user.id}, balance={user.balance}, amount={amount}")
        raise InsufficientFundsError(f"Balance {user.balance} < {amount}")

    user.balance -= amount
    user.save()
    logger.info(f"Payment processed: user={user.id}, amount={amount}")
    return True

# BAD: Clever and hard to debug
def process_payment(user, amount):
    return (lambda: (
        user.balance.__sub__(amount),
        user.save(),
        True
    )[-1])() if user.balance >= amount else (_ for _ in ()).throw(
        InsufficientFundsError()
    )
```

## Patterns for Grug

### Good Patterns

**Functions that do one thing:**

```python
def send_welcome_email(user):
    subject = "Welcome!"
    body = render_template('welcome_email.html', user=user)
    send_email(user.email, subject, body)
```

**Clear names that explain intent:**

```python
# GOOD
def get_unpaid_invoices_for_user(user_id):
    pass

# BAD
def get_inv(uid):
    pass
```

**Tests that document behavior:**

```python
def test_user_cannot_delete_others_posts():
    user1 = create_user()
    user2 = create_user()
    post = create_post(author=user1)

    with pytest.raises(PermissionDenied):
        delete_post(post=post, user=user2)
```

**Comments that explain "why":**

```python
# GOOD
# Round to 2 decimals to prevent floating point errors in payment processing
amount = round(amount, 2)

# BAD
# Increment counter
counter += 1  # Code already says this
```

### Bad Patterns

**Deep inheritance hierarchies:**

```python
# BAD: Inheritance chain
class Animal: pass
class Mammal(Animal): pass
class Primate(Mammal): pass
class Ape(Primate): pass
class Human(Ape): pass  # Grug confused which method where?

# GOOD: Composition
class Human:
    def __init__(self):
        self.body = Body()
        self.brain = Brain()
```

**Unnecessary abstractions:**

```python
# BAD: Generic interface for one implementation
class PaymentProcessorInterface(ABC):
    @abstractmethod
    def process(self, amount: Decimal) -> bool: pass

class StripePaymentProcessor(PaymentProcessorInterface):
    def process(self, amount: Decimal) -> bool:
        # Stripe logic

# GOOD: Just use Stripe directly
def process_payment(amount: Decimal) -> bool:
    # Stripe logic
    # If you add another processor later, refactor then
```

**Premature optimization:**

```python
# BAD: Optimizing before measuring
def get_users():
    # Complex caching, query optimization, etc.
    # For a table with 50 rows!

# GOOD: Start simple, measure, optimize if needed
def get_users():
    return User.objects.all()
```

**"Enterprise" patterns for small apps:**

```python
# BAD: Factory, Builder, Strategy for a small app
class UserFactoryBuilder:
    def __init__(self):
        self._strategies = {}

    def register_strategy(self, name, strategy): pass
    def build(self): pass
    # ... 100 lines later ...

# GOOD: Just create the damn user
def create_user(email, name):
    return User.objects.create(email=email, name=name)
```

## When Grug Unsure

Decision-making algorithm:

1. **Pick the simpler, more secure option**
   - If still unsure →

2. **Pick the option with less code**
   - If still unsure →

3. **Pick the option that's easier to delete later**
   - If still unsure →

4. **Ask the human**

## Grug's Toolbox

### Approved Complexity (Sometimes Necessary)

**Tests:** Yes, tests add complexity, but they catch bugs. Worth it.

**Type hints:** Yes, they add characters, but they catch errors. Worth it.

**Validations:** Yes, checking input is extra code, but prevents security issues. Worth it.

**Error handling:** Yes, try/except adds lines, but prevents crashes. Worth it.

### Rejected Complexity (Almost Never Necessary)

**Metaclasses:** No. Grug never understand. Magic bad.

**Decorators that modify behavior:** Use sparingly. Magic bad.

**Deep class hierarchies:** No. Composition over inheritance.

**Clever imports:** No. Explicit imports only.

**Monkeypatching:** No. Change source or find another way.

**Dynamic attribute access:** No. Explicit is better.

## Grug's Mantras

> "Complexity bad. Simple good."
>
> "Say no to almost everything."
>
> "Code is liability, not asset."
>
> "Grug use same stack for all projects."
>
> "Ship working software. Iterate."
>
> "Future Grug thank present Grug for simple code."
>
> "Debugging at 3am test of good code."
>
> "Grug not mass hysteria driven. Grug driven by mass simplicity."

## Real-World Examples

### Example 1: Notification System

**GRUG NO:** Multi-channel notification framework

- Abstract NotificationProvider interface
- EmailProvider, SMSProvider, PushProvider, SlackProvider
- NotificationFactory
- NotificationQueue with priority system
- Retry logic with exponential backoff
- Template engine for all notification types
- A/B testing framework for notifications

**GRUG YES:** Send email when needed

```python
def send_notification(user: User, message: str):
    send_mail(
        subject="Notification",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
```

When you need SMS later, add it then. Not before.

### Example 2: API Versioning

**GRUG NO:** Preemptive API versioning framework

- /api/v1/, /api/v2/, /api/v3/ structure
- Version negotiation middleware
- Deprecation warning system
- Automatic response transformation
- Version-specific serializers

**GRUG YES:** One API that works

```python
# api.py
@api.get("/posts")
def list_posts(request):
    return Post.objects.all()
```

Add versioning when you actually need to make breaking changes. Not before.

### Example 3: Configuration System

**GRUG NO:** Sophisticated config framework

- YAML config files
- Environment-specific overrides
- Config validation framework
- Dynamic config reloading
- Config versioning
- Encrypted secrets in config

**GRUG YES:** Environment variables

```python
# settings.py
import environ

env = environ.Env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
DATABASE_URL = env('DATABASE_URL')
```

Simple. Works. Done.

## Remember

**Grug brain small. Grug make code simple so Grug can understand later.**

**Future Grug thank present Grug for simple code.**

**Grug not try impress other developers. Grug try ship working software.**

**When in doubt, simplify.**

---

Based on [The Grug Brained Developer](https://grugbrain.dev/) by grugbrain.dev
