---
name: zapad-js-stack
description: The canonical TypeScript web stack — TanStack Start on AWS serverless (Lambda), Prisma + Postgres, Better Auth, MUI. Use this skill whenever scaffolding a new web project, choosing a tool for any layer of the stack, setting up a repo, writing server functions, designing the Prisma schema, wiring auth, or configuring the AWS deploy. Apply it even when the user doesn't name the stack explicitly but is clearly building a new TypeScript/React app, asking "what should I use for X", or making an architecture decision — default to these choices and flag deviations rather than silently picking something else.
---

# Zapad JS Stack Architecture

This is the house stack for new TypeScript web apps. It optimizes for a single developer or small team shipping B2B internal and client-facing tools fast, on AWS serverless, with end-to-end type safety and no separate API tier to maintain.

When building in this stack, **default to every choice below.** If a project's requirements genuinely conflict with a choice, say so explicitly and explain the trade-off — don't quietly substitute a different tool.

This file is the index: the manifest and the non-negotiable invariants live here and are always in play. Deeper per-layer detail lives in `references/` — read the relevant file when you start working on that layer.

## The manifest

| Layer | Choice | Notes |
|---|---|---|
| Language | TypeScript | strict mode on |
| Frontend framework | React | |
| App framework | TanStack Start | Nitro server engine; TanStack Router + Query come bundled |
| Runtime | Node.js 24 | Lambda runtime `nodejs24.x` / `NODEJS_24_X`; LTS through Apr 2028. **Node 20 is EOL on Lambda (Apr 30, 2026) — do not use** |
| Package manager | pnpm | |
| Styling | Tailwind CSS | |
| Components | MUI | |
| API layer | Colocated server functions | `createServerFn` — **no separate API tier** |
| Validation | Zod | single source of truth for inputs, forms, env |
| ORM | Prisma 7 | `compilerBuild = "small"`, singleton client |
| Database | PostgreSQL | RDS `db.m7g.large` Multi-AZ, `sa-east-1`, behind RDS Proxy |
| Auth | Better Auth | self-hosted, Entra ID (OIDC) |
| Forms | TanStack Form | Zod validators |
| Lint / format | Biome | all-in-one, replaces ESLint + Prettier |
| Testing | Vitest + Playwright | unit + e2e |
| Compute | AWS Lambda | arm64/Graviton, ZIP package; behind CloudFront + Function URL/API Gateway |
| IaC / deploy | SST | `TanStackStart` component |
| Email | Amazon SES | SPF/DKIM/DMARC configured |
| Background jobs | AWS-native | SQS + EventBridge (cron via scheduled rules) |
| File storage | S3 | linked via SST |
| Realtime | none by default | add only if a project needs it |

## Non-negotiable invariants

These rules aren't obvious and cause real bugs or security holes when violated. Keep them in mind on every task; each links to the reference with the worked detail.

1. **Auth lives inside server functions, not routes.** Every `createServerFn` is a directly-callable RPC endpoint; a `beforeLoad` guard protects only the page, not the data. Check the session inside every protected server function and treat `beforeLoad` as a UX redirect. This is the opposite of the Laravel route-middleware model. → `references/auth.md`
2. **Zod is the single source of truth.** One schema per entity feeds the server-fn input validator, TanStack Form, and env parsing; infer types with `z.infer`, never duplicate. → `references/data.md`
3. **Prisma on Lambda = singleton client + RDS Proxy + `compilerBuild = "small"`.** The ORM ships inside the SSR Lambda, on every page's cold-start path. → `references/data.md`
4. **One Lambda, colocated.** The SSR app plus all server functions are a single Lambda behind CloudFront; no separate API tier until a second consumer (mobile, public API, webhooks) appears. → `references/deploy.md`
5. **Explicit `aws-lambda` Nitro preset; arm64 + ZIP; stream only via Function URL.** The default `node-server` preset fails on Lambda; SnapStart doesn't support Node, so the cold-start posture is arm64 + small bundle. → `references/deploy.md`

## Reference files

Read the one matching the layer you're touching:

- `references/frontend.md` — TanStack Start / Router / Query patterns, MUI + Tailwind boundaries, TanStack Form, Biome.
- `references/data.md` — Prisma (client, RDS Proxy, schema, migrations, query conventions), Zod-as-source-of-truth, Postgres/RDS.
- `references/auth.md` — Better Auth + Entra ID (OIDC) wiring and the server-function security boundary.
- `references/deploy.md` — Lambda compute posture, Nitro preset, streaming, SST + resource linking, the colocated model, region.
- `references/services.md` — Email (SES), background jobs (SQS + EventBridge), file storage (S3), realtime.

## Scaffolding a new project

Set a fresh app up in this order (pull the matching reference at each step):

1. `pnpm create @tanstack/start` — select **Nitro** as the deploy adapter. (`references/deploy.md`)
2. Add Tailwind + MUI; configure Biome (`biome.json`); enable TS strict. (`references/frontend.md`)
3. Add Prisma 7 with `compilerBuild = "small"`; define the schema; set up `prisma migrate`. (`references/data.md`)
4. Add Better Auth with the `tanstackStartCookies` plugin and the Entra OIDC provider; mount the handler route; write the server-function auth middleware. (`references/auth.md`)
5. Establish the Zod-schema-per-entity convention feeding server-fn inputs and TanStack Form. (`references/data.md`)
6. Configure the Nitro `aws-lambda` preset; write the SST config using the `TanStackStart` component; link S3, RDS Proxy, and SES. (`references/deploy.md`)
7. Set up Vitest + Playwright with a smoke test of the auth flow. (`references/frontend.md`)

Confirm the AWS region is `sa-east-1` and the DB sits behind RDS Proxy before the first deploy.

## Deliberately deferred (decide per project)

Not pinned yet — pick when a project needs it, then consider adding the choice back into this skill:

- **Observability** — error tracking + tracing (Sentry is the obvious default; not yet locked).
- **Payments** — only if a project sells something (Stripe is the default candidate).
- **Realtime** — out of scope by default.
