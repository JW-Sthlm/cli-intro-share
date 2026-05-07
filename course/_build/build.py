#!/usr/bin/env python3
"""
Build the partner-flavored Copilot CLI course pages.

Run from anywhere:
    python course/_build/build.py

What it does:
  1. One-time migration: moves track-business/mN-*/README.md and track-technical/mN-*/README.md
     into flat course/{slug}.md files, applying content rewrites that drop M-numbering and
     "Track A / Track B" language. Idempotent — re-running on already-flat sources is a no-op.
  2. Generates course/{slug}.html for each lesson by rendering the markdown and wrapping it in
     course/_build/template.html. Sidebar nav and prev/next links are inserted automatically.
  3. Sanity-checks the output: fails if any "M0".."M7", "Module N", or "Track A/B" snuck through.

Source of truth: the .md files. Edit those, then re-run the build.
"""

from __future__ import annotations

import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import markdown


HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
TEMPLATE = HERE / "template.html"


# Module spec: (slug, old_track, old_folder, title, eyebrow, time, outcome, optional)
@dataclass
class Lesson:
    slug: str
    old_track: str
    old_folder: str
    title: str
    eyebrow: str
    time: str
    outcome: str
    optional: bool = False
    description: str = ""


LESSONS: list[Lesson] = [
    Lesson(
        slug="why-cli-for-partner-work",
        old_track="track-business",
        old_folder="m0-why-cli",
        title="Why CLI for partner work",
        eyebrow="Orientation",
        time="10 min",
        outcome="Decide if this is for you. Understand 'talk-to-it' vs 'code-the-thing'.",
        description="The difference between Copilot CLI and other Copilots, and why it earns a slot in your daily workflow.",
    ),
    Lesson(
        slug="setup-the-lazy-way",
        old_track="track-business",
        old_folder="m1-setup",
        title="Setup, the lazy way",
        eyebrow="Get unstuck",
        time="15–30 min",
        outcome="Working CLI on your laptop with the right accounts wired up.",
        description="Get a working CLI on your laptop in 15–30 minutes via the Express path. Manual fallback when something snags.",
    ),
    Lesson(
        slug="your-first-conversations",
        old_track="track-business",
        old_folder="m2-first-conversations",
        title="Your first conversations",
        eyebrow="Foundations",
        time="20 min",
        outcome="Summarize, rewrite, draft — without leaving the terminal.",
        description="Five practical asks that demonstrate the value plateau most users hit on day one.",
    ),
    Lesson(
        slug="files-as-context",
        old_track="track-business",
        old_folder="m3-files-as-context",
        title="Drop a file in, get insight out",
        eyebrow="Foundations",
        time="20 min",
        outcome="Analyze RFPs, partner decks, transcripts, and customer docs.",
        description="Feeding files as context — the move that turns Copilot CLI from a chat tool into a real assistant.",
    ),
    Lesson(
        slug="mcp-power-ups",
        old_track="track-business",
        old_folder="m4-mcp-power-ups",
        title="MCP power-ups: PMX, M365, GitHub",
        eyebrow="Plug into your work",
        time="20 min",
        outcome="Pull from your inbox, your calendar, your projects, your repos.",
        description="Wire up the MCP servers Microsoft partner roles actually use, so Copilot can read your real work data.",
    ),
    Lesson(
        slug="custom-ai-agents",
        old_track="track-technical",
        old_folder="m5-custom-agents",
        title="Custom AI agents",
        eyebrow="Optional · More technical",
        time="25 min",
        outcome="Build a reusable 'partner-briefing' agent.",
        description="Package a recurring task into a reusable agent the whole vTeam can call.",
        optional=True,
    ),
    Lesson(
        slug="skills",
        old_track="track-technical",
        old_folder="m6-skills",
        title="Skills",
        eyebrow="Optional · More technical",
        time="25 min",
        outcome="Package a workflow once. The whole vTeam reuses it.",
        description="Skills are auto-loaded prompt templates. Build one, share it, watch it get used.",
        optional=True,
    ),
    Lesson(
        slug="putting-it-all-together",
        old_track="track-technical",
        old_folder="m7-pipeline",
        title="Putting it all together",
        eyebrow="Optional · More technical",
        time="30 min",
        outcome="Ship one reusable asset that combines MCP + agents + skills.",
        description="An end-to-end pipeline that demonstrates how MCP, agents, and skills compose into something the whole team uses.",
        optional=True,
    ),
]


