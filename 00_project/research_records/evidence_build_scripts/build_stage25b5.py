import csv
import hashlib
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-22"
VERSION = "Stage25B Frozen Top20 v1.0"

def read_csv(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, fieldnames, rows):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def write_text(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip() + "\n", encoding="utf-8")

def append_text_once(path, marker, text):
    p = ROOT / path
    old = p.read_text(encoding="utf-8-sig") if p.exists() else ""
    if marker not in old:
        p.write_text(old.rstrip() + "\n\n" + text.rstrip() + "\n", encoding="utf-8")

def append_csv_once(path, key_field, key_value, row):
    p = ROOT / path
    rows = read_csv(path)
    if any(r.get(key_field) == key_value for r in rows):
        return
    fields = list(rows[0]) if rows else list(row)
    rows.append(row)
    write_csv(path, fields, rows)

rank = read_csv("data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv")
summary = {r["candidate_id"]: r for r in read_csv("data/h_orac_stage25b/stage25b/Stage25B_HORAC_Candidate_Summary.csv")}
evidence = read_csv("data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv")
sensitivity = read_csv("data/h_orac_stage25b/stage25b4/Stage25B4_B2_Sensitivity.csv")
master = {r["candidate_id"]: r for r in read_csv("data/literature_screening/master/Literature_Screening_Candidate_Master.csv")}

expected = ["Rosmarinic acid","Epicatechin","Catechin","Caffeic acid","Apigenin","Naringenin","Kaempferol","Daidzein","Hesperetin","Protocatechuic acid","Genistein","Quercetin","Fisetin","Rutin","Sinapic acid","p-Coumaric acid","Hesperidin","Luteolin","Naringin","Ferulic acid"]
top20 = rank[:20]
assert [r["canonical_name"] for r in top20] == expected
assert len({r["candidate_id"] for r in top20}) == 20
assert rank[20]["canonical_name"] == "Morin"
assert abs(float(rank[19]["median_H_ORAC_mol_TE_per_mol"]) - float(rank[20]["median_H_ORAC_mol_TE_per_mol"]) - 0.1575) < 1e-9
assert len(evidence) == 74
assert {t:sum(r["H_ORAC_tier"]==t for r in evidence) for t in ("A","B1","B2","X")} == {"A":7,"B1":61,"B2":4,"X":2}
assert len(rank) == 28
assert all(r["H_ORAC_tier"] in ("A","B1") for r in evidence if r["eligibility_status"] == "PRIMARY_RANKING_ELIGIBLE")

sens_by = {(r["analysis"], r["candidate_id"]): r for r in sensitivity}
enter = [r for r in sensitivity if r["membership_vs_primary"] == "enter"]
leave = [r for r in sensitivity if r["membership_vs_primary"] == "leave_from_sensitivity"]
assert [r["candidate"] for r in enter] == ["Cyanidin 3-O-glucoside","Baicalein","Cyanidin"]
assert [r["candidate"] for r in leave] == ["Luteolin","Naringin","Ferulic acid"]

frozen = []
for r in top20:
    cid = r["candidate_id"]; s = summary[cid]; m = master[cid]
    sev = [x for x in evidence if x["candidate_id"] == cid]
    counts = {t:sum(x["H_ORAC_tier"]==t for x in sev) for t in ("A","B1","B2","X")}
    sr = sens_by.get(("SENSITIVITY_A+B1+B2", cid), {})
    frozen.append({
        "primary_rank":r["rank"], "candidate_id":cid, "canonical_name":r["canonical_name"],
        "chemical_class":m["class"], "chemical_subclass":m["subclass"],
        "median_H_ORAC_mol_TE_per_mol":s["median_H_ORAC_mol_TE_per_mol"], "min_H_ORAC":s["min"], "max_H_ORAC":s["max"], "IQR":s["IQR"], "max_min_ratio":s["max_min_ratio"],
        "eligible_A_N":counts["A"], "eligible_B1_N":counts["B1"], "eligible_A_B1_N":int(counts["A"]+counts["B1"]), "B2_N":counts["B2"], "X_N":counts["X"],
        "evidence_confidence":r["evidence_confidence"], "heterogeneity_flag":r["heterogeneity_flag"], "Stage25A_research_density_rank":r["Stage25A_primary_rank"],
        "B2_sensitivity_status":sens_by.get(("PRIMARY_A+B1",cid),{}).get("membership_vs_primary","same"),
        "B2_sensitivity_rank_if_included":sr.get("rank",""), "freeze_status":"FROZEN_FOR_DOWNSTREAM_USE",
        "freeze_definition":"CANONICAL ELIGIBILITY-DEFINED PRIMARY H-ORAC TOP20 (A+B1)", "freeze_date":TODAY, "rubric_version":"H-ORAC Evidence Rubric v2.0",
        "ranking_rule":"descending median canonical v2 A+B1 H-ORAC (mol TE/mol compound)",
        "limitations_flag":"B2_SENSITIVITY_LIMITED;EXHAUSTIVE_COMPLETENESS_NOT_ACHIEVED"
    })

