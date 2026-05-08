# Copilot CLI: self-service course for Microsoft partner roles

A self-paced version of GitHub's [Copilot CLI for Beginners](https://gh.io/copilot-cli-course), adapted for **Microsoft's partner organization**. For everyone in the partner org: tech, sales, business, marketing (PSA, PTS, PDM, PSAM, PSS, PMA, and similar), and their managers. Anyone who works with partners every day.

The participant experience lives at **[the course landing page](index.html)**. This README is the editable overview for anyone browsing the source.

---

## Who this is for

| You are... | Your day looks like... | Where to focus |
|------------|------------------------|----------------|
| **Sales, business, marketing, managers, and business-side tech** (PDM, PSAM, PSS, PMA, business-side PSA) | Decks, briefings, partner emails, status updates, **Excel and Outlook all day**. You're not coding. | First five lessons (~90 min) |
| **Technical roles that script** (PTS, PSA) | Architecture conversations, demos, customer technical reviews, occasional scripting and IaC | All eight lessons (~3h) |
| Not sure | Start at the top. Decide after MCP power-ups whether to keep going. | First five, then optional |

The first five lessons cover the talk-to-it skills. After that, you can drive 80% of partner-work CLI value.

The last three lessons add the build-stuff-with-it skills: custom agents, reusable skills, end-to-end pipelines. They're marked **optional · more technical** because you'll write a little YAML and Markdown. No real programming.

---

## Lessons

### Core (everyone)

| # | Lesson | Time | What you'll be able to do |
|---|--------|------|---------------------------|
| 1 | [Why CLI for partner work](why-cli-for-partner-work.html) | 10 min | Decide if this is for you. Understand "talk-to-it" vs "code-the-thing". |
| 2 | [Setup, the lazy way](setup-the-lazy-way.html) | 15–30 min | Working CLI on your laptop with the right accounts wired up. |
| 3 | [Your first conversations](your-first-conversations.html) | 20 min | Summarize, rewrite, draft, all without leaving the terminal. |
| 4 | [Drop a file in, get insight out](files-as-context.html) | 20 min | Analyze RFPs, partner decks, transcripts, and customer docs. |
| 5 | [MCP power-ups: PMX, M365, GitHub](mcp-power-ups.html) | 20 min | Pull from your inbox, your calendar, your projects, your repos. |

### Optional · more technical

| # | Lesson | Time | What you'll be able to do |
|---|--------|------|---------------------------|
| 6 | [Custom AI agents](custom-ai-agents.html) | 25 min | Build a reusable "partner-briefing" agent. |
| 7 | [Skills](skills.html) | 25 min | Package a workflow once. The whole vTeam reuses it. |
| 8 | [Putting it all together](putting-it-all-together.html) | 30 min | Ship one reusable asset combining MCP + agents + skills. |

---

## Before you start

1. **A laptop** running Windows 10/11. (Mac works, but our examples are Windows.)
2. **GitHub Copilot access** through your Microsoft enterprise account. Check at [github.com/settings/copilot](https://github.com/settings/copilot).
3. **Two GitHub accounts wired up:**
   - Your personal GitHub username (general work)
   - Your `*_microsoft` EMU account (Microsoft-internal repos like PMX MCP)
   - No EMU yet? See [Setup, the lazy way](setup-the-lazy-way.html).
4. **Optional but recommended:** an Azure subscription you can `az login` to (your Microsoft tenant).

> No coding experience needed for the first five lessons. If you can install software and follow numbered steps, you can complete it.

---

## Visual markers across lessons

- 📖 **Plain English aside.** Extra context for non-technical roles, click-to-expand
- 🔧 **Technical deep dive.** For the optional lessons or anyone curious.
- ⚠️ **Common trap.** Pause and read. This is from real workshops.

---

## How this differs from the GitHub original

The [GitHub original](https://gh.io/copilot-cli-course) is excellent, but built for **software developers** working on a Python book app. This version:

- Uses **partner work scenarios** throughout (RFPs, briefings, vTeam updates, PMX projects)
- Adds the **EMU/personal account dance** that's specific to Microsoft
- Adds **MCP servers we actually use** (PMX, M365, GitHub) instead of generic database examples
- Calls out **data boundaries** (NDA content, partner data) explicitly
- Splits into a **core + optional** structure so non-coders can stop at the value plateau

The source course is referenced where it goes deeper than we need to.

---

## If you get stuck

1. Re-run [`pre-work/verify.ps1`](../pre-work/verify.ps1). It diagnoses 8 common problems automatically.
2. Open [`reference/troubleshooting.md`](../reference/troubleshooting.md). Known issues from real workshops.
3. Drop a question in the **Agentic AI vTeam** Teams channel.
4. The [Setup Clinic](../setup-clinic/README.md) is a 90-minute live session if async isn't working for you.

---

## What you'll build by the end

**After the first five lessons** you can:
- Open a CLI, talk to Copilot, get useful output
- Drop a partner doc in, get a structured analysis out
- Pull data from your Outlook, calendar, and PMX projects via natural language

**After all eight lessons** you can do all of that plus:
- Build a reusable partner-briefing agent
- Package a workflow as a Skill the whole vTeam uses
- Ship an end-to-end pipeline (MCP → agent → skill → output) for a real recurring task

---

## License & attribution

Adapted from [github.com/microsoft/copilot-cli-for-beginners](https://github.com/microsoft/copilot-cli-for-beginners) (MIT-licensed). Re-skinned for Microsoft partner-facing roles. Maintained by the EMEA Agentic AI vTeam.
