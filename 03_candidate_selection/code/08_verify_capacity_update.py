"""Verify the Carthamus capacity update outputs (reproducibility/checks). Run from root."""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "03_candidate_selection/12_evidence_expansion/run_carthamus_2026-11-27"
INTAKE = ROOT / "03_candidate_selection/12_evidence_expansion/intake_carthamus_2026-11-27.csv"
FIG = ROOT / "03_candidate_selection/result/figure/capacity_update_carthamus_2026-11-27"
ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok = ok and cond
GATES = ("identity_review","food_review","original_review","protocol_review","independence_review","quality_review")
rows = list(csv.DictReader(INTAKE.open(encoding="utf-8-sig", newline="")))
check("intake rows == 2", len(rows) == 2)
check("all six gates PASS + APPROVED", all(r["decision"]=="APPROVED_FOR_NEXT_ANALYSIS" and all(r[g]=="PASS" for g in GATES) for r in rows))
check("independent_n == 6 (SD)", all(r["independent_n"]=="6" and r["error_definition"]=="SD" for r in rows))
check("molar conversion = raw*1e-3", all(abs(float(r["model_mean_molar"]) - float(r["value"])*1e-3) < 1e-6 for r in rows))
rep = json.loads((RUN/"Evidence_Change_Report.json").read_text(encoding="utf-8"))
check("added_observations == 2", rep["added_observations"] == 2)
check("added_model_rows == 2 (113->115)", rep["added_model_rows"] == 2)
check("Top20 membership unchanged", rep["model_entry"] == [] and rep["model_exit"] == [])
check("released False / tier pending", rep["released"] is False and rep["automatic_tier_changes"] == 0)
check("new model RMSE < baseline RMSE", rep["new_model_metrics"]["model_RMSE"] < rep["new_model_metrics"]["baseline_RMSE"])
mp = list(csv.DictReader((RUN/"Model_Positions.csv").open(encoding="utf-8-sig", newline="")))
check("Model_Positions has both affected", {"AFF-0019","AFF-0062"} <= {r["candidate_id"] for r in mp})
check("figure PNG exists", FIG.with_suffix(".png").exists())
check("figure SVG exists", FIG.with_suffix(".svg").exists())
print("VERIFY", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
