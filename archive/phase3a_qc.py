import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
read = lambda name: list(csv.DictReader((root / name).open(encoding="utf-8-sig", newline="")))
lock = read("data/Flavonoid_Phase3_Eligibility_Lock.csv")
ev = read("data/Flavonoid_H_ORAC_Evidence_Master.csv")
top = read("data/Polyphenols_Flavonoids_Top20_v1.0.csv")
cov = read("data/Flavonoid_Ranking_Coverage.csv")
errors = []
assert len(lock) == 59 and len({r["candidate_id"] for r in lock}) == 59
assert len(ev) == 94 and len({r["evidence_id"] for r in ev}) == 94
eligible = [r for r in ev if r["tier"] in {"A", "B1"}]
for r in eligible:
    float(r["normalized_value_mol_TE_mol"])
    if not all(r[x] for x in ("DOI", "exact_location", "independent_experiment_id")):
        errors.append(f"eligible provenance {r['evidence_id']}")
dup_key = [(r["candidate_id"], r["independent_experiment_id"], r["tier"], r["normalized_value_mol_TE_mol"]) for r in ev]
if len(dup_key) != len(set(dup_key)):
    errors.append("duplicate evidence")
assert len(top) == 20
if [int(r["rank"]) for r in top] != list(range(1, 21)):
    errors.append("rank sequence")
vals = [float(r["median_H_ORAC"]) for r in top]
if vals != sorted(vals, reverse=True):
    errors.append("sort order")
ev_ids = {r["evidence_id"] for r in ev}
for r in top:
    missing = set(r["provenance_record_ids"].split(";")) - ev_ids
    if missing:
        errors.append(f"broken provenance {sorted(missing)}")
if sum(int(r["universe_N"]) for r in cov) != 59: errors.append("coverage universe")
if sum(int(r["ranking_eligible_N"]) for r in cov) != 57: errors.append("coverage eligible")
if sum(int(r["Top20_N"]) for r in cov) != 20: errors.append("coverage top20")
figs = ["Antioxidant_Taxonomy_Hierarchy.png", "Flavonoid_Top20_H_ORAC.png", "Flavonoid_Top20_Evidence_Confidence.png", "Flavonoid_Subclass_Coverage.png", "Flavonoid_Evidence_Depth_vs_ORAC.png"]
for f in figs:
    p = root / "figures" / f
    if not p.exists() or p.stat().st_size < 10_000: errors.append(f"figure {f}")
print({
    "lock": len(lock), "eligible_lock": sum(r["ranking_eligible"] == "eligible_for_ranking" for r in lock),
    "hold": sum(r["ranking_eligible"] == "hold" for r in lock), "evidence": len(ev),
    **{tier: sum(r["tier"] == tier for r in ev) for tier in ("A", "B1", "B2", "C", "X")},
    "rankable": len({r["candidate_id"] for r in eligible}), "top20": len(top), "errors": errors,
})
if errors:
    raise SystemExit(1)