# Substitutions applied to migrated markdown content.
# Keep order: most specific first.
def get_content_subs() -> list[tuple[str, str]]:
    return [
        # Title H1: "Module N: <topical>" -> just "<topical>"
        (r"^# Module \d+: ", r"# "),
        # "Module N (next)" / "Module N follows" referenced in flowing text → use topical name + link
        (r"\bModule 0\b", "Why CLI for partner work"),
        (r"\bModule 1\b", "Setup, the lazy way"),
        (r"\bModule 2\b", "Your first conversations"),
        (r"\bModule 3\b", "Drop a file in, get insight out"),
        (r"\bModule 4\b", "MCP power-ups"),
        (r"\bModule 5\b", "Custom AI agents"),
        (r"\bModule 6\b", "Skills"),
        (r"\bModule 7\b", "Putting it all together"),
        # M0–M4 / M5–M7 / M0-M7 ranges
        (r"\bM0[\u2013\u2014-]M4\b", "the first five lessons"),
        (r"\bM5[\u2013\u2014-]M7\b", "the last three lessons"),
        (r"\bM0[\u2013\u2014-]M7\b", "all eight lessons"),
        # Bare M0..M7 references
        (r"\bM0\b", "first lesson"),
        (r"\bM1\b", "Setup, the lazy way"),
        (r"\bM2\b", "Your first conversations"),
        (r"\bM3\b", "Drop a file in, get insight out"),
        (r"\bM4\b", "MCP power-ups"),
        (r"\bM5\b", "Custom AI agents"),
        (r"\bM6\b", "Skills"),
        (r"\bM7\b", "Putting it all together"),
        # Track language
        (r"Track A: Business roles \(.*?\)", "First five lessons (everyone)"),
        (r"Track B: Technical roles \(.*?\)", "Last three lessons (optional, more technical)"),
        (r"\*\*Track A:?\s*Business\*\*", "**First five lessons**"),
        (r"\*\*Track B:?\s*Technical\*\*", "**Last three lessons**"),
        (r"\bTrack A graduates\b", "Once you finish the first five lessons you"),
        (r"\bTrack B graduates\b", "Once you complete all eight lessons you"),
        (r"\bTrack A\b", "the first five lessons"),
        (r"\bTrack B\b", "the last three lessons"),
        # "👉 Track A: Back to course home" / "👉 Track B continues:" footers
        (r"^## 👉 .* \[Back to course home\].*$", "## 👉 Back to [course home](index.html)", ),
        (r"^## 👉 .*continues.*$", "## 👉 Next up: [Custom AI agents](custom-ai-agents.html)"),
        # Internal "../../README.md" -> "index.html" (course home)
        (r"\.\./\.\./README\.md", "index.html"),
        # "../../track-technical/m5-custom-agents/README.md" etc → flat HTML
        (r"\.\./\.\./track-technical/m5-custom-agents/README\.md", "custom-ai-agents.html"),
        (r"\.\./\.\./track-technical/m6-skills/README\.md", "skills.html"),
        (r"\.\./\.\./track-technical/m7-pipeline/README\.md", "putting-it-all-together.html"),
        (r"\.\./\.\./track-business/m0-why-cli/README\.md", "why-cli-for-partner-work.html"),
        (r"\.\./\.\./track-business/m1-setup/README\.md", "setup-the-lazy-way.html"),
        (r"\.\./\.\./track-business/m2-first-conversations/README\.md", "your-first-conversations.html"),
        (r"\.\./\.\./track-business/m3-files-as-context/README\.md", "files-as-context.html"),
        (r"\.\./\.\./track-business/m4-mcp-power-ups/README\.md", "mcp-power-ups.html"),
        # 3-level relative links to siblings (now 1-level): ../../../pre-work → ../pre-work, etc.
        (r"\.\./\.\./\.\./pre-work/", "../pre-work/"),
        (r"\.\./\.\./\.\./reference/", "../reference/"),
        (r"\.\./\.\./\.\./extras/", "../extras/"),
        (r"\.\./\.\./\.\./setup-clinic/", "../setup-clinic/"),
        # "v2/pre-work/..." legacy phrasing in body text
        (r"`v2/pre-work/", "`pre-work/"),
        (r"`v2/reference/", "`reference/"),
        (r"`v2/extras/", "`extras/"),
        # Track-mention notes that reference 📖/🔧 markers
        (r"📖 \*\*Business track example or callout:\*\*[^\n]*\n", ""),
        (r"🔧 \*\*Technical deep dive:\*\* Track B only; Track A folks can skip\n",
         "🔧 **Going deeper (optional):** more technical — fine to skip\n"),
        # 📖 / 🔧 / ⚠️ markers section in README
        (r"## 📖 / 🔧 / ⚠️ markers\s*\n+Throughout this course you'll see these:\s*\n+",
         "## Visual markers\n\nThroughout the lessons you'll see:\n\n"),
    ]


