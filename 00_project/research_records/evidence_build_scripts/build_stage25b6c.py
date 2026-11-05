"""Rebuild the Stage25B.6C audit; never edits canonical/frozen evidence."""
import csv
import hashlib
import itertools
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/h_orac_stage25b'
OUT = BASE / 'stage25b6c'
DOC = ROOT / 'docs/qc/stage25b6c'
SYNC = ROOT / 'docs/sync'
for p in (OUT, DOC, SYNC): p.mkdir(parents=True, exist_ok=True)

def rd(path):
    with (ROOT / path).open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))

def csvout(name, rows):
    assert rows, name
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), extrasaction='ignore')
        w.writeheader(); w.writerows(rows)

def md(name, body, directory=DOC):
    (directory / name).write_text(body.strip()+'\n', encoding='utf-8')

evidence = rd('data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv')
rank = rd('data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv')
frozen = rd('data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv')
sources6 = rd('data/h_orac_stage25b/stage25b6b/Stage25B6B_Source_Independence_Registry.csv')
errors6 = rd('data/h_orac_stage25b/stage25b6b/Stage25B6B_Error_Recovery_Master.csv')
history = rd('data/h_orac_stage25b/stage25b6a/Stage25B6A_Research_History_Indicators.csv')
manifest = rd('data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv')
eligible = [r for r in evidence if r['H_ORAC_tier'] in ('A','B1')]
assert len(evidence)==74 and len(eligible)==68 and len(rank)==28 and len(frozen)==20 and len(sources6)==16 and len(history)==157
assert all(hashlib.sha256((ROOT/r['asset_path']).read_bytes()).hexdigest()==r['sha256'] for r in manifest)
byc=defaultdict(list)
for r in eligible: byc[r['candidate_id']].append(r)
source_by_doi={s['DOI']:s for s in sources6}
rank_by_name={r['canonical_name'].lower():r for r in rank}
cid_by_name={r['canonical_name'].lower():r['candidate_id'] for r in rank}

