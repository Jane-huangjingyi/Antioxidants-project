from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA, DOCS, FIG = ROOT / "data", ROOT / "docs", ROOT / "figures" / "aqueous_antioxidant_atlas"
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

candidates = pd.read_csv(DATA / "Aqueous_Antioxidant_Candidate_Master.csv")
search = pd.read_csv(DATA / "Stage24_Literature_Search_Log.csv")
future = pd.read_csv(DATA / "Future_Candidate_Additions_Log.csv")
evidence = pd.read_csv(DATA / "Aqueous_Antioxidant_Primary_Literature_Evidence.csv")
overview = pd.read_csv(DATA / "Supervisor_Aqueous_Class_Ranking_Overview.csv")
stil = pd.read_csv(DATA / "Stilbenes_Lignans_Evidence_Master.csv")
other = pd.read_csv(DATA / "Other_Aqueous_Phytochemicals_Evidence_Master.csv")
metal = pd.read_csv(DATA / "Aqueous_Metal_Redox_Evidence.csv")
micro = pd.read_csv(DATA / "Antioxidant_Micronutrient_Redox_Profile_v2.csv")

check(len(candidates) == 157, f"candidate universe changed: {len(candidates)}")
check(search.compound.nunique() == 157 and len(search) == 157, "search log is not one row per frozen candidate")
check(not set(future.candidate).intersection(set(candidates.compound)), "future additions leaked into frozen universe")
expected = {
    "Polyphenols - Flavonoids": 59,
    "Polyphenols - Phenolic acids / conjugates": 29,
    "Polyphenols - Stilbenes / lignans": 15,
    "Vitamins / vitamin-like": 2,
    "Betalains / nitrogen-containing": 11,
    "Organosulfur compounds": 15,
    "Other food-derived redox-active phytochemicals": 26,
}
check(candidates.analysis_panel.value_counts().to_dict() == expected, "frozen panel counts differ from Stage 23")
check(stil.compound.nunique() == 15 and other.compound.nunique() == 26, "new class masters do not cover frozen panels")
check((stil.rank_eligible == "yes").sum() == 2, "stilbene/lignan rankable count is not 2")
check((other.rank_eligible == "yes").sum() == 5, "other-aqueous rankable count is not 5")
check(len(evidence) == 130, f"unexpected evidence row count: {len(evidence)}")
ranked_new = evidence[evidence.analysis_panel.isin(["Polyphenols - Stilbenes / lignans", "Other food-derived redox-active phytochemicals"]) & evidence.rank_eligible.eq("yes")]
check(ranked_new.DOI.notna().all(), "a new rank-eligible record lacks DOI")
check(ranked_new.normalized_value.notna().all(), "a new rank-eligible record lacks normalized value")
check(set(ranked_new.evidence_tier) == {"B1"}, "new numerical ranks contain a non-B1 tier")
check(len(metal) == 8 and len(micro) == 7, "metal or micronutrient profile count changed")
check(not any("global" in c.lower() and "score" in c.lower() for c in overview.columns), "global composite score column detected")
vitc = overview[overview.analysis_subpanel.eq("Vitamin C aqueous")]
check(len(vitc) == 1 and vitc.within_class_percentile.isna().all(), "Vitamin C singleton percentile must be NA")
check(overview.loc[overview.analysis_subpanel.eq("Flavonoids"), "rankable_N"].eq(25).all(), "flavonoid rankable denominator must be 25")
check(overview.loc[overview.analysis_subpanel.eq("Phenolic acids / conjugates"), "rankable_N"].eq(18).all(), "phenolic-acid denominator must be 18")

required_dirs = ["00_overview", "01_flavonoids", "02_phenolic_acids", "03_stilbenes_lignans", "04_water_soluble_vitamins", "05_betalains", "06_organosulfur", "07_other_aqueous_phytochemicals", "08_metal_chelation", "09_micronutrients", "99_methods_qc"]
for name in required_dirs:
    check((FIG / name).exists() and any((FIG / name).iterdir()), f"empty or absent figure folder: {name}")
required_figures = [
    "00_overview/Aqueous_All_Classes_Ranking_Overview.png",
    "00_overview/Aqueous_Class_Coverage_Overview.png",
    "03_stilbenes_lignans/Stilbenes_Lignans_TopN.png",
    "03_stilbenes_lignans/Stilbenes_Lignans_Primary_Literature_Coverage.png",
    "05_betalains/Betalains_Profile_Comparison.png",
    "06_organosulfur/Organosulfur_Redox_Mechanism_Profile.png",
    "07_other_aqueous_phytochemicals/Other_Aqueous_TopN.png",
    "07_other_aqueous_phytochemicals/Other_Aqueous_Primary_Literature_Coverage.png",
    "08_metal_chelation/Metal_Chelation_Evidence_Overview.png",
    "09_micronutrients/Micronutrient_Redox_Profile.png",
]
for rel in required_figures:
    path = FIG / rel
    check(path.exists() and path.stat().st_size > 10_000, f"missing/small figure: {rel}")

for rel in [
    "Stilbenes_Lignans_Ranking_Coverage.csv",
    "Other_Aqueous_Phytochemicals_Ranking_Coverage.csv",
    "Supervisor_Aqueous_Class_Ranking_Overview.csv",
]:
    check((DATA / rel).exists(), f"missing output: {rel}")
check("Stage 24" in (DOCS / "PROJECT_STAGE_INDEX_CN.md").read_text(encoding="utf-8"), "Stage index not updated")
check("Stage 24" in (ROOT / "Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md").read_text(encoding="utf-8"), "Master history not updated")
check("## Sync to ChatGPT" in (DOCS / "Supervisor_Aqueous_Ranking_Progress_CN.md").read_text(encoding="utf-8"), "supervisor sync section missing")

if errors:
    raise SystemExit("STAGE 24 QC FAILED\n- " + "\n- ".join(errors))
print("STAGE 24 QC PASSED")
print({"frozen_candidates": len(candidates), "search_log": len(search), "evidence_rows": len(evidence), "ranked_new_records": len(ranked_new), "metal_records": len(metal), "micronutrients": len(micro)})
