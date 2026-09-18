---
name: release-notes
description: "Turn recent git history into release notes an end user would actually read, illustrated with real screenshots of the running app. Use this whenever someone asks for release notes, changelog, \"what shipped\", \"novidades\", \"what's new\", a product update email, or a summary of the last N days/weeks of work for customers, a team, or a client — including when they only say \"write up what we shipped this sprint\" or \"manda um resumo do que saiu pro cliente\". Also use it when an existing release-notes draft needs screenshots, a logo, or has images that arrive broken in Gmail. Covers: triaging commits for user-facing impact, capturing app screenshots without typing credentials, baking bottom fades into images, and getting images to survive the trip into an email client. This is the factual \"what changed\" changelog — for a persuasive client-facing value or results deck, use brand-deliverables instead. Not for internal CHANGELOG.md files aimed at developers, and not for release *tagging* or deployment."
metadata:
  version: 1.0.0
---

# Release Notes

Two jobs, and the first one is the one that gets skipped. **Deciding what shipped** is editorial work — most commits are invisible to users and a few unremarkable-looking ones are the headline. **Showing it** is production work — a screenshot of a running app, cut so it belongs on the page.

### This skill vs. `brand-deliverables`

They're complementary and it's worth being clear which one the request is:

|  | **release-notes** (here) | **brand-deliverables** |
|---|---|---|
| Question answered | "What changed?" | "Was it worth it?" |
| Register | Factual, neutral, skimmable | Persuasive, framed, narrative |
| Audience | People who use the product | A client or stakeholder deciding |
| Unit | A shipped capability | An outcome or a metric |

A changelog that argues its own value reads like marketing and gets trusted less. A value deck that merely lists commits fails to make its case. Keep them apart.

Borrow freely in one direction, though: the **mechanics** of email HTML — tables with inline styles, what survives a paste, the copy button, the asset inliner — are documented once in `brand-deliverables/references/email.md`. Read that file for the how; this skill decides the what.

### Start from the template

`assets/release-email.template.html` is the Zapad-branded release email, already built: mesh band, wordmark, the 54px purple rule, eyebrow + title, one repeatable section block, an "E mais" list, and the copy button wired up. Fill the `__MARKERS__` and inline the images:

```bash
cp ${CLAUDE_PLUGIN_ROOT}/skills/release-notes/assets/release-email.template.html notes.src.html
# …fill __TITULO__, __PERIODO__, __SECAO_*__, __ITEM__, __RODAPE__…
python3 ${CLAUDE_PLUGIN_ROOT}/skills/brand-deliverables/scripts/inline_assets.py \
  notes.src.html notes.html \
  --asset MESH=${CLAUDE_PLUGIN_ROOT}/skills/release-notes/assets/mesh-band.jpg \
  --asset ZAPAD=${CLAUDE_PLUGIN_ROOT}/skills/release-notes/assets/zapad-logo.png \
  --asset SECAO_IMAGEM=shots/inbox.jpg
```

Keep editing the `.src.html` — the output carries base64 mid-markup and is not hand-editable.

It departs from the brand email standard in one way, deliberately. That standard says **no images**, because a linked image shows a broken box until the reader clicks "show images". Screenshots are the whole point here, and inlined as data URIs they arrive as real attachments that display immediately — so the reasoning behind the rule doesn't apply. Worth saying out loud when you hand the work over, so it doesn't look like the convention was forgotten.

`assets/mesh-band.jpg` and `assets/zapad-logo.png` are derivatives sized for this layout — 2.5 KB and 28 KB against the 207 KB and 126 KB masters. That matters because every byte is inlined as base64 and inflates by a third; the full-size mesh alone pushed the email past 440 KB. The masters stay in `brand-deliverables/assets/` as the single source of truth — re-cut from there if the brand changes, don't edit these.

---

## 1. Triage the history

```bash
git log --since="3 days ago" --pretty=format:"%h|%ad|%an|%s" --date=short
```

**Check the window isn't empty before writing anything.** A request for "the last 7 days" is a guess about when work happened, not a statement of fact, and repos go quiet. If the range comes back empty, find the real one and say so rather than shipping a hollow email:

```bash
git log --all -1 --date=short --pretty=format:"latest commit: %ad %h %s"
```

Then write the notes for the last window where work actually landed, **label those dates explicitly in the email**, and tell the user the literal range they asked for was empty. Silently substituting a different period produces an email dated "this week" describing work from a month ago.

Two other things that quietly corrupt the list:

