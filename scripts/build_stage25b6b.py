"""Build a conservative, reproducible Stage25B.6B diagnostic package.

No canonical evidence, rubric, or frozen assets are modified by this script.
"""
import csv
import hashlib
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/h_orac_stage25b'
OUT = DATA / 'stage25b6b'
DOC = ROOT / 'docs/qc/stage25b6b'
SYNC = ROOT / 'docs/sync'
for p in (OUT, DOC, SYNC): p.mkdir(parents=True, exist_ok=True)

def read(path):
    with (ROOT / path).open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))

def write(name, fields, rows):
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def md(name, body): (DOC / name).write_text(body.strip()+'\n', encoding='utf-8')

evidence = read('data/h_orac_stage25b/Stage25B_HORAC_Experiment_Evidence.csv')
rank = read('data/h_orac_stage25b/Stage25B_HORAC_Quantitative_Ranking.csv')
frozen = read('data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv')
err6 = read('data/h_orac_stage25b/stage25b6a/Stage25B6A_HORAC_Error_Data_Audit.csv')
history = read('data/h_orac_stage25b/stage25b6a/Stage25B6A_Research_History_Indicators.csv')
screen = read('data/h_orac_stage25b/Stage25B_HORAC_Publication_Screening.csv')
manifest = read('data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv')
eligible = [r for r in evidence if r['H_ORAC_tier'] in ('A','B1')]
assert len(evidence)==74 and len(eligible)==68 and len(rank)==28 and len(frozen)==20
assert {t:sum(r['H_ORAC_tier']==t for r in evidence) for t in ('A','B1','B2','X')}=={'A':7,'B1':61,'B2':4,'X':2}
by_c=defaultdict(list); by_d=defaultdict(list)
for r in eligible: by_c[r['candidate_id']].append(r); by_d[r['DOI'].lower()].append(r)
assert len(by_c)==28 and len(by_d)==16
e6={r['experiment_id']:r for r in err6}
scr_d={}
for r in screen:
    d=r['DOI'].lower()
    if d and d not in scr_d: scr_d[d]=r

# Source access is deliberately not inferred from prior migration labels.
access={
 '10.3390/antiox12020505':('ORIGINAL_HTML_VERIFIED','https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/','Methods; Table 3','Original experiment; Table 3 and methods checked; ± type unresolved.'),
 '10.3390/antiox11091784':('ORIGINAL_HTML_VERIFIED','https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/','Methods 2.1; Table 2','Original individual pure-acid ORAC experiments. Distinct Split laboratory, materials and protocol from Carvalho 2023.'),
 '10.3390/ijms20092328':('ORIGINAL_HTML_VERIFIED','https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/','Methods 3.1–3.3; Table 3','Original triplicate AAPH/fluorescein/Trolox flavonoid assay at National University of Singapore; model predictions not counted as measurements.'),
 '10.1021/jf010586o':('SOURCE_NOT_ACCESSIBLE','https://pubs.acs.org/doi/10.1021/jf010586o','Table 4 cited in canonical ledger, original table not freshly inspected','Publisher abstract/paywall; no independent re-verification of Table 4.'),
 '10.3390/foods10081807':('ORIGINAL_HTML_VERIFIED','https://pmc.ncbi.nlm.nih.gov/articles/PMC8392586/','Methods; results/tables','Original article available; no pairwise dataset comparison established.'),
}
sources=[]
for i,(doi,rs) in enumerate(sorted(by_d.items()),1):
    s=scr_d.get(doi,{})
    a,u,loc,note=access.get(doi,('NOT_RECHECKED_FULL_TEXT','https://doi.org/'+doi,'Canonical source_page/source_table only','Bibliographic/canonical provenance is not a fresh full-text independence check.'))
    sources.append(dict(source_id=f'6B-SRC-{i:02d}',DOI=doi,publication_year=s.get('year') or rs[0].get('year',''),original_article_title=s.get('title',''),journal=s.get('journal',''),first_author=(s.get('authors','').split(',')[0]),candidate_ids=';'.join(sorted({r['candidate_id'] for r in rs})),experiment_ids=';'.join(r['independent_experiment_id'] for r in rs),original_table_or_figure=';'.join(sorted({r['source_table'] for r in rs if r['source_table']})),assay_protocol='AAPH/fluorescein/Trolox per canonical; source-specific recheck pending',study_population_or_material='pure compound per canonical; source-specific recheck pending',laboratory_or_group='NOT_VERIFIED',sample_batch='NOT_REPORTED_OR_NOT_VERIFIED',data_collection_context='NOT_VERIFIED',possible_reused_dataset='NOT_ASSESSED',possible_republished_measurement='NOT_ASSESSED',source_access=a,evidence_location=u+' ; '+loc,verification_note=note))
