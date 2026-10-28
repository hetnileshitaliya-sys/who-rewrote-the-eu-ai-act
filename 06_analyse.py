"""Step 6: turn the coded positions into results.

Reads data/codes_ai_first_pass.json (one entry per sampled organisation:
issue -> [position, quote, note]) and data/submissions.csv (metadata).
Scores every position against the final law (see codebook.md) and writes:
  data/coded_sample.csv    one row per organisation
  data/positions_long.csv  one row per position taken
  data/summary.json        totals used by the page
"""
import collections
import csv
import json
from pathlib import Path

ISSUES = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]
NAMES = {
    "I1": "High-risk delay", "I2": "Machinery and sectoral law", "I3": "AI literacy",
    "I4": "Small mid-cap relief", "I5": "AI Office powers", "I6": "Bias-detection data",
    "I7": "Registration of exempted systems", "I8": "Transparency grace period",
}
# How the final law compares with the Commission proposal (codebook.md, checked on EUR-Lex)
DIRECTION = {"I1": "further", "I2": "further", "I3": "pulled back", "I4": "same",
             "I5": "same", "I6": "same", "I7": "pulled back", "I8": "pulled back"}
# Cases where a demand went beyond, or differed from, what the final law did
OVERRIDE = {
    ("33378261", "I1"): ("Partly won", "Asked for a 24-month delay; got fixed dates"),
    ("33380645", "I1"): ("Partly won", "Asked for two years after readiness; got fixed dates"),
    ("33377527", "I1"): ("Partly won", "Also wanted GPAI obligations delayed"),
    ("33380141", "I1"): ("Partly won", "Also wanted a further fallback delay"),
    ("33375255", "I1"): ("Partly won", "Wanted 2 Aug 2028 for Annex III too"),
    ("33365978", "I2"): ("Partly won", "Wanted Art 6(1)/Annex I(A) deleted; machinery moved to Section B instead"),
    ("33375255", "I2"): ("Partly won", "Wanted all of Section A moved; only machinery moved"),
    ("33379518", "I2"): ("Partly won", "Machinery moved; radio equipment did not"),
    ("33378261", "I2"): ("Partly won", "AI requirements for machinery deferred to delegated acts applying by Aug 2028"),
    ("33380645", "I2"): ("Lost", "Medical devices stayed in Section A"),
    ("33380655", "I2"): ("Unclear", "Asked to narrow Art 6(1) classification; not addressed directly"),
}
GROUP = {
    "BUSINESS_ASSOCIATION": "Industry", "COMPANY": "Industry", "PUBLIC_AUTHORITY": "Public authorities",
    "NGO": "Public-interest and independent", "TRADE_UNION": "Public-interest and independent",
    "CONSUMER_ORGANISATION": "Public-interest and independent",
    "ACADEMIC_RESEARCH_INSTITTUTION": "Public-interest and independent", "OTHER": "Other",
}
# Self-registered types that did not match what the organisation is
REGROUP = {
    "33375287": ("Industry", "Retail trade association self-registered as consumer organisation"),
    "33380217": ("Industry", "Association of large-company CIOs self-registered as consumer organisation"),
    "33380831": ("Industry", "Automotive suppliers' association (CLEPA) self-registered as NGO"),
    "33377635": ("Industry", "Federation of Finnish Enterprises self-registered as NGO"),
    "33379321": ("Public-interest and independent", "National human rights institute registered as 'other'"),
}
GROUPS = ["Industry", "Public-interest and independent", "Public authorities", "Other"]
SCORE = {"Won": 1, "Partly won": 0.5, "Lost": 0}


def outcome(issue, pos):
    d = DIRECTION[issue]
    if pos == "S":
        return "Won" if d in ("same", "further") else "Partly won"
    if pos == "F":
        return "Won" if d == "further" else "Lost"
    return "Partly won" if d == "pulled back" else "Lost"  # "O"


codes = json.load(open("data/codes_ai_first_pass.json", encoding="utf-8"))
subs = {r["id"]: r for r in csv.DictReader(open("data/submissions.csv", encoding="utf-8"))}

# Reproducibility check: does a freshly drawn sample match the coded one?
if Path("data/sample.csv").exists():
    drawn = {r["id"] for r in csv.DictReader(open("data/sample.csv", encoding="utf-8"))}
    status = "matches" if drawn == set(codes) else f"DIFFERS ({len(drawn ^ set(codes))} ids)"
    print(f"Sample check: freshly drawn sample {status} the coded sample")

rows, long = [], []
for i in sorted(codes, key=lambda x: subs[x]["organisation"].lower()):
    s = subs[i]
    grp, gnote = REGROUP.get(i, (GROUP[s["actor_type"]], ""))
    r = {"id": i, "organisation": s["organisation"], "actor_type": s["actor_type"],
         "group": grp, "group_note": gnote, "country": s["country"], "date": s["date"]}
    for k in ISSUES:
        pos, quote, note = codes[i].get(k, ["N", "", ""])
        oc, onote = "", ""
        if pos != "N":
            oc, onote = OVERRIDE.get((i, k), (outcome(k, pos), ""))
            long.append({"id": i, "organisation": s["organisation"], "group": grp, "group_note": gnote,
                         "issue": k, "issue_name": NAMES[k], "position": pos, "quote": quote, "note": note,
                         "final_law_direction": DIRECTION[k], "outcome": oc, "outcome_note": onote})
        r.update({k: pos, f"{k}_quote": quote, f"{k}_note": note, f"{k}_outcome": oc})
    rows.append(r)

for path, data in (("data/coded_sample.csv", rows), ("data/positions_long.csv", long)):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)

attainment = {}
for g in GROUPS:
    scored = [SCORE[x["outcome"]] for x in long if x["group"] == g and x["outcome"] in SCORE]
    attainment[g] = {"positions": len(scored),
                     "share": round(sum(scored) / len(scored) * 100) if scored else None,
                     "outcomes": dict(collections.Counter(x["outcome"] for x in long if x["group"] == g))}
summary = {"names": NAMES, "direction": DIRECTION, "organisations": len(rows),
           "positions": len(long), "attainment": attainment}
json.dump(summary, open("data/summary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"Coded organisations: {len(rows)}, positions taken: {len(long)}")
for g, a in attainment.items():
    print(f"  {g}: {a['share']}% matched ({a['positions']} positions)")
