"""Step 3: download the PDF attached to each sampled submission.

Safe to re-run: files already downloaded are skipped.
Output: pdfs/<submission id>.pdf
"""
import time
from pathlib import Path

import pandas as pd
import requests

DOWNLOAD = "https://ec.europa.eu/info/law/better-regulation/api/download/"

Path("pdfs").mkdir(exist_ok=True)
sample = pd.read_csv("data/sample.csv", dtype={"pdf_document_id": str})

saved, skipped, failed = 0, 0, []
for _, row in sample.iterrows():
    if pd.isna(row["pdf_document_id"]):
        continue  # no attachment: the text box is the whole submission
    path = Path("pdfs") / f"{row['id']}.pdf"
    if path.exists():
        skipped += 1
        continue
    try:
        r = requests.get(DOWNLOAD + row["pdf_document_id"], timeout=120)
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise ValueError("response is not a PDF")
        path.write_bytes(r.content)
        saved += 1
        print("Saved", path)
    except Exception as e:  # keep going, report at the end
        failed.append((row["id"], str(e)))
    time.sleep(1)  # be polite to the Commission's server

print(f"\nDownloaded {saved}, already had {skipped}, failed {len(failed)}")
for sub_id, err in failed:
    print("  failed:", sub_id, err)
