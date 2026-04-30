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
  @{ From = "cli-intro-v3.html";            To = "deck.html"       }
  @{ From = "cli-intro-v3-print.html";      To = "print.html"      }
)

Write-Host "Source : $source" -ForegroundColor DarkGray
Write-Host "Target : $repo"   -ForegroundColor DarkGray
Write-Host ""

foreach ($f in $map) {
  $src = Join-Path $source $f.From
  $dst = Join-Path $repo   $f.To
  if (-not (Test-Path $src)) { throw "Missing source file: $src" }
  Copy-Item $src $dst -Force
  # Fix image paths — source deck uses ../images/, share repo uses images/
  if ($f.To -match '\.html$') {
    (Get-Content $dst -Raw) -replace '\.\./images/', 'images/' | Set-Content $dst -NoNewline
  }
  Write-Host "  ✓ $($f.From) -> $($f.To)" -ForegroundColor Green
}

# Sync images (deck references ../images/ relative path)
$imgSource = Join-Path (Split-Path $source) "images"
$imgTarget = Join-Path $repo "images"
if (Test-Path $imgSource) {
  if (-not (Test-Path $imgTarget)) { New-Item $imgTarget -ItemType Directory | Out-Null }
  $imgs = Get-ChildItem $imgSource -File -Include "*.png","*.jpg","*.jpeg","*.svg","*.webp" -Recurse
  foreach ($img in $imgs) {
    Copy-Item $img.FullName (Join-Path $imgTarget $img.Name) -Force
    Write-Host "  ✓ images/$($img.Name)" -ForegroundColor Green
  }
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
