#!/usr/bin/env python3
"""
Emit the finished-*/ import source for Claude Design.

Claude Design's Example Decks are 1:1 ports of the finished-*/ folders in the
presentation-templates repo, and those use relative ../assets/ image paths.
This script derives that copy from the working deck so there is only ever one
file anyone edits by hand.

    python3 build_finished.py

Output: ../finished-integrity_wellbeing_deck/integrity-wellbeing-deck-v1.html

Do NOT hand-edit the generated file. Edit the working deck and re-run.
"""

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
SOURCE = HERE / "integrity-wellbeing-sales-deck-v2.html"
DEST_DIR = HERE.parent / "finished-integrity_wellbeing_deck"
DEST = DEST_DIR / "integrity-wellbeing-deck-v1.html"

ASSET_URL = "https://jbearup1981.github.io/presentation-templates/assets/"
ASSET_REL = "../assets/"

BANNER = (
    "<!-- GENERATED FILE — do not edit.\n"
    "     Source: integrity-wellbeing-deck/integrity-wellbeing-sales-deck-v2.html\n"
    "     Rebuild: cd integrity-wellbeing-deck && python3 build_finished.py\n"
    "     Edits made here are lost on the next rebuild. -->\n"
)


def main():
    if not SOURCE.exists():
        sys.exit(f"source deck missing: {SOURCE}")
    html = SOURCE.read_text()

    before = len(re.findall(r'src="' + re.escape(ASSET_URL), html))
    html = html.replace(ASSET_URL, ASSET_REL)
    after = len(re.findall(r'src="' + re.escape(ASSET_REL), html))

    # Nothing may still point at an absolute host, or the Design import will
    # pull a remote image instead of the repo asset.
    leftover = re.findall(r'src="https?://[^"]+', html)
    if leftover:
        sys.exit("absolute image srcs remain:\n  " + "\n  ".join(leftover[:5]))

    # Verify every referenced asset actually exists in the repo.
    missing = []
    for rel in sorted(set(re.findall(r'src="\.\./assets/([^"]+)"', html))):
        if not (HERE.parent / "assets" / rel).exists():
            missing.append(rel)
    if missing:
        sys.exit("assets referenced but not in repo:\n  " + "\n  ".join(missing))

    DEST_DIR.mkdir(exist_ok=True)
    # Banner goes after the doctype so the file still parses as HTML.
    m = re.match(r"(\s*<!DOCTYPE[^>]*>\s*)", html, re.I)
    out = (m.group(1) + BANNER + html[m.end():]) if m else BANNER + html

    DEST.write_text(out)
    print(f"  rewrote {before} asset URLs -> {ASSET_REL} ({after} relative srcs)")
    print(f"  wrote {DEST.relative_to(HERE.parent)}  "
          f"({len(out)//1024}KB, {len(re.split(r'<div class=.slide', out)) - 1} slides)")


if __name__ == "__main__":
    main()
