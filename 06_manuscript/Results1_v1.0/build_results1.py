"""Generate Results 1 tables, figure input, and Results text from frozen analysis records."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODEL = ROOT / "03_candidate_selection/08_capacity_review_validation"


def readjson(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def readcsv(path):
    return list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))


def writecsv(path, rows):
    with path.open("w", encoding="utf8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE)
    output = parser.parse_args().out
    supp = output / "Supplementary_Materials"
    supp.mkdir(parents=True, exist_ok=True)
    d = readjson(HERE / "Evidence_Snapshot.json")
    variants = readjson(MODEL / "results/model_update_summary.json")["variants"]
    review = readjson(MODEL / "review_validation_summary.json")
    ridge = readjson(ROOT / "03_candidate_selection/01_activity_model/results/completed_model_summary.json")
    probes = readcsv(MODEL / "Top20_Conditional_Uncertainty.csv")
    prof = readcsv(ROOT / "02_identity_and_evidence/results/candidate_evidence_profiles.csv")
    discovery = readcsv(ROOT / "01_candidate_discovery/results/discovery_register.csv")
    numeric, ranked, panel = d["observations"], d["rankings"], d["panel"]
    assert len({r["source_id"] for r in numeric}) == len(numeric)
    assert all(r["doi"] and r["locator"] and r["unit"] for r in ranked)
    assert all(r["human_review_status"] == "NOT_REVIEWED" for r in panel)
    outcomes = Counter(r["tier"] for r in panel)
    fl = {r["candidate_id"] for r in ranked if r["assay"] == "ORAC-FL"}
    dois = {r["doi"] for r in numeric}
    dated = {scope: len({r["doi"] for r in numeric if r["date_scope"].startswith(scope)})
             for scope in ("Primary", "Evidence-gap", "Historical")}
    model_rows = []
    for item in variants:
        model_rows.append(dict(model=item["variant"], candidates=item["candidates"], doi_reports=item["papers"],
                               input_rows=item["candidate_rows"], scored_rows=item["heldout_rows"],
                               model_rmse=item["metrics"]["predicted_log_location"]["RMSE"],
                               baseline_rmse=item["metrics"]["baseline_log_location"]["RMSE"],
                               validation="Whole DOI held out; estimable outcomes only"))
    model_rows.append(dict(model="Single-source structure Ridge", candidates=ridge["n"], doi_reports=1,
                           input_rows=ridge["n"], scored_rows=ridge["n"], model_rmse=ridge["metrics"]["selected"]["RMSE"],
                           baseline_rmse=ridge["metrics"]["matched_null"]["RMSE"], validation="Nested scaffold holds"))
    columns = ("compound", "candidate_id", "formula", "family", "food_occurrence_evidence", "food_source_DOI",
               "methods", "representative_reported_value", "representative_unit", "representative_DOI",
               "distinct_comparison_reports", "independent_studies", "quality", "material_and_assay_gate",
               "tier", "rationale", "human_review_status")
    writecsv(output / "Table1.csv", [{k:r[k] for k in columns} for r in panel])
    for file, rows in (("TableS1_Candidate_Evidence.csv", panel), ("TableS2_Assay_Ranks.csv", ranked),
                       ("TableS3_Model_Validation.csv", model_rows), ("TableS4_Original_Observations.csv", numeric),
                       ("TableS5_Source_Deletion.csv", probes)):
        writecsv(supp / file, rows)
    fig_rows = [dict(panel="A", label=k, value=v) for k,v in
                [("Discovery records",len(discovery)),("Identity profiles",len(prof)),("FL comparison",len(fl))]]
    fig_rows += [dict(panel="B", label=r["assay"], value=r["ranked_rows"]) for r in d["methods"]]
    for r in model_rows:
        if r["model"] == "EXTENDED_UNKNOWN_PH_NAME_BASED":
            continue
        label = {"EXTENDED_CONFLICT_EXCLUDED":"Expanded DOI",
                 "CORE_REPORTED_PH74_37C":"Core DOI"}.get(r["model"],"Scaffold Ridge")
        fig_rows += [dict(panel="C",label=label+" / "+k,value=r[k+"_rmse"]) for k in ("model","baseline")]
    fig_rows += [dict(panel="D",label=k,value=outcomes[k]) for k in ("A","B","C")]
    writecsv(output/"Figure1_Data.csv",fig_rows)
    low = [r for r in probes if int(r["deletion_worst_position"]) <= 20]
    bounds = ", ".join(f"{r['compound']} {r['deletion_best_position']}-{r['deletion_worst_position']}" for r in low)
    shortlist = ", ".join(r["compound"] for r in panel if r["tier"] == "A")
    first = model_rows[1]
    results = f"""# Results 1. Literature-informed prioritization of food-derived antioxidant candidates

