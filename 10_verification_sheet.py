"""Step 10: draw the blind second-coder sample for the census.

Picks a random 10% of the 270 unique submissions (27), seed 2026, from the
237 organisations. Individual citizens are left out of the draw because
their texts cannot be published alongside the sheet.
Writes data/verification_sheet.csv with empty code columns: the second coder
reads each text in texts/ and fills I1_your_code ... I8_your_code with
S / O / F / N, WITHOUT looking at data/codes_ai_first_pass.json first.
Then run 08_agreement.py.
"""
import csv
import random
from pathlib import Path

SEED, SHARE = 2026, 0.10
ISSUES = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]

census = list(csv.DictReader(open("data/census_public.csv", encoding="utf-8")))
orgs = sorted(r["id"] for r in census if not r["id"].startswith("Citizen "))
n = round(len(census) * SHARE)
picked = set(random.Random(SEED).sample(orgs, n))

out = Path("data/verification_sheet.csv")
if out.exists() and any(v.strip() for r in csv.DictReader(open(out, encoding="utf-8-sig"))
                        for k, v in r.items() if k.endswith("_your_code")):
    raise SystemExit("data/verification_sheet.csv already has codes in it; not overwriting.")

with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id", "organisation", "text_file"] + [f"{k}_your_code" for k in ISSUES] + ["your_notes"])
    for r in sorted((r for r in census if r["id"] in picked), key=lambda r: r["organisation"].lower()):
        w.writerow([r["id"], r["organisation"], f"texts/{r['id']}.txt"] + [""] * (len(ISSUES) + 1))
print(f"Wrote {out} with {n} submissions drawn from {len(orgs)} organisations (seed {SEED})")
