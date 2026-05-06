# cli-intro-share

Public-facing companion site for the **Copilot CLI for Partner Work** intro session.

Live at **https://jw-sthlm.github.io/cli-intro-share/**.

This is the surface participants land on. Slide deck, setup guide, exercises, self-service course, and reference materials. The internal source repo (`cli-intro`) stays separate so workshop facilitators can iterate without exposing notes, validation kits, or demo prep.

## What lives here

| Path | Purpose |
|------|---------|
| `index.html` | Landing page with cards for everything below |
| `setup.html` | Pre-work setup guide (the page participants run before the session) |
| `deck.html` / `print.html` | Live workshop deck and printable handout |
| `course/` | Self-service course (M0 to M7), business and technical tracks |
| `pre-work/` | `setup-guide.md`, `verify.ps1`, `verify-checklist.md`, `express-setup.ps1` |
| `exercises/` | Workshop exercises (1, 1B, 2, 3) and the synthetic input file used in Exercise 2 |
| `reference/` | `cheat-sheet.md`, `troubleshooting.md`, `after-session-resources.md` |
| `setup-clinic/` | Public-facing clinic announcement and participant prep |
| `extras/copilot-overview/` | Reference example for a packaged skill |
| `GETTING-STARTED.md` | "What is a repo?" primer for non-technical participants |

## Update workflow

Decks: run `sync.ps1` to refresh `deck.html` and `print.html` from `../cli-intro/v2/deck/`.

```powershell
cd C:\Users\jwallquist\projects\cli-intro-share
.\sync.ps1 "updated demo talking points"
```

Course and reference content: edit in `cli-intro/v2/...`, then copy across (sync.ps1 currently only handles decks; markdown sync is on the backlog).

Pages typically updates within ~1 minute. Reviewers hard-refresh (Ctrl+F5).

## Source

- This repo: published mirror, reviewer-facing
- Source of truth: [github.com/JW-Sthlm/cli-intro](https://github.com/JW-Sthlm/cli-intro) (private or public, depending on phase)