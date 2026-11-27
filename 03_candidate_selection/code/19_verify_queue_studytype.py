"""Verify refined study-type outputs. Run from root."""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
FIG = ROOT / "03_candidate_selection/result/figure/capacity_queue_studytype_2026-11-27"
ok = True
def check(n, c):
    global ok; print(("PASS " if c else "FAIL ") + n); ok = ok and c
t = list(csv.DictReader((OUT / "queue_studytype_refined_2026-11-27.csv").open(encoding="utf-8-sig", newline="")))
e = [r for r in csv.DictReader((OUT / "queue_oa_extraction_2026-11-27.csv").open(encoding="utf-8-sig", newline="")) if r["ready_for_review"] == "YES"]
s = json.loads((OUT / "queue_studytype_refined_2026-11-27_qc.json").read_text(encoding="utf-8"))
check("refined rows == ready", len(t) == len(e))
check("admissible only PURE_STANDARD", all((r["admissible_for_intake"] == "YES") == (r["study_type"] == "PURE_STANDARD") for r in t))
check("summary admissible matches", s["admissible"] == sum(r["admissible_for_intake"] == "YES" for r in t))
check("figure PNG exists", FIG.with_suffix(".png").exists())
check("figure SVG exists", FIG.with_suffix(".svg").exists())
print("VERIFY", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
