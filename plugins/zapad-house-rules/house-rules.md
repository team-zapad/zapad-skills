# Zapad House Rules

Behavioral guidelines that apply regardless of stack or which other Zapad skill is active. These
govern *how* to work; the stack-specific skills (`zapad-laravel-backend`, `zapad-js-stack`, etc.)
govern *what* the code should look like. If a stack skill's rule and this file conflict on
architecture, the stack skill wins — this file is about process and judgment, not file layout.

## 1. Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

- State assumptions explicitly before implementing. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so, even if it means pushing back on the request.
- If something is unclear, stop, name what's confusing, and ask.

## 2. Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If it could be a fifth the size, rewrite it smaller.

## 3. Surgical changes

Touch only what you must. Clean up only your own mess.

- Don't "improve" adjacent code, comments, or formatting while making an unrelated change.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Notice unrelated dead code — mention it, don't delete it, unless asked.
- Remove imports/variables/functions that your own change made unused; leave everything else.
- Test: every changed line should trace directly to the request.

## 4. Goal-driven execution

Define success criteria. Loop until verified, not until it looks done.

- Turn vague asks into verifiable goals — "fix the bug" becomes "write a test that reproduces it,
  then make it pass."
- For multi-step work, state a brief plan as `step → verify` pairs before starting.
- Don't report a task as complete on the strength of having written the code — run the real
  checks (tests, linters, the project's own gates) and look at the output before saying it's done.

---

These rules are working if diffs get smaller, fewer changes get rewritten for being
overcomplicated, and clarifying questions come before implementation instead of after a mistake.
