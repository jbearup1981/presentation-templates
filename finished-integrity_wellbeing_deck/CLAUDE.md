---
title: "Integrity Well-Being — Standalone Deck"
date: "2026-08-27"
tags: [sales, presentations, integrity-wellbeing, amaze-health, example-deck]
---

# Integrity Well-Being — Standalone Presentation Deck

Reusable pitch deck for **[[integrity-wellbeing-product|Integrity Well-Being, powered by Amaze Health]]** — the voluntary Section 125 program. Not tied to a specific prospect. Works with or without an [[Amaze_Health|Amaze Health]] rep in the room: Nexus frames the problem, the middle runs the Amaze platform deep-dive, then the Integrity mechanics, then Nexus closes on implementation.

Serves as the **Integrity Well-Being Example Deck** in [[Claude Design]].

> **`integrity-wellbeing-deck-v1.html` in this folder is GENERATED. Do not hand-edit it.**
> The editable source is `../integrity-wellbeing-deck/integrity-wellbeing-sales-deck-v2.html`.
> Rebuild with `cd ../integrity-wellbeing-deck && python3 build_finished.py`.
> Hand-editing a copy is exactly how the predecessor deck went stale — see [[#Lineage]].

## Deck Facts

- **17 slides**, 960×540 fixed, CSS-scaled
- **Fonts:** DM Serif Display (display) + DM Sans (body)
- **Color flow:** Nexus Forest (slides 1–4) → Amaze Azure (5–15) → Forest (16–17)
- **Images:** 18, all `../assets/` relative paths
- **Audience:** employers ~25+ employees, predominantly full-time W-2, stable tenure

## Slide Structure

| # | Slide | Palette |
|---|-------|---------|
| 1 | Title — diagonal split, Amaze block right | Forest |
| 2 | What We'll Cover — 8-item agenda | Forest |
| 3 | Your Nexus Team — 3-up cards | Forest |
| 4 | Why We're Here — opportunity framing | Forest |
| 5 | The Challenge — 4 problem cards (Cost, Confusion, Connection, Convenience) | Azure |
| 6 | The Platform — feature grid + phone mockup | Azure |
| 7 | The Care Model — 3-step care flow | Azure |
| 8 | How We Compare — 17/17 services vs 8 competitors | Azure |
| 9 | Real-World Scenarios — 3 patient stories | Azure |
| 10 | The Structure — four-step model + At a Glance | Azure |
| 11 | Plan Tiers — 4-tier indemnity table | Azure |
| 12 | The Paycheck — worked before/after stub | Azure |
| 13 | The Employer Win — FICA math + scaling | Azure |
| 14 | Proof — Davenport CFO testimonial + scale stats | Azure |
| 15 | Common Questions — 6 employer FAQs | Azure |
| 16 | Implementation — 8-week timeline | Forest gradient |
| 17 | Closing — contacts + logo | Forest |

## Customizing For A Client

**Safe to change per client — this is the expected customization:**

| What | Where | Notes |
|---|---|---|
| Client name / logo | Title slide | Pull from `logos/<company-slug>.(png\|svg\|jpg)` |
| Advisor + contacts | Slides 3 and 17 | See [[#Advisor Variants]] — prefer generating over hand-editing |
| Meeting date | Title slide | |
| Agenda emphasis | Slide 2 | Reorder or trim to fit the meeting length |
| Group-size examples | Slide 13 | The 75 / 200 / 500 scaling rows — swap to bracket the client's actual headcount |
| Salary in the paycheck example | Slide 12 | **Recalculate the whole stub if you change this** — see below |

**Do NOT change without a source — every number below is quoted from the website:**

- Plan tier premiums, claim payments, and the full indemnity schedule (slide 11)
- The 7.65% FICA rate, $40/ee/mo admin fee, $114.75 → $74.75 net math (slide 13)
- 17/17 services and all 8 competitor scores (slide 8)
- The 8-week implementation timeline and payroll-monitoring commitment (slide 16)
- Amaze scale claims: 150+ W-2 providers, 80+ languages, <30s response, 1,000+ free meds

Authoritative source: `../integrity-wellbeing-deck/SOURCE-OF-TRUTH-website-2026-08-17.md`, captured from the Integrity Well-Being section of nexusbenefitsolutions.com. **Read it before changing any figure.**

**If you change the salary on slide 12**, every line moves — taxable wages, all four tax lines, and the net. The published example is $55,000 (~$26.44/hr, bi-weekly $2,115.38, MFJ + 2 dependents, 12% federal, ~5.35% state) netting **+$34.62/check · +$900.12/yr**. The site also offers $45K · Plan 1050 and $85K · Plan 1500 as alternates. Don't eyeball a new number — recompute or use one of the published three.

## Advisor Variants

Four team pairings are generated from a roster rather than hand-copied:

| Slug | Team |
|---|---|
| `jason-ken` | [[Jason Bearup]] · [[Ken Fortier]] · [[Grace Morris]] |
| `jason-tom` | [[Jason Bearup]] · [[Tom Snikkers]] · [[Grace Morris]] |
| `ken` | [[Ken Fortier]] · [[Grace Morris]] (2-up layout) |
| `brenda-cam` | [[Brenda Manning]] · [[Cameron Manning]] · [[Grace Morris]] |

```bash
cd ../integrity-wellbeing-deck
python3 make_variants.py              # all four
python3 make_variants.py --only ken   # just one
```

Adding an advisor (e.g. [[Courtney Uhrig]]) is a roster entry plus a variant line in `roster.json` — no deck surgery. Only two slides differ between variants.

**Phone numbers:** we only hold real numbers for Jason and Ken. Everyone else shows email only. Never invent a placeholder — the `(616) 555-000X` fakes in older decks are a known embarrassment.

## Live Links

Presentable GitHub Pages copies, self-contained with embedded images:

- Landing page: https://jbearup1981.github.io/client-presentations/integrity.html
- Individual: `integrity-{jason-ken,jason-tom,ken,brenda-cam}.html` in the same repo

## Known Gaps

- **Plan 900 indemnity schedule is missing.** The site publishes the premium ($900) and claim payment (~$757) but no benefit amounts. The column shows em-dashes and a visible **"schedule TBC"** label so it can't be presented as complete by accident. Get the schedule from the carrier and fill it.
- **Competitor scorecard is dated** — "last verified April 18, 2026" per the site. Re-check before a significant pitch.
- **Two savings bases on slide 13** — $74.75/ee/mo is Plan 1500 specific; the scaling table uses the site's blended ~$850/ee/yr. Both are labeled; unify if it bothers you.
- **Website self-contradictions** (fix at the source, not in the deck): the employer FAQ claims no per-employee admin fee, contradicting the $40 stated twice elsewhere; and three different net-paycheck figures (+$0.00, +$34.62, +$28.93) appear for the same $55K/Plan 1500 scenario.

## Lineage

Descended from `../finished-amaze_biomed_nexus_deck/` (the BioMed program deck). The intermediate `integrity-wellbeing-sales-deck-v1.html` was a **find-and-replace** of that deck — seven text swaps renaming "Biomed" to "Integrity Wellbeing" while every number stayed BioMed's: BMPR/BMCL payroll codes, Plan 1500/1250 tiers, a $20/hr paycheck example, 16/16 services, placeholder client logos. v2 rebuilt all of it from the website.

The lesson is baked into the structure here: one editable source, generated derivatives, and a source-of-truth file to check figures against.

## Related

- [[integrity-wellbeing-product]] — naming history (Nexus Health Plus → Cornerstone → Integrity Well-Being) and product structure
- [[nexus-health-plus]] — the *separate* build-our-own-carrier-paper track (SiriusPoint / [[Howard]] / Insight Benefits). **Do not source deck facts from it.**
- [[sales-deck]] — the recipe and component system
- [[presentations]] — the deck-builder system overview