source_by_d={r['DOI']:r for r in sources}
verified_original={'10.3390/antiox12020505','10.3390/antiox11091784','10.3390/ijms20092328','10.3390/foods10081807'}
write('Stage25B6B_Source_Independence_Registry.csv',list(sources[0]),sources)

studies=[]
for r in eligible:
    src=source_by_d[r['DOI'].lower()]
    verified=r['DOI'].lower() in verified_original
    studies.append(dict(study_id=src['source_id'] if verified else '',source_id=src['source_id'],experiment_id=r['independent_experiment_id'],candidate_id=r['candidate_id'],DOI=r['DOI'],independence_evidence=('Original Methods and results report newly performed pure-compound assay; Singapore 2019, Split 2022 and Porto 2023 studies have distinct groups, materials and protocols' if verified else 'Same DOI rows grouped to one publication contribution; no source-pair dataset comparison completed'),independence_status='CONFIRMED_INDEPENDENT' if verified else 'INDEPENDENCE_UNRESOLVED',independence_reason='One original publication contribution; distinct experimental source from other verified original articles' if verified else 'Distinct DOI and experiment ID alone do not establish independent research execution',evidence_location=src['evidence_location']+' ; '+str(r['source_page']),source_access=src['source_access'],reviewer_note='Canonical A/B1 eligibility retained; study independence is a separate unapproved gate.'))
write('Stage25B6B_Study_Independence_Adjudication.csv',list(studies[0]),studies)

summary=[]
for rr in rank:
    cid=rr['candidate_id']; rs=by_c[cid]; doi_n=len({r['DOI'].lower() for r in rs})
    confirmed=len({r['DOI'].lower() for r in rs if r['DOI'].lower() in verified_original})
    unresolved=len(rs)-confirmed
    status='PASS_VERIFIED' if confirmed>=2 else ('FAIL_ON_AVAILABLE_EVIDENCE' if doi_n==1 else 'UNRESOLVED')
    summary.append(dict(candidate_id=cid,candidate_name=rr['canonical_name'],canonical_rank=rr['rank'],confirmed_independent_study_N=confirmed,possible_independent_study_N=doi_n-confirmed,distinct_original_publication_N=confirmed,distinct_DOI_publication_proxy_N=doi_n,quantitative_record_N=len(rs),independence_unresolved_N=unresolved,duplicate_or_nonindependent_N=0,proposed_minimum_study_threshold_status=status,interpretation='At least two distinct original experimental studies verified; other DOI unresolved' if confirmed>=2 else ('One available canonical source; absence of other studies not proved' if doi_n==1 else 'Multiple DOI proxies; source-pair independence unresolved')))
write('Stage25B6B_Candidate_Study_Count_Summary.csv',list(summary[0]),summary)
sum_c={r['candidate_id']:r for r in summary}

