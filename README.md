# {{ project_name }}

This is an opinionated Django template focused on getting rid of the boilerplate/setup stages when writing SaaS MVPs. The aim is to start a new project with this template and go straight into writing business logic. It is designed to be production ready (secure with monitoring and backups) but also cheap to run and host.

But building is easy, getting (and retaining) customers is hard. That's why this template is also focused on including Django powered tools for support, payments marketing, translations, monitoring and more.

To get started, make sure you have Django installed (5.1 at time of writing) and run the following command (where `project_name` is the slug of your new project):

```
pipenv run django-admin startproject \
    --template=https://github.com/braw-dev/django_project_template/archive/main.zip \
    --extension 'py,yaml,md,template,toml,json' \
    --name justfile \
    --exclude '.ruff_cache' \
    --exclude 'dev' \
    project_name
```

To understand what's going on we can refer to the [Django documentation on `startproject`/`startapp`](https://docs.djangoproject.com/en/5.1/ref/django-admin/#cmdoption-startapp-template).

## Things to do in the new project

There are some tweaks that need to be done after creating a new project to get it up and running for your project.

- [ ] Configure environment variables (API keys, Debug etc.) by copying `{{ project_name }}/.env.template` to `{{ project_name }}/.env` and customizing
- [ ] Review the `{{ project_name }}/{{ project_name }}/settings.py` settings to ensure display names are correct
- [ ] Run the tests with `just test`

## What's included?

A non-exhaustive list of what is included when starting with this template:

### Development

- A custom Django user with MFA
- Increased security
  - Minimum password length increased
  - Password hashing by Argon2id
  - Subresource Integrity SHA512 hashes added to JS and CSS files
  - User submitted content sanitized via `nh3`
