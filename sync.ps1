#Requires -Version 7.0
<#
.SYNOPSIS
  Sync the latest storyboard + presenter deck from cli-intro/v2 and push to GitHub Pages.

.EXAMPLE
  .\sync.ps1 "updated demo 1 talking points"

.EXAMPLE
  .\sync.ps1                       # uses a generic commit message
#>
param(
  [Parameter(Position = 0)]
  [string]$Message = "update: sync from cli-intro/v2"
)

$ErrorActionPreference = "Stop"

$repo   = $PSScriptRoot
$source = Resolve-Path (Join-Path $repo "..\cli-intro\v2\deck")

$map = @(
  @{ From = "cli-intro-v2-storyboard.html"; To = "storyboard.html" }
  @{ From = "cli-intro-v2.html";            To = "presenter.html"  }
)

Write-Host "Source : $source" -ForegroundColor DarkGray
Write-Host "Target : $repo"   -ForegroundColor DarkGray
Write-Host ""

foreach ($f in $map) {
  $src = Join-Path $source $f.From
  $dst = Join-Path $repo   $f.To
  if (-not (Test-Path $src)) { throw "Missing source file: $src" }
  Copy-Item $src $dst -Force
  Write-Host "  ✓ $($f.From) -> $($f.To)" -ForegroundColor Green
}

Push-Location $repo
try {
  $changes = git status --porcelain
  if (-not $changes) {
    Write-Host "`nNo changes to publish. Already up to date." -ForegroundColor Yellow
    return
  }

  Write-Host "`nChanges:" -ForegroundColor Cyan
  git -c color.ui=always status --short

  git add -A
  git commit -m $Message | Out-Null
  Write-Host "`nPushing to origin/main..." -ForegroundColor Cyan
  git push --quiet

  $sha = git rev-parse --short HEAD
  Write-Host "`n✓ Published $sha : $Message" -ForegroundColor Green
  Write-Host "  https://jw-sthlm.github.io/cli-intro-share/" -ForegroundColor Blue
  Write-Host "  (reviewers: hard-refresh Ctrl+F5, live in ~60s)" -ForegroundColor DarkGray
}
finally {
  Pop-Location
}