frozen_fields = list(frozen[0])
write_csv("data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv", frozen_fields, frozen)

prov=[]
for r in frozen:
    ev=[x for x in evidence if x["candidate_id"]==r["candidate_id"] and x["H_ORAC_tier"] in ("A","B1")]
    def uniq(field): return ";".join(dict.fromkeys(x[field] for x in ev if x.get(field)))
    prov.append({"candidate":r["canonical_name"],"candidate_id":r["candidate_id"],"primary_rank":r["primary_rank"],"experiment_ids_used":uniq("independent_experiment_id"),"source_ids_used":uniq("publication_id"),"DOIs":uniq("DOI"),"A_experiment_N":r["eligible_A_N"],"B1_experiment_N":r["eligible_B1_N"],"median_value":r["median_H_ORAC_mol_TE_per_mol"],"ranking_version":VERSION,"rubric_version":"H-ORAC Evidence Rubric v2.0","source_candidate_summary_file":"data/h_orac_stage25b/stage25b/Stage25B_HORAC_Candidate_Summary.csv","source_ranking_file":"data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv","freeze_decision":"OPTION C — FREEZE WITH EXPLICIT B2 SENSITIVITY QUALIFICATION","freeze_commit":"see Git commit containing this manifest; baseline=a042dce2eaffe6431d4122d16435441fa3b83327"})
write_csv("data/h_orac_stage25b/frozen/Stage25B_Top20_Freeze_Provenance.csv", list(prov[0]), prov)

qual=[]
for r in leave:
    qual.append({"comparison":"PRIMARY_A+B1 vs SENSITIVITY_A+B1+B2","membership_change":"LEAVE","candidate_id":r["candidate_id"],"candidate":r["candidate"],"B2_value":"","sensitivity_rank":"","why_B2":"not applicable; primary member displaced when eligible sensitivity-only B2 values are included","risk_domain":"membership sensitivity","unresolved_comparability_issue":"B2 material-comparability uncertainty in entering candidates changes cutoff membership","why_excluded_from_primary":"not excluded from primary; leaves only in sensitivity scenario","exclusion_pre_specified":"not applicable","exclusion_rank_independent":"yes","interpretation":"Primary eligibility-defined member; sensitivity-only leave"})
for r in enter:
    evb=[x for x in evidence if x["candidate_id"]==r["candidate_id"] and x["H_ORAC_tier"]=="B2"]
    caveat="; ".join(dict.fromkeys(x["major_method_caveat"] for x in evb if x["major_method_caveat"]))
    risks="; ".join(dict.fromkeys("/".join(v for v in [x["optical_interference_risk"],x["solubility_risk"],x["aggregation_risk"],x["redox_cycling_risk"]] if v and v != "not reported") for x in evb))
    qual.append({"comparison":"PRIMARY_A+B1 vs SENSITIVITY_A+B1+B2","membership_change":"ENTER","candidate_id":r["candidate_id"],"candidate":r["candidate"],"B2_value":r["median_mol_TE_per_mol"],"sensitivity_rank":r["rank"],"why_B2":caveat,"risk_domain":risks or "material comparability","unresolved_comparability_issue":caveat,"why_excluded_from_primary":"predefined unresolved material-comparability risk under rubric v2.0; retained for sensitivity only","exclusion_pre_specified":"yes","exclusion_rank_independent":"yes","interpretation":"Exclusion is an eligibility decision, not a response to ranking outcome"})
write_csv("data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv",list(qual[0]),qual)