errors=[]
skroza_error={'Protocatechuic Acid':'0.9;2','Gallic Acid':'1;1','P-Coumaric Acid':'2;1','Caffeic Acid':'2;1','Ferulic Acid':'2;0','Sinapic acid':'1;1','Rosmarinic Acid':'2;2'}
zuvela_log_error={'Genistein':'0.008','Naringenin':'0.014','Epicatechin':'0.004','Kaempferol':'0.018','Apigenin':'0.000','Quercetin':'0.003','Fisetin':'0.022','Hesperetin':'0.014','Luteolin':'0.013','Morin':'0.006','Epigallocatechin':'0.020','Myricetin':'0.000','Catechin':'0.018'}
for r in eligible:
    old=e6[r['independent_experiment_id']]
    sk=r['DOI'].lower()=='10.3390/antiox11091784'
    zu=r['DOI'].lower()=='10.3390/ijms20092328'
    pm=skroza_error.get(r['canonical_name'],'') if sk else (zuvela_log_error.get(r['canonical_name'],'') if zu else old['original_plus_minus_unclassified'])
    errors.append(dict(candidate_id=r['candidate_id'],candidate_name=r['canonical_name'],experiment_id=r['independent_experiment_id'],DOI=r['DOI'],reported_mean=r['converted_value_mol_TE_per_mol'],reported_SD=old['SD'],reported_SE=old['SE'],reported_CI=old['CI_lower']+';'+old['CI_upper'] if old['CI_lower'] or old['CI_upper'] else '',CI_level=old['CI_level'],original_plus_minus_unclassified=pm,original_error_scale='ln(ORAC)' if zu else ('µM TE at 2.5;5 µM' if sk else 'same as source table; verify'),replicate_N='3' if sk or zu else old['replicate_N_as_reported'],replicate_type='REPLICATE_TYPE_UNCLEAR',independent_run_N='NOT_VERIFIED',sample_concentration='2.5;5 µM' if sk else r['sample_concentration'],measurement_conditions='2.5 and 5 µM original assay concentrations; not independent studies' if sk else ('AAPH/fluorescein/Trolox, pH 7.4, 37°C; original ln(ORAC) error not on mol TE/mol scale' if zu else 'Source-specific method recheck pending'),error_definition='UNSPECIFIED_PLUS_MINUS' if sk or zu else old['error_type'],error_source_location='Original Table 2 ORAC 2.5/5 µM columns; Methods 2.2.2' if sk else ('Original Table 3 ln(ORAC) column; Methods 3.3' if zu else old['error_source_location']),source_access=source_by_d[r['DOI'].lower()]['source_access'],recovery_status='ORIGINAL_TABLE_VERIFIED_TYPE_UNCLEAR' if pm else ('CANONICAL_SD_RETAINED' if old['SD'] else 'NO_NEW_ERROR_RECOVERED'),CI_status='CI_NOT_ESTIMABLE'))
write('Stage25B6B_Error_Recovery_Master.csv',list(errors[0]),errors)
typed=sum(bool(r['reported_SD'] or r['reported_SE'] or r['reported_CI']) for r in errors)
any_error=sum(bool(r['reported_SD'] or r['reported_SE'] or r['reported_CI'] or r['original_plus_minus_unclassified']) for r in errors)

targets=['Rosmarinic acid','Daidzein','Fisetin','Hesperidin','Naringin']
cutoff=['Ferulic acid','Morin','Myricetin','Epigallocatechin','Gallic acid']
target_dois={
 'Daidzein':['10.1021/jf053112o'],
 'Hesperidin':['10.1111/j.1750-3841.2010.01717.x'],
 'Rosmarinic acid':['10.3390/molecules28207199'],
 'Fisetin':['10.1038/s41598-025-32257-7'],
 'Naringin':['10.1016/j.foodchem.2021.130605'],
 'Morin':['10.3389/fnut.2022.882458'],
 'Myricetin':['10.1111/j.1750-3841.2010.01717.x'],
}
name_rank={r['canonical_name'].lower():r for r in rank}
def lookup(name):
    x=name_rank.get(name.lower())
    if x:return x['candidate_id']
    for r in screen:
        if r['canonical_name'].lower()==name.lower():return r['candidate_id']
    return ''
target_rows=[]
for name in targets:
    for doi in target_dois.get(name,[]):
        s=scr_d.get(doi,{})
        target_rows.append(dict(candidate_id=lookup(name),candidate_name=name,DOI=doi,publication_year=s.get('year',''),original_article=s.get('title',''),assay_method='ORAC mentioned in metadata; H-ORAC-FL endpoint not verified',reported_value='',reported_unit='',source_location='Abstract/metadata only; original quantitative table not inspected',full_text_access='ABSTRACT_ONLY_OR_NOT_VERIFIED',study_independence='INDEPENDENCE_UNRESOLVED',provisional_rubric_eligibility='NOT_ADJUDICATED',record_status='NEW_EVIDENCE_PENDING_ADJUDICATION',finding='Candidate source only; no eligible numeric evidence established',source_url='https://doi.org/'+doi))
    if name not in target_dois:
        target_rows.append(dict(candidate_id=lookup(name),candidate_name=name,DOI='',publication_year='',original_article='',assay_method='',reported_value='',reported_unit='',source_location='Targeted existing-screen review',full_text_access='NO_SPECIFIC_QUALIFYING_SOURCE_RECOVERED',study_independence='INDEPENDENCE_UNRESOLVED',provisional_rubric_eligibility='NOT_ADJUDICATED',record_status='NO_NEW_EVIDENCE_CONFIRMED',finding='No second eligible original quantitative H-ORAC-FL study verified',source_url=''))
