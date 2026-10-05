"""Export all Marimo notebooks as WASM-powered interactive HTML for GitHub Pages.

Strategy: export each notebook to its own subdirectory, then deduplicate the
assets/ folder by keeping one shared copy at docs/assets and pointing every
index.html at it.
"""
import glob
import html as html_lib
import os
import re
import shutil
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DOCS_DIR = "docs"
NOTEBOOKS_DIR = "notebooks"

# Static files marimo ships with every export; kept once at docs root.
SHARED_STATIC = [
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "apple-touch-icon.png",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "favicon.ico",
    "logo.png",
    "manifest.json",
    "site.webmanifest",
]

# Clean docs
if os.path.exists(DOCS_DIR):
    shutil.rmtree(DOCS_DIR)
os.makedirs(DOCS_DIR, exist_ok=True)

# Export notebooks
notebooks = sorted(glob.glob(os.path.join(NOTEBOOKS_DIR, "*.py")))
succeeded = 0
failed = 0
shared_assets_copied = False

for nb in notebooks:
    name = os.path.basename(nb).replace(".py", "")
    out_dir = os.path.join(DOCS_DIR, name)

    print(f"Exporting {name}...")
    result = subprocess.run(
        [
            sys.executable, "-m", "marimo", "export", "html-wasm",
            nb, "-o", out_dir,
            "--mode", "run",
            "--show-code",
        ],
        capture_output=True, text=True, timeout=180,
    )

    if result.returncode == 0 and os.path.exists(out_dir):
        succeeded += 1
        print(f"  OK: {name}")

        # On first success, keep assets as the shared copy
        if not shared_assets_copied:
            src_assets = os.path.join(out_dir, "assets")
            shared_assets = os.path.join(DOCS_DIR, "assets")
            if os.path.exists(src_assets) and not os.path.exists(shared_assets):
                shutil.copytree(src_assets, shared_assets)
                shared_assets_copied = True
                print(f"  Saved shared assets/ ({len(os.listdir(shared_assets))} files)")

        # Remove duplicate assets from this notebook dir
        local_assets = os.path.join(out_dir, "assets")
        if os.path.exists(local_assets) and shared_assets_copied:
            shutil.rmtree(local_assets)

        # Deduplicate marimo's per-export static files: keep a single copy at
        # docs root and delete the module's copy.
        for static_file in SHARED_STATIC + [".nojekyll"]:
            src = os.path.join(out_dir, static_file)
            dst_root = os.path.join(DOCS_DIR, static_file)
            if os.path.exists(src):
                if not os.path.exists(dst_root):
                    shutil.copy2(src, dst_root)
                if static_file != ".nojekyll":
                    os.remove(src)

        # Rewrite the index.html to point to shared assets at ../assets/
        idx_path = os.path.join(out_dir, "index.html")
        if os.path.exists(idx_path):
            with open(idx_path, encoding="utf-8") as f:
                html = f.read()
            html = html.replace('"./assets/', '"../assets/')
            html = html.replace('"assets/', '"../assets/')
            html = re.sub(r'(?<=["\'])assets/', '../assets/', html)
            for static_file in SHARED_STATIC:
                html = html.replace(f'"./{static_file}"', f'"../{static_file}"')
                html = html.replace(f'"{static_file}"', f'"../{static_file}"')
            with open(idx_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(html)
    else:
        failed += 1
        print(f"  FAILED: {name}")
        if result.stderr:
            print(f"  {result.stderr[:200]}")

# Root index.html is home's, with asset paths one level shallower.
home_idx = os.path.join(DOCS_DIR, "home", "index.html")
root_idx = os.path.join(DOCS_DIR, "index.html")
if os.path.exists(home_idx):
    with open(home_idx, encoding="utf-8") as f:
        html = f.read()
    root_html = html.replace('"../assets/', '"./assets/')
    for static_file in SHARED_STATIC:
        root_html = root_html.replace(f'"../{static_file}"', f'"./{static_file}"')
    with open(root_idx, "w", encoding="utf-8", newline="\n") as f:
        f.write(root_html)
    print("\nCreated root index.html with shared asset paths")

# Publish the proof briefs and flashcard decks as plain markdown, each with an index.
for src_dir, title in (("exercises", "Proof Exercise Briefs"), ("flashcards", "Flashcard Decks")):
    if not os.path.isdir(src_dir):
        continue
    dst_dir = os.path.join(DOCS_DIR, src_dir)
    shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns("_modules"), dirs_exist_ok=True)
    files = sorted(
        os.path.relpath(p, src_dir).replace(os.sep, "/")
        for p in glob.glob(os.path.join(src_dir, "**", "*.md"), recursive=True)
        if "_modules" not in p
    )
    links = "\n".join(
        f'<li><a href="{html_lib.escape(p)}">{html_lib.escape(p)}</a></li>' for p in files
    )
    index_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Category Theory — {title}</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;line-height:1.55;color:#172033}}
a{{color:#0369a1}}
li{{margin:.4rem 0}}
</style>
</head>
<body>
<h1>Category Theory — {title}</h1>
<ul>
{links}
</ul>
<p><a href="../">Back to the course</a></p>
</body>
</html>
"""
    with open(os.path.join(dst_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(index_html)
    print(f"Copied {len(files)} files to docs/{src_dir}/")

# .nojekyll at root prevents GitHub from processing with Jekyll
nojekyll = os.path.join(DOCS_DIR, ".nojekyll")
if not os.path.exists(nojekyll):
    open(nojekyll, "w").close()

print(f"\nSite built: {succeeded} succeeded, {failed} failed")
