"""Build a six-gate adjudication worksheet for the ORAC-ready OA queue observations.
Pre-screen hints only; every gate remains PENDING for researcher decision (no auto-approval).
Run: python 03_candidate_selection/code/15_build_queue_adjudication.py
"""
import csv, json, sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
EXT = OUT / "queue_oa_extraction_2026-11-27.csv"
rows = [r for r in csv.DictReader(EXT.open(encoding="utf-8-sig", newline="")) if r["ready_for_review"] == "YES"]
GATES = ["identity_review", "food_review", "original_review", "protocol_review", "independence_review", "quality_review"]
COLS = ["source_id", "candidate_id", "doi", "title", "assay", "value", "unit", "direction", "error_definition",
        "independent_n", "protocol_block", "locator", "source_locator", "material",
        *GATES, "decision", "model_disposition", "model_mean_molar", "model_conversion_basis",
        "prescreen_identity", "prescreen_protocol", "prescreen_independence", "prescreen_quality", "orac_snippet"]
out = []
for i, r in enumerate(rows, 1):
    cids = r["candidate_ids"].split(";")
    single = len(cids) == 1
    rec = dict(source_id="SRC-QUEUE-%03d" % i, candidate_id=cids[0] if single else r["candidate_ids"],
               doi=r["doi"], title=r["title"], assay="ORAC-FL", value="", unit="", direction="Higher",
               error_definition="", independent_n="", protocol_block="", locator="", source_locator="", material="",
               decision="PENDING_HUMAN", model_disposition="", model_mean_molar="", model_conversion_basis="",
               prescreen_identity="LIKELY_SINGLE" if single else "MULTI_CHECK",
               prescreen_protocol="SIGNAL_PRESENT" if r["prot_sig"] == "YES" else "CHECK",
               prescreen_independence="N_REQUIRED" if r["err_sig"] == "YES" else "CHECK",
               prescreen_quality="UNIT_SIGNAL" if r["unit_sig"] == "YES" else "CHECK",
               orac_snippet=r["snippets"])
    for g in GATES:
        rec[g] = "PENDING"
    out.append(rec)
with (OUT / "queue_adjudication_worksheet_2026-11-27.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n"); w.writeheader(); w.writerows(out)
summary = dict(worksheet_rows=len(out), all_gates_pending=all(all(r[g] == "PENDING" for g in GATES) for r in out),
               decision_pending=all(r["decision"] == "PENDING_HUMAN" for r in out),
               prescreen=dict(Counter(r["prescreen_identity"] for r in out)),
               note="Researcher must fill value/unit/independent_n/error/protocol and set six gates PASS + APPROVED_FOR_NEXT_ANALYSIS before 03_update_evidence intake/refit.")
(OUT / "queue_adjudication_worksheet_2026-11-27_qc.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("worksheet rows:", len(out), "| prescreen:", summary["prescreen"])
