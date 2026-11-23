"""Build a shared Figure 1 ranking table from existing conditional ORAC-FL data."""
import csv
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from statistics import median

STEP = Path(__file__).resolve().parents[1]
TABLE = STEP / "result/table"
EVIDENCE = STEP.parent / "02_identity_and_evidence/result/table"
MAX_RANK_SHIFT = 10
SD_TYPES = {"SD", "SD_TRIPLICATE_EXPERIMENTS"}
SCENARIOS = ("plus_2021_conditionally", "prior", "plus_both_sensitivity",
             "only_add_2022_sensitivity", "empirical_cv_q75_sensitivity")


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def descending_ranks(values):
    ranks = {}
    for position, value in enumerate(sorted(values.values(), reverse=True), start=1):
        ranks.setdefault(value, position)
    return {key: ranks[value] for key, value in values.items()}


def conditional_observations():
    prior = read(TABLE / "01_connected_model_input.csv")
    followup = read(TABLE / "02_harmonized_observations.csv")
    rows = [(r["candidate_id"], r["doi"], r["source_block"], float(r["mean_mol_te_per_mol"]),
             r["error_type"] in SD_TYPES and bool(r["error_mol_te_per_mol"]))
            for r in prior]
    rows.extend((r["candidate_id"], r["doi"], r["doi"] + "|TABLE_PURE_ORAC_FL",
                 float(r["mean_mol_te_per_mol"]),
                 r["error_definition"] == "SD" and bool(r["sd_mol_te_per_mol"]))
                for r in followup if r["usage"] == "CONDITIONAL")
    assert len(rows) == len({row[:3] for row in rows})
    return rows


def observed_relative_capacity(blocks):
    by_candidate = defaultdict(lambda: defaultdict(list))
    for (doi, _), values in blocks.items():
        if len(values) < 2:
            continue
        for candidate, value in values.items():
            below = sum(other < value for other in values.values())
            ties = sum(other == value for other in values.values()) - 1
            percentile = Fraction(2 * below + ties, 2 * (len(values) - 1))
            by_candidate[candidate][doi].append(percentile)
    return {candidate: median(median(block) for block in reports.values())
            for candidate, reports in by_candidate.items()}


def main():
    profiles = read(EVIDENCE / "candidate_evidence_profiles.csv")
    coverage = {r["candidate_id"]: r for r in read(EVIDENCE / "01_candidate_report_coverage.csv")}
    ranks = {r["candidate_id"]: r for r in read(TABLE / "03_rank_sensitivity.csv")}
    blocks, reports, sd_reports = defaultdict(dict), defaultdict(set), defaultdict(set)
    for candidate, doi, block, mean, has_sd in conditional_observations():
        blocks[doi, block][candidate] = mean
        reports[candidate].add(doi)
        if has_sd:
            sd_reports[candidate].add(doi)
    assert reports.keys() == ranks.keys()
    observed = observed_relative_capacity(blocks)
    doi_counts = {cid: len(dois) for cid, dois in reports.items()}
    sd_shares = {cid: Fraction(len(sd_reports[cid]), n) for cid, n in doi_counts.items()}
    observed_order = descending_ranks(observed)
    support_order = descending_ranks(doi_counts)
    sd_order = descending_ranks(sd_shares)

    entries = []
    for profile in profiles:
        cid = profile["candidate_id"]
        source = coverage[cid]
        rank = ranks.get(cid)
        if rank:
            primary = int(rank[SCENARIOS[0]])
            scenarios = [int(rank[s]) for s in SCENARIOS]
            loo_best = int(rank["best_doi_deletion_both"])
            loo_worst = int(rank["worst_doi_deletion_both"])
            best = min(*scenarios, loo_best)
            worst = max(*scenarios, loo_worst)
            missing = rank["missing_in_any_doi_deletion_both"] == "YES"
            shift = "" if missing else max(primary-best, worst-primary)
            if missing:
                status = "HOLD_RANK_UNAVAILABLE_AFTER_DOI_DELETION"
            elif shift > MAX_RANK_SHIFT:
                status = f"HOLD_RANK_SHIFT_OVER_{MAX_RANK_SHIFT}"
            else:
                status = f"RETAIN_STABLE_WITHIN_{MAX_RANK_SHIFT}"
        else:
            primary = loo_best = loo_worst = best = worst = shift = ""
            scenarios = []
            status = "CONDITIONAL_MODEL_RANK_UNAVAILABLE"
        entries.append(dict(
            candidate_id=cid, compound=profile["compound_name"],
            conditional_rank=primary, validation_review_status=status,
            observed_orac_within_block_percentile=float(observed[cid]) if cid in observed else "",
            observed_orac_relative_rank=observed_order.get(cid, ""),
            typed_sd_doi_reports=len(sd_reports[cid]) if rank else "",
            typed_sd_report_fraction=float(sd_shares[cid]) if rank else "",
            sd_reporting_rank=sd_order.get(cid, ""),
            quality_weighted_rank="",
            conditional_orac_doi_reports=doi_counts.get(cid, ""),
            conditional_orac_report_count_rank=support_order.get(cid, ""),
            public_literature_links=source["public_union_report_links"],
            historical_confirmed_independent_horac_studies=profile["confirmed_independent_horac_studies"],
            best_rank_across_fit_scenarios=min(scenarios) if rank else "",
            worst_rank_across_fit_scenarios=max(scenarios) if rank else "",
            best_doi_deletion_rank_two_source_sensitivity=loo_best,
            worst_doi_deletion_rank_two_source_sensitivity=loo_worst,
            best_rank_across_fits_and_deletions=best,
            worst_rank_across_fits_and_deletions=worst,
            max_absolute_rank_shift=shift,
            adjusted_log_sd_two_source_sensitivity=rank["between_doi_adjusted_log_sd"] if rank else "",
            conditional_orac_dois=";".join(sorted(reports.get(cid, set()))),
        ))
    entries.sort(key=lambda r: (r["conditional_rank"] == "", r["conditional_rank"], r["candidate_id"]))
    assert len(entries) == len({r["candidate_id"] for r in entries}) == len(coverage)
    output = TABLE / "04_figure1_candidate_ranks.csv"
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(entries[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(entries)
    priority = [r["compound"] for r in entries
                if r["validation_review_status"] == f"RETAIN_STABLE_WITHIN_{MAX_RANK_SHIFT}"]
    print(f"Figure 1 ranks: {len(entries)} profiles, {len(ranks)} conditional ranks, "
          f"{len(priority)} stable within {MAX_RANK_SHIFT} positions.")
    print(", ".join(priority))


if __name__ == "__main__":
    main()
