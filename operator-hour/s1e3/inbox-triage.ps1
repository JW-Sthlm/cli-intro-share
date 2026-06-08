<#
.SYNOPSIS
  Morning inbox triage. Sorts your Outlook inbox into folders so only the mail
  that actually needs you stays in front of you.

.DESCRIPTION
  Reads every email in your Outlook inbox and moves the noise into four folders,
  leaving direct, small-group, and ambiguous mail in your Inbox:

    Notifications  - automated/system mail (GitHub, Azure, approvals, no-reply)
    Newsletters    - digests, dev blogs, community roundups
    Mass           - broadcasts and events (town halls, all-hands, FY kickoffs)
    Group Invites  - meeting invites blasted to a large distribution list

  Rules run in order, first match wins. The guiding principle: when in doubt,
  leave it in the Inbox. Missing a direct email is worse than leaving one
  broadcast where you can see it.

.NOTES
  Requires : Outlook desktop running on Windows (uses the Outlook COM object).
  Privacy  : No AI, no cloud calls. Nothing leaves your machine. Pure local sort.

  CHANGE ONE THING before you run it: set $MyEmail below to your own address.

  Run it manually:
    pwsh -ExecutionPolicy Bypass -File .\inbox-triage.ps1

  Run it on a schedule: see the block at the bottom of this file.

  Operator Hour S1E3
  https://jw-sthlm.github.io/cli-intro-share/operator-hour/s1e3/
#>

param([switch]$Quiet)

# --- CHANGE THIS ------------------------------------------------------------
$MyEmail              = 'you@yourcompany.com'  # your address (self-sent stays in Inbox)
$SmallGroupLimit      = 15   # a real person + me + a handful of others = keep in Inbox
$GroupInviteThreshold = 20   # bigger than this, sent to a list, not to me = move out
# ----------------------------------------------------------------------------

function Log([string]$Message) { if (-not $Quiet) { Write-Host $Message } }

