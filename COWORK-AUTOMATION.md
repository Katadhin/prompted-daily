# Prompted.daily — Cowork automation kit

Automate the *packaging cascade*, never the thinking. A finished essay+prompt goes in;
an on-site page, a homepage card, canonical tags, and a GitHub push come out — with a
human look before anything goes live.

## Two honest limits
- **The fragile joint is extraction.** Lifting "the essay" and "the prompt" cleanly is
  fuzzy (prompt boundaries, pull-quotes, multi-part prompts). That's the product's hero
  element, so the task always pauses for your review before pushing.
- **Medium's canonical is manual.** Pointing the Medium copy back at the site is a
  per-post setting in Medium (Story → Settings → Advanced → canonical link). No push can
  do it. The task will remind you.

## Setup (once)
1. Cowork on a paid plan. Scheduled/on-demand tasks run **only while Claude Desktop is
   open and the computer is awake** — not a cloud agent.
2. Connect GitHub through **Claude Code** (handles git natively) or a GitHub connector you
   authorize in-app. Your credentials stay in the connector; Claude never stores them.
3. Point Cowork at the existing working clone, `~/Documents/GitHub/prompted-site` —
   don't let it clone a second copy elsewhere; two local repos will drift.
4. Confirm Pillow is installed (`pip install Pillow --break-system-packages`) — the
   generator needs it for header image processing.

---

## Task 1 — Package & Publish (run ON-DEMAND, when a piece is done)

Save as a Cowork task. Trigger it yourself; do **not** `/schedule` it.

> **Standing instructions:**
> You are packaging a finished Prompted.daily piece for on-site canonical publishing,
> the default treatment for every new essay. I'll give you the essay text and its
> engineered prompt(s) and a short slug. If I give you a Medium URL instead, fetch it
> and extract the essay body and prompt block(s), and if the prompt boundary is at all
> ambiguous, STOP and ask me rather than guessing — the script doesn't make that call.
>
> Working in `~/Documents/GitHub/prompted-site`:
> 1. Draft `posts/<slug>.json` (see the field list in `tools/build_essay.py`'s docstring).
>    `body_html` is the essay as raw HTML. If I gave you a header image, set
>    `hero_image.src` to it; if not, omit `hero_image` entirely rather than inventing one.
> 2. Draft `card_blurb` in house voice: no "I" openers, minimal em-dashes, active prose,
>    specific over general. This is my voice to approve, not yours to finalize.
> 3. Run `python3 tools/build_essay.py posts/<slug>.json --dry-run` to catch spec problems
>    with nothing written yet. Fix anything it flags, then run it for real (no flag).
> 4. STOP. Show me the rendered article page and the new card the script printed. Do not
>    commit or push yet — the script writing files faster doesn't change this gate.
> 5. After I approve, commit and push to `main`. Report the live URL.
> 6. If a Medium URL exists or will exist, remind me to set that post's canonical link
>    to the site URL — manual, my step, no script touches Medium.

---

## Task 2 — Publishing health check (SCHEDULE this one, weekly)

Save as a Cowork task, then `/schedule` for Monday 08:00.

> **Standing instructions:**
> Audit the live site. Change no files.
> 1. Fetch `https://prompteddaily.com/` and every `/<slug>/` article page.
> 2. Confirm each returns 200 and its canonical resolves to itself.
> 3. List every homepage card still pointing to `medium.com` — migration candidates.
> 4. Flag broken links, and any article missing its prompt copy-block.
> 5. Save a short report to `~/Documents/GitHub/prompted-site/_reports/health-<date>.md` and notify me.

---

## Task 3 — Mid-week story-prep nudge (SCHEDULE this one, weekly)

Save as a Cowork task, then `/schedule` for Wednesday, whatever time you're usually at
Desktop. This nudges based on actual repo signal, not a blind weekly ping.

> **Standing instructions:**
> Check on story-prep timing. Change no files, this is a nudge only, no writes, no git actions.
> 1. In `~/Documents/GitHub/prompted-site`, run
>    `git log -1 --format=%cd --date=short -- posts/` to find when the last new post
>    spec was actually added, not just when index.html last changed.
> 2. Check whether any file in `posts/` has no matching `<slug>/index.html` folder — that
>    means a spec was drafted but never built, an unfinished piece, not a shipped one.
> 3. If something is unfinished, name it directly: "You have a spec for <slug> that
>    hasn't been built yet."
> 4. If it has been 5 or more days since the last new post AND nothing is mid-build,
>    send a nudge naming the last piece and the day count: "It's been N days since
>    [title]. Worth opening a chat to start drafting the next one, or blocking time to
>    finish whatever's underway."
> 5. If it has been fewer than 5 days and nothing is stuck mid-build, stay silent.
>    No news is the correct outcome most weeks, don't nudge just because it's Wednesday.

---

## Why this split
On-demand for publishing (you don't publish on a clock). Scheduled for monitoring (a timer
is exactly right for a health sweep). The human gate in Task 1 sits precisely where your
judgment is load-bearing — the card copy and the integrity of the lifted prompt.
