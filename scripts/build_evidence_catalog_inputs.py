"""Normalize catalogue links, never re-grade evidence or overwrite scientific tables."""
from pathlib import Path
import csv,json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'workspaces/repository_review_20261030'
base=json.loads((OUT/'Baseline.json').read_text(encoding='utf8'))
def rows(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def get(r,*keys):return next((r.get(k,'') for k in keys if r.get(k,'') not in ('','NA','N/A')), '')
papers={}; pmids={}; conflicts=[]
def paper(r,p,n):
 doi=get(r,'DOI','doi','original_paper_DOI').strip();doi=re.sub(r'^https?://(?:dx\.)?doi.org/','',doi,flags=re.I).lower()
 raw_doi=doi
 if doi and (not re.match(r'^10\.\d{4,9}/\S+$',doi) or ';' in doi or doi.count('10.')>1):doi=''
 pmid=get(r,'PMID','pmid').strip();pmid=pmid if pmid.isdigit() else ''
 title=get(r,'paper_title','article_title','title','study')
 key='DOI:'+doi if doi else pmids.get(pmid,'PMID:'+pmid) if pmid else 'ROW:'+p+':'+str(n)
 if pmid and doi:
  if pmid in pmids and pmids[pmid]!=key:conflicts.append([pmid,pmids[pmid],key,p,n])
  else:pmids[pmid]=key
 if key not in papers:papers[key]={'文献ID':key,'题名':title,'DOI':doi,'PMID':pmid,'年份':get(r,'year','publication_year','publication_date'),'期刊原始名称':get(r,'journal'),'类型原始值':get(r,'publication_type','original_or_review','review_or_original','original_research_yes_no'),'文献链接':get(r,'article_url') or ('https://doi.org/'+doi if doi else 'https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/' if pmid else ''),'首次来源表':p,'来源数据记录号':n,'元数据状态':'复合或格式异常DOI仅保留原引文，不作为单篇DOI' if raw_doi and not doi else '既有记录转录；本轮不等于全文重核','原始DOI字段':raw_doi}
 else:
  q=papers[key]
  for k,v in [('题名',title),('期刊原始名称',get(r,'journal')),('PMID',pmid),('年份',get(r,'year','publication_year','publication_date'))]:
   if not q[k] and v:q[k]=v
 return key
evidence=[]; association=[]; screening=[]; audits=[]
mechanism='workspaces/phase1c_mechanism_evidence_pilot/compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'
originals=[r['path'] for r in base['csv_tables'] if r['path'].startswith(('data/class_specific_antioxidant/','data/metal_and_micronutrients/')) and any(k in r.get('headers',[]) for k in ['DOI','original_paper_DOI']) and not r['path'].endswith('Paper_Summary.csv')]
originals+=['data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv',mechanism]
for p in originals:
 for n,r in enumerate(rows(p),1):
  pid=paper(r,p,n);me=p==mechanism
  section='结果：机制证据图谱；讨论：因果与功能边界' if me else '结果：化学抗氧化或功能证据；方法：检测构念与可比性'
  level=get(r,'H_ORAC_tier','evidence_tier','tier','evidence_strength','evidence_status')
  evidence.append({'目录证据ID':'CAT-'+hashlib.sha256((p+':'+str(n)).encode()).hexdigest()[:12], '原证据ID':get(r,'evidence_id','independent_experiment_id','paper_id'),'文献ID':pid,'候选物ID':get(r,'candidate_id'),'候选物':get(r,'canonical_name','compound_name','compound','nutrient'),'证据构念':get(r,'assay','assay_name_reported','assay_type','primary_construct_candidate','construct','assay_method'),'模型或环境':get(r,'experimental_model','assay_phase','lipid_system','solvent','buffer_or_medium'),'原始结果':get(r,'raw_reported_value','original_value','original_kq_value','functional_outcome'),'原始单位':get(r,'raw_unit','original_unit','unit'),'原证据等级':level,'等级依据原文':get(r,'tier_rationale','quality_note','major_method_caveat','notes'),'证据解释边界':'计算不等于结合；未人工批准机制不可作验证结果' if me else '特定构念内解释；不跨方法直接相加；不推断人体获益','建议文章章节':section,'章节状态':'建议；尚无已批准文章大纲','文章论点支持强度':'待人工逐论点评估；保留原等级，不新设评分','原人工状态':get(r,'human_review_status','second_reviewer_status','reviewer'),'当前目录人工状态':'NOT_REVIEWED','来源定位':get(r,'source_locator','exact_location') or '; '.join(get(r,k) for k in ['exact_table','exact_figure','exact_page','source_page','source_table','source_figure','source_supplement'] if get(r,k)),'本地原文':get(r,'source_local_path'),'来源表':p,'来源数据记录号':n,'原始行SHA256':hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest()})
for p in ['data/class_specific_antioxidant/Aqueous_Antioxidant_Paper_Summary.csv','workspaces/phase1c_mechanism_evidence_pilot/master/Study_Register.csv']:
 for n,r in enumerate(rows(p),1):paper(r,p,n)
for p in ['data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv']:
 for n,r in enumerate(rows(p),1):
  pid=paper(r,p,n)
  association.append({'文献ID':pid,'候选物ID':r['candidate_id'],'候选物':r['canonical_name'],'检索相关性原值':r['antioxidant_redox_relevant'],'纳入元数据指标原值':r['include_primary_metric'],'证据领域原值':r['relevance_domain'],'来源数据记录号':n,'状态':'题录关联；不是全文核实观察','来源表':p})
for p in ['data/h_orac_stage25b/stage25b/Stage25B_HORAC_Publication_Screening.csv','workspaces/phase1c_mechanism_evidence_pilot/search_logs/Protocatechuic_Acid_Screening_Log.csv']:
 for n,r in enumerate(rows(p),1):
  pid=paper(r,p,n);screening.append({'文献ID':pid,'候选物ID':get(r,'candidate_id') or ('AFF-0061' if 'Protocatechuic' in p else ''),'筛选决定原值':get(r,'screening_decision','method_screen_status'),'全文状态原值':get(r,'full_text_status','full_text_checked'),'排除或待决理由':get(r,'reason_CN','exclusion_reason','notes'),'来源表':p,'来源数据记录号':n})
for p in ['data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv','data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv','workspaces/phase1c_mechanism_evidence_pilot/batch_a_targeted_followup/BatchA_Human_Adjudication_Preparation.csv']:
 for n,r in enumerate(rows(p),1):
  pid=paper(r,p,n);audits.append({'文献ID':pid,'证据或实验ID':get(r,'evidence_id','experiment_id','source_id'),'候选物ID':get(r,'candidate_id','candidate_ids'),'来源状态原值':get(r,'fulltext_status','codex_adjudication_candidate','confidence_in_extraction'),'后续问题原值':get(r,'candidate_reason','source_issue','notes','source_location','original_source_location'),'原人工状态':get(r,'human_review_status'),'来源表':p,'来源数据记录号':n})
# Title-only records deliberately remain separate; do not collapse papers by fuzzy title.
journals=sorted({r['期刊原始名称'] for r in papers.values() if r['期刊原始名称']})
jt=[{'期刊原始名称':j,'JCR发布版年':2026,'JIF数据年_待官方逐刊确认':2025,'最新JIF':None,'JCR学科类别':'','JCR分区':'','期刊指标核实状态':'UNVERIFIED_OFFICIAL_JCR_ACCESS_403','查询日期':'2026-10-30','官方入口':'https://jcr.clarivate.com/','期刊搜索线索':'https://mjl.clarivate.com/','指标证据链接或导出表路径':'','人工核实备注':'按每个JCR学科类别分别登记；不可用中科院分区替代；IF不等于文章证据质量'} for j in journals]
tableindex=[]
for r in base['csv_tables']:
 p=r['path']
 if 'phase2_r_partial_library' in p:continue
 role='历史/冻结/检查点；不计为新增独立研究' if p.startswith('archive/') or '/checkpoints/' in p else '演练/过程；不计为正式证据' if any(s in p for s in ['dryrun','rebuild_check','gate2_review']) else '当前源表/审核/元数据；见逐表语义'
 tableindex.append({'来源表':p,'数据记录数':r.get('rows',0),'目录角色':role,'已抽取为具体观察':p in originals,'SHA256':next(f['sha256'] for f in base['files'] if f['path']==p),'列名':' ; '.join(r.get('headers',[]))})
payload={'papers':list(papers.values()),'evidence':evidence,'association':association,'screening':screening,'audits':audits,'journals':jt,'tables':tableindex,'conflicts':conflicts,'original_tables':originals}
(OUT/'Catalog_Input.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf8')
print(json.dumps({k:len(v) for k,v in payload.items()},ensure_ascii=False))
