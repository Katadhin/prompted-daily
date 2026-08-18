# Prompted.daily

Static single-file site for the publication. No build step, no dependencies — same drop-in
pattern as Throttle & Rust. Everything is in `index.html`.

## Deploy to GitHub Pages

**New repo (recommended for a custom domain):**
1. Create a repo, e.g. `prompted-daily`.
2. Drop `index.html`, `README.md`, and `CNAME` into the root, commit, push to `main`.
3. Repo → **Settings → Pages** → Source: *Deploy from a branch* → Branch: `main` / `/root` → Save.
4. Live at `https://<user>.github.io/prompted-daily/` within a minute or two.

## Custom domain (prompteddaily.com)

1. Keep the `CNAME` file in the repo root (it contains `prompteddaily.com`).
2. At your DNS registrar, point the domain at GitHub Pages:
   - Apex `prompteddaily.com` → four A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` → CNAME to `<user>.github.io`
3. Settings → Pages → enter `prompteddaily.com`, check **Enforce HTTPS** once the cert issues.
   *(Confirm current GitHub Pages IPs in their docs before you set DNS — they change rarely but do change.)*

## Two wire-ups before it's fully live

1. **Social URLs** — replace the `#` hrefs for LinkedIn and Facebook in the footer with your real profiles.
2. **Canonical + share image** — uncomment the `og:url` / `og:image` meta tags and add a `share.png`
   once the domain resolves, so links posted to FB/LinkedIn render a real card.

Recent-piece cards currently link to Medium (`@katadhin`). Swap each `href` for the canonical
Prompted.daily URL as posts move onto this domain.

## What this site is for

The center of gravity is the engineered prompt, not a subscribe box. Channels (FB / LinkedIn / Medium)
carry the hook and the fork; the site is the only container that holds the full unit — essay plus the
prompt a reader can run. No email capture, by design.
