#!/usr/bin/env python3
"""
Generate per-advisor variants of the Integrity Well-Being deck.

One source deck, one roster file, N output decks. Only two slides differ
between variants: the Team slide (2) and the Closing contacts slide (16).
Everything else comes straight from the source, so a content fix made once
propagates to every advisor's deck on the next run.

    python3 make_variants.py                    # build all variants
    python3 make_variants.py --only ken         # build just one
    python3 make_variants.py --base64           # also emit standalone copies

Run this instead of hand-editing a copy. Hand-edited copies are how v1 went
stale in the first place.
"""

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
SOURCE = HERE / "integrity-wellbeing-sales-deck-v2.html"
ROSTER = HERE / "roster.json"
OUTDIR = HERE / "variants"
ASSET_BASE = "https://jbearup1981.github.io/presentation-templates/assets"

# Anchors verified unique in the source deck.
TEAM_CONTAINER = "display: flex; gap: 24px;"
CLOSE_CONTAINER = "display: flex; gap: 28px;"


def card(person):
    """Team-slide card (slide 2)."""
    return (
        '    <div style="flex: 1; background: var(--ps); border-radius: 8px; '
        'padding: 28px 24px; text-align: center;">\n'
        '      <div style="margin-bottom: 14px;">'
        f'<img src="{ASSET_BASE}/{person["photo"]}" alt="{strip(person["name"])}" '
        'style="width: 97px; height: 97px; border-radius: 50%; object-fit: cover; '
        'border: 3px solid rgba(31,61,46,0.2);"></div>\n'
        '      <div style="font-family: var(--display); font-size: 20px; '
        f'color: var(--df); margin-bottom: 4px;">{person["name"]}</div>\n'
        '      <div style="font-size: 10px; color: var(--rs); letter-spacing: 1.5px; '
        'text-transform: uppercase; font-weight: 600; margin-bottom: 14px;">'
        f'{person["title"]}</div>\n'
        '      <div style="font-size: 12px; color: var(--sg); line-height: 1.7;">'
        f'{person["blurb"]}</div>\n'
        '    </div>'
    )


def contact(person):
    """Closing-slide contact block (slide 16). Phone line omitted when unknown."""
    phone = ""
    if person.get("phone"):
        phone = (
            '<div style="font-size: 10px; color: rgba(255,255,255,0.72);">'
            f'{person["phone"]}</div>'
        )
    return (
        '      <div style="display: flex; align-items: flex-start; gap: 10px;">\n'
        f'        <img src="{ASSET_BASE}/{person["photo"]}" alt="{strip(person["name"])}" '
        'style="width: 42px; height: 42px; border-radius: 50%; object-fit: cover; '
        'border: 1.5px solid var(--white-15);">\n'
        '        <div>'
        '<div style="font-size: 13px; color: rgba(255,255,255,0.92); font-weight: 600;">'
        f'{person["name"]}</div>'
        '<div style="font-size: 10px; color: rgba(255,255,255,0.62);">'
        f'{person["title"]}</div>'
        f'{phone}'
        '<div style="font-size: 10px; color: rgba(255,255,255,0.72);">'
        f'{person["email"]}</div>'
        '</div>\n'
        '      </div>'
    )


def strip(s):
    """Plain text for alt attributes — no entities."""
    return s.replace("&amp;", "and").replace("&mdash;", "-")


def replace_block(html, anchor, inner, indent):
    """
    Swap the contents of the flex container that starts at `anchor`, matching
    braces by depth so we replace exactly that container and nothing after it.
    """
    i = html.find(anchor)
    if i == -1:
        raise SystemExit(f"anchor not found: {anchor!r}")
    open_end = html.index(">", i) + 1

    depth, j = 1, open_end
    while depth:
        nxt_open = html.find("<div", j)
        nxt_close = html.find("</div>", j)
        if nxt_close == -1:
            raise SystemExit("unbalanced divs while scanning container")
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            j = nxt_open + 4
        else:
            depth -= 1
            j = nxt_close + 6
    close_start = j - 6
    return html[:open_end] + "\n" + inner + "\n" + indent + html[close_start:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="build a single variant by slug")
    ap.add_argument("--base64", action="store_true",
                    help="also emit self-contained copies with embedded images")
    args = ap.parse_args()

    if not SOURCE.exists():
        sys.exit(f"source deck missing: {SOURCE}")
    cfg = json.loads(ROSTER.read_text())
    people, variants = cfg["people"], cfg["variants"]
    src = SOURCE.read_text()
    OUTDIR.mkdir(exist_ok=True)

    if args.only:
        variants = [v for v in variants if v["slug"] == args.only]
        if not variants:
            sys.exit(f"no variant with slug {args.only!r}")

    built = []
    for v in variants:
        team = []
        for key in v["team"]:
            if key not in people:
                sys.exit(f"variant {v['slug']}: unknown person {key!r}")
            team.append(people[key])

        html = src
        html = replace_block(html, TEAM_CONTAINER,
                             "\n".join(card(p) for p in team), "  ")
        html = replace_block(html, CLOSE_CONTAINER,
                             "\n".join(contact(p) for p in team), "    ")

        # With only two cards, flex:1 stretches them across the full width and
        # the slide reads sparse. Cap the row and centre it instead.
        if len(team) == 2:
            html = html.replace(
                f'<div style="{TEAM_CONTAINER}">',
                f'<div style="{TEAM_CONTAINER} max-width: 660px; '
                'margin-left: auto; margin-right: auto; width: 100%;">', 1)

        out = OUTDIR / f"integrity-wellbeing-deck-{v['slug']}.html"
        out.write_text(html)
        built.append((v["slug"], out, [p["name"] for p in team]))
        print(f"  built {out.name:52} {', '.join(p['name'] for p in team)}")

    print(f"\n{len(built)} variant(s) -> {OUTDIR}")
    if args.base64:
        print("\nNow run, per file:")
        print("  python3 ../tools/assemble_deck.py --to-base64 <file> -o <file>")
    return built


if __name__ == "__main__":
    main()
