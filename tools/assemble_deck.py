#!/usr/bin/env python3
"""
Nexus Deck Assembly Tool — Claude Code Edition

Assembles presentation decks from finished deck components with properly
embedded base64 images. Designed for Claude Code (not Claude Projects).

KEY WORKFLOW (v2 — URL-first):
1. Finished decks (finished-*/) use relative paths (../assets/filename.png) — CLEAN HTML
2. Client decks use GitHub Pages URLs — lightweight (~35KB), editable in any AI chat
3. Standalone decks use embedded base64 — for offline/email use only
4. assemble_deck.py converts between all three formats

Commands:
    # Create new client deck from a starter (URL-based, lightweight)
    python3 assemble_deck.py --new-deck <type> --client "Name" -o <output.html>

    # Convert base64 deck → GitHub Pages URLs (450KB → 35KB)
    python3 assemble_deck.py --to-urls <deck.html> -o <output.html>

    # Convert URL deck → embedded base64 (for offline/standalone)
    python3 assemble_deck.py --to-base64 <deck.html> -o <output.html>

    # Embed relative paths as base64 (finished deck → standalone)
    python3 assemble_deck.py --embed <deck.html> -o <output.html>

    # Replace a slide by number
    python3 assemble_deck.py --replace-slide <deck.html> --slide-num 9 --slide-html <slide.html>

    # Extract a single slide by number or text match
    python3 assemble_deck.py --extract-slide <deck.html> --slide-num 9 -o slide.html
    python3 assemble_deck.py --extract-slide <deck.html> --slide-name "text" -o slide.html

    # Generate a plan comparison slide from YAML data
    python3 assemble_deck.py --plan-comparison <data.yaml> -o slide.html

    # Rebuild all 4 starters from finished decks (run after any asset changes)
    python3 assemble_deck.py --rebuild-starters

    # Verify deck integrity
    python3 assemble_deck.py --verify <deck.html>

    # List slides in a deck
    python3 assemble_deck.py --list-slides <deck.html>

    # List available assets
    python3 assemble_deck.py --list-assets

    # Get single asset as base64 data URI (for manual use)
    python3 assemble_deck.py --asset-to-base64 <filename>
"""

import argparse
import base64
import os
import re
import sys
import json
import shutil
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRESENTATIONS_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(PRESENTATIONS_DIR, 'assets')

# GitHub Pages base URL for hosted assets
GITHUB_PAGES_BASE = 'https://jbearup1981.github.io/presentation-templates/assets'

FINISHED_DECKS = {
    'renewal': os.path.join(PRESENTATIONS_DIR, 'finished-small_group_renewal_deck', 'small-group-renewal-deck-v1.html'),
    'prospect': os.path.join(PRESENTATIONS_DIR, 'finished-small_group_prospect_deck', 'small-group-prospect-deck-v1.html'),
    'amaze': os.path.join(PRESENTATIONS_DIR, 'finished-amaze_biomed_nexus_deck', 'amaze-biomed-nexus-deck-v1.html'),
    'midmarket': os.path.join(PRESENTATIONS_DIR, 'finished-mid_market_renewal_deck', 'mid-market-renewal-deck-v1.html'),
}

STARTER_MAP = {
    'renewal': 'archive/starter-small-group-renewal.html',
    'prospect': 'archive/starter-small-group-prospect.html',
    'amaze': 'archive/starter-amaze-standalone.html',
    'midmarket': 'archive/starter-mid-market-renewal.html',
}

MIME_TYPES = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
}


# ─── Core Functions ───────────────────────────────────────────────────────────

