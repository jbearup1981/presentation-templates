#!/usr/bin/env python3
"""
Emit the finished-*/ import source for Claude Design.

Claude Design's Example Decks are 1:1 ports of the finished-*/ folders in the
presentation-templates repo. Image paths stay as GitHub Pages URLs: that is
what the Design import expects ("asset paths already use GitHub Pages URLs —
no rewrites needed"), and URLs resolve no matter what folder structure the
importer ends up with. The repo also holds older finished decks using relative
../assets/ paths — that convention is not used for new imports.

This derives the copy from the working deck so there is only ever one file
anyone edits by hand.

    python3 build_finished.py

Output: ../finished-integrity_wellbeing_deck/integrity-wellbeing-deck-v1.html

Do NOT hand-edit the generated file. Edit the working deck and re-run.
"""

import pathlib
import re
import sys
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent
SOURCE = HERE / "integrity-wellbeing-sales-deck-v2.html"
DEST_DIR = HERE.parent / "finished-integrity_wellbeing_deck"
DEST = DEST_DIR / "integrity-wellbeing-deck-v1.html"

ASSET_URL = "https://jbearup1981.github.io/presentation-templates/assets/"

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

    # Every image must be a Pages URL — a relative path would break once the
    # importer moves the file, and base64 would bloat the repo.
    stray = [s for s in re.findall(r'src="([^"]+)"', html)
             if not s.startswith(ASSET_URL)]
    if stray:
        sys.exit("image srcs that are not Pages asset URLs:\n  "
                 + "\n  ".join(stray[:5]))

    assets = sorted(set(re.findall(r'src="' + re.escape(ASSET_URL) + r'([^"]+)"', html)))

    # Present in the local repo...
    missing = [a for a in assets if not (HERE.parent / "assets" / a).exists()]
    if missing:
        sys.exit("assets referenced but not in repo:\n  " + "\n  ".join(missing))

    # ...and actually served, since that is what the importer fetches.
    unserved = []
    for a in assets:
        req = urllib.request.Request(ASSET_URL + a, method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status != 200:
                    unserved.append(f"{a} (HTTP {r.status})")
        except urllib.error.HTTPError as e:
            unserved.append(f"{a} (HTTP {e.code})")
        except Exception as e:
            unserved.append(f"{a} ({type(e).__name__})")
    if unserved:
        sys.exit("assets not served from GitHub Pages — push them first:\n  "
                 + "\n  ".join(unserved))

    DEST_DIR.mkdir(exist_ok=True)
    # Banner goes after the doctype so the file still parses as HTML.
    m = re.match(r"(\s*<!DOCTYPE[^>]*>\s*)", html, re.I)
    out = (m.group(1) + BANNER + html[m.end():]) if m else BANNER + html

    DEST.write_text(out)
    print(f"  {len(assets)} assets verified present in repo and served from Pages")
    print(f"  wrote {DEST.relative_to(HERE.parent)}  "
          f"({len(out)//1024}KB, {len(re.split(r'<div class=.slide', out)) - 1} slides)")


if __name__ == "__main__":
    main()
