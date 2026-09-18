import csv, os
from collections import Counter

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
VERSION="v0.1"

def read(name):
    with open(os.path.join(DATA,name),encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(name,rows,fields):
    with open(os.path.join(DATA,name),"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)

master=read("Antioxidant_Class_Candidate_Master.csv")
identity={r["compound"]:r for r in master}
flav=read("Polyphenols_Flavonoids_Top20_v1.0.csv")
acid=read("Polyphenols_PhenolicAcids_TopN_v1.0.csv")

def stability(r):
    n=int(r["eligible_record_count"]); h=r["heterogeneity_flag"].lower(); ir=(r.get("identity_risk") or "").lower(); ar=(r.get("optical_risk") or "").lower()
    if n==1 or h=="high" or "unresolved" in ir or "high" in ir or "unresolved" in ar:
        return "Fragile"
    if n>=3 and h in ("low/not estimable","low","moderate") and r["confidence"]=="High":
        return "Stable"
    return "Moderately stable"

def depth(n):
    n=int(n)
    return "Deep (>=3 independent eligible records)" if n>=3 else ("Moderate (2 independent eligible records)" if n==2 else "Limited (1 independent eligible record)")

rows=[]
for panel,source,nrankable,status in [
    ("Polyphenols - Flavonoids",flav,25,"Top20"),
    ("Polyphenols - Phenolic acids / conjugates",acid,18,"Top available")]:
    for r in source:
        m=identity[r["compound"]]
        rank=int(r["rank"]); n=int(r["eligible_record_count"]); stab=stability(r)
        identity_risk=r.get("identity_risk") or "Identity locked at candidate level; glycoside/aglycone and stereochemistry remain record-specific QC fields"
        assay_risk=r.get("optical_risk") or "Historical H-ORAC-FL protocols are broadly comparable but non-identical; compound-specific optical/linearity QC is often incomplete"
        caveat=r["caveat"]
        if panel.endswith("Phenolic acids / conjugates") and r["compound"]=="Chlorogenic acid":
            caveat += " Ou 2001 generic chlorogenic mapping remains Tier X and is not pooled."
        rows.append({
          "overview_version":VERSION,"parent_class":m["parent_class"],"analysis_panel":panel,"subclass":r["subclass"],"compound":r["compound"],"canonical_name":m["canonical_name"],"PubChem_CID":r["PubChem_CID"],"InChIKey":r["InChIKey"],
          "within_class_rank":rank,"within_class_N_rankable":nrankable,"within_class_percentile":round(100*(nrankable-rank+1)/nrankable,1),"within_class_status":status,
          "primary_construct":"AAPH-derived radical oxidation of fluorescein / peroxyl-radical-related chain-breaking capacity","primary_metric_name":"H-ORAC-FL","primary_value":r["median_H_ORAC"],"primary_unit":"mol Trolox equivalents/mol compound",
          "eligible_record_count":n,"confidence":r["confidence"],"single_study_flag":r["single_study_flag"],"heterogeneity_flag":r["heterogeneity_flag"],"identity_risk":identity_risk,"assay_risk":assay_risk,
          "evidence_depth_category":depth(n),"evidence_stability":stab,"major_caveat":caveat,"provenance_record_ids":r["provenance_record_ids"],
          "dietary_exposure_umol_day":"NA","exposure_source":"Not reviewed","exposure_quality":"Not reviewed","bioavailability_summary":"Not reviewed","human_evidence_level":"Not reviewed",
          "direct_chemical_antioxidant_profile":"H-ORAC-FL profile available; see primary construct/value fields","endogenous_defense_profile":"Not reviewed","lipid_phase_activity":"Not reviewed","singlet_oxygen_activity":"Not reviewed","NRF2_GSH_GPX_profile":"Not reviewed","SOD_CAT_profile":"Not reviewed","NOX_mitochondrial_ROS_profile":"Not reviewed","ferroptosis_lipid_profile":"Not reviewed","direct_target_level":"Not reviewed","safety_prooxidant_context":"Not reviewed","experimental_tractability":"Not reviewed"
        })

fields=list(rows[0])
for forbidden in ("global_rank","global_score","standardized_ORAC_score","z_score","weighted_score","composite_antioxidant_score"):
    assert forbidden not in fields
assert len(rows)==38 and Counter(r["analysis_panel"] for r in rows)==Counter({"Polyphenols - Flavonoids":20,"Polyphenols - Phenolic acids / conjugates":18})
assert all(r["within_class_percentile"]<=100 for r in rows)
write("Global_Top_Overview_Master_v0.1.csv",rows,fields)

matrix=[
 ("Dietary intake","yes","Directly comparable","µmol/day","Molar dietary exposure may be compared when source, food form and intake model are aligned.","Absorption and matrix effects remain separate; missing intake is not zero.","Not reviewed"),
 ("Eligible independent study count","yes","Directly comparable","count","Counts evidence depth under the class-specific eligibility rule.","Equal counts do not imply equal protocol quality or biological importance.","Complete for Phase 3A/3B"),
 ("Evidence confidence category","yes","Directly comparable","High / Moderate / Low / Very low","Compares confidence labels generated from independent evidence depth and heterogeneity.","Confidence rules must remain harmonized; it does not compare antioxidant magnitude.","Complete for Phase 3A/3B"),
 ("Human evidence level","yes","Directly comparable","H1–H6 plus separate PK flag","Compares evidence hierarchy when the same human-evidence rubric is applied.","PK exposure must not be interpreted as efficacy.","Not reviewed"),
 ("Direct-target evidence tier","yes","Directly comparable","T1–T5","Compares the type of target evidence under the shared target hierarchy.","Only T1/T2 are direct-target layers; tier is not target potency.","Not reviewed"),
 ("Safety / prooxidant status","yes","Directly comparable","shared categorical risk status","Compares the presence and evidence grade of dose-window or prooxidant concerns.","Risk depends on dose, matrix, metal environment and population.","Not reviewed"),
 ("Within-class percentile","no","Profile comparable","0–100 within-class percentile","Shows relative position inside each class-specific eligible universe.","Equal percentiles do not mean equal antioxidant magnitude and cannot create a global rank.","Complete for Phase 3A/3B"),
 ("Mechanism domains","no","Profile comparable","domain-specific categorical profile","Shows which redox domains have evidence without adding them into one score.","Different domains represent different constructs and evidence depths.","Not reviewed"),
 ("Bioavailability","no","Profile comparable","compound/metabolite PK profile","Supports comparison of exposure patterns and metabolite relevance.","Cmax, AUC, conjugation and tissue exposure are not one common scalar.","Not reviewed"),
 ("Experimental tractability","no","Profile comparable","shared categorical profile","Compares feasibility after a common rubric is applied.","Depends on model, analytical platform, solubility and assay objective.","Not reviewed"),
 ("Evidence stability","no","Profile comparable","Stable / Moderately stable / Fragile","Shows robustness of the class-specific estimate.","Stability is distinct from effect magnitude and confidence.","Complete for Phase 3A/3B"),
 ("H-ORAC value","no","Not directly comparable","mol TE/mol within compatible H-ORAC-FL arm","May compare compounds only under compatible H-ORAC-FL conditions.","Cannot be assumed commensurate with L-ORAC or other class-specific constructs; historical protocols remain non-identical.","Available for Phase 3A/3B only"),
 ("L-ORAC value","no","Not directly comparable","mol TE/mol within validated L-ORAC arm","Potential within-arm metric for lipophilic compounds.","H- and L-ORAC are not automatically on one scale.","Not reviewed"),
 ("Singlet-oxygen quenching rate/value","no","Not directly comparable","assay-specific rate/value","Relevant to carotenoids under a separately frozen construct.","Different physical/chemical quenching systems and units prevent direct mixing with H-ORAC.","Not reviewed"),
 ("KEAP1/NRF2 evidence","no","Not directly comparable","mechanism-evidence tier/profile","Represents regulatory evidence rather than direct chemical capacity.","Pathway activation, expression and causal dependence must remain separated.","Not reviewed"),
 ("Mineral cofactor relevance","no","Not directly comparable","context-dependent profile","Represents enzyme cofactor or redox-context relevance.","Elements are not structurally defined antioxidant small molecules and can become prooxidant depending on context.","Not reviewed")]
mfields=["dimension","directly_comparable_yes_no","comparison_type","valid_unit_or_scale","interpretation","major_caveat","current_data_status"]
write("Cross_Class_Comparability_Matrix_v0.1.csv",[dict(zip(mfields,x)) for x in matrix],mfields)

# Human-readable schema pilot; the two panels are deliberately presented in separate blocks.
stabc=Counter(r["evidence_stability"] for r in rows)
def table(block):
    out=["| Compound | Analysis panel | Class rank | Rankable N | Percentile | Primary construct | Primary value | n | Confidence | Stability | Major caveat |",
         "|---|---|---:|---:|---:|---|---:|---:|---|---|---|"]
    for r in block:
        out.append(f"| {r['compound']} | {r['analysis_panel']} | {r['within_class_rank']} | {r['within_class_N_rankable']} | {r['within_class_percentile']:.1f} | H-ORAC-FL | {r['primary_value']} | {r['eligible_record_count']} | {r['confidence']} | {r['evidence_stability']} | {r['major_caveat']} |")
    return "\n".join(out)

fl=[r for r in rows if r["analysis_panel"]=="Polyphenols - Flavonoids"]
pa=[r for r in rows if r["analysis_panel"].endswith("Phenolic acids / conjugates")]
leaders=fl[:5]+pa[:5]
md=f"""# Global Top Overview Schema Pilot v0.1

**日期：2026-09-18｜状态：Schema pilot completed; global comparison not completed**

## 1. Purpose and boundary

本文件验证一个可扩展的 Global Top Overview 数据结构。本轮只纳入已完成的两个 H-ORAC-FL class-specific outputs：Flavonoids Top20 和 Phenolic acids / conjugates Top available 18，共 38 行。表格并列展示 class-specific rank、原始 primary construct、evidence depth、confidence、stability 与 caveat；不创建 global rank、global score、z-score、weighted score 或 composite antioxidant score，也不按 H-ORAC 数值把两类重新混排。

## 2. Percentile definition

`within_class_percentile = 100 × (within_class_N_rankable − within_class_rank + 1) / within_class_N_rankable`。Rank 1 固定为 100；最低类内名次仍保留大于 0 的百分位。该字段只反映候选在自己类别及其已获得 A/B1 的 rankable universe 中的位置。Flavonoid Rank 1/25 与 phenolic-acid Rank 1/18 都可为 100，但这不表示二者 chemical antioxidant magnitude 相等或可直接比较。

## 3. Evidence stability definition

`Stable` 要求多项独立 eligible records、低或中等异质性、身份清楚，并达到较深证据量；`Moderately stable` 表示至少两项记录，但仍有 protocol differences、Moderate confidence 或一定异质性；`Fragile` 表示单研究、高异质性或未解决的 identity/assay concern。Stability 描述 estimate robustness；confidence 描述现有证据等级与深度，二者不与 primary value 合成总分。

## 4. Flavonoids Top20

{table(fl)}

## 5. Phenolic acids / conjugates Top available 18

{table(pa)}

Phase 3B 的 4 个 candidate holds 不在 18-row overview 中，因为它们没有进入 class ranking；Ou 2001 generic chlorogenic record 继续保持 Tier X，未并入 chlorogenic-acid primary value。高异质性候选维持 provisional confidence，没有在本轮重新裁决。

## 6. Head-to-head class leaders

下表只把两个 panel 各自 Top5 并列展示，便于查看数据结构；不回答“谁整体更强”。

{table(leaders)}

## 7. Cross-Class Comparability Matrix

本轮定义 16 个比较维度：6 个在使用共同单位或共同证据 rubric 时可较直接比较，5 个只能作 profile comparison，5 个不得直接数值混排。Dietary intake、study count、evidence confidence、human evidence、direct-target tier 与 safety/prooxidant status 可在定义一致时并列；within-class percentile、mechanism domains、bioavailability、experimental tractability 和 evidence stability 只用于 profile；H-ORAC、L-ORAC、singlet-oxygen quenching、KEAP1/NRF2 evidence 与 mineral-cofactor relevance 必须保留各自 construct。详细规则见 `data/Cross_Class_Comparability_Matrix_v0.1.csv`。

## 8. Missingness audit

Identity、class-specific rank、primary construct/value、eligible study count、confidence、single-study、heterogeneity、caveat 和 provenance 已齐全。Direct chemical antioxidant profile 可由现有 H-ORAC-FL 字段表达。以下字段尚未按统一 protocol 系统审阅，统一标记为 `Not reviewed` 或 `NA`：quantitative dietary exposure、exposure quality、bioavailability/PK、human evidence、endogenous-defense mechanisms、lipid-phase activity、singlet-oxygen activity、NRF2/GSH/GPX、SOD/CAT、NOX/mitochondrial ROS、ferroptosis/lipid profile、direct-target tier、safety/prooxidant context 和 experimental tractability。`Not reviewed` 不得改写为 `No evidence`。

## 9. Readiness assessment

1. **当前是否可以正式做 Global Top Overview？** 数据结构可用于 pilot 并列展示，但不能宣称已经完成正式 Global Overview。
2. **哪些字段齐全？** 两类的 identity、within-class rank/percentile、primary H-ORAC-FL construct/value、evidence depth、confidence、heterogeneity、stability、assay/identity caveat 和 provenance 齐全。
3. **哪些字段缺失？** 暴露、PK、人体、机制、target、安全与实验可开发性尚未系统审阅。
4. **是否需要 non-H-ORAC class？** 是。当前两个输入都是 polyphenol subclasses，并共享 H-ORAC-based construct，尚不能验证 schema 对真正不同 primary constructs 的适配性。至少完成 Vitamins 或 Carotenoids 后才能测试。
5. **最大科学风险是什么？** 把相同的类内 percentile 或 evidence category误读为跨 construct 的 antioxidant magnitude，或因两个现有类别都使用 H-ORAC 而错误认为未来所有类别都可用相同数值轴。

## 10. Recommended next non-H-ORAC test class

建议先执行 **Carotenoids ranking**，因为它能直接压力测试 singlet-oxygen/lipid-phase primary construct、光学干扰、溶解与聚集问题，并明确证明 overview 必须保留原始 class-specific unit，而不能退回 ORAC 单轴。Vitamins 类别混合 vitamin C 与 tocopherol/tocotrienol，内部还需要 H/L 与具体 construct 分层，作为首个 schema stress test 的解释复杂度更高。本建议不等于开始执行该排名。

## 11. Human-review status

本轮没有触发新的 candidate adjudication，也未修改现有排名。Phase 3B 的 Feruloylquinic acid、generic p-Coumaroylquinic acid、2,3-Dihydroxybenzoic acid、3,4,5-Trimethoxybenzoic acid、Ou 2001 generic chlorogenic mapping 与高异质性事项继续按 `data/Human_Review_Log.csv` 保持 pending；overview 仅继承现有 identity risk、stability 与 caveat。

## Sync to ChatGPT

**A. rows included：**38。**B. classes included：**Flavonoids Top20 与 Phenolic acids / conjugates Top available 18。**C. fields complete：**identity、class rank/percentile/status、H-ORAC-FL construct/value/unit、n、confidence、single-study、heterogeneity、identity/assay risk、depth、stability、caveat、provenance。**D. fields missing：**quantitative exposure、PK、human、mechanism、target、安全和 tractability。**E. comparability dimensions：**6 directly comparable with shared definitions，5 profile comparable。**F. non-comparable dimensions：**H-ORAC、L-ORAC、singlet-oxygen quenching、KEAP1/NRF2、mineral cofactor relevance。**G. stability distribution：**Stable={stabc['Stable']}、Moderately stable={stabc['Moderately stable']}、Fragile={stabc['Fragile']}。**H. class leaders：**Flavonoids 为 epicatechin、catechin、gallocatechin、apigenin、isorhamnetin；phenolic acids 为 rosmarinic、caffeic、gentisic、protocatechuic、vanillic acid。**I. schema risks：**percentile 被误读为 magnitude、Not reviewed 被误读为 no evidence、两个 H-ORAC panels 无法验证跨 construct 适配性。**J. formal Global Overview ready：**否；schema pilot ready。**K. recommended next non-H-ORAC class：**Carotenoids。**L. human-review item triggered：**无新增；继承 Phase 3B pending items。
"""
with open(os.path.join(ROOT,"docs","Global_Top_Overview_Schema_Pilot_CN.md"),"w",encoding="utf-8") as f:f.write(md)

print("Global schema rows",len(rows),Counter(r["evidence_stability"] for r in rows))
print("Comparability dimensions",len(matrix),Counter(x[2] for x in matrix))
