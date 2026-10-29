"""Step 9 (full census): download and extract EVERY unique submission,
not just the sample. Duplicate filers keep their latest submission.
Individual citizens are included but never named.

Safe to re-run: files already downloaded or extracted are skipped.
Output: pdfs/<id>.pdf and texts/<id>.txt for all unique submissions (kept local),
        data/census.csv listing them (kept local: it holds citizens' portal ids),
        data/census_public.csv, the same list with citizens shown only as
        "Citizen 01", "Citizen 02"... (published; used by 06_analyse.py).
Run with --meta-only to write the two lists without downloading anything.
"""
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from pypdf import PdfReader

DOWNLOAD = "https://ec.europa.eu/info/law/better-regulation/api/download/"
Path("pdfs").mkdir(exist_ok=True)
Path("texts").mkdir(exist_ok=True)

df = pd.read_csv("data/submissions.csv", dtype={"pdf_document_id": str, "id": str})
df["key"] = df["organisation"].fillna("").str.strip().str.lower()
df.loc[df["key"] == "", "key"] = df["id"]  # each citizen counts separately
census = df.sort_values(["date", "id"]).drop_duplicates("key", keep="last").drop(columns="key")
census.drop(columns="text").to_csv("data/census.csv", index=False, encoding="utf-8")
public = census.drop(columns=["text", "pdf_document_id"]).copy()
citizen = public["actor_type"].isin(["EU_CITIZEN", "NON_EU_CITIZEN"])
aliases = {i: f"Citizen {n:02d}" for n, i in enumerate(sorted(public.loc[citizen, "id"]), 1)}
public.loc[citizen, "organisation"] = public.loc[citizen, "id"].map(aliases)
public.loc[citizen, ["id", "country", "transparency_register"]] = [None, None, None]
public.loc[citizen, "id"] = public.loc[citizen, "organisation"]
public.to_csv("data/census_public.csv", index=False, encoding="utf-8")
print(f"Unique submissions: {len(census)} ({int(citizen.sum())} individual citizens, anonymised)")
if "--meta-only" in sys.argv:
    sys.exit(0)

failed = []
for n, row in enumerate(census.itertuples(), 1):
    pdf = Path("pdfs") / f"{row.id}.pdf"
    if isinstance(row.pdf_document_id, str) and not pdf.exists():
        try:
            r = requests.get(DOWNLOAD + row.pdf_document_id, timeout=120)
            r.raise_for_status()
            if not r.content.startswith(b"%PDF"):
                raise ValueError("not a PDF")
            pdf.write_bytes(r.content)
        except Exception as e:
            failed.append((row.id, str(e)))
        time.sleep(1)

    txt = Path("texts") / f"{row.id}.txt"
    if not txt.exists():
        who = row.organisation if isinstance(row.organisation, str) and row.organisation else "(individual citizen)"
        parts = [f"ORGANISATION: {who}",
                 f"ACTOR TYPE: {row.actor_type} | COUNTRY: {row.country} | DATE: {row.date}", "",
                 "--- PORTAL TEXT ---", row.text if isinstance(row.text, str) else ""]
        if pdf.exists():
            try:
                parts += ["", "--- ATTACHED PDF ---",
                          "\n".join(p.extract_text() or "" for p in PdfReader(pdf).pages)]
            except Exception as e:
                parts += ["", f"[PDF could not be read: {e}]"]
        txt.write_text("\n".join(parts), encoding="utf-8")
    if n % 25 == 0:
        print(f"  {n}/{len(census)} done")

print(f"Finished: {len(list(Path('texts').glob('*.txt')))} text files, {len(failed)} downloads failed")
for i, e in failed:
    print("  failed:", i, e)
