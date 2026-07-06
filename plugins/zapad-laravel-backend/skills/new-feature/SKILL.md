---
name: laravel-new-feature
description: Apply this skill when the user asks to add a new feature, create a new domain/resource, or implement something end-to-end in this Laravel project — e.g. "add a new feature for X", "create a Chat module", "implement message archiving", "how should I build this". This is the orchestrating workflow skill: it walks through every file a full feature touches, in order, and defers to laravel-project-structure for where files go and laravel-coding-guidelines for how to write their internals. Also use laravel-testing once the feature's classes exist. Do not use this for a single isolated change (e.g. "add a column", "fix this validation rule") — go straight to the relevant layer instead.
metadata:
  version: 1.0.0
---

# Building a New Feature

A "feature" here means a new domain capability end-to-end: something a user can trigger via a route that changes state. Follow this order — each step depends on the previous one existing.

Before starting, confirm the domain name (e.g. `Chat`, `Billing`, `Settings/Profile`) — every file in every step nests under it. See `laravel-project-structure` for the exact folder/naming pattern per component.

---

## Step-by-step

**1. Migration + Model**
Create the migration and the Eloquent model. Model gets only relationships, casts, scopes, accessors — see `laravel-coding-guidelines`.

**2. Policy**
One `{Model}Policy` per model touched, in `app/Policies/`. Write the authorization rule even if it seems obvious now — the FormRequest will need it in step 4.

**3. Domain exceptions (if any failure modes exist)**
Identify the business failures this feature can hit (e.g. "conversation is closed", "limit reached"). Create one exception per failure in `app/Exceptions/{Domain}/`, implementing the `DomainException` marker interface. Skip this step if the feature genuinely can't fail for business reasons — don't invent exceptions preemptively.

**4. Action**
Create `app/Actions/{Domain}/{Verb}{Noun}.php` with a single `handle()` method. This is where all the logic from steps 1–3 comes together: it receives models and primitives, performs the writes (wrapped in `DB::transaction()` if 2+ writes), and throws the domain exceptions from step 3 when applicable.

**5. Form Request**
Create `app/Http/Requests/{Domain}/{Verb}{Resource}Request.php`. `authorize()` calls the Policy from step 2. `rules()` validates the input the Action needs.

**6. Controller**
Create `app/Http/Controllers/{Domain}/{Verb}{Resource}Controller.php` with a single `__invoke()`. It type-hints the FormRequest and the Action, calls `$action->handle(...)`, and returns a response. Nothing else — no queries, no auth calls, no try/catch.

