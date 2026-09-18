from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "figures" / "aqueous_antioxidant_atlas"

candidates = pd.read_csv(DATA / "Aqueous_Antioxidant_Candidate_Master.csv")
evidence = pd.read_csv(DATA / "Aqueous_Antioxidant_Primary_Literature_Evidence.csv")
papers = pd.read_csv(DATA / "Aqueous_Antioxidant_Paper_Summary.csv")
micro = pd.read_csv(DATA / "Antioxidant_Micronutrient_Redox_Profile.csv")

assert len(candidates) == 157
blocked = r"Carotenoid|tocopherol|tocotrienol|mineral cofactors"
assert not candidates["parent_class"].fillna("").str.contains(blocked, case=False, regex=True).any()
assert len(evidence) == 109 and len(papers) == 25 and len(micro) == 7

eligible = evidence[evidence["rank_eligible"].eq("yes")]
required = ["DOI", "original_value", "original_unit", "normalized_value", "normalized_unit",
            "conversion_formula", "independent_experiment_id"]
for col in required:
    assert eligible[col].notna().all(), f"missing {col} in rank-eligible evidence"
needs_mw = eligible[~eligible["conversion_formula"].eq("direct molar value")]
assert needs_mw["molecular_weight_used"].notna().all(), "MW missing where conversion requires it"
assert eligible[["exact_table", "exact_figure", "exact_page", "supplementary_location"]].notna().any(axis=1).all()

rank_files = [
    DATA / "Polyphenols_Flavonoids_Top20_v1.0.csv",
    DATA / "Polyphenols_PhenolicAcids_TopN_v1.0.csv",
    DATA / "VitaminC_TopAvailable_v1.0.csv",
]
known = set(evidence["legacy_record_id"].dropna().astype(str))
for path in rank_files:
    ranking = pd.read_csv(path)
    for value in ranking["provenance_record_ids"].dropna().astype(str):
        for record_id in [x.strip() for x in value.replace("|", ";").split(";") if x.strip()]:
            assert record_id in known, f"unresolved provenance {record_id} from {path.name}"

required_figures = [
    "Aqueous_Antioxidant_Class_Overview.png", "Aqueous_Class_Ranking_Leaders.png",
    "Aqueous_Primary_Literature_Coverage.png", "Aqueous_Evidence_Confidence_Overview.png",
    "Aqueous_Metal_Redox_Framework.png",
]
for name in required_figures:
    path = FIG / "00_overview" / name
    assert path.exists() and path.stat().st_size > 10_000, f"missing/small figure {name}"

for retained in [DATA / "Carotenoids_TopN_v1.0.csv", DATA / "VitaminE_TopN_v1.0.csv"]:
    assert retained.exists(), f"paused lipid output was lost: {retained.name}"

print({
    "candidate_rows": len(candidates),
    "evidence_rows": len(evidence),
    "rank_eligible_records": len(eligible),
    "paper_units": len(papers),
    "paper_units_with_doi": int(papers["DOI"].notna().sum()),
    "micronutrients": len(micro),
    "overview_figures": len(required_figures),
    "status": "PASS",
})
