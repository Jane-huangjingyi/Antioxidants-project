"""Verify the queue adjudication worksheet. Run from root."""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
ok = True
def check(n, c):
    global ok; print(("PASS " if c else "FAIL ") + n); ok = ok and c
GATES = ["identity_review", "food_review", "original_review", "protocol_review", "independence_review", "quality_review"]
w = list(csv.DictReader((OUT / "queue_adjudication_worksheet_2026-11-27.csv").open(encoding="utf-8-sig", newline="")))
e = [r for r in csv.DictReader((OUT / "queue_oa_extraction_2026-11-27.csv").open(encoding="utf-8-sig", newline="")) if r["ready_for_review"] == "YES"]
s = json.loads((OUT / "queue_adjudication_worksheet_2026-11-27_qc.json").read_text(encoding="utf-8"))
check("worksheet rows == ORAC-ready", len(w) == len(e))
check("all six gates PENDING", all(all(r[g] == "PENDING" for g in GATES) for r in w))
check("decision PENDING_HUMAN (no auto-approval)", all(r["decision"] == "PENDING_HUMAN" for r in w))
check("no auto-filled value/independent_n", all(r["value"] == "" and r["independent_n"] == "" for r in w))
check("snippet present for review", all(r["orac_snippet"].strip() for r in w))
print("VERIFY", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
