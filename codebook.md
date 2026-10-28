# Codebook: Who rewrote the EU AI Act?

**Research question.** Whose demands made it into the final Digital Omnibus on AI, Regulation (EU) 2026/1744?

**Corpus.** Feedback submitted to the Commission's proposal COM(2025)836 on the Have Your Say portal (21 November 2025 to 13 March 2026): 274 submissions. The coded sample is about 80 organisations, drawn by `02_sample.py` under the rules stated in that script.

**Unit of analysis.** One organisation's submission, combining the portal text and any attached PDF (`texts/<id>.txt`).

## Position codes (one per issue)

| Code | Meaning | Apply when the submission… |
|---|---|---|
| **S** | Supports the proposal | welcomes or accepts the Commission's change on this issue as drafted |
| **O** | Opposes | asks to drop, narrow or reverse the change, or to keep the original AI Act rule |
| **F** | Wants it to go further | asks for more delay, more relief or a wider change than the Commission proposed |
| **N** | Not mentioned | does not address the issue, or mentions it with no position |

Rules:
- Code only what the organisation states. A general call for "simplification" is **N** on every issue unless it names the issue.
- If a submission contains both S and F on the same issue, code **F** (the stronger demand) and note it.
- Every code other than N needs a short quote in the `_quote` column. No quote, no code.
- Ambiguous? Code **N** and explain in `coder_notes`.

## The eight contested issues

Both columns were checked on 28 Oct 2026: the proposal against COM(2025)836 and the final law against Regulation (EU) 2026/1744 (CELEX 32026R1744), both on EUR-Lex. **Direction** compares the final law with the proposal: *same*, *further* (more relief or delay than proposed) or *pulled back* (closer to the original AI Act).

| ID | Issue | What the Commission proposed (COM(2025)836) | What the final law did (2026/1744) | Direction |
|---|---|---|---|---|
| I1 | Delay of high-risk obligations | Rules apply 6 months (Annex III) or 12 months (Annex I) after a Commission decision that standards and support tools exist; long-stop dates 2 Dec 2027 and 2 Aug 2028 | Fixed dates: Annex III from 2 Dec 2027, Annex I from 2 Aug 2028 (Recital 40) | Further: the conditional trigger is replaced by the full long-stop delay |
| I2 | Machinery and sectoral product law | No move of the Machinery Regulation; guidance on its interplay with the AI Act | Machinery Regulation 2023/1230 moved from Annex I Section A to Section B; AI requirements via delegated acts applying by 2 Aug 2028 (Recital 42) | Further: a change the Commission did not propose |
| I3 | AI literacy (Art. 4) | Company duty removed: Commission and Member States "shall encourage" providers and deployers | Providers and deployers must "take measures to support the development of AI literacy"; no guaranteed level (Art. 4(1)) | Pulled back: a softened company duty survives |
| I4 | Relief for small mid-caps | Extend SME privileges to SMCs (documentation, quality management, lower fine caps) | Extended; SMC defined (Recital 6; Art. 3(14a)–(14b); Art. 17(2)) | Same |
| I5 | AI Office powers | Exclusive competence over AI systems built on the provider's own GPAI model (excluding Annex I products) and over VLOP/VLOSE systems | Same scope, plus investigation and fining powers set out in the Regulation (Art. 75(1); Arts 75a–75d) | Same scope; powers spelled out in law rather than left to implementing acts |
| I6 | Special-category data for bias detection | New Art. 4a extending bias-detection processing beyond high-risk systems, with strict conditions | New Art. 4a, "exceptionally" and "to the extent strictly necessary" | Same |
| I7 | Registration of exempted systems | Art. 49(2) deleted: no registration, documentation kept on request | Registration in the EU database kept, with streamlined Annex VIII content; Recital 22: registration "remains crucial for effective market surveillance and public accountability" | Pulled back: registration survives in lighter form |
| I8 | Transparency (Art. 50) timing | Six months for pre-existing generative AI systems: comply by 2 Feb 2027 | Four months: comply by 2 Dec 2026 (Recital 38) | Pulled back: shorter grace period |

## Outcome coding (after position coding)

For each issue, record whether the final law moved **towards the proposal**, **beyond it** (further), or **back from it** (towards the original AI Act). A demand counts as:
- **Won**: the final law matches the organisation's position
- **Partly won**: the final law moved in its direction but less far
- **Lost**: the final law went the other way

Language on the page: "the final law matched these demands", never "these groups caused the change".

## Reliability

A second person independently codes 20% of the sample (16 submissions, chosen at random). Agreement is reported per issue (percentage agreement and Cohen's kappa). Disagreements are discussed and the codebook is updated; changes are dated below.

## Change log
- 2026-10-28: first version. Proposal and final-law columns checked against EUR-Lex texts of COM(2025)836 and Regulation (EU) 2026/1744; Direction column added.
