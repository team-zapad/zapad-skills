---
name: zapad-new-project
description: The wizard for starting a new Zapad project from zero. Use it whenever the user wants to create a new project, start a new app or service, bootstrap/scaffold a repository, or says "vamos começar um projeto novo" — including when they don't name this skill and just describe the app they want to build. It collects title, objective, language and framework, guarantees a git repository exists before the first file is written, scaffolds README.md, CLAUDE.md and .gitignore, commits in English, and then hands off to the stack skill that owns the real scaffold. Do not use it for a new feature inside an existing project.
metadata:
  version: 1.0.0
---

# Starting a New Project

This is the entry point for a project that doesn't exist yet. It does four things nothing else does — pin down what's being built, guarantee git is there first, leave the answers written down, and route to the right stack skill. It does **not** scaffold the app itself: that's `zapad-js-stack` or `zapad-laravel-backend`.

Run the steps in order. Step 2 is a gate, not a suggestion.

---

## Step 1. Collect the answers

Ask all four in a single `AskUserQuestion` call. Don't guess any of them from the conversation — the point of the wizard is that they're stated.

| Field | What to ask |
|---|---|
| **Title** | Project name. Goes into `README.md`, `CLAUDE.md` and the initial commit. |
| **Objective** | One sentence: what problem it solves, for whom. |
| **Language** | TypeScript · PHP · Other |
| **Framework** | Follows from the language: TypeScript → TanStack Start (`zapad-js-stack`); PHP → Laravel (`zapad-laravel-backend`); Other → free text |

If the answers land outside the two house stacks, say so explicitly and continue anyway — flag the deviation, don't silently substitute a house choice.

## Step 2. Git before any file — gate

```bash
git rev-parse --git-dir
```

- Not a repository → run `git init` **now**.
- Already one → carry on.

**No file is written until this passes.** That includes `.gitignore` and `README.md`. The point is that the project's very first file is already tracked by a repository, so nothing exists outside version control at any moment.

## Step 3. Scaffold the three documents

Only these three. Everything else belongs to the stack skill.

- **`README.md`** — title, the objective sentence, the chosen stack, and a `## Getting started` placeholder the stack skill fills in.
- **`CLAUDE.md`** — title, objective, language/framework, and which Zapad plugin governs the project (`zapad-js-stack` or `zapad-laravel-backend`). This is what makes the wizard's answers outlive the session.
- **`.gitignore`** — for the language (Node/TypeScript or PHP/Laravel). Keep it short; the framework's own scaffolder ships a fuller one and will extend it.

If the stack scaffolder refuses to run in a non-empty directory (`laravel new` in place, some `create-*` CLIs), run the scaffolder first inside the repo created in step 2, then write these three files on top of its output. The git gate still comes first either way.

## Step 4. Initial commit

Use `zapad-semantic-commit`. In English, like every commit:

```
chore: initialize <title>
```

## Step 5. Hand off

Invoke the stack skill and let it do the actual scaffold:

| Framework | Hand off to |
|---|---|
| TanStack Start / TypeScript | `zapad-js-stack` |
| Laravel / PHP | `zapad-laravel-backend` — `laravel-project-structure`, then `laravel-new-feature` for the first feature |
| Anything else | No house skill — say so, and fall back to `zapad-house-rules` alone |

Don't restate what those skills already say about structure, dependencies or deploy. This skill's job ends when they take over.