# A verified source must expose its own pure-standard measurement in original Methods/results.
# Other sources remain unresolved, irrespective of DOI count or canonical grade.
verified={
 '10.1007/s00217-022-04135-3':('https://link.springer.com/article/10.1007/s00217-022-04135-3','Methods; Table 6; n=4','Rothe/Germany','Pure standards assayed individually with AAPH/fluorescein/Trolox; beer-spiking experiment is separate.'),
 '10.1093/chromsci/bmad007':('https://academic.oup.com/chromsci/article/61/6/530/7030839','Experimental; Table I','HPLC-ORAC method-development group','Own pure ferulic/luteolin microplate ORAC measurements; on-line mixture values not substituted.'),
 '10.3389/fphys.2022.1047916':('https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2022.1047916/full','Methods 2.3; Table 1; Figure 3','Graton/Brazil','Own pure protocatechuic acid AAPH/fluorescein/Trolox measurement; triplicate is technical/design n, not three studies.'),
 '10.3390/antiox11091784':('https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/','Methods 2.2.2; Table 2','Skroza/Croatia','Own pure-acid ORAC measurements; two concentrations are one study.'),
 '10.3390/antiox12020505':('https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/','Methods; Table 3','Carvalho/Portugal','Own pure-compound TE_AUC measurements; ± type unresolved.'),
 '10.3390/foods10081807':('https://pmc.ncbi.nlm.nih.gov/articles/PMC8392586/','Methods; results tables','Foods 2021 group','Own pure-compound ORAC measurements; within-paper replicates one study.'),
 '10.3390/ijms20092328':('https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/','Methods 3.1–3.3; Table 3','Žuvela/Singapore','Table 3 experimental ln(ORAC) separated from PLS/ANN predictions.'),
}
partial={
 '10.1007/s12039-019-1618-5':'Publisher abstract located; compound-level original ORAC table/Methods not accessible.',
 '10.1016/j.foodchem.2008.08.013':'Original abstract/institutional record located; full results table requires copy.',
 '10.1016/j.foodchem.2010.11.092':'Institutional PDF lead located; matching canonical pure ellagic-acid table not yet independently checked.',
 '10.1021/jf010586o':'ACS publisher abstract accessible, original Table 4 blocked; historical values not reverified.',
 '10.1021/jf0305231':'ACS publisher abstract accessible; original result table blocked.',
 '10.1021/jp307746c':'ACS abstract accessible; original measured versus calculated table unresolved.',
 '10.1039/d1ra08918h':'RSC original landing/PDF located; compound-level matching table not independently extracted.',
 '10.1271/bbb.110717':'Publisher PDF located; compound-level matching table not independently extracted.',
 '10.3390/ijms150916351':'Original article located; specific canonical table and newly measured versus cited values not yet reconciled.',
}
assert len(verified)+len(partial)==16
source_rows=[]
for s in sources6:
    doi=s['DOI']; v=verified.get(doi); url=v[0] if v else 'https://doi.org/'+doi
    source_rows.append(dict(source_id=s['source_id'],DOI=doi,publication_year=s['publication_year'],first_author=s['first_author'],candidate_ids=s['candidate_ids'],experiment_ids=s['experiment_ids'],fulltext_status='ORIGINAL_FULLTEXT_VERIFIED' if v else ('SOURCE_ACCESS_BLOCKED' if doi.startswith('10.1021/') or doi.startswith('10.1016/') or doi.startswith('10.1007/s12039') else 'ORIGINAL_AVAILABLE_TABLE_NOT_CLOSED'),original_measurement_status='VERIFIED_ORIGINAL_EXPERIMENT' if v else 'UNRESOLVED',study_group=v[2] if v else 'NOT_VERIFIED',material='PURE_STANDARD' if v else 'CANONICAL_PURE_STANDARD_NOT_RECHECKED',assay='AAPH_FLUORESCEIN_TROLOX' if v else 'SOURCE_SPECIFIC_PROTOCOL_NOT_CLOSED',source_location=v[1] if v else s['original_table_or_figure'],source_url=url,reused_data_evidence='NO_REUSE_IDENTIFIED_IN_CHECKED_METHODS' if v else 'NOT_ASSESSED',verification_note=v[3] if v else partial[doi]))
csvout('Stage25B6C_Source_Fulltext_Verification.csv',source_rows)

pair=[]; closure=[]
for rr in rank:
    cid=rr['candidate_id']; ds=sorted({r['DOI'].lower() for r in byc[cid]}); vd=[d for d in ds if d in verified]
    for d1,d2 in itertools.combinations(ds,2):
        both=d1 in verified and d2 in verified
        status='CONFIRMED_INDEPENDENT' if both else ('SOURCE_INACCESSIBLE' if any(source_by_doi[d]['source_access']=='SOURCE_NOT_ACCESSIBLE' or d.startswith('10.1021/') for d in (d1,d2)) else 'UNRESOLVED')
        s1=source_by_doi[d1]; s2=source_by_doi[d2]
        pair.append(dict(candidate_id=cid,candidate_name=rr['canonical_name'],source_id_1=s1['source_id'],source_id_2=s2['source_id'],DOI_1=d1,DOI_2=d2,study_group_1=verified[d1][2] if d1 in verified else 'NOT_VERIFIED',study_group_2=verified[d2][2] if d2 in verified else 'NOT_VERIFIED',experimental_material_1='PURE_STANDARD' if d1 in verified else 'UNRESOLVED',experimental_material_2='PURE_STANDARD' if d2 in verified else 'UNRESOLVED',experiment_date_or_context='Distinct publication methods/results' if both else 'NOT_COMPARABLE_YET',original_measurement_evidence='BOTH_ORIGINAL_RESULTS_VERIFIED' if both else 'ONE_OR_BOTH_NOT_VERIFIED',reused_data_evidence='No shared dataset identified in original methods/results; distinct experimental groups' if both else 'NOT_ASSESSED',independence_decision=status,decision_basis='Separate groups and newly generated pure-standard assay results; not technical repeats' if both else 'DOI difference alone insufficient',source_location=(verified[d1][0]+' ; '+verified[d2][0]) if both else 'https://doi.org/'+d1+' ; https://doi.org/'+d2,access_status='BOTH_VERIFIED' if both else 'PARTIAL',remaining_uncertainty='' if both else 'Original result table and reuse comparison pending'))
    n=len(vd); status='PASS_VERIFIED' if n>=2 else ('FAIL_ON_AVAILABLE_EVIDENCE' if len(ds)==1 else 'UNRESOLVED')
    closure.append(dict(candidate_id=cid,candidate_name=rr['canonical_name'],canonical_rank=rr['rank'],confirmed_independent_study_N=n,confirmed_source_DOIs=';'.join(vd),possible_independent_study_N=len(ds)-n,quantitative_record_N=len(byc[cid]),distinct_DOI_N=len(ds),unresolved_source_N=len(ds)-n,proposed_threshold_status=status,decision_basis='At least two individually verified original pure-standard datasets from separate groups' if n>=2 else ('Only one canonical DOI' if len(ds)==1 else 'Original source-level verification incomplete'),canonical_change='NONE'))