def file_to_data_uri(filepath):
    """Convert an image file to a single-line base64 data URI."""
    ext = os.path.splitext(filepath)[1].lower()
    mime = MIME_TYPES.get(ext)
    if not mime:
        raise ValueError(f"Unknown image type: {ext}")
    with open(filepath, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f'data:{mime};base64,{data}'


def resolve_asset(name):
    """Find an asset file by name (exact or fuzzy match)."""
    exact = os.path.join(ASSETS_DIR, name)
    if os.path.exists(exact):
        return exact
    # Fuzzy match
    for fname in os.listdir(ASSETS_DIR):
        if name.lower() in fname.lower():
            return os.path.join(ASSETS_DIR, fname)
    return None


# ─── Embed: Convert relative paths to base64 ─────────────────────────────────

def embed_images(html, base_dir=None):
    """Replace all relative image paths with base64 data URIs.

    Handles:
    - src="../assets/filename.png"
    - src="assets/filename.png"
    - src="./assets/filename.png"
    """
    def replace_src(match):
        full_match = match.group(0)
        path = match.group(1)
        # Extract just the filename
        filename = os.path.basename(path)
        asset_path = resolve_asset(filename)
        if asset_path:
            try:
                data_uri = file_to_data_uri(asset_path)
                return f'src="{data_uri}"'
            except Exception as e:
                print(f"  WARNING: Could not embed {filename}: {e}", file=sys.stderr)
                return full_match
        else:
            print(f"  WARNING: Asset not found: {filename}", file=sys.stderr)
            return full_match

    # Match src attributes with relative paths to assets
    pattern = r'src="(\.\.?/assets/[^"]+|assets/[^"]+)"'
    result = re.sub(pattern, replace_src, html)
    return result


# ─── URL Conversion: base64 ↔ GitHub Pages URLs ─────────────────────────────

def build_asset_index():
    """Build a mapping of base64 data URI prefixes to asset filenames.

    For each asset, compute the first 80 chars of the base64 string — enough
    to uniquely identify any image without loading the full data URI.
    """
    index = {}
    for fname in os.listdir(ASSETS_DIR):
        fpath = os.path.join(ASSETS_DIR, fname)
        ext = os.path.splitext(fname)[1].lower()
        if ext not in MIME_TYPES or not os.path.isfile(fpath):
            continue
        try:
            data_uri = file_to_data_uri(fpath)
            # Use first 80 chars of the base64 portion as the fingerprint
            prefix = data_uri[:120]
            index[prefix] = fname
        except Exception:
            continue
    return index


def base64_to_urls(html):
    """Replace base64 data URIs with GitHub Pages URLs.

    Matches each base64 src against the asset library fingerprints.
    Falls back to a comment marker if no match is found.
    """
    index = build_asset_index()
    converted = 0
    unmatched = 0

    def replace_base64(match):
        nonlocal converted, unmatched
        data_uri = match.group(1)
        prefix = data_uri[:120]

        if prefix in index:
            fname = index[prefix]
            url = f'{GITHUB_PAGES_BASE}/{fname}'
            converted += 1
            return f'src="{url}"'

        # Try shorter prefixes as fallback
        for plen in [100, 80, 60]:
            short = data_uri[:plen]
            for idx_prefix, fname in index.items():
                if idx_prefix[:plen] == short:
                    url = f'{GITHUB_PAGES_BASE}/{fname}'
                    converted += 1
                    return f'src="{url}"'

        unmatched += 1
        return match.group(0)  # Leave as-is

    # Match base64 data URIs in src attributes
    result = re.sub(
        r'src="(data:image/[a-z+/]+;base64,[A-Za-z0-9+/=]+)"',
        replace_base64,
        html
    )

    print(f"  Converted {converted} images to URLs, {unmatched} unmatched")
    return result


def urls_to_base64(html):
    """Replace GitHub Pages URLs with base64 data URIs from local assets."""
    converted = 0

    def replace_url(match):
        nonlocal converted
        url = match.group(1)
        fname = url.split('/')[-1]
        asset_path = resolve_asset(fname)
        if asset_path:
            try:
                data_uri = file_to_data_uri(asset_path)
                converted += 1
                return f'src="{data_uri}"'
            except Exception as e:
                print(f"  WARNING: Could not convert {fname}: {e}", file=sys.stderr)
                return match.group(0)
        else:
            print(f"  WARNING: Asset not found locally: {fname}", file=sys.stderr)
            return match.group(0)

    pattern = re.escape(GITHUB_PAGES_BASE) + r'/([^"]+)'
    result = re.sub(f'src="({pattern})"', replace_url, html)
    print(f"  Converted {converted} URLs to base64")
    return result


def relative_to_urls(html):
    """Replace relative asset paths with GitHub Pages URLs."""
    converted = 0

    def replace_rel(match):
        nonlocal converted
        path = match.group(1)
        fname = os.path.basename(path)
        url = f'{GITHUB_PAGES_BASE}/{fname}'
        converted += 1
        return f'src="{url}"'

    result = re.sub(r'src="(\.\.?/assets/[^"]+|assets/[^"]+)"', replace_rel, html)
    print(f"  Converted {converted} relative paths to URLs")
    return result


# ─── Slide Replace ───────────────────────────────────────────────────────────

def get_slide_boundaries(html):
    """Get start/end positions of every slide div in the deck."""
    boundaries = []
    matches = list(re.finditer(r'<div class="slide"', html))
    for i, m in enumerate(matches):
        start = m.start()
        # Find the end: start of next slide, or end of slides-container
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            # Last slide — find the closing of slides-container
            container_end = html.find('</div><!-- /slides-container -->', start)
            if container_end == -1:
                # Fallback: find the comment block after the last slide
                comment = html.find('<!-- =====', start + 100)
                if comment == -1:
                    container_end = len(html)
                else:
                    end = comment
                    boundaries.append((start, end))
                    continue
            end = container_end
        boundaries.append((start, end))
    return boundaries


def replace_slide_by_number(html, slide_num, new_slide_html):
    """Replace slide N (1-indexed) with new HTML content."""
    boundaries = get_slide_boundaries(html)
    if slide_num < 1 or slide_num > len(boundaries):
        raise ValueError(f"Slide {slide_num} out of range (deck has {len(boundaries)} slides)")

    start, end = boundaries[slide_num - 1]
    return html[:start] + new_slide_html + html[end:]


def extract_slide_by_number(html, slide_num):
    """Extract slide N (1-indexed) as HTML string."""
    boundaries = get_slide_boundaries(html)
    if slide_num < 1 or slide_num > len(boundaries):
        raise ValueError(f"Slide {slide_num} out of range (deck has {len(boundaries)} slides)")

    start, end = boundaries[slide_num - 1]
    return html[start:end]


# ─── Plan Comparison Generator ───────────────────────────────────────────────
#
# Generates beautiful plan comparison slides matching the Nexus design system.
# Uses CSS variables (--df, --sg, --ch, --rs, --fl, --az-dk, --az-md, --ps, --nw)
# and fonts (--display = DM Serif Display, --body = DM Sans) from the deck CSS.
#
# Supports: medical, dental, vision, or any benefit comparison.
# Layout adapts: 2 cards (wide), 3 cards (medium), 4 cards (compact).
# Split mode: 4+ cards auto-split into 2 slides (2 per slide).
#
# YAML schema: see templates/ directory for examples.

# CSS variable mappings for tag colors
TAG_COLORS = {
    'current':     'var(--az-md)',   # Muted blue - neutral
    'renewal':     'var(--rs)',      # Rust/red - attention
    'recommended': 'var(--az-dk)',   # Deep blue - action
    'alternative': 'var(--fl)',      # Forest green - option
    'budget':      'var(--sg)',      # Sage - conservative
}


def _benefit_row(label, value, highlight=None):
    """Generate a single benefit row with optional highlight."""
    val_style = 'font-weight: 600; color: var(--ch);'
    if highlight == 'better':
        val_style += ' background: rgba(42,160,60,0.12); border-radius: 3px; padding: 0 3px;'
    elif highlight == 'worse':
        val_style += ' background: rgba(200,50,50,0.10); border-radius: 3px; padding: 0 3px;'
    return f'        <div style="display: flex; justify-content: space-between;"><span style="color: #4a5a50;">{label}</span><span style="{val_style}">{value}</span></div>'


def _divider():
    """Thin divider line between benefit groups."""
    return '        <div style="height: 1px; background: rgba(31,61,46,0.08); margin: 2px 0;"></div>'


def generate_plan_comparison(yaml_path):
    """Generate plan comparison slide(s) from YAML data.

    Returns a list of slide HTML strings. Auto-splits 4+ cards into 2 slides.
    """
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required. Install: pip3 install pyyaml")
        sys.exit(1)

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    cards = data.get('cards', [])
    title = data.get('title', 'Medical Plan Options')
    section = data.get('section', '05 \u2014 PLAN COMPARISON')
    layout = data.get('layout', 'auto')
    num_cards = len(cards)

    if layout == 'auto':
        layout = 'split' if num_cards >= 4 else 'single'

    if layout == 'split' and num_cards >= 4:
        mid = 2
        slides = []
        slides.append(_build_comparison_slide(
            cards[:mid], section, title,
            subtitle=data.get('slide1_subtitle', None)
        ))
        slides.append(_build_comparison_slide(
            cards[mid:],
            section,
            data.get('slide2_title', title + ' \u2014 Alternatives'),
            subtitle=data.get('slide2_subtitle', None)
        ))
        return slides
    else:
        return [_build_comparison_slide(cards, section, title)]


def _build_comparison_slide(cards, section, title, subtitle=None):
    """Build a single plan comparison slide with N cards."""
    num = len(cards)
    grid = f'repeat({num}, 1fr)'

    cards_html = []
    for card in cards:
        cards_html.append(_build_card(card))

    subtitle_html = ''
    if subtitle:
        subtitle_html = f'\n    <div style="font-size: 12px; color: var(--sg); margin-top: -10px; margin-bottom: 4px;">{subtitle}</div>'

    nl = chr(10)
    return f"""<div class="slide" style="padding: 44px 64px; background: var(--nw); display: flex; flex-direction: column;">

  <div style="margin-bottom: 14px;">
    <div class="slide-header-tag">{section}</div>
    <div class="slide-title" style="font-size: 26px;">{title}</div>{subtitle_html}
  </div>
  <div style="display: grid; grid-template-columns: {grid}; gap: 16px; flex: 1;">
{nl.join(cards_html)}
  </div>

  <div class="slide-footer">Nexus Benefit Solutions &mdash; Confidential</div>
</div>
"""


def _build_card(card, font='9px'):
    """Build a single plan comparison card matching Nexus design system."""
    tag = card.get('tag', 'CURRENT')
    tag_key = tag.lower().split()[0]
    tag_color = card.get('tag_color', TAG_COLORS.get(tag_key, 'var(--az-md)'))

    price_bg_map = {
        'var(--az-md)': 'rgba(43,108,176,0.08)',
        'var(--rs)':    'rgba(192,57,43,0.08)',
        'var(--az-dk)': 'rgba(26,63,107,0.08)',
        'var(--fl)':    'rgba(42,82,64,0.06)',
        'var(--sg)':    'rgba(90,106,94,0.06)',
    }
    price_bg = price_bg_map.get(tag_color, 'rgba(43,108,176,0.08)')

    bottom_bg_map = {
        'var(--az-md)': 'rgba(43,108,176,0.1)',
        'var(--rs)':    'rgba(192,57,43,0.1)',
        'var(--az-dk)': 'rgba(26,63,107,0.1)',
        'var(--fl)':    'rgba(42,82,64,0.08)',
        'var(--sg)':    'rgba(90,106,94,0.08)',
    }
    bottom_bg = bottom_bg_map.get(tag_color, 'rgba(43,108,176,0.1)')

    price_color = 'var(--df)' if tag_color == 'var(--fl)' else 'var(--az-dk)'

    logo_file = card.get('logo', '')
    logo_html = ''
    if logo_file:
        logo_src = f'{GITHUB_PAGES_BASE}/{logo_file}'
        logo_html = f'<img src="{logo_src}" alt="{card.get("carrier", "")}" style="height: 23px; object-fit: contain;">'

    plan_name = card.get('plan_name', '')
    monthly = card.get('monthly', '')
    annual = card.get('annual', '')
    change = card.get('change', '')
    bottom_text = card.get('bottom_text', '')

    change_html = ''
    if change:
        change_color = 'var(--rs)' if '+' in str(change) else 'var(--fl)'
        change_html = f' <span style="color: {change_color}; font-weight: 700;">{change}</span>'

    # Build benefit rows
    benefits = card.get('benefits', {})
    rows = []
    items = list(benefits.items())
    copay_start = None
    rx_start = None
    for i, (label, value) in enumerate(items):
        ll = label.lower()
        if copay_start is None and ll in ('pcp', 'specialist', 'copay'):
            copay_start = i
        if rx_start is None and ('rx' in ll or 'generic' in ll):
            rx_start = i

    for i, (label, value) in enumerate(items):
        if i == copay_start or i == rx_start:
            rows.append(_divider())
        highlight = None
        if isinstance(value, dict):
            highlight = value.get('highlight')
            value = value.get('value', '')
        rows.append(_benefit_row(label, str(value), highlight))

    nl = chr(10)
    benefits_html = nl.join(rows)

    # Rates section
    rates = card.get('rates', {})
    rates_html = ''
    if rates:
        rates_note = card.get('rates_note', '')
        rates_note_html = ''
        if rates_note:
            rates_note_html = f'        <div style="font-size: 7px; color: var(--sg); text-align: center; font-style: italic; margin-bottom: 2px;">{rates_note}</div>\n'
        rate_rows = []
        for tier, amt in rates.items():
            rate_rows.append(f'        <div style="display: flex; justify-content: space-between; padding: 1px 0;"><span style="color: #4a5a50;">{tier}</span><span style="font-weight: 600; color: var(--ch);">{amt}</span></div>')
        rates_html = f"""      <div style="margin-top: 6px; padding-top: 6px; border-top: 2px solid rgba(31,61,46,0.08);">
        <div style="font-weight: 600; text-align: center; margin-bottom: 3px; font-size: 8px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--sg);">Monthly Rates</div>
{rates_note_html}{nl.join(rate_rows)}
      </div>"""

    badge = card.get('badge', '')
    badge_html = ''
    if badge:
        badge_html = f'\n      <div style="text-align: center; font-size: 7px; font-weight: 700; color: var(--rs); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">{badge}</div>'

    bottom_html = ''
    if bottom_text:
        bottom_color = 'var(--az-dk)' if tag_color != 'var(--fl)' else 'var(--df)'
        bottom_html = f"""      <div style="margin-top: 6px; padding: 5px 8px; background: {bottom_bg}; border-radius: 4px; text-align: center;">
        <div style="font-size: 12px; color: {bottom_color}; font-weight: 500;">{bottom_text}</div>
      </div>"""

    return f"""    <!-- {card.get('carrier', '')} \u2014 {tag} -->
    <div style="background: var(--ps); border-radius: 8px; padding: 5px 10px 12px; display: flex; flex-direction: column; border-top: 3px solid {tag_color}; font-size: {font}; box-shadow: 0 3px 12px rgba(0,0,0,0.1), 0 1px 4px rgba(0,0,0,0.06);">
      <div style="display: flex; flex-direction: column; align-items: center; gap: 2px; margin-bottom: 3px;">{logo_html}<span style="font-size: 9px; color: {tag_color}; letter-spacing: 1px; text-transform: uppercase; font-weight: 600;">{tag}</span></div>
      <div style="font-family: var(--display); font-size: 11px; color: var(--df); margin-bottom: 6px; line-height: 1.3; text-align: center;">{plan_name}</div>
      <div style="text-align: center; padding: 7px 0; background: {price_bg}; border-radius: 5px; margin-bottom: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div style="font-family: var(--display); font-size: 18px; color: {price_color};">{monthly}<span style="font-family: var(--body); font-size: 9px; color: var(--sg); font-weight: 400;">/mo</span></div>
        <div style="font-size: 8px; color: var(--ch); display: flex; align-items: center; gap: 4px;">{annual}{change_html}</div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 3px; flex: 1;">
{benefits_html}
      </div>
{rates_html}
{badge_html}
{bottom_html}
    </div>"""


def generate_dental_vision(yaml_path):
    """Generate a dental & vision comparison slide from YAML data."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required. Install: pip3 install pyyaml")
        sys.exit(1)

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    section = data.get('section', '06 \u2014 ANCILLARY BENEFITS')
    title = data.get('title', 'Dental & Vision')
    subtitle = data.get('subtitle', '')
    dental = data.get('dental', {})
    vision = data.get('vision', {})
    rates = data.get('rates', {})
    combined = data.get('combined', {})

    subtitle_html = f'\n  <div style="font-size: 12px; color: var(--sg); margin-top: 30px; margin-bottom: 10px;">{subtitle}</div>' if subtitle else ''

    # Dental card
    dental_rows = ''
    for label, value in dental.get('benefits', {}).items():
        dental_rows += f'        <tr><td style="padding: 2px 0; color: var(--sg); border-bottom: 1px solid rgba(31,61,46,0.08);">{label}</td><td style="padding: 2px 0; text-align: right; font-weight: 600; color: var(--df); border-bottom: 1px solid rgba(31,61,46,0.08);">{value}</td></tr>\n'

    dental_html = f"""    <div style="background: var(--ps); border-radius: 6px; padding: 8px 12px; border-left: 3px solid var(--rs); display: flex; flex-direction: column;">
      <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px;">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--rs)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 2C4.5 2 3 4.5 3 7c0 2.5 1.2 4.5 1.8 6.5.6 2 1.2 4.5 2.2 6.5.5 1 1.2 2 2 2s1.2-.5 1.5-1.5c.3-1 .5-2 1.5-2s1.2 1 1.5 2c.3 1 .8 1.5 1.5 1.5s1.5-1 2-2c1-2 1.6-4.5 2.2-6.5C19.8 11.5 21 9.5 21 7c0-2.5-1.5-5-4-5-1.5 0-2.5.8-3.5 2h-3C9.5 2.8 8.5 2 7 2z"/></svg>
        <div style="font-family: var(--display); font-size: 12px; color: var(--df);">{dental.get('plan_name', 'Dental')}</div>
      </div>
      <table style="width: 100%; font-size: 9px; border-collapse: collapse;">
{dental_rows}      </table>
    </div>"""

    # Vision card
    vision_rows = ''
    for label, value in vision.get('benefits', {}).items():
        vision_rows += f'        <tr><td style="padding: 2px 0; color: var(--sg); border-bottom: 1px solid rgba(31,61,46,0.08);">{label}</td><td style="padding: 2px 0; text-align: right; font-weight: 600; color: var(--df); border-bottom: 1px solid rgba(31,61,46,0.08);">{value}</td></tr>\n'

    vision_html = f"""    <div style="background: var(--ps); border-radius: 6px; padding: 8px 12px; border-left: 3px solid var(--fl); display: flex; flex-direction: column;">
      <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px;">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--fl)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        <div style="font-family: var(--display); font-size: 12px; color: var(--df);">{vision.get('plan_name', 'Vision')}</div>
      </div>
      <table style="width: 100%; font-size: 9px; border-collapse: collapse;">
{vision_rows}      </table>
    </div>"""

    # Rate comparison table
    rate_table_html = ''
    if rates:
        columns = rates.get('columns', [])
        tiers = rates.get('tiers', [])
        totals = rates.get('totals', {})

        col_headers = ''
        sub_headers = ''
        for col in columns:
            col_name = col.get('name', '')
            col_color = col.get('color', 'var(--df)')
            colspan = col.get('colspan', 1)
            col_headers += f'          <th colspan="{colspan}" style="padding: 3px 6px; text-align: center; font-weight: 600; color: {col_color}; border-bottom: 2px solid rgba(31,61,46,0.12);">{col_name}</th>\n'
            for sub in col.get('subs', [col_name]):
                sub_headers += f'          <th style="padding: 2px 6px; text-align: right; font-weight: 500; color: var(--sg); font-size: 8px; border-bottom: 1px solid rgba(31,61,46,0.08);">{sub}</th>\n'

        tier_rows = ''
        for i, tier in enumerate(tiers):
            bg = ' style="background: rgba(31,61,46,0.02);"' if i % 2 == 1 else ''
            tier_name = tier.get('name', '')
            cells = ''
            for j, val in enumerate(tier.get('values', [])):
                weight = 'font-weight: 600; color: var(--df);' if j % 2 == 1 else 'color: var(--sg);'
                cells += f'<td style="padding: 3px 6px; text-align: right; {weight}">{val}</td>'
            tier_rows += f'        <tr{bg}><td style="padding: 3px 0; color: var(--df); font-weight: 500;">{tier_name}</td>{cells}</tr>\n'

        total_cells = ''
        for val in totals.get('values', []):
            color = totals.get('color', 'var(--df)')
            total_cells += f'<td style="padding: 4px 6px; text-align: right; font-weight: 700; color: {color};">{val}</td>'

        rate_table_html = f"""  <div style="margin-top: 8px; background: var(--ps); border-radius: 6px; padding: 7px 14px;">
    <table style="width: 100%; font-size: 9px; border-collapse: collapse;">
      <thead>
        <tr>
          <th style="padding: 3px 0; text-align: left; font-weight: 600; color: var(--df); border-bottom: 2px solid rgba(31,61,46,0.12);"></th>
{col_headers}        </tr>
        <tr>
          <th style="padding: 2px 0; text-align: left; font-weight: 500; color: var(--sg); font-size: 8px; border-bottom: 1px solid rgba(31,61,46,0.08);">Tier</th>
{sub_headers}        </tr>
      </thead>
      <tbody>
{tier_rows}      </tbody>
      <tfoot>
        <tr style="border-top: 2px solid rgba(31,61,46,0.12);"><td style="padding: 4px 0; font-weight: 600; color: var(--df);">Group Total</td>{total_cells}</tr>
      </tfoot>
    </table>
  </div>"""

    combined_html = ''
    if combined:
        combined_html = f"""  <div style="margin-top: 8px; padding: 8px 20px; background: rgba(31,61,46,0.04); border: 1px solid var(--ps); border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 11px; color: var(--ch);"><strong style="color: var(--df);">{combined.get('label', 'Combined Dental & Vision')}</strong></div>
    <div style="display: flex; gap: 18px; align-items: center;">
      <div style="font-family: var(--display); font-size: 16px; color: var(--df);">{combined.get('monthly', '')}<span style="font-family: var(--body); font-size: 9px; color: var(--sg); font-weight: 400;">/mo</span></div>
      <div style="width: 1px; height: 18px; background: rgba(31,61,46,0.12);"></div>
      <div style="font-family: var(--display); font-size: 16px; color: var(--rs);">{combined.get('annual', '')}<span style="font-family: var(--body); font-size: 9px; color: var(--sg); font-weight: 400;">/yr</span></div>
    </div>
  </div>"""

    return f"""<div class="slide" style="padding: 44px 64px; background: var(--nw); display: flex; flex-direction: column;">

  <div style="margin-bottom: 0;">
    <div class="slide-header-tag">{section}</div>
    <div class="slide-title" style="font-size: 26px; margin-bottom: 0;">{title}</div>
  </div>{subtitle_html}
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
{dental_html}
{vision_html}
  </div>
{rate_table_html}
{combined_html}

  <div class="slide-footer">Nexus Benefit Solutions &mdash; Confidential</div>
</div>
"""


# ─── Fix Broken Starters (ASSET comment format) ──────────────────────────────

def fix_broken_starter(html):
    """Fix starters that have ASSET comments with multi-line base64.

    Pattern in broken starters:
        <img src="data:image/svg+xml;base64,PHN2ZyB...
        <!-- ASSET: filename.ext (NNN bytes) -->
        data:image/type;base64,AAABBB...actual data...==
        " style="..." alt="...">

    Fix: extract filename from ASSET comment, read actual file, replace entire
    broken img tag with a clean one using single-line base64.
    """
    # Find all broken img tags that contain ASSET comments
    pattern = re.compile(
        r'(<img\s+)'                             # img tag start
        r'src="data:image/[^;]+;base64,[^\n]*\n'  # broken src start + newline
        r'<!-- ASSET:\s*([^\s(]+)[^>]*-->\n'      # ASSET comment with filename
        r'data:image/[^\n]+\n'                     # actual base64 line
        r'"\s*'                                    # closing quote
        r'((?:style|alt|class)[^>]*>)',            # remaining attributes
        re.MULTILINE
    )

    def replace_broken(match):
        img_start = match.group(1)    # '<img '
        filename = match.group(2)      # 'filename.ext'
        rest = match.group(3)          # 'style="..." alt="...">'

        asset_path = resolve_asset(filename)
        if asset_path:
            data_uri = file_to_data_uri(asset_path)
            return f'{img_start}src="{data_uri}" {rest}'
        else:
            print(f"  WARNING: Asset not found for ASSET comment: {filename}", file=sys.stderr)
            return match.group(0)

    result = pattern.sub(replace_broken, html)

    # Also clean up any remaining floating ASSET blocks
    result = re.sub(
        r'\n<!-- ASSET: [^\n]+-->\ndata:image/[^\n]+\n',
        '\n',
        result
    )

    return result


# ─── Verify: Check deck image integrity ───────────────────────────────────────

def verify_deck(html):
    """Verify all images in a deck are properly formed."""
    issues = []

    # Check for multi-line src attributes (base64 with newlines)
    multiline_srcs = re.findall(
        r'src="data:image/[a-z+/]+;base64,[A-Za-z0-9+/=]+\n', html
    )
    if multiline_srcs:
        issues.append(f'{len(multiline_srcs)} img src attributes have newlines in base64 (BROKEN)')

    # Check for ASSET comments inside img tags
    asset_in_img = re.findall(r'<img[^>]*<!-- ASSET:', html, re.DOTALL)
    if asset_in_img:
        issues.append(f'{len(asset_in_img)} img tags contain ASSET comments (BROKEN)')

    # Check for img tags that bleed into next elements
    img_tags = list(re.finditer(r'<img[^>]+>', html, re.DOTALL))
    bleeding = 0
    for m in img_tags:
        tag = m.group(0)
        if '<div' in tag or '</div' in tag:
            bleeding += 1
    if bleeding:
        issues.append(f'{bleeding} img tags bleed into adjacent HTML (BROKEN)')

    # Check for multi-line img tags
    unclosed = 0
    for m in img_tags:
        tag = m.group(0)
        if '\n' in tag:
            unclosed += 1
    if unclosed:
        issues.append(f'{unclosed} img tags span multiple lines (BROKEN)')

    # Check for floating ASSET comments
    floating = len(re.findall(r'\n<!-- ASSET: [^\n]+-->\ndata:image/', html))
    if floating:
        issues.append(f'{floating} floating ASSET comment blocks (cleanup needed)')

    # Check for relative path images (not embedded)
    relative = len(re.findall(r'src="\.\.?/assets/', html))
    if relative:
        issues.append(f'{relative} images use relative paths (not standalone — run --embed)')

    total = len(img_tags)

    return {
        'total_images': total,
        'issues': issues,
        'clean': len(issues) == 0,
    }


# ─── Rebuild Starters ────────────────────────────────────────────────────────

def rebuild_starters():
    """Rebuild all starter decks from finished decks with embedded base64.

    For starters WITH a finished deck: read finished deck, embed relative paths.
    For starters WITHOUT a finished deck: fix broken ASSET comments in place.
    """
    results = {}

    # Phase 1: Rebuild from finished decks
    for name, finished_path in FINISHED_DECKS.items():
        starter_name = STARTER_MAP.get(name)
        if not starter_name:
            continue
        starter_path = os.path.join(PRESENTATIONS_DIR, starter_name)

        if not os.path.exists(finished_path):
            print(f"  SKIP {name}: finished deck not found at {finished_path}")
            results[name] = 'skipped'
            continue

        print(f"  Building {starter_name} from {os.path.basename(finished_path)}...")

        with open(finished_path) as f:
            html = f.read()

        embedded = embed_images(html)
        check = verify_deck(embedded)

        if os.path.exists(starter_path):
            shutil.copy2(starter_path, starter_path + '.bak')

        with open(starter_path, 'w') as f:
            f.write(embedded)

        if check['clean']:
            print(f"  ✓ {starter_name}: {check['total_images']} images, CLEAN")
            results[name] = 'clean'
        else:
            print(f"  ✗ {starter_name}: {len(check['issues'])} issues")
            results[name] = 'issues'

    # Phase 2: Fix starters without finished decks (e.g., midmarket)
    for name, starter_fname in STARTER_MAP.items():
        if name in results:
            continue  # Already handled above
        starter_path = os.path.join(PRESENTATIONS_DIR, starter_fname)
        if not os.path.exists(starter_path):
            continue

        print(f"  Fixing {starter_fname} (no finished deck — fixing ASSET comments)...")

        with open(starter_path) as f:
            html = f.read()

        fixed = fix_broken_starter(html)
        check = verify_deck(fixed)

        shutil.copy2(starter_path, starter_path + '.bak')
        with open(starter_path, 'w') as f:
            f.write(fixed)

        if check['clean']:
            print(f"  ✓ {starter_fname}: {check['total_images']} images, CLEAN")
            results[name] = 'clean'
        else:
            print(f"  ✗ {starter_fname}: {len(check['issues'])} issues:")
            for issue in check['issues']:
                print(f"    ✗ {issue}")
            results[name] = 'issues'

    return results


# ─── New Deck: Copy starter + text replacements ──────────────────────────────

def new_deck(starter_name, client_name, output_path):
    """Create a new client deck from a starter template."""
    # Find the starter
    starter_path = None
    for key, fname in STARTER_MAP.items():
        if starter_name.lower() in key.lower() or starter_name.lower() in fname.lower():
            starter_path = os.path.join(PRESENTATIONS_DIR, fname)
            break

    if not starter_path or not os.path.exists(starter_path):
        print(f"ERROR: Starter '{starter_name}' not found. Available: {list(STARTER_MAP.keys())}")
        sys.exit(1)

    # Verify starter is clean first
    with open(starter_path) as f:
        html = f.read()

    check = verify_deck(html)
    if not check['clean']:
        print(f"WARNING: Starter has image issues. Run --rebuild-starters first.")
        for issue in check['issues']:
            print(f"  ✗ {issue}")

    # Basic text replacements (Claude Code will do the detailed customization)
    html = html.replace('[Client Name]', client_name)
    html = html.replace('[Company Name]', client_name)
    html = html.replace('Client Name', client_name)

    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✓ New deck created: {output_path}")
    print(f"  Source: {os.path.basename(starter_path)}")
    print(f"  Client: {client_name}")
    print(f"  Images: {check['total_images']} (all embedded)")


# ─── Add Image: Embed a new asset into a deck ────────────────────────────────

def add_image_to_deck(deck_path, asset_name, alt_text=None):
    """Get the img tag HTML for adding a new image to a deck.

    Returns the complete <img> tag as a single line, ready to paste.
    """
    asset_path = resolve_asset(asset_name)
    if not asset_path:
        print(f"ERROR: Asset '{asset_name}' not found in {ASSETS_DIR}")
        sys.exit(1)

    data_uri = file_to_data_uri(asset_path)
    alt = alt_text or os.path.splitext(asset_name)[0].replace('-', ' ').title()

    # Output the complete img tag
    img_tag = f'<img src="{data_uri}" alt="{alt}" style="max-height: 60px; object-fit: contain;">'
    print(f"<!-- Image: {asset_name} ({os.path.getsize(asset_path)} bytes) -->")
    print(img_tag)
    return img_tag


# ─── Slide Operations ─────────────────────────────────────────────────────────

def extract_slide(html, slide_identifier):
    """Extract a single slide from an HTML deck by text content match."""
    slides = list(re.finditer(r'<div class="slide"', html))
    for i, m in enumerate(slides):
        start = m.start()
        end = slides[i + 1].start() if i + 1 < len(slides) else len(html)
        chunk = html[start:end]
        if slide_identifier in chunk:
            return chunk
    return None


def extract_all_slides(html):
    """Extract all slides as (index, title, html) tuples."""
    slides = list(re.finditer(r'<div class="slide"', html))
    results = []
    for i, m in enumerate(slides):
        start = m.start()
        end = slides[i + 1].start() if i + 1 < len(slides) else len(html)
        chunk = html[start:end]
        title_match = re.search(r'slide-title[^>]*>([^<]+)', chunk)
        header_match = re.search(r'slide-header-tag[^>]*>([^<]+)', chunk)
        section_match = re.search(r'section-tag[^>]*>([^<]+)', chunk)
        title = (title_match or header_match or section_match)
        title_text = title.group(1).strip() if title else f'Slide {i + 1}'
        results.append((i + 1, title_text, chunk))
    return results


# ─── Asset Operations ─────────────────────────────────────────────────────────

def list_assets():
    """List all available assets."""
    assets = []
    for fname in sorted(os.listdir(ASSETS_DIR)):
        fpath = os.path.join(ASSETS_DIR, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1].lower()
            if ext in MIME_TYPES:
                assets.append({
                    'name': fname,
                    'path': fpath,
                    'size_bytes': os.path.getsize(fpath),
                    'mime': MIME_TYPES[ext],
                })
    return assets


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Nexus Deck Assembly Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Create a client deck (URL-based, lightweight):
    python3 assemble_deck.py --new-deck renewal --client "Sena Info Tech" -o sena-deck.html

  Convert base64 deck to URL-based (450KB → 35KB):
    python3 assemble_deck.py --to-urls big-deck.html -o light-deck.html

  Convert URL deck to standalone base64:
    python3 assemble_deck.py --to-base64 light-deck.html -o standalone-deck.html

  Extract slide 9:
    python3 assemble_deck.py --extract-slide deck.html --slide-num 9 -o slide9.html

  Replace slide 9 with edited version:
    python3 assemble_deck.py --replace-slide deck.html --slide-num 9 --slide-html slide9.html

  Generate plan comparison from YAML:
    python3 assemble_deck.py --plan-comparison plans.yaml -o comparison-slide.html

  Verify a deck:
    python3 assemble_deck.py --verify my-deck.html
        """
    )

    parser.add_argument('--embed', metavar='DECK', help='Embed relative-path images as base64')
    parser.add_argument('--to-urls', metavar='DECK', help='Convert base64 images to GitHub Pages URLs')
    parser.add_argument('--to-base64', metavar='DECK', help='Convert GitHub Pages URLs to embedded base64')
    parser.add_argument('--rebuild-starters', action='store_true', help='Rebuild all starters from finished decks')
    parser.add_argument('--new-deck', metavar='STARTER', help='Create new deck from a starter (renewal/prospect/amaze)')
    parser.add_argument('--client', metavar='NAME', help='Client name for new deck')
    parser.add_argument('--verify', metavar='DECK', help='Verify deck image integrity')
    parser.add_argument('--add-image', metavar='DECK', help='Generate img tag for an asset')
    parser.add_argument('--asset', metavar='NAME', help='Asset filename for --add-image')
    parser.add_argument('--list-assets', action='store_true', help='List all available assets')
    parser.add_argument('--asset-to-base64', metavar='NAME', help='Get base64 data URI for an asset')
    parser.add_argument('--extract-slide', metavar='DECK', help='Extract a slide by number or text match')
    parser.add_argument('--slide-name', metavar='TEXT', help='Text to identify the slide')
    parser.add_argument('--slide-num', metavar='N', type=int, help='Slide number (1-indexed)')
    parser.add_argument('--replace-slide', metavar='DECK', help='Replace a slide in a deck')
    parser.add_argument('--slide-html', metavar='FILE', help='HTML file containing the replacement slide')
    parser.add_argument('--plan-comparison', metavar='YAML', help='Generate plan comparison slide from YAML')
    parser.add_argument('--dental-vision', metavar='YAML', help='Generate dental & vision comparison slide from YAML')
    parser.add_argument('--list-slides', metavar='DECK', help='List all slides in a deck')
    parser.add_argument('--output', '-o', metavar='FILE', help='Output file path')

    args = parser.parse_args()

    if args.rebuild_starters:
        print("Rebuilding all starter decks from finished decks...\n")
        results = rebuild_starters()
        print(f"\nDone. {sum(1 for v in results.values() if v == 'clean')}/{len(results)} clean.")

    elif args.to_urls:
        print(f"Converting {args.to_urls} to URL-based images...")
        with open(args.to_urls) as f:
            html = f.read()
        # Handle both base64 and relative paths
        result = base64_to_urls(html)
        result = relative_to_urls(result)
        out = args.output or args.to_urls.replace('.html', '-urls.html')
        with open(out, 'w') as f:
            f.write(result)
        old_size = os.path.getsize(args.to_urls)
        new_size = os.path.getsize(out)
        print(f"✓ {out}: {old_size:,}B → {new_size:,}B ({100 - new_size * 100 // old_size}% smaller)")

    elif args.to_base64:
        print(f"Converting {args.to_base64} to embedded base64...")
        with open(args.to_base64) as f:
            html = f.read()
        result = urls_to_base64(html)
        out = args.output or args.to_base64.replace('.html', '-standalone.html')
        with open(out, 'w') as f:
            f.write(result)
        print(f"✓ {out}: standalone deck with embedded images")

    elif args.embed:
        with open(args.embed) as f:
            html = f.read()
        embedded = embed_images(html)
        check = verify_deck(embedded)
        out = args.output or args.embed.replace('.html', '-embedded.html')
        with open(out, 'w') as f:
            f.write(embedded)
        if check['clean']:
            print(f"✓ {out}: {check['total_images']} images embedded, CLEAN")
        else:
            print(f"✗ {out}: {check['total_images']} images, {len(check['issues'])} issues:")
            for issue in check['issues']:
                print(f"  ✗ {issue}")

    elif args.new_deck:
        if not args.client:
            print("ERROR: --client required with --new-deck")
            sys.exit(1)
        out = args.output or f"{args.client.lower().replace(' ', '-')}-deck.html"
        new_deck(args.new_deck, args.client, out)

    elif args.replace_slide:
        if not args.slide_num:
            print("ERROR: --slide-num required with --replace-slide")
            sys.exit(1)
        if not args.slide_html:
            print("ERROR: --slide-html required with --replace-slide")
            sys.exit(1)
        with open(args.replace_slide) as f:
            html = f.read()
        with open(args.slide_html) as f:
            new_slide = f.read()
        try:
            result = replace_slide_by_number(html, args.slide_num, new_slide)
            out = args.output or args.replace_slide
            with open(out, 'w') as f:
                f.write(result)
            print(f"✓ Slide {args.slide_num} replaced in {out}")
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(1)

    elif args.plan_comparison:
        print(f"Generating plan comparison from {args.plan_comparison}...")
        slides = generate_plan_comparison(args.plan_comparison)
        if args.output:
            if len(slides) == 1:
                with open(args.output, 'w') as f:
                    f.write(slides[0])
                print(f"✓ 1 slide written to {args.output}")
            else:
                base, ext = os.path.splitext(args.output)
                for i, slide in enumerate(slides, 1):
                    path = f"{base}-{i}{ext}"
                    with open(path, 'w') as f:
                        f.write(slide)
                    print(f"✓ Slide {i} written to {path}")
        else:
            for i, slide in enumerate(slides, 1):
                if len(slides) > 1:
                    print(f"\n<!-- SLIDE {i} -->")
                print(slide)

    elif args.dental_vision:
        print(f"Generating dental & vision slide from {args.dental_vision}...")
        slide_html = generate_dental_vision(args.dental_vision)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(slide_html)
            print(f"✓ Dental & vision slide written to {args.output}")
        else:
            print(slide_html)

    elif args.verify:
        with open(args.verify) as f:
            html = f.read()
        result = verify_deck(html)
        # Also check for URL-based images
        url_count = len(re.findall(re.escape(GITHUB_PAGES_BASE), html))
        base64_count = len(re.findall(r'src="data:image/', html))
        relative_count = len(re.findall(r'src="\.\.?/assets/', html))
        if result['clean']:
            print(f"✓ CLEAN — {result['total_images']} images")
        else:
            print(f"✗ ISSUES — {result['total_images']} images:")
            for issue in result['issues']:
                print(f"  ✗ {issue}")
        print(f"  Image sources: {url_count} URL, {base64_count} base64, {relative_count} relative")

    elif args.add_image:
        if not args.asset:
            print("ERROR: --asset required with --add-image")
            sys.exit(1)
        add_image_to_deck(args.add_image, args.asset)

    elif args.list_assets:
        assets = list_assets()
        print(f"{'Name':<40} {'Size':>8}  {'URL'}")
        print('-' * 100)
        for a in assets:
            url = f"{GITHUB_PAGES_BASE}/{a['name']}"
            print(f"{a['name']:<40} {a['size_bytes']:>7}B  {url}")
        print(f"\n{len(assets)} assets in {ASSETS_DIR}")
        print(f"GitHub Pages: {GITHUB_PAGES_BASE}/")

    elif args.asset_to_base64:
        path = resolve_asset(args.asset_to_base64)
        if path:
            print(file_to_data_uri(path))
        else:
            print(f"Asset not found: {args.asset_to_base64}")
            sys.exit(1)

    elif args.extract_slide:
        with open(args.extract_slide) as f:
            html = f.read()
        slide = None
        if args.slide_num:
            try:
                slide = extract_slide_by_number(html, args.slide_num)
            except ValueError as e:
                print(f"ERROR: {e}")
                sys.exit(1)
        elif args.slide_name:
            slide = extract_slide(html, args.slide_name)
        else:
            print("ERROR: --slide-num or --slide-name required")
            sys.exit(1)

        if slide:
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(slide)
                print(f"Slide extracted to {args.output}")
            else:
                print(slide)
        else:
            print(f"Slide not found")
            sys.exit(1)

    elif args.list_slides:
        with open(args.list_slides) as f:
            html = f.read()
        slides = extract_all_slides(html)
        for num, title, chunk in slides:
            size = len(chunk)
            img_count = len(re.findall(r'<img', chunk))
            print(f"  {num:>2}. {title:<50} ({size:,}B, {img_count} imgs)")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
