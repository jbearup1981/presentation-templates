---
title: "Integrity Well-Being — Sales Deck"
date: "2026-08-20"
tags: [sales, presentations, integrity-wellbeing, amaze-health]
---

# Integrity Well-Being — Sales Deck

Standalone, reusable pitch deck for **[[integrity-wellbeing-product|Integrity Well-Being, powered by Amaze Health]]** — the voluntary Section 125 program. Not tied to a specific prospect. Built off the **Amaze Standalone** recipe in the [[sales-deck]] system (17 slides).

## Vision

One deck that carries an employer from "what is this?" to "send us a census." Nexus opens and frames the problem, the middle runs the Amaze platform deep-dive, then the Integrity mechanics (plan tiers → paycheck math → employer win), and Nexus closes on implementation. Works with or without an Amaze rep in the room.

## Current Status

**v2 is current and field-ready**, with one open data gap (Plan 900 indemnity schedule — see Known Issues).

| File | State |
|---|---|
| `integrity-wellbeing-sales-deck-v2.html` | **Current.** Rebuilt 2026-08-20 from the website source of truth. |
| `integrity-wellbeing-sales-deck-v1.html` | Superseded — kept for diff/rollback only. Do not send. |
| `SOURCE-OF-TRUTH-website-2026-08-17.md` | Authoritative program facts scraped from the live site. **Read this before editing the deck.** |

## The v1 Problem (why v2 exists)

v1 (dated Jul 23, 2026) was a **pure find-and-replace** of the older BioMed deck — seven text swaps renaming "Biomed" to "Integrity Wellbeing" and nothing else. Every number in it was BioMed's. Confirmed by diffing the two files. Specifically wrong in v1:

- Payroll codes still **BMPR / BMCL** (BioMed's codes), 8 instances
- Plan tiers **1500 / 1250** with BioMed's indemnity schedule (wrong amounts, wrong benefit names)
- Paycheck example built on **$20/hr, +$23.92/check** — BioMed-era
- Employer math **$1,377 FICA − $480 PEPM = ~$897/yr** — unverified against CEHAS terms
- Comparison slide claimed **16/16 services**; every competitor score was wrong
- Momentum slide had **placeholder client logos** (Permaloc, Steel 21, two churches)
- Team slide had fake phone numbers `(616) 555-000X` and stale titles
- Implementation showed a generic **6-week** rollout

## What v2 Changed

Source of truth: **nexusbenefitsolutions.com/amaze-health** (Integrity Well-Being section), per [[Jason Bearup|Jason]] 2026-08-19.

| Slide | Change |
|---|---|
| 1 — Agenda | Re-sectioned to 8 items to match the new slide numbering |
| 2 — Team | Real titles from the site (Founder/CEO, Founder/CRO, Associate Account Manager); real phones for Jason + Ken; advisor load corrected 25–35 → **30–40** per the public /about page |
| 5 — Platform | "80+ specialties" was not a claim we publish → replaced with the sourced specialty-access language |
| 7 — How We Compare | Rebuilt: **17/17** services (11 medical + 6 non-medical), all 8 competitor scores corrected against the live scorecard, bar widths recomputed on a 17 base |
| 8 — Scenarios | ER-avoided figure aligned to our published **$1,800+** (was $500+) |
| 9 — Structure | Rebuilt as the site's **four-step structure** + "At a Glance" strip |
| 10 — Plan Tiers | Rebuilt as a **4-tier** table with the real indemnity schedule; hospitalization example recalculated to **$2,800** for 3 days on Plan 1500 |
| 11 — Paycheck | Rebuilt on the site's fully-documented worked example: $55K salary, **+$34.62/check, +$900.12/yr**, $18,000+ coverage value |
| 12 — Employer Win | Rebuilt: 7.65% FICA, **$114.75 − $40 = $74.75/ee/mo**, $44,850/yr on 50 ee, plus the 75/200/500 scaling table |
| 13 — Proof | Logo wall → **Anthony Anderson / Davenport University CFO** testimonial (already public on the site, so pre-cleared) + Amaze scale stats |
| 14 — FAQ | Six employer-facing questions rewritten from the site's 18-question FAQ; dropped the stale BMPR/BMCL payroll question, added the monthly-engagement requirement |
| 15 — Implementation | **8-week** timeline + the ongoing automated payroll-monitoring commitment |
| 16 — Closing | Real titles, real phones, brightened contact text |
| Global | "Integrity Wellbeing" → **"Integrity Well-Being"** (site spelling); all BMPR/BMCL removed; images converted to GitHub Pages URLs so the deck survives being emailed |

## Decisions Jason Made (2026-08-20)

The website contradicts itself in three places. Resolved as:

1. **Plan tiers — all four are real and sellable:** Plan 1500 / 1200 / 1050 / 900. (The site shows 1050 in the tier table and 900 in an FAQ; both are live products.)
2. **Employer admin fee is $40/ee/mo** — the site's "no per-employee admin fees" line is wrong. Deck shows the fee inside the math and leads with the net.
3. **Momentum slide uses the Davenport testimonial**, not client logos — avoids naming groups without written permission.

## Known Issues

- **Plan 900 indemnity schedule is missing.** The site publishes premium ($900) and claim payment (~$757) but no benefit amounts. The deck shows the Plan 900 column with em-dashes and a visible **"schedule TBC"** label under the header so it can't be presented as complete by accident. **Fix:** get the schedule from the carrier and fill the column.
- **Two savings bases coexist on slide 12** — $74.75/ee/mo ($897/yr) is Plan 1500 specific; the scaling table uses the site's blended ~$850/ee/yr. Both are labeled, but if Jason wants one basis throughout, the scaling table needs recomputing.
- **Competitor scorecard is dated** — figures "last verified April 18, 2026" per the site. Worth a re-check before a big pitch.
- Slide 15 has a deliberate whitespace gap mid-slide; acceptable but could carry content if wanted.

## Open Items

- Confirm the **hyphenation** standard: the site says "Integrity Well-Being", the [[Augusta Tower]] employee flyer and the memory note say "Integrity Wellbeing". Deck follows the site. Pick one house style.
- Site inconsistency worth fixing on the **website** (not the deck): the employer FAQ claims no per-employee admin fee, contradicting the $40 stated twice elsewhere. Also three different net-paycheck figures (+$0.00 hero, +$34.62 worked example, +$28.93 FAQ) for the same $55K/Plan 1500 scenario.
- Decide whether a **client-logo slide** returns once groups give written permission (Great Lakes Label, Stearns Drilling, [[Augusta Tower]] are on Integrity per the vault).

## Build Notes

Use the deck tool, not hand-editing:

```bash
python3 /Users/jasonsmac/ClaudeCodeTerminal_Projects/1-sales/presentations/tools/assemble_deck.py --list-slides integrity-wellbeing-sales-deck-v2.html
```

- Slide numbers in the tool are **1-based excluding the title slide**; in the DOM the title slide is `.slide[0]`, so tool slide *N* = `.slide[N]`.
- Always run `--to-urls` after `--replace-slide` — replacements can reintroduce relative image paths, which break when the deck is emailed.
- Always finish with `--verify`.
- Design system: 960×540 fixed slides, DM Serif Display + DM Sans, Nexus green (slides 0–3) → Amaze blue (4–14) → green (15–16). Body text on blue should be **≥ rgba(255,255,255,0.82)** — the inherited `--white-70` reads too faint when projected.
- Check for overflow after any edit: no slide should exceed `scrollHeight` 540.

## Related

- [[integrity-wellbeing-product]] — naming history and product structure
- [[nexus-health-plus]] — the *separate* build-our-own-carrier-paper track (SiriusPoint / [[Howard]] / Insight Benefits). **Do not source deck facts from it.**
- [[sales-deck]] — the recipe/component system this deck is built on
- `finished-amaze_biomed_nexus_deck/` — the BioMed ancestor
