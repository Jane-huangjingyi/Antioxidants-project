"""Refine the ORAC-ready queue subset by study type (pure standard vs matrix/food vs epidemiology vs method).
Corrects over-inclusive single-compound triage: matrix studies linking one compound are NOT admissible.
Only PURE_STANDARD leads may proceed to six-gate intake. Run: python 03_candidate_selection/code/17_refine_queue_studytype.py
"""
import csv, json, re, sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
rows = [r for r in csv.DictReader((OUT / "queue_oa_extraction_2026-11-27.csv").open(encoding="utf-8-sig", newline="")) if r["ready_for_review"] == "YES"]
EPI = re.compile(r"participant|cohort|EPIC|plasma|dietary|cross-sectional|case-control|patients|subjects|human study", re.I)
MATRIX = re.compile(r"\bpulp|fruit|fern|frond|peptide|hydrolys|extract|PlantCrystal|flour|leaf|leaves|seed|oil|wine|honey|tea|coffee|juice|berry|berries|vegetable|mushroom|algae|seaweed|propolis|molasses|flower|microgreen|sprout|bran|husk|shell|stem|root|bark|formulation|nano|emulsion|liposome", re.I)
METHOD = re.compile(r"development and validation|on-line|biosensor|method development|assay validation", re.I)
PURE = re.compile(r"pure|standard|reference (compound|standard)|authentic", re.I)
out = []
for r in rows:
    txt = (r["title"] or "") + " " + (r["snippets"] or "")
    if EPI.search(txt): st = "EPIDEMIOLOGY_HUMAN"
    elif METHOD.search(txt): st = "METHOD"
    elif MATRIX.search(txt): st = "MATRIX_FOOD"
    elif PURE.search(txt): st = "PURE_STANDARD"
    else: st = "UNCLEAR"
    out.append(dict(doi=r["doi"], candidate_ids=r["candidate_ids"], title=r["title"], study_type=st,
                    admissible_for_intake="YES" if st == "PURE_STANDARD" else "NO",
                    reason="matrix/food linking one compound, not pure standard" if st == "MATRIX_FOOD" else
                           ("human/epidemiology, not compound ORAC" if st == "EPIDEMIOLOGY_HUMAN" else
                            ("method development" if st == "METHOD" else ("pure standard candidate" if st == "PURE_STANDARD" else "needs manual check")))))
with (OUT / "queue_studytype_refined_2026-11-27.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
c = Counter(r["study_type"] for r in out)
summary = dict(ready=len(out), study_type=dict(c), admissible=sum(r["admissible_for_intake"] == "YES" for r in out),
               note="Matrix/food/epidemiology/method studies are NOT admissible for single-compound capacity intake even if they link one compound.")
(OUT / "queue_studytype_refined_2026-11-27_qc.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("ready:", len(out), "| study_type:", dict(c), "| admissible:", summary["admissible"])
