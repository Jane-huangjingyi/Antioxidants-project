"""Prepare a six-gate intake CSV for the Carthamus 2024 ORAC-FL observations (reproducible).
Reads provenance, applies researcher adjudications (2026-11-27: Carthamus n=6 admitted; Wang kept held),
emits intake + rationale/QC json. Run: python 03_candidate_selection/code/06_prepare_capacity_intake.py
"""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
PROV = ROOT / "02_identity_and_evidence/inputs/provenance/ORAC_Tranche1_Observations_2026-11-26.csv"
OUTDIR = ROOT / "03_candidate_selection/12_evidence_expansion"
INTAKE = OUTDIR / "intake_carthamus_2026-11-27.csv"
QC = OUTDIR / "intake_carthamus_2026-11-27_qc.json"
DOI = "10.1016/j.jsps.2024.102106"
COLS = ["source_id","candidate_id","doi","first_public_date","assay","value","unit","direction",
        "error_definition","independent_n","protocol_block","locator","source_locator","material",
        "identity_review","food_review","original_review","protocol_review","independence_review",
        "quality_review","decision","model_disposition","model_mean_molar","model_conversion_basis"]
rows = []
for r in csv.DictReader(PROV.open(encoding="utf-8-sig", newline="")):
    if r["doi"] != DOI:
        continue
    raw = float(r["raw_mean"])
    molar = raw * 1e-3  # µM TE/mM sample = 1e-3 mol TE/mol
    rows.append(dict(
        source_id="SRC-CARTHAMUS2024-" + r["candidate_id"],
        candidate_id=r["candidate_id"], doi=DOI, first_public_date="2024-01-01",
        assay="ORAC-FL", value=r["raw_mean"], unit=r["raw_unit"], direction="Higher",
        error_definition="SD", independent_n="6",
        protocol_block="ORAC-FL_pH7.4_37C_reviewer-accepted-assumption",
        locator=r["source_locator"], source_locator=r["source_locator"], material=r["reported_material"],
        identity_review="PASS", food_review="PASS", original_review="PASS", protocol_review="PASS",
        independence_review="PASS", quality_review="PASS",
        decision="APPROVED_FOR_NEXT_ANALYSIS", model_disposition="APPROVED_CONNECTED_FL",
        model_mean_molar=f"{molar:.4f}",
        model_conversion_basis="µM TE/mM sample = 1e-3 mol TE/mol (Table 3); protocol pH7.4/37C reviewer-accepted assumption; SD n=6 Table 3 footer"))
with INTAKE.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n"); w.writeheader(); w.writerows(rows)
qc = dict(prepared_rows=len(rows), doi=DOI,
          gate_rationale=dict(identity_review="isolated compounds 1/4 matched to AFF-0062/AFF-0019",
                              food_review="isolated pure standards, not food matrix",
                              original_review="Table 3 ORAC column read from source",
                              protocol_review="researcher-accepted pH7.4/37C fluorescein assumption (2026-11-26)",
                              independence_review="SD n=6 confirmed Table 3 footer; researcher confirmed 2026-11-27",
                              quality_review="molar unit clean; SD not SEM"),
          conversion="model_mean_molar = raw_mean * 1e-3",
          held_this_round=dict(Wang_2025="row-level independent_n unknown (SEM 3-7 study-wide); researcher kept held 2026-11-27",
                               other_tranche_rows="HOLD error-type/unit-conflict/graphical/concentration-scale"),
          first_public_date_note="year-level 2024-01-01 from DOI; exact date pending")
QC.write_text(json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8")
print("intake rows:", len(rows), "->", INTAKE.name)
for r in rows: print("  ", r["candidate_id"], r["value"], r["unit"], "-> molar", r["model_mean_molar"])
