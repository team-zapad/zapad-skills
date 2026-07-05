---
name: laravel-coding-guidelines
description: Apply this skill whenever you are writing or reviewing the INTERNALS of a Laravel class — deciding what logic goes where, how to name something, how to handle errors, whether to use a transaction, how to structure a scope, whether a piece of duplication should be extracted, whether an abstraction (interface, trait, base class) is justified, or making code pass Pint/Larastan. Activate on requests like "review this code", "is this idiomatic", "refactor this action/controller", "is there too much duplication here", "is this over-engineered", "how should I name this", "why is Larastan complaining", "format this", "make this cleaner/more readable", or any code you are about to write inside a Controller, Action, Model, FormRequest, Event, Listener, Job, or Integration. For WHERE a file should live and what to name its file/folder, use laravel-project-structure. For the ordered steps of building a whole feature, use laravel-new-feature.
metadata:
  version: 1.0.0
---

# Laravel Coding Guidelines

These are the internal-quality rules for this codebase. `laravel-project-structure` tells you where a file lives; this skill tells you what's allowed to be inside it.

---

## Baseline PHP style

- All code is written in English — class/method/variable names, route names, config keys, commit messages, **and comments**. No exceptions, even for comments describing local business rules.
- `declare(strict_types=1);` at the top of every new file.
- Explicit return types and parameter types on every method, always — including `void` and `never`.
- Constructor property promotion for dependency injection (`public function __construct(private readonly Thing $thing) {}`).
- `readonly` properties by default unless mutation is required.
- PHP 8.4 attributes where the framework supports them (e.g. `#[Fillable([...])]`, `#[Hidden([...])]`) instead of static `$fillable`/`$hidden` arrays.
- Prefer first-class callable syntax and native enums over string constants for closed sets of values.

---

## Naming — must read like Laravel's own code

Laravel core is the style guide. If unsure how to name something, check how Laravel or a first-party package names the equivalent.

- **Classes**: `PascalCase`. Models are singular nouns (`Conversation`, never `Conversations`); Actions/Jobs are verb+noun (`SendMessage`, `ProcessMessageAttachments`).
- **Domain-prefix generic-suffix classes, don't prefix specific ones.** Verb-named or resource-named classes (Actions, Controllers, FormRequests, Exceptions) are already unique enough that their namespace disambiguates them — never prefix those with the domain (`Chat/StoreMessageController`, not `Chat/ChatStoreMessageController`). But catch-all architectural nouns — `Service`, `Repository`, `Manager` — recur in every domain folder and collide in IDE fuzzy-search (Cmd+P/Cmd+O) when unprefixed, so those get the domain folded into the name: `CheckoutSessionService`, not `Session/SessionService`. This is the same reasoning that already gives Integration clients their name — `WhatsAppClient`, never a bare `Client` (see the Naming & Location Reference in `laravel-project-structure`).
- **Methods and variables**: `camelCase` — `sendMessage()`, `$conversationId`. Never snake_case, never Hungarian-notation prefixes.
- **Database**: `snake_case` columns, plural `snake_case` table names (`conversation_participants`). Let Laravel infer the table name from the model; don't set `$table` unless it truly can't be inferred.
- **Booleans**: prefix `is`/`has`/`can`/`should` — `isArchived`, `hasParticipants`. A bare adjective as a method name (`archived()`) is ambiguous with an accessor and should be avoided.
- **Relationships**: named after what they return, matching Eloquent convention — `hasMany` is plural (`messages()`), `belongsTo`/`hasOne` is singular (`conversation()`, `sender()`).
- **No abbreviations** beyond ones PHP/Laravel already treat as idiomatic. `$req`, `$msg`, `$conv` are out; `$request`, `$message`, `$conversation` are in. Short loop/catch variables (`$i`, `$e`) are fine.
- A name should make its type and intent obvious without opening the file. If a variable needs a comment to explain what it holds, rename it instead.

---

## Duplication and abstraction — mechanical rules

These are checkable rules, not judgment calls. Apply them literally.

