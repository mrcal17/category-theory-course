"""Regenerate PROGRESS.md from the proof briefs in exercises/.

Usage: python tools/make_progress.py

Existing Status and Notes cells are preserved (rows are matched on the brief path),
so it is safe to re-run after adding or renaming briefs.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "PROGRESS.md")

ROW = re.compile(r"^\| `(exercises/[^`]+)` \|.*\| ([^|]*) \| ([^|]*) \|$")


def existing_rows():
    rows = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            for line in f:
                m = ROW.match(line.rstrip("\n"))
                if m:
                    rows[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    return rows


def main():
    keep = existing_rows()
    lines = [
        "# Progress",
        "",
        "One row per proof exercise. Status: `todo`, `drafted` (written, not yet reviewed),",
        "`revise` (reviewed, gaps found) or `done` (reviewed, no gaps). Claude updates a row",
        "after reviewing the proof in `proofs/`.",
        "",
    ]
    for mod_dir in sorted(glob.glob(os.path.join(ROOT, "exercises", "[0-9][a-z]"))):
        mid = os.path.basename(mod_dir)
        briefs = sorted(glob.glob(os.path.join(mod_dir, "p[0-9][0-9]_*.md")))
        if not briefs:
            continue
        lines += [f"## {mid.upper()}", "", "| Brief | Title | Type | Status | Notes |", "|---|---|---|---|---|"]
        for brief in briefs:
            rel = os.path.relpath(brief, ROOT).replace(os.sep, "/")
            with open(brief, encoding="utf-8") as f:
                text = f.read()
            title = text.splitlines()[0].split("—", 1)[-1].strip()
            m = re.search(r"\*\*Type:\*\* ([a-z-]+)", text)
            kind = m.group(1) if m else "?"
            status, notes = keep.get(rel, ("todo", ""))
            lines.append(f"| `{rel}` | {title} | {kind} | {status} | {notes} |")
        lines.append("")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
