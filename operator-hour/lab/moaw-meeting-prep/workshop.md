---
published: false
type: workshop
title: Prep for a meeting, on two surfaces
short_title: Prep for a meeting
description: One job almost everyone in a partner role does every week. Run it twice, on M365 Copilot and on Copilot CLI, and feel which door fits.
level: beginner
authors:
  - Johan Wallquist
contacts:
  - "linkedin.com/in/johanwallquist"
duration_minutes: 20
tags: copilot, ai, partner, productivity, operator-hour
sections_title:
  - The scenario
  - M365 Copilot (Ask)
  - Copilot CLI (Hand off)
  - Compare and pick
---

# Prep for a meeting

One job almost everyone in a partner role does every week. You'll run it twice, on two different surfaces, and feel why one fits a quick reply and the other fits real homework. Same task. Two doors. You decide which you'd reach for.

## The scenario

You have a meeting tomorrow with **Northwind Traders**, a fictional company we all share so nobody touches real data. You want a one-page brief before you walk in: who they are, what changed recently, three things worth talking about, and a short follow-up email you can send after.

<div class="task" data-title="Your sample input">

> Copy the fact pack below. It's the only input you need for both surfaces. In real life you'd point the tools at your own notes instead.

</div>

```text
Northwind Traders is a mid-size logistics and distribution company, around 1,200 staff, HQ in Rotterdam. They run a mix of on-prem warehouse systems and some cloud. Last quarter they announced a push into same-day delivery and said data is their bottleneck. Our last call, three months ago: they were curious about analytics but worried about cost and skills. Action left open: send them a short view on where to start.
```

<div class="info" data-title="Safe to share">

> Northwind Traders is fictional. Nothing here is sensitive. Don't paste real customer names, real pipeline numbers, or anything confidential into AI tools during this lab. The sample data models good practice.

</div>

---

# M365 Copilot (Ask)

**Band: Ask. Setup: none.** The fastest door. It's already open in Teams, Word, Outlook, or the Copilot app. No install. You paste, it answers, you watch the whole time. Best when the job is small and you want it now.

## Step 1: Open Copilot where you already work

Teams, Word, Outlook, or [the Copilot app](https://m365.cloud.microsoft/chat). Any of them. You need a Microsoft 365 Copilot licence, which most of you already have.

## Step 2: Paste the prompt with the fact pack

Copy the prompt below, then paste the sample fact pack from the scenario where it says to. Send it.

```text
I have a meeting tomorrow with a company. Using only the facts I paste below, write me a one-page prep brief I can read in two minutes:

- Who they are, in two lines.
- What changed recently and why it matters to them.
- Three things worth talking about.
- Three smart questions I could ask.

Keep it plain and short. Don't invent anything that isn't in my facts.

Here are the facts:
[paste the Northwind fact pack here]
```

## Step 3: Ask it to draft the follow-up

Stay in the same chat and ask for the email. It remembers the brief.

```text
Now write a short, warm follow-up email I can send after the meeting. Reference the same three talking points. Five sentences, no jargon, end with one clear next step.
```

<div class="info" data-title="What good looks like">

> A tidy brief and an email in under a minute, without leaving the app you were already in. For a quick prep on something you mostly know, this is hard to beat.

</div>

<div class="warning" data-title="Where it breaks">

> It only knows what you paste, plus what's already in your own M365 files. It won't go dig up Northwind's latest news on the open web, it won't pull five sources together, and it won't save you a reusable file. Every step is you asking, it answering. Push past a quick job and you feel the ceiling.

</div>

---

# Copilot CLI (Hand off)

**Band: Hand off. Setup: one-time install, a terminal.** The other door. You brief it once and it does the homework: plans the work, pulls from more than one place, writes a file you keep, drafts the email, and tells you what it couldn't verify. More setup, far higher ceiling. Best when the job is real work, not a one-liner.

## Step 1: Install it once

If you've never run the CLI, follow the [setup guide](https://jw-sthlm.github.io/cli-intro-share/setup.html) first. Fifteen minutes, one time. You need GitHub Copilot access. After that, this lab takes minutes.

## Step 2: Drop the fact pack in a folder

Make an empty folder, open the CLI in it, and save the sample fact pack as `northwind.md`. This is your safe sample input.

## Step 3: Hand it the whole job in one go

One brief, many steps. It writes its own plan and works through it.

```text
Read northwind.md in this folder. I'm meeting this company tomorrow.

Do the prep for me:
1. Pull together what's worth knowing, including anything recent you can find about this kind of company moving into same-day delivery.
2. Write a one-page brief as a file called brief.md: who they are, what changed, three talking points, three smart questions.
3. Draft a short follow-up email as email.md.
4. At the end, list anything you couldn't verify so I know what to double-check.

I'm not a developer. Explain what you're doing in plain language as you go.
```

## Step 4: Read what it made

You now have two files you can reuse: `brief.md` and `email.md`, plus a short list of things to fact-check. Ask it to change anything in plain language.

<div class="info" data-title="What good looks like">

> You walked away. It ran several steps, wrote files you keep, and flagged its own gaps. The kind of prep that usually eats half an hour, sitting in a folder waiting for you.

</div>

<div class="warning" data-title="Where it breaks">

> There's a setup cost and a terminal. It's overkill for a two-line answer, and you wouldn't open it just to reword one email. The power costs you a little friction up front.

</div>

---

# Compare and pick

Same job. Two doors. Now compare what you felt.

| | M365 Copilot · Ask | Copilot CLI · Hand off |
|---|---|---|
| Setup | None, already open | One-time install, a terminal |
| Who drives | You, every step | It does, after one brief |
| How deep | What you paste plus your files | Multiple sources, its own plan |
| What you keep | An answer in the chat | Files you reuse next time |
| Best for | Quick prep you mostly know | Real homework you'd rather skip |

<div class="tip" data-title="The takeaway is yours, not mine">

> Neither one wins. Ask is the right door for a fast job in an app you're already in. Hand off is the right door when the work is big enough to walk away from. Most weeks you'll use both, and now you can feel which is which.

</div>

## Try the same job on more surfaces

CoWork runs this hand-off style without a terminal. The GitHub Copilot App carries it on your phone. Scout could watch your calendar and prep you unasked. Those tracks land as the Lab grows.

Back to [the Operator Lab](https://jw-sthlm.github.io/cli-intro-share/operator-hour/lab/) to pick another use case.

**Still not a developer.** Just stopped doing the same prep by hand every week.