csvout('Stage25B6C_Pairwise_Study_Independence.csv',pair)
csvout('Stage25B6C_Candidate_Independence_Closure.csv',closure)
byclosure={r['candidate_id']:r for r in closure}

target_map={
 'Rosmarinic acid':[('10.3390/molecules28207199','PLANT_MATERIAL_ORAC','PROPOSED_X','Perilla material ORAC correlates with rosmarinic content; not pure rosmarinic-acid H-ORAC','https://www.mdpi.com/1420-3049/28/20/7199')],
 'Daidzein':[('10.1021/jf053112o','ORIGINAL_ABSTRACT_ONLY','NOT_ASSESSABLE','Isoflavone assays reported; original pure-compound ORAC-FL result and unit not verified','https://pubs.acs.org/doi/10.1021/jf053112o')],
 'Fisetin':[('10.1038/s41598-025-32257-7','PLANT_EXTRACT_ORAC','PROPOSED_X','Pithecellobium extract/isolate paper; no verified pure fisetin H-ORAC endpoint','https://www.nature.com/articles/s41598-025-32257-7')],
 'Hesperidin':[('10.1111/j.1750-3841.2010.01717.x','MIXTURE_INTERACTION','NOT_ASSESSABLE','Orange phenolic interactions; pure hesperidin endpoint/table not verified','https://ift.onlinelibrary.wiley.com/doi/abs/10.1111/j.1750-3841.2010.01717.x')],
 'Naringin':[('10.1016/j.foodchem.2021.130605','FOOD_MATRIX','NOT_ASSESSABLE','Citrus pulp flavonoids; pure naringin H-ORAC-FL endpoint not verified','https://doi.org/10.1016/j.foodchem.2021.130605')],
 'Morin':[('10.3389/fnut.2022.882458','QSPR_MODEL','PROPOSED_X','QSPR model is not a second direct H-ORAC measurement','https://www.frontiersin.org/articles/10.3389/fnut.2022.882458/full')],
 'Myricetin':[('10.1111/j.1750-3841.2010.01717.x','MIXTURE_INTERACTION','NOT_ASSESSABLE','Orange phenolic interactions; pure myricetin endpoint/table not verified','https://ift.onlinelibrary.wiley.com/doi/abs/10.1111/j.1750-3841.2010.01717.x')],
}
target_names=['Rosmarinic acid','Daidzein','Fisetin','Hesperidin','Naringin','Ferulic acid','Morin','Myricetin','Epigallocatechin','Gallic acid','Vitamin C']
target=[]
for name in target_names:
    cid='AFF-0104' if name=='Vitamin C' else cid_by_name[name.lower()]
    leads=target_map.get(name)
    if name=='Vitamin C': leads=[('10.1021/jf010586o','SOURCE_ACCESS_BLOCKED','NOT_ASSESSABLE','Original Table 4 blocked; 0.95 historical value not reverified','https://pubs.acs.org/doi/10.1021/jf010586o'),('10.3390/antiox12020505','ORIGINAL_FULLTEXT_VERIFIED','PROPOSED_B1','Table 3 original L-ascorbic acid 0.53±0.03 TE_AUC; ± type unresolved; source-level rubric review remains pending','https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/')]
    if not leads: leads=[('', 'EXISTING_CANONICAL_ONLY','NOT_ASSESSABLE','No additional qualified pure-compound source verified in targeted 6C search','')]
    for doi,kind,grade,note,url in leads:
        target.append(dict(candidate_id=cid,candidate_name=name,DOI=doi,source_type=kind,original_article_exists='YES' if doi else 'NO_NEW_SOURCE',original_fulltext_checked='YES' if kind in ('PLANT_MATERIAL_ORAC','PLANT_EXTRACT_ORAC','ORIGINAL_FULLTEXT_VERIFIED') else 'NO_OR_PARTIAL',pure_compound_H_ORAC_FL_value_verified='YES' if name=='Vitamin C' and doi.endswith('12020505') else 'NO',AAPH_fluorescein_Trolox='YES' if name=='Vitamin C' and doi.endswith('12020505') else 'NOT_VERIFIED_OR_NOT_APPLICABLE',original_value='0.53 ± 0.03' if name=='Vitamin C' and doi.endswith('12020505') else '',original_unit='TE_AUC mol/mol' if name=='Vitamin C' and doi.endswith('12020505') else '',conversion_status='NO_NEW_CONVERSION',provisional_grade=grade,independence='NOT_ESTABLISHED_FOR_NEW_THRESHOLD',decision=note,source_url=url))
