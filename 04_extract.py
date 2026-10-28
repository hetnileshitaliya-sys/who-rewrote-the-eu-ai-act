"""Step 4: build one text file per sampled submission, combining the
text typed into the portal with the text of the attached PDF.

Output: texts/<submission id>.txt
Flags any submission with very little text (often a scanned PDF)
so it can be read by hand.
"""
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

Path("texts").mkdir(exist_ok=True)
sample = pd.read_csv("data/sample.csv")

flagged = []
for _, row in sample.iterrows():
    parts = [
        f"ORGANISATION: {row['organisation']}",
        f"ACTOR TYPE: {row['actor_type']} | COUNTRY: {row['country']} | DATE: {row['date']}",
        "",
        "--- PORTAL TEXT ---",
        str(row["text"]) if pd.notna(row["text"]) else "",
    ]
    pdf = Path("pdfs") / f"{row['id']}.pdf"
    if pdf.exists():
        try:
            reader = PdfReader(pdf)
            pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            pdf_text = f"[PDF could not be read: {e}]"
        parts += ["", "--- ATTACHED PDF ---", pdf_text]

    text = "\n".join(parts)
    (Path("texts") / f"{row['id']}.txt").write_text(text, encoding="utf-8")
    if len(text) < 800:
        flagged.append(f"{row['id']} ({row['organisation']})")

print(f"Wrote {len(sample)} text files to texts/")
if flagged:
    print("Read these by hand (little extractable text):")
    for f in flagged:
        print("  ", f)
