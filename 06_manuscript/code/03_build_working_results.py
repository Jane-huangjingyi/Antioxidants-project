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
        rank_rows = list(csv.DictReader(stream))
    decisions = Counter(row["validation_review_status"] for row in rank_rows)
    retained = [row["compound"] for row in rank_rows
                if row["validation_review_status"] == "RETAIN_STABLE_WITHIN_10"]
    retained_names = ", ".join(retained[:-1]) + " and " + retained[-1] if len(retained) > 1 else "".join(retained)
    retained_detail = f" The retained set comprised {retained_names}." if retained_names else ""
    ascorbate = next(row for row in rank_rows if row["candidate_id"] == "AFF-0104")
    rosmarinic = next(row for row in rank_rows if row["candidate_id"] == "AFF-0084")
    prior = validation["prior"]
    current = validation["plus_2021_conditionally"]
    sensitivity = validation["plus_both_sensitivity"]
    pending = sum(queue["pending_routes"].values())
    reviewed = queue["priority_reports"] - pending
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        f"""# Results

## Evidence discovery and screening coverage

The available exports yielded {screen["provisional_intake_union"]:,} provisional report records after identifier reconciliation (Fig. 1a). Automated screening used titles and abstracts for {screen["abstract_checked"]:,} records and titles alone for {screen["title_only"]:,}. It linked {screen["candidate_covered"]} of {screen["candidate_profiles"]} compound profiles to at least one report. The priority ORAC queue contained {queue["priority_reports"]} records. At the analysis checkpoint, {reviewed} had a documented source-review scope and {pending} remained pending. Targeted extraction also used original reports from earlier source-recovery work. See the [candidate evidence coverage table](../../02_identity_and_evidence/result/table/01_candidate_report_coverage.csv) and [full-text batch summary](../../02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json).

## Conditional ORAC-FL ranking

The conditional model used {current["rows"]} observations from {current["dois"]} DOI reports and covered {current["compounds"]} compounds. The protocol sensitivity used {sensitivity["rows"]} observations from {sensitivity["dois"]} DOI reports. For the same {current["same_prior_test_rows"]} estimable whole-report holdout observations, log-capacity RMSE was {prior["same_prior_test_rmse"]:.3f} for the prior model, {current["same_prior_test_rmse"]:.3f} for the expanded conditional model, and {sensitivity["same_prior_test_rmse"]:.3f} for the protocol sensitivity. The [rank and source-deletion table](../../03_candidate_selection/result/table/03_rank_sensitivity.csv) shows conditional ranks and their sensitivity to source choice. DOI counts describe reports. Independent experiments require separate verification.

In the separate single-report structure analysis, scaffold-holdout RMSE was 0.945 for the selected Ridge analysis and 0.953 for the matched baseline, with an out-of-fold R² of −0.24. This analysis provided no cross-report validation of structure-based predictions.

## Rank stability identified compounds for further evaluation

With the ±10-position rule, {len(retained)} of {current["compounds"]} ranked compounds were retained (Fig. 1c).{retained_detail} Of the remaining compounds, {decisions["HOLD_RANK_SHIFT_OVER_10"]} exceeded ten positions and {decisions["HOLD_RANK_UNAVAILABLE_AFTER_DOI_DELETION"]} lost their rank in at least one DOI deletion. Rosmarinic acid ranked {rosmarinic["conditional_rank"]} in the conditional model. Its combined range reached rank {rosmarinic["worst_rank_across_fits_and_deletions"]}. L-ascorbic acid ranked {ascorbate["conditional_rank"]} and was supported by {ascorbate["conditional_orac_doi_reports"]} conditional-model reports. These examples illustrate the distinct roles of observed capacity, reporting coverage and model stability (Fig. 1b,c). The [Figure 1 ranking table](../../03_candidate_selection/result/table/04_figure1_candidate_ranks.csv) records each decision. The retained compounds constitute candidates for experimental qualification in a prospective absorbance assay.
""",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