csvout('Stage25B6C_Targeted_Source_Screening.csv',target)
csvout('Stage25B6C_Provisional_Rubric_Adjudication.csv',[dict(candidate_id=r['candidate_id'],candidate_name=r['candidate_name'],DOI=r['DOI'],provisional_rubric_grade=r['provisional_grade'],pure_compound_endpoint_verified=r['pure_compound_H_ORAC_FL_value_verified'],primary_eligible_now='NO_NEW_CANONICAL_ADMISSION',rubric_version='v2.0_UNCHANGED',decision_basis=r['decision'],human_review='PENDING_HUMAN_REVIEW') for r in target])
csvout('Stage25B6C_New_Evidence_Proposals.csv',[dict(candidate_id=r['candidate_id'],candidate_name=r['candidate_name'],DOI=r['DOI'],new_quantitative_evidence_verified='YES_PROVISIONAL' if r['candidate_name']=='Vitamin C' and r['DOI'].endswith('12020505') else 'NO',proposed_grade=r['provisional_grade'],proposed_action='FORMAL_SOURCE_ADJUDICATION' if r['candidate_name']=='Vitamin C' else 'NO_PRIMARY_INCLUSION',canonical_record_added='NO',review_status='PENDING_HUMAN_REVIEW',source_url=r['source_url']) for r in target])

