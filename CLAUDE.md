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

### GitHub Repositories

Two repos manage the presentation system:

| Repo | URL | Pages URL | Purpose |
|------|-----|-----------|---------|
| `presentation-templates` | github.com/jbearup1981/presentation-templates | jbearup1981.github.io/presentation-templates/ | Templates, assets, design system, instructions |
| `client-presentations` | github.com/jbearup1981/client-presentations | jbearup1981.github.io/client-presentations/ | Finished client decks (Harloff, Northern Jet, etc.) |

**Template repo structure:**
```
presentation-templates/
  INSTRUCTIONS.md                              ← Sole file for Claude project
  team.md                                      ← Full team directory (7 members)
  assets/                                      ← Shared images, logos, photos
  components/
    base/
      base.css                                 ← All shared CSS (vars, fonts, utilities, print)
      base.js                                  ← Navigation, scaling, fullscreen, responsive mode
    slides/
      nexus-title.html ... nexus-closing.html  ← 7 Nexus green slides
      benchmarking-simple.html ... client-portal.html  ← 9 benchmarking/discovery slides
      amaze-problem.html ... amaze-implementation.html ← 12 Amaze blue slides
      blank-green.html ... blank-transition.html       ← 4 blank templates
    catalog.html                               ← Visual catalog — all 32 slides as thumbnails
  recipes/
    small-group-renewal.md                     ← 24-slide recipe
    small-group-prospect.md                    ← 19-slide recipe
    amaze-standalone.md                        ← 17-slide recipe
  finished-amaze_biomed_nexus_deck/            ← Reference templates (design source)
  finished-small_group_prospect_deck/
  finished-small_group_renewal_deck/
```

### Modular Component System (Built Mar 2, 2026)
Decks are assembled from 32 individual slide components — like Lego pieces. Each component is a standalone HTML file containing just the `<div class="slide">...</div>` block. The agent:
1. Fetches `base.css` + `base.js` for the HTML shell
2. Fetches selected slide components from `components/slides/`
3. Inserts them into the shell in order
4. Customizes EDITABLE fields with client data
5. Outputs a complete standalone HTML deck

**Key URLs:**
- **Catalog:** `https://jbearup1981.github.io/presentation-templates/components/catalog.html`
- **Slides:** `https://jbearup1981.github.io/presentation-templates/components/slides/[name].html`
- **Assets:** `https://jbearup1981.github.io/presentation-templates/assets/[filename]`
- **Recipes:** `https://jbearup1981.github.io/presentation-templates/recipes/[name].md`

### Prospect/Client Deck Workflow
1. Advisor uses Claude project → picks slides from catalog or recipe
2. Agent assembles custom deck from components
3. Finished deck gets committed to the `client-presentations` repo
4. GitHub Pages hosts the live version — add a `.webloc` link to the prospect/client folder
5. Final deliverable also drops into the client's OneDrive folder

### Claude Projects Setup
**One project, ultra-lean context.** Only `INSTRUCTIONS.md` goes into the Claude project:
- **Project instructions:** `INSTRUCTIONS.md` (pasted as system prompt — sole knowledge file)
- **GitHub integration:** Connected to `jbearup1981/presentation-templates` repo
- **How it works:** Agent fetches only the specific slide components needed — not entire templates. Each component is ~2-5KB. A 20-slide deck loads ~60-100KB of slide HTML vs. 150KB+ for a monolithic template.
- **Scales cleanly:** New components/recipes added to the repo. No project reconfiguration needed.

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

## Team
Full team directory in `team.md` (7 members): Jason Bearup, Ken Fortier, Brenda Manning, Cameron Manning, Tom Snikkers, Grace Morris, Sophie Sanders. Agent fetches this when building any deck and asks which team members to include.

**Default team (if not specified):** Jason Bearup, Ken Fortier, Grace Morris.

## Future Plans

### Additional Slide Components
New components can be added anytime by creating a new HTML file in `components/slides/`, updating the catalog, and adding to relevant recipes. Likely additions:
- Large group benchmarking slides
- HR-focused benefits overview
- Open enrollment employee-facing slides

### Responsive Web Page Templates (Planned)
Build the first one when an advisor requests a web version of a specific deck, then use it as a reference for future web pages.

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

### Mar 2, 2026 — Git Repo Structure & Claude Projects Architecture
- Created `presentation-templates` repo (github.com/jbearup1981/presentation-templates) — GitHub Pages enabled
- Renamed `harloff-deck` repo to `client-presentations` for finished client decks
- Pushed all templates, assets, and docs to presentation-templates repo
- Scraped team data from nexusbenefitsolutions.com JS bundles → created `team.md` with 7 members
- Initial architecture: agent fetches full templates from repo on demand
- Testing revealed: Claude.ai can't fetch from GitHub domains (restricted) + full 150KB templates cause rapid context compaction

### Mar 2, 2026 — Modular Slide Component System
- Pivoted from monolithic templates to modular "Lego piece" components
- Analyzed all 3 templates: found ~60-70% shared content, 10 slides 100% identical across templates
- Extracted shared CSS into `components/base/base.css` (all variables, fonts, utilities, print, responsive)
- Extracted shared JS into `components/base/base.js` (navigation, scaling, fullscreen, responsive mode)
- Broke templates into 32 individual slide components in `components/slides/`
  - 7 Nexus Green (opening/closing)
  - 9 Benchmarking & Discovery
  - 12 Amaze Health (blue)
  - 4 Blank Templates (green, blue, dark green, transition gradient)
- Built visual catalog page (`components/catalog.html`) — all slides as labeled thumbnails, grouped by section
- Wrote 3 recipe files in `recipes/` matching original template slide orders
- Rewrote `INSTRUCTIONS.md` for component-based assembly workflow
- Pushed to GitHub, catalog verified live on GitHub Pages

### Mar 2, 2026 — Catalog Lightbox + Advanced Medical Renewal Components
- Added click-to-zoom lightbox to catalog.html — click any thumbnail to see full-size slide, ESC/click-outside to close
- Created 4 new advanced medical renewal components:
  - `claims-analysis` — 3-year claims trending, large claimants, loss ratio with CSS bar chart
  - `stop-loss-renewal` — Specific/aggregate stop-loss, lasers, rate history table
  - `funding-comparison` — 3-column fully insured vs. level-funded vs. self-funded comparison
  - `network-analysis` — Provider network disruption modeling with check/X indicators
- Reorganized catalog into 7 sections (was 4): Nexus Green, Benchmarking & Discovery, Medical Renewal Simple, Medical Renewal Advanced, Transitions & General, Amaze Health, Blank Templates
- Created `recipes/midmarket-renewal.md` — 23-slide recipe for self-funded/level-funded renewals
- Updated INSTRUCTIONS.md: new components in listing, data gathering guidance, midmarket recipe, catalog link more prominent
- Total components: 36 (was 32), Total recipes: 4 (was 3)

## Open Items
- [ ] **Test in Claude Projects** — paste INSTRUCTIONS.md, verify agent can fetch components and assemble a deck
- [ ] Phone numbers still placeholders on component closing slides
- [ ] Client Momentum slide has placeholder logos/names
- [ ] No responsive web page templates built yet (build on demand)
- [ ] Consider adding `amaze-how-it-works` and `amaze-patient-stories` to prospect recipe (currently only in amaze-standalone)
