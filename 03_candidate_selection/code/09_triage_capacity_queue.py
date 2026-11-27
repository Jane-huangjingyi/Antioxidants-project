"""Reproducible scope triage of the ORAC full-text review queue (title-based, no network).
Classifies each lead as METHOD_DEVELOPMENT / MIXTURE_EXTRACT_FOOD / SINGLE_COMPOUND_CANDIDATE /
MULTI_COMPOUND_UNCLEAR, flagging the single-compound subset eligible for next extraction+intake.
Run: python 03_candidate_selection/code/09_triage_capacity_queue.py
"""
import csv, json, re, sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "download_raw/07_机构与机器筛选_2026-11-26/stage2_machine_screening/ORAC_Fulltext_Review_Queue.csv"
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
METHOD = re.compile(r"development and validation|on-line|hplc-.*(orac|antioxidant)|esi-hrms|method development|assay (development|validation)|biosensor|electrochemiluminescence", re.I)
MIXTURE = re.compile(r"\bextract|essential oil|\bwine|molasses|\bflower|\bfruit|\bmicrogreen|\bhoney|\btea|\bcoffee|\bjuice|\bpeel|\bseed|\bleaf|\bleaves|\broot|\bbark|\bhydrolysate|polysaccharide|\bprotein|\bberry|\bberries|\bvegetable|\bcereal|\bgrain|\bmushroom|\balgae|\bseaweed|\bpropolis|\bpollen|\bvinegar|\bsauce|\bpaste|\bpowder of|\bfood\b|\bdiet\b|\bmeal\b|\bflour\b|\bran\b|\bhull|\bhusk|\bshell|\bstem|\bshoot|\b sprout", re.I)
rows = list(csv.DictReader(QUEUE.open(encoding="utf-8-sig", newline="")))
out = []
for r in rows:
    t = r["title"] or ""
    n = int(r["names_linked"] or 0)
    if METHOD.search(t): scope = "METHOD_DEVELOPMENT"
    elif MIXTURE.search(t): scope = "MIXTURE_EXTRACT_FOOD"
    elif n == 1: scope = "SINGLE_COMPOUND_CANDIDATE"
    else: scope = "MULTI_COMPOUND_UNCLEAR"
    out.append(dict(article_key=r["article_key"], doi=r["doi"], title=t, candidate_ids=r["candidate_ids"],
                    names_linked=n, scope=scope,
                    eligible_for_extraction="YES" if scope == "SINGLE_COMPOUND_CANDIDATE" else "NO"))
with (OUT / "queue_scope_triage_2026-11-27.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
cnt = Counter(r["scope"] for r in out)
summary = dict(total=len(out), scope_counts=dict(cnt),
               eligible_single_compound=cnt.get("SINGLE_COMPOUND_CANDIDATE", 0),
               note="Title-based scope triage; single-compound subset eligible for next full-text extraction + six-gate intake. Mixtures/extracts/methods out of scope for single-compound capacity model.")
(OUT / "queue_scope_triage_2026-11-27_qc.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("queue rows:", len(out), "| scope:", dict(cnt))
