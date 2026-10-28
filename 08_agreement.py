"""Step 8: inter-coder agreement.

Compares the human second coder's codes in data/verification_sheet.csv
(columns I1_your_code ... I8_your_code, values S / O / F / N)
with the first-pass codes, and writes data/agreement.csv:
per issue, percentage agreement and Cohen's kappa.
Blank cells are skipped, so the script can be run part-way through.
"""
import collections
import csv
import json

ISSUES = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]
VALID = {"S", "O", "F", "N"}

codes = json.load(open("data/codes_ai_first_pass.json", encoding="utf-8"))
sheet = list(csv.DictReader(open("data/verification_sheet.csv", encoding="utf-8-sig")))


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in VALID) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


out, all_pairs, disagreements = [], [], []
for k in ISSUES:
    pairs = []
    for r in sheet:
        human = (r.get(f"{k}_your_code") or "").strip().upper()
        if not human:
            continue
        if human not in VALID:
            raise SystemExit(f"Row {r['organisation']}, {k}: '{human}' is not one of S, O, F, N")
        first = codes[r["id"]].get(k, ["N"])[0]
        pairs.append((first, human))
        if first != human:
            disagreements.append((r["organisation"], k, first, human))
    all_pairs += pairs
    if pairs:
        kp = kappa(pairs)
        out.append({"issue": k, "coded": len(pairs),
                    "agreement_pct": round(100 * sum(a == b for a, b in pairs) / len(pairs)),
                    "kappa": "" if kp is None else round(kp, 2)})

if not all_pairs:
    raise SystemExit("No codes filled in yet in data/verification_sheet.csv")
kp = kappa(all_pairs)
out.append({"issue": "All", "coded": len(all_pairs),
            "agreement_pct": round(100 * sum(a == b for a, b in all_pairs) / len(all_pairs)),
            "kappa": "" if kp is None else round(kp, 2)})
with open("data/agreement.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)

for row in out:
    print(f"{row['issue']}: {row['agreement_pct']}% agreement, kappa {row['kappa']} ({row['coded']} cells)")
if disagreements:
    print("\nDisagreements to discuss:")
    for org, k, a, b in disagreements:
        print(f"  {org} {k}: first pass {a}, you {b}")
