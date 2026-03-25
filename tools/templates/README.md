# YAML Templates for Slide Generation

These templates define the data schema for generating comparison slides.
Copy a template, fill in client data, run the tool.

## Medical Plan Comparison
```bash
cp templates/medical-comparison.yaml /path/to/client/plans.yaml
# Edit plans.yaml with client data
python3 assemble_deck.py --plan-comparison plans.yaml -o slides.html
```
- 4+ cards auto-split into 2 slides (Current+Renewal / Alternatives)
- Tag presets: `current`, `renewal`, `recommended`, `alternative`, `budget`
- Benefit highlights: `{value: "$30", highlight: "better"}` or `"worse"`
- Benefits auto-group with dividers before PCP and Rx rows

## Dental & Vision
```bash
cp templates/dental-vision.yaml /path/to/client/dv.yaml
# Edit dv.yaml with client data
python3 assemble_deck.py --dental-vision dv.yaml -o slide.html
```
- Two benefit summary cards (dental + vision) with SVG icons
- Rate comparison table with current vs renewal columns
- Combined total summary bar at bottom

## Available Carrier Logos
Run `python3 assemble_deck.py --list-assets` for full list. Common ones:
- `uhc-logo.png`, `bcbs-michigan-logo.png`, `beam-logo.png`
- `optimyl-logo.png`, `trustmark-logo.png`, `sana-logo.png`
- `priorityhealth-logo-green.svg`
