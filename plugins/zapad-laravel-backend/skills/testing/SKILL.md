---
name: laravel-testing
description: Apply this skill when writing, reviewing, or fixing Pest tests in this Laravel project — Actions, Controllers, Policies, Events/Listeners, Notifications, Jobs, or Integrations. Activate on "write a test for X", "test this action/controller/policy", "why is this test failing", "add a feature test", "add a unit test", or any mention of Pest, RefreshDatabase, factories, or fakes. This assumes the project structure and naming from laravel-project-structure and the architecture from laravel-coding-guidelines — use those to know where the code under test lives before writing its test.
metadata:
  version: 1.0.0
---

# Laravel Testing (Pest)

Every layer of the architecture has one clear place to be tested and one clear way to test it. Don't test the same behavior twice at two layers.

---

## Directory layout — mirrors `app/`

```
tests/
  Unit/
    Actions/{Domain}/SendMessageTest.php
    Policies/MessagePolicyTest.php
  Feature/
    {Domain}/StoreMessageTest.php          ← named after the Controller's action, tests the full HTTP cycle
```

- **Unit tests**: Actions and Policies — no HTTP, no middleware, calling the class directly.
- **Feature tests**: Controllers — full HTTP request through routing, middleware, FormRequest, Action, and response.

---

## What to test at each layer

| Layer | Test type | What it verifies |
|---|---|---|
| Action | Unit | Every `handle()` outcome: the happy path's return value/side effects, and every `DomainException` it can throw |
| FormRequest | Feature (via the controller) | Validation failures return 422 with the right error keys; authorization failures return 403 |
| Controller | Feature | HTTP status, redirect target, response shape, and that the DB actually changed |
| Policy | Unit | Each policy method, true and false cases, using real (not mocked) User/Model instances |
| Event | Feature (via the Action's test) | `Event::fake()` + `assertDispatched(EventClass::class)` |
| Listener | Unit | Call `handle()` directly with a constructed event instance; assert side effect (e.g. notification sent) |
| Notification | Unit or Feature | `Notification::fake()` + `assertSentTo($user, NotificationClass::class)` |
| Job | Feature (via the Action's test) | `Queue::fake()` + `assertPushed(JobClass::class)` — don't re-test the job's internals here, that's the job's own unit test |
| Integration client | Unit | `Http::fake()` for success, known error, and unexpected-status cases; assert the right `DomainException` is thrown |

---

## Conventions

- Use Pest's functional syntax (`it()`, `test()`, `expect()`), not PHPUnit classes.
- `uses(RefreshDatabase::class)` in `tests/Pest.php` (or per-file) for any test touching the DB.
- Authenticate with `actingAs($user)`, never manually set session/guard state.
- Build data with model factories, not raw `Model::create()` in the test body — this keeps tests resilient to schema changes.
- One behavior per test. If a test name needs "and" to describe it, split it.
- Arrange–Act–Assert, with a blank line between each section for readability.

```php
// tests/Unit/Actions/Chat/SendMessageTest.php
it('creates a message from the sender in the conversation', function () {
    $sender = User::factory()->create();
    $conversation = Conversation::factory()->create();

    $message = (new SendMessage())->handle($sender, $conversation, 'Hello');

    expect($message->user_id)->toBe($sender->id)
        ->and($message->conversation_id)->toBe($conversation->id)
        ->and($message->body)->toBe('Hello');
});

it('throws when the conversation is closed', function () {
    $sender = User::factory()->create();
    $conversation = Conversation::factory()->closed()->create();

    (new SendMessage())->handle($sender, $conversation, 'Hello');
})->throws(ConversationClosedException::class);
```

```php
// tests/Feature/Chat/StoreMessageTest.php
it('stores a message and redirects back', function () {
    $user = User::factory()->create();
    $conversation = Conversation::factory()->create();

    $response = actingAs($user)
        ->post(route('chat.messages.store', $conversation), ['body' => 'Hi']);

    $response->assertRedirect();
    expect(Message::where('conversation_id', $conversation->id)->count())->toBe(1);
});

it('rejects a body over 2000 characters', function () {
    $user = User::factory()->create();
    $conversation = Conversation::factory()->create();

    actingAs($user)
        ->post(route('chat.messages.store', $conversation), ['body' => str_repeat('a', 2001)])
        ->assertSessionHasErrors('body');
});

it('denies access to a user who is not a participant', function () {
    $outsider = User::factory()->create();
    $conversation = Conversation::factory()->create();

    actingAs($outsider)
        ->post(route('chat.messages.store', $conversation), ['body' => 'Hi'])
        ->assertForbidden();
});
```

---

## Coverage expectations

- Every Action gets a unit test for its happy path and every `DomainException` branch it can throw.
- Every Controller gets a feature test for: success, validation failure, authorization failure.
- Every Policy method gets both a true and false case.
- Every Integration client gets `Http::fake()` tests for success and each distinct error mapping.
- Don't unit-test Controllers or feature-test Actions directly — that's redundant coverage of the same logic at the wrong layer.

## Running tests

```bash
php artisan test              # standard run
vendor/bin/pest --parallel    # faster local runs
vendor/bin/pest --coverage    # requires Xdebug/PCOV
```