# Per-link rewrites in markdown for the README overview specifically (table linking to old paths).
README_LINK_REWRITES: list[tuple[str, str]] = [
    ("track-business/m0-why-cli/README.md", "why-cli-for-partner-work.html"),
    ("track-business/m1-setup/README.md", "setup-the-lazy-way.html"),
    ("track-business/m2-first-conversations/README.md", "your-first-conversations.html"),
    ("track-business/m3-files-as-context/README.md", "files-as-context.html"),
    ("track-business/m4-mcp-power-ups/README.md", "mcp-power-ups.html"),
    ("track-technical/m5-custom-agents/README.md", "custom-ai-agents.html"),
    ("track-technical/m6-skills/README.md", "skills.html"),
    ("track-technical/m7-pipeline/README.md", "putting-it-all-together.html"),
]


def apply_subs(text: str, extra: list[tuple[str, str]] | None = None) -> str:
    for pattern, repl in get_content_subs():
        text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    if extra:
        for old, new in extra:
            text = text.replace(old, new)
    return text


def migrate_markdown() -> None:
    """Move track-X/mY/README.md → flat course/{slug}.md with content rewrites. Idempotent."""
    moved = 0
    for lesson in LESSONS:
        old_path = COURSE / lesson.old_track / lesson.old_folder / "README.md"
        new_path = COURSE / f"{lesson.slug}.md"
        if new_path.exists() and not old_path.exists():
            continue  # already migrated
        if not old_path.exists():
            print(f"  [skip] no source for {lesson.slug} (already migrated and old folder cleared)")
            continue
        content = old_path.read_text(encoding="utf-8")
        content = apply_subs(content)
        new_path.write_text(content, encoding="utf-8")
        moved += 1
        print(f"  [migrated] {lesson.old_track}/{lesson.old_folder}/README.md -> {lesson.slug}.md")
    # Remove the now-empty track folders
    for track in ("track-business", "track-technical"):
        track_dir = COURSE / track
        if track_dir.exists():
            shutil.rmtree(track_dir)
            print(f"  [removed] {track}/")
    print(f"  Migrated {moved} markdown sources.")
    # Rewrite the README overview's links and Track language — only if subs actually change content.
    readme = COURSE / "README.md"
    if readme.exists():
        rd = readme.read_text(encoding="utf-8")
        rewritten = apply_subs(rd, extra=README_LINK_REWRITES)
        if rewritten != rd:
            readme.write_text(rewritten, encoding="utf-8")
            print(f"  [rewrote] README.md")


