# Presentation Deck Builder — Project Documentation

## Vision
A complete presentation system for Nexus Benefit Solutions advisors. Advisors come here to build customized slide decks for prospect and client meetings. Every deck follows the same design system, stays on-brand, and can be produced quickly by picking a template and filling in client data.

Long-term: expand to include additional templates, a component library of reusable elements, and responsive web page versions of presentations for mobile/leave-behind use cases.

## Current State

### Templates (3 built, optimized, production-ready)

| Template | File | Slides | Use Case |
|----------|------|--------|----------|
| Small Group Renewal | `small_group_renewal_deck/small-group-renewal-deck-v1.html` | 24 | Existing clients with upcoming renewal. Renewal analysis + plan comparison + Amaze/Biomed pitch. |
| Small Group Prospect | `small_group_prospect_deck/small-group-prospect-deck-v1.html` | 19 | New prospects. Discovery recap + benchmarking + capabilities + Amaze/Biomed pitch. |
| Amaze Biomed Standalone | `amaze_biomed_nexus_deck/amaze-biomed-nexus-deck-v1.html` | 17 | Standalone Amaze/Biomed program pitch. Not tied to any prospect. Used with Amaze reps. |

### Design System
All templates share one unified design system documented in `INSTRUCTIONS.md`:
- **Dimensions:** 960x540px slides, CSS-scaled
- **Fonts:** DM Serif Display (headings) + DM Sans (body) — Google Fonts
- **Colors:** Nexus green/earth palette (7 variables) + Amaze blue/teal palette (4 variables) + 13 RGBA white opacity variables
- **Color flow:** Green intro → Blue Amaze section → Green closing (every deck)
- **Assets:** Shared `assets/` folder at project root

### Optimizations Applied (Mar 1, 2026)
- **13 RGBA CSS variables** added to `:root` in all templates (`--white-06` through `--white-90`)
- **14 utility CSS classes** extracted from repeated inline styles (`.check-item`, `.faq-card`, `.feature-card`, `.stat-badge`, `.client-card`, `.section-tag-blue`, etc.)
- **~190 inline→class replacements** across all three files
- **`<!-- EDITABLE: ... -->` / `<!-- FIXED: ... -->`** comment markers added throughout for agent guidance
- **Enhanced print CSS** — `@media print` block with `print-color-adjust: exact` for Chrome PDF output
- **Responsive scroll mode** — `?mode=responsive` URL parameter stacks slides vertically for quick scrollable viewing
- **Template identifier watermarks** on all title slides (right panel) — covered by company images when customized

### File Structure
```
sales_presentations_templates/
  CLAUDE.md                                    ← This file (project documentation)
  INSTRUCTIONS.md                              ← Agent instructions for Claude Projects (Co-Work)
  assets/                                      ← Shared images, logos, photos
    jason-bearup.jpg, ken-fortier.jpg, grace-morris.jpg
    amaze-logo.png, nexus-logo-white.svg, nexus-logo-forest.svg
    bcbs-michigan-logo.png, priorityhealth-logo-green.svg
    galileo-logo.svg, healthjoy-logo.png, teladoc-logo.png,
    mdlive-logo.svg, recuro-logo.png, firefly-logo.png,
    talkspace-logo.png, cerebral-logo.png
    doctor-telehealth.jpg, comparison-icon-*.svg (8 icons)
  finished-amaze_biomed_nexus_deck/
    amaze-biomed-nexus-deck-v1.html
    CLAUDE.md                                  ← Deck-specific documentation
  finished-small_group_prospect_deck/
    small-group-prospect-deck-v1.html
  finished-small_group_renewal_deck/
    small-group-renewal-deck-v1.html
```

### Prospect/Client Deck Workflow
- Templates live here. Customized decks live in the prospect/client folder under `sales/2_Prospects/` or `sales/1_Clients/`.
- When a deck is finalized, host it on GitHub Pages and add a `.webloc` link file to the prospect folder pointing to the live URL (not the repo).
- Finished deliverables get dropped into the client's OneDrive folder for long-term storage and mobile access.

