"""Verify OA queue extraction outputs. Run from root."""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
FIG = ROOT / "03_candidate_selection/result/figure/capacity_queue_oa_extraction_2026-11-27"
ok = True
def check(n, c):
    global ok; print(("PASS " if c else "FAIL ") + n); ok = ok and c
t = list(csv.DictReader((OUT / "queue_oa_extraction_2026-11-27.csv").open(encoding="utf-8-sig", newline="")))
tri = [r for r in csv.DictReader((OUT / "queue_scope_triage_2026-11-27.csv").open(encoding="utf-8-sig", newline="")) if r["eligible_for_extraction"] == "YES"]
s = json.loads((OUT / "queue_oa_extraction_2026-11-27_qc.json").read_text(encoding="utf-8"))
check("extraction rows == eligible leads", len(t) == len(tri))
check("ready implies OA + snippets", all((r["ready_for_review"] == "YES") <= (r["oa"] == "YES" and int(r["n_snip"]) > 0) for r in t))
check("summary ready matches", s["ready_for_review"] == sum(r["ready_for_review"] == "YES" for r in t))
check("figure PNG exists", FIG.with_suffix(".png").exists())
check("figure SVG exists", FIG.with_suffix(".svg").exists())
print("VERIFY", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