def render_lesson_html(lesson: Lesson, idx: int) -> str:
    md_path = COURSE / f"{lesson.slug}.md"
    md_text = md_path.read_text(encoding="utf-8")

    # Strip the first H1 + the time/outcome callout block (we render those in the lesson header).
    md_text = re.sub(r"^# .*\n", "", md_text, count=1, flags=re.MULTILINE)
    # Strip the "> ⏱️ Estimated time:" + "> 🎯 You'll be able to:" lines — replaced by lesson-meta-row.
    md_text = re.sub(
        r"^> ⏱️[^\n]*\n(?:> 🎯[^\n]*\n)?", "", md_text, count=1, flags=re.MULTILINE
    )
    # The lesson markdown often opens with a leading "---" separator — drop it if present at top.
    md_text = re.sub(r"^\s*---\s*\n+", "", md_text, count=1)

    # Render markdown to HTML
    md_engine = markdown.Markdown(
        extensions=["extra", "tables", "fenced_code", "attr_list", "sane_lists", "toc"],
        output_format="html5",
    )
    body_html = md_engine.convert(md_text)

    # Build sidebar with current lesson highlighted
    sidebar_items = []
    for j, l in enumerate(LESSONS):
        cls = " is-optional" if l.optional else ""
        a_cls = "is-current" if j == idx else ""
        sidebar_items.append(
            f'<li class="{cls.strip()}"><a class="{a_cls}" href="{l.slug}.html">{l.title}</a></li>'
        )
    sidebar = "\n      ".join(sidebar_items)

    # Prev / Next nav
    if idx > 0:
        prev = LESSONS[idx - 1]
        prev_html = (
            f'<a class="prev" href="{prev.slug}.html">'
            f'<div class="nav-dir">Previous</div>'
            f'<div class="nav-title">{prev.title}</div>'
            f"</a>"
        )
    else:
        prev_html = (
            '<a class="prev" href="index.html">'
            '<div class="nav-dir">Previous</div>'
            '<div class="nav-title">Course home</div>'
            "</a>"
        )
    if idx < len(LESSONS) - 1:
        nxt = LESSONS[idx + 1]
        next_html = (
            f'<a class="next" href="{nxt.slug}.html">'
            f'<div class="nav-dir">Next</div>'
            f'<div class="nav-title">{nxt.title}</div>'
            f"</a>"
        )
    else:
        next_html = (
            '<a class="next" href="index.html">'
            '<div class="nav-dir">Next</div>'
            '<div class="nav-title">Back to course home</div>'
            "</a>"
        )

    template = TEMPLATE.read_text(encoding="utf-8")
    eyebrow_class = "is-optional" if lesson.optional else ""
    out = (
        template.replace("{{LESSON_TITLE}}", lesson.title)
        .replace("{{LESSON_EYEBROW}}", lesson.eyebrow)
        .replace("{{EYEBROW_CLASS}}", eyebrow_class)
        .replace("{{TIME}}", lesson.time)
        .replace("{{OUTCOME}}", lesson.outcome)
        .replace("{{SIDEBAR_ITEMS}}", sidebar)
        .replace("{{BODY}}", body_html)
        .replace("{{PREV}}", prev_html)
        .replace("{{NEXT}}", next_html)
    )
    return out


def sanity_check_output(lesson: Lesson, html: str) -> list[str]:
    findings = []
    bad_patterns = [
        (r"\bM[0-7]\b", "stray M-reference"),
        (r"\bModule [0-9]\b", "stray Module-N reference"),
        (r"\bModules [0-9]", "stray plural Modules-N reference"),
        (r"\bmodules [0-9]", "stray lowercase modules-N reference"),
        (r"\bTrack [AB]\b", "stray Track A/B reference"),
        (r"track-business/", "stray old-folder path"),
        (r"track-technical/", "stray old-folder path"),
        (r"\.\./\.\./\.\./", "stray 3-level relative path"),
        (r"\.\./m[0-9]-", "stray ../m{n}- relative path"),
        (r"the (first five|last three) lessons (covers|continues|caveat|graduates|is)", "grammar damage from naive Track sub"),
        (r"\[([^\]]+)\]\(\1\.html\)", "doubled link text"),
        (r": Setup, the lazy way\]", "doubled lesson title"),
    ]
    for pat, label in bad_patterns:
        for m in re.finditer(pat, html):
            ctx_start = max(0, m.start() - 30)
            ctx_end = min(len(html), m.end() + 30)
            ctx = html[ctx_start:ctx_end].replace("\n", " ")
            findings.append(f"  [{lesson.slug}] {label} '{m.group()}' — ...{ctx}...")
    return findings


def main() -> int:
    print("== Migrate markdown sources ==")
    migrate_markdown()

    print("\n== Build lesson HTML ==")
    all_findings: list[str] = []
    for idx, lesson in enumerate(LESSONS):
        html = render_lesson_html(lesson, idx)
        out_path = COURSE / f"{lesson.slug}.html"
        out_path.write_text(html, encoding="utf-8")
        size_kb = out_path.stat().st_size / 1024
        print(f"  [built] {lesson.slug}.html ({size_kb:.1f} KB)")
        all_findings.extend(sanity_check_output(lesson, html))

    if all_findings:
        print("\n== Sanity-check findings ==")
        for f in all_findings:
            print(f)
        print(f"\n  Total findings: {len(all_findings)}")
        return 1
    print("\n  Sanity check: clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
