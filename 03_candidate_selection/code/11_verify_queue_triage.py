"""Verify queue scope triage outputs. Run from root."""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
FIG = ROOT / "03_candidate_selection/result/figure/capacity_queue_scope_triage_2026-11-27"
QUEUE = ROOT / "download_raw/07_机构与机器筛选_2026-11-26/stage2_machine_screening/ORAC_Fulltext_Review_Queue.csv"
ok = True
def check(n, c):
    global ok; print(("PASS " if c else "FAIL ") + n); ok = ok and c
q = list(csv.DictReader(QUEUE.open(encoding="utf-8-sig", newline="")))
t = list(csv.DictReader((OUT / "queue_scope_triage_2026-11-27.csv").open(encoding="utf-8-sig", newline="")))
s = json.loads((OUT / "queue_scope_triage_2026-11-27_qc.json").read_text(encoding="utf-8"))
check("triage rows == queue rows", len(t) == len(q))
check("scope counts sum == total", sum(s["scope_counts"].values()) == len(t))
check("eligible flag consistent", all((r["eligible_for_extraction"] == "YES") == (r["scope"] == "SINGLE_COMPOUND_CANDIDATE") for r in t))
check("figure PNG exists", FIG.with_suffix(".png").exists())
check("figure SVG exists", FIG.with_suffix(".svg").exists())
print("VERIFY", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