write('Stage25B6B_Single_Record_Targeted_Recovery.csv',list(target_rows[0]),target_rows)

cut_rows=[]
for name in cutoff:
    cid=lookup(name); sm=sum_c.get(cid,{}); ds=target_dois.get(name,[])
    for doi in ds or ['']:
        s=scr_d.get(doi,{})
        cut_rows.append(dict(candidate_id=cid,candidate_name=name,canonical_rank=sm.get('canonical_rank',''),canonical_A_B1_record_N=sm.get('quantitative_record_N',0),canonical_distinct_DOI_proxy_N=sm.get('distinct_DOI_publication_proxy_N',0),confirmed_independent_study_N=sm.get('confirmed_independent_study_N',0),pending_DOI=doi,pending_title=s.get('title',''),supporting_evidence='Existing A/B1 quantitative records; 2022 and 2023 original studies independently confirmed for Gallic Acid' if name=='Gallic acid' else 'Existing A/B1 quantitative records only',non_supporting_evidence='Pending source has no verified pure-compound quantitative H-ORAC-FL value',method_incompatibility='NOT_ASSESSED_OR_NOT_VERIFIED',duplicate_source_risk='NOT_ASSESSED',source_access='ABSTRACT_ONLY_OR_NOT_VERIFIED' if doi else 'NO_TARGETED_SOURCE_VERIFIED',threshold_status=sm.get('proposed_minimum_study_threshold_status','FAIL_ON_AVAILABLE_EVIDENCE'),backfill_decision='ELIGIBLE_VERIFIED_SCENARIO' if sm.get('proposed_minimum_study_threshold_status')=='PASS_VERIFIED' else 'NOT_ELIGIBLE_FOR_VERIFIED_SCENARIO',note='No B2/X or pending source promoted to primary.'))
write('Stage25B6B_Cutoff_and_Backfill_Evidence_Audit.csv',list(cut_rows[0]),cut_rows)

vit=[]
for doi,val,access_v in [('10.1021/jf010586o','0.95','SOURCE_NOT_ACCESSIBLE'),('10.3390/antiox12020505','0.53','ORIGINAL_HTML_VERIFIED')]:
    vit.append(dict(candidate_id='AFF-0104',vitamin_form='L-Ascorbic acid',DOI=doi,historical_value_mol_TE_per_mol=val,original_value_verified='NO' if access_v=='SOURCE_NOT_ACCESSIBLE' else 'YES_TABLE_3',source_access=access_v,original_research='YES_METHOD_ARTICLE' if val=='0.95' else 'YES_EXPERIMENTAL_ARTICLE',independence_status='INDEPENDENCE_UNRESOLVED',assay_compatibility='HISTORICAL_COMPATIBLE_RECHECK_REQUIRED',error_type='UNSPECIFIED_PLUS_MINUS' if val=='0.53' else 'NOT_VERIFIED',canonical_stage25b_record_N=0,proposed_action='FORMAL_V2_RECONCILIATION_REQUEST',review_status='PENDING_HUMAN_REVIEW',source_location='Table 4 cited by historical master; original inaccessible' if val=='0.95' else 'Original article Table 3, TE_AUC; 0.53 ± 0.03',source_url='https://doi.org/'+doi))
write('Stage25B6B_Vitamin_Evidence_Change_Request_Candidates.csv',list(vit[0]),vit)

maturity=[]
for h in history:
    cid=h['candidate_id']; sm=sum_c.get(cid,{})
    maturity.append(dict(candidate_id=cid,candidate_name=h['canonical_name'],earliest_research_year=h['earliest_original_publication_year'],latest_research_year=h['latest_original_publication_year'],research_span_years=h['research_span_years'],original_publication_N=h['metadata_deduplicated_publication_N'],recent_5_year_publication_N=h['recent_5_year_publication_N_2022_2026'],recent_10_year_publication_N=h['recent_10_year_publication_N_2017_2026'],H_ORAC_original_publication_N=sm.get('distinct_original_publication_N',0),H_ORAC_distinct_DOI_proxy_N=sm.get('distinct_DOI_publication_proxy_N',0),confirmed_independent_HORAC_study_N=sm.get('confirmed_independent_study_N',0),metadata_QC_status=h['history_QC'] or 'METADATA_ONLY_NOT_FULLY_VERIFIED',interpretation='General antioxidant/redox history; not specific H-ORAC study count'))
write('Stage25B6B_Research_Maturity_Verified.csv',list(maturity[0]),maturity)

