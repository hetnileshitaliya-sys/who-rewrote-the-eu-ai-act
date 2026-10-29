# Who rewrote the EU AI Act?

A legislative tracker of public feedback to the EU's **Digital Omnibus on AI** (proposal COM(2025)836, procedure 2025/0359(COD), adopted as Regulation (EU) 2026/1744, in force since 27 July 2026), and of whose demands the final law matched.

**Author:** Het Italiya, BSc International Business Management, University of Bristol. Independent pilot project, built with AI assistance (see below).

## Research question
Whose demands did the final Digital Omnibus on AI match: industry, public-interest groups, public authorities or citizens?

## Data
- **Source:** European Commission, Have Your Say portal, feedback on COM(2025)836 (21 Nov 2025 to 13 Mar 2026). 274 submissions.
- **Census:** every submission, with repeat filings by one organisation reduced to the latest: 270 unique submissions (`09_census.py`). Individual citizens are included as a group, shown only as "Citizen 01", "Citizen 02"..., and their portal ids appear in no published file.
- **Coding:** framework coding on eight issues against fixed categories in [`codebook.md`](codebook.md). Each position is tracked through the Commission proposal, Parliament's report, the Council's general approach and the final law.
- **Reliability:** a blind second coder codes a random 10% (27 submissions, seed 2026, `10_verification_sheet.py`); `08_agreement.py` reports agreement and Cohen's kappa.

## How to reproduce

Requires Python 3.10+.

```
pip install -r requirements.txt
python 01_collect.py             # list of all submissions -> data/submissions.csv (local)
python 09_census.py              # unique submissions -> data/census_public.csv; PDFs and texts -> pdfs/, texts/ (local)
python 06_analyse.py             # score positions against the final law -> data/coded_census.csv, data/positions_long.csv, data/summary.json
python 10_verification_sheet.py  # draw the blind second-coder sample -> data/verification_sheet.csv
python 08_agreement.py           # second-coder agreement, once the verification sheet is filled in
python 07_build_page.py          # tracker page -> docs/index.html
```

`09_census.py --meta-only` writes the submission lists without downloading PDFs. `setup/rebuild.yml` is a GitHub Actions workflow that runs this pipeline on every push (move it to `.github/workflows/` to switch it on). On Windows you can double-click `run_all.bat`.

The earlier 80-submission pilot (`02_sample.py` to `05_coding_sheet.py`) is kept for the record.

## Published data
- `data/codes_ai_first_pass.json`: every code with its supporting quote, unchanged from the AI-assisted first pass.
- `data/outcome_overrides.csv`: outcomes judged by hand, each with a reason.
- `data/coded_census.csv`: one row per submission. `data/positions_long.csv`: one row per position taken.

## Limitations
- Submissions are positions in a policy debate, not evidence of what organisations do in practice.
- Matching a demand to the final law shows correspondence, not influence.
- Lobbying through other channels (meetings, Parliament, Council) is not captured.
- The Council's position on moving machinery out of Annex I Section A comes from reporting on the negotiations.

## How this was built
This is an AI-assisted pilot. Claude (Anthropic) wrote the scripts and produced the first-pass coding: issue passages were located by keyword search, each was coded with a supporting quote, and every blank cell was re-checked with a broader search. I directed the project, ran the pipeline, and am checking the coding through the blind second-coder sample. The first pass is kept unchanged so any correction is visible.

## Data reuse
Submissions are published by the European Commission. This repository publishes metadata and coding, not full submission texts.

## Status (29 October 2026)
- 270 unique submissions coded on eight issues; 154 take at least one position (468 positions).
- **Verification in progress:** 27 submissions drawn for blind second coding (`data/verification_sheet.csv`).

## Draft findings (subject to verification)
- Share of positions matched by the final law (partly won counts as half): industry 57% (337 positions), public-interest and independent groups 42% (96), public authorities 46% (14), citizens 71% (7, indicative only).
- The 80-submission pilot gave 57% and 43%, so the sample estimate held under the full census.
- The final law went further than the Commission proposed on the two issues industry pushed (fixed high-risk delay dates; machinery moved to Annex I Section B), and pulled back on four issues public-interest groups contested (AI literacy, bias-detection data, registration of exempted systems, transparency grace period).
- Manufacturers and their associations (our classification, 25 submitters) were matched on 54% of their positions.
