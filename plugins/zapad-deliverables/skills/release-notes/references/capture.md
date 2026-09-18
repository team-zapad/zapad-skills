# Capturing screenshots of a running app

Read this before the first navigation. Authentication and demo data both cost far more to fix after a capture session than before one.

## Contents

- [Getting a session without typing credentials](#getting-a-session-without-typing-credentials)
- [Making the data presentable](#making-the-data-presentable)
- [Framing](#framing)
- [Preview server](#preview-server)
- [Cleanup](#cleanup)

---

## Getting a session without typing credentials

Entering passwords into forms is off-limits, including seeded dev passwords, and "it's only `password` on localhost" doesn't change that. It also isn't necessary — every framework can hand you a session directly.

**Laravel.** Add a route guarded by the environment, hit it, then remove it:

```php
// TEMP: screenshot session helper. Delete after capture.
if (app()->environment('local')) {
    Route::get('__shot-login', function () {
        auth()->loginUsingId(1); // the account that holds the data

        return redirect('/');
    });
}
```

Use the **file-editing tools** for this, not a shell heredoc appending to `routes/web.php` — the shell form tends to get blocked, and an Edit is easier to revert precisely.

Afterwards, remove it and confirm with `git status --short` that the file is clean. A dev-only auth bypass left in a branch is a genuinely bad thing to commit, and the environment guard is not an excuse.

**Other stacks:** the same shape applies — Django `force_login` behind a `DEBUG` check, Rails `sign_in` in a development-only route, a signed one-time link. Prefer whatever the framework already offers over minting tokens by hand.

**Pick the right account.** Multi-tenant apps drop you into whichever workspace is first, which is often the empty one. Check which tenant actually holds data before capturing:

```bash
php artisan tinker --execute 'foreach(\App\Models\User::with("teams")->get() as $u){echo $u->id." ".$u->email." ".$u->teams->pluck("slug")->implode(",").PHP_EOL;}'
```

---

## Making the data presentable

Seeded dev data reads as fake because it is. Rows named `Teste`, `new deal`, `asdf`, and faker's lorem ipsum tell the reader they're looking at a toy. A sparse board with two placeholder cards is worse than no screenshot.

Seed a realistic set first — plausible names, plausible amounts, enough rows that the layout looks inhabited. Two things bite:

**Mass-assignment guards.** Tenant foreign keys are often deliberately *not* fillable, so `create()` and `updateOrCreate()` silently drop them and you get a NOT NULL violation. Check the model before writing the seeder:

```php
#[Fillable(['title', 'contact_id', 'value_cents'])]  // note: no team_id
```

Use `forceFill([...])->save()` to bypass it. That's acceptable in a throwaway seeding script; it would not be acceptable in application code.

**Tinker with a file argument hangs.** `php artisan tinker script.php` waits for input. Use `require` instead, and keep the script in the scratchpad directory:

```bash
timeout 90 php artisan tinker --execute 'require "/abs/path/seed.php";'
```

Write the script with the Write tool rather than a heredoc — same reason as the route.

Tell the user afterwards what you inserted and how to remove it. This is their database, and the fact that it already held fake data is not consent to add more.

---

## Framing

- **Window at 1440×900** via `resize_window`, then downscale captures to **1200px** wide. A 600px email column wants a 2× asset; anything larger is wasted bytes.
- **Scroll away from error states.** Red failed-send banners, 404s, and empty states are honest but they aren't what the section illustrates. Scrolling a few ticks usually finds a clean stretch of the same view.
- **One feature per shot.** A screenshot doing double duty gets cropped or faded into uselessness. Capture the emoji picker open *and* the plain thread separately.
- **Capture the state, not the cursor.** Take the shot after the UI settles; a half-open menu or a visible tooltip that isn't the subject reads as a mistake.
- Use `save_to_disk: true` only on shots you intend to keep — screenshots you're merely looking at don't need saving.

Downscale and convert in one step:

```bash
magick shot.jpg -resize 1200x -quality 88 assets/inbox.jpg
```

---

## Preview server

The browser tools cannot open `file://`. Serve the directory and background it, otherwise the call blocks until timeout:

```bash
python3 -m http.server 8899     # Bash tool, run_in_background: true
```

`http.server` sends no charset, so a UTF-8 file renders as mojibake unless the HTML carries `<meta charset="utf-8">`. Add the tag rather than debugging the encoding.

---

## Cleanup

Before reporting done:

```bash
git status --short              # temp route gone?
pkill -f "http.server 8899"     # server stopped?
```

Close any tabs you opened with `tabs_close_mcp` unless the user asked to keep them.