uncert=[]
for rr in rank:
    cid=rr['candidate_id']; rs=by_c[cid]; vs=sorted(float(x['converted_value_mol_TE_per_mol']) for x in rs); es=[x for x in errors if x['candidate_id']==cid]
    q=statistics.quantiles(vs,n=4,method='inclusive') if len(vs)>1 else None
    uncert.append(dict(candidate_id=cid,candidate_name=rr['canonical_name'],potency_median=rr['median_H_ORAC_mol_TE_per_mol'],evidence_eligibility='CANONICAL_A_B1',confirmed_independent_study_N=sum_c[cid]['confirmed_independent_study_N'],distinct_DOI_proxy_N=sum_c[cid]['distinct_DOI_publication_proxy_N'],measurement_typed_error_N=sum(bool(x['reported_SD'] or x['reported_SE'] or x['reported_CI']) for x in es),measurement_any_error_N=sum(bool(x['reported_SD'] or x['reported_SE'] or x['reported_CI'] or x['original_plus_minus_unclassified']) for x in es),between_record_IQR=(q[2]-q[0] if q else ''),range_min=vs[0],range_max=vs[-1],heterogeneity_flag=rr['heterogeneity_flag'],assay_comparability='SOURCE_LEVEL_PARTIAL',source_independence=sum_c[cid]['proposed_minimum_study_threshold_status'],evidence_confidence='NOT_RECALIBRATED',research_maturity='SEPARATE_METADATA_DIMENSION',CI_status='CI_NOT_ESTIMABLE',rank_probability='RANK_PROBABILITY_NOT_ESTIMABLE',study_threshold_status=sum_c[cid]['proposed_minimum_study_threshold_status']))
write('Stage25B6B_Confidence_and_Uncertainty_Readiness.csv',list(uncert[0]),uncert)

sc=[]
sc1_ids={r['candidate_id'] for r in summary if int(r['quantitative_record_N'])>=2}
sc1_order=[r['candidate_id'] for r in rank if r['candidate_id'] in sc1_ids]
for rr in rank:
    cid=rr['candidate_id']; sm=sum_c[cid]; n=int(sm['quantitative_record_N']); s2=sm['proposed_minimum_study_threshold_status']
    sc.append(dict(candidate_id=cid,candidate_name=rr['canonical_name'],canonical_rank=rr['rank'],canonical_median=rr['median_H_ORAC_mol_TE_per_mol'],scenario_0_frozen_membership='YES' if int(rr['rank'])<=20 else 'NO',scenario_1_record_N_threshold='PASS' if n>=2 else 'FAIL',scenario_1_rank=sc1_order.index(cid)+1 if cid in sc1_ids else '',scenario_1_top20_membership='YES' if cid in sc1_order[:20] else 'NO',scenario_2_verified_study_threshold=s2,scenario_2_top20_membership='YES_VERIFIED' if s2=='PASS_VERIFIED' else 'NO_VERIFIED_PASS',scenario_3_threshold_and_uncertainty=s2+';CI_NOT_ESTIMABLE;RANK_PROBABILITY_NOT_ESTIMABLE',prospective_eligibility='NEW_EVIDENCE_PENDING_ADJUDICATION' if cid in {x['candidate_id'] for x in target_rows+cut_rows if x.get('pending_DOI') or x.get('DOI')} else 'NONE_CONFIRMED',note='No pending/B2/X evidence used; unresolved is not PASS.'))
write('Stage25B6B_Top20_Revision_Readiness_Scenarios.csv',list(sc[0]),sc)

cr=[]
def add_cr(cid,typ,doi,change,impact,basis):
    cr.append(dict(change_request_id=f'6B-CR-{len(cr)+1:03d}',candidate_id=cid,affected_experiment_id='',affected_source_id=doi,change_type=typ,current_canonical_state='NO_CHANGE',proposed_change=change,evidence_basis=basis,potential_rank_impact=impact,review_status='PENDING_HUMAN_REVIEW',human_approval_required='YES'))
for x in target_rows:
    if x['DOI']:add_cr(x['candidate_id'],'NEW_SOURCE_SCREEN',x['DOI'],'Retrieve full text; adjudicate quantitative endpoint and v2 eligibility','POSSIBLE',x['source_location'])
