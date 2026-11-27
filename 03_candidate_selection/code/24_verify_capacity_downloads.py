"""Verify newly downloaded capacity PDFs (PMID-named in 01 folder), match to the paywalled list,
pre-screen study type / pure-standard ORAC, and update the remaining download list.
Run: python 03_candidate_selection/code/24_verify_capacity_downloads.py
"""
import csv, re, sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
import pymupdf
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
PDFDIR = ROOT / "download_raw/01_文献下载与全文提取_2026-11-26"
LIST = OUT / "capacity_paywalled_download_list_2026-11-27.csv"
listrows = list(csv.DictReader(LIST.open(encoding="utf-8-sig", newline="")))
by_pmid = {r["pmid"]: r for r in listrows if r["pmid"]}
by_doi = {r["doi"].lower(): r for r in listrows}
EPI = re.compile(r"participant|cohort|EPIC|plasma|dietary|cross-sectional|case-control|patients|subjects|serum", re.I)
MATRIX = re.compile(r"\bpulp|fruit|fern|frond|peptide|hydrolys|extract|PlantCrystal|flour|leaf|leaves|seed|oil|wine|honey|tea|coffee|juice|berry|berries|vegetable|mushroom|algae|seaweed|propolis|molasses|flower|microgreen|sprout|bran|husk|shell|stem|root|bark|formulation|nano|emulsion|liposome|ferment|lentil|zein|tissue|homogenate|clam|fish|rat|mice|mouse", re.I)
ORAC = re.compile(r"ORAC|oxygen radical absorbance", re.I)
PURE = re.compile(r"pure|standard|reference compound|Trolox equivalent.* (ascorbic|gallic|caffeic|ferulic|coumaric|chlorogenic|catechin|quercetin|curcumin|naringenin|hesperidin)", re.I)
ver = []; downloaded_dois = set(); downloaded_pmids = set()
for p in sorted(PDFDIR.glob("*.pdf")):
    if not p.stem.isdigit():
        continue
    pmid = p.stem
    try:
        doc = pymupdf.open(str(p)); txt = re.sub(r"\s+", " ", "\n".join(pg.get_text() for pg in doc))
    except Exception:
        continue
    dm = re.search(r"10\.\d{4,9}/[^\s\"<>]+", txt)
    doi = (dm.group(0).rstrip(".;,") if dm else "").lower()
    matched = by_pmid.get(pmid) or by_doi.get(doi)
    if not matched:
        continue
    downloaded_dois.add(matched["doi"].lower()); downloaded_pmids.add(pmid)
    if EPI.search(txt): st = "EPIDEMIOLOGY_HUMAN"
    elif MATRIX.search(txt): st = "MATRIX_FOOD"
    elif PURE.search(txt): st = "PURE_STANDARD"
    else: st = "CHECK"
    ver.append(dict(pmid=pmid, doi=matched["doi"], candidate_ids=matched["candidate_ids"], title=matched["title"],
                    study_type=st, orac_present="YES" if ORAC.search(txt) else "NO",
                    admissible_hint="YES" if st == "PURE_STANDARD" and ORAC.search(txt) else "NO"))
with (OUT / "capacity_downloads_verified_2026-11-27.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(ver[0]), lineterminator="\n"); w.writeheader(); w.writerows(ver)
remaining = [r for r in listrows if r["doi"].lower() not in downloaded_dois and r["pmid"] not in downloaded_pmids]
REM = OUT / "capacity_remaining_download_list_2026-11-27.csv"
with REM.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(listrows[0]), lineterminator="\n"); w.writeheader(); w.writerows(remaining)
print("downloaded matched:", len(ver), "| study_type:", dict(Counter(v["study_type"] for v in ver)),
      "| admissible_hint:", dict(Counter(v["admissible_hint"] for v in ver)))
print("remaining to download:", len(remaining))
