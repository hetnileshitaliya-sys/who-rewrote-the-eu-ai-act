"""Step 2: draw the coding sample.

Rules (stated on the methods page):
1. Individual citizens are excluded; only organisations are coded.
2. Organisations that filed more than once keep their latest submission.
3. Small actor groups (public authorities, trade unions, consumer
   organisations, academic institutions) are included in full.
4. The remaining places, up to a target of 80, are filled by a random
   draw taking the same share from each larger group.
   random_state=42 makes the draw reproducible.

Output: data/sample.csv
"""
import pandas as pd

TARGET = 80
SEED = 42
CITIZENS = ["EU_CITIZEN", "NON_EU_CITIZEN"]
# Spelling below is the Commission's own (including "INSTITTUTION")
SMALL_GROUPS = [
    "PUBLIC_AUTHORITY",
    "TRADE_UNION",
    "CONSUMER_ORGANISATION",
    "ACADEMIC_RESEARCH_INSTITTUTION",
]

df = pd.read_csv("data/submissions.csv")

orgs = df[~df["actor_type"].isin(CITIZENS)].copy()
orgs["org_key"] = orgs["organisation"].str.strip().str.lower()
before = len(orgs)
orgs = orgs.sort_values(["date", "id"]).drop_duplicates("org_key", keep="last")
duplicates_removed = before - len(orgs)

take_all = orgs[orgs["actor_type"].isin(SMALL_GROUPS)]
rest = orgs[~orgs["actor_type"].isin(SMALL_GROUPS)]
share = (TARGET - len(take_all)) / len(rest)
sampled = rest.groupby("actor_type").sample(frac=share, random_state=SEED)

sample = pd.concat([take_all, sampled]).drop(columns="org_key")
sample = sample.sort_values(["actor_type", "organisation"])
sample.to_csv("data/sample.csv", index=False, encoding="utf-8")

print(f"Organisations: {before} submissions, {duplicates_removed} duplicates removed, {len(orgs)} unique")
print(f"Sample: {len(sample)} organisations (target {TARGET}, seed {SEED})")
print(sample["actor_type"].value_counts().to_string())