for x in cut_rows:
    if x['pending_DOI'] and x['pending_DOI'] not in {y['affected_source_id'] for y in cr}:add_cr(x['candidate_id'],'CUTOFF_SOURCE_SCREEN',x['pending_DOI'],'Retrieve full text; check exclusion/eligibility symmetrically','POSSIBLE',x['pending_title'])
add_cr('AFF-0104','HISTORICAL_CANONICAL_RECONCILIATION','10.1021/jf010586o;10.3390/antiox12020505','Formal v2.0 source-by-source adjudication only after approval','POSSIBLE','Historical 0.95 and original 2023 Table 3 0.53±0.03; first original table inaccessible')
add_cr('ALL_28','STUDY_INDEPENDENCE_THRESHOLD','','Approve or reject N>=2 verified original studies as v1.1 gate','HIGH','Researcher approved direction, not formal v1.1 freeze')
write('Stage25B6B_Proposed_Change_Requests.csv',list(cr[0]),cr)

bad=[]
for h in history:
    try:
        if int(h['latest_original_publication_year'])>2026 or int(h['earliest_original_publication_year'])<1900:bad.append(h['candidate_id'])
    except (ValueError,TypeError):bad.append(h['candidate_id'])
flagged=sum(h['history_QC']=='SOURCE_LATEST_YEAR_FUTURE_OR_INVALID' for h in history)

md('Stage25B6B_Error_Recovery_Coverage_Report_CN.md',f'''# Stage25B.6B 误差回查

68 条 A/B1 记录中，明确 SD/SE/CI 类型 {typed}/68；原文有数值 ± 但类型未明者 {any_error-typed} 条；任意误差信息 {any_error}/68。新增的 7 条来自 [Skroza 2022 原文 Table 2 / Methods 2.2.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/)：每个化合物在 2.5 和 5 µM 两列各有一个 ± 值，Methods 写 3 replicates，但未定义 ± 是 SD 还是 SE。另 13 条来自 [Žuvela 2019 原文 Table 3 / Methods 3.3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/)的 `ln(ORAC) ±`，不能直接作为 mol TE/mol 尺度的 SD。两文重复类型均未证实为独立研究。Carvalho 2023 Table 3 的 3 个 ± 值仍为 `UNSPECIFIED_PLUS_MINUS`。其余未报告的误差保持缺失，不置零。独立实验次数、95%CI 均未取得足以可靠推断的数据。逐条见 `Stage25B6B_Error_Recovery_Master.csv`。''')
md('Stage25B6B_VitaminC_Canonical_Reconciliation_CN.md','''# Vitamin C canonical 衔接

L-Ascorbic acid（AFF-0104）历史表有 2 条 B1：Ou 2001 0.95、Carvalho 2023 0.53 mol TE/mol，历史中位数 0.74。Carvalho 原文 Table 3 已核实 0.53 ± 0.03，± 类型未定义；Ou 原文 Table 4 仍付费不可访问，0.95 未能独立复核。两篇 DOI 不足以证实相互独立的数据采集。两条均未进入 Stage25B canonical 表，现有资料指向迁移/裁决缺口而不是已获批准的纳入。建议经人工批准后进行逐来源 Rubric v2.0 衔接；此轮不迁移。Dehydroascorbic acid 是另一化学形式，不能并入 AFF-0104；Vitamin E 为脂相证据，不与水相 H-ORAC 混排。

原文：[Carvalho 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)；[Ou 2001 出版商页面](https://pubs.acs.org/doi/10.1021/jf010586o)。''')
md('Stage25B6B_Statistical_Method_Readiness_CN.md',f'''# 统计方法可行性

现有 A+B1 中位数是效力排序统计量，不能转译为 95%CI、Top20 入选概率或统计显著性。68 条记录只有 3 条明确 SD，{any_error-typed} 条 ± 类型未明；Caffeic Acid 和 Gallic Acid 各有两项已核实独立原始实验，但尚缺少充分的逐研究误差定义与可比性数据。因此候选物 CI 与 rank probability 均不可估。多记录候选物可报告中位数、IQR、范围作为描述性记录间离散度；只有已核实独立来源的子集可谨慎称研究间比较。若后续明确均值、SD、实验 N、重复类型及方法可比性，可预注册研究层级随机效应模型或层级贝叶斯模型，并用敏感性分析检查单位换算和协议差异；本轮不改变 canonical 中位数。''')

