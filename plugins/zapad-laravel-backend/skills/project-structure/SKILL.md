---
name: laravel-project-structure
description: Apply this skill when you need to know WHERE a piece of Laravel code belongs or WHAT to name it — not how to write its internals. Activate when the user asks "where does this go", "what should I name this class", "how is this project organized", references a folder like Actions/, Requests/, Policies/, Integrations/, or when generating any new file and you need its path/namespace/filename before writing content. This is a reference/lookup skill, not a workflow — for the end-to-end steps of building a feature, use laravel-new-feature; for how to write the internals well, use laravel-coding-guidelines.
metadata:
  version: 1.0.0
---

# Laravel Project Structure

This project uses single-action controllers with a dedicated Actions layer. Every domain concept (e.g. `Chat`, `Billing`, `Settings/Profile`) gets a matching folder under each of the paths below. Consistency of location and naming matters more than any individual file's contents.

---

## Directory Layout

```
app/
  Actions/
    {Domain}/                  ← mirrors Http/Controllers/{Domain}/ exactly, 1:1
      SendMessage.php
      DeleteMessage.php
  Http/
    Controllers/
      {Domain}/
        StoreMessageController.php
        DestroyMessageController.php
    Requests/
      {Domain}/
        StoreMessageRequest.php
  Models/
    Message.php
  Policies/
    MessagePolicy.php
  Events/
    {Domain}/
      MessageSent.php
  Listeners/
    {Domain}/
      NotifyParticipantsOfNewMessage.php
  Notifications/
    {Domain}/
      NewMessageNotification.php
  Jobs/
    {Domain}/
      ProcessMessageAttachments.php
  Integrations/
    {Provider}/
      WhatsAppClient.php
  Exceptions/
    {Domain}/
      ConversationClosedException.php
  Concerns/                    ← shared validation traits only, cross-layer use
routes/
  {domain}.php
tests/
  Feature/
    {Domain}/
  Unit/
    {Domain}/
```

**The golden rule:** `Actions/{Domain}/` always mirrors `Http/Controllers/{Domain}/` 1:1. If a controller moves, its action moves with it. Nested domains nest identically — `Controllers/Settings/Profile/` ⇄ `Actions/Settings/Profile/`.

---

## Naming & Location Reference

| Component | Location | Naming pattern | Example |
|---|---|---|---|
| Controller | `app/Http/Controllers/{Domain}/` | `{Verb}{Resource}Controller` | `StoreMessageController` |
| Action | `app/Actions/{Domain}/` | `{Verb}{Noun}` | `SendMessage` |
| Form Request | `app/Http/Requests/{Domain}/` | `{Verb}{Resource}Request` | `StoreMessageRequest` |
| Model | `app/Models/` (flat, no domain folders) | Singular noun | `Message` |
| Policy | `app/Policies/` (flat) | `{Model}Policy` | `MessagePolicy` |
| Domain Exception | `app/Exceptions/{Domain}/` | `{Condition}Exception` | `ConversationClosedException` |
| Event | `app/Events/{Domain}/` | Past-tense noun phrase | `MessageSent` |
| Listener | `app/Listeners/{Domain}/` | `{Verb}{Noun}` describing the reaction | `NotifyParticipantsOfNewMessage` |
| Notification | `app/Notifications/{Domain}/` | `{Noun}Notification` | `NewMessageNotification` |
| Job | `app/Jobs/{Domain}/` | Describes the work | `ProcessMessageAttachments` |
| Integration client | `app/Integrations/{Provider}/` | `{Provider}Client` | `WhatsAppClient` |
| Route file | `routes/{domain}.php` | lowercase domain name | `routes/chat.php` |
| Route name | — | `{domain}.{resource}.{action}` | `chat.messages.store` |
| Feature test | `tests/Feature/{Domain}/` | `{Action}Test` | `StoreMessageTest` |
| Unit test | `tests/Unit/{Domain}/` | `{ActionClass}Test` | `SendMessageTest` |

Notes:
- Models and Policies are **flat** (no domain subfolders) — a `Message` model is always `app/Models/Message.php` regardless of which domain features touch it.
- Everything else (Controllers, Actions, Requests, Events, Listeners, Notifications, Jobs, Exceptions, tests) is **nested by domain**.

---

## `app/Concerns/` — the one exception folder

Only put a trait here when the same logic is needed **outside** a single layer — e.g. validation rules shared between a FormRequest and a Fortify action or console command. Two FormRequests sharing rules is not sufficient justification; inline duplication is preferred over a premature abstraction. If you're reaching for `Concerns/` and can't name a second *layer* (not just a second class) that needs it, keep it inline.

---

## Routes

- One file per domain: `routes/{domain}.php`, required from `web.php` (or `api.php` for API-only domains).
- Group related routes under a single `Route::middleware([...])` call — never repeat middleware per route.
- Every route is named: `{domain}.{resource}.{action}`.

```php
// routes/chat.php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::post('conversations/{conversation}/messages', StoreMessageController::class)
        ->name('chat.messages.store');
});
```

---

## Quick decision checklist when creating a new file

1. What domain does this belong to? → determines the `{Domain}` folder segment.
2. Is it a Controller, Action, Request, Event, Listener, Notification, Job, or Integration? → look up its row above for location + naming pattern.
3. Is it a Model or Policy? → flat folder, no domain segment.
4. Does the Actions folder still mirror Controllers after this change? → if not, fix the mismatch before moving on.
