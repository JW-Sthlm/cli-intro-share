# Operator Hour — Weekly Broadcast Playbook

The post-session ritual. Tuesday 11:30 (right after the session ends) until Wednesday morning.

Last validated: S1E1, May 26 2026. Should work for E2-E6 without changes unless tooling shifts.

## Naming conventions

- Episodes are `s1e1/`, `s1e2/`, …, lowercase, no padding zero.
- Episode page is `<episode>/index.html`.
- Email subject prefix for broadcasts: `Operator Hour E<N> → <punchy half>` (no em dashes, use `→`).
- Teams chat wrap message lead: `📣 Operator Hour E<N> wrap`.

## Pre-session (the morning of, or the day before)

1. **Episode page** exists as a *preview* — what we'll cover, what to bring, no recap yet. URL stays stable across pre and post states.
2. **Landing page** row for this episode points to the preview (`<a class="ep" href="s1eN/">`). No `--published` class yet.
3. **Otto** is up to date with last episode's recap + transcript (see `Update-Otto` step at the bottom).
4. **Use Case Finder** (or whatever live demo is planned) has been dry-run once. Don't run the demo blind.

## Post-session — the broadcast wave

Order matters. Some steps depend on prior ones.

### 1. Update the episode page recap

In `operator-hour/s<season>e<episode>/index.html`:

- Replace the preview body with the Recap structure from `s1e1/index.html`:
  - Narrative paragraphs in `.recap`
  - One `.pull` quote callout if a moment stood out (Otto debut, volunteer moment, etc.)
  - **Operator move** paragraph (`<p><strong>Operator move:</strong> …</p>`)
  - **What the room asked** paragraph (3-5 questions paraphrased, answers in parentheses)
- Take-home block — *this week's one action*. This is what bridges to next episode.
- Resources cards — recording link (active, with the real Stream URL), prompts, anything role-specific.
- What's next cards — link to the next episode + the self-service course.
- **Closing refrain** — write a fresh second sentence. Never reuse one from a prior episode.
- Meta block — update the episode summary line + audience tag.

### 2. Update the landing page

In `operator-hour/index.html`:

**Promote the just-shipped episode:**
- Change `<div class="ep">` to `<a class="ep ep--published" href="s<season>e<episode>/">`
- Add the badge inside the title: `<span class="ep-badge">▶ Watch recap</span>`

