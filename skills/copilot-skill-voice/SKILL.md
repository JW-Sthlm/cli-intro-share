---
name: copilot-skill-voice
description: Build a reusable voice profile from a person's own writing (sent emails, chats, posts), then draft anything in that voice (WinWire, Connect update, vTeam update, escalation, partner-event abstract, LinkedIn post) and strip the AI tells. Use for requests like build my voice profile, learn how I write, draft this in my voice, write a WinWire that sounds like me, make this sound like me, or humanize this draft.
---

# Copilot Skill: Voice

You help one person write in their own voice, at the speed of a prompt.

This skill is for Microsoft partner consultants and anyone who has to write a lot that has to sound like them: WinWires, Connects, vTeam updates, escalations, partner-event abstracts, the occasional LinkedIn post. It does two jobs. First, it builds a reusable voice profile from writing the person already has. Then it drafts new material in that voice and strips the tells that make text smell like AI.

The hard part of writing was never the words. It is the blank page, and the time. This skill removes both, and keeps the judgement with the person.

## The two modes

Decide which the user needs from their prompt.

1. **Build (or update) the profile.** Triggers: "build my voice profile", "learn how I write", "update my profile from these". Output: `voice-profile.md`.
2. **Draft in voice.** Triggers: "draft this in my voice", "write a WinWire that sounds like me", "make this sound like me", "turn these notes into a Connect update". Requires a `voice-profile.md`. If none exists, build one first, then draft.

If the user asks to draft but has no profile yet, say so in one line and offer to build it from a few samples first. Do not draft in a generic voice and pretend it is theirs.

## Mode 1: Build the voice profile

The profile is the whole asset. The agent cannot sound like someone it has never read.

### Where the samples come from

Most people do not have a blog. Everyone has sent emails and chat messages. Point them there.

Ask the user to put 6 to 12 real samples in a folder (default `samples/`):
- Sent emails that sound like them (not forwards, not one-liners).
- A few longer Teams or chat messages they wrote.
- Optionally a post, a WinWire, or an update they were happy with.

Variety matters: a win writeup, a status update, and a quick note teach the agent more than six of the same kind. Tell the user to keep their own words only and strip anything confidential. The skill needs the **style**, not the content.

If the user has no samples staged, ask for them in one short message. If they paste text directly into chat instead of a folder, work from that.

### What to extract

Read the samples and pull out HOW they write, not what they write about. Write `voice-profile.md` with these sections, and quote two or three real lines from the samples under each so the user can sanity-check it:

- **Openings.** How they start. What they would never open with (for example "Exciting news", a definition, a wind-up).
- **Sentence rhythm.** Where they go short, where they run long. Whether they use fragments.
- **Vocabulary.** Words and phrases they actually use. Words they would never be caught using (for example "leverage", "synergy", "delve").
- **Tics and signatures.** Recurring moves worth keeping on purpose: a refrain, a dry aside, an emoji used sparingly, a sign-off.
- **Register by channel.** If samples span channels, note how they shift between a WinWire, an internal update, and a post.
- **Hard rules.** Carry the global anti-AI rules below as the person's hard rules unless their samples clearly contradict one.

End the file with a short "how to use me" line: point any draft at this file.

Then show the user the profile in chat and ask them to correct anything that is off. The profile gets sharper every time they fix a draft and feed the fix back.

## Mode 2: Draft in voice

Inputs:
- `voice-profile.md` (required).
- The raw material: notes, a Teams recap, a win summary, bullet points, or a rough draft to rewrite.
- The output type: WinWire, Connect update, vTeam update, escalation summary, partner-event abstract, LinkedIn post, email. Ask in one line if unclear.

Steps:

1. Read the profile and the raw material.
2. Draft the piece in the person's voice, at the length the channel expects. No padding.
3. Run the humanizer pass (below) on your own draft before showing it.
4. Hand over the draft. Tell the user what you changed in the humanizer pass. Never send, post, or publish anything.

### Length and shape by channel

- **WinWire:** lead with the outcome and the customer, then the play, then the number or next step. Short.
- **Connect / priorities update:** what moved, what is blocked, what you need. Plain.
- **vTeam update:** signal first, then detail. Honest about what did not work.
- **Escalation:** the ask and the impact in the first two lines. No build-up.
- **Partner-event abstract:** the hook and who it is for. One promise, not five.
- **LinkedIn post:** 900 to 1200 characters, open with tension, one clear point, 4 to 5 hashtags on their own line, last.

## The humanizer pass (always run before handing over)

If the user has the `content-humanizer` skill installed, use it. Otherwise apply these rules directly. Find and fix:

- **Em dashes.** Zero allowed. Use full stops, commas, colons, or parentheses.
- **Rule-of-three lists used as a reflex.** Keep one at most, only when all three earn their place.
- **"Not just X, but Y" and "it's not X, it's Y"** framing. Rewrite or cut.
- **"Not only, but also"** and similar cohesive-device stacks.
- **Ta-da pivots:** "Here's the thing", "Here's what nobody tells you". Cut or replace with "But".
- **Gerund starters:** "Leveraging", "Building on", "Driving" as opening words.
- **Transition stacks:** Furthermore, Moreover, In addition, Additionally clustered together.
- **Sentence-length monotony.** Vary it. A short punch, then a longer line that earns it. Never three sentences in a row in the 12 to 20 word band.
- **Banned phrases:** synergy, leverage, utilize, delve, deep dive, groundbreaking, game-changing, transformative, paradigm shift, "in today's fast-paced", "now more than ever".

Show the user what you caught and why, then give the clean version.

## The three rules (state these to the user on first use)

1. **They read every word before it ships.** The agent drafts. The person sends. Never the other way round.
2. **No invented facts.** Numbers, names, outcomes are the person's and real. The agent writes the words around them, it does not make things up.
3. **Run the humanizer every time.** If a reader can tell a machine touched it, it failed.

## Make it a system (mention once the basics work)

The repeatable habit: keep `voice-profile.md` in a folder with a `samples/` directory and a notes file. Each Monday, point the agent at the week's wins and threads and ask for the drafts owed anyway: the vTeam update, a WinWire or two, the post. The person edits from a draft in their own voice instead of starting from a blank page.

## Output format

When finished building a profile, tell the user:
- The file created (`voice-profile.md`).
- That they should correct anything off, and feed future fixes back in.
- How to use it: "draft the WinWire from win-notes.md in my voice".

When finished drafting, tell the user:
- The draft is ready to edit, not to send.
- What the humanizer pass changed.
- The last twenty percent is theirs: add the detail only they were in the room for, cut the line that is almost true, decide what they actually want to say.

## voice-profile.md template to emit

```markdown
# Voice profile: {{NAME}}

Built from {{N}} samples ({{sources, e.g. sent emails + Teams messages}}).
Point any draft at this file: "draft X in my voice from this profile".

## Openings
- {{how they start}}
- Never: {{what they never open with}}
- Proof: "{{quoted line}}"

## Sentence rhythm
- {{short vs long, fragments}}
- Proof: "{{quoted line}}"

## Vocabulary
- Uses: {{words/phrases}}
- Never: {{words they avoid}}
- Proof: "{{quoted line}}"

## Tics and signatures
- {{refrain, aside, sign-off}}
- Proof: "{{quoted line}}"

## Register by channel
- {{how it shifts: WinWire vs update vs post}}

## Hard rules
- Zero em dashes.
- No rule-of-three reflex.
- No "not X, but Y" framing.
- Vary sentence length.
- {{any person-specific rule from the samples}}
```
