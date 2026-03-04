# Presentation Deck Builder — Project Documentation

## Vision
A complete presentation system for Nexus Benefit Solutions advisors. Advisors build customized slide decks for prospect and client meetings by picking slides from a component library, and an AI agent assembles and customizes them.

**Current:** Claude Projects on claude.ai Team — advisors interact conversationally, agent builds decks as artifacts with embedded images. Shipped to team Mar 3, 2026.

**Near-term:** Expand component library (compliance, voluntary benefits, ICHRA, level-funded). Add viewer analytics to hosted decks. Extend to benefit guides and compliance documents.

**Long-term:** Custom web app launched from the CRM. Advisor clicks "Create Deck" on a client record → slide catalog with click-to-select UI → LLM handles customization behind the scenes → deck auto-saves to OneDrive and links to CRM record. No Claude subscription needed for advisors. Swap LLMs at will. No context window constraints (database stores components, LLM only sees surgical requests).

## Architecture

### Claude Projects (Current — Shipped Mar 3)

Three files uploaded to a Claude Team project:

| File | Size | Tokens (~) | Purpose |
|------|------|-----------|---------|
| `INSTRUCTIONS.md` | ~21KB | ~5K | System prompt — how to build decks, recipes, guidelines |
| `nexus-components-master.html` | ~232KB | ~60K | All 36 slide components + base CSS + base JS + team directory |
| `nexus-assets-base64.html` | ~123KB | ~31K | 16 shared images compressed and base64-encoded |
| **Total** | **~376KB** | **~96K** | **48% of 200K Team context window** |

**Connectors enabled:** M365 (auto-save to OneDrive)
**Tools enabled:** Web search (finding client logos/info)

### How Decks Get Built (Claude Projects)
1. Advisor starts a conversation, describes the meeting
2. Agent recommends a recipe or advisor picks slides from the catalog
3. Agent reads component HTML from `nexus-components-master.html`
4. Agent embeds images from `nexus-assets-base64.html` as data URIs
5. Agent outputs complete HTML deck as an artifact — renders in the viewer
6. Advisor flips through slides, requests changes conversationally
7. Agent auto-saves to `Deck_Build_History/` on shared OneDrive via M365

### Key Artifact Viewer Constraints (Discovered Mar 3)
- **No inline onclick handlers** — artifact sandbox blocks them. Use `addEventListener` in JS instead. Fixed in `base.js`.
- **No external image loading** — artifact sandbox blocks external URLs. All shared images must be base64 data URIs embedded in the HTML.
- **Output size limit ~150KB** — artifacts truncate beyond this. Component-built decks (~80-100KB) fit. Legacy monolithic decks (180KB+) don't.
- **Cloudflare script injection** — files downloaded from GitHub Pages include a Cloudflare email-decode script that breaks in the sandbox. Strip it if importing legacy decks.

### GitHub Repositories

| Repo | Pages URL | Purpose |
|------|-----------|---------|
| `presentation-templates` | jbearup1981.github.io/presentation-templates/ | Source components, assets, catalog, design system |
| `client-presentations` | jbearup1981.github.io/client-presentations/ | Finished client decks with shareable links |

### Design System
- **Dimensions:** 960x540px slides, CSS-scaled
- **Fonts:** DM Serif Display (headings) + DM Sans (body) — Google Fonts
- **Colors:** Nexus green/earth palette (7 vars) + Amaze blue/teal palette (4 vars) + 13 RGBA white opacity vars
- **Color flow:** Green intro → Blue Amaze section → Green closing
- **CSS:** 14 utility classes, EDITABLE/FIXED comment markers throughout
- **Navigation:** addEventListener-based (artifact-safe), arrow keys, touch swipe, fullscreen

## Components (36 total, 4 recipes)

### Slide Library

**Nexus Green (Opening & Closing) — 7:**
`nexus-title` · `nexus-agenda` · `nexus-team` · `nexus-intro` · `nexus-approach` · `nexus-capabilities` · `nexus-closing`

**Benchmarking & Discovery — 4:**
`discovery-recap` · `benchmarking-simple` · `section-transition` · `client-portal`

**Medical Renewal — Simple — 5:**
`benchmarking-renewal` · `plan-comparison` · `pos-strategy` · `dental-vision` · `supplemental`

**Medical Renewal — Advanced (Self-Funded / Level-Funded) — 4:**
`claims-analysis` · `stop-loss-renewal` · `funding-comparison` · `network-analysis`

**Amaze Health (Blue) — 12:**
`amaze-problem` · `amaze-solutions` · `amaze-how-it-works` · `amaze-patient-stories` · `amaze-biomed` · `amaze-insurance` · `amaze-paycheck` · `amaze-everybody-wins` · `amaze-faq` · `amaze-market-comparison` · `amaze-client-momentum` · `amaze-implementation`

