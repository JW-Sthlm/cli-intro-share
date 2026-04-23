# cli-intro-share

Public preview of the **Copilot CLI for Partner Work** intro session storyboard and presenter deck.

Published via GitHub Pages — reviewers get a stable link, push updates as they're made.

## Update workflow

```powershell
cd C:\Users\jwallquist\projects\cli-intro-share
.\sync.ps1 "updated demo talking points"
```

`sync.ps1` copies the latest `storyboard.html` + deck from `../cli-intro/v2/deck/`, commits, and pushes. Reviewers hard-refresh (Ctrl+F5) — Pages typically updates within ~1 minute.

## Files

- `index.html` — landing page with links
- `storyboard.html` — reviewer doc (TL;DR + slide-by-slide script + demo cards)
- `presenter.html` — the 10-slide deck as it will be delivered

Source of truth lives in `../cli-intro/v2/`. This repo is a published mirror only.
