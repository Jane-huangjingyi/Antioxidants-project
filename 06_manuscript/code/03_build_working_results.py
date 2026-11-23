"""Render working manuscript results from the current literature analysis."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "02_identity_and_evidence/result/table/audit"
MODEL = ROOT / "03_candidate_selection/result/model"
OUTPUT = ROOT / "06_manuscript/result/02_results_working.md"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    screen = read_json(EVIDENCE / "Screening_QC.json")
    queue = read_json(EVIDENCE / "Fulltext_Batch_Summary.json")
    validation = read_json(MODEL / "02_whole_doi_validation.json")["models"]
    with (MODEL.parent / "table/04_figure1_candidate_ranks.csv").open(encoding="utf-8", newline="") as stream:
        decisions = Counter(row["validation_review_status"] for row in csv.DictReader(stream))
    prior = validation["prior"]
    current = validation["plus_2021_conditionally"]
    sensitivity = validation["plus_both_sensitivity"]
    pending = sum(queue["pending_routes"].values())
    reviewed = queue["priority_reports"] - pending
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        f"""# Working Results 1. Literature-informed candidate prioritization

## Literature screening

The available exports yielded {screen["provisional_intake_union"]:,} provisional report records after identifier reconciliation. Automated screening used titles and abstracts for {screen["abstract_checked"]:,} records and titles alone for {screen["title_only"]:,}. It linked {screen["candidate_covered"]} of {screen["candidate_profiles"]} compound profiles to at least one report. The priority ORAC queue contains {queue["priority_reports"]} records, with {reviewed} scoped reviews recorded and {pending} records pending. Final scientific eligibility remains open. See the [candidate evidence coverage table](../../02_identity_and_evidence/result/table/01_candidate_report_coverage.csv) and [full-text batch summary](../../02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json).

## Conditional ORAC-FL ranking

The conditional model used {current["rows"]} observations from {current["dois"]} DOI reports and covered {current["compounds"]} compounds. The protocol sensitivity used {sensitivity["rows"]} observations from {sensitivity["dois"]} DOI reports. For the same {current["same_prior_test_rows"]} estimable whole-report holdout observations, log-capacity RMSE was {prior["same_prior_test_rmse"]:.3f} for the prior model, {current["same_prior_test_rmse"]:.3f} for the expanded conditional model, and {sensitivity["same_prior_test_rmse"]:.3f} for the protocol sensitivity. The [rank and source-deletion table](../../03_candidate_selection/result/table/03_rank_sensitivity.csv) shows conditional ranks and their sensitivity to source choice. DOI counts describe reports. Independent experiments require separate verification.

With the ±10-position stability rule, {decisions["RETAIN_STABLE_WITHIN_10"]} of {current["compounds"]} ranked compounds were retained for further evaluation. {decisions["HOLD_RANK_SHIFT_OVER_10"]} exceeded ten positions and {decisions["HOLD_RANK_UNAVAILABLE_AFTER_DOI_DELETION"]} lost their rank in at least one DOI deletion. The [Figure 1 ranking table](../../03_candidate_selection/result/table/04_figure1_candidate_ranks.csv) records each decision. Experimental validation in the selected absorbance assay remains a future step.
""",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
