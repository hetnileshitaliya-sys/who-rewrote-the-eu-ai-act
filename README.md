# Who rewrote the EU AI Act?

An evidence map of public feedback to the EU's **Digital Omnibus on AI** (proposal COM(2025)836, adopted as Regulation (EU) 2026/1744, in force since 27 July 2026), and of whose demands the final law matched.

**Author:** Het Italiya, BSc International Business Management, University of Bristol. Independent project.

## Research question
Whose demands made it into the final Digital Omnibus on AI: industry, civil society or public authorities?

## Data
- **Source:** European Commission, Have Your Say portal, feedback on COM(2025)836 (21 Nov 2025 to 13 Mar 2026). 274 submissions.
- **Sample:** about 80 organisations. Individual citizens are excluded and not named. Small actor groups are included in full; larger groups are randomly sampled (seed 42). See `02_sample.py`.
- **Coding:** framework coding against fixed categories in [`codebook.md`](codebook.md), with a 20% second-coder reliability check.

## How to reproduce

Requires Python 3.10+.

```
pip install -r requirements.txt
python 01_collect.py      # list of all submissions -> data/submissions.csv
python 02_sample.py       # coding sample -> data/sample.csv
python 03_download.py     # attached PDFs -> pdfs/
python 04_extract.py      # one text file per submission -> texts/
python 05_coding_sheet.py # blank coding sheet -> data/coding_sheet.csv
```

On Windows you can double-click `run_all.bat` instead.

## Limitations
- Submissions are positions in a policy debate, not evidence of what organisations do in practice.
- Matching a demand to the final law shows correspondence, not influence.
- Organisations that lobbied through other channels (meetings, Parliament, Council) are not captured.

## How this was built
Code written with AI assistance (Claude). I ran, reviewed and tested every script, and made and checked all coding decisions by hand.

## Data reuse
Submissions are published by the European Commission. Check the Commission's reuse terms before redistributing the raw texts; this repository publishes metadata and coding, not full submission texts.

## Status (28 October 2026)
- 274 submissions collected; 80 organisations sampled and coded on eight issues (`data/coded_sample.csv`, one row per organisation; `data/positions_long.csv`, one row per position).
- First-pass coding was AI-assisted: issue passages were located by keyword search, coded with a supporting quote, and every "not mentioned" cell was re-checked with a broader search. The AI first pass is kept unchanged in `data/codes_ai_first_pass.json`.
- **Verification in progress:** I am independently coding a random 20% (16 organisations, `data/verification_sheet.csv`). Agreement per issue will be reported here before the map is published.
- The evidence map page is `docs/index.html` (publishable with GitHub Pages).

## Draft findings (subject to verification)
- Share of positions matched by the final law (partly won counts as half): industry 61% (75 positions), public-interest and independent groups 40% (68), public authorities 36% (11, indicative only).
- The final law went further than the Commission proposed on the two issues only industry pushed (fixed high-risk delay dates; machinery moved to Annex I Section B), and pulled back on the three issues public-interest groups contested most (AI literacy, registration of exempted systems, transparency grace period).
