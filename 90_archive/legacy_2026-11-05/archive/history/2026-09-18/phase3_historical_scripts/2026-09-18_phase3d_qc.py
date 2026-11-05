import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def rows(name):
    with open(ROOT / "data" / name, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

lock = rows("Vitamin_Phase3_Eligibility_Lock.csv")
assert len(lock) == 10
assert sum("aqueous" in r["vitamin_subpanel"] for r in lock) == 2
assert sum("lipid-phase" in r["vitamin_subpanel"] for r in lock) == 8
dha = next(r for r in lock if r["compound"] == "Dehydroascorbic acid")
assert dha["ranking_eligible"] == "hold"

vc = rows("VitaminC_TopAvailable_v1.0.csv")
assert len(vc) == 1 and float(vc[0]["primary_value"]) == 0.74
assert vc[0]["within_subpanel_percentile"] == "NA"
assert vc[0]["percentile_status"] == "single eligible candidate / percentile not informative"

ve = rows("VitaminE_TopN_v1.0.csv")
assert len(ve) == 8
assert [int(r["rank"]) for r in ve] == [1, 1, 3, 3, 5, 5, 7, 7]
for vitamer in ("alpha", "beta", "gamma", "delta"):
    pair = [float(r["primary_value"]) for r in ve if r["vitamer"] == vitamer]
    assert len(pair) == 2 and pair[0] == pair[1]

glob = rows("Global_Top_Overview_Master_v0.3.csv")
assert len(glob) == 56 and {r["overview_version"] for r in glob} == {"v0.3"}
vit = [r for r in glob if r["parent_class"] == "Vitamins / vitamin-like antioxidants"]
assert len(vit) == 9 and all(r["analysis_subpanel"] for r in vit)
asc = next(r for r in vit if r["compound"] == "L-Ascorbic acid")
assert asc["within_class_percentile"] == "NA"
assert "single eligible candidate" in asc["within_class_status"]

for name in (
    "VitaminC_Primary_Construct.png", "VitaminE_TopN_Primary_Construct.png",
    "VitaminE_Evidence_Confidence.png", "VitaminE_Assay_Environment_Coverage.png",
    "Vitamins_ParentClass_Overview.png", "Global_Overview_With_Vitamins.png",
):
    p = ROOT / "figures" / name
    assert p.exists() and p.stat().st_size > 10_000, name

print("Phase 3D QC passed: 10 candidates; Vitamin C percentile NA; Vitamin E percentile within N=8; Global v0.3=56 rows; 6 figures present.")
