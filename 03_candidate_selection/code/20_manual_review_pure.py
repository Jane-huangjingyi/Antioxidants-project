"""Definitive manual review of the 4 PURE_STANDARD queue leads (researcher-assisted, recorded).
Run: python 03_candidate_selection/code/20_manual_review_pure.py
"""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
V = [
 ("10.1007/s11356-025-35893-8", "NEW-GSH", "NOT_ADMISSIBLE", "ORAC on Baltic clam tissue homogenate (ecotoxicology biomarker), not a pure GSH standard"),
 ("10.1080/14756366.2022.2041627", "AFF-0030", "PENDING_RESEARCHER", "pure naringenin skeleton ORAC 5.2 eq (Table 4) but row-level n/error not extracted; outside retained set; derivative-focused paper"),
 ("10.1371/journal.pone.0291000", "AFF-0159", "PENDING_RESEARCHER", "curcumin control ORAC (fluorescein 75mM PB 37C AAPH) but technical triplicate only; outside retained set; pulsed-light treatment study"),
 ("10.3389/fnut.2020.584900", "AFF-0036", "NOT_ADMISSIBLE", "ORAC of purified finger-citron flavonoid fraction (FFC), a mixture not a single pure compound"),
]
with (OUT / "queue_pure_manual_review_2026-11-27.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["doi", "candidate_id", "verdict", "reason"]); w.writerows(V)
from collections import Counter
c = Counter(v[2] for v in V)
summary = dict(reviewed=len(V), verdicts=dict(c), clean_admissible_now=0,
               note="OA queue yields no clean admissible single-compound ORAC addition without researcher adjudication of the 2 borderline; capacity ranking stable (Carthamus refit Top20 unchanged).")
(OUT / "queue_pure_manual_review_2026-11-27_qc.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("reviewed:", len(V), dict(c))
