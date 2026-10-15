"""Build read-only-derived Phase 1 evidence, framework, and governance assets.

All inputs are existing project assets. This script never writes canonical, frozen,
rubric, human-decision, or prior-stage files. New source findings are proposals.
"""
import csv
import hashlib
import os
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-15'
BASE_SHA = '493d3ca4fd62f65ec01179444fd4d9a3dd33ecb5'
A = ROOT/'data/h_orac_stage25b/stage25b6d'
AD = ROOT/'docs/qc/stage25b6d'
B = ROOT/'data/framework'
BD = ROOT/'docs/framework'
J = ROOT/'data/dual_track_phase1'
JD = ROOT/'docs/dual_track_phase1'
G = ROOT/'current_review'
for p in (A, AD, B, BD, J, JD, G): p.mkdir(parents=True, exist_ok=True)

def read(rel):
    with (ROOT/rel).open('r', encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))

def out(path, rows, fields=None):
    assert rows, path
    fields = fields or list(rows[0])
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader(); w.writerows(rows)

def md(path, value): path.write_text(value.strip()+'\n', encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def relative(path): return path.relative_to(ROOT).as_posix()
def value(x):
    try: return float(x)
    except (TypeError,ValueError): return None

evidence=read('data/h_orac_stage25b/Stage25B_HORAC_Experiment_Evidence.csv')
eligible=[r for r in evidence if r['H_ORAC_tier'] in ('A','B1')]
ranking=read('data/h_orac_stage25b/Stage25B_HORAC_Quantitative_Ranking.csv')
candidate=read('data/literature_screening/master/Literature_Screening_Candidate_Master.csv')
source6=read('data/h_orac_stage25b/stage25b6c/Stage25B6C_Source_Fulltext_Verification.csv')
close6=read('data/h_orac_stage25b/stage25b6c/Stage25B6C_Candidate_Independence_Closure.csv')
error6=read('data/h_orac_stage25b/stage25b6c/Stage25B6C_Error_Definition_Closure.csv')
history6=read('data/h_orac_stage25b/stage25b6c/Stage25B6C_Research_Maturity_QC.csv')
cr6=read('data/h_orac_stage25b/stage25b6c/Stage25B6C_Proposed_Change_Requests.csv')
registry=read('CANONICAL_ASSET_REGISTRY.csv')
manifest=read('data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv')
assert len(evidence)==74 and len(eligible)==68 and len(ranking)==28 and len(candidate)==157 and len(source6)==16
assert len(close6)==28 and len(error6)==68 and len(history6)==157 and len(cr6)==14
assert all(sha(ROOT/r['asset_path'])==r['sha256'] for r in manifest)
rubric=ROOT/'docs/methods/h_orac_framework/H_ORAC_Evidence_Rubric_v2.0_CN.md'
protected_before={p:sha(p) for p in [rubric,ROOT/'data/h_orac_stage25b/Stage25B_HORAC_Experiment_Evidence.csv',ROOT/'data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv']}
by_candidate=defaultdict(list)
for r in eligible: by_candidate[r['candidate_id']].append(r)
rank_by_id={r['candidate_id']:r for r in ranking}
candidate_by_id={r['candidate_id']:r for r in candidate}
history_by_id={r['candidate_id']:r for r in history6}
source_by_doi={r['DOI'].lower():r for r in source6}

# Track A: the newly recovered institutional original is the sole newly closed
# canonical source. Other source rows retain their actual unresolved status.
hayes='10.1016/j.foodchem.2010.11.092'
hayes_url='https://capa.ufpr.br/portal/wp-content/uploads/2017/10/Food-Chemistry.pdf'
source=[]
for r in source6:
    x=dict(r)
    if r['DOI'].lower()==hayes:
        x.update(fulltext_status='ORIGINAL_FULLTEXT_VERIFIED',original_measurement_status='VERIFIED_ORIGINAL_EXPERIMENT',study_group='Hayes/Teagasc Ireland',material='PURIFIED_ELLAGIC_ACID_COMMERCIAL_PRODUCT',assay='AAPH_FLUORESCEIN_TROLOX',source_location='Methods 2.3.4 p.950; Table 1 and footnote p.951',source_url=hayes_url,reused_data_evidence='Original paper reports its own assay; no data reuse identified',verification_note='Ellagic acid ORAC 151.77 ± 3.57 g Trolox/100 g dry sample; mean ± SD of three determinations. Pure product assayed separately from olive extract.')
    x['stage25b6d_change']='NEW_FULLTEXT_CLOSURE' if r['DOI'].lower()==hayes else 'CARRIED_FORWARD_NO_NEW_ORIGINAL_TABLE'
    x['unresolved_issue']='' if x['original_measurement_status']=='VERIFIED_ORIGINAL_EXPERIMENT' else r['verification_note']
    source.append(x)
out(A/'Stage25B6D_Source_Closure.csv',source)
verified={r['DOI'].lower() for r in source if r['original_measurement_status']=='VERIFIED_ORIGINAL_EXPERIMENT'}
assert len(verified)==8

study=[]; closure=[]
for r in eligible:
    s=source_by_doi[r['DOI'].lower()]
    is_verified=r['DOI'].lower() in verified
    study.append(dict(candidate_id=r['candidate_id'],candidate_name=r['canonical_name'],source_DOI=r['DOI'],study_id='STUDY-'+r['DOI'].lower() if is_verified else '',experiment_id=r['independent_experiment_id'],original_experiment='YES_VERIFIED' if is_verified else 'UNRESOLVED',experimental_material='PURE_STANDARD_OR_PURIFIED_PRODUCT' if is_verified else 'CANONICAL_LABEL_NOT_ORIGINALLY_RECHECKED',assay_method='AAPH_FLUORESCEIN_TROLOX' if is_verified else 'SOURCE_METHOD_NOT_CLOSED',original_table_location='Methods 2.3.4; Table 1' if r['DOI'].lower()==hayes else s['source_location'],independence_decision='ONE_VERIFIED_ORIGINAL_STUDY_CONTRIBUTION' if is_verified else 'UNRESOLVED',decision_basis='Own original experiment; one DOI contributes at most one study per candidate' if is_verified else 'Original matching result table or data origin remains unresolved',access_status='ORIGINAL_FULLTEXT_VERIFIED' if is_verified else s['fulltext_status'],unresolved_issue='' if is_verified else s['verification_note'],source_url=hayes_url if r['DOI'].lower()==hayes else s['source_url']))
for r in close6:
    ds=sorted({x['DOI'].lower() for x in by_candidate[r['candidate_id']]})
    vd=[d for d in ds if d in verified]
    n=len(vd)
    status='PASS_VERIFIED' if n>=2 else ('FAIL_ON_AVAILABLE_EVIDENCE' if len(ds)==1 else 'UNRESOLVED')
    closure.append(dict(candidate_id=r['candidate_id'],candidate_name=r['candidate_name'],canonical_rank=r['canonical_rank'],quantitative_record_N=len(by_candidate[r['candidate_id']]),distinct_DOI_N=len(ds),confirmed_independent_study_N=n,confirmed_source_DOIs=';'.join(vd),unresolved_source_N=len(ds)-n,eligibility_status=status,eligibility_interpretation='At least two original pure-compound studies verified' if n>=2 else ('Only one canonical source available; other studies not proven absent' if len(ds)==1 else 'One or more original source tables/data origins unresolved'),formal_v11_status='NOT_CREATED',source_basis='Stage25B.6D Source Closure; Stage25B.6C pairwise audit'))
out(A/'Stage25B6D_Study_Independence_Adjudication.csv',study)
out(A/'Stage25B6D_Candidate_Eligibility.csv',closure)
closure_by_id={r['candidate_id']:r for r in closure}
assert sum(r['eligibility_status']=='PASS_VERIFIED' for r in closure)==9

errors=[]
for r in error6:
    x=dict(r)
    if r['DOI'].lower()==hayes:
        x.update(error_type_verified='SD_VERIFIED_ORIGINAL_TABLE',error_value='3.57',error_scale='g Trolox/100 g dry compound',replicate_N='3',replicate_type='THREE_DETERMINATIONS_IN_SAME_STUDY',original_source_location='Hayes 2011 Table 1 footnote p.951',conversion_validity='SD scale conversion valid for same linear mass-to-molar factor; approximately 0.0431 mol TE/mol',confidence_in_extraction='ORIGINAL_TABLE_VERIFIED',CI_status='CI_NOT_ESTIMABLE')
    x['independent_study_N_from_replicates']='0'
    x['source_url']=hayes_url if r['DOI'].lower()==hayes else source_by_doi[r['DOI'].lower()]['source_url']
    errors.append(x)
out(A/'Stage25B6D_Error_and_Replicate_Audit.csv',errors)
typed=sum(r['error_type_verified'] in ('SD_VERIFIED_ORIGINAL_TABLE','SD_VERIFIED_IN_PRIOR_CANONICAL_AUDIT') for r in errors)
numeric=sum(bool(r['error_value']) for r in errors)
assert typed==4 and numeric==27

profiles=[]
for r in ranking:
    cid=r['candidate_id']; cc=closure_by_id[cid]; es=[x for x in errors if x['candidate_id']==cid]
    profiles.append(dict(candidate_id=cid,candidate_name=r['canonical_name'],canonical_rank=r['rank'],H_ORAC_median_mol_TE_per_mol=r['median_H_ORAC_mol_TE_per_mol'],canonical_A_B1_record_N=len(by_candidate[cid]),confirmed_independent_study_N=cc['confirmed_independent_study_N'],independence_status=cc['eligibility_status'],typed_SD_record_N=sum(x['error_type_verified'] in ('SD_VERIFIED_ORIGINAL_TABLE','SD_VERIFIED_IN_PRIOR_CANONICAL_AUDIT') for x in es),numeric_error_record_N=sum(bool(x['error_value']) for x in es),heterogeneity_flag=r['heterogeneity_flag'],CI_status='CI_NOT_ESTIMABLE',ranking_uncertainty='RANK_UNCERTAINTY_NOT_ESTIMABLE',evidence_scope='IN_VITRO_H_ORAC_ONLY',formal_rank_changed='NO'))
out(A/'Stage25B6D_HORAC_Evidence_Profile.csv',profiles)
cr=[dict(change_request_id='6D-'+r['change_request_id'],change_type=r['change_type'],candidate_id=r['candidate_id'],source_DOI=r['source_DOI'],proposed_change=r['proposed_change'],evidence_basis=r['evidence_basis'],potential_impact=r['potential_impact'],review_status='PENDING_HUMAN_REVIEW',action_taken='NONE') for r in cr6]
cr += [dict(change_request_id='6D-CR-015',change_type='SOURCE_AND_ERROR_CLOSURE',candidate_id='AFF-0085',source_DOI=hayes,proposed_change='Approve source-level verification and typed SD addition to future evidence metadata only',evidence_basis='Original Hayes Methods 2.3.4 and Table 1 footnote',potential_impact='PRECISION_PROFILE_NO_RANK_CHANGE',review_status='PENDING_HUMAN_REVIEW',action_taken='NONE'),dict(change_request_id='6D-CR-016',change_type='CORRECT_6C_TARGETED_SOURCE_INTERPRETATION',candidate_id='AFF-0014;AFF-0034;AFF-0011',source_DOI='10.3389/fnut.2022.882458',proposed_change='Replace model-only description with original AAPH-fluorescein fixed-concentration AUC experiment; keep out of TE primary',evidence_basis='Original Methods and Figures 2–5; no Trolox-equivalent conversion in paper',potential_impact='EVIDENCE_COVERAGE_NOT_PRIMARY_RANK',review_status='PENDING_HUMAN_REVIEW',action_taken='NONE')]
out(A/'Stage25B6D_Proposed_Change_Requests.csv',cr)

md(AD/'Stage25B6D_VitaminC_Reconciliation_CN.md', '''# Vitamin C 原始证据衔接

对象为 AFF-0104 L-Ascorbic acid，不能与 dehydroascorbic acid 等其他化学形式合并。Ou 2001 DOI 10.1021/jf010586o 的原始 Table 4 经出版社与定点公开来源检索仍未合法取得，历史记录中的 0.95 mol TE/mol 是未完成原表核实的转录，状态 `SOURCE_ACCESS_BLOCKED`。Carvalho 2023 原文 Methods 与 Table 3 报告 L-ascorbic acid 0.53 ± 0.03 TE_AUC，使用 AAPH–fluorescein–Trolox；± 类型未明确，不能写作 SD。两篇书目及研究组不同，但 Ou 的原始实验表未核实，不能宣布双独立研究门槛通过。

Stage25B canonical 实验表没有 AFF-0104 记录；这是待逐来源 rubric v2.0 裁决的衔接缺口，不证明维生素 C 的实验无效。建议先取得 Ou 原表并复核纯品、剂量、单位、方法及数据独立性，再由人工批准 Change Request。此轮未迁移数据或更改排名。体外 H-ORAC 不等于人体抗氧化或临床效力。

原始入口：[Ou 2001](https://pubs.acs.org/doi/10.1021/jf010586o)，[Carvalho 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)。''')
md(AD/'Stage25B6D_Ranking_Readiness_CN.md', f'''# H-ORAC 证据闭环与排名准备度

现有 74 条 canonical 实验及 68 条 A/B1 记录未改动。16 个既有 DOI 中 {len(verified)} 个原始纯品/纯化产品实验可定位，{16-len(verified)} 个仍缺匹配原表或数据归属核实。28 种可排名候选中 9 种 `PASS_VERIFIED`、10 种 `UNRESOLVED`、9 种 `FAIL_ON_AVAILABLE_EVIDENCE`；最后一种状态仅指当前资料不足，不证明别处无研究。Ellagic acid 的 Hayes 2011 原表已恢复，但它仍只有一项 canonical 来源，不改变 9 种达标数。

27/68 条有数值误差，其中 4/68 条可明确为 SD；新增的一条为 Hayes 2011 Ellagic acid 151.77 ± 3.57 g Trolox/100 g dry compound，原文表注明确为三次测定的均值 ± SD。这三次测定仍是一项研究。Žuvela 2019 的 ln(ORAC) ± 不得直接作为 mol TE/mol 误差。跨研究 IQR 只描述离散性；候选物 95%CI 和排名概率仍不可估。

重要更正：Platzer 2022（10.3389/fnut.2022.882458）虽以 QSPR 为题，却有新做的纯品 AAPH–fluorescein ORAC 实验，包括 Morin 和 Naringin。原文以固定浓度 AUC 展示，未给可重建的 Trolox 当量转换，因此当前不能进入 mol TE/mol primary，亦不能称为纯模型预测。该更正列入待人工审批 CR。维生素 C 的 Ou Table 4 仍阻断。Top20 v1.0 与 rubric v2.0 保持不变；尚不足以生成 v1.1。''')
md(AD/'Stage25B6D_QC_Report_CN.md', f'''# Stage25B.6D QC

冻结 manifest {len(manifest)}/{len(manifest)} SHA256 匹配。74 条 canonical、157 种候选、68 条 A/B1 和冻结 Top20 未改动；B2/X 未进入 primary。现有来源核实 {len(verified)}/16，双独立研究通过 9/28。Hayes 原表把有数值误差记录从 26 增至 27、明确 SD 从 3 增至 4；未把三次测定当三项研究。未取得 Ou 原表，不使用二手值补齐；未生成 CI/p 值；Platzer 原始 AUC 与 TE 构念分开。全部 {len(cr)} 项 CR 待人工审批。未批量处理 1,641 pending，未生成或冻结 v1.1。''')

# Track B: an endpoint-specific dictionary, never a numerical composite score.
dimensions={
 'D1':('抗氧化活性','Antioxidant Activity','特定化学或生物实验体系中的可观测抗氧化终点','比较同构实验终点，识别机制差异','ORAC-FL;DPPH;ABTS;FRAP;CUPRAC;CAA;oxidative-stress endpoints','数值及方法元数据','原单位；仅有效换算后报告共同单位','原始研究 Methods、结果表、单位与条件','化合物身份及实验终点可追溯','食品提取物数值不得归给单体；预测值不算实测','NOT_SEARCHED;SOURCE_INACCESSIBLE;NOT_APPLICABLE','特定体系内活性大小','人体健康获益或跨方法数值相加'),
 'D2':('证据可靠性','Evidence Reliability','针对指定终点与结论的来源、设计、独立性和偏倚评价','判断结论能否由原始证据支撑','originality;independent study N;design;precision;heterogeneity;comparability;completeness;bias;claim fit','分类及研究计数','研究项数；分类状态','逐篇原文、方法、实验表及数据复用比对','与具体终点和结论绑定','DOI 数、技术重复或综述不能代替独立研究','UNRESOLVED;SOURCE_INACCESSIBLE;NOT_SEARCHED','特定结论的证据强弱','物质永久固定的全局可信度'),
 'D3':('研究成熟度','Research Maturity','一般抗氧化及特定方法研究在时间与原始研究数量上的积累','识别研究覆盖与新近性','earliest year;latest year;span;deduplicated original N;recent 5y N;recent 10y N;assay-specific N','年份与去重计数','年；项研究','可解析书目及原文；明确去重','研究主题与实验来源界定','元数据记录数不等于独立原始研究','METADATA_ONLY;YEAR_UNRESOLVED;NOT_SEARCHED','证据积累范围','抗氧化效力或临床效果'),
 'D4':('生物学相关性','Biological Relevance','从细胞、动物到人体的暴露、机制与结果适切性','评价实验条件到应用目标的外推距离','cell;animal;human observational;human intervention;dose;duration;outcome;mechanism','设计、剂量、结果方向','模型/暴露单位按原文','原始研究设计、模型、暴露和结局','身份、剂量与对照可查','化学 ORAC 不作为人体获益替代','NOT_SEARCHED;OUTCOME_UNVERIFIED','模型内可观察的生物反应','跨物种或人体因果推断'),
 'D5':('应用可行性','Application Feasibility','目标用途所需的稳定性、供应、暴露、安全和工艺条件','判断候选进入开发或干预的实际约束','stability;processing;bioavailability;safety;food source;dose feasibility;availability;application limits','定性/定量、按场景','剂量、暴露、浓度等原单位','原始稳定性、药代、安全、加工与法规来源','产品/人群/剂量场景明确','食品中存在不等于可用剂量或安全','NOT_SEARCHED;IDENTITY_UNRESOLVED','已核实场景下的开发条件','批准用途或安全性保证'),
}
indicator_specs=[
 ('D1','ORAC_FL','水相 ORAC-FL','Hydrophilic ORAC-FL','AAPH–fluorescein–Trolox 纯品动力学终点','mol TE/mol','同一构念、身份、方法和换算可复核','缺 Trolox/单位不可换算；脂相或提取物','H_ORAC_CANONICAL'),
 ('D1','DPPH','DPPH 清除','DPPH radical scavenging','稳定自由基吸光度变化，报告浓度/时间','原始 IC50 或百分比','限定相同浓度/溶剂/时间比较','不换算为 ORAC','NOT_POPULATED'),
 ('D1','ABTS','ABTS 清除','ABTS radical cation scavenging','ABTS 阳离子自由基终点','原始 TEAC/IC50/百分比','同协议与浓度比较','不与 ORAC 数值相加','NOT_POPULATED'),
 ('D1','FRAP','铁还原能力','Ferric reducing antioxidant power','Fe3+ 还原终点','原始 Fe2+ 当量','同化学体系比较','不解释为过氧自由基清除','NOT_POPULATED'),
 ('D1','CUPRAC','铜还原能力','Cupric reducing antioxidant capacity','Cu2+ 还原终点','原始 Trolox 当量','同协议比较','不直接与 FRAP/ORAC 汇总','NOT_POPULATED'),
 ('D1','CAA','细胞抗氧化活性','Cellular antioxidant activity','细胞内荧光氧化应激代理终点','原始 CAA 单位','模型、暴露和细胞毒性均可核实','不等同人体效力','NOT_POPULATED'),
 ('D1','OX_STRESS','其他氧化应激终点','Other oxidative-stress endpoint','需指明具体模型和生物标志物','原始单位','有清楚实验模型和对照','不泛化为统一活性单位','NOT_POPULATED'),
 ('D2','ORIGINALITY','原始性与二次引用','Source originality','原始实验、综述、再分析或预测区分','分类','原文实验设计与结果定位','二次引用不新增研究','PARTIAL'),
 ('D2','INDEPENDENT_N','独立原始研究数','Independent original-study count','按数据采集而非 DOI 或孔位计数','项研究','逐研究实验来源可核查','技术/生物重复不单独计数','PARTIAL'),
 ('D2','PRECISION','测量精度','Measurement precision','SD/SE/CI、重复次数、类型与尺度','原尺度','误差定义和 n 原文明确','未定义 ± 不赋 SD','PARTIAL'),
 ('D2','HETEROGENEITY','研究间异质性','Between-study heterogeneity','经核实独立研究的终点离散与协议差异','原单位及描述指标','至少两项可比独立研究','记录 IQR 不等于 CI','PARTIAL'),
 ('D2','BIAS','偏倚与完整性','Bias and source completeness','选择性报告、来源访问和实验干扰','分类','完整 Methods/结果/QC','不可访问不作低风险推断','PARTIAL'),
 ('D3','EARLIEST','最早原始发表年','Earliest original publication year','去重后最早相关原始研究年份','年','书目/原文核实','异常年份不猜测','METADATA_ONLY'),
 ('D3','LATEST','最近原始发表年','Latest original publication year','去重后最近相关原始研究年份','年','书目/原文核实','未来年份标记待核','METADATA_ONLY'),
 ('D3','SPAN','研究跨度','Research span','最早至最近原始研究的包含端点年数','年','起止年均有效','缺失不按零年','METADATA_ONLY'),
 ('D3','ORIGINAL_N','去重原始研究数','Deduplicated original-study count','按实验/队列去重的原始研究数','项研究','全文或稳定研究标识','metadata publication N 不冒充 study N','NOT_POPULATED'),
 ('D3','RECENT_5_10','近5年与10年研究','Recent 5- and 10-year studies','按明确截点的原始研究数','项研究','出版日期与去重可核','不与论文热度混同','METADATA_ONLY'),
 ('D3','ASSAY_N','方法专项研究数','Assay-specific original-study count','指定实验方法的独立原始研究数','项研究','逐原文方法和数据独立性核实','一般抗氧化论文不自动计入','PARTIAL'),
 ('D4','CELL','细胞模型证据','Cell-model evidence','细胞种类、剂量、时长、结局和毒性','原始模型单位','原始对照实验','不外推人体','NOT_POPULATED'),
 ('D4','ANIMAL','动物模型证据','Animal-model evidence','物种、剂量、暴露、组织终点','原始剂量单位','原始对照实验','不直接外推人体','NOT_POPULATED'),
 ('D4','HUMAN_OBS','人体观察证据','Human observational evidence','暴露估计与结果关联','原始效应量','人群、混杂控制可核','关联不等于因果','METADATA_ONLY'),
 ('D4','HUMAN_INT','人体干预证据','Human intervention evidence','干预剂量、时长、预设结局','原始效应量','对照与依从性可核','不能以化学活性代替临床终点','METADATA_ONLY'),
 ('D5','STABILITY','稳定性与加工','Stability and processing fit','热/光/pH/配方稳定与加工损失','原始条件单位','目标食品工艺条件','单一体外条件不泛化','NOT_POPULATED'),
 ('D5','BIOAVAIL','生物利用度与暴露','Bioavailability and exposure','吸收、代谢、达到作用浓度的可行性','浓度/剂量','人体或适切模型数据','体外效力不等于可达暴露','NOT_POPULATED'),
 ('D5','SAFETY','安全与剂量','Safety and dose feasibility','不良反应、相互作用和适用人群','原始剂量','人体/权威安全资料','缺报告不等于安全','NOT_POPULATED'),
 ('D5','SOURCE','食品来源与供应','Food source and availability','来源、含量、纯度、供应链','原始含量单位','身份与具体来源可核','food_sources 字段不证实可规模化供应','METADATA_ONLY'),
]
indicators=[]
for dim,code,cn,en,definition,unit,include,exclude,current in indicator_specs:
    d=dimensions[dim]
    indicators.append(dict(dimension_id=dim,dimension_name_cn=d[0],dimension_name_en=d[1],dimension_scientific_definition=d[2],dimension_evaluation_purpose=d[3],indicator_id=code,indicator_name_cn=cn,indicator_name_en=en,indicator_definition=definition,data_type=d[5],unit=unit,original_source_requirement=d[7],inclusion_rule=include,exclusion_rule=exclude,missing_state=d[10],supported_claim=d[11],unsupported_claim=d[12],food_ingredient_applicability='YES_CONTEXT_SPECIFIC',nutrition_health_applicability='YES_CONTEXT_SPECIFIC',mechanistic_research_applicability='YES_CONTEXT_SPECIFIC',current_data_status=current))
out(B/'Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv',indicators)

assay_specs=[
 ('ORAC-FL','Peroxyl radical scavenging','AAPH; fluorescein kinetic decay','Net AUC relative to Trolox','mol TE/mol if valid','HAT-dominant chemical assay','Only same aqueous pure-compound construct comparable'),
 ('DPPH','Stable radical reduction','DPPH absorbance','IC50 or percent inhibition','original','SET/HAT mixed, solvent dependent','Do not combine numerically with ORAC'),
 ('ABTS','Radical cation reduction','ABTS radical cation absorbance','TEAC or IC50','original','SET/HAT mixed','Do not combine numerically with ORAC'),
 ('FRAP','Ferric reduction','Fe3+-TPTZ absorbance','Fe2+ equivalents','original','SET','Not a peroxyl scavenging measure'),
 ('CUPRAC','Cupric reduction','Cu2+ complex absorbance','Trolox equivalents or original','original','SET','Not interchangeable with FRAP'),
 ('CAA','Cellular oxidative-stress proxy','Cell DCF fluorescence with exposure','Cellular antioxidant activity','original','cell model','Requires cytotoxicity and exposure context'),
 ('OTHER_OX_STRESS','Model-specific oxidative stress','Defined cell/animal/human marker','Specific biomarker','original','biological','No universal potency conversion'),
 ('HORAC_HYDROXYL','Hydroxyl radical absorbance capacity','Hydroxyl radical source','Method-specific endpoint','original','chemical','Acronym HORAC here is not hydrophilic H-ORAC-FL'),
]
out(B/'Antioxidant_Assay_and_Evidence_Type_Dictionary.csv',[dict(assay_method=a,reaction_mechanism=b,experimental_system=c,endpoint=d,unit_rule=e,evidence_type=f,claim_boundary=g,required_source='Original Methods and results; compound identity; conditions') for a,b,c,d,e,f,g in assay_specs])
scenario_specs=[
 ('Food Ingredient Development','稳定性、风味/加工与安全条件下的配料表现','D5 safety;stability;processing;D1 assay-specific activity','D2 independence;D3 maturity;D4 bioavailability','Identity verified; safe intended-use exposure; at least one reproducible relevant assay recommended','Food-use safety, impurities, allergen, interactions','In vitro assay does not establish shelf-life benefit','Food matrix stability and human exposure if claims are made'),
 ('Nutrition and Health Intervention','特定人群和剂量下的健康结局','D4 human intervention;D5 safety/exposure','D1 chemistry;D2 reliability;D3 maturity','Human endpoint evidence for efficacy claim; dose and safety evidence','Adverse events, interactions, vulnerable populations','ORAC/animal result not a clinical effect','Controlled human studies with prespecified outcomes'),
 ('Mechanistic Research','解析清除/信号通路与剂量-反应机制','D1 mechanism-specific assays;D4 cell/animal model','D2 source and design;D3 study coverage;D5 reagent stability','Reproducible identity, orthogonal assays and relevant controls','Assay interference, off-target toxicity, redox cycling','Mechanistic signal not a product or clinical claim','Orthogonal perturbation and replication'),
]
out(B/'Application_Scenario_Applicability_Matrix.csv',[dict(application_scenario=a,scientific_goal=b,core_indicators=c,supporting_indicators=d,minimum_evidence_recommendation=e,safety_focus=f,invalid_inference=g,additional_evidence=h,weight='NOT_SET_V0_1',ranking='NOT_GENERATED') for a,b,c,d,e,f,g,h in scenario_specs])

identity=[]; availability=[]
for c in candidate:
    cid=c['candidate_id']; hist=history_by_id[cid]; cc=closure_by_id.get(cid)
    cid_raw=c['PubChem_CID']; key=c['InChIKey']; synonyms=c['synonyms_used']
    status='IDENTITY_UNRESOLVED' if not key or not cid_raw else 'IDENTIFIER_PRESENT_NOT_STRUCTURALLY_RECHECKED'
    identity.append(dict(candidate_id=cid,canonical_name_en=c['canonical_name'],canonical_name_cn='NOT_CURATED',synonyms=synonyms,PubChem_CID_as_recorded=cid_raw,InChIKey=key,identity_status=status,form_and_stereochemistry_rule='Do not merge aglycone/glycoside, L/D forms, oxidized/reduced forms or unspecified salts',source='data/literature_screening/master/Literature_Screening_Candidate_Master.csv',proposed_universe_change='NONE',human_review='REQUIRED_IF_IDENTITY_CONFLICT'))
    for dim in dimensions:
        if dim=='D1':
            st='AVAILABLE_VERIFIED' if cc and int(cc['unresolved_source_N'])==0 else ('AVAILABLE_UNVERIFIED' if cc else 'NOT_SEARCHED')
            basis='H-ORAC-specific source audit: VERIFIED means every A/B1 source for this candidate was checked against its original report; no cross-assay completeness implied' if cc else 'No full cross-assay evaluation in v0.1'
        elif dim=='D2':
            st='AVAILABLE_UNVERIFIED' if cc else 'NOT_SEARCHED'; basis='H-ORAC-specific independence/precision partial' if cc else 'No endpoint-specific reliability audit'
        elif dim=='D3':
            st='AVAILABLE_UNVERIFIED' if hist['year_parse_status']!='MISSING_OR_INVALID' else 'AVAILABLE_UNVERIFIED'; basis='Stage25A metadata publication history; original-study dedup not complete'
        elif dim=='D4':
            st='AVAILABLE_UNVERIFIED' if value(c['human_study_N']) and value(c['human_study_N'])>0 else 'NOT_SEARCHED'; basis='Human-study metadata count only; outcomes not adjudicated' if st=='AVAILABLE_UNVERIFIED' else 'No outcome-level biological audit'
        else:
            st='NOT_SEARCHED'; basis='Food source metadata alone is not application feasibility'
        if status=='IDENTITY_UNRESOLVED': st='IDENTITY_UNRESOLVED'
        availability.append(dict(candidate_id=cid,candidate_name=c['canonical_name'],evidence_dimension=dim,availability_status=st,coverage_basis=basis,verified_original_study_N=cc['confirmed_independent_study_N'] if dim in ('D1','D2') and cc else '',data_source='Stage25B6D audit' if dim in ('D1','D2') and cc else ('Stage25A metadata' if dim in ('D3','D4') else ''),missing_interpretation='Missing or unsearched does not imply ineffectiveness',last_verified_date=DATE))
out(B/'Candidate_Identity_and_Synonym_Audit.csv',identity)
out(B/'Candidate_157_Data_Availability_Matrix.csv',availability)
assert len(identity)==157 and len(availability)==785

md(BD/'Comprehensive_Antioxidant_Framework_v0.1_CN.md', '''# 综合抗氧化候选功能物质评价框架 v0.1

本框架以现有 157 种候选物及原 candidate_id 为边界，服务食品与功能配料开发、营养健康干预、机制研究三个场景。共享的是身份、原始研究与终点证据底座，不共享一个未经论证的总权重或总排名。五维依次为 D1 抗氧化活性、D2 证据可靠性、D3 研究成熟度、D4 生物学相关性、D5 应用可行性；每个维度的中英名称、定义、二级指标、单位、来源、纳排和可支持/不能支持的结论，见双语指标字典。

D1 必须先按方法与实验体系拆分；H-ORAC-FL 的 mol TE/mol 与 DPPH、ABTS、FRAP、CUPRAC、CAA 不可直接相加。D2 绑定具体终点和论断，独立研究数、测量精度、异质性与偏倚各自展示。D3 区分一般抗氧化研究积累与方法专项研究积累，不代表效力。D4 从化学、细胞、动物到人体按模型和暴露逐级解释，不作自动外推。D5 按安全、加工、稳定、来源、剂量与暴露核实可行性，食品存在性并非安全或可达剂量证据。

每个候选×维度保留 `AVAILABLE_VERIFIED`、`AVAILABLE_UNVERIFIED`、`NOT_REPORTED`、`NOT_SEARCHED`、`SOURCE_INACCESSIBLE`、`NOT_APPLICABLE`、`IDENTITY_UNRESOLVED` 等可扩展状态。v0.1 数据矩阵只填已建立来源链的覆盖状态；`NOT_SEARCHED` 不代表无效。任何综合优选前应先确定应用场景、待支持的具体论断、最低证据门槛和缺失处理，并预注册权重或采用非加权多准则比较；本轮不评分、不输出综合 Top20、不修改候选全集。''')
md(BD/'Comprehensive_Antioxidant_Indicator_Guide_v0.1_CN.md', '''# 指标使用说明 v0.1

先确认 candidate_id、化学形式、异构体和纯度，再明确研究问题与应用场景。每条数据应保留 `assay_method`、`reaction_mechanism`、`experimental_system`、`endpoint`、`original_value`、`original_unit`、仅在有效时填入的 `normalized_value` 与依据、实验条件、DOI 和证据状态。缺失保留缺失，未检索保留未检索。D2 的研究独立性按原始数据采集判断，非按 DOI 或测量孔计数；D3 的论文元数据不得冒充原始研究数。D4 需记录模型、剂量/暴露、时长、结局、机制、方向、研究设计和外推限制。D5 仅建立安全、加工、稳定、供应与暴露所需字段，暂无数据的条目不填零。

判读顺序：先终点适配，再来源原始性与身份，再单位和方法可比性，然后研究级重复、精度与异质性，最后判断场景相关性。体外 H-ORAC 的高值只能支持该化学测定条件下的容量陈述，不能直接支持人体抗氧化或临床疗效。''')
md(BD/'Evidence_Grading_and_Claim_Boundaries_CN.md', '''# 证据分级与论断边界

证据等级必须是“候选物×终点×论断×场景”的判断，不建立永久的物质总等级。原始方法和结果表可核查、身份与单位明确、实验独立且无重要未解决干扰者，可支撑相应实验终点的有限比较；原文不可取得或结果归属不明则 `UNRESOLVED`，不是阴性结果。技术重复增加测量精度信息，不增加独立研究数。预测模型与实测值分列。不同方法的数值不自动换算，食品提取物结果不归给单一成分。

化学实验支持化学体系陈述；细胞实验支持该模型与剂量下的反应；动物实验不直接证成人体效力；人体观察研究通常支持关联；受控人体干预才可能支持限定人群、剂量和结局的干预因果论断，仍需风险与复现评估。`High confidence` 不等于 95% 概率，IQR 不是 95%CI，缺失误差不是零。''')
available_counts=Counter(r['availability_status'] for r in availability)
md(BD/'Comprehensive_Framework_Feasibility_Report_CN.md', f'''# 框架 v0.1 可行性

157 种候选均保留原 candidate_id，生成 785 个候选×维度状态。D1 仅对已有 H-ORAC canonical 范围提供来源级可用性，其他 DPPH/ABTS/FRAP/CUPRAC/CAA 尚未逐候选审计；D2 只对 28 种可排名候选有部分 H-ORAC 独立性/误差信息；D3 继承 Stage25A 论文元数据，不能称为经全文确认的独立研究数量；D4 只有部分人体研究的元数据计数，尚无结局审定；D5 尚未开展可行性原始证据评价。矩阵状态总计：{dict(available_counts)}。现阶段可提供证据覆盖和缺口地图，不可形成五维综合分数、通用 Top20 或人体效力排序。''')
md(BD/'Framework_v0.1_QC_Report_CN.md',f'''# 框架 v0.1 QC

身份表 {len(identity)} 行，与候选 master 的 157 个唯一 candidate_id 一一对应；维度矩阵 {len(availability)} 行，每候选 5 行且无重复键。双语字典 {len(indicators)} 个二级指标、五维均有定义、单位、纳排和论断边界。三场景均未设权重；无综合评分或综合 Top20；缺失未填零。Stage25A 人体论文计数和一般研究历史仅标为元数据级，未误写为已核实疗效或研究独立性。''')

# Joint: a 157-row profile is explicitly a coverage prototype, not a score.
joint=[]; gaps=[]
for c in candidate:
    cid=c['candidate_id']; cc=closure_by_id.get(cid); rr=rank_by_id.get(cid); h=history_by_id[cid]
    human=value(c['human_study_N']) or 0
    joint.append(dict(candidate_id=cid,candidate_name=c['canonical_name'],H_ORAC_activity_mol_TE_per_mol=rr['median_H_ORAC_mol_TE_per_mol'] if rr else '',H_ORAC_evidence_status=cc['eligibility_status'] if cc else 'NOT_SEARCHED_FOR_RANKABLE_DATA',independent_study_N=cc['confirmed_independent_study_N'] if cc else '',measurement_uncertainty='TYPED_SD_PARTIAL_CI_NOT_ESTIMABLE' if cc and any(x['candidate_id']==cid and x['error_type_verified'] in ('SD_VERIFIED_ORIGINAL_TABLE','SD_VERIFIED_IN_PRIOR_CANONICAL_AUDIT') for x in errors) else ('ERROR_TYPE_UNRESOLVED_OR_NOT_REPORTED' if cc else 'NOT_SEARCHED'),research_maturity='METADATA_ONLY_'+h['year_parse_status'],other_antioxidant_assay_coverage='NOT_SEARCHED_V0_1',biological_evidence_coverage='HUMAN_PUBLICATION_METADATA_UNVERIFIED' if human>0 else 'NOT_SEARCHED_V0_1',application_evidence_coverage='NOT_SEARCHED_V0_1',major_evidence_gaps=';'.join(([f"{cc['unresolved_source_N']} H-ORAC source(s) unresolved"] if cc and int(cc['unresolved_source_N']) else [])+['Cross-assay; biological outcome; application feasibility not adjudicated']),claim_limitations='H-ORAC in vitro chemistry is not human efficacy; no composite score',profile_status='PROTOTYPE_PARTIAL',source='Stage25B canonical ranking; Stage25B6D; Stage25A metadata'))
    if cc and cc['eligibility_status']!='PASS_VERIFIED':
        gaps.append(dict(priority='P0' if cc['eligibility_status']=='UNRESOLVED' else 'P1',candidate_id=cid,candidate_name=c['canonical_name'],dimension='D1_D2',evidence_gap='Original H-ORAC study independence / source closure',current_state=cc['eligibility_status'],needed_evidence='Original matching full text, experiment provenance and data reuse check',claim_blocked='Two-study qualification for future ranking',approval_status='PENDING_HUMAN_REVIEW'))
    if h['year_parse_status']=='MISSING_OR_INVALID':
        gaps.append(dict(priority='P2',candidate_id=cid,candidate_name=c['canonical_name'],dimension='D3',evidence_gap='Invalid or missing publication year',current_state=h['metadata_QC_status'],needed_evidence='Original bibliographic publication date',claim_blocked='Research-maturity time span',approval_status='PENDING_HUMAN_REVIEW'))
gaps.append(dict(priority='P0',candidate_id='AFF-0104',candidate_name='L-Ascorbic acid',dimension='D1_D2',evidence_gap='Ou 2001 original Table 4 unavailable',current_state='SOURCE_ACCESS_BLOCKED',needed_evidence='Lawful original Table 4 and source-specific v2 rubric adjudication',claim_blocked='Vitamin C canonical reconciliation',approval_status='PENDING_HUMAN_REVIEW'))
gaps.append(dict(priority='P1',candidate_id='AFF-0014;AFF-0034',candidate_name='Morin; Naringin',dimension='D1',evidence_gap='Platzer original AUC lacks Trolox-equivalent normalization',current_state='ORIGINAL_AUC_VERIFIED_NOT_PRIMARY_COMPARABLE',needed_evidence='Original TE calibration or separate non-primary endpoint treatment',claim_blocked='mol TE/mol primary inclusion',approval_status='PENDING_HUMAN_REVIEW'))
out(J/'Candidate_Multidimensional_Evidence_Profile_v0.1.csv',joint)
out(J/'Priority_Evidence_Gap_List.csv',gaps)
field_map=[
 ('candidate_id','candidate_id','Direct identity join','YES','Identity must remain fixed'),
 ('canonical_name','candidate_name','Display label only','YES','Use candidate_id for joins'),
 ('median_H_ORAC_mol_TE_per_mol','H_ORAC_activity_mol_TE_per_mol','Copy canonical A+B1 median without recalculation','YES','In vitro chemical endpoint only'),
 ('confirmed_independent_study_N','independent_study_N','Study-level source audit','YES_FOR_28','No DOI proxy or technical repeats'),
 ('proposed_threshold_status','H_ORAC_evidence_status','Use 6D eligibility state','YES_FOR_28','Unresolved distinct from fail'),
 ('error_type_verified','measurement_uncertainty','Aggregate typed versus untyped availability','PARTIAL','No CI imputation'),
 ('earliest_original_publication_year','research_maturity','Metadata-only until source repair','PARTIAL','Not potency'),
 ('other_assays','other_antioxidant_assay_coverage','No existing systematic per-candidate audit','NO','NOT_SEARCHED'),
 ('human_study_N','biological_evidence_coverage','Metadata count only','PARTIAL','No effect inference'),
 ('application_feasibility','application_evidence_coverage','No source-level evaluation','NO','NOT_SEARCHED'),
]
out(J/'HORAC_to_Comprehensive_Framework_Field_Map.csv',[dict(source_field=a,target_field=b,mapping_rule=c,available_now=d,claim_guard=e) for a,b,c,d,e in field_map])
md(JD/'Comprehensive_Prioritization_Method_Options_CN.md','''# 综合优选方法备选

v0.1 不设权重，也不生成综合 Top20。下一阶段可考虑三种可预注册方案：其一，各场景分别设最低证据门槛，过门槛后按维度展示非支配候选（Pareto），避免把不可比单位相加；其二，按事先确定的场景目标和指标标准化规则做多准则决策分析，并对权重与缺失处理做敏感性分析；其三，先做研究组合而非物质总排名，按“证据缺口×可获得性×影响决策的可能性”安排补证。任何量化模型都需先解决身份、原始来源、跨方法可比性、人体结局和安全性，并由研究者批准权重与门槛。现阶段三方案均为方法选项，不是结果。''')
md(JD/'Dual_Track_Integration_QC_Report_CN.md',f'''# 双轨整合 QC

联合画像 {len(joint)} 行，candidate_id 与冻结 157 候选一一对应；H-ORAC 数值仅对原 28 种可排名候选填入，其他均空白而非零。独立研究数来自 6D 来源核查，研究成熟度明标 metadata-only，其他实验、生物结局和应用可行性未完成审定时标 `NOT_SEARCHED`。未把 H-ORAC 等同人体效力、未跨方法相加、未设置五维权重或综合分数。Track A 条件完成，Track B v0.1 框架完成，联合画像为阶段性原型。''')

# Track G: baseline inventory of every tracked file, preserving provenance.
tracked_raw=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT)
tracked=[x.decode('utf-8') for x in tracked_raw.split(b'\0') if x]
assert len(tracked)>=550
reg_by_path={r['canonical_path'].replace('\\','/'):r for r in registry}
text_index='\n'.join((ROOT/x).read_text(encoding='utf-8-sig',errors='replace') for x in ('PROJECT_FILE_INDEX_CN.md','docs/PROJECT_STAGE_INDEX_CN.md'))
inventory=[]; hash_groups=defaultdict(list)
for rel in tracked:
    p=ROOT/rel
    if not p.is_file(): continue
    digest=sha(p); hash_groups[digest].append(rel)
    role=reg_by_path.get(rel,{}).get('asset_role','') or ('SCRIPT' if rel.startswith(('scripts/','R/')) else ('ARCHIVE' if rel.startswith('archive/') else ('SCIENTIFIC_SUPPORT' if rel.endswith(('.csv','.md','.pdf','.png','.svg')) else 'PROJECT_SUPPORT')))
    protected=rel in {r['asset_path'] for r in manifest} or rel in ('CANONICAL_ASSET_REGISTRY.csv','data/class_specific_antioxidant/Human_Review_Log.csv') or 'Rubric' in rel
    priority='P0_CORE_SCIENTIFIC' if protected or rel.startswith('data/h_orac_stage25b/frozen/') else ('P1_PROCESS' if any(k in rel.lower() for k in ('qc','sync','review','adjudication','provenance','evidence','manifest')) else ('P2_REFERENCE' if rel.startswith('archive/') else 'P1_ACTIVE'))
    inventory.append(dict(file_path=rel,file_name=p.name,extension=p.suffix.lower(),file_size=p.stat().st_size,sha256=digest,git_tracked='YES',last_modified_or_commit=datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d'),scientific_role=role,canonical_status=reg_by_path.get(rel,{}).get('current_status','NOT_REGISTERED'),referenced_by='PROJECT_INDEX' if rel in text_index else ('CANONICAL_ASSET_REGISTRY' if rel in reg_by_path else 'NOT_DETERMINED_STATIC_SCAN'),duplicate_group='',proposed_action='RETAIN',action_rationale='Protected or process provenance' if priority.startswith(('P0','P1')) else 'No deletion authorized without content/reference review',approval_required='YES_FOR_DELETION_MOVE_MERGE',priority_class=priority))
for x in inventory:
    members=hash_groups[x['sha256']]
    x['duplicate_group']='SHA256-'+x['sha256'][:12] if len(members)>1 else ''
out(G/'Repository_File_Inventory.csv',inventory)
duplicate=[]
for digest,members in hash_groups.items():
    if len(members)<2: continue
    for rel in members:
        reg=reg_by_path.get(rel,{})
        duplicate.append(dict(file_path=rel,duplicate_group='SHA256-'+digest[:12],duplicate_type='BYTE_IDENTICAL',group_members=';'.join(members),unique_scientific_information='BYTE_IDENTITY_ONLY_CONTEXT_NOT_REVIEWED',effective_reference='YES' if rel in text_index or rel in reg_by_path else 'NOT_DETERMINED',rebuildable='NOT_ASSESSED',canonical_counterpart=next((x for x in members if x!=rel and x in reg_by_path),''),proposed_action='RETAIN_PENDING_CONTEXT_REVIEW',risk_level='HIGH' if rel in reg_by_path or rel.startswith('archive/') else 'MEDIUM',approval_status='PENDING_HUMAN_REVIEW',rationale='Byte match does not establish dispensability; freeze and provenance roles require review'))
for rel,new in [('docs/qc/stage25b6c/Stage25B6C_Revision_Readiness_Report_CN.md','docs/qc/stage25b6d/Stage25B6D_Ranking_Readiness_CN.md'),('docs/sync/CHATGPT_SYNC_STAGE25B6C.md','docs/sync/CHATGPT_SYNC_DUAL_TRACK_PHASE1.md')]:
    duplicate.append(dict(file_path=rel,duplicate_group='VERSION_CHAIN_6C_TO_PHASE1',duplicate_type='SUPERSEDED_VERSION',group_members=rel+';'+new,unique_scientific_information='YES_PRIOR_DECISION_AND_TIMEPOINT',effective_reference='YES',rebuildable='PARTIAL',canonical_counterpart=new,proposed_action='RETAIN_AS_PROVENANCE',risk_level='HIGH',approval_status='PENDING_HUMAN_REVIEW',rationale='Later report updates status but does not erase historical evidence or decisions'))
out(G/'Duplicate_and_Obsolete_File_Audit.csv',duplicate)
out(G/'File_Migration_and_Provenance_Map.csv',[dict(original_path=r['file_path'],proposed_new_path='',operation='NO_MOVE_EXECUTED',reason=r['rationale'],source_sha256=next((x['sha256'] for x in inventory if x['file_path']==r['file_path']),''),approval_status='PENDING_HUMAN_REVIEW') for r in duplicate])
md(G/'Proposed_File_Cleanup_Plan_CN.md',f'''# 文件清理建议（未执行）

本轮对 {len(inventory)} 个受 Git 管理文件建立 SHA256、大小、状态和初步科学角色清单；识别 {len(hash_groups)} 个不同字节哈希，其中 {sum(len(v)>1 for v in hash_groups.values())} 个存在字节相同的文件组。字节相同只证明内容相同，不证明冻结快照、引用路径或过程记录可删。旧 6C 报告与新 6D 报告是版本链，不是可直接合并的同义副本。

建议按风险逐组人工核查：先核对引用和科学角色，再比较人工批注、版本差异和可重建性。P0 原始证据、canonical、Rubric、冻结资产及关键脚本保留；P1 裁决/QC/Change Request/Human Review Log 保留；P2 历史报告可考虑标注归档但保留映射；P3 仅在证明无引用、可再生且无独有科学信息后才提议删除。本轮无已批准的删除、合并或移动；重复审计表中的任何建议均 `PENDING_HUMAN_REVIEW`。''')

md(G/'LATEST_PROJECT_STATUS_CN.md',f'''# 项目最新状态（{DATE}）

正式科学成果仍是 Stage25B.5 冻结的 H-ORAC primary Top20 v1.0；本轮没有生成 v1.1。Track A Stage25B.6D 为条件完成：16 个既有 DOI 中 {len(verified)} 个已定位原始纯品结果，8 个来源仍有原表/归属缺口；28 种候选中 9 种达到拟议双独立研究门槛。Hayes 2011 原文新增确认 Ellagic acid 的均值 ± SD；维生素 C 的 Ou Table 4 仍不可合法取得。Track B 完成五维、三场景框架 v0.1 和 157×5 数据覆盖矩阵，但生物结局与应用可行性尚未系统核实。Track G 建立唯一最新阅读入口及全仓库盘点；没有删除、合并、移动任何原资产。全部科学变更仍待研究者逐项批准。

可向导师汇报：H-ORAC 是体外化学测定；独立性、精度、研究成熟度和生物学相关性分别评价；新框架已形成可追溯的数据字典与缺口清单。暂不能宣称新版 Top20、综合 Top20、人体抗氧化效力或统计显著差异。''')
md(G/'CURRENT_DECISIONS_AND_GAPS.md',f'''# 当前决策与证据缺口

1. H-ORAC 双独立研究门槛：当前 9/28 可核实，通过名单在 6D 资格表；正式采用及 v1.1 修订仍需人工决定。阻碍正式修订。
2. 原表缺口：8/16 既有 DOI 仍有匹配结果或数据归属缺口；Ou 2001 Table 4 尤其影响 Vitamin C。建议合法获取原文并逐来源裁决，不能用二手值补表。阻碍相关候选纳入。
3. 误差：27/68 有数值，4/68 类型明确为 SD；CI 和排名概率不可估。建议优先补 Methods 与表注，不把技术重复当研究数。
4. Platzer 2022 更正：该 QSPR 论文同时报告原始纯品 ORAC AUC 实验；AUC 未给可重建 Trolox 当量，不进入 mol TE/mol primary。建议更正 6C 文字并单列非 primary 方法证据，需人工批准。
5. 综合框架：三场景最低证据门槛、指标权重和安全要求尚待研究者确认；v0.1 不评分。
6. 文件治理：发现相同字节组与历史版本链，但无自动删除/迁移。任何实质清理需逐项批准。''')
md(G/'README_CURRENT_REVIEW.md',f'''# Antioxidants Project 最新成果阅读入口

项目目标：基于原始研究证据，分别评价抗氧化活性、证据可靠性、研究成熟度、生物学相关性和应用可行性，为食品配料、营养健康干预及机制研究提供可解释的候选优选依据。本目录是唯一的最新成果**阅读入口**，不是新的权威数据目录；正式源文件仍在 `data/`、`docs/`、`scripts/` 等原路径。

当前阶段为双轨 Phase 1（{DATE}）。Track A 的 Stage25B.6D 条件完成，原始来源 {len(verified)}/16 已核实，双独立研究 9/28 达标；Vitamin C 原表缺口仍在。Track B 框架 v0.1 与 157 种候选覆盖矩阵已完成，但许多生物和应用指标尚未检索。最新**正式**排名仍为 Stage25B.5 Frozen Top20 v1.0；所有 6D 与综合框架文件是审计/方法版本，不是新的 Top20。

阅读顺序：第一步看 [最新状态](LATEST_PROJECT_STATUS_CN.md)；第二步看 [Track A 证据准备度](../docs/qc/stage25b6d/Stage25B6D_Ranking_Readiness_CN.md) 和 [Track B 框架](../docs/framework/Comprehensive_Antioxidant_Framework_v0.1_CN.md)；第三步查 [资格表](../data/h_orac_stage25b/stage25b6d/Stage25B6D_Candidate_Eligibility.csv)、[指标字典](../data/framework/Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv) 与 [157×5 覆盖矩阵](../data/framework/Candidate_157_Data_Availability_Matrix.csv)；第四步看 [当前决策](CURRENT_DECISIONS_AND_GAPS.md)、[双轨 QC](../docs/dual_track_phase1/Dual_Track_Integration_QC_Report_CN.md) 和 [清理建议](Proposed_File_Cleanup_Plan_CN.md)。完整资产路径见 [项目导航](PROJECT_NAVIGATION.md)。

可向导师汇报核查进展、双研究门槛及五维框架原则。暂不能宣称 v1.1、综合 Top20、人体疗效或统计显著性。建议先补关键原表、审批科学 CR 和场景门槛；不自动进入评分或文件清理。''')

sync_path=ROOT/'docs/sync/CHATGPT_SYNC_DUAL_TRACK_PHASE1.md'
new_science=[relative(p) for folder in (A,AD,B,BD,J,JD) for p in sorted(folder.iterdir()) if p.is_file()]
md(sync_path,f'''# Dual-Track Phase 1 同步给 ChatGPT

A. Git 基线为 `{BASE_SHA}`；提交后的最新 SHA 应以仓库 `git rev-parse HEAD` 或 Codex 最终回复为准。把当前提交的 SHA 写进同一提交内会产生自引用哈希，因此本文件不伪造未来 SHA。

B. Track A：Stage25B.6D 条件完成。16 DOI 中 {len(verified)} 原始纯品/纯化产品结果已定位，8 个仍有缺口。C. Track B：五维、三场景 v0.1 框架、{len(indicators)} 项双语二级指标及 157×5 覆盖矩阵已建，无权重/综合排名。D. Track G：`current_review/` 作为唯一阅读入口，全仓库盘点与重复审计完成，无实质删除、移动、合并。

E. 28 种 H-ORAC 候选：9 `PASS_VERIFIED`、10 `UNRESOLVED`、9 `FAIL_ON_AVAILABLE_EVIDENCE`。F. Vitamin C：Carvalho 2023 0.53±0.03 原表已定位，Ou 2001 Table 4 仍阻断，未迁入 canonical。G. 误差：27/68 有数值，4/68 类型明确为 SD；ln(ORAC) ± 不能直接搬到 mol TE/mol，CI/排名概率不可估。H. 框架分别评价 D1 活性、D2 可靠性、D3 成熟度、D4 生物学相关性、D5 应用可行性。I. 157 候选各有 5 个覆盖状态，未检索不作阴性。J. 从 `current_review/README_CURRENT_REVIEW.md` 按四步阅读，导航链接直接指向权威源文件，无第二套 canonical 拷贝。

K. 仓库基线受 Git 管理文件 {len(inventory)} 个，字节重复组 {sum(len(v)>1 for v in hash_groups.values())} 个；只提出逐组审查，不自动清理。L. 本轮新增科学资产 {len(new_science)} 个，另建 `current_review/` 导航/盘点和本同步文件；预计只修改必要根索引/registry，无移动或删除。新增科学资产路径：{'; '.join(new_science)}。

M. 所有 {len(cr)} 项 6D CR、双研究门槛、Vitamin C 衔接、Platzer 文字更正、三场景门槛/权重以及任何文件清理均待人工批准。N. 可向导师汇报原始来源审计进展、误差边界、五维框架及缺口。O. 不可宣称新版 Top20、人体抗氧化效力、跨方法总分或统计显著差异。P. 下一步建议：合法获取关键原表，逐项批准科学 CR，定义各场景最低证据要求后再考虑优选方法；本轮不启动评分或清理。''')

# Current review is link-first. Registry items remain in their authoritative paths.
special=[
 ('最新状态','Latest project status',relative(G/'LATEST_PROJECT_STATUS_CN.md'),'Track G','CURRENT_REPORT','P0'),
 ('Track A 证据准备度','H-ORAC ranking readiness',relative(AD/'Stage25B6D_Ranking_Readiness_CN.md'),'Track A','CURRENT_REPORT','P0'),
 ('Track A 候选资格','H-ORAC candidate eligibility',relative(A/'Stage25B6D_Candidate_Eligibility.csv'),'Track A','CURRENT_REPORT','P0'),
 ('Track A 维生素C衔接','Vitamin C reconciliation',relative(AD/'Stage25B6D_VitaminC_Reconciliation_CN.md'),'Track A','PENDING_REVIEW','P1'),
 ('Track B 五维框架','Comprehensive antioxidant framework',relative(BD/'Comprehensive_Antioxidant_Framework_v0.1_CN.md'),'Track B','CURRENT_REPORT','P0'),
 ('双语指标字典','Bilingual indicator dictionary',relative(B/'Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv'),'Track B','CURRENT_REPORT','P1'),
 ('157种候选覆盖矩阵','Candidate data availability matrix',relative(B/'Candidate_157_Data_Availability_Matrix.csv'),'Track B','CURRENT_REPORT','P1'),
 ('联合证据画像','Multidimensional evidence profile',relative(J/'Candidate_Multidimensional_Evidence_Profile_v0.1.csv'),'Joint','CURRENT_REPORT','P1'),
 ('文件清理建议','Proposed cleanup plan',relative(G/'Proposed_File_Cleanup_Plan_CN.md'),'Track G','PENDING_REVIEW','P0'),
 ('最新同步','Dual-track ChatGPT sync',relative(sync_path),'Joint','CURRENT_REPORT','P0'),
 ('冻结Top20 v1.0','Frozen primary H-ORAC Top20 v1.0','data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv','Formal','CANONICAL_SOURCE','P0'),
]
role_cn={'DATA':'数据','REPORT':'报告','SYNC':'阶段同步','METHOD':'方法','FIGURE':'图','SCRIPT':'脚本','PROJECT NAVIGATION':'项目导航','FINAL ASSESSMENT':'最终评估'}
items={}
for r in registry:
    rel=r['canonical_path'].replace('\\','/')
    if rel in ('current_review/CURRENT_DELIVERABLES_INDEX.csv','current_review/PROJECT_NAVIGATION.md'): continue
    if not (ROOT/rel).is_file(): continue
    stage=r['stage_origin']
    status='CANONICAL_SOURCE' if r['current_status']=='ACTIVE_CANONICAL' else ('PENDING_REVIEW' if r['current_status']=='ACTIVE_WORK_IN_PROGRESS' else 'CURRENT_REPORT')
    if stage.startswith(('25B.6A','25B.6B','25B.6C')): status='HISTORICAL_ARCHIVE'
    items[rel]=dict(title_cn=role_cn.get(r['asset_role'],'项目资产')+'：'+r['asset_name'],title_en=r['asset_name'],track='Formal/Previous stage' if status=='HISTORICAL_ARCHIVE' else r['scientific_module'],version=stage,status=status,canonical_source_path=rel,review_copy_path='',source_commit=BASE_SHA,sha256=sha(ROOT/rel),last_verified_date=DATE,supersedes=r['replacement_for'],review_priority='P0' if status=='CANONICAL_SOURCE' else 'P2',notes='Authoritative path; linked from current_review, not copied')
for title_cn,title_en,rel,track,status,priority in special:
    assert (ROOT/rel).is_file(),rel
    items[rel]=dict(title_cn=title_cn,title_en=title_en,track=track,version='v0.1' if track in ('Track B','Joint') else 'Stage25B.6D' if track=='Track A' else 'v1.0' if track=='Formal' else '2026-10-15',status=status,canonical_source_path=rel,review_copy_path='',source_commit=BASE_SHA,sha256=sha(ROOT/rel),last_verified_date=DATE,supersedes='Stage25B.6C diagnostic report' if rel.endswith('Stage25B6D_Ranking_Readiness_CN.md') else '',review_priority=priority,notes='Direct authority link; no review snapshot')
for folder,track in ((A,'Track A'),(AD,'Track A'),(B,'Track B'),(BD,'Track B'),(J,'Joint'),(JD,'Joint'),(G,'Track G')):
    for p in folder.iterdir():
        if not p.is_file() or p.name in ('CURRENT_DELIVERABLES_INDEX.csv','PROJECT_NAVIGATION.md','Repository_Governance_QC_Report_CN.md'): continue
        rel=relative(p)
        if rel not in items: items[rel]=dict(title_cn='当前成果：'+p.stem,title_en=p.stem,track=track,version='v0.1' if track in ('Track B','Joint') else 'Stage25B.6D' if track=='Track A' else DATE,status='CURRENT_REPORT' if track!='Track G' else 'PENDING_REVIEW',canonical_source_path=rel,review_copy_path='',source_commit=BASE_SHA,sha256=sha(p),last_verified_date=DATE,supersedes='',review_priority='P1' if track!='Track G' else 'P2',notes='Direct authority link; no snapshot')
index=[]
for i,(rel,r) in enumerate(sorted(items.items(),key=lambda pair:(pair[1]['review_priority'],pair[0])),1):
    index.append(dict(deliverable_id=f'DP1-{i:03d}',**r))
out(G/'CURRENT_DELIVERABLES_INDEX.csv',index)

from urllib.parse import quote
lines=['# 项目成果导航','',f'验证日期：{DATE}。本页以链接指向权威源文件；`review_files/` 未建立快照，故不存在第二套可修改的 canonical 数据。状态：`CANONICAL_SOURCE` 为正式源；`CURRENT_REPORT` 为本轮/仍有效报告；`PENDING_REVIEW` 需人工审批；`HISTORICAL_ARCHIVE` 保留既往诊断与来源链；`READ_ONLY_SNAPSHOT` 本轮为零。','', '| 中文名称 | English name | 用途/轨道 | 版本 | 状态 | 权威源文件 | current_review 阅读位置 | 最近验证 | 冻结 | 人工审批 | 被取代版本 |','|---|---|---|---|---|---|---|---|---|---|---|']
for r in index:
    rel=r['canonical_source_path']; href='../'+quote(rel,safe='/.-_')
    frozen='YES' if rel.startswith('data/h_orac_stage25b/frozen/') or 'Rubric_v2.0' in rel else 'NO'
    approval='YES' if r['status']=='PENDING_REVIEW' or r['track']=='Track A' and '6D' in r['version'] else 'NO'
    lines.append('| '+' | '.join([r['title_cn'].replace('|','/'),r['title_en'].replace('|','/'),r['track'].replace('|','/'),r['version'],r['status'],f'`{rel}`',f'[打开源文件]({href})',DATE,frozen,approval,r['supersedes'] or '—'])+' |')
md(G/'PROJECT_NAVIGATION.md','\n'.join(lines))

missing_links=[r['canonical_source_path'] for r in index if not (ROOT/r['canonical_source_path']).is_file()]
assert not missing_links
assert all(sha(p)==digest for p,digest in protected_before.items())
assert all(sha(ROOT/r['asset_path'])==r['sha256'] for r in manifest)
md(G/'Repository_Governance_QC_Report_CN.md',f'''# Repository governance QC

当前导航 {len(index)} 个权威源链接全部通过文件存在性检查；`CURRENT_DELIVERABLES_INDEX.csv` 每条源文件 SHA256 在生成时核实，`review_copy_path` 全空（没有竞争性快照）。冻结 manifest {len(manifest)}/{len(manifest)} 匹配；Rubric v2.0、74 条 canonical 实验和 Frozen Top20 v1.0 前后 SHA256 相同。全仓库盘点以任务启动时的 {len(inventory)} 个受 Git 管理文件为基线，新成果另由 current_review 索引登记。未删除、移动、合并原文件；关键脚本和旧路径未改变。清理建议全部待人工审批。提交与远端一致性需在 commit/push 后再次确认；本报告不预先宣称推送成功。''')
print(f'Phase1 generated: A sources={len(verified)}/16 pass=9 errors={numeric}/68 typed={typed}; B indicators={len(indicators)} availability={len(availability)}; inventory={len(inventory)} indexed={len(index)} duplicate_rows={len(duplicate)}')