### Claude Projects (Co-Work) Setup
Upload to a Claude Desktop project:
- **System prompt:** `INSTRUCTIONS.md`
- **Knowledge files:** All 3 HTML templates + key assets (logos, team photos)
- Agents in Co-Work follow INSTRUCTIONS.md to guide advisors through template selection, data gathering, and deck customization.

## Output Formats

### 1. Slide Deck (Primary)
The standard format. Fixed 960x540 slides with arrow-key navigation. Like PowerPoint in a browser.
- **File:** `template-name-v1.html`
- **Use:** Meetings, presentations, screen sharing

### 2. Scrollable Web View (Quick)
Same slide deck file, different rendering. Stacks all slides vertically for scrolling.
- **Activate:** `file.html?mode=responsive`
- **Use:** Quick sharing when someone just needs to scroll through

### 3. Responsive Web Page (Separate File)
A completely separate HTML file that presents the same content as a proper responsive website. Not slides stacked — flowing content, mobile-first, text reflows. Like a well-designed landing page.
- **File:** `template-name-v1-web.html` (alongside the slide deck)
- **Use:** Leave-behinds, shareable links, mobile viewing
- **Build:** Only when requested. Not every deck needs one.
- **Details:** Full documentation in INSTRUCTIONS.md under "Responsive Web Page Format"

### 4. Print (CSS Mode)
Both slide decks and web pages support printing via `@media print` CSS already embedded.
- **How:** Chrome → Print → check "Background graphics" → Landscape → None margins → Save as PDF

## Team on All Decks
- **Jason Bearup** — Lead Advisor
- **Ken Fortier** — Relationship Manager
- **Grace Morris** — Account Manager
- Phone numbers are placeholders in templates — update per deck

## Future Plans

### Additional Templates (Planned)
No specific templates designed yet. As new meeting types come up, new templates will be built following the same design system. Likely candidates:
- Large group prospect/renewal
- HR-focused benefits overview
- Open enrollment employee presentation
- Amaze Health employee-facing pitch

### Component Library (Planned)
A reference HTML file (`components.html`) containing every reusable slide element — stat cards, tables, FAQ grids, timelines, etc. Agents copy from here instead of writing markup from scratch. Ensures everything stays on-brand even when customizing.

Not built yet. INSTRUCTIONS.md has enough guidance for now. Build when template count grows and component reuse becomes frequent.

### Responsive Web Page Templates (Planned)
Instructions are documented in INSTRUCTIONS.md. No web page templates built yet. Build the first one when an advisor requests a web version of a specific deck, then use it as a reference for future web pages.

## Session History

### Mar 1, 2026 — Template Optimization & System Buildout
- Built all 3 templates from prior sessions' work (Amaze deck from Harloff/NMJS sources, Prospect/Renewal as new builds)
- Reorganized folder structure (subfolders per template, shared assets)
- Genericized all templates (removed client-specific data, added placeholders)
- Created INSTRUCTIONS.md for Claude Projects
- CSS optimization pass: 13 RGBA variables, 14 utility classes, ~190 inline replacements
- Fixed HTML comment `--` issue (changed to em dashes)
- Updated prospect closing slide to match renewal (team photos)
- Added template identifier watermarks to all three title slides
- Added enhanced print CSS and `?mode=responsive` scroll mode to all templates
- Documented responsive web page format in INSTRUCTIONS.md
- Documented print workflow in INSTRUCTIONS.md

### Mar 1, 2026 — Prospect Folder Consolidation & Backup
- Harloff prospect folder consolidated: 3 HTML files + factory image moved from Downloads, live presentation link added
- Northern Jet webloc renamed and pointed to live GitHub Pages URL (not repo)
- Removed stale GitHub Repo webloc files from all template folders (templates don't need repo links)
- Updated both prospect CLAUDE.md files with correct local paths and live links
- iCloud backup set up via launchd rsync job (every 15 min, excludes .git/node_modules)

## Open Items
- [ ] Phone numbers still placeholders on all template closing slides
- [ ] Client Momentum slide (Amaze deck slide 14) has placeholder logos/names
- [ ] Component library not built yet (instructions sufficient for now)
- [ ] No responsive web page templates built yet (instructions documented, build on demand)
- [ ] Cameron Manning and Brenda Manning photos in assets but not on any current template team slides