try {
    Log "Connecting to Outlook..."
    $outlook = New-Object -ComObject Outlook.Application
    $ns      = $outlook.GetNamespace("MAPI")
    $inbox   = $ns.GetDefaultFolder(6)

    # Ensure destination folders exist as subfolders of Inbox
    Log "Ensuring destination folders exist..."
    foreach ($name in @('Mass', 'Notifications', 'Newsletters', 'Group Invites')) {
        try   { $null = $inbox.Folders.Item($name) }
        catch { Log "  Creating folder: $name"; $null = $inbox.Folders.Add($name) }
    }

    $myEmailLower = $MyEmail.ToLowerInvariant()
    $stats   = @{ Inbox=0; Notifications=0; Newsletters=0; Mass=0; 'Group Invites'=0 }
    $moves   = @()
    $kept    = @()

    # Collect items first (avoids the COM index-shift bug while moving)
    Log "Reading inbox items..."
    $all = @()
    for ($i = 1; $i -le $inbox.Items.Count; $i++) { $all += $inbox.Items.Item($i) }
    Log "Classifying $($all.Count) items..."

    foreach ($item in $all) {
        # Only handle mail (43) and meeting requests (53)
        if ($item.Class -notin @(43, 53)) { continue }

        $sender     = "$($item.SenderEmailAddress)".ToLowerInvariant()
        $senderName = "$($item.SenderName)"
        $subject    = "$($item.Subject)"
        $to         = "$($item.To)"
        $cc         = "$($item.CC)"
        $isMeeting  = ($item.Class -eq 53)
        $recipCount = (@($to -split ';').Count + @($cc -split ';').Count)
        $addressedToMe = ($to -like "*$myEmailLower*" -or $cc -like "*$myEmailLower*")

        $dest = 'Inbox'

        # RULE 0 - Self-sent: keep in Inbox
        if ($sender -eq $myEmailLower) {
            $dest = 'Inbox'
        }
        # RULE 1 - Notifications: automated / system mail
        elseif (
            $sender -like '*noreply*' -or $sender -like '*no-reply*' -or
            $sender -like '*donotreply*' -or $sender -like '*notifications@*' -or
            $sender -like '*github*' -or $sender -like '*alert@*' -or
            $sender -like '*approval@*' -or
            $subject -match 'Action required|Approval request|Your daily briefing|Mentioned you in'
        ) {
            $dest = 'Notifications'
        }
        # RULE 2 - Newsletters: digests, blogs, roundups
        elseif (
            $sender -like '*engage.mail*' -or
            $senderName -like '*Developer Blog*' -or
            $senderName -like '*Community Calendar*' -or
            $subject -match 'Announcement:|digest|newsletter|weekly recap|weekly roundup|Daily Digest|field comms'
        ) {
            $dest = 'Newsletters'
        }
        # RULE 3 - Small-group protection: a real person + me + a few others stays in Inbox
        elseif ($addressedToMe -and $recipCount -le $SmallGroupLimit -and $sender -notlike '*noreply*') {
            $dest = 'Inbox'
        }
        # RULE 4 - Mass: broadcasts and events (only when NOT addressed directly to me)
        elseif (
            -not $addressedToMe -and (
                $to -like '*All*' -or $to -like '*Community*' -or $cc -like '*All*' -or
                $recipCount -gt $GroupInviteThreshold -or
                $subject -match 'Community Call|Geo Review|GTM|Office Hours|All-Hands|All Hands|Town Hall|FY2|Company Meeting|save the date|conference|Jumpstart|Hackathon'
            )
        ) {
            $dest = 'Mass'
        }
        # RULE 5 - Group invites: meeting blasted to a large list, not to me
        elseif ($isMeeting -and $recipCount -gt $GroupInviteThreshold -and -not $addressedToMe) {
            $dest = 'Group Invites'
        }
        # RULE 6 - Default: keep in Inbox

        $stats[$dest]++
        if ($dest -eq 'Inbox') {
            $subj = if ($subject.Length -gt 65) { $subject.Substring(0,65) + '...' } else { $subject }
            $kept += "  [$senderName] $subj"
        } else {
            $moves += @($item, $dest)
        }
    }

    # Execute moves after classification is complete
    Log "Moving $([int]($moves.Count / 2)) items..."
    $folders = @{}
    foreach ($name in @('Mass', 'Notifications', 'Newsletters', 'Group Invites')) {
        $folders[$name] = $inbox.Folders.Item($name)
    }
    for ($i = 0; $i -lt $moves.Count; $i += 2) {
        try   { [void]$moves[$i].Move($folders[$moves[$i+1]]) }
        catch { Log "  Warning: could not move: $($moves[$i].Subject)" }
    }

    Log ""
    Log "========== TRIAGE REPORT =========="
    Log "Total processed : $($all.Count)"
    Log "  Kept in Inbox : $($stats.Inbox)"
    Log "  Notifications : $($stats.Notifications)"
    Log "  Newsletters   : $($stats.Newsletters)"
    Log "  Mass          : $($stats.Mass)"
    Log "  Group Invites : $($stats.'Group Invites')"
    if ($kept.Count -gt 0) {
        Log ""
        Log "========== STILL IN YOUR INBOX =========="
        $kept | ForEach-Object { Log $_ }
    }
    Log ""
    Log "Done."
}
catch {
    Write-Error "Error: $_"
    exit 1
}

# --- RUN IT ON A SCHEDULE (Windows Task Scheduler) --------------------------
# Run this once in PowerShell to register an hourly job, 08:00 to 17:00.
# Replace the path with where you saved this file. Outlook must be running.
#
#   $action  = New-ScheduledTaskAction -Execute 'pwsh.exe' `
#       -Argument '-ExecutionPolicy Bypass -File "C:\path\to\inbox-triage.ps1" -Quiet'
#   $trigger = New-ScheduledTaskTrigger -Once -At 8am `
#       -RepetitionInterval (New-TimeSpan -Hours 1) `
#       -RepetitionDuration (New-TimeSpan -Hours 9)
#   Register-ScheduledTask -TaskName 'Inbox Triage' -Action $action -Trigger $trigger
#
# To stop it later:  Unregister-ScheduledTask -TaskName 'Inbox Triage'
# ----------------------------------------------------------------------------