- Simple, environment variable driven configuration
  - Uses [`django-environ`](https://django-environ.readthedocs.io/en/latest/quickstart.html)
  - Reads a `.env` file or environment variables
  - Single `settings.py` file
- Common SaaS models & structure
  - Users live within Teams (which are Django Groups)
  - A Team can have different permissions based on what they've paid for
- Minimal external services
  - SQLite for the database (although can be changed via environment variables)
  - [Diskcache](https://pypi.org/project/diskcache/) for SSD based caching
- Lightweight API endpoints
  - Django Ninja setup with version API routes (`/api/v1/*`)
- Testing and TDD supported
  - Playwright for functional tests
  - Django native Unittest runner
  - Coverage support
- Static typing to catch bugs early
  - `mypy` with `django-stubs` for type checking
- Static assets served simply and efficiently
  - Static files served with Python via Whitenoise
  - Static files hashed (versioned) and compressed in collectstatic step
- Frontend ready to develop
  - HTMX for incremental HTML updates with fragments
  - Tailwind CSS & Daisy UI for styling
  - Re-usable HTML components using [`django-cotton`](https://django-cotton.com/)
- `justfile` for repetitive commands
  - Simply run `just` to see the targets available
- Code style enforced
  - Ruff linting and formatting built in to editor and run at commit time with pre-commit

### Marketing

- Market your service
  - Wagtail CMS for writing blog articles
  - SEO optimisations for all views with [`django-meta`](https://django-meta.readthedocs.io/en/latest/)
  - Privacy policy and Terms & Conditions pages out the box via inbuilt static pages
- Capture user interest
  - Newsletter sign-up page & components saves email to your Django database
- Support your customers
  - Embedded [Chatwoot](https://www.chatwoot.com/) for customer support (requires additional self hosting)

### Business development

- Take payments
  - Accept Stripe payments and sync with [`dj-stripe`](https://github.com/dj-stripe/dj-stripe)
- Support multiple languages
  - Using the inbuilt Django i18n framework to extract strings
  - Auto translated into different languages via DeepL and [`polygot-translator`](https://pypi.org/project/django-polyglot-translator/)
- Deploy to a VPS
  - Containerised and run via Podman & Systemctl
  - Infrastructure as code via Ansible for server setup and deployments
  - Supports multiple sites on a single VPS

These decisions are primarily based on my own experience when bootstrapping projects. I am open to improvements and suggestions or if you disagree/do things differently then please feel free to fork and make your own adjustments.

### Deployment

Deployment is also opinionated and is expected to be deployed to a VPS/Dedicated server running Ubuntu 24 LTS behind a CDN. Multiple sites can be hosted on the same server.

<!-- TODO(kisamoto): Diagram of infrastructure -->

<!-- Todo(kisamoto): Add ansible scripts for setup and deployment -->

#### Auxiliary services

This project is designed to work with [`braw-dev/django_auxiliary_services`](https://github.com/braw-dev/django_auxiliary_services).

## Example app

An example django-app is available under example_app. By default it is not registered in the `INSTALLED_APPS` section of `settings.py` however it can be added as `example_app`.

The code exists to show off structure and best practices of the different tools available in this starter template.

<!-- todo(kisamoto): add example_app -->

## Motivation

Financial freedom, living from your own companies/projects. You want to work from anywhere and be financially stable enough to support yourself (and any dependants).

You have a a long list of ideas to create micro SaaS projects and bring in some money and you know success won't happen over night. You'll need to leave your SaaS online for some time and do some marketing to attract customers. Because of this hosting should be cheap and reliable. Ideally as you add a new site, your costs won't increase.

SEO is important to help customers discover your website. You need a way to publish optimised landing pages and track their conversion rates. This will help you better understand your potential user base and what they are searching for.

Setting realistic expectations, you're not going to be the next Facebook. It's highly probable you won't even get any users. But you want to try. You believe in your ideas and want to bring them to the world. You'll be over the moon if you can reach 1'000 users.

Success to you is a project that brings in money to cover the costs of running itself and the time you invested in it. Anything more goes towards your goal of being financially independent from your projects.

Because of this you have sanity checked your business model. If your target budget is $5'000/month and you can make $5/customer, you're aiming for 1'000 customers.

You pick boring technologies. Boring technologies are the ones you know, that a lot of people know. They are mature and stable. This is not the time to be learning new things. New things require more time. They often "go wrong" as you find out their quirks. Worse, immature things likely have bugs that will hinder your progress.

You know that every project takes time and effort to build. Regardless of which idea you pick, you know there will be some repeated things you need to include: authentication, authorization, payments, documentation, support, backups etc.

Every project follows the same template. Common functionality should be ready to go in the template. You don't need context switching or the additional effort of holding many different technologies in your head at the same time. Any change in one project should be easily reproducible in another.

Despite being a solo-developer or a small (<10 people) team, you still want to offer a great experience. Clean design; clear documentation; contact details for help & support; self-service billing management - all of these are additional yet essential parts.

When things go wrong you receive an automated alert (not from a customer) and have backups to restore from. Downtime is acceptable, data-loss is not.

You respect your users privacy and security. Services are setup securely by default with regular deployments for security updates. To ensure minimal disruption you leverage static types and maintain a test suite with reasonable coverage to catch bugs before they hit production.

While you make a conscious effort to keep the number of external services low, you know this is unavoidable. To minimise maintenance effort you leverage the multi-tenancy features to share these services between your projects.

You need to understand your finances and your project demand so you build Business Intelligence dashboards that show your revenue (total and by project), your expenses (total and by project) and expected profit (before taxes). You also have graphs showing top performing landing pages, user flow and churn rate that you use to fine tune your projects.

In the end you will have a collection of projects, built on the same foundation. Some will bring in more than others. Some may not bring in anything at all. Across all of them though, you've hit your goal. Your choice now is whether to grow them more, create new projects or try to keep everything as it is.

## Development

This section contains instructions about what to do after you've started your project from this template using the `django-admin` command above.

<!-- todo(kisamoto): Full devcontainer for standardised development environments -->

### Installing requirements

#### Python backend

> **Note**: We recommend `Python3.12`

```
$ just install
```

This creates a virtual environment, installs the dependencies and installs `pre-commit`.

### Setting environment variables

Environment variables are loaded from a `.env` file.

We provide a pre-configured environment file for local development (this should **never be used in production**). We can copy the local `.env.template` file with the defaults and this can be modified by developers for their own needs.

```shell
$ # Copy local environment defaults
$ cp .env.template .env
```

All sensitive settings should be modified for use on the production environment.

```shell
$ # Collect static files for serving via Whitenoise
$ just collectstatic

$ # Run the local django development server
$ just runserver
```

### Keeping to the style guide

Code styling is enforced by [Ruff](https://docs.astral.sh/ruff/) (run as part of pre-commit and the CI/CD pipeline).

We choose to follow the [HackSoftware Django guide](https://github.com/HackSoftware/Django-Styleguide) wherever we can for the layout and structure of our code.

## Continuously integrating and deploying

As our code is hosted on Github, we leverage [Github Actions](https://github.com/features/actions).

## Production architecture

### Configuration

To make it easy to setup a server (e.g. for disaster recovery, fail-overs, future scaling etc.), we use [Ansible](https://docs.ansible.com/ansible/latest/index.html) to install OS dependencies and manage our configuration as code.

### Backend

{{ project_name }} is a Python + [Django](https://www.djangoproject.com/) application.

#### Migrations

Migrations are run as part of the automated CI/CD pipeline and thus must never be "breaking" migrations to minimize service disruption.

By this we mean we prefer to make two migrations (and releases) which may affect running code.

For example, given that we must rename a column in our database. If we simply rename the column the old code will break. If there is a delay in deploying the newer version, or we need to roll back then the old code will not be compatible with the new column name. In this case we would add a second column with the new name (copying the values from the original column). Then, in a second release we would delete the old column. Should we have to roll back our code would still function (although may be out of date - this could be rectified by copying the values from the new column to the old).

Database migrations should be repeatable (e.g. use `IF NOT EXISTS` etc.)

### Search

To make it fast and easy to find organizations we integrate with [Meilisearch](https://github.com/meilisearch/meilisearch) which indexes and searches all of our results as fast as possible.

### Caching

Due to the read-heavy nature of the product we heavy use of caching throughout the stack.

[Redis](https://redis.io/) is used for caching database calls and template renders.

[Bunny](https://bunnycdn.com/) is used as a CDN for compressed & versioned static assets as well as image optimisation.

### Backups

We use [Borg](https://www.borgbackup.org/) to backup our database and static assets.

### Monitoring

To catch application errors and monitor system usage we use [NewRelic](https://newrelic.com/) and their alerting capabilities.

### Containers

[Docker Hub](https://hub.docker.com/) hosts our containers and scans them for vulnerabilities.

### Password hashing

Passwords are stored and hashed using Argon2id.

### Vulnerabilities

If you discover a security vulnerability we encourage you to please disclose this responsibly to [security@{{ project_name }}](mailto:security@{{ project_name }}). We will endeavour to act quickly and reward if we can.

## Configuration

[`django-environ`](https://django-environ.readthedocs.io/en/latest/) is used to manage configuration in the `settings.py` file. To use, copy the `.env.template` file to `.env` and update the values as needed. If local overrides are required, put them into `.env.local`.

## Security

### Object level permissions

[`django-guardian`](https://github.com/django-guardian/django-guardian) is used for granular permissions. This includes permissions to access certain features as part of the subscribed plan. e.g. a `Premium` plan will have more permissions than a `Basic` plan.

### Authentication

[`django-allauth`](https://docs.allauth.org/en/latest/introduction/index.html) is configured for regular accounts with the following setup:

- Local accounts (no external social accounts). Chosen for speed and don't have to register any additional social accounts.
- Email addresses as username
- Login via code is enabled
- Multi-factor authentication via TOTP or Passkey

### Subresource Integrity

[SRI](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) SHA512 hashes are added to static JS and CSS resources thanks to [`django-sri`](https://github.com/RealOrangeOne/django-sri).

## Development

- [Pipenv](https://pipenv.pypa.io/en/latest/) for dependency management
- [Playwright](https://playwright.dev/) for end-to-end user tests

### Prerequisites

- [`pipenv`](https://pipenv.pypa.io/en/latest/) for python dependency management
- [`entr`](https://github.com/eradman/entr) for hot reloading tests (`just test-watch`)
- [`rg`](https://github.com/BurntSushi/ripgrep) for finding the python and html files suitable for hot reloading

### Setup

1. Clone repo
1. `just install` (this will setup a virtual environment and install dependencies)

### Debugging

- [`debug-toolbar`](https://github.com/jazzband/django-debug-toolbar) for SQL query analysis

### Linting & Formatting

[`ruff`](https://docs.astral.sh/ruff/) is used to format (drop in replacement for `black`) and lint code (run as part of a `pre-commit` hook).

### Test Driven Development (TDD)

To practice TDD with this, the best way is:

1. Write a behaviour test that uses Playwright to simulate user behaviour
1. [optional] Debug Playwright tests by appending `PWDEBUG=1` to command to run tests

#### Models

Use [factory boy](https://github.com/FactoryBoy/factory_boy) to make it easier to test models.

#### Testing Best Practices

_todo(kisamoto)_

## Backups

[`borg`](https://github.com/borgbackup/borg) and [borgmatic](https://torsion.org/borgmatic/) are used for backups to [BorgBase](https://www.borgbase.com/).

### Database

_todo(kisamoto)_

## Monitoring and alerting

Both server & application monitoring and alerting are handled by [Grafana Cloud](https://grafana.com/).

## Recommendations & best practices

Follow the [Hack Django Style guide](https://github.com/HackSoftware/Django-Styleguide).

### Sanitise user input

Use [`nh3`](https://github.com/messense/nh3) to sanitise user input as soon as it is received.

### Use the debug toolbar (only in development)

## How to use this template

```
pipenv run django-admin startproject \
    --template=django_project_template \
    --extension 'py,yaml,md,template,toml,json' \
    --name justfile \
    --exclude '.ruff_cache' \
    --exclude 'dev' \
    {{ project_name }} {{ path }}
```

### Developing on the template

If developing on the template directly, need to be able to quickly use the template to see what the output looks like. To do this, ansible playbooks are provided.

_Note: Will need to have `pipenv` installed and do a `pipenv install --dev`_

```
pipenv run ansible-playbook ./dev/01-test-project-template.yaml
```

This will automatically create a new django project using this template in a temporary directory.

---

If in doubt, check [awesome django](https://github.com/wsvincent/awesome-django) for libraries.

Always remember the [grug developer](https://grugbrain.dev/).

---

- [Django for startup founders](https://alexkrupp.typepad.com/sensemaking/2021/06/django-for-startup-founders-a-better-software-architecture-for-saas-startups-and-consumer-apps.html)

## Todo

Additional things to do:

- [ ] Development in a dev container that's suitable for Mac and Linux
- [ ] Finish implementing [logging and metrics capturing](https://rafed.github.io/devra/posts/cloud/django-mlt-observability-with-opentelemetry/) to Grafana
- [ ] Example application demonstrating what it can do and how to use the installed Django apps