**Blank Templates — 4:**
`blank-green` · `blank-blue` · `blank-dark-green` · `blank-transition`

### Recipes

| Recipe | Slides | Use Case |
|--------|--------|----------|
| Small Group Renewal | 24 | Existing client, fully insured, upcoming renewal |
| Mid-Market Renewal | 23 | Self-funded/level-funded, 50-500 lives |
| Small Group Prospect | 19 | New prospect, first/second meeting |
| Amaze Standalone | 17 | Program-only pitch, Amaze reps |

### Amaze Section Tiering
- **Quick Intro (5 slides):** problem → solutions → biomed → paycheck → everybody-wins
- **Standard Pitch (9 slides):** + how-it-works → insurance → faq → implementation
- **Full Deep Dive (12 slides):** + patient-stories → market-comparison → client-momentum

### Image Asset Library (16 images, 123KB base64)
Team photos (3), Nexus logo, Amaze logo, doctor-telehealth, carrier logos (2), competitor logos (8). All compressed to appropriate display sizes (100-250px). SVGs kept as vectors.

## Smart Agent Guidelines (in INSTRUCTIONS.md)
1. **Large files** — extract data points, don't keep raw PDFs in context
2. **Incomplete data** — build skeleton with placeholders, fill when data arrives
3. **Revisions** — output only the changed slide, not the whole deck
4. **Deck reuse** — recognize pasted HTML as a template, swap data
5. **Logos** — use URL directly, don't stall if no logo available
6. **Don't over-ask** — use what the advisor already told you
7. **Slide count gut check** — flag if over 28-30 slides
8. **Amaze tiering** — recommend Quick/Standard/Full based on meeting type

## Auto-Save & Build Tracking
- Every deck includes an HTML comment build log (client, advisor, date, recipe, new assets, custom slides)
- Agent auto-saves to `Deck_Build_History/` on shared OneDrive via M365 connector
- Graceful fallback if M365 not connected — embedded log is the backup
- Jason reviews periodically, best custom slides/assets get added to the component library

## Future Vision

### Custom Web App (Deck Builder v2)
- Launch from "Create Deck" button on CRM client record
- Pre-loads client data (company, size, industry, carrier, renewal date, advisor)
- Click-to-select slide catalog (not drag-and-drop — click adds slide to next position)
- LLM behind the scenes for customization — only sees the specific slide being edited, not the whole library
- No context window constraints — components in database, not in LLM context
- Auto-save to OneDrive, link back to CRM record
- Multi-LLM — swap Claude/OpenAI/local models as needed
- No per-seat AI subscription for advisors — API costs only
- Extends to benefit guides, compliance documents, any templated deliverable

### Viewer Analytics
- Track who opened the deck, when, how many times, time per slide
- Embed lightweight analytics script in hosted decks (Plausible/Umami for v1)
- Long-term: tie back to CRM prospect record, notify advisor on opens
- No commercial tool does CRM-integrated presentation analytics — this is a market gap

### Assets MCP (Future)
- MCP server that serves images on demand: `get_asset("jason-bearup.jpg")` → returns base64 data URI
- Keeps Claude project ultra-light — just INSTRUCTIONS.md
- Component MCP could serve slide HTML on demand too
- Build when library exceeds ~60 components or asset library grows significantly

### Multi-Project Strategy (Optional)
Could split into specialized projects if the all-in-one gets too heavy:
- Small Group project (renewal + prospect components)
- Mid-Market project (claims, stop-loss, funding, network components)
- Amaze Standalone project (Amaze-only components)
- Each project lighter, more focused context. Trade-off: less flexibility to mix across types.

## Component Roadmap

Educational slides (introduce concepts) vs. Data slides (client-specific numbers). Both plug-and-play.

### Priority (Build Next)
1. Level-funded explainer (3 slides) — advisors pitching this frequently
2. ICHRA explainer (2-3 slides) — growing market
3. Voluntary benefits overview (2 slides) — common upsell
4. Mid-level benchmarking (2-3 slides) — fills gap between simple and in-depth
5. Disability + FMLA pairing (2 slides) — high-value for larger groups

### Full Roadmap
- **Benchmarking:** Simple (BUILT), Mid-level, In-depth
- **Funding:** Fully insured (BUILT), Self-funded (BUILT), Level-funded, ICHRA
- **Voluntary:** Dental/vision (BUILT), Supplemental (BUILT), Voluntary overview, Disability, Life/AD&D
- **Ben Admin:** Client portal (BUILT), Ben admin platform, Mobile benefit guides
- **Amaze:** Core pitch (BUILT), Extended implementation, Employee-facing pitch
- **Compliance:** Small group, Mid-market, General (COBRA/FMLA/HIPAA/125)

