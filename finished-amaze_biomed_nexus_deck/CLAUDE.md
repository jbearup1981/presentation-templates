# Amaze Health Biomed — Standalone Presentation Deck

## Overview
Standalone presentation deck for the Amaze Health / Biomed program. This is a reusable template — not tied to any specific prospect. Used when bringing an Amaze Health rep into a meeting: Nexus opens and frames the opportunity, the middle section dives deep into Amaze Health and Biomed mechanics, and Nexus closes with implementation and next steps.

## Current Deck
- **File:** `amaze-biomed-deck-v1.html` (17 slides, self-contained HTML)
- **Design:** 960x540px fixed-dimension slides, CSS-scaled (0.88 factor)
- **Fonts:** DM Serif Display + DM Sans (Google Fonts)
- **Color flow:** Nexus green/earth tones (slides 1-4) → Amaze blue/teal (slides 5-15) → Nexus green (slides 16-17)
- **Assets:** Shared `../assets/` folder at presentations root

## Team on Deck
- **Jason Bearup** — Lead Advisor
- **Ken Fortier** — Relationship Manager
- **Grace Morris** — Account Manager
- Placeholder phone numbers throughout (need real numbers)

## Slide Structure (17 slides)

### Nexus Intro (Green — slides 1-4)
1. Title — Diagonal layout, Amaze blue color block on right
2. Agenda — Numbered list (01-07), Harloff-style clean layout
3. Your Nexus Team — Jason, Ken, Grace
4. Why We're Here — Opportunity framing with stats

### Amaze Health Deep Dive (Blue — slides 5-10)
5. The Problem — 4 problem cards (Cost, Connection, Confusion, Convenience)
6. What Employees Get — 3x2 feature grid + iPhone mockup + stat badges
7. How Amaze Health Works — 3-step care model + info cards
8. Market Comparison — 16/16 bar chart with competitor logos
9. Patient Stories — 3 real-world scenario cards
10. Introducing Biomed — Section 125, pre-tax, voluntary overlay

### Program Mechanics (Blue — slides 11-15)
11. Insurance Benefits — Plan 1500 vs Plan 1250 table
12. Paycheck Example — $20/hr ($1,600 bi-weekly), Michigan taxes, +$23.92/paycheck
13. Everybody Wins — Employee + Employer benefits, ~$897/yr net per employee
14. Client Momentum — "Expanding Rapidly Across West Michigan" — 8 placeholder client logos + "+ More enrolling monthly"
15. FAQ — 6 Q&A cards in 2x3 grid

### Close (Green — slides 16-17)
16. Implementation Timeline — 6-week rollout plan
17. Closing — Jason/Ken/Grace contacts, Nexus logo

## Paycheck Math ($20/hr, Plan 1500, Michigan)
- Gross: $1,600.00 bi-weekly
- BMPR: $692.31 ($1,500/mo x 12 / 26)
- BMCL: $553.85 ($1,200/mo x 12 / 26)
- Net without Biomed: $1,308.38
- Net with Biomed: $1,332.30
- **Difference: +$23.92/paycheck**
- Employer FICA savings: ~$1,377/yr - $480 PEPM fee = ~$897/yr net per employee

## Design Notes
- All blue slides have unique multi-radial-gradient backgrounds (no two identical)
- Competitor logos on Market Comparison slide: white via `brightness(0) invert(1)` filter
- HealthJoy, Cerebral, Teladoc PNGs had white backgrounds removed via Pillow (originals backed up as *-original.png in assets)
- MDLive and Cerebral logos sized 20% smaller; Firefly 10% smaller
- Present tense throughout (this is a pitch, not a conditional proposal)

## Placeholders Remaining
- Phone numbers for Jason, Ken, Grace on closing slide
- Client logos and names on slide 14 (Client Momentum)

## Source Decks
- Copied slides from NMJS deck (slides 14-24) and Harloff deck (title, team, agenda layouts)
- Only 2 truly new slides: How Amaze Health Works (slide 7), Patient Stories (slide 9)

## Status
- Deck built and design-refined through multiple iterations
- Ready for final data entry (client logos, phone numbers) and field use
