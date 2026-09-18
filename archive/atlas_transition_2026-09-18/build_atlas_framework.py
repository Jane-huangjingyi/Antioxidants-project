import csv, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DOC=ROOT/'docs'; STAGES=DOC/'stages'; DATA=ROOT/'data'; RDIR=ROOT/'R'
for d in [DOC,STAGES,DATA,RDIR]: d.mkdir(parents=True,exist_ok=True)
ARCH='archive/legacy_pre_class_balanced_2026-09-18'

stage_data=[
(0,'Scientific question definition','Completed / archived','最初 Phase 0–1 protocol 与决策日志','界定正常膳食、结构明确的原型小分子，并区分 chemical capacity、人体相关性、机制和 target evidence。','尚未形成候选数值榜；综合评分仍是初始框架。'),
(1,'Initial antioxidant candidate framework','Completed / superseded','v1.0 protocol、证据层级和数据字典','建立 100 分多维框架、候选宇宙规则、代谢物/安全性/协同与 T1–T5 target hierarchy。','多维评分无法用一句话回答“抗氧化能力按什么排”。'),
(2,'Antioxidant assay comparison','Completed / archived','assay audit、assay comparison/rubric','系统区分 HAT、ET、DPPH、ABTS、FRAP、CUPRAC、TRAP 和 ORAC，确认 assays 测量不同 constructs。','方法比较本身不产生 compound ranking。'),
(3,'ORAC-FL primary metric decision','Completed / superseded for all-class use','assay audit、primary metric recommendation、v2.0 protocol','把 ORAC-FL 冻结为酚类 H-arm 的 primary chemical-capacity metric；单位 mol TE/mol compound。','ORAC 不代表人体效果，也不适合所有类别。'),
(4,'H-ORAC / L-ORAC separation','Completed / active principle','v2.0 protocol、candidate scope','禁止未桥接的 H/L 混排；水相酚类与脂相 tocopherol/carotenoid 分臂。','历史 L-arm 数据覆盖不足。'),
(5,'Literature eligibility framework','Completed / active for H-ORAC','ORAC eligibility rubric、v2.1 addendum','定义 A/B1/B2/C/X；A 仅正式排名，A+B1 可做探索性历史比较。','Tier A 为 0；B1 仍来自非完全一致 protocols。'),
(6,'Candidate scope definition','Completed / superseded by Atlas taxonomy','Candidate Scope Definition','冻结正常膳食、结构明确单体及 H/L/special-case 范围。','仍以 ORAC compatibility 为中心，不能覆盖所有功能类别。'),
(7,'17-compound ORAC pilot','Completed / archived','17 个代表性候选与 record template','17 个候选首轮抽取；原始 pilot 得到 11 条 quantitative records、Tier A=0。','样本小，9 个候选缺 usable data；不能形成正式 Top20。'),
(8,'Historical exploratory ORAC ranking','Completed / archived','重判后的 16 条记录与 targeted search','拆分 B1/B2，使有限 H-ORAC 历史趋势可视化；17 个候选中形成探索性覆盖。','非标准化实验真值，L-arm 仍过少。'),
(9,'H-arm phenolic/polyphenolic candidate universe expansion','Completed / archived','candidate scope、PubChem identity、ORAC records','建立 50 个 food-derived H-arm phenolic/polyphenolic candidates。','文献覆盖受 popularity、probe、光学干扰和报告完整性影响。'),
(10,'Provisional H-ORAC Top20','Completed / archived','50-candidate universe 与 A/B1 records','形成 20 个 provisional phenolic candidates；初榜前五 quercetin、epicatechin、catechin、quercitrin、caffeic acid。','多数仅 single-study；不是跨类别 Top20。'),
(11,'Top20 evidence consolidation','Completed / archived','Top10 单研究复核、关键缺失候选 targeted search','新增独立 B1 后，排名前五更新为 epicatechin、catechin、quercetin、kaempferol、naringenin；quercetin/catechin/epicatechin 达 High。','Tier A 仍为 0；若干重要候选仍受方法缺口影响。'),
(12,'Ready / Conditionally ready shortlist','Completed / archived','consolidated ranking 与 assay-risk review','输出 20-row target-mapping shortlist，分 Ready、Conditionally ready、Not ready。','readiness 不是 biological importance 或最终 target list。'),
(13,'MASTER H-ORAC screening pipeline','Completed / archived supporting SOP','protocol、数据字典、脚本、change logs','形成总 SOP、11 个子 SOP、模板、checklist、双人复核和无 AI 指南。','仅适用于 H-ORAC phenolic workflow。'),
(14,'Class-balanced dietary antioxidant panel pilot','Completed as pilot / active source data','H-ORAC shortlist、暴露资料和类别要求','构建 20 个有机因子 + 5 个矿物情境节点；12 个 core 的 intake ratio 18.62-fold。','暴露估计异质；该 20-compound panel 不是最终设计。'),
(15,'Mechanism/pathway evidence master','Pilot completed / active ledger','class-balanced panel、核心机制原始文献','形成 25 条最小机制证据 ledger，按 Strong/Moderate/Limited/Predictive 编码。','未系统覆盖全部 compound×mechanism；空白表示未审阅。'),
(16,'Transition to Antioxidant Functional Factor Atlas','Framework completed; analyses not completed','Stage 0–15 历史、pilot panel 和 mechanism ledger','冻结 class-specific Top-N + profile-based cross-class comparison 的 Atlas 架构。','各类 candidate universe、正式 Top-N、完整机制综述、最终实验 panel 和 target mapping 尚未完成。')]

