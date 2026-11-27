"""Build the paywalled download list for the capacity line (single-compound leads without OA).
Run: python 03_candidate_selection/code/23_build_paywalled_download_list.py
"""
import csv, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
EPI = re.compile(r"participant|cohort|EPIC|plasma|dietary|cross-sectional|case-control|patients|subjects|serum", re.I)
MATRIX = re.compile(r"\bpulp|fruit|fern|frond|peptide|hydrolys|extract|PlantCrystal|flour|leaf|leaves|seed|oil|wine|honey|tea|coffee|juice|berry|berries|vegetable|mushroom|algae|seaweed|propolis|molasses|flower|microgreen|sprout|bran|husk|shell|stem|root|bark|formulation|nano|emulsion|liposome|ferment|lentil|zein", re.I)
METHOD = re.compile(r"development and validation|on-line|biosensor|method development|assay validation", re.I)
def st(t):
    if EPI.search(t): return "EPIDEMIOLOGY_HUMAN"
    if METHOD.search(t): return "METHOD"
    if MATRIX.search(t): return "MATRIX_FOOD"
    return "CHECK_PURE"
rows = [r for r in csv.DictReader((OUT / "queue_oa_extraction_2026-11-27.csv").open(encoding="utf-8-sig", newline="")) if r["oa"] == "NO"]
# dedupe by doi
seen = set(); out = []
for r in rows:
    if r["doi"] in seen: continue
    seen.add(r["doi"])
    out.append(dict(doi=r["doi"], candidate_ids=r["candidate_ids"], title=r["title"], pmid=r["pmid"],
                    study_type_hint=st(r["title"] or ""),
                    doi_url="https://doi.org/" + r["doi"],
                    pubmed_url=("https://pubmed.ncbi.nlm.nih.gov/%s/" % r["pmid"]) if r["pmid"] else ""))
out.sort(key=lambda r: (r["study_type_hint"] != "CHECK_PURE", r["doi"]))
dest = OUT / "capacity_paywalled_download_list_2026-11-27.csv"
with dest.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
print("paywalled unique papers:", len(out), "->", dest.name)
