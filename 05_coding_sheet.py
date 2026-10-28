"""Step 5: create the blank coding sheet, one row per sampled
organisation and one column per contested issue in codebook.md.

Output: data/coding_sheet.csv (open in Excel and fill in)
Will not overwrite an existing sheet, so your coding is never lost.
"""
from pathlib import Path

import pandas as pd

ISSUES = [
    "I1_delay_high_risk",
    "I2_machinery_sectoral",
    "I3_ai_literacy",
    "I4_smc_relief",
    "I5_ai_office_powers",
    "I6_bias_data",
    "I7_registration",
    "I8_transparency_timing",
]

out = Path("data/coding_sheet.csv")
if out.exists():
    print("data/coding_sheet.csv already exists, not overwriting.")
else:
    sample = pd.read_csv("data/sample.csv")
    sheet = sample[["id", "organisation", "actor_type", "country"]].copy()
    for issue in ISSUES:
        sheet[issue] = ""            # S / O / F / N, see codebook.md
        sheet[issue + "_quote"] = ""  # short supporting quote
    sheet["coder_notes"] = ""
    sheet.to_csv(out, index=False, encoding="utf-8-sig")  # utf-8-sig opens cleanly in Excel
    print(f"Created {out} with {len(sheet)} rows")
