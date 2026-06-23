# Authentication

Better Auth (self-hosted) against Microsoft Entra ID via OIDC.

## The security boundary (invariant #1)

In TanStack Start, every `createServerFn` is an RPC endpoint reachable by a direct HTTP POST, regardless of which page rendered the UI that calls it. A `beforeLoad` route guard protects the *page experience* but does **not** stop someone hitting the server function directly. If auth lives only in `beforeLoad`, the data is exposed.

**Rule:** enforce the session check *inside every protected server function* (`auth.api.getSession({ headers })` via Better Auth middleware). Treat `beforeLoad` as a UX redirect only. This is the opposite of the Laravel mental model where route middleware protects everything behind it — do not carry that assumption over. Tests must hit server functions directly to verify this (see `frontend.md`).

## Entra ID (OIDC) wiring

- Configure Entra as a Microsoft/OIDC provider: client ID + secret + tenant ID, redirect URI pointing at the Better Auth handler, scopes `openid profile email`.
- Mount the handler at `/src/routes/api/auth/$.ts`.
- Use the `tanstackStartCookies` plugin — it must be **last** in the plugins array.
- Sessions and users live in the project's own Postgres (no per-MAU SaaS cost; data stays in `sa-east-1`).

## Future: multiple client directories

If a project later needs many client directories each with their own IdP, reach for Better Auth's SSO plugin (SAML/OIDC) before considering a managed provider (WorkOS/Clerk).