deliver=[]
for r in frozen:
    deliver.append({"Rank":r["primary_rank"],"Candidate":r["canonical_name"],"Class":r["chemical_class"],"Median_HORAC":r["median_H_ORAC_mol_TE_per_mol"],"Eligible_experiment_N":r["eligible_A_B1_N"],"Tier_A_N":r["eligible_A_N"],"Tier_B1_N":r["eligible_B1_N"],"Confidence":r["evidence_confidence"],"Heterogeneity":r["heterogeneity_flag"],"Stage25A_research_density_rank":r["Stage25A_research_density_rank"],"B2_sensitivity_note":"LEAVES_TOP20_IF_B2_INCLUDED" if r["B2_sensitivity_status"]=="leave_from_sensitivity" else "UNCHANGED_MEMBERSHIP"})
write_csv("data/h_orac_stage25b/frozen/Stage25B_Final_Top20_Deliverable.csv",list(deliver[0]),deliver)

handoff=[]
for r in frozen:
    row={"candidate_id":r["candidate_id"],"canonical_name":r["canonical_name"],"primary_HORAC_rank":r["primary_rank"],"median_HORAC":r["median_H_ORAC_mol_TE_per_mol"],"evidence_confidence":r["evidence_confidence"]}
    for f in ("food_source_status","dietary_exposure_status","human_evidence_status","PK_bioavailability_status","mechanism_status","direct_target_status","safety_prooxidant_status","tractability_status"): row[f]="NOT_YET_ASSESSED"
    handoff.append(row)
write_csv("data/top20_characterization/Top20_Downstream_Handoff_Master.csv",list(handoff[0]),handoff)

names="\n".join(f"{r['primary_rank']}. {r['canonical_name']} — {r['median_H_ORAC_mol_TE_per_mol']} mol TE/mol (N={r['eligible_A_B1_N']}, {r['evidence_confidence']})" for r in frozen)
limitations="""1. H-ORAC 是化学抗氧化容量构念，不是人体疗效。\n2. 只有 H-ORAC-compatible 候选可进入该定量汇聚。\n3. B2 因未解决的 material comparability risks 不进入 primary ranking。\n4. 纳入 B2 会导致 Top20 三进三出。\n5. 部分候选仅有一个 eligible experiment。\n6. 多个候选存在显著异质性。\n7. rank20 与 rank21 仅差 0.1575 mol TE/mol。\n8. Ferulic acid 标记为 HIGH_HETEROGENEITY。\n9. 1,641 条 publication records 尚未完成全文裁决。\n10. Stage25A 指标是 metadata-deduplicated antioxidant/redox original-publication count，不是独立研究数或抗氧化效力。\n11. Top20 不是临床、营养或转化优先级排名。"""

write_text("docs/qc/Stage25B5_Primary_Top20_Freeze_Decision_CN.md",f"""# Stage25B.5 Primary H-ORAC Top20 冻结决定

## 正式决定

研究者已选择 Option C：**FREEZE WITH EXPLICIT B2 SENSITIVITY QUALIFICATION**。本项目于 {TODAY} 正式冻结 **CANONICAL ELIGIBILITY-DEFINED PRIMARY H-ORAC TOP20 (A+B1)**，版本为 **{VERSION}**。该集合基于 canonical H-ORAC Evidence Rubric v2.0，仅纳入 Tier A/B1 quantitative evidence；Tier B2 因存在预定义且未解决的 material comparability risks，仅用于 sensitivity analysis，不进入 primary ranking。B2 排除是 rank-independent 的方法学 eligibility 决策，不是观察排名结果后作出的决定。

Primary ranking stability = **FROZEN**：rubric v2.0 migration 后 Top20 membership 未变化。B2 sensitivity robustness = **LIMITED**：纳入 B2 后 Cyanidin 3-O-glucoside、Baicalein、Cyanidin 进入，Luteolin、Naringin、Ferulic acid 离开，故不得描述为对所有 evidence assumptions 完全稳健。Exhaustive literature completeness = **NOT ACHIEVED**：1,641 条 pending publication records 未完成全文裁决，因此这是当前 adjudicated evidence set 上的 project-level freeze，不是 exhaustive systematic-review closure。

## 冻结名单

{names}

rank20 为 Ferulic acid（4.032，N=4，Moderate，HIGH_HETEROGENEITY），rank21 为 Morin（3.8745，N=2，Moderate），差值 0.1575 mol TE/mol。

## 必须伴随使用的限制

{limitations}

任何新增证据、pending records 重处理、identity/unit/duplicate/provenance 错误均不得 silent change frozen Top20；必须提交 CHANGE REQUEST，记录原因、受影响候选与实验及预期排名影响，并经研究者批准后才能 UNFREEZE / VERSION UPDATE。
""")

