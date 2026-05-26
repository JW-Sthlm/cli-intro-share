# Copilot Instructions — cli-intro-share

## What this repo is

Public-facing landing pages for everything Johan ships externally on Copilot CLI. Two things live here today, but anything else partner-facing or community-facing belongs here too:

1. **`/operator-hour/`** — the weekly "Operator Hour" internal series (Microsoft non-coders, partner-facing roles). One landing page + one folder per episode (`s1e1/`, `s1e2/`, …) + a few standalone resources (`use-case-finder.html`).
2. **`/course/`** — eight self-paced lessons of the Copilot CLI course (the longer-form companion to the series).

Hosted on GitHub Pages at https://jw-sthlm.github.io/cli-intro-share/.

## Operator Hour — series facts

- Six weekly episodes, Tuesdays 10:30 CET, 45 min each (5 + 20 + 10 + 5 format).
- Season 1 audience: EMEA EPS + GCPS partner-facing non-coders.
- Host: Johan. Sidekick: **Otto** — a Copilot agent that runs in the cohort Teams team + meeting chat.
- Cohort Teams team: **AI-First Operator** (public-to-Microsoft-tenant). Anyone clicks to join.
- Always speak in plain language. Audience is not developers. "Just talk to it" beats any syntax.

## Visual conventions

Stay in the existing design system. Don't introduce new fonts, palettes, or spacing scales.

