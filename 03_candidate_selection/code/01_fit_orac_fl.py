"""Refit a separate conditional ORAC-FL evidence increment with reproducible weights."""
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median, stdev
import sys

HERE = Path(__file__).resolve().parent
TABLE = HERE.parent / "result/table"
AUDIT = TABLE / "audit"
MODEL = HERE.parent / "result/model"
BASE = HERE.parent / "08_capacity_review_validation"
sys.path.insert(0, str(HERE.parent / "06_verified_source_update"))
from fit_verified_source_diagnostics import design, fit_shrunk_paper_effects, np

SD_TYPES = {"SD", "SD_TRIPLICATE_EXPERIMENTS"}


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def export(name, rows):
    path = TABLE / name if name == "01_connected_model_input.csv" else AUDIT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize(r):
    factor = {"MOLAR_TE": 1, "UMOL_TE_PER_G": 1e-6, "MMOL_TE_PER_G": 1e-3}.get(r["unit"])
    if factor is None:
        return None, None
    if r["unit"] != "MOLAR_TE":
        factor *= float(r["molecular_weight"])
    mean = factor * float(r["mean"])
    error = factor * float(r["error"]) if r["error"] else None
    if not math.isfinite(mean) or mean <= 0 or (error is not None and (error < 0 or not math.isfinite(error))):
        raise ValueError(r["evidence_id"])
    return mean, error


def cv(r):
    if r["error_type"] in SD_TYPES and r["reported_error"]:
        return float(r["reported_error"]) / float(r["mean"])
    return None


def dispersion_multiplier(relative_sd, scale):
    return max(.10, 1 / (1 + (relative_sd / scale)**2)) if relative_sd is not None else 1


def weights(rows, mode, scale=.25):
    count = Counter(r["doi"] for r in rows)
    values = []
    for r in rows:
        relative_sd = cv(r)
        penalty = dispersion_multiplier(relative_sd, scale) if mode == "CV" else 1
        values.append(penalty / count[r["doi"]] if mode != "ROW" else 1)
    return np.asarray(values) / np.mean(values)


def fit(rows, mode, scale=.25):
    ids = sorted({r["candidate_id"] for r in rows})
    matrix = design(rows, ids, sorted({r["source_block"] for r in rows}))
    y = np.log([float(r["mean"]) for r in rows])
    w = np.sqrt(weights(rows, mode, scale))
    coeff = fit_shrunk_paper_effects(matrix * w[:,None], y * w, len(ids), 10)
    return ids, matrix, y, coeff


def positions(ids, locations):
    return {cid: 1 + sum(value > locations[i]+1e-10 for value in locations)
            for i,cid in enumerate(ids)}


def metrics_and_deletion(rows, mode, *, include_best=False):
    errors, simple = [], []
    universe = {r["candidate_id"] for r in rows}
    worst = dict.fromkeys(universe, 1)
    best = dict.fromkeys(universe, len(universe))
    missing = set()
    for doi in sorted({r["doi"] for r in rows}):
        train = [r for r in rows if r["doi"] != doi]
        ids, matrix, y, beta = fit(train, mode)
        residual_projection = np.eye(matrix.shape[1]) - np.linalg.pinv(matrix, rcond=1e-12) @ matrix
        for cid in universe:
            if cid not in ids:
                worst[cid] = len(universe)
                best[cid] = 1
                missing.add(cid)
                continue
            j = ids.index(cid)
            comparable = [k for k in range(len(ids))
                          if np.linalg.norm(residual_projection[:,j]-residual_projection[:,k])<1e-8]
            lower = sum(beta[j]-beta[k]>1e-10 for k in comparable)
            worst[cid] = max(worst[cid],len(universe)-lower)
            if include_best:
                higher = sum(beta[k]-beta[j]>1e-10 for k in comparable)
                best[cid] = min(best[cid], 1+higher)
        for r in rows:
            cid = r["candidate_id"]
            if r["doi"] != doi or cid not in ids:
                continue
            j = ids.index(cid)
            if np.linalg.norm(residual_projection[:,j]) >= 1e-8:
                continue
            target = math.log(float(r["mean"]))
            errors.append((target-beta[j])**2)
            simple.append((target-np.mean([v for v,t in zip(y,train) if t["candidate_id"]==cid]))**2)
    metrics = dict(scored=len(errors),rmse=float(np.sqrt(np.mean(errors))),
                   matched_baseline=float(np.sqrt(np.mean(simple))))
    if include_best:
        return metrics, best, worst, missing
    return metrics, worst


