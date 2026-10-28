"""Step 1: download the list of all feedback submissions to the
Digital Omnibus on AI proposal, COM(2025)836, from the European
Commission's Have Your Say portal.

Output: data/submissions.csv (one row per submission)
"""
from pathlib import Path

import pandas as pd
import requests

API = "https://ec.europa.eu/info/law/better-regulation/api/allFeedback"
PUBLICATION_ID = 21325  # COM(2025)836, feedback period 21 Nov 2025 to 13 Mar 2026
CITIZENS = {"EU_CITIZEN", "NON_EU_CITIZEN"}

Path("data").mkdir(exist_ok=True)
rows = []
page = 0

while True:
    params = {"publicationId": PUBLICATION_ID, "page": page, "size": 100}
    response = requests.get(API, params=params, timeout=60)
    response.raise_for_status()
    items = response.json().get("content") or []
    if not items:
        break

    for item in items:
        is_citizen = item["userType"] in CITIZENS
        attachments = item.get("attachments") or []
        rows.append({
            "id": item["id"],
            "date": item["dateFeedback"][:10].replace("/", "-"),
            "actor_type": item["userType"],
            "country": item["country"],
            "size": item.get("companySize"),
            # Private individuals are not named in our data
            "organisation": None if is_citizen else (item.get("organization") or "").strip(),
            "transparency_register": item.get("trNumber"),
            "has_pdf": len(attachments) > 0,
            "pdf_document_id": attachments[0]["documentId"] if attachments else None,
            "text": item.get("feedback"),
        })
    page += 1

df = pd.DataFrame(rows)
df.to_csv("data/submissions.csv", index=False, encoding="utf-8")

print(f"Saved {len(df)} submissions to data/submissions.csv")
print(df["actor_type"].value_counts().to_string())
