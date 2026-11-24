"""Score the external fisetin measurement against the first-round ORAC-FL model."""
import csv
import math
import subprocess
from importlib import import_module

ledger = import_module("05_build_evidence_round_tables")
fit = import_module("01_fit_orac_fl").fit


def baseline_training(first_sha, first):
    observations = ledger.rank_builder.conditional_observations()
    expected_pairs = {(cid, doi) for cid, row in first.items()
                      for doi in filter(None, row["conditional_orac_dois"].split(";"))}
    assert len(observations) == 125
    assert {(cid, doi) for cid, doi, *_ in observations} == expected_pairs
    table = ledger.TABLE
    for name in ("01_connected_model_input.csv", "02_harmonized_observations.csv"):
        path = table / name
        committed = subprocess.check_output(
            ["git", "show", f"{first_sha}:{path.relative_to(ledger.ROOT).as_posix()}"], cwd=ledger.ROOT
        )
        assert path.read_bytes().replace(b"\r\n", b"\n") == committed
    read = ledger.rank_builder.read
    training = [dict(candidate_id=row["candidate_id"], doi=row["doi"],
                     source_block=row["source_block"], mean=row["mean_mol_te_per_mol"],
                     reported_error=row["error_mol_te_per_mol"], error_type=row["error_type"])
                for row in read(table / "01_connected_model_input.csv")]
    training.extend(dict(candidate_id=row["candidate_id"], doi=row["doi"],
                         source_block=row["doi"] + "|TABLE_PURE_ORAC_FL",
                         mean=row["mean_mol_te_per_mol"], reported_error=row["sd_mol_te_per_mol"],
                         error_type=row["error_definition"])
                    for row in read(table / "02_harmonized_observations.csv") if row["usage"] == "CONDITIONAL")
    return training


def main():
    first_sha, first = ledger.snapshot(ledger.BASELINE)
    raw = ledger.rank_builder.read(
        ledger.IDENTITY / "inputs/provenance/ORAC_Targeted_Observations_2026-11-23.csv"
    )
    external, = (row for row in raw if row["model_disposition"].startswith("EXTERNAL_DIAGNOSTIC"))
    assert external["raw_unit"] == "µM TE/µM sample"
    training = baseline_training(first_sha, first)
    assert external["doi"] not in {row["doi"] for row in training}
    table = ledger.TABLE
    ids, _, _, beta = fit(training, "CV")
    cid = external["candidate_id"]
    estimate = math.exp(beta[ids.index(cid)])
    measured = float(external["raw_mean"])
    output = dict(baseline_commit=first_sha, candidate_id=cid, doi=external["doi"],
                  source_locator=external["source_locator"], observed_mol_te_per_mol=measured,
                  reported_sd=float(external["raw_error"]), predicted_mol_te_per_mol=estimate,
                  observed_over_predicted=measured / estimate,
                  log_observed_minus_log_predicted=math.log(measured / estimate),
                  disposition=external["model_disposition"])
    with (table / "audit/External_ORAC_Diagnostic.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output), lineterminator="\n")
        writer.writeheader()
        writer.writerow(output)
    print(f"{cid}: observed {measured:.2f}, predicted {estimate:.3f}, ratio {measured / estimate:.2f}")


if __name__ == "__main__":
    main()