err=[]; reps=[]
for r in errors6:
    doi=r['DOI'].lower(); typed=bool(r['reported_SD'] or r['reported_SE'] or r['reported_CI'])
    scale='ln(ORAC)' if doi=='10.3390/ijms20092328' else ('µM TE at source concentrations' if doi=='10.3390/antiox11091784' else 'SOURCE_SCALE_NOT_FULLY_VERIFIED')
    etype='SD_VERIFIED_IN_PRIOR_CANONICAL_AUDIT' if typed else ('ERROR_TYPE_UNRESOLVED' if r['original_plus_minus_unclassified'] else 'NO_NUMERIC_ERROR_REPORTED_OR_RECOVERED')
    err.append(dict(candidate_id=r['candidate_id'],candidate_name=r['candidate_name'],experiment_id=r['experiment_id'],DOI=doi,error_type_verified=etype,error_value=r['reported_SD'] if typed else r['original_plus_minus_unclassified'],error_scale=scale,replicate_N=r['replicate_N'],replicate_type='TECHNICAL_OR_RUN_TYPE_UNRESOLVED' if r['replicate_N']=='3' else r['replicate_type'],original_source_location=r['error_source_location'],conversion_validity='DO_NOT_COPY_LOG_ERROR_TO_MOL_SCALE' if scale=='ln(ORAC)' else ('ORIGINAL_SCALE_ONLY' if not typed else 'CANONICAL_SD_RETAINED'),confidence_in_extraction='HIGH_FOR_NUMBER_LOW_FOR_TYPE' if r['original_plus_minus_unclassified'] else ('PRIOR_VERIFIED' if typed else 'MISSING'),CI_status='CI_NOT_ESTIMABLE'))
    reps.append(dict(experiment_id=r['experiment_id'],candidate_id=r['candidate_id'],DOI=doi,reported_replicate_N=r['replicate_N'],replicate_type='NOT_CONFIRMED_AS_INDEPENDENT_BIOLOGICAL_OR_LAB_RUNS',independent_study_contribution='ONE_SOURCE_MAXIMUM',source_location=r['error_source_location'],review_status='NO_TECHNICAL_REPEAT_COUNTED_AS_NEW_STUDY'))
csvout('Stage25B6C_Error_Definition_Closure.csv',err)
csvout('Stage25B6C_Replicate_Design_Audit.csv',reps)

maturity=[]
for h in history:
    cid=h['candidate_id']; cc=byclosure.get(cid,{})
    qc=h['history_QC'] or 'NO_SOURCE_LEVEL_REPAIR'
    years=(h['earliest_original_publication_year'],h['latest_original_publication_year'])
    missing=not all(y.isdigit() and 1900<=int(y)<=2026 for y in years)
    maturity.append(dict(candidate_id=cid,candidate_name=h['canonical_name'],earliest_original_publication_year=years[0],latest_original_publication_year=years[1],research_span_years=h['research_span_years'],deduplicated_original_publication_N=h['metadata_deduplicated_publication_N'],recent_5_year_publication_N=h['recent_5_year_publication_N_2022_2026'],recent_10_year_publication_N=h['recent_10_year_publication_N_2017_2026'],H_ORAC_original_study_N=cc.get('confirmed_independent_study_N','0'),H_ORAC_distinct_DOI_proxy_N=cc.get('distinct_DOI_N','0'),source_level_year_repair='NONE_NO_ORIGINAL_BIBLIOGRAPHIC_RECONCILIATION',metadata_QC_status=qc,year_parse_status='MISSING_OR_INVALID' if missing else 'PARSEABLE_NOT_ORIGINAL_VALIDATED',research_scope='GENERAL_ANTIOXIDANT_HISTORY_NOT_H_ORAC_POTENCY',source=h['history_source']))
csvout('Stage25B6C_Research_Maturity_QC.csv',maturity)

sc1=[r['candidate_id'] for r in rank if len(byc[r['candidate_id']])>=2]
sc2=[r['candidate_id'] for r in rank if byclosure[r['candidate_id']]['proposed_threshold_status']=='PASS_VERIFIED']
scenario=[]
for rr in rank:
    cid=rr['candidate_id']; cc=byclosure[cid]; vals=sorted(float(x['converted_value_mol_TE_per_mol']) for x in byc[cid]); q=statistics.quantiles(vals,n=4,method='inclusive') if len(vals)>1 else None
    scenario.append(dict(candidate_id=cid,candidate_name=rr['canonical_name'],frozen_rank=rr['rank'],canonical_median_mol_TE_per_mol=rr['median_H_ORAC_mol_TE_per_mol'],scenario_0_frozen_top20='YES' if int(rr['rank'])<=20 else 'NO',scenario_1_record_gate='PASS' if cid in sc1 else 'FAIL',scenario_1_rank=sc1.index(cid)+1 if cid in sc1 else '',scenario_2_verified_study_gate=cc['proposed_threshold_status'],scenario_2_rank=sc2.index(cid)+1 if cid in sc2 else '',scenario_3_error_type_count=sum(x['candidate_id']==cid and x['error_type_verified']=='SD_VERIFIED_IN_PRIOR_CANONICAL_AUDIT' for x in err),scenario_3_between_record_IQR=q[2]-q[0] if q else '',scenario_3_CI='CI_NOT_ESTIMABLE',scenario_3_rank_uncertainty='RANK_UNCERTAINTY_NOT_ESTIMABLE',prospective_scenario='PENDING_HUMAN_ADJUDICATION' if rr['canonical_name'] in target_names else 'NO_NEW_PROPOSAL',formal_v11_status='NOT_CREATED'))