write_text("docs/methods/h_orac_framework/Stage25B_HORAC_Selection_and_Ranking_Method_Final_CN.md",f"""# Stage25B H-ORAC 选择与排名最终方法

## 工作流

157 个 aqueous candidate universe → unified research-evidence-density screening → Stage25A provisional Top50 → H-ORAC applicability QC → 47 个 retrieval candidates → H-ORAC literature retrieval → canonical evidence adjudication → H-ORAC Evidence Rubric v2.0 → Tier A/B1 eligible quantitative evidence → 28 个 rankable candidates → {VERSION}。

Stage25A primary metric 为 **metadata-deduplicated antioxidant/redox original-publication count**。legacy 字段 `antioxidant_independent_publication_N` 仅为 backward compatibility，**DO NOT INTERPRET AS INDEPENDENT-STUDY COUNT**；该指标也不是 antioxidant potency。

Primary ranking 仅使用 rubric v2.0 Tier A+B1 的独立实验，以 mol Trolox equivalents/mol compound 的 median H-ORAC 降序排列；不建立 publication、exposure、citation、human evidence 或其他维度的复合总分。B2 仅作预先规定的 sensitivity analysis。74 条已裁决实验迁移后为 A=7、B1=61、B2=4、X=2（C=0），形成 28 个 primary-rankable candidates。

## 可追溯性与解释

正式图由 `R/stage25b5/` 脚本读取 frozen CSV 生成；frozen candidate provenance 可回溯至 experiment ID、publication/source ID 与 DOI。排名解释限于当前 candidate universe、当前已裁决证据、rubric v2.0 和 A+B1 eligibility rule。

## 限制

{limitations}
""")

write_text("docs/supervisor/Stage25B_Primary_Top20_Supervisor_Summary_CN.md",f"""# Stage25B Primary H-ORAC Top20 导师摘要

本项目从 157 种水相候选开始，经统一研究基础筛选得到 Top50，其中 47 种进入 H-ORAC 检索；在 canonical H-ORAC Evidence Rubric v2.0 下，最终 28 种具有 A/B1 可比定量证据。研究者选择 Option C，并冻结 eligibility-defined Primary H-ORAC Top20（A+B1），用于下一阶段多维 translational characterization。

Frozen Top20 为：{', '.join(r['canonical_name'] for r in frozen)}。rank20 Ferulic acid 为 4.032 mol TE/mol，rank21 Morin 为 3.8745，差 0.1575。若在 sensitivity analysis 中纳入 B2，则 Cyanidin 3-O-glucoside、Baicalein、Cyanidin 进入，Luteolin、Naringin、Ferulic acid 离开。因此该集合是 eligibility-defined primary set，而不是 absolute antioxidant ranking；它也不是人体疗效、营养价值或转化优先级排名。1,641 条记录仍待裁决，故本次为项目级冻结而非穷尽性系统综述关闭。

下一步只允许基于该 frozen set 开展 food source/exposure、human evidence、PK/bioavailability、mechanism/redox biology、direct target、safety/prooxidant、tractability 与 evidence stability 的多维画像；不得以简单加权或全局综合分数替代多维判断。
""")

