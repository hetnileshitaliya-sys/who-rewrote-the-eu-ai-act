"""Step 7: build the evidence map page, docs/index.html, from the results.

Fills docs/template.html with data/positions_long.csv and data/summary.json.
If data/agreement.csv exists (from 08_agreement.py), the page reports the
second-coder agreement; otherwise it keeps the "not yet verified" banner.
"""
import csv
import datetime
import json
from pathlib import Path

summary = json.load(open("data/summary.json", encoding="utf-8"))
rows = []
for r in csv.DictReader(open("data/positions_long.csv", encoding="utf-8-sig")):
    rows.append({"organisation": r["organisation"], "group": r["group"], "gnote": r["group_note"],
                 "issue": r["issue"], "position": r["position"], "quote": r["quote"], "note": r["note"],
                 "outcome": r["outcome"], "outcome_note": r["outcome_note"]})
data = {"names": summary["names"], "direction": summary["direction"], "rows": rows}

agreement = Path("data/agreement.csv")
if agreement.exists():
    a = {r["issue"]: r for r in csv.DictReader(open(agreement, encoding="utf-8"))}["All"]
    kappa = f", Cohen's kappa {a['kappa']}" if a["kappa"] else ""
    banner = (f'<div class="banner">Verified: a human second coder independently coded a random 20% '
              f'sample ({a["coded"]} issue codes), agreeing on {a["agreement_pct"]}%{kappa}.</div>')
    verify = (f"<li>First-pass coding was AI-assisted and then checked: a human second coder independently "
              f"coded a random 20% of submissions (16), agreeing on {a['agreement_pct']}% of issue codes{kappa}. "
              f"Per-issue figures are in data/agreement.csv.</li>")
else:
    banner = ('<div class="banner">Draft for review. Coding is not yet verified by a second coder. '
              'Not for circulation.</div>')
    verify = ('<li>First-pass coding was AI-assisted, using keyword-located passages and a second broader '
              'search over every "not mentioned" cell. A human second coder is checking a random 20% '
              '(16 submissions); agreement will be reported here.</li>')

page = Path("docs/template.html").read_text(encoding="utf-8")
page = (page.replace("__BANNER__", banner).replace("__VERIFY__", verify)
            .replace("__DATE__", f"{datetime.date.today().day} {datetime.date.today():%B %Y}")
            .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
Path("docs/index.html").write_text(page, encoding="utf-8")
print(f"Built docs/index.html with {len(rows)} positions ({'verified' if agreement.exists() else 'draft'})")