csvout('Stage25B6C_Eligibility_and_Rank_Scenarios.csv',scenario)

cr=[]
def add(typ,cid,doi,proposal,basis,impact):
    cr.append(dict(change_request_id=f'6C-CR-{len(cr)+1:03d}',change_type=typ,candidate_id=cid,source_DOI=doi,current_state='FROZEN_V1_UNCHANGED',proposed_change=proposal,evidence_basis=basis,potential_impact=impact,review_status='PENDING_HUMAN_REVIEW',approval_required='YES'))
for t in target:
    if t['DOI']: add('TARGETED_SOURCE',t['candidate_id'],t['DOI'],'Approve source-specific v2.0 disposition; no automatic canonical entry',t['decision'],'POSSIBLE_ELIGIBILITY')
add('STUDY_INDEPENDENCE_GATE','ALL_28','','Formally decide N>=2 verified original-study gate for future v1.1','Researcher endorsed direction; current freeze not changed','HIGH')
add('SOURCE_RECONCILIATION','ALL_28','','Resolve inaccessible or table-unchecked canonical sources before final gate','9/16 sources not closed','HIGH')
add('VITAMIN_C_RECONCILIATION','AFF-0104','10.1021/jf010586o;10.3390/antiox12020505','Obtain Ou Table 4 and adjudicate both rows under v2.0','Carvalho verified; Ou original table blocked','POSSIBLE_NEW_CANDIDATE')
add('ERROR_DEFINITION','ALL_68','','Correct types only where original footnote/Methods confirms','26 numeric errors; 3 typed SD, 23 untyped','PRECISION_ONLY')
add('RESEARCH_HISTORY_METADATA','ALL_157','','Source-repair invalid/missing years separately from potency','7 flags and 13 year gaps inherited; not guessed','MATURITY_ONLY')
csvout('Stage25B6C_Proposed_Change_Requests.csv',cr)

