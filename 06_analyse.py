"""Step 6: turn the coded positions into results (full census).

Reads data/codes_ai_first_pass.json (one entry per submission:
issue -> [position, quote, note]), data/census_public.csv (metadata, from 09_census.py)
data/outcome_overrides.csv (hand-judged outcomes, each with a reason) and
data/adjudication.csv (the author's final ruling wherever the first pass and the
second coder disagreed; the first pass itself is never edited).
Scores every position against the final law (see codebook.md) and writes:
  data/coded_census.csv    one row per submission
  data/positions_long.csv  one row per position taken
  data/summary.json        totals used by the page

Individual citizens are never named: 09_census.py replaces them with "Citizen 01",
"Citizen 02"... and their portal ids appear in no published file.
"""
import collections
import csv
import json

ISSUES = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]
NAMES = {
    "I1": "High-risk delay", "I2": "Machinery and sectoral law", "I3": "AI literacy",
    "I4": "Small mid-cap relief", "I5": "AI Office powers", "I6": "Bias-detection data",
    "I7": "Registration of exempted systems", "I8": "Transparency grace period",
}
# How the final law compares with the Commission proposal (codebook.md, checked on EUR-Lex)
DIRECTION = {"I1": "further", "I2": "further", "I3": "pulled back", "I4": "same",
             "I5": "same", "I6": "pulled back", "I7": "pulled back", "I8": "pulled back"}
GROUP = {
    "BUSINESS_ASSOCIATION": "Industry", "COMPANY": "Industry", "PUBLIC_AUTHORITY": "Public authorities",
    "NGO": "Public-interest and independent", "TRADE_UNION": "Public-interest and independent",
    "CONSUMER_ORGANISATION": "Public-interest and independent",
    "ACADEMIC_RESEARCH_INSTITTUTION": "Public-interest and independent", "OTHER": "Other",
    "EU_CITIZEN": "Individual citizens", "NON_EU_CITIZEN": "Individual citizens",
}
# Self-registered types that did not match what the organisation is
REGROUP = {
    "33375287": ("Industry", "Retail trade association self-registered as consumer organisation"),
    "33380217": ("Industry", "Association of large-company CIOs self-registered as consumer organisation"),
    "33380831": ("Industry", "Automotive suppliers' association (CLEPA) self-registered as NGO"),
    "33377635": ("Industry", "Federation of Finnish Enterprises self-registered as NGO"),
    "33379395": ("Industry", "Commercial certification body (BSI Group) registered as 'other'"),
    "33380700": ("Industry", "Chamber of commerce and industry registered as 'other'"),
    "33379321": ("Public-interest and independent", "National human rights institute registered as 'other'"),
    "33369439": ("Public-interest and independent", "Statutory workers' chamber registered as 'other'"),
    "33379354": ("Public authorities", "Association of municipalities registered as NGO"),
    "33380658": ("Public authorities", "Statutory social insurance bodies registered as NGO"),
}
# Our classification: firms and associations whose members make physical products under EU product law
MANUFACTURING = {
    "33364509", "33365978", "33378261", "33380773", "33379364", "33370323", "33380724", "33379697",
    "33373874", "33379286", "33380266", "33380831", "33380655", "33380844", "33363104", "33380645",
    "33380813", "33378980", "33380081", "33380293", "33380458", "33379788", "33362963", "33372698",
    "33380441",
}
GROUPS = ["Industry", "Public-interest and independent", "Public authorities", "Individual citizens", "Other"]
SCORE = {"Won": 1, "Partly won": 0.5, "Lost": 0}


def outcome(issue, pos):
    d = DIRECTION[issue]
    if pos == "S":
        return "Won" if d in ("same", "further") else "Partly won"
    if pos == "F":
        return "Won" if d == "further" else "Lost"
    return "Partly won" if d == "pulled back" else "Lost"  # "O"


codes = json.load(open("data/codes_ai_first_pass.json", encoding="utf-8"))
for a in csv.DictReader(open("data/adjudication.csv", encoding="utf-8")):
    old = codes[a["id"]].get(a["issue"], ["N", "", ""])
    if a["final"] != old[0]:
        quote = a["quote"] or (old[1] if a["final"] != "N" else "")
        codes[a["id"]][a["issue"]] = [a["final"], quote, f"Adjudicated by the author: {a['reason']}"]
meta = {r["id"]: r for r in csv.DictReader(open("data/census_public.csv", encoding="utf-8"))}
override = {(r["id"], r["issue"]): (r["outcome"], r["note"])
            for r in csv.DictReader(open("data/outcome_overrides.csv", encoding="utf-8"))}
missing = set(meta) - set(codes)
assert not missing, f"Uncoded submissions: {sorted(missing)[:10]}"

rows, long = [], []
for i in sorted(meta, key=lambda x: (x.startswith("Citizen "), meta[x]["organisation"].lower())):
    s = meta[i]
    grp, gnote = REGROUP.get(i, (GROUP[s["actor_type"]], ""))
    public_id, name = i, s["organisation"]
    r = {"id": public_id, "organisation": name, "actor_type": s["actor_type"], "group": grp,
         "group_note": gnote, "manufacturing": "yes" if i in MANUFACTURING else "",
         "country": s["country"], "date": s["date"]}
    for k in ISSUES:
        pos, quote, note = codes[i].get(k, ["N", "", ""])
        oc, onote = "", ""
        if pos != "N":
            oc, onote = override.get((i, k), (outcome(k, pos), ""))
            long.append({"id": public_id, "organisation": name, "group": grp, "group_note": gnote,
                         "manufacturing": r["manufacturing"], "issue": k, "issue_name": NAMES[k],
                         "position": pos, "quote": quote, "note": note,
                         "final_law_direction": DIRECTION[k], "outcome": oc, "outcome_note": onote})
        r.update({k: pos, f"{k}_quote": quote, f"{k}_note": note, f"{k}_outcome": oc})
    rows.append(r)

for path, data in (("data/coded_census.csv", rows), ("data/positions_long.csv", long)):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)


def share(items):
    scored = [SCORE[x["outcome"]] for x in items if x["outcome"] in SCORE]
    return (round(sum(scored) / len(scored) * 100) if scored else None), len(scored)


attainment = {}
for g in GROUPS:
    mine = [x for x in long if x["group"] == g]
    pct, n = share(mine)
    attainment[g] = {"submissions": sum(1 for r in rows if r["group"] == g),
                     "with_positions": len({x["organisation"] for x in mine}),
                     "positions": n, "share": pct,
                     "outcomes": dict(collections.Counter(x["outcome"] for x in mine))}
pct, n = share([x for x in long if x["manufacturing"]])
manufacturing = {"submissions": len(MANUFACTURING & set(meta)), "positions": n, "share": pct,
                 "with_positions": len({x["organisation"] for x in long if x["manufacturing"]})}
issues = {}
for k in ISSUES:
    mine = [x for x in long if x["issue"] == k]
    issues[k] = {g: dict(collections.Counter(x["position"] for x in mine if x["group"] == g)) for g in GROUPS}
summary = {"names": NAMES, "direction": DIRECTION, "submissions": len(rows),
           "with_positions": len({x["organisation"] for x in long}), "positions": len(long),
           "attainment": attainment, "manufacturing": manufacturing, "issues": issues}
json.dump(summary, open("data/summary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"Submissions: {len(rows)} ({summary['with_positions']} took a position), positions: {len(long)}")
for g, a in attainment.items():
    print(f"  {g}: {a['share']}% matched ({a['positions']} positions, {a['submissions']} submissions)")
print(f"  Manufacturing subset: {pct}% matched ({n} positions)")
