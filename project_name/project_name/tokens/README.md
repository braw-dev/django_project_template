# API Tokens

This app provides team-scoped API tokens for programmatic access.

## Security properties

- token plaintext is shown only once at creation time
- only the token secret hash is stored
- token authentication is the explicit unscoped lookup path
- a valid token sets `request.team` for the rest of the request
- token revocation and expiry are checked on every request

## Token format

Tokens look like:

```text
mst_live_<lookup><secret>
```

Where:

- `lookup` is a short indexed identifier used to find the token row
- `secret` is the high-entropy secret checked against the stored hash

## Public token identifier

Each token also has a public `token_id` based on `typeid-python`, used for API and UI references.

## API surface

- `GET /api/v1/teams/{team_slug}/tokens/`
- `POST /api/v1/teams/{team_slug}/tokens/`
- `DELETE /api/v1/teams/{team_slug}/tokens/{token_id}/`
- `GET /api/v1/tokens/me/` with `Authorization: Bearer <token>`

See `SECURITY.md` for the multi-tenancy and auth model.