files={
0:['docs/Antioxidant_Screening_Protocol_CN.md','docs/Phase_0_1_Decision_Log_CN.md'],
1:['config/Evidence_Hierarchy_and_Scoring_Rubric.csv','config/Candidate_Universe_Data_Dictionary.csv'],
2:['docs/Antioxidant_Assay_Method_Audit_CN.md','config/Antioxidant_Assay_Comparison.csv'],
3:['docs/Primary_Antioxidant_Metric_Recommendation_CN.md','docs/Antioxidant_Screening_Protocol_v2.0_CN.md'],
4:['docs/Stage1_vs_Stage2_Framework_CN.md','docs/Candidate_Scope_Definition_CN.md'],
5:['config/ORAC_Literature_Eligibility_Rubric.csv','docs/Antioxidant_Screening_Protocol_v2.1_Addendum_CN.md'],
6:['docs/Candidate_Scope_Definition_CN.md'],7:['data/ORAC_Pilot_Raw_Extraction.csv','docs/ORAC_Pilot_Results_CN.md'],
8:['data/ORAC_Pilot_Reclassified_A_B1_B2.csv','data/ORAC_Exploratory_Compound_Summary.csv'],
9:['data/H_ORAC_Phenolic_Candidate_Universe.csv','data/H_ORAC_Phenolic_Literature_Records.csv'],
10:['data/H_ORAC_Provisional_Ranking.csv','figures/H_ORAC_Provisional_Top20.png'],
11:['data/Top20_Evidence_Consolidation_Records.csv','data/Top20_Ranking_Before_After.csv'],
12:['data/Target_Mapping_Shortlist_v0.1.csv'],13:['docs/MASTER_H_ORAC_SCREENING_PIPELINE_v1.0_CN.md','README_H_ORAC_PIPELINE.md'],
14:['Antioxidant_Panel_Master.csv','Antioxidant_Project_MASTER_Report_v1.0_CN.md'],15:['Antioxidant_Mechanism_Evidence_Master.csv'],
16:['Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md','docs/Antioxidant_Functional_Factor_Taxonomy_CN.md','docs/Class_Specific_TopN_Ranking_Rules_CN.md']}