## 1.1 Discovery and evidence assembly

The discovery register contained {len(discovery)} entries and yielded {len(prof)} chemical profiles (Figure 1A). The targeted original-evidence release contained {len(numeric)} observations from {len(dois)} DOI-linked reports. Of these reports, {dated['Primary']} were in the primary-window stratum, {dated['Evidence-gap']} in the 2016-2019 evidence-gap extension, and {dated['Historical']} provided historical comparison. The report count describes the extraction overlay. Automated retrieval covered a broader corpus whose title, abstract and full-text screening remained incomplete. Study independence and experimental replication were retained as distinct fields (Table S4).

## 1.2 Assay-specific antioxidant activity

There were {len(ranked)} ranked observations in {len(d['blocks'])} within-source blocks, including conditional ORAC-FL comparisons for {len(fl)} compounds (Figure 1B and Table S2). A comparison block fixes the report, assay, reported protocol, unit and response direction. A block can include unresolved material or dose-scale conditions, which are carried with each observation. The same-source FL and PGR comparison showed substantial reordering, so no common scale was assigned across probes. Crocin lacked a qualified comparison panel.

## 1.3 Model validation and robustness

The expanded conditional FL model used {first['input_rows']} observations across {first['doi_reports']} DOI reports. On {first['scored_rows']} estimable held-out outcomes, log-scale RMSE was {first['model_rmse']:.3f}, compared with {first['baseline_rmse']:.3f} for the matched mean baseline (Figure 1C and Table S3). The single-paper structure Ridge had scaffold-held-out RMSE {model_rows[-1]['model_rmse']:.3f} versus {model_rows[-1]['baseline_rmse']:.3f} for the null. This experiment provides no independent-study evidence of structural transfer. Equal-row and DOI-balanced conditional top-20 sets shared {review['weighting_top20_overlap']} members. The three most consistently high candidates in the fixed component had source-deletion position bounds of {bounds} (Table S5). These bounds quantify sensitivity to sources, with sampling uncertainty unestimated.

## 1.4 Candidate priorities for aqueous verification

The study proposed {len(panel)} compounds for experimental consideration, comprising {outcomes['A']} first-priority, {outcomes['B']} exploratory and {outcomes['C']} deferred candidates (Figure 1D and Table 1). The initial qualification panel comprises {shortlist}. This selection spans flavanols, distinct phenolic acid chemistry, ascorbate and a reduced thiol. Eligibility for aqueous testing requires researcher review and qualification of the exact materials and assay conditions. The prioritization combines quantitative evidence, source reliability and expected assay suitability. It does not assign a pooled potency position.

## Supplementary results

Table S1 gives the full candidate evidence and rationale. Tables S2 and S4 retain the separation between ranked observations and all reviewed extraction rows. Table S3 reports model and baseline RMSE on defined estimable sets. Table S5 contains source-deletion position bounds for the conditional FL comparison. The two nominal-dose bridge analyses shared {review['dose_top20_overlap_equal_row']} and {review['dose_top20_overlap_equal_DOI']} top-20 members under equal-row and equal-DOI weights, respectively.
"""
    (output / "Results1.md").write_text(results, encoding="utf8")


if __name__ == "__main__":
    main()