write_text("docs/qc/Stage25B5_Final_Freeze_and_Closure_Report_CN.md",f"""# Stage25B.5 最终冻结与关闭报告

**Q1 Primary Top20 是否正式冻结？** 是，{TODAY} 以 {VERSION} 正式冻结。  
**Q2 冻结定义是什么？** CANONICAL ELIGIBILITY-DEFINED PRIMARY H-ORAC TOP20 (A+B1)，按 canonical v2 A+B1 median H-ORAC 降序。  
**Q3 Frozen Top20 有哪些？** {', '.join(r['canonical_name'] for r in frozen)}。  
**Q4 B2 sensitivity 如何改变 membership？** Cyanidin 3-O-glucoside、Baicalein、Cyanidin 进入；Luteolin、Naringin、Ferulic acid 离开，三进三出。  
**Q5 为什么仍允许 freeze？** Primary eligibility rule 与 B2 排除均为预定义、rank-independent；rubric migration 后 primary membership 稳定，且敏感性差异被明确限定和披露。  
**Q6 哪些 limitations 必须伴随使用？** 见下列限制，尤其是化学构念非人体疗效、B2 robustness limited、单实验与异质性、截止差小、证据不穷尽。  
**Q7 1,641 pending 如何处理？** 原样保留，本轮未继续裁决，不用二手数值替代。  
**Q8 Stage25B 是否关闭？** 是：**STAGE25B CLOSED — PRIMARY H-ORAC TOP20 FROZEN WITH EXPLICIT B2 SENSITIVITY QUALIFICATION**。  
**Q9 是否可进入下一阶段？** 是：**READY FOR TOP20 TRANSLATIONAL CHARACTERIZATION**，但本轮未执行任何下游搜索或评分。  
**Q10 什么情况允许重开？** 新增 H-ORAC evidence、重处理 pending、发现 identity/unit/duplicate/provenance error 时，须先提交 CHANGE REQUEST 并获研究者批准，方可 unfreeze/version update。

## Integrity checks

A–Q 均通过：Top20 与 canonical ranking 一致；20 个唯一 candidate IDs；primary median 无 B2/C/X；排名可复现；rank20/21 与 0.1575 差值正确；B2 三进三出精确复现；157/50/47 状态不变；1,641 pending 未触碰；无新候选、target mapping、translational scoring 或 global composite score。

## 限制

{limitations}
""")

write_text("docs/sync/CHATGPT_SYNC_STAGE25B5.md",f"""# CHATGPT SYNC — Stage25B.5

- Decision: Option C — FREEZE WITH EXPLICIT B2 SENSITIVITY QUALIFICATION
- Frozen version: {VERSION}; definition: CANONICAL ELIGIBILITY-DEFINED PRIMARY H-ORAC TOP20 (A+B1)
- Frozen Top20: {', '.join(r['canonical_name'] for r in frozen)}
- Cutoff: rank20 Ferulic acid 4.032 (N=4, Moderate, HIGH_HETEROGENEITY); rank21 Morin 3.8745 (N=2, Moderate); gap 0.1575 mol TE/mol
- B2 sensitivity: ENTER Cyanidin 3-O-glucoside, Baicalein, Cyanidin; LEAVE Luteolin, Naringin, Ferulic acid
- Tables: `data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv`, `Stage25B_Top20_Freeze_Provenance.csv`, `Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv`, `Stage25B_Final_Top20_Deliverable.csv`
- Figures: `figures/aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.png/.svg`; `HORAC_Top20_B2_Sensitivity.png/.svg`
- Integrity: primary stable/frozen; B2 robustness limited; exhaustive completeness not achieved; 1,641 pending untouched
- Checksums: `data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv`
- Handoff: `data/top20_characterization/Top20_Downstream_Handoff_Master.csv`; all downstream dimensions NOT_YET_ASSESSED

**STAGE25B CLOSED — PRIMARY H-ORAC TOP20 FROZEN WITH EXPLICIT B2 SENSITIVITY QUALIFICATION**  
**READY FOR TOP20 TRANSLATIONAL CHARACTERIZATION**
""")

append_text_once("PROJECT_FILE_INDEX_CN.md","Stage25B.5 frozen package","""## Stage25B.5 frozen package

- Frozen tables: `data/h_orac_stage25b/frozen/`
- Final method: `docs/methods/h_orac_framework/Stage25B_HORAC_Selection_and_Ranking_Method_Final_CN.md`
- Freeze/closure: `docs/qc/Stage25B5_Primary_Top20_Freeze_Decision_CN.md`, `docs/qc/Stage25B5_Final_Freeze_and_Closure_Report_CN.md`
- Canonical figures: `figures/aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.*`, `HORAC_Top20_B2_Sensitivity.*`
- Downstream skeleton: `data/top20_characterization/Top20_Downstream_Handoff_Master.csv`
- Status: STAGE25B CLOSED — PRIMARY H-ORAC TOP20 FROZEN WITH EXPLICIT B2 SENSITIVITY QUALIFICATION.""")
append_text_once("docs/PROJECT_STAGE_INDEX_CN.md","Stage25B.5 — CLOSED","""## Stage25B.5 — CLOSED / FROZEN FOR DOWNSTREAM USE

Option C completed. Primary A+B1 H-ORAC Top20 frozen as v1.0 with explicit B2 sensitivity qualification. B2 robustness is LIMITED; exhaustive literature completeness is NOT ACHIEVED (1,641 pending untouched). Ready for Top20 translational characterization; no downstream search or scoring was performed in this stage.""")
append_text_once("Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md","Stage25B.5 — Primary H-ORAC Top20 Freeze","""## 2026-09-22 — Stage25B.5 — Primary H-ORAC Top20 Freeze

Researcher selected Option C. The canonical eligibility-defined A+B1 Top20 was frozen as Stage25B Frozen Top20 v1.0 after all integrity checks passed. Rubric v2.0 migration retained primary membership; B2 sensitivity produced three enters/three leaves and is explicitly qualified. The 1,641 pending publication records were not processed. Stage25B is closed and the downstream multidimensional characterization skeleton is ready; no target/mechanism/human/food/PK/safety work was initiated.""")