def main():
    raw = read(BASE/"results/Analysis_Data_and_Dispositions.csv")
    baseline = [r for r in raw if r["extended_conflict_excluded_diagnostic"]=="YES"]
    provenance = {r["evidence_id"]:r for r in read(BASE/"Capacity_Row_Review.csv")}
    additions, sensitivity, audit = [], [], []
    for r in read(HERE.parent/"inputs/provenance/10_orac_evidence_increment/Extracted_Observations.csv"):
        mean, error = normalize(r)
        audit.append(dict(**r, molar_mean=mean, molar_reported_error=error, human_review_status="NOT_REVIEWED"))
        if r["disposition"] not in {"CONDITIONAL","FORM_SENSITIVITY"}:
            continue
        row = dict(evidence_id=r["evidence_id"], candidate_id=r["candidate_id"], doi=r["doi"],
                   mean=mean, reported_error=error if error is not None else "", error_type=r["error_type"],
                   source_block=r["doi"]+"|"+r["protocol"], numeric_locator=r["locator"])
        (additions if r["disposition"]=="CONDITIONAL" else sensitivity).append(row)
    assert len(baseline)==113 and len({r["doi"] for r in baseline})==11
    assert not ({r["doi"] for r in baseline} & {r["doi"] for r in additions})
    rows = baseline+additions
    assert len({r["evidence_id"] for r in rows})==len(rows)
    assert len({(r["candidate_id"],r["source_block"]) for r in rows})==len(rows)
    assert {r["candidate_id"] for r in additions+sensitivity} <= {r["candidate_id"] for r in baseline}
    export("Harmonized_New_Observations.csv",audit)
    export("01_connected_model_input.csv", [dict(evidence_id=r["evidence_id"],candidate_id=r["candidate_id"],
            doi=r["doi"],source_block=r["source_block"],mean_mol_te_per_mol=r["mean"],
            error_mol_te_per_mol=r["reported_error"],error_type=r["error_type"],locator=r["numeric_locator"],
            baseline_raw_mean=provenance.get(r["evidence_id"],{}).get("raw_mean",""),
            baseline_raw_unit=provenance.get(r["evidence_id"],{}).get("raw_units",""),
            source_set="INCREMENT" if r in additions else "V1_BASELINE",human_review_status="NOT_REVIEWED")
            for r in rows])
    scenarios = [
        ("baseline",baseline,"ROW",.25),("updated_row",rows,"ROW",.25),("updated_doi",rows,"DOI",.25),
        ("updated_cv",rows,"CV",.25),("cv_stronger",rows,"CV",.15),("cv_milder",rows,"CV",.40),
        ("parent_form_sensitivity",rows+sensitivity,"CV",.25),
        ("exclude_2025_calibration_pending",baseline+[r for r in additions if not r["evidence_id"].startswith("SAD")],"CV",.25),
    ]
    ranks = {}
    for label, data, mode, threshold in scenarios:
        ids, matrix, y, coeff = fit(data,mode,threshold)
        ranks[label]=positions(ids,coeff[:len(ids)])
    validation = {}
    for label, data, mode in [(s[0],s[1],s[2]) for s in scenarios[:4]]:
        validation[label], bounds = metrics_and_deletion(data,mode)
        if label=="updated_cv":
            cv_worst=bounds
    for r, w in zip(rows,weights(rows,"CV")):
        r["applied_cv"]=cv(r)
        r["weight"]=w
    export("Observation_Weights.csv",[dict(evidence_id=r["evidence_id"],doi=r["doi"],candidate_id=r["candidate_id"],
            error_type=r["error_type"],relative_SD=r["applied_cv"],
            dispersion_multiplier=dispersion_multiplier(r["applied_cv"],.25),doi_cv_weight=r["weight"])
            for r in rows])
    ids, matrix, y, beta = fit(rows,"CV")
    adjusted = y - matrix[:,len(ids):] @ beta[len(ids):]
    by_study = defaultdict(list)
    by_study_cv = defaultdict(list)
    for r,v in zip(rows,adjusted):
        key=(r["candidate_id"],r["doi"])
        by_study[key].append(float(v))
        if r["applied_cv"] is not None:
            by_study_cv[key].append(r["applied_cv"])
    names = {r["candidate_id"]:r["compound_name"] for r in read(HERE.parents[1]/"02_identity_and_evidence/result/table/candidate_evidence_profiles.csv")}
    output=[]
    for cid in sorted(ids,key=lambda cid:ranks["updated_cv"][cid]):
        values = [median(v) for (c,d),v in by_study.items() if c==cid]
        cvs = [median(v) for (c,d),v in by_study_cv.items() if c==cid]
        output.append(dict(candidate_id=cid,compound=names[cid],doi_count=len(values),
            median_relative_SD_by_DOI=median(cvs) if cvs else "",typed_sd_DOIs=len(cvs),
            min_doi_relative_SD=min(cvs) if cvs else "",max_doi_relative_SD=max(cvs) if cvs else "",
            between_DOI_adjusted_log_SD=stdev(values) if len(values)>=3 else "",
            cv_delete_one_worst=cv_worst[cid],**{label:r[cid] for label,r in ranks.items()}))
    export("Ranking_and_Variability.csv",output)
    strong = [r["compound"] for r in output if r["doi_count"]>=2 and
              max(r["updated_row"],r["updated_doi"],r["updated_cv"],r["cv_delete_one_worst"])<=20]
    summary = dict(base_rows=len(baseline), updated_rows=len(rows), updated_dois=len({r["doi"] for r in rows}),
                   typed_sd_rows=sum(r["applied_cv"] is not None for r in rows),
                   high_relative_sd_rows=sum(r["applied_cv"] is not None and r["applied_cv"]>=.25 for r in rows),
                   comparison=validation, provisional_shortlist=strong, stage1_snapshot_replaced=False)
    MODEL.mkdir(parents=True, exist_ok=True)
    (MODEL/"01_orac_fl_fit_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf8")
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