1. The same logic appearing in 1 or 2 places stays duplicated, written inline both times. Do not extract it.
2. The same logic appearing in 3 or more places gets extracted, on the 3rd occurrence, into whichever mechanism this codebase already has for that kind of logic (see rules 3–4 below). "Same logic" means the same business meaning — two `if` checks that happen to look alike but mean different things are not the same logic and are never merged.
3. A query constraint used in 2 or more places is extracted to a model scope. This is the one exception to the "3 occurrences" threshold, because scopes are the codebase's designated tool for this and cost nothing to add.
4. A validation or business rule needed in two different layers (e.g. a FormRequest and a console command, or two different Actions in different domains) is extracted to a trait in `app/Concerns/` the moment the second layer needs it — do not wait for a 3rd occurrence when the duplication crosses layers.
5. Every class has exactly one reason to change. Concrete test before writing a class or a `handle()`/`__invoke()` method: write a single sentence describing what it does. If that sentence contains "and," stop and split it into two classes or two methods.
6. When a new business case appears — a new state, a new provider, a new notification channel, a new type of the same thing — write a new class (Action, Listener, Job, or Integration client). Do not add a parameter plus an `if`/`switch`/`match` branch to an existing class to handle it.
7. Do not create an interface for a class until a second concrete implementation of that same contract exists somewhere in the codebase right now. One Integration client, one Action, one Job = write the concrete class directly, with no interface.
8. Do not add a constructor parameter, config key, method argument, or trait "for future flexibility" or "in case we need it later." Add it only when a second concrete caller exists today that needs a different value or behavior.
9. If code depends on an interface with multiple implementations, every implementation must produce the same kind of result and throw the same kind of exceptions for the same conditions — the calling code must never need an `instanceof` check or a comment like "this one behaves differently."
10. Every collaborator a class needs is received through its constructor (see Baseline PHP style). Never call `new SomeService()` inside a method body — inject it instead, even if there is currently only one implementation.

---

## Readability — code should read like well-written prose

- Guard clauses over nested conditionals: return or throw early, keep the happy path unindented.
- No more than 2 levels of nesting in a method. Past that, extract a private method or move the logic to another class.
- Comments explain *why*, never *what* — the code itself says what it does through naming. `// increment counter` next to `$count++` should be deleted; `// Stripe requires cents, not dollars` earns its place.
- No magic numbers or strings — name them as constants, enums, or config values (`self::MAX_BODY_LENGTH` instead of a bare `2000` repeated in a rule and a check).
- Keep methods short enough to read on one screen. A `handle()` or `__invoke()` that scrolls is a sign the logic belongs in another class.
- Favor clarity over cleverness: no one-liner chains that need re-reading twice, no nested ternaries. If a colleague would have to trace it in their head, write it as two lines instead of one.

---

## Controllers — thin by construction

- Single `__invoke()` method only. No multi-action resource controllers.
- Responsibility: receive request → call one Action → return a response. Nothing else.
- **Never** in a controller: Eloquent queries, `$this->authorize()`, business conditionals, `DB::transaction()`, try/catch.
- If a controller has more than ~10 lines or an `if` statement, that logic belongs in the Action or FormRequest.

## Actions — where business logic lives

- One class, one public `handle(...)` method.
- Receives Eloquent models and primitives — **never** the `$request` object. This keeps Actions callable from console commands, jobs, and tests without an HTTP context.
- No authorization logic inside an Action — authorization is a FormRequest/Policy concern.
- Signals failure exclusively by throwing a domain exception — never `null`, `false`, or an empty collection to mean "didn't work."
- No base class or interface for Actions — a plain `final` class per rule 7. Nothing is shared through inheritance; shared behavior (auth, validation, transactions) is composed via constructor collaborators, not a parent class.

### Composing Actions

An Action may need another Action's logic as a sub-step (e.g. creating an order also needs to notify someone). This is a normal collaborator, covered by rule 10 (Duplication and abstraction): constructor-inject the other Action and call its `handle()` — never instantiate it inline.

```php
final readonly class CreateOrder
{
    public function __construct(
        private NotifyOrderCreated $notifyOrderCreated,
    ) {}

    public function handle(Cart $cart): Order
    {
        return DB::transaction(function () use ($cart) {
            $order = Order::create([...]);

            $this->notifyOrderCreated->handle($order);

            return $order;
        });
    }
}
```

- The outer Action owns the transaction; a nested Action never opens its own `DB::transaction()`.
- A `DomainException` thrown by the nested Action is **not** caught by the calling Action — let it bubble to the global handler (see Error handling below). The surrounding transaction rolls back automatically because the exception propagates out of the `DB::transaction()` closure.

