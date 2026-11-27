"""Verify manual review + funnel outputs. Run from root."""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
FIG = ROOT / "03_candidate_selection/result/figure/capacity_evidence_funnel_2026-11-27"
ok = True
def check(n, c):
    global ok; print(("PASS " if c else "FAIL ") + n); ok = ok and c
r = list(csv.DictReader((OUT / "queue_pure_manual_review_2026-11-27.csv").open(encoding="utf-8-sig", newline="")))
s = json.loads((OUT / "queue_pure_manual_review_2026-11-27_qc.json").read_text(encoding="utf-8"))
check("manual review rows == 4", len(r) == 4)
check("verdicts recorded", all(x["verdict"] in ("NOT_ADMISSIBLE", "PENDING_RESEARCHER") for x in r))
check("clean admissible now == 0", s["clean_admissible_now"] == 0)
check("funnel PNG exists", FIG.with_suffix(".png").exists())
check("funnel SVG exists", FIG.with_suffix(".svg").exists())
print("VERIFY", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