stage_names=['Stage_00_Scientific_Question_CN.md','Stage_01_Initial_Candidate_Framework_CN.md','Stage_02_Antioxidant_Assay_Comparison_CN.md','Stage_03_ORAC_Primary_Metric_Decision_CN.md','Stage_04_H_vs_L_ORAC_Framework_CN.md','Stage_05_Literature_Eligibility_and_Tiering_CN.md','Stage_06_Candidate_Scope_Definition_CN.md','Stage_07_ORAC_Pilot_CN.md','Stage_08_Exploratory_ORAC_Ranking_CN.md','Stage_09_H_ORAC_Candidate_Universe_CN.md','Stage_10_Provisional_Top20_CN.md','Stage_11_Evidence_Consolidation_CN.md','Stage_12_Target_Mapping_Readiness_CN.md','Stage_13_MASTER_Pipeline_CN.md','Stage_14_Class_Balanced_Panel_Pilot_CN.md','Stage_15_Mechanism_Evidence_Framework_CN.md','Stage_16_Current_Transition_to_Functional_Factor_Atlas_CN.md']

def status_for(i,f):
 if i==16:return 'active'
 if i in (14,15):return 'supporting'
 return 'archived' if i!=4 and i!=5 else 'active principle / archived source'

for (i,name,status,inp,result,lim),fn in zip(stage_data,stage_names):
 frows='\n'.join(f'| `{(ARCH+"/"+f) if i<14 else f}` | 历史或当前阶段输出 | {status_for(i,f)} |' for f in files[i])
 why='前一阶段无法充分解决本阶段的操作性问题，因此需要单独冻结规则或补充证据。'
 if i==0: why='项目需要先区分 chemical antioxidant capacity、biological redox effect 与 translational priority，避免把不同问题混为一个排名。'
 nxt='进入下一阶段以解决当前限制。' if i<16 else '等待框架审核；随后按 NEXT_STEP_ROADMAP 执行，不自动开展候选扩展或 target mapping。'
 text=f'''# Stage {i:02d} — {name}\n\n## 1. Stage purpose\n\n解决：{result.split("；")[0]}。\n\n## 2. Why this stage was necessary\n\n{why}\n\n## 3. Input\n\n{inp}；仅使用项目现存数据、冻结决策与可追溯来源。\n\n## 4. Method\n\n审阅相应 protocol、结构化数据、脚本、图形和 change log；按当时冻结规则执行身份核对、assay 判定、证据分层、聚合或框架设计。未完成的动作不写成结果。\n\n## 5. Decision rules\n\n证据质量高于数量；化学能力不等于人体功效；H/L 不无条件混排；缺失数据不记为零；glycoside/aglycone、stereoisomer、salt/hydrate 不合并；direct target 与 pathway effect 分层。具体规则以本阶段列出的源文件为准。\n\n## 6. Output files\n\n| file | role | current status |\n| --- | --- | --- |\n{frows}\n\n## 7. Main results\n\n{result}\n\n## 8. Scientific interpretation\n\n该结果说明本阶段的操作性问题已达到“{status}”对应的完成度，并为下一步提供了可追溯输入。\n\n## 9. What this result does NOT mean\n\n它不证明 ORAC 高等于人体抗氧化效果高，不证明文献空白等于无机制，也不把 provisional/pilot 输出解释为最终跨类别排名。\n\n## 10. Limitations\n\n{lim}\n\n## 11. Decision made\n\n冻结状态：**{status}**。后续版本必须保留本阶段原始值、排除记录和变更原因。\n\n## 12. Next stage\n\n{nxt}\n'''
 (STAGES/fn).write_text(text,encoding='utf-8')

# Stage index
lines=['# PROJECT STAGE INDEX（CN）','', '本目录按真实科学逻辑重建 Stage 0–16。`Completed` 表示相应文件和结果确实存在；`Pilot` 或 `Provisional` 不能解释为最终结论；`Not completed` 明确保留。','', '| Stage | Stage name | Scientific question | Status | Key input | Key output | Main conclusion | Major limitation | File status |','|---:|---|---|---|---|---|---|---|---|']
for i,name,status,inp,res,lim in stage_data:
 lines.append(f'| {i} | {name} | 本阶段如何解决其对应操作性问题？ | {status} | {inp} | {files[i][0]} | {res} | {lim} | {"active" if i==16 else ("supporting" if i in (14,15) else "archived/superseded")} |')
