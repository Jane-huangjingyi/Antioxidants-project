"""Read-only source audit and scenario simulation for Stage25B.6A.

Writes new diagnostic assets only. It never modifies Stage25B.5 frozen inputs.
"""
import csv
import hashlib
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/h_orac_stage25b/stage25b6a"
DOC = ROOT / "docs/qc/stage25b6a"
SYNC = ROOT / "docs/sync"
DATE = "2026-10-09"
CURRENT_YEAR = 2026

def read(rel):
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def doc(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")

def number(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None

def year(s):
    n = number(s)
    return int(n) if n is not None and n.is_integer() and 1900 <= n <= CURRENT_YEAR else None

ev = read("data/h_orac_stage25b/Stage25B_HORAC_Experiment_Evidence.csv")
rank = read("data/h_orac_stage25b/Stage25B_HORAC_Quantitative_Ranking.csv")
summ = {r["candidate_id"]:r for r in read("data/h_orac_stage25b/Stage25B_HORAC_Candidate_Summary.csv")}
master = read("data/literature_screening/master/Literature_Screening_Candidate_Master.csv")
master_by_id = {r["candidate_id"]:r for r in master}
pub = read("data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv")
retrieval = {r["candidate_id"]:r for r in read("data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv")}
frozen = read("data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv")
vitlock = read("data/candidate_universe/Vitamin_Phase3_Eligibility_Lock.csv")
vce = read("data/class_specific_antioxidant/VitaminC_Aqueous_Evidence_Master.csv")

assert len(ev)==74 and len(rank)==28 and len(master)==157 and len(frozen)==20 and len(retrieval)==47
assert [r["candidate_id"] for r in rank[:20]]==[r["candidate_id"] for r in frozen]
assert Counter(r["H_ORAC_tier"] for r in ev)=={"A":7,"B1":61,"B2":4,"X":2}
eligible = [r for r in ev if r["H_ORAC_tier"] in ("A","B1") and r["eligibility_status"]=="PRIMARY_RANKING_ELIGIBLE"]
assert len(eligible)==68
by_candidate=defaultdict(list)
for r in eligible:by_candidate[r["candidate_id"]].append(r)

# DOI counts are publication proxies. The source table does not supply verified study IDs.
independence=[]
for r in ev:
    cid=r["candidate_id"]
    independence.append({
        "experiment_id":r["independent_experiment_id"],"candidate_id":cid,"candidate_name":r["canonical_name"],
        "DOI":r["DOI"],"source_id":r["publication_id"],"study_id":"",
        "distinct_DOI_candidate_N":len({x["DOI"] for x in by_candidate[cid] if x["DOI"]}),
        "study_independence":"UNCLEAR","experiment_independence":"UNCLEAR",
        "source_independence_field":r["independence_status"],
        "replicate_type":"UNCLEAR","replicate_N_as_reported":r["replicate_N"],
        "original_value":r["raw_reported_value"],"original_unit":r["raw_unit"],
        "normalized_value_mol_TE_per_mol":r["converted_value_mol_TE_per_mol"],
        "SD_as_stored":r["SD"],"SE_as_stored":r["SE"],"CI_as_stored":r["CI"],"tier":r["H_ORAC_tier"],
        "primary_eligible":"yes" if r in eligible else "no",
        "source_location":"; ".join(x for x in [r["source_page"],r["source_table"],r["source_figure"]] if x),
        "provenance_status":r["provenance_status"],
        "interpretation":"Experiment ID or distinct DOI is not proof of independent research execution."
    })
write(DATA/"Stage25B6A_Evidence_Independence_Audit.csv",independence)

# Existing SD/SE are preserved as source fields. The 2023 Table 3 ± values are
# separately noted because that table does not label the displayed dispersion type.
reported_pm={"quercetin":"1.32","caffeic acid":"0.69","gallic acid":"0.06"}
error_rows=[]
for r in eligible:
    pm = reported_pm.get(r["canonical_name"].lower(),"") if r["DOI"]=="10.3390/antiox12020505" else ""
    has_error=bool(r["SD"].strip() or r["SE"].strip() or r["CI"].strip() or pm)
    error_rows.append({
        "candidate_id":r["candidate_id"],"candidate_name":r["canonical_name"],
        "experiment_id":r["independent_experiment_id"],"DOI":r["DOI"],"study_id":"",
        "HORAC_value":r["raw_reported_value"],"original_unit":r["raw_unit"],
        "normalized_value_mol_TE_per_mol":r["converted_value_mol_TE_per_mol"],
        "error_type":"SD_IN_CANONICAL" if r["SD"] else ("SE_IN_CANONICAL" if r["SE"] else ("CI_IN_CANONICAL" if r["CI"] else ("UNSPECIFIED_PLUS_MINUS_IN_ORIGINAL" if pm else "NOT_REPORTED_IN_CANONICAL"))),
        "SD":r["SD"],"SE":r["SE"],"CI_lower":"","CI_upper":"","CI_level":"",
        "original_plus_minus_unclassified":pm,
        "technical_replicate_N":"","biological_replicate_N":"","independent_experiment_N":"",
        "replicate_N_as_reported":r["replicate_N"],
        "error_reported":"yes" if has_error else "not confirmed",
        "error_extractable":"yes_type_unresolved" if pm else ("yes" if r["SD"] or r["SE"] or r["CI"] else "not established"),
        "error_source_location":"Table 3, TE_AUC" if pm else (r["source_table"] if has_error else ""),
        "error_provenance_status":"ORIGINAL_ARTICLE_TABLE_3_VERIFIED_TYPE_UNCLEAR" if pm else (r["provenance_status"] if has_error else "NOT_EXTRACTED"),
        "source_path":"https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/" if pm else "data/h_orac_stage25b/Stage25B_HORAC_Experiment_Evidence.csv",
        "independence_status":"UNCLEAR",
        "CI_status":"CI_NOT_ESTIMABLE"
    })
write(DATA/"Stage25B6A_HORAC_Error_Data_Audit.csv",error_rows)

uncertainty=[]
for rr in rank:
    cid=rr["candidate_id"]; q=by_candidate[cid]; es=[x for x in error_rows if x["candidate_id"]==cid]
    vals=[float(x["converted_value_mol_TE_per_mol"]) for x in q]
    sn=summ[cid]
    error_n=sum(x["error_reported"]=="yes" for x in es)
    uncertainty.append({
        "original_rank":rr["rank"],"candidate_id":cid,"candidate_name":rr["canonical_name"],
        "quantitative_record_N":len(q),"distinct_DOI_publication_proxy_N":len({x["DOI"] for x in q}),
        "confirmed_independent_study_N":"","study_independence":"INDEPENDENCE_UNRESOLVED",
        "SD_record_N":sum(bool(x["SD"]) for x in es),"SE_record_N":sum(bool(x["SE"]) for x in es),
        "CI_record_N":sum(bool(x["CI_lower"] or x["CI_upper"]) for x in es),
        "unclassified_plus_minus_record_N":sum(bool(x["original_plus_minus_unclassified"]) for x in es),
        "any_reported_error_record_N":error_n,
        "error_coverage_fraction":round(error_n/len(q),6),
        "between_record_median_mol_TE_per_mol":statistics.median(vals),
        "IQR_canonical":sn["IQR"] if len(q)>=2 else "NOT_APPLICABLE_SINGLE_RECORD",
        "range_min":min(vals),"range_max":max(vals),
        "heterogeneity_flag":rr["heterogeneity_flag"],"existing_confidence":rr["evidence_confidence"],
        "CI_status":"CI_NOT_ESTIMABLE","rank_uncertainty":"UNQUANTIFIED",
        "note":"One record cannot estimate between-study heterogeneity." if len(q)==1 else "Distinct DOI count is not confirmed independent-study count."
    })
write(DATA/"Stage25B6A_Candidate_Uncertainty_Summary.csv",uncertainty)

# Included Stage25A records already reconcile to each candidate's metadata-deduplicated count.
pub_by=defaultdict(list)
for r in pub:
    if r["include_primary_metric"]=="yes":pub_by[r["candidate_id"]].append(r)
history=[]
for m in master:
    cid=m["candidate_id"]; q=pub_by[cid]
    years=[year(x["year"]) for x in q]; years=[x for x in years if x is not None]
    eq=by_candidate[cid]; ey=[year(x["year"]) for x in eq]; ey=[x for x in ey if x is not None]
    earliest=year(m["first_antioxidant_publication_year"])
    latest=year(m["latest_antioxidant_publication_year"])
    if earliest is None and years:earliest=min(years)
    if latest is None and years:latest=max(years)
    history.append({
        "candidate_id":cid,"canonical_name":m["canonical_name"],"Stage25A_rank":m["primary_rank"],
        "earliest_original_publication_year":earliest or "",
        "latest_original_publication_year":latest or "",
        "research_span_years":latest-earliest+1 if earliest and latest and latest>=earliest else "",
        "metadata_deduplicated_publication_N":m["metadata_deduplicated_original_publication_N"],
        "recent_5_year_publication_N_2022_2026":sum(2022<=x<=2026 for x in years),
        "Stage25A_source_recent_5y_publication_N":m["recent_5y_publication_N"],
        "recent_10_year_publication_N_2017_2026":sum(2017<=x<=2026 for x in years),
        "independent_HORAC_study_N":"","study_independence_status":"INDEPENDENCE_UNRESOLVED" if eq else "NO_PRIMARY_RECORD",
        "distinct_HORAC_DOI_publication_proxy_N":len({x["DOI"] for x in eq}),
        "eligible_HORAC_quantitative_record_N":len(eq),
        "first_HORAC_publication_year":min(ey) if ey else "",
        "latest_HORAC_publication_year":max(ey) if ey else "",
        "history_source":"data/literature_screening/master/Literature_Screening_Candidate_Master.csv; data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv",
        "history_QC":"SOURCE_LATEST_YEAR_FUTURE_OR_INVALID" if year(m["latest_antioxidant_publication_year"]) is None and m["latest_antioxidant_publication_year"] else "STAGE25A_METADATA_NOT_STUDY_COUNT"
    })
assert len(history)==157
write(DATA/"Stage25B6A_Research_History_Indicators.csv",history)

vitamin=[]
for v in vitlock:
    cid=v["candidate_id"]
    m=master_by_id.get(cid)
    aq=next((x for x in read("data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv") if x["InChIKey"]==v["InChIKey"]),None)
    q=[x for x in ev if x["candidate_id"]==cid]
    vc=[x for x in vce if x["compound"]=="L-Ascorbic acid"] if cid=="AFF-0104" else []
    vitamin.append({
        "candidate_id":cid,"vitamin_form":v["compound"],"in_157_universe":"yes" if m else "no",
        "in_aqueous_master":"yes" if aq else "no",
        "Stage25A_rank":m["primary_rank"] if m else "",
        "Stage25A_Top50":m["Top50_primary"] if m else "no",
        "in_Stage25B_retrieval_set":"yes" if cid in retrieval else "no",
        "retrieval_decision":retrieval[cid]["retrieval_decision"] if cid in retrieval else "",
        "exclusion_or_nonentry_step":("Stage25B canonical adjudication/consolidation gap" if cid=="AFF-0104" else ("Stage25A Top50/applicability" if m and m["Top50_primary"]!="yes" else "not in 157 aqueous candidate universe")),
        "stage25B_eligibility":m["stage25B_ORAC_eligibility"] if m else "out_of_universe",
        "historical_original_HORAC_record_N":len(vc),
        "historical_original_DOIs":";".join(x["DOI"] for x in vc),
        "historical_original_values_units":";".join(x["original_value"]+" "+x["original_unit"] for x in vc),
        "historical_evidence_tiers":";".join(x["tier"] for x in vc),
        "historical_distinct_DOI_publication_proxy_N":len({x["DOI"] for x in vc}),
        "confirmed_independent_study_N":"",
        "unit_conversion_status":"direct mol TE/mol; no conversion required" if vc else "not established",
        "historical_HORAC_median_mol_TE_per_mol":statistics.median(float(x["normalized_value"]) for x in vc) if vc else "",
        "canonical_Stage25B_record_N":len(q),
        "canonical_Stage25B_A_B1_N":sum(x["H_ORAC_tier"] in ("A","B1") for x in q),
        "canonical_HORAC_rank":"not_rankable" if cid not in {x["candidate_id"] for x in rank} else next(x["rank"] for x in rank if x["candidate_id"]==cid),
        "construct_compatibility":"historical H-ORAC-FL compatible; canonical re-adjudication required" if vc else ("lipid-phase primary; aqueous H-ORAC comparability not established" if "Tocopher" in v["compound"] or "Tocotrienol" in v["compound"] else "not established"),
        "form_solubility_caveat":v["hold_reason"] or v["notes"],
        "method_interference_status":"historical assay QC in source master; re-adjudication pending" if vc else "not established for aqueous H-ORAC-FL",
        "source_path":"data/class_specific_antioxidant/VitaminC_Aqueous_Evidence_Master.csv" if vc else "data/candidate_universe/Vitamin_Phase3_Eligibility_Lock.csv",
        "status":"HISTORICAL_B1_NOT_IN_CANONICAL_STAGE25B" if vc else "NO_CANONICAL_A_B1_HORAC_RECORD"
    })
write(DATA/"Stage25B6A_Vitamin_Eligibility_and_HORAC_Audit.csv",vitamin)

eligible_n2=[r for r in rank if int(r["independent_eligible_experiment_N"])>=2]
scenario=[]
for r in rank:
    cid=r["candidate_id"]; n=int(r["independent_eligible_experiment_N"])
    doi_n=len({x["DOI"] for x in by_candidate[cid]})
    scenario.append({
        "original_rank":r["rank"],"candidate_id":cid,"candidate":r["canonical_name"],
        "original_HORAC_mol_TE_per_mol":r["median_H_ORAC_mol_TE_per_mol"],
        "experiment_N_as_labeled":n,"distinct_DOI_publication_proxy_N":doi_n,
        "confirmed_independent_study_N":"",
        "scenario_0_membership":"YES" if int(r["rank"])<=20 else "NO",
        "scenario_1_membership":"YES" if r in eligible_n2[:20] else "NO",
        "scenario_1_simulated_rank":eligible_n2.index(r)+1 if r in eligible_n2 else "",
        "scenario_2_membership":"INDETERMINATE" if doi_n>=2 else "NO_ON_AVAILABLE_RECORDS",
        "reason_for_exclusion":"single quantitative record under scenario 1; fewer than two distinct source DOIs" if n==1 else "independent-study status unverified under scenario 2",
        "reason_for_inclusion":"at least two A/B1 quantitative records in distinct DOIs; median/order unchanged" if n>=2 else "frozen v1.0 only",
        "uncertainty_flag":"INDEPENDENCE_UNRESOLVED;CI_NOT_ESTIMABLE",
        "scenario_2_interpretation":"Distinct DOI is a publication proxy, not proof of independent original studies."
    })
assert len(eligible_n2)==19
write(DATA/"Stage25B6A_Top20_Revision_Scenarios.csv",scenario)

frozen_hash=hashlib.sha256((ROOT/"data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv").read_bytes()).hexdigest()
source_manifest=read("data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv")
assert frozen_hash==next(x["sha256"] for x in source_manifest if x["asset_path"].endswith("Stage25B_Frozen_Primary_HORAC_Top20.csv"))
assert len(vce)==2 and [float(x["normalized_value"]) for x in vce]==[0.95,0.53]

one_top=[x["canonical_name"] for x in frozen if x["eligible_A_B1_N"]=="1"]
added=[x["canonical_name"] for x in eligible_n2 if int(x["rank"])>20]
sd_n=sum(bool(x["SD"]) for x in error_rows)
error_n=sum(x["error_reported"]=="yes" for x in error_rows)
future_n=sum(x["history_QC"]=="SOURCE_LATEST_YEAR_FUTURE_OR_INVALID" for x in history)

doc(DOC/"Stage25B6A_Confidence_Framework_v1.1_DRAFT_CN.md",f"""
# Confidence Framework v1.1 DRAFT

现行 Stage25B v2.0 将 eligibility、A/B1/B2 及 High/Moderate/Low 分开，但现有 confidence 未系统纳入经核实的独立研究数量、实验精度覆盖及排名不确定性。本草案不改变 canonical rubric 或 Frozen Top20 v1.0。

拟议框架先保留五个独立判断：**eligibility** 决定哪些记录进入 A+B1；**effect magnitude** 是这些记录的中位 H-ORAC；**evidence confidence** 评价独立来源、重复、precision、assay comparability 和异质性；**ranking uncertainty** 报告名次稳定性；**research maturity** 单独展示 Stage25A 历史与出版密度。不得相乘、加权或合并为一个总分。

| 维度 | 现有规则/数据 | v1.1 拟议规则 | 原因及预期影响 |
|---|---|---|---|
| 独立来源 | `independent_experiment_id`，但无验证 study ID | 先核实研究团队、实验批次和数据复用；至少 2 项独立原始研究才考虑高置信度 | 当前 28 种的 study N 均不能被证实，故不能直接按 DOI 升级 confidence |
| 重复与精度 | 68 条 A/B1 中仅 {sd_n} 条有 canonical SD；CI 为 0 | 原文逐项提取 replicate type、n、SD/SE/CI 及所在位置；缺失记 unknown | 缺失误差不等于零；排名 precision 暂不可量化 |
| 异质性 | canonical IQR/range/flag | N≥2 时报告跨记录分布；单记录记不可估计；研究间分布须以核实独立研究为单位 | 防止把技术重复当成跨研究稳定性 |
| 方法可比性 | Rubric v2.0 A/B1/B2 | 保持 eligibility 不变，confidence 另记录 assay protocol 差异 | 不因排名变化回调 tier |
| 研究历史 | Stage25A metadata count/first-last year | 作为独立画像与导师汇报列，不自动进入 H-ORAC 排名 | 历史长度与化学效力不同 |

拟议 High：至少两项经确认独立研究、可审计 precision 和可接受的方法一致性，且无无法解释的重大异质性；Moderate：至少两项确认独立研究但 precision 或一致性存在报告缺口；Low/Uncertain：单一来源或来源独立性尚未确认。阈值和类别名称均须研究者审批，不得在本轮回写现有 confidence。若另设最低门槛，当前 v1.0 的 Rosmarinic acid、Daidzein、Fisetin、Hesperidin、Naringin 首先受影响；按记录 N≥2 顺延后仅 19 种，不能凑足 Top20。正式 v1.1 修订须先发 CHANGE REQUEST 并批准 unfreeze/version update。
""")

doc(DOC/"Stage25B6A_Vitamin_C_Case_Report_CN.md",f"""
# Vitamin C 个案：为何未进入 Frozen H-ORAC Top20

L-Ascorbic acid 是 157 种候选物之一（AFF-0104），Stage25A 排名第 2，进入 Top50 与 47 种 Stage25B retrieval set，决定为 `include_ready`。它不是在研究基础筛选或 H-ORAC applicability QC 阶段被排除。当前 Stage25B candidate summary 对其记录 346 条 screen、0 条 full text assessed、0 条 canonical A/B1，故无 canonical primary rank。180 条仍为 pending prioritized full-text adjudication，不能据此推定无原始证据。

既有分类证据主表逐篇记录两项原始 H-ORAC-FL B1：Ou 等（2001，DOI 10.1021/jf010586o，Table 4 p.4622）为 0.95 mol TE/mol；Carvalho 等（2023，DOI 10.3390/antiox12020505，Table 3）为 0.53 mol TE/mol。两值中位数 0.74 mol TE/mol，分别来自不同原始论文。2023 原文 Table 3 将 AUC 法值列为 **0.53 ± 0.03**，但该表未明确标识 ± 的统计量类型，不能直接录为 SD、SE 或 95%CI。2001 原文位置与数值由既有项目证据表标记为“original paper and exact table location verified”；本轮未取得可直接复核该表图像的开放全文，因此保留该来源验证状态并建议定点复核。两条分类证据尚未迁移到 Stage25B canonical 74 条实验表；本轮不修改该表或排名。

以现有 28 种 canonical rankable candidates 比较，0.74 低于第 28 名 Gallic acid 的 1.25 mol TE/mol。因此，即使将历史两值在未来通过 v2.0 逐项复核并纳入，它也不会因当前中位数直接进入 Top20；但不得在未经 re-adjudication 和 change control 的情况下写入正式排名。VC 的 H-ORAC 化学容量、体内抗氧化作用及营养重要性属于不同构念。Dehydroascorbic acid 为另一个候选（AFF-0105，Stage25A 第 70），不能与 L-ascorbic acid 合并。自然 tocopherol/tocotrienol 在项目维生素锁定表中属于 lipid-phase panel；本轮无可比的 canonical aqueous H-ORAC A/B1 证据，不能为了导师问题临时改变水相纳入规则。

原始来源：Ou 等，[DOI 10.1021/jf010586o](https://doi.org/10.1021/jf010586o)；Carvalho 等，[原始全文 Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)。本地逐条记录：`data/class_specific_antioxidant/VitaminC_Aqueous_Evidence_Master.csv`；当前 canonical 状态：`data/h_orac_stage25b/Stage25B_HORAC_Candidate_Summary.csv`。
""")

method_table="""| 方法 | 数据需求及当前满足程度 | 结论 |
|---|---|---|
| 经确认独立研究 N≥2 | study ID、数据复用核查；当前未满足 | 推荐作为正式修订候选，先完成来源独立性审计 |
| IQR/range | 至少 2 个可比定量记录；19/28 满足记录数 | 推荐描述性报告；不可称 95%CI |
| 实验间 CV | ≥2 个可比、独立且具有适当尺度的估计；研究独立性未知 | 暂不推荐作为跨研究 precision 指标 |
| Bootstrap median CI | 经验证独立研究的原始估计，足够研究数；当前不足 | 不计算；两研究 bootstrap 不能弥补稀疏证据 |
| Random-effects meta-analysis | 每研究 effect/SE 与可比性、足够研究数；多数无误差 | 当前不执行；k=2 异质性极不稳定 |
| Leave-one-study-out | 至少 3 项经验证独立研究较有解释力；当前未知 | 定点复核后可做诊断，当前不可正式估计 |
| Rank stability | 研究级重抽样或合理误差模型；当前无 | 仅可做规则门槛情景模拟，不给概率 |
| Prediction interval | 稳定异质性估计及足够研究数；当前无 | 不估计 |"""

decision_table="""| 决策 | recommended_option | evidence_basis | remaining_uncertainty | impact_if_approved |
|---|---|---|---|---|
| D1 最低门槛 | 优先审查 ≥2 独立原始研究；N≥2 记录仅作过渡诊断 | 当前 9/28 仅一记录，19/28 有≥2记录 | study ID 均未核实 | 会触发 v1.1 change request；不能自动凑足20 |
| D2 95%CI | 当前不计算，标 CI_NOT_ESTIMABLE | 68 条 A/B1 的 error/replicate 结构不足 | 原文可能有尚未提取的数据 | 不会产生虚假的显著性结论 |
| D3 研究历史 | 单独展示 | 157 种均有 Stage25A 指标；与化学容量不同 | 元数据年值需 QC | 导师汇报增加历史维度，不改变中位排名 |
| D4 维生素 | 定点复核 VC 两原文并审计 canonical 缺口；其他维生素按方法适配另列 | VC 已在 Top50/retrieval，历史有 2 B1 | 2001 表格和统计误差需复核 | 可决定是否发起针对性 evidence change request |
| D5 v1.1 条件 | 暂不具备正式冻结条件 | ≥2记录情景仅19种；study 独立性未证实 | 门槛与补充检索范围未决 | 维持 v1.0，待研究者批准修订 |
| D6 优先回查 | Rosmarinic acid、Daidzein、Fisetin、Hesperidin、Naringin；再查 rank20/21 与 VC | 前五名为 Frozen Top20 单记录，cutoff 差 0.1575 | 原文重复/误差结构 | 决定最低门槛与排序可信度 |
| D7 补充 H-ORAC | 只对上述 cutoff/单点/VC 开展定点检索 | 1,641 pending 未全量裁决 | 新证据量未知 | 形成 change request 输入，不批量重开 Stage25B |"""

doc(DOC/"Stage25B6A_Supervisor_Feedback_Assessment_CN.md",f"""
# Stage25B.6A 导师反馈证据审计与 Top20 修订模拟

**证据单位。** Publication 是原始论文；independent study 是独立开展且没有数据复用的研究；independent experiment 是独立实验运行；technical replicate 是同一次运行的重复测量；biological replicate 是独立生物样本；quantitative estimate 是一条可提取数值。本文的 68 条 A/B1 是 quantitative records，现有 `independent_experiment_id` 标签不能单独证明独立研究或独立实验运行。每个候选的不同 DOI 数可作为不同原始发表的线索，须核对方法、作者、材料和数据表后才能裁决 study independence。

**核心发现。** Frozen Top20 v1.0 保持不变。74 条 canonical 实验中 A=7、B1=61、B2=4、X=2；28 种可排序候选对应 68 条 A/B1 定量记录。`Eligible_experiment_N` 是当前数据表中的独立实验标签数，不能直接当作统计学独立样本数：study ID 和技术/生物重复层级均未系统记录。各候选的 A/B1 记录来自不同 DOI，但不同论文与独立研究不能画等号，故 scenario 2 当前无可确证的 20 人名单。

**误差与不确定性。** 68 条 A/B1 中，canonical SD 仅 {sd_n} 条、SE 0、CI 0；本轮从 Carvalho 2023 原文 Table 3 额外核对 Quercetin、Caffeic acid、Gallic acid 的 ± 值，但原表未明示其误差类型，单独标为 `UNSPECIFIED_PLUS_MINUS_IN_ORIGINAL`。按“任何已报告数值误差信息”计 {error_n}/68（{error_n/68:.1%}），按可确认 SD/SE/CI 类型计 {sd_n}/68（{sd_n/68:.1%}）；候选层面及排名差异的可信 95%CI 均为 `CI_NOT_ESTIMABLE`。原文中的技术重复 n=3 不能替代独立研究 n=3。IQR/range 只作描述性分布，不能当作置信区间。

**研究历史。** 157 种候选均有 Stage25A metadata-deduplicated antioxidant/redox original-publication count；本轮按已纳入的 provenance 记录另算 2017–2026 十年出版数，并区分一般抗氧化文献年份与已裁决 H-ORAC 年份。{future_n} 个候选的主表 latest year 超出当前年份或无效，历史表已经标旗；第一/末年须核对元数据。导师汇报推荐首年、跨度、去重原始论文数及近五/十年数作为独立维度；H-ORAC 特定 DOI 数仅为来源代理，不是 study N。

**维生素。** VC（AFF-0104）是 Stage25A 第 2 名，已进入 Top50 和 47 种检索集；未进入 Top20 的直接流程原因是 Stage25B canonical 表尚无其 A/B1 定量记录。既有分类证据主表有 Ou 2001 0.95 与 Carvalho 2023 0.53 两条历史 B1，中位 0.74 mol TE/mol；当前最末可排序第 28 名为 1.25。VC 的原始来源核验与 canonical re-adjudication 是特定缺口，不能在本轮把分类证据直接接入 Frozen Top20。其他维生素形式参见专项表。

**排名模拟。** Scenario 0 为现行 Frozen Top20。Scenario 1 的 ≥2 A/B1 记录规则排除现行 Top20 中的 {', '.join(one_top)}；依原中位数顺延加入 {', '.join(added)}，结果仅 **19** 种符合门槛，缺第 20 名，未用 B2 补足。Scenario 2 要求 ≥2 经核实独立原始研究：9 种单记录候选按现有记录可确定不符合，其余 19 种均 `INDEPENDENCE_UNRESOLVED`，不能形成正式 Top20。

**方法适用性。**

{method_table}

**修订方案比较。**

| 方案 | 优点 | 缺点与统计学合理性 | 数据可执行性、预计影响 | 需补数据与导师汇报适用性 |
|---|---|---|---|---|
| A：至少2条独立实验记录 | 可立即展示单记录剔除的方向，保留中位数 | 实验 ID 的独立性未证实；门槛是证据量规则，不是显著性检验 | 现有表可执行；只余19种，不能构成Top20 | 需核对批次/重复；适合作为诊断情景，不宜称正式名单 |
| B：至少2项独立原始研究 | 直接回应跨研究复现要求 | 2项研究仍无法稳定估计异质性或名次CI | study ID 缺失；9种单记录确定不符合，19种无法裁决 | 需逐篇核查作者、实验和数据复用；适合作为下一版候选门槛 |
| C：研究门槛＋精度和置信度审查＋研究历史单列 | 同时回应导师四点，保持效力、证据质量与研究历史的不同含义 | 工作量较大；需要预先批准规则，不能以简单加权总分替代 | 当前仅能提出框架；正式名单等待来源和误差核查 | 定点补充单记录、cutoff及VC原文；最适合完整导师汇报的最终结构 |

推荐 C 作为下一轮设计方向；本轮不选择正式修订方案。三案均不改变 H-ORAC 原数值，也不生成全局加权总分。现阶段不宣称不同候选名次差具有统计学显著性。

**HUMAN DECISIONS REQUIRED**

{decision_table}

本轮状态：**STAGE25B.6A — SUPERVISOR FEEDBACK AUDIT COMPLETE**。Frozen Top20 v1.0 与 Stage25B canonical rubric/证据表保持不变；若研究者批准修订，先建立 CHANGE REQUEST，再按批准范围核对独立研究、误差与针对性证据，另行决定是否更新 v1.1。
""")

doc(SYNC/"CHATGPT_SYNC_STAGE25B6A.md",f"""
# CHATGPT SYNC — Stage25B.6A

Stage25B.6A audit complete; Frozen Top20 v1.0 unchanged. `Eligible_experiment_N` counts labeled quantitative records, not validated independent studies. Across 28 rankable candidates there are 68 A/B1 records. Only {sd_n}/68 have canonical SD; 0 SE, 0 CI. Three further 2023 original-article ± values were located but their error type is not identified in Table 3. Candidate/rank 95%CI: `CI_NOT_ESTIMABLE`.

History: all 157 have Stage25A metadata-deduplicated antioxidant/redox publication counts; ten-year counts derived from publication provenance. Keep history separate from H-ORAC potency. VC (AFF-0104) was Stage25A rank 2, Top50 and in the 47 retrieval set, but Stage25B has 0 canonical A/B1. Historical primary-paper B1 values 0.95 (Ou 2001) and 0.53 (Carvalho 2023) yield 0.74; source/canonical reconciliation remains a targeted task.

Scenario 0: Frozen v1.0 unchanged. Scenario 1 (≥2 A/B1 records): Rosmarinic acid, Daidzein, Fisetin, Hesperidin and Naringin leave; Morin, Myricetin, Epigallocatechin and Gallic acid enter; only 19 eligible, so no complete Top20. Scenario 2 (≥2 independently verified original studies): 9 single-record candidates fail on available records; 19 remain independence-unresolved, so no formal list. Recommended design direction: independently verified study threshold with precision/heterogeneity review; history as a separate dimension; no composite score. Human decisions D1–D7 are in the assessment report. No Stage25B.6B work started.

**STAGE25B.6A — SUPERVISOR FEEDBACK AUDIT COMPLETE**
""")

# Small, append-only project navigation entries. Frozen status is not changed.
for rel, marker, entry in [
    ("PROJECT_FILE_INDEX_CN.md","Stage25B.6A supervisor feedback audit","## Stage25B.6A supervisor feedback audit\n\nDiagnostic CSVs: `data/h_orac_stage25b/stage25b6a/`. Scientific assessment and draft framework: `docs/qc/stage25b6a/`. ChatGPT handoff: `docs/sync/CHATGPT_SYNC_STAGE25B6A.md`. Stage25B Frozen Top20 v1.0 remains the current formal version."),
    ("docs/PROJECT_STAGE_INDEX_CN.md","Stage25B.6A — SUPERVISOR FEEDBACK AUDIT COMPLETE","## Stage25B.6A — SUPERVISOR FEEDBACK AUDIT COMPLETE\n\nEvidence independence, error coverage, research history, vitamins and minimum-evidence scenarios are audited in `docs/qc/stage25b6a/` and `data/h_orac_stage25b/stage25b6a/`. Frozen Top20 v1.0 remains unchanged; v1.1 requires separate human decision and change control."),
    ("Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md","Stage25B.6A — Supervisor Feedback Evidence Audit","## 2026-10-09 — Stage25B.6A — Supervisor Feedback Evidence Audit\n\nAudited independent evidence units, precision, 157-candidate research history and vitamin eligibility; simulated ≥2-record and ≥2-independent-study gates. The record gate leaves only 19 eligible candidates; study independence is unresolved. Frozen Top20 v1.0 and canonical rubric remain unchanged. See `docs/qc/stage25b6a/Stage25B6A_Supervisor_Feedback_Assessment_CN.md`.")
]:
    p=ROOT/rel
    old=p.read_text(encoding="utf-8-sig")
    if marker not in old:p.write_text(old.rstrip()+"\n\n"+entry+"\n",encoding="utf-8")

print(f"Stage25B.6A built: 74 independence rows, 68 A/B1 error rows, 28 summaries/scenarios, 157 histories, {len(vitamin)} vitamins; error {error_n}/68, typed SD {sd_n}/68, scenario1 {len(eligible_n2)}.")
