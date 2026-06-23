# Data layer

Prisma, PostgreSQL/RDS, and the Zod validation contract.

## Zod is the single source of truth (invariant #2)

- One schema per entity, defined once, reused for: the server-function input validator, the TanStack Form validators, and env parsing.
- Infer TypeScript types with `z.infer` — never hand-write a parallel type or a second validation pass.

## Prisma on Lambda (invariant #3)

Three rules, because the ORM ships inside the SSR Lambda and is on every page's cold-start path:

- **Singleton client** at module scope so warm invocations reuse the connection. Never instantiate `PrismaClient` per request.
- **RDS Proxy** in front of Postgres. Vanilla RDS + Lambda exhausts `max_connections` under concurrency; the Proxy is the fix and is ORM-independent.
- **`compilerBuild = "small"`** in the generator, to trim the cold-start bundle.

Prisma was chosen for DX (Eloquent-like ergonomics) over Drizzle's lighter footprint, eyes open. The three rules above recover most of the cold-start gap.

## Schema & queries

- Schema-first in `schema.prisma`. Migrations via `prisma migrate`.
- Prefer the typed query API. Drop to `$queryRaw` only for genuinely complex aggregations, and keep those isolated.

## Database

- PostgreSQL on RDS, region `sa-east-1`.
- **The DB sits behind RDS Proxy** — this is the invariant; confirm it before the first deploy.
- Instance class and Multi-AZ are **per-project sizing decisions**, not house defaults. Start small (e.g. a `t4g`/`m7g` class matched to load) and enable Multi-AZ for production or anything that can't tolerate failover downtime. Don't pin a fixed instance size into every project.
