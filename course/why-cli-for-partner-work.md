# Why CLI for partner work

> ⏱️ **Estimated time:** 10 min reading
> 🎯 **You'll be able to:** decide whether this course is for you, and what you can realistically do with the CLI in your job.

---

## The pitch in one sentence

You can talk to GitHub Copilot from your terminal, and it can read files, search your inbox, query your projects, and produce real artefacts. Faster than chat.com, more powerful than the assistant in Outlook.

That's the whole pitch. The rest of this module is "is that actually useful for *your* job?"

<details markdown="1">
<summary><strong>Why bother with a CLI at all? Don't I already have M365 Copilot?</strong></summary>

Quick analogy: M365 Copilot is the librarian. You ask, it finds, it reads back. CLI Copilot is the contractor. You give it a job, it goes off and does it.

M365 Copilot is great at what it sees: your email, calendar, Office files. Ask it about a thread, it summarizes. Ask it to draft a reply, it does. But it lives inside the M365 surface and stays there.

CLI Copilot is a different shape. It runs on your machine, in your terminal, and it actually does things. Runs commands. Edits files. Calls APIs. Ties tools together.

What the CLI gives you that M365 Copilot doesn't:

1. **Reach beyond M365.** Through MCP connectors, you plug in anything that exposes one: PMX, GitHub, your own internal services, partner APIs, local repos. M365 Copilot is fixed to what Microsoft ships. The CLI is open.
2. **Execute, don't just retrieve.** *"Pull last week's PMX projects, draft a one-pager for each, save to OneDrive."* Ask once, it runs the whole chain. M365 Copilot can find and summarize. The CLI can do the work.
3. **Speak every other command-line tool for you.** Azure CLI, GitHub CLI, git, npm. You don't need to memorize syntax. Tell Copilot what you want; it picks the tool and runs it.
4. **Live where your real work happens.** Your repos, your scripts, your files, your terminal. No tab-switching, no re-uploading.

Set up once. Use it for real work after.

> **A taste of what's possible:** *"Find my last three meetings with Contoso, summarize what we discussed, check their PMX project status, then draft a follow-up email for me to review before sending."* Calendar + PMX + Outlook + Copilot reasoning, chained in one prompt. That's the CLI.

</details>

---

## Two ways to use this course

📖 **Use it (lessons 1–5, ~90 minutes).** You talk to the CLI. Drop files in. Get answers. Get drafts. Skills and agents that other people built do the heavy lifting. You never see code.

🔧 **Make stuff with it (lessons 6–8, +~90 minutes).** Same CLI. Now you build your own agents, your own skills, your own little tools. You still don't write code. You describe what you want, the CLI builds it, you redirect when it's wrong, you ship when it's right.

### The optional lessons aren't "for the techy people"

They're for anyone tired of doing the same thing every Monday morning. Anyone who's ever thought "there should be a tool that does this." Anyone who watched a colleague spin up an HTML deck in 10 minutes and wondered how.

The barrier used to be coding. Now the barrier is having the idea and 30 minutes.

You can build:

- An agent that knows your partners, their priorities, and last quarter's notes. It drafts your prep doc in 60 seconds.
- A skill that turns "give me the QBR deck for Contoso" into a finished slide outline
- A mini-app that pulls your week's PMX projects, your inbox highlights, and your calendar into one Monday-morning briefing
- An HTML presentation in the time it takes to make coffee

You never see the code. You think, you talk, you iterate. The CLI handles the rest.

### Which path?

| You want... | Stop at |
|-------------|---------|
| Results today, no time to invest | After lesson 5 |
| To stop repeating yourself | Keep going through 8 |
| To finally build that tool you always wished existed | Keep going through 8 |
| To support a partner conversation Friday and that's it | After lesson 5 |
| Not sure | After lesson 5. If by then you're thinking "I want this to remember my partners and my templates," you're ready for the rest. |

