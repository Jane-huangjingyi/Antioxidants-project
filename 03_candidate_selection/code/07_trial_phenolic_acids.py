"""Compare the first-round ranking with an isolated Table 1 unit sensitivity."""
import json
import math
from importlib import import_module

external = import_module("06_check_external_orac")
ledger = external.ledger
model = import_module("01_fit_orac_fl")
predict = import_module("02_validate_and_rank").predictions_on_prior_rows


def main():
    first_sha, first = ledger.snapshot(ledger.BASELINE)
    baseline = external.baseline_training(first_sha, first)
    for index, row in enumerate(baseline):
        row["evidence_id"] = index
    source = ledger.rank_builder.read(
        ledger.IDENTITY / "inputs/provenance/ORAC_Four_Phenolic_Acids_2025.csv"
    )
    assert len({row["candidate_id"] for row in source}) == len(source) == 4
    assert {row["doi"] for row in source}.isdisjoint({row["doi"] for row in baseline})
    assert all(first[row["candidate_id"]]["conditional_rank"] for row in source)
    assert all(row["raw_unit"] == "mmol TE/mmol" and row["error_definition"] == "SEM"
               and row["model_disposition"] == "CONDITIONAL_TRIAL_TABLE_UNIT" for row in source)
    added = [dict(candidate_id=row["candidate_id"], doi=row["doi"],
                  source_block=row["doi"] + "|PH74_NET_AUC_100MIN_TABLE1",
                  mean=row["raw_mean"], reported_error=row["raw_error"], error_type="SEM")
             for row in source]
    trial = baseline + added
    assert all(model.cv(row) is None for row in added)
    ids, _, _, beta = model.fit(trial, "CV")
    ranks = model.positions(ids, beta[:len(ids)])
    doi_ids, _, _, doi_beta = model.fit(trial, "DOI")
    doi_ranks = model.positions(doi_ids, doi_beta[:len(doi_ids)])
    old_ids, _, _, old_beta = model.fit(baseline, "CV")
    assert model.positions(old_ids, old_beta[:len(old_ids)]) == {
        cid: int(row["conditional_rank"]) for cid, row in first.items() if row["conditional_rank"]
    }
    diagnostics, best, worst, missing = model.metrics_and_deletion(trial, "CV", include_best=True)
    base_diagnostics, _, _, _ = model.metrics_and_deletion(baseline, "CV", include_best=True)
    first_prediction = predict(baseline, baseline)
    trial_prediction = predict(trial, baseline)
    common = [row for row in baseline if row["evidence_id"] in first_prediction.keys()
              & trial_prediction.keys()]
    paired_rmse = {
        label: math.sqrt(sum((math.log(float(row["mean"])) - predictions[row["evidence_id"]])**2
                             for row in common) / len(common))
        for label, predictions in (("first", first_prediction), ("trial", trial_prediction))
    }
    measured = {r["candidate_id"]: r for r in source}
    comparison = []
    for cid, row in first.items():
        old = row["conditional_rank"]
        if not old:
            continue
        rank = ranks[cid]
        lo, hi = min(best[cid], doi_ranks[cid]), max(worst[cid], doi_ranks[cid])
        status = ("HOLD_RANK_UNAVAILABLE_AFTER_DOI_DELETION" if cid in missing else
                  "HOLD_RANK_SHIFT_OVER_10" if max(rank - lo, hi - rank) > 10
                  else "RETAIN_STABLE_WITHIN_10")
        comparison.append(dict(
            candidate_id=cid, compound=row["compound"], first_rank=old,
            first_status=row["validation_review_status"], trial_rank=rank,
            trial_minus_first=rank - int(old), trial_best=lo, trial_worst=hi,
            trial_status=status,
            new_report_doi=measured.get(cid, {}).get("doi", ""),
            new_table_mean_mmol_te_per_mmol=measured.get(cid, {}).get("raw_mean", ""),
            analysis_status="EXPLORATORY_TABLE_UNIT_SENSITIVITY",
        ))
    directory = ledger.STEP / "12_evidence_expansion"
    ledger.write(directory / "Trial_Phenolic_Acid_Rank_Comparison.csv", comparison)
    summary = dict(baseline_commit=first_sha, trial_observations=len(trial),
                   trial_dois=len({row["doi"] for row in trial}),
                   compared_compounds=len(comparison), added_observations=len(added),
                   baseline_holdout=base_diagnostics, trial_holdout=diagnostics,
                   matched_holdout=dict(rows=len(common), **paired_rmse))
    (directory / "Trial_Phenolic_Acid_Diagnostics.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
