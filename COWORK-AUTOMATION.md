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
3. Clone the repo somewhere Cowork can read/write, e.g. `~/prompted-site`.
4. Keep an existing article as the template — any `<slug>/index.html`
   (start from `the-conversation-was-compounding/index.html`).

---

## Task 1 — Package & Publish (run ON-DEMAND, when a piece is done)

Save as a Cowork task. Trigger it yourself; do **not** `/schedule` it.

> **Standing instructions:**
> You are packaging a finished Prompted.daily piece. I'll give you the essay text and its
> engineered prompt(s) and a short slug. If I give you a Medium URL instead, fetch it and
> extract the essay body and prompt block(s) — and if the prompt boundary is at all
> ambiguous, STOP and ask me rather than guessing.
>
> Working in `~/prompted-site`:
> 1. Copy the template `the-conversation-was-compounding/index.html` to a new
>    `<slug>/index.html`. Keep all styling and the copy-button behavior.
> 2. Replace title, kicker, dek, date, byline, essay body, and prompt block(s). Put each
>    prompt in its own copy-block card. Preserve house voice in any copy you write: no "I"
>    openers, minimal em-dashes, active prose, specific over general.
> 3. Set the page `<link rel="canonical">` to `https://prompteddaily.com/<slug>/`.
> 4. On `index.html`, add a card to the `.cards` grid: kicker, title, a one-line blurb,
>    `href="/<slug>/"`, CTA "Read + run the prompt". Draft the blurb but FLAG it — the
>    blurb is my voice to approve, not yours to finalize.
> 5. If a Medium URL exists, add "Also published on Medium" to the article footer.
> 6. STOP. Show me the rendered article page and the new card. Do not commit or push yet.
> 7. After I approve, commit and push to `main`. Report the live URL.
> 8. Remind me to set the Medium post's canonical link to the site URL (manual, my step).

---

## Task 2 — Publishing health check (SCHEDULE this one, weekly)

Save as a Cowork task, then `/schedule` for Monday 08:00.

> **Standing instructions:**
> Audit the live site. Change no files.
> 1. Fetch `https://prompteddaily.com/` and every `/<slug>/` article page.
> 2. Confirm each returns 200 and its canonical resolves to itself.
> 3. List every homepage card still pointing to `medium.com` — migration candidates.
> 4. Flag broken links, and any article missing its prompt copy-block.
> 5. Save a short report to `~/prompted-site/_reports/health-<date>.md` and notify me.

---

## Why this split
On-demand for publishing (you don't publish on a clock). Scheduled for monitoring (a timer
is exactly right for a health sweep). The human gate in Task 1 sits precisely where your
judgment is load-bearing — the card copy and the integrity of the lifted prompt.