frozen_ok=all(hashlib.sha256((ROOT/r['asset_path']).read_bytes()).hexdigest()==r['sha256'] for r in manifest)
assert frozen_ok
md('Stage25B6B_QC_Report_CN.md',f'''# Stage25B.6B QC

QC01–04：冻结资产 manifest SHA256 {len(manifest)}/{len(manifest)} 匹配；74 条 canonical、A7/B1 61/B2 4/X2、28 rankable、157 候选基线未修改。QC05：仅针对既有筛查记录少量 DOI，未批量处理 1,641 pending。QC06–08、16：DOI 仅作代理；2019、2022、2023 与 Foods 2021 的原始实验在原文定位后计数，其余未自动确认；技术重复和综述未计入研究 N。QC09–10：缺失误差未置零；IQR/范围未解释为 CI。QC11–15、17–19：新来源未纳入正式排名，B2/X 未纳入 primary；不足 20 不补齐；VC 未迁移；研究历史未参与数值排名；新数值未声称来自未定位的原文；未生成 v1.1。QC20：`scripts/build_stage25b6b.py` 可重建 11 CSV 与报告。限制：本轮完成逐来源审计登记，但大多数原文尚未完成全量独立性/误差重提取，不能把登记完成等同于实验证据核实完成。''')

single=sum(int(x['distinct_DOI_publication_proxy_N'])==1 for x in summary)
multi=28-single
md('Stage25B6B_Final_Assessment_CN.md',f'''# Stage25B.6B 最终评估

状态：**STAGE25B.6B BLOCKED BY SPECIFIC EVIDENCE GAPS**。本轮完成 68 条 A/B1 的逐条来源登记、16 个 DOI 的来源索引、28 种候选物的保守研究计数和定点候选来源清单；未完成能证明跨论文数据独立性的原文对照，因此不构成 Top20 v1.1 冻结依据。

Q1–Q3：已确认至少 2 项独立原始研究 **3/28（Caffeic Acid、Quercetin、Gallic Acid）**；已确认恰好 1 项 **20/28**；其余 **5/28** 还没有可确认的独立原始来源。现有 canonical 中 {single} 种仅 1 个 DOI 代理、{multi} 种至少 2 个 DOI 代理；单 DOI 者为 `FAIL_ON_AVAILABLE_EVIDENCE`，并不证明其他文献不存在；多 DOI 但不足 2 项已核实者为 `UNRESOLVED`。三项通过来自 [Žuvela 2019 原文 Methods 3.1–3.3 / Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/)、[Skroza 2022 原文 Methods 2.1 / Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/) 和 [Carvalho 2023 原文 Methods 2.1–2.2 / Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)：不同研究组、各自制备纯品并开展新实验；未把文中模型预测或同文技术重复算作第二研究。

Q4–Q6：明确 SD/SE/CI {typed}/68，任意数值误差由 6A 的 6/68 增至 {any_error}/68；新增 7 条 Skroza 2022 Table 2 的未定义 ±，另 13 条 Žuvela 2019 Table 3 的 `ln(ORAC) ±`，均不是新增可直接使用的 SD。{multi} 种多记录候选物可报告记录间中位数、IQR、范围，不能无条件称为独立研究间分布。正式 95%CI 与入榜概率均不可估。

Q7–Q8：5 种单记录 Top20 仅找到 Daidzein、Hesperidin 等待查论文线索，未核实任何新增合格 H-ORAC-FL 定量研究；没有核实第 20 种符合拟议门槛的候选物。当前 **3** 种达到严格 `PASS_VERIFIED`；6A 的 19 种只是“至少两条记录”情景，不是独立研究达标数。

Q9：VC 2023 原文 Table 3 的 0.53±0.03 已核实，± 类型不明；2001 的 0.95 原表不可访问；独立性未证实。未入 canonical 属待批准的衔接/裁决缺口，不得静默迁移。

Q10：研究成熟度表继承 6A 的元数据去重结果，保留 {flagged} 个未来/无效年份标志，另有 {len(bad)} 个候选物缺少可解析的起止年份；原始论文与综述、重复 DOI、跨候选映射仍需逐项核实，因此不能称为全面通过元数据 QC。一般抗氧化研究数量不等于 H-ORAC 研究数量。

Q11–Q12：尚不能提出可执行 v1.1 冻结方案。变更请求包括独立研究门槛、单记录/边界候选来源全文裁决、VC 衔接；详见 CR 清单，均待人工批准。

Q13：建议继续定点检索 Daidzein（10.1021/jf053112o）、Hesperidin/Myricetin（10.1111/j.1750-3841.2010.01717.x）、Rosmarinic acid 与 Naringin 的纯品 H-ORAC-FL 原表，以及 Ferulic/Morin/Gallic 的边界补证；需先得到研究者对范围和资源的批准，不扩大至全部 pending。

Q14：可向导师明确解释：效力中位数、证据资格、研究独立性、测量精度、研究成熟度和排名不确定性是不同维度；描述性 IQR 不是 CI，High confidence 不是 95% 入榜概率。

Q15：建议进入 6C 的前提是取得关键全文、完成跨 DOI 数据集比对和误差定义定位，并批准正式门槛与 CR；本轮不自动启动。

## HUMAN DECISIONS REQUIRED

| ID | 推荐选项 | 依据/未解问题 | 影响 | 需批准 |
|---|---|---|---|---|
| D1 | 暂不正式启用 N≥2 门槛 | 3/28 通过严格核实；其余需原文比对 | v1.1 资格 | 是 |
| D2 | 批准定点原文进入 v2.0 裁决，不自动纳入 | 候选来源无已核实定量值 | 新证据 | 是 |
| D3 | 批准 VC 逐来源衔接 | 2001 原表不可访问，2023 已定位 | VC 资格 | 是 |
| D4 | 批准关键来源误差提取 | 类型仅 {typed}/68 | CI 可行性 | 是 |
| D5 | 仅扩大上述点名候选物检索 | 5 个单记录和 cutoff 缺口 | 入选集合 | 是 |
| D6 | 接受不足 20 的候选集原则 | 门槛不可为凑数放宽 | 名单规模 | 是 |
| D7 | 暂不启动正式修订 | 独立性、误差与 VC 缺口 | v1.1 冻结 | 是 |

原始支持：[Carvalho 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)、[Ou 2001 出版商摘要](https://pubs.acs.org/doi/10.1021/jf010586o)。''')