## Form Requests — validation + authorization together

- `authorize()` always delegates to a Policy: `$this->user()->can('action', $this->route('model'))`. Never inline authorization conditionals here.
- Rules live inline in `rules()` by default. Only extract to `app/Concerns/` when the same rules are needed in a *different layer* (e.g. a Fortify action or console command) — not just in a second FormRequest.

## Models — data shape only

- Only relationships, casts, scopes, and accessors belong on a Model. No business logic, no side effects, no calls to Actions/Notifications from a Model.
- Casts via `protected function casts(): array`, not the `$casts` property.
- Every relationship method has an explicit return type (`BelongsTo`, `HasMany`, etc.).

## Queries & scopes

- Rule of thumb: a query constraint used in 2+ places gets extracted to a model scope; used once, it stays inline in the Action.
- Scope names are adjective/state-based — `unread`, `active`, `forUser` — never verb-based (`getUnread`, `filterActive`).

## Database transactions

- Wrap in `DB::transaction()` only when an Action performs **2 or more writes**. Single-write Actions don't need one.
- Test: "if the second write fails, would the first leave the DB inconsistent?" If yes → transaction. If no → skip it.
- Transactions belong inside Actions, never in Controllers.

## Error handling

| Error type | Thrown by | Handled by |
|---|---|---|
| Validation failure | FormRequest | Laravel automatically |
| Authorization failure | FormRequest | Laravel automatically |
| Domain failure (e.g. "conversation is closed") | Action | Global handler in `bootstrap/app.php` |
| Infrastructure failure (DB down, Redis unreachable) | Anywhere | Laravel default (500) — do not catch |

Rules:
- All expected business failures implement the `DomainException` marker interface (`app/Exceptions/DomainException.php`).
- A domain exception's `$message` is the user-facing string — it must be safe to display as-is.
- Controllers never catch exceptions. Actions never catch bare `\Exception` or `\Throwable` — swallowing infrastructure failures hides real outages.
- Register handling once, globally:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (DomainException $e, Request $request) {
        if ($request->expectsJson()) {
            return response()->json(['message' => $e->getMessage()], 422);
        }
        return back()->withErrors(['error' => $e->getMessage()]);
    });
})
```

## Events, Listeners, Notifications, Jobs

- The Action that causes a state change dispatches the Event — never the Controller.
- Listeners implement `ShouldQueue` by default; side effects must not block the HTTP response.
- Use Laravel's automatic event discovery. Never call `Event::listen()` manually. Verify with `php artisan event:list` that each listener appears exactly once.
- Notifications are sent from queued Listeners, not directly from Actions. An Action dispatches an event; a Listener calls `->notify()`.
- Job vs. queued Listener: explicitly triggered work (from an Action, command, or schedule) is a **Job**; work that reacts to a domain event is a **queued Listener**.

## External API integrations

- One client class per provider under `app/Integrations/{Provider}/`. The client only speaks HTTP — no business logic.
- Detect known API-level business errors and translate them into a `DomainException`. Call `$response->throw()` for everything else so infrastructure failures surface as 500s.
- Register the named HTTP client in `AppServiceProvider`; credentials come from `config/{provider}.php`, sourced from `.env`.

---

## Tooling gates

Every non-trivial change should pass both before being considered done:

**Laravel Pint** — formatting only, zero tolerance for drift.
```bash
vendor/bin/pint --dirty   # format only changed files
vendor/bin/pint --test    # CI check, no changes written
```

**Larastan / PHPStan** — static analysis. Do not add new baseline suppressions; fix the type instead.
```bash
vendor/bin/phpstan analyse
```
Common fixes when Larastan complains:
- Missing return type → add it.
- `Collection` without generics → annotate with `@return Collection<int, Message>`.
- Untyped array shape → replace with a typed DTO or add a precise `@param array{...}` docblock.
- Nullable value used without a check → narrow it explicitly rather than suppressing.

If Pint and Larastan disagree with a rule in this file, this file wins for architectural decisions (where logic lives); the tools win for mechanical style and type-safety issues.

These same two commands (plus the test suite) should also run in CI, independent of whether the change was made with Claude Code — the plugin's local hook only fires if a dev is actually using it. Copy `templates/laravel-quality-gate.yml` from this plugin into the project's `.github/workflows/` once per repo.