(DOC/'PROJECT_STAGE_INDEX_CN.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Candidate master derived from pilot without modifying values
with open(ROOT/'Antioxidant_Panel_Master.csv',encoding='utf-8-sig') as f: old=list(csv.DictReader(f))
cf=['compound','canonical_name','PubChem_CID','InChIKey','class','subclass','dietary_source','candidate_status','class_ranking_eligible','exposure_mg_day','exposure_umol_day','exposure_source','assay_primary','assay_secondary','current_review_status','notes']
classmap={'Polyphenol':'Flavonoids','Phenolic acid':'Phenolic acids / phenolic conjugates','Phenolic conjugate':'Phenolic acids / phenolic conjugates','Vitamin':'Vitamins / vitamin-like antioxidants','Carotenoid':'Carotenoids','Organosulfur':'Organosulfur compounds','Other food phenolic':'Other food-derived redox-active phytochemicals','Mineral micronutrient':'Antioxidant-related micronutrients / mineral cofactors'}
with open(DATA/'Antioxidant_Class_Candidate_Master.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=cf);w.writeheader()
 for r in old:
  cl=classmap[r['chemical_class']]; eligible='yes' if r['current_H_ORAC_rank'] else ('not yet adjudicated' if r['panel_status']!='micronutrient_context' else 'not applicable')
  w.writerow({'compound':r['compound'],'canonical_name':r['canonical_name'],'PubChem_CID':r['PubChem_CID'],'InChIKey':r['InChIKey'],'class':cl,'subclass':r['subclass'],'dietary_source':r['representative_foods'],'candidate_status':'cross-class pilot v1.0; not final','class_ranking_eligible':eligible,'exposure_mg_day':r['typical_intake_mg_day'],'exposure_umol_day':r['typical_intake_umol_day'],'exposure_source':r['exposure_reference'],'assay_primary':r['antioxidant_capacity_assay'],'assay_secondary':'class-specific; see ranking rules','current_review_status':'pilot reviewed; class-wide systematic review not completed','notes':r['exclusion_or_caveat']})

# Ranking master: copy only actual H-ORAC ranks; other classes explicitly not completed
rankf=['class','compound','primary_metric','primary_value','unit','eligible_record_count','evidence_confidence','provisional_rank','TopN_status','ranking_version','caveat']
with open(DATA/'Antioxidant_Class_Ranking_Master.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=rankf);w.writeheader()
 for r in old:
  cl=classmap[r['chemical_class']]
  if r['current_H_ORAC_rank']:
   w.writerow({'class':cl,'compound':r['compound'],'primary_metric':'literature-derived H-ORAC-FL median','primary_value':r['H_ORAC_median'],'unit':'mol TE/mol compound','eligible_record_count':r['H_ORAC_B1_count'],'evidence_confidence':r['H_ORAC_confidence'],'provisional_rank':r['current_H_ORAC_rank'],'TopN_status':'legacy phenolic provisional ranking; source layer only','ranking_version':'H-ORAC consolidation v0.1','caveat':'Not a cross-class rank; A=0; protocols non-identical.'})
  else:
   w.writerow({'class':cl,'compound':r['compound'],'primary_metric':'class-specific framework not yet executed','primary_value':'','unit':'','eligible_record_count':'','evidence_confidence':'Not reviewed','provisional_rank':'','TopN_status':'Not completed','ranking_version':'Atlas framework v1.0','caveat':'No rank assigned; pilot inclusion is not Top-N status.'})

# Mechanism master: preserve all columns and add gap semantics
with open(ROOT/'Antioxidant_Mechanism_Evidence_Master.csv',encoding='utf-8-sig') as f: mech=list(csv.DictReader(f)); mf=list(mech[0])
for c in ['reviewed_status','systematic_search_completed','evidence_gap_status']:
 if c not in mf: mf.append(c)
with open(DATA/'Antioxidant_Mechanism_Evidence_Master.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=mf);w.writeheader()
 for r in mech:
  r.update(reviewed_status='pilot evidence item reviewed',systematic_search_completed='no',evidence_gap_status='not yet systematically reviewed; blank cells must not be read as no evidence');w.writerow(r)

print('Built stage docs and 3 active data masters')
