# Production Architecture & Deployment

Deployment is opinionated and is expected to be deployed to a VPS/Dedicated server running Ubuntu 24 LTS behind a CDN. Multiple sites can be hosted on the same server.

## App Configuration

[`django-environ`](https://django-environ.readthedocs.io/en/latest/) is used to manage configuration in the `settings.py` file. To use, copy the `.env.dist` file to `.env` and update the values as needed. If local overrides are required, put them into `.env.local`.

## Production Architecture

### Server Configuration Management

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

Due to the read-heavy nature of the product we heavily use caching throughout the stack.

[Dragonfly](https://www.dragonflydb.io/) is the default Redis-compatible cache for database calls and template renders.

[Bunny](https://bunnycdn.com/) is used as a CDN for compressed & versioned static assets as well as image optimisation.

### Backups

[`borg`](https://github.com/borgbackup/borg) and [borgmatic](https://torsion.org/borgmatic/) are used for backups to [BorgBase](https://www.borgbase.com/).

### Monitoring

To catch application errors and monitor system usage we use [NewRelic](https://newrelic.com/) and their alerting capabilities.

### Containers

[Docker Hub](https://hub.docker.com/) hosts our containers and scans them for vulnerabilities.

### Password hashing

Passwords are stored and hashed using Argon2id.

### Vulnerabilities

If you discover a security vulnerability we encourage you to please disclose this responsibly to [security@{{ project_name }}](mailto:security@{{ project_name }}). We will endeavour to act quickly and reward if we can.

## Security Details

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

## Monitoring and Alerting

Both server & application monitoring and alerting are handled by [Grafana Cloud](https://grafana.com/).