sync_text=f'''# CHATGPT_SYNC_STAGE25B6B

A. Stage25B.6B 审计资产完成；状态为 **BLOCKED BY SPECIFIC EVIDENCE GAPS**，不启动 6C、不冻结 v1.1。

B. Git baseline SHA：`0fb723abf0f32980520692430e92a37ab6447bab`；本轮提交 SHA 见 Codex 最终同步说明（提交无法在自身内容中嵌入自身 SHA）。

C. 28 种候选物、68 条 A/B1、16 个 DOI：严格确认 ≥2 独立研究 3（Caffeic Acid、Quercetin、Gallic Acid）；20 种恰好 1 项已确认、5 种 0 项，多数来源仍有未解决的独立性。{single} 种仅 1 DOI 代理，{multi} 种 ≥2 DOI 代理。DOI 不等于研究。

D. 明确误差类型 {typed}/68，任意误差 {any_error}/68；新增 7 条 Skroza 2022 和 13 条 Žuvela 2019 的未定义 ±，没有新增可确认误差类型。

E. 5 种单记录 Top20 未核实第二项合格定量研究；Daidzein/Hesperidin 等只有待裁决线索。

F. VC：2023 原表 0.53±0.03 已核，± 类型不明；Ou 2001 原表不可访问；canonical 0 条，需批准衔接。

G. 研究成熟度仅是一般抗氧化元数据维度，{flagged} 个未来/无效年份标志及 {len(bad)} 个空白年份待修；不参与效力排名。

H. Scenario 0=原冻结 20；Scenario 1=至少 2 记录，19 种；Scenario 2/3=严格已核实通过 3，不能补齐 20。

I. 缺口：关键论文全文、跨 DOI 数据集独立性、误差定义、VC 2001 原表。

J. Human decisions D1–D7 见最终评估；全部待研究者批准。

K. 建议有范围地进行 6C 原文获取和两两来源比对；本轮停止。

P0：本文件、`docs/qc/stage25b6b/Stage25B6B_Final_Assessment_CN.md`、研究计数、情景、CR CSV。P1：来源/逐条研究、误差、VC、定点恢复及 QC。P2：成熟度及辅助诊断 CSV。'''
(SYNC / 'CHATGPT_SYNC_STAGE25B6B.md').write_text(sync_text,encoding='utf-8')
print(f'OK: {len(sources)} sources, {len(studies)} records, {len(summary)} candidates, typed_error={typed}, any_error={any_error}, one_DOI={single}, >=2_DOI={multi}, frozen_manifest={len(manifest)}/{len(manifest)}')
