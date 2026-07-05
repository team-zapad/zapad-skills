# zapad-skills

Zapad's shared [Claude Code](https://claude.com/claude-code) skills, distributed as a plugin marketplace.

## Install

Add the marketplace once (per machine):

```
/plugin marketplace add team-zapad/zapad-skills
```

Then install the skill into any project:

```
/plugin install zapad-house-rules
/plugin install zapad-js-stack
/plugin install zapad-laravel-backend
```

Update later with `/plugin marketplace update zapad-skills`.

## Org-wide rollout

The manual install above is per-developer, per-project. For a team, that's 4 commands someone has
to remember to run every time — the two options below make it automatic instead.

**Tier 1 — per-project, no admin access needed.**
Each dev still adds the marketplace once, ever, per machine (`/plugin marketplace add
team-zapad/zapad-skills`). Then commit this to every Zapad project's `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "zapad-house-rules@zapad-skills": true,
    "zapad-laravel-backend@zapad-skills": true,
    "zapad-js-stack@zapad-skills": true
  }
}
```

Anyone who clones the project and opens it in Claude Code gets all three plugins active —
no per-project `/plugin install`.

**Tier 2 — org-enforced, zero developer action.**
Claude Code supports a managed settings file that a developer's own settings cannot override.
Deploy it via MDM (Jamf/Kandji/Intune/GPO) or a new-laptop setup script, to:
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`
- Windows: `C:\Program Files\ClaudeCode\managed-settings.json`

```json
{
  "extraKnownMarketplaces": [
    { "name": "zapad-skills", "source": { "type": "github", "repo": "team-zapad/zapad-skills", "ref": "main" } }
  ],
  "enabledPlugins": [
    { "marketplace": "zapad-skills", "plugin": "zapad-house-rules" },
    { "marketplace": "zapad-skills", "plugin": "zapad-laravel-backend" },
    { "marketplace": "zapad-skills", "plugin": "zapad-js-stack" }
  ]
}
```

This is the actual one-click (zero-click) install: every dev, every project, every machine, all
Zapad conventions active from the first `claude` command, with no opt-in step to forget. An
optional `strictKnownMarketplaces` field can also block devs from adding unapproved marketplaces
— left out here since that's a bigger policy call than "install our skills."

## Skills

### `zapad-house-rules`

Stack-agnostic behavioral guidelines, independent of any specific tech stack: think before coding,
simplicity first, surgical changes, goal-driven execution with verify loops. Delivered via a
`SessionStart` hook (`hooks/hooks.json` + `scripts/inject-house-rules.sh`) that injects
[`house-rules.md`](plugins/zapad-house-rules/house-rules.md) into context at the start of every
session — active regardless of which stack plugin is also installed, no per-project CLAUDE.md
editing required.

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

### `zapad-laravel-backend`

Zapad's canonical Laravel backend architecture: single-action controllers, an Actions layer for
business logic, Form Requests for validation + authorization, domain exceptions, and Pest testing
conventions. Bundled as five separate skills so each triggers only on its own concern:

| | |
|---|---|
| `project-structure` | Where every component type lives and how it's named — a lookup skill, not a workflow |
| `coding-guidelines` | How to write internals: thin controllers, pure Actions, error handling, naming, duplication/abstraction rules, Pint + Larastan gates |
| `new-feature` | The ordered, end-to-end workflow for building a full feature, from migration to tests |
| `testing` | Pest conventions — what to test at each layer, fakes, worked examples |
| `conformance-review` | Audits an existing codebase against the other four skills' rules and produces a prioritized refactor punch list |

Also ships a `PostToolUse` hook (`hooks/hooks.json` + `scripts/lint.sh`): runs Pint and Larastan on
a `.php` file right after it's edited, active automatically once the plugin is installed — no
`.claude/settings.json` editing required. It's a fast per-file check, not a substitute for
`new-feature`'s step 11 (the real gate before calling a feature done).

All of the above only fires if a dev is actually using Claude Code with this plugin installed.
[`templates/laravel-quality-gate.yml`](plugins/zapad-laravel-backend/templates/laravel-quality-gate.yml)
is the backstop that doesn't depend on that — a GitHub Actions workflow (Pint + Larastan + tests)
to copy into each Laravel project's `.github/workflows/` once, so every PR gets checked
regardless of how it was written.

See [`plugins/zapad-laravel-backend/skills/`](plugins/zapad-laravel-backend/skills/).

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest
plugins/
  zapad-house-rules/
    .claude-plugin/plugin.json      # plugin manifest
    house-rules.md                  # the guidelines themselves
    hooks/hooks.json                # SessionStart -> injects house-rules.md into context
    scripts/inject-house-rules.sh   # the script hooks.json calls
  zapad-js-stack/
    .claude-plugin/plugin.json      # plugin manifest
    skills/zapad-js-stack/          # the skill
      SKILL.md
      references/
  zapad-laravel-backend/
    .claude-plugin/plugin.json      # plugin manifest
    skills/
      project-structure/SKILL.md
      coding-guidelines/SKILL.md
      new-feature/SKILL.md
      testing/SKILL.md
      conformance-review/SKILL.md
    hooks/hooks.json                  # auto-runs Pint + Larastan after editing a .php file
    scripts/lint.sh                   # the script hooks.json calls
    templates/laravel-quality-gate.yml # CI backstop, copy into a project's .github/workflows/
```