**Palette (defined in every page's `:root`):**
- `--bg:#0D1117`, `--bg-2:#010409`, `--panel:#161B22`, `--border:#30363D`
- `--text:#E6EDF3`, `--muted:#A6B0BC`
- `--teal:#39D2C0` — primary accent, "active / live / actionable"
- `--purple:#8957E5`, `--green:#3FB950`, `--amber:#D29922`, `--pink:#F778BA`

**Type:**
- Display: Mona Sans (weights 400, 600, 700, 800, 900)
- Mono: JetBrains Mono (weights 400, 600)

**Patterns (don't re-invent — reuse):**

| Class | Use for |
|-------|---------|
| `.card` | Primary clickable action (Use Case Finder, Recording, etc). Solid panel + border. |
| `.card-tag.teal` / `.amber` / `.muted` | Status pill at the bottom of a card. |
| `.section-label` | Small uppercase mono label above a group of cards. |
| `.ep` | One row in the season list. `<a>` if linkable, `<div>` if not yet. |
| `.ep--published` | **Shipped** episode row. Adds: teal accent left bar (4px), gradient tint fading right, outer glow, slight margin so it floats above the rest. |
| `.ep-badge` | Pill inside `.ep--published .ep-title`, content: `▶ Watch recap`. |
| `.invite-note` | "Not on the calendar invite?" sidebar. Same teal-accent-left + gradient identity as `.ep--published` — they're siblings, not separate styles. |
| `.takehome` | Subtle teal gradient block, the one CTA per episode page. |
| `.pull` | Quote callout with teal left border. |
| `.refrain` | Closing line on every episode page. |

**The "edge-color" rule:** anything that has a `border-left:3-4px solid var(--teal)` plus a teal-to-transparent gradient is part of the same family — published rows, invite-notes, pull quotes. If you add a new component that's "live / actionable", give it that same identity. Don't invent a second accent treatment.

**Glow rule:** only the *currently most recent* published episode gets the outer glow. Older published episodes keep the accent bar + gradient but drop the heavy 28px outer glow (otherwise the page lights up like a Christmas tree by episode three). Change the rule when we get there; for now, single glowing row.

## Voice rules for episode pages

Follow Johan's voice profile (in his global instructions). The high-leverage rules for episode pages specifically:

- **Closing refrain mandatory.** Every episode page ends with `<p class="refrain"><strong>Still not a developer.</strong> …</p>`. The second sentence is context-specific to *that* episode. Never reuse the second sentence verbatim across episodes.
- **No em dashes.** Use full stops, commas, parentheses, or "but". Hyphen-space-hyphen for mid-sentence pauses is allowed.
- **No rule-of-three reflex.** Max one triplet per page.
- **Vary sentence length.** Mix short punchy sentences with longer ones. Never let three sentences in a row land in 12-20 words.
- **"Operator move"** is the recurring callout pattern in the Recap section — `<p><strong>Operator move:</strong> …</p>` followed by the one action the audience should take from this episode.
- **"What the room asked"** paragraph in the Recap captures live Q&A. Pattern: question (paraphrased) followed by Otto/Johan's answer in parentheses.
- Sensory anchor (rainy evening / coffee / etc) is optional. Only use when the moment IS the story. Most episode pages don't need it.

## Episode page template

`s1e1/index.html` is canonical. Copy it for new episodes and update:

1. `<title>` and the `.tag` line (`S1 · Episode N · Tue MMM DD YYYY`)
2. `<h1>` with the accent span on the punchy half
3. `.sub` — one-line standfirst
4. Recap section — narrative + pull quote + "What the room asked" paragraph + operator move
5. Take-home block — the one action this week
6. Resources cards — recording, prompts, anything specific to this episode
7. What's next cards — the immediate next episode + the self-service course
8. Refrain
9. Meta — episode + host + feedback

**Pre-session vs post-session state:** the same URL serves both. Pre-session, the page is a "preview" — what we'll cover, what to bring. Post-session evening, swap recap content in and flip the landing page row to `.ep--published`.

## Broadcast workflow (post-session)

Full checklist lives in [`operator-hour/PLAYBOOK.md`](../operator-hour/PLAYBOOK.md). The short version, in order:

1. Update the episode page recap content + add the recording link to the Recording card.
2. Flip the landing page row to `.ep--published` and add the `▶ Watch recap` badge.
3. Move the previous episode's glow off (drop heavy outer glow, keep accent + gradient).
4. Post Teams meeting chat wrap message via agency MCP (`agency mcp teams --transport http --port 0`).
5. Create Outlook broadcast email draft via COM (template lives in the session workspace).
6. Set Stream recording description + chapters (manual UI paste — no API).
7. Refresh Otto with the episode's transcript + recap.
8. Commit, push, verify Pages deploys (Actions workflow auto-fires on push to main).

## GitHub Pages deployment

- **Build type:** GitHub Actions (`build_type=workflow`). Set via `gh api -X PUT repos/JW-Sthlm/cli-intro-share/pages -f build_type=workflow`.
- **Workflow:** [`.github/workflows/deploy-pages.yml`](workflows/deploy-pages.yml). Uses `actions/checkout@v4`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`. **Do not add `actions/configure-pages`** — it failed repeatedly during a codeload outage on May 26 2026 and is not needed for pure static HTML.
- **`.nojekyll`** at repo root is required — bypasses Jekyll, since this is pure static HTML.
- **Verify after push:** wait ~60s after push, then hit `https://jw-sthlm.github.io/cli-intro-share/...?nocache=$(Get-Random)` to skip cache. Hard-refresh in the browser is Ctrl+F5.
- If a workflow run fails on action download (codeload.github.com errors), GitHub Actions is degraded. Wait 5-15 min and rerun via `gh run rerun <id>`.

## Conventions when editing

- Inline styles in HTML are OK for one-off tweaks, but if a pattern repeats twice, hoist it to a class.
- Don't introduce a CSS framework or build step. The whole site is hand-written HTML + inline `<style>` per page. Keep it that way.
- Each page has its own `:root` palette and `<style>` block. That's intentional — pages are standalone and self-contained.
- Never reformat or reflow the entire stylesheet of an existing page on a small change. Surgical edits only.
- Outbound URLs to LinkedIn, Stream, Teams join links etc. always include `target="_blank" rel="noopener"`.
- The `Mona Sans` font is preferred over `Plus Jakarta Sans` for cli-intro-share. Other Johan repos may use Plus Jakarta Sans — that's their call.
