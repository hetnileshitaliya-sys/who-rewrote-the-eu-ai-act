"""Step 7: build the legislative tracker page, docs/index.html, from the results.

Fills docs/template.html with data/positions_long.csv, data/coded_census.csv
and data/summary.json. If data/agreement.csv exists (from 08_agreement.py),
the page reports the second-coder agreement; otherwise it keeps the
"not yet verified" banner.
"""
import csv
import datetime
import json
from pathlib import Path

ISSUES = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]
summary = json.load(open("data/summary.json", encoding="utf-8"))
rows = [{"organisation": r["organisation"], "group": r["group"], "manufacturing": r["manufacturing"],
         "issue": r["issue"], "position": r["position"], "quote": r["quote"], "note": r["note"],
         "outcome": r["outcome"], "outcome_note": r["outcome_note"]}
        for r in csv.DictReader(open("data/positions_long.csv", encoding="utf-8-sig"))]
subs = []
for r in csv.DictReader(open("data/coded_census.csv", encoding="utf-8-sig")):
    codes = {k: r[k] for k in ISSUES if r[k] != "N"}
    if codes:
        subs.append({"organisation": r["organisation"], "group": r["group"], "gnote": r["group_note"],
                     "manufacturing": r["manufacturing"], "codes": codes})
data = {"names": summary["names"], "direction": summary["direction"], "summary": summary,
        "rows": rows, "subs": subs}

n_sheet = sum(1 for _ in csv.DictReader(open("data/verification_sheet.csv", encoding="utf-8-sig")))
agreement = Path("data/agreement.csv")
if agreement.exists():
    a = {r["issue"]: r for r in csv.DictReader(open(agreement, encoding="utf-8"))}["All"]
    kappa = f", Cohen's kappa {a['kappa']}" if a["kappa"] else ""
    per = {r["issue"]: r for r in csv.DictReader(open(agreement, encoding="utf-8"))}
    weakest = min((k for k in ISSUES if per.get(k, {}).get("kappa")), key=lambda k: float(per[k]["kappa"]))
    n_adj = sum(1 for r in csv.DictReader(open("data/adjudication.csv", encoding="utf-8")) if r["second_coder"])
    banner = (f'<div class="banner">Checked: the author, as second coder, independently coded a random 10% of '
              f'submissions ({n_sheet}) and agreed with the AI-assisted first pass on {a["agreement_pct"]}% of '
              f'{a["coded"]} issue codes{kappa}. Every disagreement was then ruled on by the author.</div>')
    verify = (f"<li>First-pass coding was AI-assisted. The author independently coded a random 10% of submissions "
              f"({n_sheet}) as second coder: agreement {a['agreement_pct']}%{kappa}. The author then ruled on all "
              f"{n_adj} disagreements (data/adjudication.csv); the first pass is kept unchanged. The least reliable "
              f"issue is {summary['names'][weakest]} (kappa {per[weakest]['kappa']}), so read it with more caution.</li>")
else:
    banner = ('<div class="banner">Draft for review. Coding is not yet verified by a second coder. '
              'Not for circulation.</div>')
    verify = (f"<li>First-pass coding was AI-assisted. A human second coder is independently coding a random "
              f"10% of submissions ({n_sheet}, drawn by script with a fixed seed); agreement will be "
              f"reported here.</li>")

today = datetime.date.today()
page = Path("docs/template.html").read_text(encoding="utf-8")
page = (page.replace("__BANNER__", banner).replace("__VERIFY__", verify)
            .replace("__DATE__", f"{today.day} {today:%B %Y}")
            .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
Path("docs/index.html").write_text(page, encoding="utf-8")
print(f"Built docs/index.html: {len(subs)} submitters, {len(rows)} positions "
      f"({'verified' if agreement.exists() else 'draft'})")