**7. Route**
Add the route to `routes/{domain}.php` (create the file if this is the domain's first route, and `require` it from `web.php`/`api.php`). Name it `{domain}.{resource}.{action}`.

**8. Events, Listeners, Notifications, Jobs — only if this feature needs side effects**
Ask: does anything else in the system need to react to this state change (notify a user, sync search, process an attachment)?
- Reaction to *this* state change happening → Event dispatched from the Action (step 4) + a queued Listener.
- User-facing notification as a result → the Listener calls `->notify()`, not the Action directly.
- Explicitly triggered background work (not a reaction) → a Job dispatched from the Action.
If none of this applies, skip the step entirely — don't add events for their own sake.

**9. External integration — only if this feature calls a third-party API**
Add/reuse a client in `app/Integrations/{Provider}/`. The Action calls the client; the client throws domain exceptions for known API errors and `$response->throw()`s everything else.

**10. Tests**
Use `laravel-testing` now that the classes exist:
- Unit test for the Action (happy path + every domain exception branch).
- Feature test for the Controller (success, validation failure, authorization failure).
- Unit tests for the Policy (true/false per method).
- If an Integration client was added, `Http::fake()` tests for it.

**11. Self-check — the gate before you say "done"**
Do not tell the user the feature is complete on the strength of having written the files. Actually run the commands below and look at their real output before claiming success:
```bash
vendor/bin/pint --dirty
vendor/bin/phpstan analyse
php artisan test --filter={Domain}
```
Then re-read `laravel-conformance-review`'s Step 2 checklist against only the files you just touched (not the whole app) — it's the same rulebook, used here as a self-audit instead of a report. If anything in this step surfaces a problem, fix it before reporting completion, don't mention it as a caveat.

---

## Worked example: "Archive Conversation"

Domain: `Chat`. Walking the steps:

1. No new migration needed — reuses existing `Conversation` model. Add `archived_at` column + migration.
2. `ConversationPolicy::archive(User $user, Conversation $conversation): bool` — must be a participant.
3. `AlreadyArchivedException implements DomainException` — thrown if archiving twice.
4. `app/Actions/Chat/ArchiveConversation.php` — single write, no transaction needed; sets `archived_at`, throws `AlreadyArchivedException` if already set; dispatches `ConversationArchived`.
5. `app/Http/Requests/Chat/ArchiveConversationRequest.php` — `authorize()` → `$this->user()->can('archive', $this->route('conversation'))`; no body fields to validate.
6. `app/Http/Controllers/Chat/ArchiveConversationController.php` — single `__invoke()`.
7. `routes/chat.php` → `Route::post('conversations/{conversation}/archive', ArchiveConversationController::class)->name('chat.conversations.archive');`
8. `ConversationArchived` event + a queued `NotifyParticipantsConversationArchived` listener that sends a `database` notification. (No job needed — nothing here is explicitly triggered background work.)
9. No external integration involved.
10. `tests/Unit/Actions/Chat/ArchiveConversationTest.php` (happy path + `AlreadyArchivedException`), `tests/Feature/Chat/ArchiveConversationTest.php` (200/redirect, 403 for non-participant), `tests/Unit/Policies/ConversationPolicyTest.php`.

---

## Checklist before calling the feature done

Every box here means "I ran/verified this and saw it pass" — not "this looks right." If you haven't executed step 11, you haven't earned any of these checkmarks.

- [ ] `Actions/{Domain}/` mirrors `Controllers/{Domain}/` — no orphaned files on either side
- [ ] Controller has exactly one method and zero business logic
- [ ] Action never receives `$request`
- [ ] Every business failure path has a `DomainException`, and each one is tested
- [ ] Route is named and grouped with correct middleware
- [ ] `vendor/bin/pint --dirty` and `vendor/bin/phpstan analyse` both pass — actually run, not assumed
- [ ] Unit test for the Action, feature test for the Controller, both exist and pass — actually run, not assumed

## Consistency pass — match your siblings (do this every time, before "done")

Consistency beats "best style" (see `laravel-coding-guidelines` § Consistency beats local optimality). A feature isn't done until the new code looks like the code already around it. Open the sibling files in the SAME domain and layer and diff your new code against their patterns — then fix yours to match, even where you'd personally choose differently. These are the drifts that slip through review, so check each explicitly:

- [ ] **Action verbs** — the new create/update/delete Action uses the SAME verb as its siblings (all `Register*`, or all `Store*` — not a new `Save*` next to `Register*`). One operation, one verb across the layer.
- [ ] **Dependency injection** — the controller injects its Action the same way its siblings do: all via the constructor, or all via `__invoke` — never a mix within the domain.
- [ ] **Names tell the truth about type** — `is`/`has`/`can`/`should` names hold only booleans; a variable holding a number/string/model is named for what it holds (`$minInternetSpeed`, not `$hasInternet`). No name needs a comment to reveal its type.
- [ ] **Return types** — a new list/show/store endpoint returns the same shape and type as the sibling list/show/store endpoints; don't introduce a new way to return a collection or resource.
- [ ] **Controller ⇄ Action mirror** — the new Controller has an Action in the mirrored `Actions/{Domain}` path (the PostToolUse hook warns on this, but confirm it).
- [ ] **File & test naming** — the test file, class, and method names follow the pattern the sibling files already use.

When your instinct and the existing pattern disagree, follow the pattern and move on. If the pattern is genuinely wrong, fix the whole set in a separate pass — never ship the new file as the lone exception.
