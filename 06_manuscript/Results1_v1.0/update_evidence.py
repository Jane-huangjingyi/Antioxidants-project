"""Dry-run a reviewed evidence increment into a new directory; v1.0 is read-only."""
import argparse
from collections import defaultdict
from datetime import date
import math
from pathlib import Path
import sys

from build_results1 import HERE, MODEL, ROOT, readcsv, readjson, writecsv
from json import dumps

sys.path.insert(0, str(ROOT / "03_candidate_selection/09_aqueous_candidate_priority_v0.1"))
from build_priority import METHODS, observation, rank

sys.path.insert(0, str(ROOT / "03_candidate_selection/06_verified_source_update"))
import fit_verified_source_diagnostics as diag

GATES = ("identity_review", "food_review", "original_review", "protocol_review",
         "independence_review", "quality_review")
ASSAYS = set(METHODS)


def fit(rows):
    candidates = sorted({r["candidate_id"] for r in rows})
    estimates, _ = diag.fit(rows, candidates, "SHRINK_10")
    locations = dict(zip(candidates, map(float, estimates)))
    order = sorted(candidates, key=lambda cid: (-locations[cid], cid))
    obs, predicted, simple = [], [], []
    for doi in sorted({r["doi"] for r in rows}):
        training = [r for r in rows if r["doi"] != doi]
        ids = sorted({r["candidate_id"] for r in training})
        if not ids:
            continue
        blocks = sorted({r["source_block"] for r in training})
        design = diag.design(training, ids, blocks)
        projection = diag.np.linalg.pinv(design, rcond=1e-12) @ design
        estimate, _ = diag.fit(training, ids, "SHRINK_10")
        for r in rows:
            if r["doi"] != doi or r["candidate_id"] not in ids:
                continue
            j = ids.index(r["candidate_id"])
            v = diag.np.eye(design.shape[1])[j]
            if diag.np.linalg.norm(projection @ v - v) >= 1e-8:
                continue
            obs.append(math.log(float(r["mean"])))
            predicted.append(float(estimate[j]))
            simple.append(float(diag.np.mean([math.log(float(t["mean"])) for t in training
                                              if t["candidate_id"] == r["candidate_id"]])))
    def rmse(values):
        return math.sqrt(sum((x-y)**2 for x,y in zip(obs, values))/len(obs)) if obs else None
    return locations, {cid:i+1 for i,cid in enumerate(order)}, dict(scored=len(obs),
                 model_RMSE=rmse(predicted), baseline_RMSE=rmse(simple))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--intake", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--cutoff", type=date.fromisoformat, default=date(2026, 11, 17))
    a = p.parse_args()
    out = a.out.resolve()
    assert not out.is_relative_to(HERE), "Use a new, separate output directory."
    assert not out.exists(), "Choose an unused output directory."
    base = readjson(HERE / "Evidence_Snapshot.json")
    profiles = {r["candidate_id"]:r["compound_name"] for r in readcsv(
        ROOT / "02_identity_and_evidence/results/candidate_evidence_profiles.csv")}
    existing = {(r["candidate_id"],r["doi"],r["assay"],r["locator"]) for r in base["observations"]}
    source_ids = {r["source_id"] for r in base["observations"]}
    combined = list(base["observations"])
    fl = [r for r in readcsv(MODEL/"results/Analysis_Data_and_Dispositions.csv")
          if r["extended_conflict_excluded_diagnostic"] == "YES"]
    assert len(fl) == 113
    new_fl = list(fl)
    linked = {r["candidate_id"] for r in fl}
    model_keys = {(r["doi"],r["candidate_id"],r["source_block"]) for r in fl}
    pending, used = [], []
    for r in readcsv(a.intake):
        r["doi"] = r["doi"].strip().lower().removeprefix("https://doi.org/")
        key = tuple(r[k] for k in ("candidate_id","doi","assay","locator"))
        try:
            assert r["decision"] == "APPROVED_FOR_NEXT_ANALYSIS" and all(r[g] == "PASS" for g in GATES)
            assert r["candidate_id"] in profiles and r["doi"].startswith("10.") and "/" in r["doi"]
            assert date(2016,1,1) <= date.fromisoformat(r["first_public_date"]) <= a.cutoff
            assert r["source_id"] and r["source_id"] not in source_ids and key not in existing
            assert r["assay"] in ASSAYS and r["direction"] in {"Higher","Lower"}
            assert all(r[k].strip() for k in ("unit","protocol_block","locator","source_locator","material"))
            assert math.isfinite(float(r["value"]))
        except (AssertionError, KeyError, ValueError):
            pending.append(dict(source_id=r.get("source_id",""), reason="Review, duplicate, date, identity or field gate"))
            continue
        source_ids.add(r["source_id"])
        existing.add(key)
        cid = r["candidate_id"]
        combined.append(observation(cid, profiles[cid], r["assay"], r["doi"], r["value"], None,
                        r["unit"], r["protocol_block"], r["direction"], r["locator"],
                        "Conditional within source", "", "Primary" if r["first_public_date"] >= "2020" else "Evidence-gap",
                        material=r["material"], source_id=r["source_id"], source=r["source_locator"],
                        independent_n=r["independent_n"], error_type=r["error_definition"]))
        used.append(r)
        if r["model_disposition"] != "APPROVED_CONNECTED_FL":
            continue
        block = r["doi"]+"|"+r["protocol_block"]
        model_key = (r["doi"], cid, block)
        try:
            mean = float(r["model_mean_molar"])
            assert r["assay"] == "ORAC-FL" and cid in linked and r["model_conversion_basis"].strip()
            assert mean > 0 and math.isfinite(mean) and model_key not in model_keys
        except (ValueError, AssertionError):
            pending.append(dict(source_id=r["source_id"], reason="Model gate; observation retained for assay comparison only"))
            continue
        model_keys.add(model_key)
        new_fl.append(dict(candidate_id=cid, doi=r["doi"], source_block=block, mean=mean))
    ranking, strata = rank(combined)
    base_location, base_positions, base_metrics = fit(fl)
    new_location, new_positions, new_metrics = fit(new_fl) if len(new_fl)>len(fl) else (base_location,base_positions,base_metrics)
    old_ranks = {r["source_id"]:r["rank_in_block"] for r in base["rankings"]}
    changes = [{"source_id":r["source_id"],"old_rank":old_ranks.get(r["source_id"],""),
                "new_rank":r["rank_in_block"]} for r in ranking if old_ranks.get(r["source_id"]) != r["rank_in_block"]]
    ranked_ids = {r["source_id"] for r in ranking}
    changes += [dict(source_id=s,old_rank=n,new_rank="") for s,n in old_ranks.items() if s not in ranked_ids]
    old_top = {k for k,v in base_positions.items() if v <= 20}
    new_top = {k for k,v in new_positions.items() if v <= 20}
    affected = {r["candidate_id"] for r in used}
    out.mkdir(parents=True)
    writecsv(out/"Candidate_Membership_Review.csv", [
        dict(candidate_id=cid,prior_tier=next((row["tier"] for row in base["panel"] if row["candidate_id"]==cid),""),
             affected_by_new_direct_evidence=cid in affected,proposed_next_tier="",decision="PENDING_HUMAN")
        for cid in sorted(affected | {r["candidate_id"] for r in base["panel"]})])
    writecsv(out/"Model_Positions.csv",[dict(candidate_id=cid, baseline_location=base_location[cid],
        next_location=new_location[cid], baseline_position=base_positions[cid], next_position=new_positions[cid])
        for cid in sorted(base_positions)])
    writecsv(out/"Ranked_Observations.csv", ranking)
    summary = dict(released=False, added_observations=len(used),
        new_report_DOIs=sorted({r["doi"] for r in used}-{r["doi"] for r in base["observations"]}),
        independent_study_count_change="Requires scientific adjudication",
        affected_candidates=sorted(affected), added_model_rows=len(new_fl)-len(fl),
        old_model_metrics=base_metrics, new_model_metrics=new_metrics, protocol_blocks=len(strata),
        model_entry=sorted(new_top-old_top), model_exit=sorted(old_top-new_top), changed_rank_rows=changes,
        holds=pending, stability_status="REVIEW_REQUIRED" if changes or new_top!=old_top or used else "BASELINE_REPLAY",
        automatic_tier_changes=0)
    (out/"Evidence_Change_Report.json").write_text(dumps(summary,indent=2)+"\n", encoding="utf8")
    print("increment",len(used),"rank changes",len(changes),"model rows",len(new_fl), "scored",new_metrics["scored"])


if __name__ == "__main__":
    main()
