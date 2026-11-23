"""Reconcile a scoped full-text batch and test its effect on the connected ORAC model."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median, stdev
from importlib import import_module

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVENANCE = HERE.parent/"inputs/provenance"
PREVIOUS = PROVENANCE/"10_orac_evidence_increment"
IDENTITY = ROOT/"02_identity_and_evidence"
LOCAL = ROOT/"download_raw/stage2_machine_screening"
model = import_module("01_fit_orac_fl")
cv, fit, metrics_and_deletion = model.cv, model.fit, model.metrics_and_deletion
positions, read, np = model.positions, model.read, model.np
FOLLOWUP = PROVENANCE/"11_orac_fulltext_followup"


def write(path, rows):
    with path.open("w",encoding="utf-8",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def review_queue(reviews):
    old = read(IDENTITY/"03_date_scoped_review/results/Original_ORAC_Source_Progress.csv")
    earlier = {r["doi"].lower():r["progress"] for r in old if r["doi"]}
    increment = {r["doi"] for r in read(PREVIOUS/"Source_Review.csv")}
    reference = IDENTITY/"inputs/provenance/results1_v1.0/original_observations.csv"
    frozen = {r["doi"] for r in read(reference)}
    source = read(LOCAL/"Report_Screening.csv")
    routes = defaultdict(set)
    for r in read(LOCAL/"Candidate_Report_Links.csv"):
        if r["association"] == "NAME_LEAD":
            routes[r["article_key"]].add(r["candidate_id"])
    output = []
    batch_hits = {}
    for r in source:
        key, doi = r["article_key"], r["doi"].lower()
        if doi in reviews:
            batch_hits.setdefault(doi,set()).add(r["disposition"])
        if r["disposition"] != "HIGH_PRIORITY_ORAC_FULLTEXT":
            continue
        if doi in reviews:
            status = "SCOPED_REVIEW_THIS_BATCH"
        elif doi in increment or doi in frozen or earlier.get(doi) == "TARGETED_SOURCE_SCOPE_RECORDED":
            status = "REUSE_RECORDED_SCOPE"
        elif doi in earlier:
            status = "EXISTING_ACCESS_OR_SCOPE_QUEUE"
        else:
            status = "PENDING_NEW_SCOPE"
        candidates = routes[key]
        output.append(dict(article_key=key,doi=doi,title=r["title"],candidate_ids=";".join(sorted(candidates)),
                           names_linked=len(candidates),ascorbic_lead="AFF-0104" in candidates,
                           review_status=status,human_review_status="NOT_REVIEWED"))
    output.sort(key=lambda r:(r["review_status"],not r["ascorbic_lead"],-r["names_linked"],r["article_key"]))
    assert len(output) == 567
    write(LOCAL/"ORAC_Fulltext_Review_Queue.csv",output)
    return Counter(r["review_status"] for r in output), {k:sorted(v) for k,v in batch_hits.items()}


def harmonize(profiles, reviews):
    raw = read(FOLLOWUP/"Original_Observations.csv")
    assert len(raw) == len({r["id"] for r in raw})
    audit, blocks = [], defaultdict(list)
    for r in raw:
        review = reviews[r["doi"]]
        cid = r["candidate_id"]
        mw = profiles[cid]["molecular_weight_g_mol"] if cid else ""
        if r["raw_unit"] == "MOL_TE_PER_MOL":
            factor = 1.0
        else:
            assert r["raw_unit"] == "UMOL_TE_PER_MG"
            factor = float(mw)*.001 if mw else None
        mean = float(r["mean"])*factor if factor else None
        sd = float(r["sd"])*factor if factor else None
        audit.append(dict(**r,reference_mw=mw,conversion_factor=factor,mean_mol_te_per_mol=mean,
                          sd_mol_te_per_mol=sd,source_url=review["source_url"],
                          error_definition="SD",human_review_status="NOT_REVIEWED"))
        if factor:
            blocks[r["usage"]].append(dict(evidence_id=r["id"],candidate_id=cid,doi=r["doi"],
                mean=mean,reported_error=sd,error_type="SD",source_block=r["doi"]+"|TABLE_PURE_ORAC_FL"))
    write(model.TABLE/"02_harmonized_observations.csv",audit)
    return blocks


def predictions_on_prior_rows(training, targets):
    prediction = {}
    for doi in sorted({r["doi"] for r in targets}):
        train = [r for r in training if r["doi"] != doi]
        ids, matrix, _, beta = fit(train,"CV")
        null_space = np.eye(matrix.shape[1]) - np.linalg.pinv(matrix,rcond=1e-12)@matrix
        estimable = {cid:float(beta[j]) for j,cid in enumerate(ids)
                     if np.linalg.norm(null_space[:,j]) < 1e-8}
        for r in targets:
            if r["doi"] == doi and r["candidate_id"] in estimable:
                prediction[r["evidence_id"]] = estimable[r["candidate_id"]]
    return prediction


def ranking(base, conditional, protocol, profiles):
    compound_ids = {r["candidate_id"] for r in base}
    for block in (conditional,protocol):
        assert len({r["candidate_id"] for r in block}&compound_ids) >= 2
        assert {r["doi"] for r in block}.isdisjoint({r["doi"] for r in base})
    assert len({r["evidence_id"] for r in base+conditional+protocol}) == len(base+conditional+protocol)
    cv_values = [cv(r) for r in base+conditional+protocol if cv(r) is not None]
    q75 = float(np.quantile(cv_values,.75))
    data = {
        "prior":base,
        "plus_2021_conditionally":base+conditional,
        "plus_both_sensitivity":base+conditional+protocol,
        "only_add_2022_sensitivity":base+protocol,
    }
    ranks, diagnostics = {}, {}
    heldout = {r["evidence_id"]:np.log(float(r["mean"])) for r in base}
    prior_prediction = predictions_on_prior_rows(base,base)
    for label, cohort in data.items():
        ids, _, _, beta = fit(cohort,"CV")
        ranks[label] = positions(ids,beta[:len(ids)])
        if label == "plus_both_sensitivity":
            metrics, both_best, both_worst, both_missing = metrics_and_deletion(cohort, "CV", include_best=True)
        else:
            metrics, _ = metrics_and_deletion(cohort, "CV")
        diagnostics[label] = dict(rows=len(cohort),dois=len({r["doi"] for r in cohort}),
                                  compounds=len(ids),**metrics)
        prediction = predictions_on_prior_rows(cohort,base)
        common = sorted(prior_prediction.keys() & prediction.keys())
        diagnostics[label]["same_prior_test_rows"] = len(common)
        diagnostics[label]["same_prior_test_rmse"] = float(np.sqrt(np.mean([
            (prediction[key]-heldout[key])**2 for key in common
        ])))
        diagnostics[label]["prior_rmse_on_same_rows"] = float(np.sqrt(np.mean([
            (prior_prediction[key]-heldout[key])**2 for key in common
        ])))
    both = data["plus_both_sensitivity"]
    ids, matrix, y, beta = fit(both,"CV",q75)
    empirical = positions(ids,beta[:len(ids)])
    adjusted = y-matrix[:,len(ids):]@beta[len(ids):]
    grouped = defaultdict(list)
    for row,value in zip(both,adjusted):
        grouped[row["candidate_id"],row["doi"]].append(float(value))
    per_candidate = defaultdict(list)
    for (cid,_),values in grouped.items():
        per_candidate[cid].append(median(values))
    result = []
    for cid in ids:
        summaries = per_candidate[cid]
        result.append(dict(candidate_id=cid,compound=profiles[cid]["compound_name"],
            **{name:score.get(cid,"") for name,score in ranks.items()},
            empirical_cv_q75_sensitivity=empirical[cid],best_doi_deletion_both=both_best[cid],
            worst_doi_deletion_both=both_worst[cid],
            missing_in_any_doi_deletion_both="YES" if cid in both_missing else "NO",
            doi_reports_both=len(summaries),between_doi_adjusted_log_sd=stdev(summaries) if len(summaries)>=3 else "",
            status="EXPLORATORY"))
    return sorted(result,key=lambda r:r["plus_both_sensitivity"]),diagnostics,q75


def main():
    profiles = {r["candidate_id"]:r for r in read(IDENTITY/"result/table/candidate_evidence_profiles.csv")}
    reviews = {r["doi"]:r for r in read(FOLLOWUP/"Source_Review.csv")}
    counts, batch = review_queue(reviews)
    prior_path = model.TABLE/"01_connected_model_input.csv"
    signature = hashlib.sha256(prior_path.read_bytes()).hexdigest()
    prior = [dict(evidence_id=r["evidence_id"],candidate_id=r["candidate_id"],doi=r["doi"],
                  mean=r["mean_mol_te_per_mol"],reported_error=r["error_mol_te_per_mol"],
                  error_type=r["error_type"], source_block=r["source_block"]) for r in read(prior_path)]
    assert len(prior)==119
    blocks = harmonize(profiles,reviews)
    ranks, metrics, q75 = ranking(prior,blocks["CONDITIONAL"],blocks["PROTOCOL_SENSITIVITY"],profiles)
    write(model.TABLE/"03_rank_sensitivity.csv",ranks)
    prior_top20 = {r["compound"] for r in ranks if r["prior"] <= 20}
    top20_delta = {}
    for scenario in ("plus_2021_conditionally","plus_both_sensitivity","empirical_cv_q75_sensitivity"):
        top20 = {r["compound"] for r in ranks if r[scenario] <= 20}
        top20_delta[scenario] = dict(enter=sorted(top20-prior_top20),exit=sorted(prior_top20-top20))
    assert hashlib.sha256(prior_path.read_bytes()).hexdigest()==signature
    summary = dict(qc="PASS",reviewed_sources=len(reviews),priority_queue_status=counts,
                   queue_dispositions_by_reviewed_doi=batch,models=metrics,
                   top20_delta_against_prior=top20_delta,
                   empirical_cv_q75_descriptive=q75,prior_model_input_sha256=signature)
    (model.MODEL/"02_whole_doi_validation.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