- **Uncommitted work in the tree has not shipped.** `git status` may show a whole feature in progress. It isn't news until it's released, so leave it out.
- **Check whether a draft for this window already exists** (`release-notes*.html` in the repo root, a previous email). If one does, the user may have sent it — say so before they send a near-duplicate. Do not inherit its claims either: trace every line back to a commit in the window, because an earlier draft can contain assertions that were never true or belong to a different release.

Then read the **full bodies** of anything that might be user-facing:

```bash
git log -1 --format=%B <sha>
```

This second pass is not optional, and it's where the judgment lives. Subject lines are written for other developers and they misrepresent user impact in both directions:

- `feat:` is often plumbing a user will never notice — a client library realigned to a new API version, a payload class extracted behind an interface.
- `fix:` is sometimes the whole story. "stop the composer clearing the message being typed next" is a bug report a customer would have written themselves.
- `refactor:` occasionally deletes a screen people use daily, which is very much news.

Drop merge commits, test-only commits, ADRs and docs, dependency bumps, and tooling chores. What survives gets **grouped by user-visible capability, not by commit** — five commits building one channel integration are one section with one heading.

Ask yourself, per item: *could a customer notice this without being told?* If no, cut it. A release-notes email that lists a mass-assignment guard is one nobody finishes reading.

### Length

One or two sentences per feature, and **around 500–600 words of visible copy for a whole release**. That budget is not arbitrary: left unconstrained this task reliably lands near 900 words, which is the length at which people stop reading and the one users complain about first.

Release notes are skimmed, not read — the reader wants to know whether anything affects them, then leave. If you find yourself explaining *how* something works, you've drifted into documentation. The commit body has the depth; the email has the headline.

Claims must be traceable to a commit you actually read. "Now sends a notification" is a promise, and if the commit only changed how a mention is *displayed*, you have invented a feature the product does not have.

---

## 2. Write in the language the UI speaks

Check what users actually see, not what the repo is written in. Commit messages and code comments are frequently English in an app whose interface is not — that mismatch is easy to miss and produces notes in the wrong language for the audience.

```bash
php artisan config:show app.locale   # Laravel
```

Better still, look at a screenshot once the app is up (step 3) — the rendered UI is the ground truth, and it also catches untranslated strings worth reporting back as bugs.

---

## 3. Capture the screenshots

Load the `claude-in-chrome` skill first; the browser tools need it. Details that are easy to get wrong are in **`references/capture.md`** — read it before the first navigation, because two of them (authentication and demo data) are much cheaper to handle up front than to discover after a capture session.

The short version:

- **Never type a password**, even a seeded dev one. Get a session by asking the framework for it — in Laravel, a temporary `local`-only route calling `auth()->loginUsingId()`, reverted afterwards.
- **Look at the seeded data before capturing.** Dev databases are full of `Teste` and `new deal` and lorem ipsum. A screenshot of that undermines the email more than having no screenshot at all.
- **Keep error states out of the frame.** Failed sends, empty states, and red toasts are honest but they are not what the section is illustrating. Scroll to a clean part of the view.
- Window at 1440×900, then downscale to 1200px wide for a 600px email column so it stays sharp on retina.

---

## 4. Fade the bottom of each screenshot

**Only when the screenshot's own background is close to the card colour.** The fade dissolves a screenshot into the page; it does not bridge a contrast gap. A dark app screenshot faded toward a white card produces a grey smear where the two meet — worse than the hard edge it was meant to fix. Decide first:

| Card | Screenshot | Do |
|---|---|---|
| Dark, ≈ the app's own chrome | Dark app | **Fade** — they meet invisibly |
| Light (the Zapad template) | Dark app | **No fade.** Contain it: 1px `#E4DCF3` border, `border-radius:8px` on all four corners |
| Light | Light app | Fade works, but a border usually reads better |

When it does apply, the fade has to be **baked into the image file** — a CSS gradient overlay or a pseudo-element is exactly the kind of thing email clients strip, so it would work in your preview and vanish for the reader.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/release-notes/scripts/fade_bottom.py shot.jpg out.jpg --bg '#13161e'
```

The script composites a transparent→background gradient over the bottom of the image and flattens it, so the result is an ordinary JPEG that already dissolves into a page of that colour. It defaults to 30% of the image height; pass `--depth` to change it.

Two consequences worth knowing:

- **Drop the image's border and square its bottom corners** (`border:0; border-radius:10px 10px 0 0`). A 1px border would draw a line straight across the fade, which is worse than no fade.
- **Shorten the fade when the bottom of the frame is the point.** If the section is about a button in the composer and the composer is at the bottom of the shot, a 30% fade erases the subject. Around 15% keeps it legible.

The fade only works against a known solid background. If the email's card colour changes, the images have to be re-cut — keep the unfaded originals as masters.

---

## 5. Get the images into the email

This is where the work usually fails, and the failure is silent: the page looks right in a browser and arrives in Gmail with empty boxes.

**Relative paths and `localhost` URLs do not survive.** Mail clients resolve image sources on their own servers, which can reach neither `release-notes-assets/shot.jpg` nor `http://localhost:8899/…`. Anything unreachable is dropped.