passes=len(sc2); unresolved=sum(x['proposed_threshold_status']=='UNRESOLVED' for x in closure)
typed=sum(x['error_type_verified']=='SD_VERIFIED_IN_PRIOR_CANONICAL_AUDIT' for x in err)
numeric=sum(bool(x['error_value']) for x in err)
flagged=sum(x['metadata_QC_status']=='SOURCE_LATEST_YEAR_FUTURE_OR_INVALID' for x in maturity)
missing=sum(x['year_parse_status']=='MISSING_OR_INVALID' for x in maturity)
assert typed==3 and numeric==26 and flagged==7 and missing==13
md('Stage25B6C_VitaminC_Source_Closure_CN.md',f'''# Vitamin C 来源闭环

L-Ascorbic acid（AFF-0104）历史值为 Ou 2001 0.95、Carvalho 2023 0.53 mol TE/mol，历史中位数 0.74；这些不是本轮新计算或 canonical 纳入。Ou [出版商原文入口](https://pubs.acs.org/doi/10.1021/jf010586o)仅能查到书目/摘要，Table 4 未合法取得，状态 `SOURCE_ACCESS_BLOCKED`，故 0.95 仍为历史转录而非原表复核。Carvalho [原文 Methods/Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)报告 L-ascorbic acid 0.53 ± 0.03 TE_AUC，使用 AAPH、fluorescein、Trolox；± 的统计定义未从原文明确恢复，不能当 SD。两文作者、年代与实验场景不同，支持不同研究组的初步判断，但 Ou 数据未复核，AFF-0104 的双研究资格仍为 `UNRESOLVED`。Stage25B 未迁移原因是迁移/来源逐项裁决尚未完成；不能推断为科学排除。建议正式 CR 后取得 Ou Table 4 并逐项套用原 rubric v2.0；目前不迁移、不改排名。H-ORAC 是特定体外化学测定，不能解释为人体抗氧化或临床效力。''')
md('Stage25B6C_Revision_Readiness_Report_CN.md',f'''# Stage25B.6C 修订准备度

本轮在 16 个既有 DOI 中核实 {len(verified)} 个来源的原始纯品实验及结果定位；其余 {len(partial)} 个保留来源或表格缺口。68 条 A/B1、28 种可排名候选、原中位数与 v1.0 Top20 不变。拟议双独立研究门槛 `PASS_VERIFIED` 为 {passes}/28（6B 为 3/28），`UNRESOLVED` 为 {unresolved}/28；单来源者为现有证据不足，不等于文献不存在。逐对核查表说明来源组、材料和原文定位；不同 DOI 未直接计数。通过者可追溯到 closure 表中的具体 DOI。

Scenario 0 是冻结 v1.0；Scenario 1 仅要求两条 A/B1 定量记录，{len(sc1)} 种达标；Scenario 2 要求两项核实的独立原始研究，{passes} 种达标，距 20 种还差 {max(0,20-passes)} 种；Scenario 3 在 Scenario 2 上附加测量误差和记录间离散画像，不改变资格。Prospective 仅列待裁决来源，不生成正式名次。{numeric}/68 有任意数值误差，其中 {typed}/68 的 SD 类型明确；95%CI、排名概率均不可估，IQR 不等于 CI。研究成熟度独立展示，不进入 H-ORAC 中位数。

定点线索没有核实出可直接加入现有 28 种排名的第二项合格纯品 H-ORAC-FL 新研究。Vitamin C 的 Carvalho 原表可定位，Ou Table 4 仍阻断；所有新增/更正均为 `PENDING_HUMAN_REVIEW`。导师可汇报方法学与进展，不宜宣称修订 Top20 已稳定。正式 v1.1 需要研究者先裁决 CR、补齐关键原表和达到门槛的候选数量；不为凑数降低标准。''')
md('Stage25B6C_Supervisor_Update_CN.md',f'''# 给导师的 Stage25B.6C 进展

一、老师上次提出的问题：研究历史、实验误差、维生素 C，以及单点证据能否支撑高置信度排名。

二、已完成：对 16 个既有 DOI 建立原文核查表，对跨来源进行逐对独立性裁决；定点排查五个单记录候选和五个边界候选；复核 68 条误差记录与 157 种候选的研究历史元数据。

三、能够确认：{passes} 种候选达到拟议的至少两项独立原始研究要求，仍不足 20 种。效力中位数、研究独立性、测量精度与研究间差异分开报告。研究历史只反映证据成熟度，不参与 H-ORAC 效力排序。缺失误差不记为零。

四、未解决：{len(partial)} 篇既有来源的原始表格或数据归属未关闭；Ou 2001 Table 4 未取得；多数 ± 的统计定义不明。单点来源和待裁决新线索不能自动进入正式名单。

五、下一步原则：维持 rubric v2.0、A+B1 primary 与原中位数；只按原文核实结果提交变更请求，不以技术重复充作独立研究，不为凑足 20 种放宽标准。H-ORAC 是体外化学测定，不等同人体抗氧化效果。

六、预计交付：来源与逐对独立性表、资格情景、误差及研究历史 QC、正式变更请求，经人工审批后再考虑 v1.1。

【可以现在向导师汇报的内容】上述审计覆盖和方法学原则、已核实的 {passes} 种及具体证据缺口。

【暂时不能向导师宣称的内容】Top20 已更新、研究间差异显著、存在可靠 95%CI 或人体效力排序。

【建议等待补证后再汇报的内容】维生素 C 双来源正式资格及任何 v1.1 成员名单。''')
md('Stage25B6C_Supervisor_WeChat_Draft_CN.md',f'''老师您好，我们按您提出的研究历史、实验误差、维生素 C 和单点证据问题，重新核查了现有 H-ORAC 来源及跨论文独立性。目前有 {passes} 种候选具备至少两项已核实的独立原始研究，尚不足以形成新的 20 种正式名单。研究历史将单独作为证据成熟度展示，不参与效力排序；测量误差与研究间差异也分别评价，缺失误差不会按零处理。维生素 C 的一篇原始表格仍需获取。我们已整理来源审计、资格情景和待审批变更请求，补证与您确认后再讨论是否修订 Top20。''')
md('Stage25B6C_QC_Report_CN.md',f'''# Stage25B.6C QC

冻结 manifest SHA256 {len(manifest)}/{len(manifest)} 匹配；Rubric v2.0、Frozen Top20 v1.0、74 条 canonical、157 候选均未由本脚本修改。A/B1 为 68 条，B2/X 未入 primary，1,641 pending 未批量处理。16 DOI 中 {len(verified)} 篇完成原始纯品结果定位，{len(partial)} 篇保留缺口；逐对裁决不以 DOI 数或技术重复自动判独立，Žuvela 预测值不计实测。26 条数值误差中仅 3 条类型明确；未设零、未生成 CI/p 值。VC 未迁移，研究历史未纳入加权分数。所有 {len(cr)} 项 CR 为待人工审批；未生成或冻结 Top20 v1.1。限制：未取得的原始表格不能由摘要或二手数值补足。''')
md('CHATGPT_SYNC_STAGE25B6C.md',f'''# Stage25B.6C 同步

Commit SHA：提交后以本仓库 `git rev-parse HEAD` 为准；此文件在提交前生成，避免自引用哈希。

28 种候选：双独立原始研究 `PASS_VERIFIED` {passes}（6B 为 3），`UNRESOLVED` {unresolved}；其余为现有单来源不足。16 DOI：{len(verified)} 原始纯品实验结果已定位，{len(partial)} 原始表格/数据归属未关闭。逐候选 DOI 及逐对裁决见 6C CSV；未把 DOI 数、技术重复或模型预测当研究数。

五种单记录 Top20：Rosmarinic、Daidzein、Fisetin、Hesperidin、Naringin 均无第二项已核实合格纯品 H-ORAC-FL 实验；紫苏与植物提取物线索不适用。边界 Ferulic/Morin/Myricetin/Epigallocatechin/Gallic 按既有 A+B1 来源重新核查，Morin QSPR 不能当实测。VC：Carvalho Table 3 已核实 0.53±0.03，Ou Table 4 `SOURCE_ACCESS_BLOCKED`，历史 0.95/0.74 不迁入 canonical。

误差：26/68 有数值，3/68 明确 SD；Žuvela 的 ln(ORAC) ± 不可直接搬到 mol TE/mol。研究历史：7 个未来/无效年份标志、13 个起止年份缺口保留，未猜测修复，独立于效力。Scenario 1 两记录 {len(sc1)} 种；Scenario 2 双核实研究 {passes} 种，距 20 种差 {max(0,20-passes)}；Scenario 3 仅加误差/异质性画像；prospective 待批准。CI 和排名概率不可估。

未解决：{len(partial)} 篇既有来源原表、Ou Table 4、定点来源纯品终点、± 类型与研究历史元数据。{len(cr)} 项 CR 均待人工审批。导师汇报可进行方法学/进度说明，不能宣称 v1.1 已形成。下一阶段建议先取得关键原表并逐项批准 CR；本轮不启动 6D、不冻结 v1.1。
''', SYNC)
print(f'6C generated: verified={len(verified)}, pass={passes}, unresolved={unresolved}, typed={typed}, numeric={numeric}, flags={flagged}, missing={missing}, CR={len(cr)}')
