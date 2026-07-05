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

- [ ] `Actions/{Domain}/` mirrors `Controllers/{Domain}/` — no orphaned files on either side
- [ ] Controller has exactly one method and zero business logic
- [ ] Action never receives `$request`
- [ ] Every business failure path has a `DomainException`, and each one is tested
- [ ] Route is named and grouped with correct middleware
- [ ] `vendor/bin/pint --dirty` and `vendor/bin/phpstan analyse` both pass
- [ ] Unit test for the Action, feature test for the Controller, both exist and pass