Pick by destination:

| Destination | Use | Why |
|---|---|---|
| Pasted by hand into Gmail/Outlook | **base64 data URIs** | Self-contained; compose windows convert them to real attachments |
| Mailchimp, Resend, any bulk sender | **absolute `https://` URLs** | Senders reject data URIs at send time |

**Never leave a live `<img>` pointing at an image you don't have.** A `src="cid:logo"` or a path you intend to fill in later renders as a broken box, and a placeholder nobody notices goes out to every recipient. If the notes are being handed over for screenshots to be added later, leave each slot as an **HTML comment** carrying the correct markup — invisible if forgotten, one uncomment away when the image exists:

```html
<!-- <img src="inbox-fade.jpg" width="528" alt="Caixa de entrada"
     style="display:block;width:100%;max-width:528px;height:auto;border:0;border-radius:10px 10px 0 0;"> -->
```

For data URIs, reuse the inliner from the brand skill rather than writing another one — it takes `__MARKER__` placeholders and swaps in the encoded file:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/brand-deliverables/scripts/inline_assets.py \
  notes.src.html notes.html --asset SHOT1=assets/inbox-fade.jpg
```

Keep editing the `.src.html`; the output has base64 blobs in the middle of the markup and is not reviewable by hand.

### Make the copy step reliable

Select-all-copy from a rendered page is lossy and depends on the browser. The dependable pattern is a **wrapper page with a copy button** that writes the block to the clipboard as `text/html` — `brand-deliverables/references/email.md` has the `ClipboardItem` snippet and the required fallback. Build the wrapper around the notes block rather than handing over a bare HTML file.

### Two small things that cost an hour each

- Put `<meta charset="utf-8">` at the top of the fragment. Without it, a local preview renders `são` as `sÃ£o` and you will go looking for an encoding bug in the wrong place. Mail clients set charset from message headers and ignore the stray tag.
- `file://` URLs cannot be opened by the browser tools. Serve the directory instead, and background it so it doesn't block:

```bash
python3 -m http.server 8899    # via Bash run_in_background: true
```

### The no-images convention

The Zapad email standard says no images, because a recipient sees broken placeholders until they click "show images". That reasoning holds for *linked* images. Screenshots pasted into a compose window become attachments and display immediately, so illustrated release notes are a deliberate exception — worth stating when you hand the work over, so nobody thinks the convention was forgotten.

---

## 6. Logos

Email clients do not render SVG. Convert once, at 2× the display size:

```bash
rsvg-convert -w 240 -h 240 public/favicon.svg -o assets/logo.png
```

An app's favicon is often the cleanest available mark, already cropped and on-brand. Check there before asking for a file.

**Don't invent the product's name.** `APP_NAME` is often unset in development, so the UI says "Laravel" and there is nothing authoritative to copy. Inferring a name from the repo directory or a commit message puts a name the company may not use in front of every customer. Ask, or leave it out — a release email works fine without one.

---

## Leave the repo as you found it

This workflow touches things outside the deliverable — a temporary route, seeded rows, a background server. Before reporting done:

```bash
git status --short          # temp route reverted?
pkill -f "http.server 8899" # preview server stopped?
```

Say plainly what you changed in the dev database and how to undo it. Silently mutating someone's local data, even data that was already fake, is the kind of thing they find out about a week later while debugging something unrelated.

Generated files (`release-notes.html`, `assets/`) land untracked in the repo root. Mention them so the user can gitignore or move them.

---

## Project specifics

This skill ships with the plugin and runs against whatever repo you're in. The values that
differ per project — which tenant holds the data, how to get a session, mass-assignment
quirks when seeding, the card colour, where the logo lives — belong in a per-project
reference.

**Write that reference into the project's own repo, not into this plugin.** A plugin is
reinstalled and updated wholesale, so a file added under it is lost on the next update, and
it would follow you into every other repo where it is wrong. `.claude/skills/release-notes-<project>/SKILL.md`
in the project, or a section in its `CLAUDE.md`, both survive.

Use these headings — Language, Running the app, Session for capture, Screens worth
capturing, Seeding, Design, Logo. Working them out costs maybe ten minutes the first time
and nothing on every release after.

**Read a project reference only when the working directory is that project.** In any other
repo it is wrong in its specifics and will send you to routes and models that don't exist.
