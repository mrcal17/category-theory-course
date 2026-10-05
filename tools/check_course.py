"""Validate notebooks and proof briefs.

Usage:
    python tools/check_course.py            # everything
    python tools/check_course.py 1a 2b      # only these modules (prefix match)
    python tools/check_course.py --fast 1a  # skip executing the notebooks

Checks per notebook: `marimo check`, runs as a script, standard header, raw (non f-string)
markdown, nav footer, and for teaching modules the required sections and six proof briefs.
Checks per brief: template headings, hints in <details>, no solution section.
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(ROOT, "notebooks")
EX_DIR = os.path.join(ROOT, "exercises")

# Modules that are not teaching modules: no Compute It / Prove It sections required.
NON_TEACHING = {"home", "0a", "7a"}
REQUIRED_NB_SECTIONS = [
    "## Common Proof Mistakes",
    "## Why This Matters",
    "## Compute It",
    "## Prove It",
]
REQUIRED_BRIEF_SECTIONS = [
    "## Statement",
    "## What you may use",
    "## What a complete proof must show",
    "## Hints — one at a time",
    "## Check yourself",
    "## Write it up",
]
FORBIDDEN_BRIEF = re.compile(r"^#+\s*(solution|proof|answer|worked)\b", re.I | re.M)
FORBIDDEN_WORDS = re.compile(r"\b(clearly|obviously|it is easy to see|trivially)\b", re.I)


def module_id(path):
    name = os.path.basename(path)[:-3]
    return "home" if name == "home" else name.split("_")[0]


def check_notebook(path, fast):
    problems = []
    mid = module_id(path)
    with open(path, encoding="utf-8") as f:
        src = f.read()

    if '__generated_with = "0.23.9"' not in src or 'marimo.App(width="medium")' not in src:
        problems.append("non-standard header")
    if not src.rstrip().endswith("app.run()"):
        problems.append("does not end with app.run()")
    if re.search(r"mo\.md\(\s*f[r]?\"", src) or re.search(r"mo\.md\(\s*rf\"", src):
        problems.append("f-string markdown cell")
    if "plt.show()" in src:
        problems.append("plt.show() used")
    for bad in ("import torch", "import pandas", "import polars", "import networkx", "import sympy"):
        if bad in src:
            problems.append(f"non-pyodide-safe import: {bad}")
    if mid != "home" and "Course home](../)" not in src:
        problems.append("missing nav footer")
    hits = sorted({m.group(1).lower() for m in FORBIDDEN_WORDS.finditer(src)})
    if hits:
        problems.append(f"banned words: {', '.join(hits)}")

    if mid not in NON_TEACHING:
        for section in REQUIRED_NB_SECTIONS:
            if section not in src:
                problems.append(f"missing section '{section}'")
        if "**Goal.**" not in src or "**What made it work.**" not in src:
            problems.append("no proof in proof-anatomy form")
        if "mo.ui." not in src:
            problems.append("no interactive element")
        if "# TODO" not in src:
            problems.append("no Compute It skeleton (# TODO)")
        briefs = sorted(glob.glob(os.path.join(EX_DIR, mid, "p[0-9][0-9]_*.md")))
        if len(briefs) != 6:
            problems.append(f"expected 6 proof briefs in exercises/{mid}/, found {len(briefs)}")
        for brief in briefs:
            if os.path.basename(brief) not in src:
                problems.append(f"notebook does not list {os.path.basename(brief)}")
            problems += [f"{os.path.basename(brief)}: {p}" for p in check_brief(brief, mid)]

    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "marimo", "check", path],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
    )
    if result.returncode != 0:
        tail = (result.stdout + result.stderr).strip().splitlines()[-12:]
        problems.append("marimo check failed:\n      " + "\n      ".join(tail))
    if not fast:
        try:
            result = subprocess.run(
                [sys.executable, path], capture_output=True, text=True,
                encoding="utf-8", errors="replace", env=env, timeout=300, cwd=ROOT,
            )
            if result.returncode != 0:
                tail = result.stderr.strip().splitlines()[-8:]
                problems.append("fails when run as a script:\n      " + "\n      ".join(tail))
        except subprocess.TimeoutExpired:
            problems.append("timed out (>300 s) when run as a script")
    return problems


def check_brief(path, mid):
    problems = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    first = text.splitlines()[0] if text else ""
    if not re.match(rf"^# {mid.upper()}·P\d\d — \S", first):
        problems.append(f"title line should look like '# {mid.upper()}·P01 — Title'")
    if not re.search(r"\*\*Type:\*\* (warm-up|core|stretch) · \*\*Technique:\*\*", text):
        problems.append("missing or malformed Type/Technique line")
    positions = [text.find(s) for s in REQUIRED_BRIEF_SECTIONS]
    for section, pos in zip(REQUIRED_BRIEF_SECTIONS, positions):
        if pos < 0:
            problems.append(f"missing section '{section}'")
    if all(p >= 0 for p in positions) and positions != sorted(positions):
        problems.append("sections out of order")
    n_hints = text.count("<details>")
    if not 3 <= n_hints <= 4 or n_hints != text.count("</details>"):
        problems.append(f"expected 3-4 balanced <details> hints, found {n_hints}")
    if FORBIDDEN_BRIEF.search(text):
        problems.append("contains a Solution/Proof/Answer heading")
    slug = os.path.basename(path)
    if f"proofs/{mid}/{slug}" not in text:
        problems.append(f"'Write it up' should point at proofs/{mid}/{slug}")
    return problems


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fast = "--fast" in sys.argv
    notebooks = sorted(glob.glob(os.path.join(NB_DIR, "*.py")))
    if args:
        wanted = tuple(a.lower() for a in args)
        notebooks = [n for n in notebooks if os.path.basename(n).lower().startswith(wanted)]
    if not notebooks:
        print("No notebooks matched.")
        return 1
    failed = 0
    for nb in notebooks:
        problems = check_notebook(nb, fast)
        name = os.path.basename(nb)
        if problems:
            failed += 1
            print(f"FAIL  {name}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"ok    {name}")
    print(f"\n{len(notebooks) - failed} ok, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
