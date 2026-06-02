# Copilot Skill Deck Maker

A small Copilot skill for turning notes, meeting recaps, or a topic into a single-file HTML presentation.

It was built for Microsoft partner consultants in the AI Operator Intro, the business-side Copilot CLI course. The idea is simple: you should be able to paste rough material into Copilot and get a deck you can open in a browser, send as one file, and present without fighting formatting late in the evening.

The skill is inspired by Johan's larger Slidemaster agent. This version is intentionally smaller. No framework clone. No PowerPoint dependency. No build step.

## Why it exists

Consultants often leave a meeting with useful notes and a weak next artifact.

This skill gives you a clean first deck from that raw material:

- One self-contained HTML file.
- Partner brand-matched look when you provide a homepage URL.
- Built-in presenter notes via `?presenter=notes`.
- Arrow-key navigation and fullscreen.
- Clear anti-AI writing rules baked into the workflow.

It will not replace your judgement. Good. That is the point.

## Install in Copilot CLI

### 1. Copy the skill file

Create the skill folder and copy `SKILL.md` into it.

```powershell
New-Item -ItemType Directory -Force "$HOME\.copilot\skills\copilot-skill-deck-maker"
Copy-Item ".\SKILL.md" "$HOME\.copilot\skills\copilot-skill-deck-maker\SKILL.md" -Force
```

On macOS or Linux:

```bash
mkdir -p ~/.copilot/skills/copilot-skill-deck-maker
cp ./SKILL.md ~/.copilot/skills/copilot-skill-deck-maker/SKILL.md
```

### 2. Restart your Copilot CLI session

Skills are loaded when the session starts.

### 3. Try it

```text
Make a deck from these notes: <paste notes>
```

Or:

```text
Build slides about our AI readiness workshop. Use https://www.example-partner.com for brand matching.
```

## Use it in VS Code Copilot Chat

VS Code Copilot Chat does not load Copilot CLI skills from `~/.copilot/skills` automatically.

Use one of these paths:

1. Create `.github/copilot-instructions.md` in your repo and paste the contents of `SKILL.md` under a clear heading.
2. Or create `.github/instructions/copilot-skill-deck-maker.instructions.md` and paste the same content there.
3. Start a new chat and ask Copilot to follow the deck maker instructions.

Keep the instruction file with the project if you want the whole team to use it.

## Example prompt

```text
Make a deck from these notes.
Audience: partner delivery leads.
Length: 5 slides.
Brand: https://www.example-partner.com
Notes:
- The workshop showed that consultants lose time after meetings.
- The team wants faster recap, deck, and follow-up creation.
- Main risk is trusting the first draft too much.
- Next step is a two-week pilot with three account teams.
```

## What you get

Open the example deck here:

[example.html](./example.html)

You get a browser presentation with branded styling, speaker notes, and a clean next step. One file. Send it, open it, present it.

Made for the [AI Operator Intro](../../) by Johan Wallquist, for Microsoft partner consultants.