### How to Add New Components
1. Create HTML file in `components/slides/` following existing conventions
2. Add thumbnail to `components/catalog.html` in the appropriate section
3. Add to relevant recipes in `recipes/`
4. Update component listing in `INSTRUCTIONS.md`
5. Add compressed image to `nexus-assets-base64.html` if new assets needed
6. Update `nexus-components-master.html` with the new component
7. Commit, push — GitHub Pages updates automatically

## Market Research (Mar 3, 2026)

### Competitive Landscape
- **Gamma** — market leader (70M users, $2.1B valuation). AI-native, web cards. PPTX export has formatting issues. Generate API available.
- **Beautiful.ai** — best layout automation. "Smart slides" reformat as you add content.
- **Prezent** — enterprise ($$$). 35K+ brand-compliant slides, AI assistant "Astrid."
- **Microsoft Copilot for PowerPoint** — generates from prompts, fabricates statistics. Functional but not beautiful.
- **Canva AI** — Magic Design, Docs to Decks. Swiss army knife but "Canva-ish" output.

### Key Insights
- "Presentation as code" (version-controlled, component-based, assembled by AI) is an emerging pattern — we're ahead of the curve
- HTML is the right primary format for AI-generated, brand-controlled presentations
- No AI tool has deep native CRM integration — manual data export is universal. CRM→deck pipeline is a real differentiator.
- Viewer analytics (who opened, time per slide) is becoming table stakes for sales presentations
- MCP servers exist for PPTX generation (SlideSpeak, 2slides) — could add PPTX export if clients demand it

### Relevant Tools to Watch
- `frontend-slides` — Claude Code skill for HTML presentations (github.com/zarazhangrui/frontend-slides)
- SlideSpeak MCP — generates PPTX from Claude conversations
- 2slides MCP — PPTX via pre-built themes, agent skills architecture

## Session History

### Mar 1, 2026 — Template Optimization & System Buildout
- Built all 3 templates, genericized, created INSTRUCTIONS.md
- CSS optimization: 13 RGBA variables, 14 utility classes, ~190 inline replacements
- Print CSS, responsive scroll mode, template watermarks

### Mar 1, 2026 — Prospect Folder Consolidation
- Harloff and Northern Jet prospect folders consolidated
- iCloud backup set up

### Mar 2, 2026 — Modular Component System
- Pivoted from monolithic templates to 32 modular components
- Extracted base CSS/JS, built visual catalog, wrote 3 recipes
- Created presentation-templates repo on GitHub Pages

### Mar 2, 2026 — Lightbox + Advanced Components
- Catalog lightbox (click-to-zoom thumbnails)
- 4 new advanced medical renewal components (claims, stop-loss, funding, network)
- Catalog reorganized into 7 sections, midmarket-renewal recipe added
- Component roadmap documented (educational vs. data slides)

### Mar 3, 2026 — Claude Projects Shipping & Architecture
- Built `nexus-components-master.html` (232KB) — all 36 components + CSS + JS + team in one knowledge file
- Built `nexus-assets-base64.html` (123KB) — 16 shared images compressed and base64-encoded for artifact viewer
- Rewrote INSTRUCTIONS.md: removed Git-fetching, recipes embedded inline, base64 asset workflow
- Added Smart Agent Guidelines (8 items) including Amaze section tiering (Quick 5/Standard 9/Full 12)
- Added auto-save workflow: deck build log in HTML comments + M365 auto-save to OneDrive Deck_Build_History
- Fixed base.js for artifact sandbox: replaced inline onclick with addEventListener, pushed to GitHub
- Discovered artifact viewer constraints: no external images, ~150KB output limit, Cloudflare script injection
- Tested and shipped to Claude Team — Amaze Biomed standalone deck built perfectly with all assets rendering
- Northern Jet legacy deck analyzed — 908KB (872KB base64 image blob), extracted aircraft image, created clean version with GitHub Pages URLs. Legacy decks too big for artifacts; view at GitHub Pages link, edit through chat.
- Comprehensive market research: AI presentation landscape, enterprise tools, modular design best practices, MCP servers
- Long-term vision documented: custom web app launched from CRM, click-to-select UI, viewer analytics, no context window constraints

## Open Items
- [x] ~~Test in Claude Projects~~ — SHIPPED Mar 3, Amaze deck built perfectly
- [ ] Phone numbers still placeholders on component closing slides
- [ ] Client Momentum slide has placeholder logos/names
- [ ] No responsive web page templates built yet (build on demand)
- [ ] Consider adding `amaze-how-it-works` and `amaze-patient-stories` to prospect recipe
- [ ] Add viewer analytics to GitHub Pages-hosted decks (Plausible/Umami)
- [ ] Test Northern Jet deck editing workflow (GitHub Pages link + chat)
- [ ] Record Loom walkthrough for advisor onboarding
- [ ] Add Brenda/Cameron/Tom/Sophie photos to asset library when available
- [ ] Build first priority components (level-funded explainer, ICHRA explainer)
