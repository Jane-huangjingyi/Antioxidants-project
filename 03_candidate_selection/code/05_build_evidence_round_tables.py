"""Build compound evidence coverage and compare two versioned rank tables."""
import argparse
import csv
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from importlib import import_module

rank_builder = import_module("04_build_figure1_ranks")
STEP = Path(__file__).resolve().parents[1]
ROOT = STEP.parent
TABLE = STEP / "result/table"
IDENTITY = ROOT / "02_identity_and_evidence"
BASELINE = "e4c300c4220a8c671d899149ae079336dabfbebc"
RANK_PATH = "03_candidate_selection/result/table/04_figure1_candidate_ranks.csv"
SCOPED = {
    "CACHED_XML_SCOPE_RECORDED", "PUBLIC_FULLTEXT_SCOPE_RECORDED",
    "REUSE_RECORDED_SCOPE", "SCOPED_REVIEW_THIS_BATCH",
}


def write(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def snapshot(ref):
    sha = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], cwd=ROOT, text=True
    ).strip()
    data = subprocess.check_output(["git", "show", f"{sha}:{RANK_PATH}"], cwd=ROOT)
    return sha, {r["candidate_id"]: r for r in csv.DictReader(data.decode("utf-8").splitlines())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--updated-ref", help="Commit containing the updated Figure 1 rank table")
    parser.add_argument("--queue", type=Path, default=ROOT /
                        "download_raw/stage2_machine_screening/ORAC_Fulltext_Batches.csv")
    args = parser.parse_args()
    read = rank_builder.read
    profiles = {r["candidate_id"]: r for r in read(IDENTITY / "result/table/candidate_evidence_profiles.csv")}
    coverage = {r["candidate_id"]: r for r in read(IDENTITY / "result/table/01_candidate_report_coverage.csv")}
    first_sha, first = snapshot(BASELINE)
    current = {r["candidate_id"]: r for r in read(ROOT / RANK_PATH)}
    assert profiles.keys() == coverage.keys() == current.keys()

    observations = rank_builder.conditional_observations()
    counts = Counter(cid for cid, *_ in observations)
    observed_dois = defaultdict(set)
    for cid, doi, *_ in observations:
        observed_dois[cid].add(doi)
    held = defaultdict(list)
    for r in read(IDENTITY / "inputs/provenance/ORAC_Control_Observations_2026-11-23.csv"):
        held[r["candidate_id"]].append(r)
    scoped, pending = defaultdict(set), defaultdict(set)
    queue_available = args.queue.is_file()
    if queue_available:
        for r in read(args.queue):
            bucket = scoped if r["review_status"] in SCOPED else pending
            for cid in filter(None, r["candidate_ids"].split(";")):
                bucket[cid].add(r["article_key"])

    evidence = []
    for cid, r in current.items():
        source, profile, held_rows = coverage[cid], profiles[cid], held[cid]
        assert scoped[cid].isdisjoint(pending[cid])
        if queue_available:
            assert len(scoped[cid]) + len(pending[cid]) == int(source["orac_priority_name_reports"])
        assert observed_dois[cid] == set(filter(None, r["conditional_orac_dois"].split(";")))
        assert len(observed_dois[cid]) == int(r["conditional_orac_doi_reports"] or 0)
        evidence.append(dict(
            candidate_id=cid, compound=r["compound"], formula=profile["molecular_formula"],
            food_occurrence_status=profile["food_occurrence_status"],
            direct_name_report_links=source["direct_name_reports"],
            orac_priority_name_report_links=source["orac_priority_name_reports"],
            priority_name_links_with_scope_logged=len(scoped[cid]) if queue_available else "",
            priority_name_links_pending_scope=len(pending[cid]) if queue_available else "",
            conditional_model_observations=counts[cid],
            conditional_model_doi_reports=int(r["conditional_orac_doi_reports"] or 0),
            conditional_model_dois=r["conditional_orac_dois"],
            conditional_model_dois_with_typed_sd=int(r["typed_sd_doi_reports"] or 0),
            historical_confirmed_independent_horac_studies=r["historical_confirmed_independent_horac_studies"],
            new_extracted_observations_held=len(held_rows),
            new_held_dois=";".join(sorted({h["doi"] for h in held_rows})),
            new_held_dispositions=";".join(sorted({h["model_disposition"] for h in held_rows})),
            conditional_rank=r["conditional_rank"], rank_stability_status=r["validation_review_status"],
        ))
    assert counts.keys() <= profiles.keys() and held.keys() <= profiles.keys()

    update_sha, update = snapshot(args.updated_ref) if args.updated_ref else ("", {})
    if not args.updated_ref:
        assert first == current, "Current ranks changed; supply the committed updated rank table."
    assert not args.updated_ref or update_sha != first_sha
    comparison = []
    for cid in dict.fromkeys([*first, *update]):
        a, b = first.get(cid, {}), update.get(cid, {})
        old, new = a.get("conditional_rank", ""), b.get("conditional_rank", "")
        comparison.append(dict(
            candidate_id=cid, compound=(b or a)["compound"],
            first_commit=first_sha, first_rank=old,
            first_best_rank=a.get("best_rank_across_fits_and_deletions", ""),
            first_worst_rank=a.get("worst_rank_across_fits_and_deletions", ""),
            first_status=a.get("validation_review_status", ""),
            update_commit=update_sha, updated_rank=new,
            updated_best_rank=b.get("best_rank_across_fits_and_deletions", ""),
            updated_worst_rank=b.get("worst_rank_across_fits_and_deletions", ""),
            updated_status=b.get("validation_review_status", ""),
            updated_minus_first_rank=int(new) - int(old) if new and old else "",
            comparison_status=(
                "AWAITING_UPDATED_FIT" if not update_sha else
                "RANKED_IN_BOTH" if new and old else
                "NEWLY_RANKED" if new else
                "RANK_LOST" if old else "UNRANKED_IN_BOTH"
            ),
        ))
    write(TABLE / "05_compound_evidence_inclusion.csv", evidence)
    write(TABLE / "06_round_rank_comparison.csv", comparison)
    print(f"{len(evidence)} compounds, {sum(counts.values())} model observations, "
          f"{len(comparison)} comparison rows, queue available={queue_available}")


if __name__ == "__main__":
    main()