registry_rows=[
{"scientific_module":"H-ORAC frozen ranking","asset_role":"FROZEN MASTER","asset_name":"Stage25B Frozen Primary H-ORAC Top20 v1.0","canonical_path":"data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv","source_of_truth":"yes","derived_from":"Stage25B_HORAC_Quantitative_Ranking.csv + Candidate Summary + Evidence","used_by":"Top20 translational characterization","stage_origin":"25B.5","current_status":"ACTIVE_CANONICAL","replacement_for":"","notes":"Eligibility-defined A+B1; B2 sensitivity explicitly qualified"},
{"scientific_module":"H-ORAC frozen ranking","asset_role":"FINAL DELIVERABLE","asset_name":"Stage25B Final Top20 Deliverable","canonical_path":"data/h_orac_stage25b/frozen/Stage25B_Final_Top20_Deliverable.csv","source_of_truth":"no","derived_from":"Stage25B Frozen Primary H-ORAC Top20 v1.0","used_by":"supervisor/downstream handoff","stage_origin":"25B.5","current_status":"ACTIVE_CANONICAL","replacement_for":"","notes":"Compact reporting table"},
{"scientific_module":"H-ORAC frozen ranking","asset_role":"CANONICAL FIGURE","asset_name":"Frozen Primary H-ORAC Top20","canonical_path":"figures/aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.png","source_of_truth":"no","derived_from":"Stage25B_Frozen_Primary_HORAC_Top20.csv","used_by":"supervisor/reporting","stage_origin":"25B.5","current_status":"ACTIVE_CANONICAL","replacement_for":"","notes":"R-generated; median, range/IQR and evidence depth"},
{"scientific_module":"H-ORAC frozen ranking","asset_role":"SENSITIVITY FIGURE","asset_name":"Top20 B2 sensitivity qualification","canonical_path":"figures/aqueous_antioxidant_atlas/HORAC_Top20_B2_Sensitivity.png","source_of_truth":"no","derived_from":"Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv","used_by":"qualification/reporting","stage_origin":"25B.5","current_status":"ACTIVE_CANONICAL","replacement_for":"","notes":"Membership changes only; not a second ranking"}
]
reg=read_csv("CANONICAL_ASSET_REGISTRY.csv"); existing={r["canonical_path"] for r in reg}; reg.extend(r for r in registry_rows if r["canonical_path"] not in existing); write_csv("CANONICAL_ASSET_REGISTRY.csv",list(reg[0]),reg)

append_csv_once("data/class_specific_antioxidant/Human_Review_Log.csv","stage","Stage25B.5",{
    "stage":"Stage25B.5","compound":"Stage25B Frozen Primary Top20 v1.0","source":"docs/qc/Stage25B5_Primary_Top20_Freeze_Decision_CN.md","issue_type":"freeze decision",
    "issue_description":"Option C selected; rubric v2.0; canonical eligibility-defined A+B1 Top20 frozen; B2 sensitivity 3 enter/3 leave; 1,641 pending not adjudicated; downstream use approved; Stage25B closed.",
    "codex_recommendation":"Freeze with explicit B2 sensitivity qualification; use only as eligibility-defined primary set.",
    "human_decision":"Option C selected — FREEZE WITH EXPLICIT B2 SENSITIVITY QUALIFICATION","reviewer":"Researcher + ChatGPT","date":TODAY,
    "effect_on_ranking":"Stage25B Frozen Top20 v1.0 fixed for downstream use; changes require approved change request."
})

print("Stage25B.5 tabular and documentary assets built; integrity assertions passed.")