**Demote the previous published episode (from E2 onwards):**
- Keep `ep--published` and the badge.
- Remove the heavy outer glow on it (the `0 0 28px -2px rgba(57,210,192,.45)` part of `box-shadow`).
- Only the most recent shipped episode glows. Older ones keep accent bar + gradient + badge.
- (You'll probably want to introduce a `.ep--published.ep--latest` modifier when we hit E2. Add it then, not now.)

### 3. Post the Teams meeting chat wrap message

Use the agency MCP (documented in Johan's global instructions). Quick recap of the path:

```powershell
# Start the proxy
$proxy = Start-Process -FilePath "C:\Users\jwallquist\AppData\Roaming\agency\CurrentVersion\agency.exe" `
  -ArgumentList "mcp teams --transport http --port 0" -PassThru -NoNewWindow -RedirectStandardOutput "$env:TEMP\teams-mcp.log"
Start-Sleep -Seconds 3
$port = (Select-String -Path "$env:TEMP\teams-mcp.log" -Pattern "port (\d+)").Matches.Groups[1].Value
$base = "http://127.0.0.1:$port/"

# JSON-RPC: initialize → notifications/initialized → ListChats (filter by topic) → SendMessageToChat
```

The full JSON-RPC sequence is in the global instructions. The meeting chat ID for the AI-First Operator series is:
`19:meeting_MTk1ODVjY2QtYTRjOC00OTc3LTkxMTAtOWYwZjY1MDZlOGEy@thread.v2` (S1E1 chat).
Each episode has its own meeting chat ID. Find via `ListChats` with `topic: "AI-first Operator Hour"`.

**Wrap message template** (HTML body):

```html
<p>📣 <b>Operator Hour E<N> wrap</b></p>
<p>Recap, recording, and your 5-minute take-home for the week:<br>
👉 <a href="https://jw-sthlm.github.io/cli-intro-share/operator-hour/s<season>e<episode>/">jw-sthlm.github.io/cli-intro-share/operator-hour/s<season>e<episode>/</a></p>
<p>Otto is in this chat — @mention with any follow-up question, even after the meeting ends.</p>
<p>Next Tuesday at 10:30 CET: <i>E<N+1> · <title></i>.</p>
<p>#via-Agentic-CLI</p>
```

Tag with `#via-Agentic-CLI` per the global rule (this is an agent-sent message).

### 4. Create the Outlook broadcast email draft

Use the `create-email-draft.ps1` template in the session workspace. The COM-based approach lands the draft directly in Outlook's Drafts folder. Refresh Outlook (Send/Receive) if you don't see it immediately.

**Email subject:** `Operator Hour E<N> → <punchy title> · recap, recording, and your 5-minute take-home before next Tuesday`

**Body anchors** (keep order):
1. Lead with the one-line takeaway from the session.
2. Recording link (jump-cut to the page, not the raw Stream URL).
3. The one operator move from the recap.
4. Reminder: cohort team is open-join (link).
5. What's next Tuesday in one sentence.
6. `#via-Agentic-CLI` footer.

**Recipients pattern:** TO = Johan (self), BCC = the 107-person broadcast list. Don't expose recipient identities.

### 5. Set the Stream video description + chapters

**Manual UI step. No API supports this.** Open the recording in Stream, paste the description block, add chapters.

**Description template:**
```
S1E<N> · <Title> · <Date>

<3-line summary of what we covered.>

Recap, prompts, and your take-home for the week:
https://jw-sthlm.github.io/cli-intro-share/operator-hour/s<season>e<episode>/

Chapters:
00:00 Intro
0X:XX <Section 1>
0X:XX <Section 2>
…
0X:XX Wrap + take-home
```

Chapters in the description are just text — Stream's actual chapter UI is set separately by clicking "Add chapter" at each timestamp. Both are worth doing.

### 6. Refresh Otto

Otto needs to know about this episode going forward. Steps:

1. Pull the meeting transcript (from Stream → Transcript download → save as `s<season>e<episode>-transcript.txt`).
2. Combine with the recap page content into Otto's knowledge.
3. Redeploy Otto in the cohort team (see `deploy-otto.ps1` if it exists in the session workspace; otherwise manual upload via Copilot Studio).
4. Verify Otto answers a known-from-this-episode question correctly before signing off.

### 7. Commit, push, verify deploy

```powershell
cd C:\Users\jwallquist\projects\cli-intro-share
git add -A
git commit -m "S1E<N> recap: page, landing update, broadcast wave" `
  -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push origin main
```

Pages auto-deploys via the Actions workflow. Wait ~60s, then verify:

```powershell
$r = Invoke-WebRequest -Uri "https://jw-sthlm.github.io/cli-intro-share/operator-hour/?nocache=$(Get-Random)" -UseBasicParsing
if ($r.Content -match "S1E<N>") { "live" } else { "still cached" }
```

If the Actions workflow fails on a codeload action download, GitHub is degraded. Wait, then `gh run rerun <id>`.

## Done. Now go for a walk.

The broadcast wave is the longest part of the cadence — usually 60-90 minutes the first time, 30-45 min once the rhythm is in place. Don't try to do it during the session itself. Capture rough recap notes during, finish the page in the afternoon.

## Backlog for future iterations

- `Update-Otto` PowerShell helper that automates step 6 (currently manual).
- Auto-detect "add me to the invite" in cohort team chat → Otto replies + @mentions Johan.
- Scaffold remaining episode pages (s1e3 through s1e6) as previews now so the URLs exist before each session.
- Pre-session reminder template (Sunday evening) that goes to the cohort team chat.
