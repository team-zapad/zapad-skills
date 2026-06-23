# zapad-skills

Zapad's shared [Claude Code](https://claude.com/claude-code) skills, distributed as a plugin marketplace.

## Install

Add the marketplace once (per machine):

```
/plugin marketplace add team-zapad/zapad-skills
```

Then install the skill into any project:

```
/plugin install zapad-js-stack
```

Update later with `/plugin marketplace update zapad-skills`.

## Skills

### `zapad-js-stack`

The canonical Zapad TypeScript web stack and the non-negotiable invariants behind it:
TanStack Start on AWS serverless (Lambda), Prisma 7 + PostgreSQL/RDS, Better Auth (Entra ID OIDC),
MUI + Tailwind, SST deploy. It triggers when scaffolding a new TypeScript/React app, choosing a tool
for any layer, or making an architecture decision — defaulting to the house choices and flagging deviations.

| | |
|---|---|
| App framework | TanStack Start (Nitro) |
| Compute | AWS Lambda (arm64, ZIP) via SST |
| Data | Prisma 7 + PostgreSQL/RDS behind RDS Proxy |
| Auth | Better Auth + Entra ID (OIDC) |
| UI | MUI + Tailwind |
| Validation | Zod (single source of truth) |

See [`plugins/zapad-js-stack/skills/zapad-js-stack/SKILL.md`](plugins/zapad-js-stack/skills/zapad-js-stack/SKILL.md).

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest
plugins/
  zapad-js-stack/
    .claude-plugin/plugin.json      # plugin manifest
    skills/zapad-js-stack/          # the skill
      SKILL.md
      references/
```
