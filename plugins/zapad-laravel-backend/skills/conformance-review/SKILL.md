---
name: laravel-conformance-review
description: Apply this skill when asked to review, audit, or assess an EXISTING Laravel codebase against this project's own conventions — not generic Laravel best practice. Activate on "review this codebase", "audit this for conformance", "is this following our conventions", "what's drifted from our architecture", "give me a refactor punch list", or when handed an old/inherited Laravel app and asked where it stands. This produces a single prioritized report; it does not fix anything itself. For writing NEW code correctly the first time, use laravel-project-structure (where) and laravel-coding-guidelines (how) directly instead — this skill is for judging code that already exists.
metadata:
  version: 1.0.0
---

# Laravel Conformance Review

You are reviewing a codebase against **this project's documented architecture** — `laravel-project-structure`, `laravel-coding-guidelines`, `laravel-new-feature`, and `laravel-testing` — not against generic Laravel idioms. A codebase can be perfectly idiomatic Laravel and still fail this review because it doesn't follow our single-action-controller + Actions architecture. Conversely, don't flag something as wrong just because it's unusual Laravel — flag it only if it contradicts a rule in one of those four files.

Be blunt. Don't soften findings, don't pad the report with praise, and don't invent problems in a module that's genuinely fine — leave it out.

---

## Step 1: Map before judging

Before writing any finding, open representative files from each area — don't judge from file names alone:

- A few Controllers, a few Actions, a few FormRequests — old and recent.
- Every file matching a generic-suffix name: `Service`, `Manager`, `Helper`, `Util`, `Repository`. These are where logic dumps and naming drift concentrate.
- The largest file in `app/Models/` and the largest in `app/Actions/` — size is usually a proxy for a class doing more than one thing.
- `routes/*.php`, `bootstrap/app.php` (exception handling), and `app/Concerns/` (should be nearly empty — see rule below).
- A sample of `tests/Unit/Actions/` and `tests/Feature/` — or their absence.

## Step 2: Check against the actual rules

Pull findings only from what's documented in the other three skills. Concretely check:

**Structure** (`laravel-project-structure`)
- Does `app/Actions/{Domain}/` mirror `app/Http/Controllers/{Domain}/` 1:1? Any orphaned file on either side (a Controller with no matching Action, or vice versa) is a finding.
- Are Models and Policies flat (no domain subfolders)? Is everything else nested by domain?
- Do names follow the table (`{Verb}{Resource}Controller`, `{Verb}{Noun}` Action, `{Provider}Client`, etc.)?
- Generic-suffix classes (`Service`, `Repository`, `Manager`, `Client`) — domain-prefixed where a real name collision exists across domains, not prefixed everywhere reflexively.
- `app/Concerns/` — any trait in here shared by only one layer (e.g. two FormRequests and nothing else) is a violation; it should only hold logic shared *across* layers.

**Internals** (`laravel-coding-guidelines`)
- Controllers: single `__invoke()`, zero Eloquent queries, zero `$this->authorize()`, zero business conditionals, zero `DB::transaction()`, zero try/catch. Any of these present is a finding.
- Actions: single `handle()`, never receives `$request`, no authorization logic, failure signaled only via a thrown `DomainException` (never `null`/`false`/empty collection).
- Actions calling Actions: constructor-injected, never `new SomeAction()` inline; the outer Action owns the one `DB::transaction()`; no base class or interface exists purely to share behavior between Actions.
- Duplication: same logic in 3+ places not yet extracted; a query constraint repeated in 2+ places not yet a scope; an interface with only one implementation; a constructor/config param added "for future flexibility" with no second caller today.
- Nesting depth >2 in any method; magic numbers/strings not named as constants; a `handle()`/`__invoke()` that doesn't fit on one screen.
- Error handling: every expected business failure implements the `DomainException` marker; Controllers/Actions never catch bare `\Exception`/`\Throwable`.
- Events dispatched from Controllers instead of Actions; Notifications sent directly from an Action instead of via a queued Listener; synchronous work in the request cycle that should be a queued Job.
- Integration clients containing business logic instead of only translating HTTP responses into `DomainException`s.

**Feature completeness** (`laravel-new-feature`)
- For a given domain, are all the pieces present — Policy, Model, domain Exceptions, Action, FormRequest, Controller + named route, and (where applicable) Events/Listeners/Jobs? A domain with a Controller but no FormRequest, or an Action with no matching test, is an incomplete feature, not a style nit.

**Testing** (`laravel-testing`)
- Every Action has a unit test covering the happy path and every `DomainException` branch.
- Every Controller has a feature test covering the full HTTP cycle (success + authorization failure).
- No Action feature-tested and no Controller unit-tested directly (redundant coverage at the wrong layer) — note this as waste, not as missing coverage.
- Critical paths (auth, payments, permissions, anything mutating money or access) with zero test coverage are the highest-priority testing gaps.

Explicitly out of scope: PSR-12/formatting, import order, whitespace — Pint and Larastan already gate these (see the Tooling gates section of `laravel-coding-guidelines`); don't re-litigate what a tool already enforces.

## Step 3: Write the report

```
# Conformance Review — [repo/project name]

## Summary
2-4 sentences: overall drift from our documented architecture, the single biggest systemic
gap, and whether this is a targeted cleanup or needs a broader pass.

## Findings

### Critical
(Findings that risk data integrity, security, or production stability)

### High
(Findings that significantly hurt maintainability or actively contradict the architecture)

### Medium
(Real deviations, but contained or low-blast-radius)

### Low
(Worth aligning eventually, not urgent)
```

Each finding:

```
**[Short title]** — `app/Path/To/Area`
What's wrong: [1-3 sentences, concrete, no hedging]
Rule violated: [which skill + rule, e.g. "coding-guidelines § Actions — never receives $request"]
Why it matters: [concrete consequence — bug risk, scaling issue, onboarding cost]
Suggested direction: [1-2 sentences — enough to seed a refactor task, not a full implementation]
```

Severity guidance:
- **Critical**: swallowed/silent domain failures, missing authorization, raw business logic executed with no error boundary — data loss, security, or incident risk.
- **High**: broken Controller↔Action mirror, business logic in the wrong layer, Actions receiving `$request`, untested critical paths — actively causes bugs or blocks safe change.
- **Medium**: naming drift, missing domain-prefix on a real collision, premature abstraction, incomplete feature (missing test, missing FormRequest) — costly but contained.
- **Low**: cosmetic-adjacent drift, a `Concerns/` trait that's borderline but not yet harmful.

Order findings within each severity by how central the affected domain is to the app — core domain logic first, peripheral features last.

## Constraints

- Every finding points to a real file or directory — no "the codebase in general" claims.
- Every finding names the specific rule it violates and which skill documents that rule.
- Skip anything Pint/Larastan already catches.
- Don't pad: a domain that already matches the architecture doesn't get a finding.
- This is a report only — do not fix findings in this pass unless explicitly asked to.