Both paths use the same CLI. Lessons 6–8 just add the moves you make once you're tired of repeating yourself.

---

## What this can replace in your day

📖 **Examples we've seen actually work for partner roles:**

| Today you... | With Copilot CLI you... |
|--------------|--------------------------|
| Read a 12-page partner RFP, then write a 1-page summary | Drop the RFP in a folder, ask "summarize for an account exec" |
| Open Outlook, scroll the last week, write a partner update | Ask "summarize my emails with Contoso this month" via M365 MCP |
| Click through PMX to remind yourself what's open with a partner | Ask "what PMX projects do I have with Contoso" via PMX MCP |
| Draft the same QBR template for the 4th time this quarter | Have a Skill that generates the skeleton (optional lessons 6–8) |
| Pull data from your inbox, calendar, and a CSV into one update | One CLI session, all three sources, finished draft |
| Build an internal tool that's been on your wish list for 18 months | Describe it, iterate, ship it (optional lessons 6–8) |

---

<details>
<summary><strong>What this is NOT</strong>: common confusions, click to expand</summary>

⚠️

- **Not VS Code Copilot.** That's the assistant inside an editor. This is a separate tool that runs in your terminal. They share an account but they're different products.
- **Not chat.copilot.microsoft.com / M365 Copilot.** That's a chat product for documents and meetings. The CLI is more flexible (talks to your filesystem, runs commands, accepts MCP servers) but less polished.
- **Not autonomous.** It does what you ask. Step by step. You stay in the driver's seat. It will never email a partner without your say-so.

</details>

<details>
<summary><strong>"I'm not a terminal person"</strong>: the terminal thing demystified</summary>

📖 That's fine. You don't need to be.

The terminal here is just a text-input window where you type natural language and get answers back. The same way you'd type into a chat box. The difference is:

- It can read files in the folder you're in
- It can run commands when you tell it to
- It remembers context within a session
- You can press the ⬆️ arrow key to recall yesterday's prompts (this alone is a productivity win)

That's it. If you can use a chat box, you can use this terminal.

</details>

---

## ⚠️ Data boundaries: read this

You will be tempted to drop NDA partner content, customer data, internal Microsoft code into the CLI. Some of it is fine. Some of it is not.

**Safe by default:**
- Public docs, websites, partner press releases
- Your own drafts and notes
- Anything you'd post in your team's general Teams channel

**Stop and think first:**
- Customer-confidential content under NDA: fine for *summarization* you keep internal, never for content you'll send back externally.
- Internal Microsoft strategy docs: same rule.
- Anything labeled Confidential or Highly Confidential: read your org's data policy first.

**Never:**
- Anything you'd be uncomfortable seeing in a screenshot of the CLI window
- Credentials, tokens, customer PII

The CLI sends what you give it to a Copilot endpoint. Treat it the same way you treat M365 Copilot or any other AI tool your org has approved.

---

<details>
<summary><strong>"Will I break anything?"</strong>: the safety story</summary>

📖 No. This course never asks you to:
- Delete files you didn't create
- Run scripts you don't understand
- Touch production systems
- Modify your inbox or calendar

The CLI can *read* a lot. To *change* anything (send an email, update a calendar, modify a file) it asks you first. You stay in the driver's seat.

🔧 **Heads-up for the optional lessons:** when you build agents and pipelines you can grant some operations to run automatically. We'll cover that explicitly in Custom AI agents.

</details>

---

## ✅ You're ready for Setup, the lazy way if you can answer these

1. What does the *use it* path let you do? *(talk, ask, get drafts, never see code)*
2. What does the *make stuff* path add on top? *(build your own agents, skills, mini-tools, still no coding)*
3. Name two things this is NOT. *(VS Code Copilot; M365 Copilot; autonomous AI)*
4. What's one thing in your week that this could replace? *(your answer here)*
5. What's one thing you should stop and think about before pasting into the CLI? *(NDA content, credentials, customer PII)*

---

