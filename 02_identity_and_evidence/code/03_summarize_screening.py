"""Summarize machine-assigned roles and evaluate quantitative selection readiness."""
import json
import math
from collections import Counter, defaultdict
from statistics import median

from importlib import import_module

screen = import_module("02_screen_public_snapshot")
AUDIT, TABLE, LOCAL, ROOT = screen.AUDIT, screen.TABLE, screen.LOCAL, screen.ROOT
rows, save = screen.rows, screen.save

REPORT_ROLES = {
    "ACTIVITY_QUANT_LEAD": "quantitative_activity",
    "ACTIVITY_METHOD_MENTION": "activity_method",
    "ANALYTICAL_DETECTION_LEAD": "chemical_detection",
    "FOOD_OCCURRENCE_LEAD": "food_occurrence",
    "CONDITION_OR_PROCESSING_LEAD": "conditions_or_processing",
}


def screen_qc():
    summary = json.loads((AUDIT/"Screening_Summary.json").read_text(encoding="utf-8"))
    report = rows(LOCAL/"Report_Screening.csv")
    links = rows(LOCAL/"Candidate_Report_Links.csv")
    sample = rows(LOCAL/"Recall_Audit_Sample.csv")
    keys = {r["article_key"] for r in report}
    assert len(keys) == len(report) == summary["provisional_intake_union"]
    assert len(links) == summary["candidate_report_links"] == len({
        (r["article_key"],r["candidate_id"]) for r in links
    })
    assert all(r["article_key"] in keys for r in links)
    assert all(r["automated_exclusion"] == "NO" and r["final_inclusion"] == "NOT_ADJUDICATED" for r in report)
    assert all(r["audit_outcome"] == "PENDING" for r in sample)
    assert summary["abstract_checked"] + summary["title_only"] + summary["no_title_or_abstract"] == len(report)
    assert len(sample) == summary["audit_sample_rows"]
    assert 500 == summary["local_wos_accessions"]
    assert 65248 == summary["pubmed_unique_pmids"]
    assert 62458 == summary["europe_pmc_route_keys"]
    results = Counter()
    for r in report:
        for role in r["evidence_role_leads"].split(";"):
            results[role] += 1
    by_candidate = defaultdict(Counter)
    for r in links:
        if r["association"] == "NAME_LEAD":
            by_candidate[r["candidate_id"]].update(r["evidence_role_leads"].split(";"))
    save(TABLE/"02_candidate_evidence_role_leads.csv",[
        dict(candidate_id=r["candidate_id"],compound=r["compound"],**{
            label:by_candidate[r["candidate_id"]][role] for role,label in REPORT_ROLES.items()
        }, status="TITLE_ABSTRACT_NAME_ASSOCIATION_ONLY")
        for r in rows(TABLE/"01_candidate_report_coverage.csv")
    ])
    summary["role_leads_nonexclusive"] = {label:results[role] for role,label in REPORT_ROLES.items()}
    summary["qc_status"] = "PASS_SNAPSHOT_INTEGRITY_ONLY"
    (AUDIT/"Screening_QC.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")


def readiness():
    data = rows(ROOT/"03_candidate_selection/result/table/audit/Ranking_and_Variability.csv")
    estimate = [float(r["between_DOI_adjusted_log_SD"]) for r in data if r["between_DOI_adjusted_log_SD"]]
    # Descriptive cohort benchmark. It is not an estimate of assay sampling variance.
    ref = median(estimate)
    output = []
    for r in data:
        n = int(r["doi_count"])
        sd = r["between_DOI_adjusted_log_SD"]
        stable_top20 = (
            n >= 2 and max(int(r[field]) for field in (
                "updated_doi","updated_cv","cv_stronger","cv_milder","cv_delete_one_worst",
                "parent_form_sensitivity","exclude_2025_calibration_pending"
            )) <= 20
        )
        output.append(dict(
            candidate_id=r["candidate_id"], compound=r["compound"],
            capacity_rank=int(r["updated_cv"]), doi_reports=n,
            typed_sd_doi_reports=r["typed_sd_DOIs"],
            loo_worst_rank=r["cv_delete_one_worst"],
            stable_capacity_gate="PASS" if stable_top20 else "NO",
            overall_sd_benchmark=ref, benchmark_compounds=len(estimate),
            adjusted_log_sd=sd,
            dispersion_ratio=float(sd)/ref if sd and ref > 0 else "",
            descriptive_dispersion_factor=1/(1+(float(sd)/ref)**2) if sd and ref > 0 else "",
            report_coverage_factor=1-math.exp(-n/3),
            scoring_status="PENDING_EXPERIMENT_INDEPENDENCE_AND_REPORT_QUALITY"
        ))
    save(ROOT/"03_candidate_selection/result/table/audit/Objective_Priority_Readiness.csv",sorted(output,key=lambda r:r["capacity_rank"]))


if __name__=="__main__":
    screen_qc()
    readiness()
