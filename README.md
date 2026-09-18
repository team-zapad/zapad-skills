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
/plugin install zapad-design-flow
/plugin install zapad-deliverables
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

**Designers are a separate profile.** Tier 1 does not work for `zapad-design-flow`: a designer uses
it to *create* the project, so there is no project yet whose `.claude/settings.json` could enable it.
Either put the two `/plugin` commands in design onboarding, or give the design group its own Tier 2
payload with `zapad-design-flow` alone. That profile should not get `zapad-js-stack` or
`zapad-laravel-backend` — both would push a prototype toward the production stack this plugin
deliberately avoids.

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

### `zapad-design-flow`

The git and project workflow for **designers**, written in Portuguese. Nine skills that take a
designer from nothing to a high-fidelity prototype online without having to learn git first. Scoped
to prototype repos — Vite + React + Tailwind, pure front end, no `.env`, no production access —
deliberately lighter than `zapad-js-stack`.

| | |
|---|---|
| `configurar` | Node, git identity and GitHub auth. Once per person. |
| `novo-projeto` | Creates a new prototype and gets it running in the browser |
| `rodar-projeto` | Gets an existing prototype running here, and writes the project's `CLAUDE.md` if there is none |
| `nova-tarefa` | A clean branch off an up-to-date `main` |
| `salvar` | Commits one finished idea, screening out what must not go in |
| `mandar-pro-time` | Pushes, opens the PR and hands back the preview link |
| `socorro` | One door for when things break — six cases, safe fix only |
| `atualizar` | Merges `main` into the branch before it rots |
| `preparar-entrega` | Separates reusable components from prototype shortcuts and writes `HANDOFF.md` |

Like `zapad-house-rules`, it ships a `SessionStart` hook (`hooks/hooks.json` +
`scripts/inject-convencoes.sh`) that injects
[`convencoes.md`](plugins/zapad-design-flow/convencoes.md) into context: branch naming, commit
format and the safety guards apply with or without a command — the nine skills are a shortcut to the
full path, not the only door. The hook only affects whoever installs this plugin; devs are untouched.

Anything that stays in the repo is English (branch, commit, PR); anything spoken to the person is
Portuguese. Destructive git is out of the plugin entirely — no `reset --hard`, no force push, no
`rebase`, no history rewriting. When that is the only known way out, the skill stops and prepares a
Discord message with the technical state attached.

See [`plugins/zapad-design-flow/`](plugins/zapad-design-flow/).

### `zapad-deliverables`

Everything a Zapad client actually sees. Two skills that split on a single question — *what
changed?* versus *was it worth it?* — and deliberately do not borrow each other's register, because
a changelog that argues its own value gets trusted less and a value deck that lists commits fails to
make its case.

| | |
|---|---|
| `release-notes` | Turns git history into notes a customer would read, illustrated with real screenshots of the running app |
| `brand-deliverables` | Decks, pasteable email summaries and WhatsApp/social cards in the Zapad visual identity |

They share the mechanics of email HTML — tables with inline styles, what survives a paste into
Gmail, the copy button, `scripts/inline_assets.py` — documented once in
[`brand-deliverables/references/email.md`](plugins/zapad-deliverables/skills/brand-deliverables/references/email.md)
and reused by both. That shared file is why they ship as one plugin rather than two.

What `release-notes` is mostly about is the judgment before the writing: most commits are invisible
to users and a few unremarkable-looking ones are the headline, so it reads full commit bodies rather
than subject lines, groups by user-visible capability rather than by commit, and holds a release to
roughly 500–600 words. It also **never types a password** to reach a screen worth capturing — it
asks the framework for a session through a temporary local-only route, and reverts it.

Per-project values (how to get a session, which tenant holds the data, the card colour, where the
logo lives) belong in the project's own repo, not in this plugin — the skill says so and gives the
headings to use.

See [`plugins/zapad-deliverables/skills/`](plugins/zapad-deliverables/skills/).

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
  zapad-design-flow/
    .claude-plugin/plugin.json      # plugin manifest
    convencoes.md                   # the always-on conventions
    hooks/hooks.json                # SessionStart -> injects convencoes.md into context
    scripts/inject-convencoes.sh    # the script hooks.json calls
    skills/                         # the nine designer skills, in Portuguese
      configurar/SKILL.md
      novo-projeto/SKILL.md
      rodar-projeto/SKILL.md
      nova-tarefa/SKILL.md
      salvar/SKILL.md
      mandar-pro-time/SKILL.md
      socorro/SKILL.md
      socorro/references/casos.md
      atualizar/SKILL.md
      preparar-entrega/SKILL.md
  zapad-deliverables/
    .claude-plugin/plugin.json      # plugin manifest
    skills/
      release-notes/
        SKILL.md
        references/capture.md       # screenshots without typing credentials
        assets/                     # the branded release email template
        scripts/fade_bottom.py      # bakes a bottom fade into a screenshot
        evals/evals.json
      brand-deliverables/
        SKILL.md
        references/                 # deck.md, email.md, card.md
        assets/                     # templates + brand masters
        scripts/inline_assets.py    # shared by both skills
```
