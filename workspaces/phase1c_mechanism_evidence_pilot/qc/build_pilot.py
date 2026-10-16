"""Build isolated v0.1 pilot from retained public-source metadata and reviewed observations.
No source-table writes, no Git mutations, no network analysis. Python standard library only.
"""
from pathlib import Path
import csv,json,hashlib,re,subprocess,datetime,xml.etree.ElementTree as ET
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'workspaces/phase1c_mechanism_evidence_pilot';RAW=OUT/'search_logs/raw'
def j(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def readjson(p):return json.loads(p.read_text(encoding='utf-8'))
def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def write(name,value):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:f.write(value if isinstance(value,str) else j(value))
def csvout(name,rows):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT).decode('utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (OUT/'master/Compound_Mechanism_Evidence_Master.csv').exists(),'Stop: output already exists'
baseline=readjson(OUT/'qc/Start_Baseline.json')
assert git('rev-parse','HEAD')==baseline['HEAD']
t002=readcsv(ROOT/'data/candidate_universe/Antioxidant_Class_Candidate_Master.csv');assert len(t002)==191
compound=next(r for r in t002 if r['candidate_id']=='AFF-0061')
ref=readjson(RAW/'PubChem_CID72.json')['response']['PropertyTable']['Properties'][0]
assert compound['PubChem_CID']==str(ref['CID']) and compound['InChIKey']==ref['InChIKey'] and compound['molecular_formula']==ref['MolecularFormula']
uniprot=readjson(RAW/'UniProt_Target_Identifiers.json')['response']['results']
def accession(gene,species):
 hits=[x['primaryAccession'] for x in uniprot if x['organism']['scientificName']==species and any(g.get('geneName',{}).get('value','').casefold()==gene.casefold() for g in x.get('genes',[]))]
 return hits[0] if len(hits)==1 else 'UNRESOLVED'
ep=readjson(RAW/'EPMC01_results.json')['results'];focus=readjson(RAW/'EPMC02_results.json')['results']
epmid={r['id']:r for r in ep if r['source']=='MED'}
pub={}
for filename in ['Selected_PubMed_Metadata.xml','Additional_PubMed_Metadata.xml']:
 for a in ET.parse(RAW/filename).findall('./PubmedArticle'):
  pmid=a.findtext('./MedlineCitation/PMID');article=a.find('./MedlineCitation/Article')
  ids={x.get('IdType'):x.text for x in a.findall('./PubmedData/ArticleIdList/ArticleId')}
  dates=article.findall('./ArticleDate');date_type='ELECTRONIC_PUBLICATION';precision='DAY'
  if dates:
   d=dates[0];dateval='-'.join([d.findtext('Year'),d.findtext('Month').zfill(2),d.findtext('Day').zfill(2)])
  else:
   d=article.find('./Journal/JournalIssue/PubDate');y=d.findtext('Year','');m=d.findtext('Month','');day=d.findtext('Day','')
   months={x:i for i,x in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],1)}
   m=str(months[m]) if m in months else m
   dateval=y+('-'+m.zfill(2) if m else '')+('-'+day.zfill(2) if day else '')
   precision='DAY' if day else 'MONTH' if m else 'YEAR';date_type='JOURNAL_ISSUE_DATE'
  pub[pmid]={'study_id':'ST-PMID-'+pmid,'PMID':pmid,'DOI':ids.get('doi','NOT_REPORTED'),'PMCID':ids.get('pmc','NOT_AVAILABLE'),'article_title':''.join(article.find('ArticleTitle').itertext()),'journal':article.findtext('./Journal/Title'),'publication_date':dateval,'publication_date_type':date_type,'publication_date_precision':precision,'article_url':'https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/','retraction_status':'RETRACTED' if a.find(".//CommentsCorrections[@RefType='RetractionIn']") is not None else 'RETRACTION_NOTICE' if a.find(".//CommentsCorrections[@RefType='RetractionOf']") is not None else 'NO_RETRACTION_LINK_IN_RETRIEVED_PUBMED','raw_date_metadata':j([ET.tostring(x,encoding='unicode') for x in article.findall('./ArticleDate')]+[ET.tostring(article.find('./Journal/JournalIssue/PubDate'),encoding='unicode')]),'bibliographic_verification':'PUBMED_AND_EPMC' if pmid in epmid else 'PUBMED_XML','publication_independence':'UNIQUE_PUBLICATION_ID; CROSS_PAPER_EXPERIMENT_REUSE_NOT_FULLY_ASSESSED'}
included=['32520409','37482908','39589556','41594941','42170612','37025617','42413844','32007785','11023549','11714376']
full=['32520409','37482908','39589556','41594941','42170612','37025617']
evidence=[]
required='candidate_id compound_name compound_form PubChem_CID InChIKey study_id article_title DOI PMID journal publication_date publication_date_type article_url target_gene target_protein UniProt_ID target_species target_role target_effect_direction pathway_name pathway_ID pathway_database pathway_effect_direction experimental_model species cell_line_or_tissue dose dose_unit treatment_duration assay_method control_group evidence_id evidence_relation_type target_validation_status functional_outcome effect_context source_figure_or_table source_verification_status evidence_status notes'.split()
extra='PMCID publication_date_precision compound_form_as_reported identity_mapping_status identity_reference_url experiment_id observation_endpoint administration_route pretreatment_duration challenge_agent challenge_dose challenge_duration target_experimental_support direct_target_status target_identifier_status target_identifier_source source_local_path source_locator source_result_paraphrase_CN source_review_mode search_source_ids extraction_date extracted_by human_review_status publication_status experiment_independence_status'.split()
fields=required+extra
def add(pmid,serial,**v):
 s=pub[pmid];isfull=pmid in full
 row={f:'UNRESOLVED' for f in fields};row.update({k:s[k] for k in ['study_id','article_title','DOI','PMID','journal','publication_date','publication_date_type','article_url','PMCID','publication_date_precision']})
 local='search_logs/raw/'+(s['PMCID']+'.xml') if (RAW/(s['PMCID']+'.xml')).exists() else 'search_logs/raw/PMC7443473_browser_response.html' if pmid=='32520409' else 'search_logs/raw/'+('Additional_PubMed_Metadata.xml' if pmid in ['11023549','11714376'] else 'Selected_PubMed_Metadata.xml')
 row.update(candidate_id='AFF-0061',compound_name=compound['canonical_name'],compound_form='PARENT_ACID_AUTHOR_REPORTED',PubChem_CID=compound['PubChem_CID'],InChIKey=compound['InChIKey'],compound_form_as_reported='protocatechuic acid',identity_mapping_status='PARENT_REFERENCE_LINK_NOT_SAMPLE_ANALYTICALLY_VERIFIED',identity_reference_url='https://pubchem.ncbi.nlm.nih.gov/compound/72',evidence_id=f'ME-AFF0061-{pmid}-{serial:03d}',experiment_id=f'EXP-{pmid}-{serial:03d}',target_gene='NOT_APPLICABLE',target_protein='NOT_APPLICABLE',UniProt_ID='NOT_APPLICABLE',target_species='NOT_APPLICABLE',target_role='NOT_APPLICABLE',target_effect_direction='NOT_APPLICABLE',pathway_name='NOT_APPLICABLE',pathway_ID='NOT_APPLICABLE',pathway_database='NOT_APPLICABLE',pathway_effect_direction='NOT_APPLICABLE',administration_route='NOT_APPLICABLE',pretreatment_duration='NOT_APPLICABLE',challenge_agent='NONE',challenge_dose='NOT_APPLICABLE',challenge_duration='NOT_APPLICABLE',source_verification_status='FULL_TEXT_VERIFIED' if isfull else 'ABSTRACT_ONLY',evidence_status='PILOT_PROVISIONAL',source_local_path=local,source_review_mode='METHODS_RESULTS_AND_LEGEND_TEXT; IMAGES_NOT_INDEPENDENTLY_AUDITED' if isfull else 'PUBMED_ABSTRACT_TEXT_ONLY',source_figure_or_table='UNRESOLVED_ABSTRACT_ONLY' if not isfull else 'UNRESOLVED',source_locator='PubMed Abstract' if not isfull else 'UNRESOLVED',target_experimental_support='YES_FULL_TEXT' if isfull else 'REPORTED_ABSTRACT_ONLY',direct_target_status='NOT_ESTABLISHED',target_identifier_status='NOT_APPLICABLE',target_identifier_source='NOT_APPLICABLE',extraction_date='2026-10-16',extracted_by='CODEX_SOURCE_REVIEW',human_review_status='NOT_REVIEWED',publication_status=s['retraction_status'],experiment_independence_status='WITHIN_PUBLICATION_LINKED; CROSS_PUBLICATION_REUSE_UNRESOLVED',search_source_ids='EPMC01; EPMC02' if any(r.get('id')==pmid and r.get('source')=='MED' for r in focus) else 'EPMC01',notes='未进行人体疗效或膳食剂量可达性推断。')
 row.update(v)
 if row['target_gene'] not in ['NOT_APPLICABLE','UNRESOLVED']:
  row['UniProt_ID']=accession(row['target_gene'],row['target_species'])
  row['target_identifier_status']='REFERENCE_IDENTIFIER_MATCH_NOT_EXPERIMENTAL_VALIDATION' if row['UniProt_ID']!='UNRESOLVED' else 'UNRESOLVED_SPECIES_OR_GENE'
  row['target_identifier_source']='search_logs/raw/UniProt_Target_Identifiers.json'
 if row['pathway_name']!='NOT_APPLICABLE':row['pathway_ID']='UNRESOLVED';row['pathway_database']='AUTHOR_NAMED_AXIS_OR_PROCESS_NOT_ONTOLOGY_MAPPED'
 evidence.append(row)

add('32520409',1,target_gene='Sirt3',target_protein='SIRT3',target_species='Mus musculus',target_role='FUNCTIONAL_MEDIATOR',target_effect_direction='DEPENDENCE_SUPPORTED',pathway_name='SIRT3/ACSF3-associated hepatic lipid metabolism',pathway_effect_direction='PROTECTIVE_EFFECT_ATTENUATED_BY_KNOCKOUT',experimental_model='IN_VIVO',species='Mus musculus',cell_line_or_tissue='C57BL/6 WT and global Sirt3 knockout; liver',dose='30',dose_unit='mg/kg/day',treatment_duration='8 weeks',administration_route='NOT_REPORTED',challenge_agent='high-fat diet',challenge_dose='2% cholesterol; 7% lard; 8.3% yolk; 16.7% sucrose; 66% standard diet',challenge_duration='8 weeks',assay_method='Sirt3 knockout; liver histology',control_group='WT HFD without PCA; Sirt3 knockout HFD with/without PCA; genotype-specific normal diet',evidence_relation_type='FUNCTIONAL_CAUSAL',target_validation_status='GENETIC_LOSS_OF_FUNCTION_DEPENDENCE',functional_outcome='PCA对肝脂肪变的改善在Sirt3缺失小鼠中丧失。',observation_endpoint='hepatic steatosis histology',effect_context='高脂饮食；跨基因型比较；直接结合未验证。',source_figure_or_table='Figure 2l',source_locator='Methods 2.1; Results 3.3; Figure 2l',source_result_paraphrase_CN='敲除支持SIRT3功能参与，不证明PCA直接结合。')
add('32520409',2,target_gene='SIRT3',target_protein='SIRT3; PDB 3GLS model',target_species='UNRESOLVED',target_role='PREDICTED_BINDING_TARGET',target_effect_direction='PREDICTED_BINDING',experimental_model='IN_SILICO',species='NOT_APPLICABLE',cell_line_or_tissue='NOT_APPLICABLE',dose='NOT_APPLICABLE',dose_unit='NOT_APPLICABLE',treatment_duration='NOT_APPLICABLE',assay_method='AutoDock Vina molecular docking',control_group='NOT_REPORTED',evidence_relation_type='COMPUTATIONAL_PREDICTION',target_validation_status='PREDICTION_ONLY',functional_outcome='对接提出PCA与SIRT3口袋相互作用。',observation_endpoint='predicted ligand-pocket pose',effect_context='蛋白模型物种未独立核实；无生物物理结合实验证据。',source_figure_or_table='Figure 2c-d',source_locator='Methods 2.8; Results 3.3; Figure 2c-d',source_result_paraphrase_CN='论文对接措辞不升级为直接结合。',target_experimental_support='NO_FOR_THIS_OBSERVATION',direct_target_status='PREDICTED_ONLY')
add('37482908',1,target_gene='Kmo',target_protein='Kynurenine 3-monooxygenase',target_species='Mus musculus',target_role='OMICS_ASSOCIATED_GENE',target_effect_direction='DECREASED',experimental_model='IN_VIVO',species='Mus musculus',cell_line_or_tissue='male C57BL/6NTac; heart',dose='100',dose_unit='mg/kg/day',treatment_duration='9 days',administration_route='INTRAMUSCULAR',challenge_agent='isoproterenol infusion',challenge_dose='80 mg/kg/day',challenge_duration='14 days',assay_method='RNA sequencing',control_group='ISO+DMSO versus ISO+PCA; sham+DMSO reference',evidence_relation_type='OMICS_ASSOCIATION',target_validation_status='OMICS_ASSOCIATION_ONLY',functional_outcome='Kmo在PCA干预相关转录组候选基因中下调。',observation_endpoint='Kmo transcript abundance',effect_context='第6天开始PCA；RNA-seq相关，不构成直接靶点。',source_figure_or_table='Figure 4A,C',source_locator='Methods 2.2,2.11; Results 3.4; Figure 4A,C',source_result_paraphrase_CN='RNA-seq用于候选发现。',target_experimental_support='YES_OMICS_ONLY')
add('37482908',2,target_gene='Kmo',target_protein='Kynurenine 3-monooxygenase',target_species='Mus musculus',target_role='MEASURED_EXPRESSION_RESPONSE',target_effect_direction='DECREASED',experimental_model='IN_VIVO',species='Mus musculus',cell_line_or_tissue='male C57BL/6NTac; heart',dose='100',dose_unit='mg/kg/day',treatment_duration='9 days',administration_route='INTRAMUSCULAR',challenge_agent='isoproterenol infusion',challenge_dose='80 mg/kg/day',challenge_duration='14 days',assay_method='qRT-PCR',control_group='ISO+DMSO versus ISO+PCA',evidence_relation_type='PATHWAY_MODULATION',target_validation_status='EXPRESSION_CHANGE_ONLY',functional_outcome='Kmo mRNA降低。',observation_endpoint='Kmo mRNA qRT-PCR',effect_context='同一动物研究的独立检测，非第二项独立研究；不根据平行siRNA表型认定药物依赖。',source_figure_or_table='Figure 5D',source_locator='Methods 2.2,2.5; Results 3.4; Figure 5D',source_result_paraphrase_CN='qPCR验证转录变化，不证明直接结合。')
add('39589556',1,target_gene='Nfe2l2',target_protein='NRF2',target_species='Mus musculus',target_role='FUNCTIONAL_MEDIATOR',target_effect_direction='DEPENDENCE_SUPPORTED',pathway_name='NRF2-associated ferroptosis defense',pathway_effect_direction='PROTECTIVE_EFFECT_ATTENUATED_BY_KNOCKOUT',experimental_model='IN_VIVO',species='Mus musculus',cell_line_or_tissue='male C57BL/6J WT and Nrf2 knockout; liver',dose='100',dose_unit='mg/kg/day',treatment_duration='10 weeks',administration_route='ORAL',challenge_agent='high-fat diet',challenge_dose='60 kcal% fat',challenge_duration='10 weeks',assay_method='Nrf2 knockout; liver BODIPY lipid-peroxidation staining',control_group='genotype-matched high-fat diet without PCA; normal-diet groups',evidence_relation_type='FUNCTIONAL_CAUSAL',target_validation_status='GENETIC_LOSS_OF_FUNCTION_DEPENDENCE',functional_outcome='PCA降低肝脂质过氧化的作用在Nrf2缺失时受限。',observation_endpoint='liver lipid peroxidation (BODIPY)',effect_context='动物模型功能参与；不证明NRF2为直接结合蛋白。',source_figure_or_table='Figure 6L',source_locator='Methods Animal studies; Figure 6L; associated Results',source_result_paraphrase_CN='敲除对照支持NRF2参与抗脂质过氧化效应。')
add('39589556',2,pathway_name='oxidative stress response gene-set enrichment',pathway_effect_direction='ENRICHMENT_ASSOCIATION_DIRECTION_NOT_ASSIGNED',experimental_model='IN_VITRO',species='Homo sapiens',cell_line_or_tissue='MHCC97-H',dose='5',dose_unit='µM',treatment_duration='16 h',assay_method='RNA-seq and gene ontology enrichment',control_group='untreated cells',evidence_relation_type='OMICS_ASSOCIATION',target_validation_status='NOT_APPLICABLE_PATHWAY_ONLY',functional_outcome='差异基因富集涉及氧化应激相关过程。',observation_endpoint='oxidative-stress-related enriched terms',effect_context='富集不等于通路激活方向或任何蛋白直接靶点。',source_figure_or_table='Figure 2D',source_locator='Methods RNA sequencing; Figure 2D',source_result_paraphrase_CN='仅记录基因集富集，不转为蛋白靶点。',target_experimental_support='NOT_APPLICABLE')
for serial,gene,protein,direction,panel in [(1,'HDAC1','HDAC1','DECREASED','4I-J'),(2,'GATA4','GATA4','INCREASED','4I-J'),(3,'RELA','NF-κB p65','DECREASED_NUCLEAR_TRANSLOCATION','4E')]:
 add('41594941',serial,target_gene=gene,target_protein=protein,target_species='Homo sapiens',target_role='MEASURED_EXPRESSION_OR_LOCALIZATION_RESPONSE',target_effect_direction=direction,pathway_name='HDAC1/GATA4-associated NF-κB signaling',pathway_effect_direction='INFLAMMATORY_SIGNALING_ATTENUATED',experimental_model='IN_VITRO',species='Homo sapiens',cell_line_or_tissue='HUVEC',dose='100',dose_unit='µM',treatment_duration='24 h',challenge_agent='angiotensin II pretreatment',challenge_dose='1 µM',challenge_duration='24 h before PCA',assay_method='immunofluorescence' if gene=='RELA' else 'western blot',control_group='Ang II with normal medium after 24 h; untreated control',evidence_relation_type='PATHWAY_MODULATION',target_validation_status='LOCALIZATION_OR_EXPRESSION_CHANGE_ONLY',functional_outcome=protein+'：'+direction,observation_endpoint=protein+' nuclear localization' if gene=='RELA' else protein+' abundance',effect_context='不把表达/定位变化当直接结合或必要性。',source_figure_or_table='Figure '+panel,source_locator='Methods 2.8-2.11; Results 3.4; Figure '+panel,source_result_paraphrase_CN='PCA处理后的蛋白表达/定位响应。')
add('41594941',4,target_gene='HDAC1',target_protein='HDAC1',target_species='UNRESOLVED',target_role='PREDICTED_BINDING_TARGET',target_effect_direction='PREDICTED_BINDING',experimental_model='IN_SILICO',species='NOT_APPLICABLE',cell_line_or_tissue='NOT_APPLICABLE',dose='NOT_APPLICABLE',dose_unit='NOT_APPLICABLE',treatment_duration='NOT_APPLICABLE',assay_method='AutoDock Vina docking and molecular dynamics',control_group='NOT_REPORTED',evidence_relation_type='COMPUTATIONAL_PREDICTION',target_validation_status='PREDICTION_ONLY',functional_outcome='计算模型预测PCA与HDAC1相互作用。',observation_endpoint='predicted binding pose and simulation stability',effect_context='未将模拟结合稳定性解释为实验直接结合。',source_figure_or_table='Figure 6',source_locator='Methods 2.14-2.16; Results 3.6; Figure 6',source_result_paraphrase_CN='对接/MD预测与细胞实验分行。',target_experimental_support='NO_FOR_THIS_OBSERVATION',direct_target_status='PREDICTED_ONLY')
add('41594941',5,target_gene='GATA4',target_protein='GATA4',target_species='Homo sapiens',target_role='GENETIC_PERTURBATION_READOUT',target_effect_direction='NO_ADDITIONAL_CHANGE',pathway_name='HDAC1/GATA4-associated NF-κB signaling',pathway_effect_direction='NO_SIGNIFICANT_ADDITIONAL_EFFECT',experimental_model='IN_VITRO',species='Homo sapiens',cell_line_or_tissue='HUVEC with si-HDAC1',dose='100',dose_unit='µM',treatment_duration='24 h',challenge_agent='Ang II; si-HDAC1 transfection',challenge_dose='Ang II 1 µM; siRNA 100 pmol/well',challenge_duration='Ang II 24 h; siRNA knockdown assessed at 48 h',assay_method='western blot with HDAC1 siRNA intervention',control_group='Ang II+PCA alone; Ang II+si-HDAC1 alone',evidence_relation_type='PATHWAY_MODULATION',target_validation_status='GENETIC_PHENOCOPY_NONADDITIVITY_NOT_NECESSITY',functional_outcome='联合干预对GATA4的额外改善未达统计学显著。',observation_endpoint='GATA4 abundance under combined intervention',effect_context='阴性增量结果；平行表型及非加和不自动证明PCA作用必须依赖HDAC1。',source_figure_or_table='Figure 5C-D',source_locator='Methods 2.13; Results 3.5; Figure 5C-D',source_result_paraphrase_CN='保留联合组无显著额外效应，不升级为救援或必要性。',notes='转染与药物完整时间线需Gate 2逐图复核；未分析未取样的其他剂量。')
add('42170612',1,target_gene='UNRESOLVED',target_protein='α-amylase; reagent species/isoform unresolved',target_species='UNRESOLVED',target_role='BIOPHYSICAL_BINDING_PREPARATION',target_effect_direction='BINDING_REPORTED',experimental_model='CELL_FREE',species='UNRESOLVED',cell_line_or_tissue='commercial α-amylase preparation',dose='12',dose_unit='mmol/L syringe concentration',treatment_duration='19 injections; 60 s injection; 90 s interval',assay_method='isothermal titration calorimetry at 25 °C',control_group='PCA titrated into PBS; dilution heat subtracted',evidence_relation_type='DIRECT_BINDING',target_validation_status='BINDING_REPORTED_TARGET_PREPARATION_CONFLICT',functional_outcome='ITC报告相互作用热信号。',observation_endpoint='ITC thermogram and binding isotherm',effect_context='方法写α-amylase 7.6 µM，Figure 2B图注写saliva；蛋白来源物种未报告。',source_figure_or_table='Figure 2B',source_locator='Methods 2.7.2; Results 3.3; Figure 2B',source_result_paraphrase_CN='保留生物物理观察，但因方法/图注不一致而暂停具体直接靶点认定。',direct_target_status='UNRESOLVED_SOURCE_CONFLICT',evidence_status='HOLD_TARGET_PREPARATION_REVIEW',notes='12 mmol/L为注射器浓度，不是滴定池最终暴露浓度；不赋予人AMY1/AMY2或UniProt。')
add('42170612',2,target_gene='TAS2R16',target_protein='hTAS2R16',target_species='Homo sapiens',target_role='PREDICTED_BINDING_TARGET',target_effect_direction='PREDICTED_BINDING',experimental_model='IN_SILICO',species='NOT_APPLICABLE',cell_line_or_tissue='NOT_APPLICABLE',dose='NOT_APPLICABLE',dose_unit='NOT_APPLICABLE',treatment_duration='100 ns simulation',assay_method='molecular dynamics',control_group='NOT_REPORTED',evidence_relation_type='COMPUTATIONAL_PREDICTION',target_validation_status='PREDICTION_ONLY',functional_outcome='模拟报告PCA受体复合物稳定性。',observation_endpoint='complex trajectory stability',effect_context='不将分子动力学替代受体功能或结合实验。',source_figure_or_table='Figure 6',source_locator='Methods 2.8.5; Results 3.5; Figure 6',source_result_paraphrase_CN='味觉受体关系仅预测，不据此推导抗氧化机制。',target_experimental_support='NO_FOR_THIS_OBSERVATION',direct_target_status='PREDICTED_ONLY')
add('37025617',1,target_gene='Nos3',target_protein='eNOS',target_species='Mus musculus',target_role='MEASURED_PHOSPHORYLATION_READOUT',target_effect_direction='INCREASED_PHOSPHORYLATION',pathway_name='Akt/eNOS signaling',pathway_effect_direction='INCREASED_PHOSPHORYLATION_RESPONSE',experimental_model='IN_VITRO',species='Mus musculus',cell_line_or_tissue='mBMEC',dose='100',dose_unit='nM',treatment_duration='overnight; exact hours NOT_REPORTED',challenge_agent='IL-1β',challenge_dose='0.5 ng/mL',challenge_duration='overnight',assay_method='western blot p-eNOS Ser1177/eNOS',control_group='IL-1β without PCA; untreated cells',evidence_relation_type='PATHWAY_MODULATION',target_validation_status='PHOSPHORYLATION_CHANGE_ONLY',functional_outcome='eNOS磷酸化比值上升。',observation_endpoint='p-eNOS/eNOS ratio',effect_context='原论文标题的directly指直接孵育，不是直接蛋白结合。',source_figure_or_table='Figure 4B,D',source_locator='Methods 2.4,2.7; Figure 4B,D',source_result_paraphrase_CN='保留磷酸化响应，不当作结合靶点。')
add('37025617',2,target_gene='UNRESOLVED',target_protein='Akt family; isoform unresolved',target_species='Mus musculus',target_role='PHARMACOLOGICALLY_IMPLICATED_MEDIATOR',target_effect_direction='DEPENDENCE_SUPPORTED',pathway_name='Akt/eNOS signaling',pathway_effect_direction='PCA_RESPONSE_ATTENUATED_BY_INHIBITOR',experimental_model='IN_VITRO',species='Mus musculus',cell_line_or_tissue='mBMEC',dose='100',dose_unit='nM',treatment_duration='overnight; exact hours NOT_REPORTED',challenge_agent='IL-1β with Akt inhibitor IV',challenge_dose='IL-1β 0.5 ng/mL; Akt inhibitor IV 1 µM',challenge_duration='overnight',assay_method='Akt inhibitor IV; western blot p-eNOS/eNOS',control_group='IL-1β+PCA without Akt inhibitor',evidence_relation_type='FUNCTIONAL_CAUSAL',target_validation_status='PHARMACOLOGICAL_SUPPORT_NOT_GENETIC_NECESSITY',functional_outcome='Akt抑制剂减弱PCA的eNOS磷酸化响应。',observation_endpoint='p-eNOS/eNOS response with inhibitor',effect_context='抑制剂支持功能参与但存在特异性限制；不自动映射AKT1。',source_figure_or_table='Figure 5B',source_locator='Methods 2.4; Figure 5B',source_result_paraphrase_CN='药理参与证据与直接结合分开。')
add('42413844',1,target_gene='TRAF2',target_protein='TRAF2 TRAF domain',target_species='UNRESOLVED',target_role='ABSTRACT_REPORTED_BINDING_TARGET',target_effect_direction='BINDING_REPORTED',experimental_model='CELL_FREE',species='NOT_APPLICABLE',cell_line_or_tissue='TRAF2 protein/domain preparation; species unresolved',dose='UNRESOLVED',dose_unit='UNRESOLVED',treatment_duration='UNRESOLVED',assay_method='fluorescence spectroscopy and calorimetry; abstract-level methods',control_group='UNRESOLVED',evidence_relation_type='DIRECT_BINDING',target_validation_status='ABSTRACT_REPORTED_BINDING_NOT_FULL_TEXT_VERIFIED',functional_outcome='摘要报告PCA与TRAF2结构域直接相互作用。',observation_endpoint='reported biophysical interaction',effect_context='仅摘要；蛋白构建物、剂量和对照未核实。',source_result_paraphrase_CN='保留直接结合报告类别，但不标全文验证。',direct_target_status='REPORTED_ABSTRACT_ONLY',evidence_status='HOLD_FULL_TEXT_REVIEW')
add('42413844',2,target_gene='TRAF2',target_protein='TRAF2',target_species='Homo sapiens',target_role='ABSTRACT_REPORTED_FUNCTIONAL_MEDIATOR',target_effect_direction='DEPENDENCE_REPORTED',pathway_name='TRAF2-associated c-Myc survival signaling',pathway_effect_direction='CELL_SURVIVAL_INCREASE_REPORTED',experimental_model='IN_VITRO',species='Homo sapiens',cell_line_or_tissue='HAP1 leukemia cells',dose='UNRESOLVED',dose_unit='µM',treatment_duration='UNRESOLVED',assay_method='functional analyses; exact perturbation not established from abstract',control_group='UNRESOLVED',evidence_relation_type='FUNCTIONAL_CAUSAL',target_validation_status='ABSTRACT_REPORTED_DEPENDENCE_ONLY',functional_outcome='摘要报告低微摩尔PCA提高细胞活力且与TRAF2有关。',observation_endpoint='HAP1 viability',effect_context='白血病细胞存活增加不应自动描述为健康获益；剂量仅定性范围。',source_result_paraphrase_CN='因果参与为摘要报告，未认定具体敲除或救援设计。',evidence_status='HOLD_FULL_TEXT_REVIEW')
add('32007785',1,target_gene='Sirt1',target_protein='SIRT1',target_species='Mus musculus',target_role='ABSTRACT_REPORTED_PATHWAY_MEDIATOR',target_effect_direction='UNRESOLVED',pathway_name='SIRT1/NF-κB signaling',pathway_effect_direction='INFLAMMATORY_RESPONSE_SUPPRESSION_REPORTED',experimental_model='IN_VITRO',species='Mus musculus',cell_line_or_tissue='BV2 microglia',dose='UNRESOLVED',dose_unit='UNRESOLVED',treatment_duration='UNRESOLVED',challenge_agent='LPS',challenge_dose='UNRESOLVED',challenge_duration='UNRESOLVED',assay_method='UNRESOLVED_ABSTRACT_ONLY',control_group='UNRESOLVED',evidence_relation_type='PATHWAY_MODULATION',target_validation_status='ABSTRACT_PATHWAY_ASSOCIATION_ONLY',functional_outcome='摘要报告炎症介质释放减少并涉及SIRT1/NF-κB。',observation_endpoint='BV2 inflammatory mediator release',effect_context='未将下游PC12模型压入本条；精确蛋白方向及基因干预未核实。',source_result_paraphrase_CN='仅摘要关系；不推断直接结合。')
add('11023549',1,target_gene='Tyr',target_protein='Tyrosinase',target_species='Mus musculus',target_role='PHARMACOLOGICALLY_IMPLICATED_BIOACTIVATION_MEDIATOR',target_effect_direction='DEPENDENCE_SUPPORTED',pathway_name='tyrosinase-associated PCA bioactivation and oxidative stress',pathway_effect_direction='PRO_OXIDATIVE_RESPONSE',experimental_model='IN_VIVO',species='Mus musculus',cell_line_or_tissue='female ICR mouse skin',dose='20000',dose_unit='nmol topical dose',treatment_duration='3 h',administration_route='TOPICAL',assay_method='skin glutathione measurement; arbutin pharmacological comparison',control_group='PCA alone versus PCA with arbutin; exact arbutin dose UNRESOLVED',evidence_relation_type='FUNCTIONAL_CAUSAL',target_validation_status='ABSTRACT_PHARMACOLOGICAL_SUPPORT_ONLY',functional_outcome='高剂量PCA降低皮肤GSH；arbutin对抗此反应。',observation_endpoint='skin glutathione',effect_context='促氧化情境；不能外推正常膳食剂量或人体效应。',source_result_paraphrase_CN='保留毒性与生物活化信号；不证明TYR直接结合。')
for serial,dose,unit,duration,route,tissue in [(1,'500','mg/kg','NOT_REPORTED','INTRAPERITONEAL','ICR mouse liver'),(2,'0.1','% drinking-water concentration','60 days','DRINKING_WATER','ICR mouse kidney')]:
 add('11714376',serial,pathway_name='glutathione redox homeostasis',pathway_effect_direction='GLUTATHIONE_DEPLETION',experimental_model='IN_VIVO',species='Mus musculus',cell_line_or_tissue=tissue,dose=dose,dose_unit=unit,treatment_duration=duration,administration_route=route,assay_method='tissue glutathione measurement; detailed assay unresolved',control_group='UNRESOLVED_ABSTRACT_ONLY',evidence_relation_type='PATHWAY_MODULATION',target_validation_status='NOT_APPLICABLE_PATHWAY_ONLY',functional_outcome='组织GSH降低。',observation_endpoint=tissue+' GSH',effect_context='高剂量/亚慢性暴露；剂量与模型分行；GSH为代谢物，不填作蛋白靶点。',source_result_paraphrase_CN='保留促氧化方向；全文剂量设计待审。',target_experimental_support='NOT_APPLICABLE')

# Screened publication registry. Every other discovery record remains explicitly unreviewed.
decisions={p:('INCLUDE_PILOT_PROVISIONAL','优先覆盖证据类型与情境；非穷尽提取') for p in included}
decisions.update({'26180584':('EXCLUDE_RETRACTED','PubMed RetractionIn PMID41947015；不纳入有效证据'),'41947015':('EXCLUDE_RETRACTION_NOTICE','撤稿通知，不是独立原始实验'),'14705020':('HOLD_FORM_ORIGIN_REVIEW','摘要称PCA为quercetin在LOX内的降解产物；不自动作为给予母体PCA的实验'),'37117448':('BACKGROUND_METHODS_ONLY','未来网络医学背景；不运行算法，不作为本试点原儿茶酸机制实验'),'29129792':('EXCLUDE_DERIVATIVE','研究对象为原儿茶酸乙酯；不自动映射AFF-0061母体')})
registry=[]
for pmid,(decision,reason) in decisions.items():
 if pmid in pub:s=pub[pmid].copy()
 else:
  r=epmid[pmid];s={k:'NOT_RETRIEVED' for k in next(iter(pub.values()))};s.update(study_id='ST-PMID-'+pmid,PMID=pmid,DOI=r.get('doi','NOT_REPORTED'),PMCID=r.get('pmcid','NOT_AVAILABLE'),article_title=r['title'],journal=r.get('journalInfo',{}).get('journal',{}).get('title','NOT_REPORTED'),article_url='https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/')
 s.update(screening_decision=decision,screening_reason_CN=reason,evidence_record_count=sum(r['PMID']==pmid for r in evidence),source_review_status='FULL_TEXT_VERIFIED' if pmid in full else 'ABSTRACT_ONLY' if pmid in included else 'METADATA_OR_ABSTRACT_SCREEN_ONLY',human_review_status='NOT_REVIEWED');registry.append(s)

cluster={};pmidkey={}
for r in ep:
 key='PMID:'+r['id'] if r['source']=='MED' else 'DOI:'+r['doi'].lower().strip() if r.get('doi') else r['source']+':'+r['id']
 if r.get('doi'):
  for existing,v in cluster.items():
   if v['DOI'] and v['DOI']==r['doi'].lower().strip():key=existing;break
 v=cluster.setdefault(key,dict(discovery_record_id=key,PMID=r['id'] if r['source']=='MED' else '',DOI=r.get('doi','').lower().strip(),article_title=r.get('title',''),source_identifiers=[],search_source_ids=['EPMC01'],source_abstract_available='YES' if r.get('abstractText') else 'NO'))
 v['source_identifiers'].append(r['source']+':'+r['id'])
 if r['source']=='MED':v['PMID']=r['id'];pmidkey[r['id']]=key
focusids={x['source']+':'+x['id'] for x in focus}
pmids=readjson(RAW/'PUBMED01_esearch.json')['esearchresult']['idlist']
for pmid in pmids:
 if pmid not in pmidkey:
  key='PMID:'+pmid;cluster[key]=dict(discovery_record_id=key,PMID=pmid,DOI='',article_title='',source_identifiers=['PUBMED:'+pmid],search_source_ids=['PUBMED01'],source_abstract_available='NOT_RETRIEVED')
 else:cluster[pmidkey[pmid]]['search_source_ids'].append('PUBMED01')
for v in cluster.values():
 if set(v['source_identifiers'])&focusids:v['search_source_ids'].append('EPMC02')
 decision,reason=decisions.get(v['PMID'],('NOT_SCREENED','未完成个体筛选；不等同排除或零机制证据'))
 v.update(screening_decision=decision,reason_CN=reason,extraction_status='EXTRACTED_SELECTED_OBSERVATIONS' if v['PMID'] in included else 'NOT_EXTRACTED',full_text_status='FULL_TEXT_VERIFIED' if v['PMID'] in full else 'ABSTRACT_ONLY' if v['PMID'] in included else 'NOT_ASSESSED',human_review_status='NOT_REVIEWED')
 v['source_identifiers']=j(v['source_identifiers']);v['search_source_ids']=j(v['search_source_ids'])
screen=list(cluster.values())

# Complete bilingual operational dictionary; these are NEW pilot definitions, not amendments to T002.
definitions={
'candidate_id':('候选物稳定主键；仅链接T002，不改源表。','Stable T002 candidate key; never rewrites source identity.'),
'compound_name':('T002的候选显示名，不作为合并键。','T002 display name, not an entity-merging key.'),
'compound_form':('本观察的化学形式类别；衍生物必须独立判定。','Chemical-form class used in this observation; derivatives require separate decisions.'),
'PubChem_CID':('关联母体的参考CID；不声称实验样品已测定或作者报告该CID。','Reference-parent CID, not proof of experimental sample characterization.'),
'InChIKey':('参考母体完整结构键；不代替实验试剂鉴定。','Full reference-parent InChIKey, not experimental reagent authentication.'),
'study_id':('按原始出版物分配的稳定标识；不是跨论文实验独立性保证。','Stable original-publication identifier, not proof of independent cohorts.'),
'article_title':('原始文献题名，来自出版物级元数据。','Original article title from publication-level metadata.'),
'DOI':('出版物DOI；从文章本身ID列表提取，不取参考文献DOI。','Article DOI from its own identifier list, never a cited-reference DOI.'),
'PMID':('原始文章PubMed标识，文本保存。','PubMed article identifier stored as text.'),
'journal':('原文期刊全名。','Source journal title.'),
'publication_date':('明确记录的发表日期；保留年/月精度，不补造日期。','Explicit publication date, preserving incomplete precision without imputation.'),
'publication_date_type':('日期事件类型，区分电子发表与卷期日期。','Date event: electronic publication versus journal issue.'),
'article_url':('文章可访问入口，不保证全文开放。','Article landing URL, not a guarantee of full-text availability.'),
'target_gene':('本观察对应单个基因的物种特异符号；蛋白家族不推断基因。','One species-specific gene symbol; family measurements do not imply an isoform.'),
'target_protein':('原文蛋白或家族名；不是自动验证的药物结合靶点。','Reported protein or family label, not automatically a binding target.'),
'UniProt_ID':('单一基因及物种一致的参考蛋白accession；不证实试剂或因果。','Reference accession matched to gene and species, not assay or causal validation.'),
'target_species':('被研究蛋白的物种；重组蛋白不从细胞模型推定物种。','Protein species; never infer recombinant species from a cell model.'),
'target_role':('蛋白在该观察中的角色，区分读数、介导与结合预测。','Observation-specific role: readout, mediator, or predicted binding target.'),
'target_effect_direction':('相对指定对照的单一作用方向或依赖关系；非统计效应量。','Single comparator-relative response or dependency, not an effect size.'),
'pathway_name':('单个作者命名通路轴或生物过程；不冒充标准通路实体。','One author-named axis or process, not necessarily an ontology pathway.'),
'pathway_ID':('经独立核对的标准通路ID；未映射保留UNRESOLVED。','Independently checked pathway identifier; unresolved if unmapped.'),
'pathway_database':('通路ID的数据库；作者命名轴用专门标记。','Pathway identifier authority, or explicit author-axis marker.'),
'pathway_effect_direction':('特定模型和对照中的通路响应；富集不自动解释为激活。','Model-specific pathway response; enrichment does not imply activation.'),
'experimental_model':('本行单一实验或计算环境类别。','One experimental or computational model category per row.'),
'species':('实验模型生物物种，与target_species分列。','Organism of the experimental model, separate from target species.'),
'cell_line_or_tissue':('单一细胞系、组织或蛋白制备及必要基因型。','One cell line, tissue, or protein preparation with relevant genotype.'),
'dose':('单个剂量值；不把多个独立剂量拼入一行。','Single dose value; separate independently resolved doses into separate rows.'),
'dose_unit':('原始单位及浓度基准，区分注射器浓度和最终暴露。','Source unit and concentration basis, including syringe versus final exposure.'),
'treatment_duration':('PCA干预时长及单位；未明确小时的overnight原样保留。','PCA exposure duration; preserve overnight without inventing hours.'),
'assay_method':('实际支持该观察的方法；摘要未说明则不推断。','Method supporting this observation; do not infer unspecified abstract methods.'),
'control_group':('与本观察对应的对照与比较；未核实保持未解决。','Observation-specific comparator and controls, unresolved if unverified.'),
'evidence_id':('唯一稳定观察标识；同论文不同观察分配不同后缀。','Unique stable observation identifier within a linked publication.'),
'evidence_relation_type':('证据关系类别，不是质量分或直接靶点批准。','Evidence relationship class, not a quality score or target approval.'),
'target_validation_status':('本行实验支持程度；区分必要性、药理支持、表达、组学、预测。','Row-specific support: dependency, pharmacology, expression, omics, or prediction.'),
'functional_outcome':('本行单一主要观察结果；保留阴性和促氧化结局。','One principal observation outcome, retaining negative and pro-oxidant results.'),
'effect_context':('剂量、疾病、时序及解释边界；不代替结果。','Disease, exposure timing, and interpretation context, separate from outcomes.'),
'source_figure_or_table':('支持观察的原始图表及面板；摘要不能虚构图号。','Original figure/table and panel; never invent locators for abstract-only records.'),
'source_verification_status':('已核查的来源层级；全文文本核查不等于图像完整性审计。','Verified source level; full-text reading is not image-integrity review.'),
'evidence_status':('试点记录纳入/待审状态，不表示人工批准。','Pilot inclusion/hold state, never human approval.'),
'notes':('必要补充与未解决信息，不承载隐藏的批准决定。','Supplementary notes and unresolved details, not hidden approval decisions.'),
'PMCID':('文章的PMC标识；不是全文核查已完成标记。','PMC article identifier, not proof of completed full-text verification.'),
'publication_date_precision':('发表日期实际可支持的粒度。','Actual supported publication-date precision.'),
'compound_form_as_reported':('作者使用的化学形式名称，不替换成参考结构名。','Chemical-form wording used by the authors, not overwritten by reference names.'),
'identity_mapping_status':('实验物质与参考母体的关联核查层级。','Level of linkage between experimental substance and reference parent.'),
'identity_reference_url':('母体身份公共参考来源。','Public reference source for parent chemical identity.'),
'experiment_id':('具体实验/比较标识；共用材料可有不同检测，不计成独立研究。','Experiment/comparison identifier; linked assays are not independent studies.'),
'observation_endpoint':('本行单一主要读数，便于识别重复实验。','One principal endpoint used for observation deduplication.'),
'administration_route':('PCA给药途径；无报告不得由同类实验推断。','PCA administration route; never infer from similar experiments.'),
'pretreatment_duration':('PCA预处理时长，与后续挑战分开。','PCA pretreatment interval, separate from subsequent challenges.'),
'challenge_agent':('本模型的刺激物或明确遗传/药理干预。','Challenge stimulus or explicit genetic/pharmacological perturbation.'),
'challenge_dose':('刺激物剂量；不同刺激物清晰命名，不替代PCA剂量。','Named challenge doses, separate from the PCA dose.'),
'challenge_duration':('刺激/基因干预的时序，不与PCA时长混为一谈。','Challenge/perturbation timeline, distinct from PCA duration.'),
'target_experimental_support':('该观察是否有实验支持及来源层级；不跨行升级预测。','Observation-level experimental support and source depth; never promote predictions across rows.'),
'direct_target_status':('直接结合认定层级，与功能参与独立。','Direct-binding determination level, independent of functional mediation.'),
'target_identifier_status':('基因/物种到蛋白标识的映射状态；不是实验验证。','Gene/species-to-accession mapping state, not experimental validation.'),
'target_identifier_source':('蛋白标识查询的保存来源。','Retained source for protein identifier lookup.'),
'source_local_path':('本试点目录内保存的原始文本/元数据相对路径。','Pilot-relative path to retained source text or metadata.'),
'source_locator':('方法、结果小节与图表定位的联合指针。','Combined methods/results section and figure/table locator.'),
'source_result_paraphrase_CN':('基于实际阅读的简短中文释义，不是作者逐字引文。','Short Chinese source-based paraphrase, not a verbatim quotation.'),
'source_review_mode':('说明核查正文/图注还是仅摘要；不假称逐图检查。','Specifies text/legend versus abstract review without claiming image verification.'),
'search_source_ids':('与检索日志对应的检索标识列表。','Search-log identifiers supporting discovery.'),
'extraction_date':('本轮提取日期ISO格式。','ISO extraction date.'),
'extracted_by':('自动/辅助提取者，不写成人工审稿人。','Extractor identity, not a human scientific reviewer.'),
'human_review_status':('独立人工科学审查状态，本版未审核。','Independent human scientific review state; unreviewed in this version.'),
'publication_status':('检索时元数据中的撤稿关联状态；无标记不是绝对无问题。','Retraction-link status at retrieval; no flag is not a guarantee of validity.'),
'experiment_independence_status':('同论文关联及跨论文实验复用的核实状态。','Within-publication linkage and cross-publication experiment-reuse assessment.')}
assert set(fields)==set(definitions)
enums={f:sorted({r[f] for r in evidence}) for f in ['compound_form','publication_date_type','publication_date_precision','target_role','target_effect_direction','experimental_model','evidence_relation_type','target_validation_status','source_verification_status','evidence_status','target_experimental_support','direct_target_status','human_review_status','publication_status']}
enums['evidence_relation_type']=['DIRECT_BINDING','FUNCTIONAL_CAUSAL','PATHWAY_MODULATION','OMICS_ASSOCIATION','COMPUTATIONAL_PREDICTION']
dictionary=[]
for order,f in enumerate(fields,1):
 cn,en=definitions[f]
 rule=j(enums[f]) if f in enums else 'OPEN_TEXT_SINGLE_VALUE; identifiers require source verification; units preserve source basis'
 if f in ['dose']:rule='single numeric text OR UNRESOLVED OR NOT_REPORTED OR NOT_APPLICABLE; no inferred conversion'
 dictionary.append(dict(field_order=order,field_name=f,definition_cn=cn,definition_en=en,data_type='numeric_text_or_explicit_missing_marker' if f=='dose' else 'string',allowed_values_or_rule=rule,missing_value_rule_cn='NOT_REPORTED=已读来源未报告；UNRESOLVED=无法核实；NOT_APPLICABLE=不适用；NOT_AVAILABLE=无该公共标识；不得填0或以空白替代。',missing_value_rule_en='Distinguish not reported, unresolved, not applicable and unavailable; never impute zero or conflate states.',filling_instruction_cn=cn+' 仅写本行可溯源内容；不得外推其他模型、剂量或直接靶点。',required_rule='FIELD_REQUIRED; explicit missing marker allowed except stable keys and article identity',unit_rule='dose_unit specifies source unit' if f=='dose' else 'not a numeric measurement unless specified in definition',definition_status='PILOT_OPERATIONAL_DRAFT_NOT_HUMAN_APPROVED',version='v0.1'))

# Quality controls are executable checks, not approval of scientific interpretations.
checks=[]
def check(name,ok,detail):
 checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail_CN':detail})
check('schema_and_dictionary',set(fields)==set(definitions) and all(set(r)==set(fields) for r in evidence),'全部必需字段和扩展字段均有中英文定义、允许规则、缺失规则及填写说明。')
check('unique_evidence_id',len({r['evidence_id'] for r in evidence})==len(evidence),'观察ID唯一。')
fingerprints=[tuple(r[f] for f in ['PMID','experimental_model','cell_line_or_tissue','dose','treatment_duration','target_protein','observation_endpoint','evidence_relation_type']) for r in evidence]
check('duplicate_observation_fingerprint',len(set(fingerprints))==len(fingerprints),'按论文/模型/剂量/时长/对象/主要读数/关系检查重复；跨论文实验复用仍待审。')
check('candidate_identity',all(r['candidate_id']=='AFF-0061' and r['PubChem_CID']=='72' and r['InChIKey']==ref['InChIKey'] for r in evidence),'母体参考身份一致；不表示每篇试剂结构被独立复测。')
check('publication_identity',all(r['DOI']==pub[r['PMID']]['DOI'] for r in evidence),'文章自身ID列表核对，未误用参考文献DOI。')
check('retracted_excluded',all(r['PMID'] not in ['26180584','41947015'] for r in evidence),'已撤稿研究及通知仅保留筛选/来源记录。')
check('prediction_not_experimental_binding',all(r['direct_target_status']=='PREDICTED_ONLY' and r['target_experimental_support']=='NO_FOR_THIS_OBSERVATION' for r in evidence if r['evidence_relation_type']=='COMPUTATIONAL_PREDICTION'),'同论文有其他实验也不将对接记录升级。')
check('abstract_not_figure_verified',all(r['source_figure_or_table']=='UNRESOLVED_ABSTRACT_ONLY' and r['source_review_mode']=='PUBMED_ABSTRACT_TEXT_ONLY' for r in evidence if r['source_verification_status']=='ABSTRACT_ONLY'),'摘要行无虚构Figure/Table。')
check('source_files_exist',all((OUT/r['source_local_path']).exists() for r in evidence),'所有观察有实际保存的来源文件。')
check('one_compound_only',{r['candidate_id'] for r in evidence}=={'AFF-0061'},'没有虚构其他190条候选物证据。')
check('all_fields_explicit',all(all(v!='' and v is not None for v in r.values()) for r in evidence),'缺失使用明确状态标记，不以0替代。')
check('no_human_approval',all(r['human_review_status']=='NOT_REVIEWED' for r in evidence),'未宣布人工科学审核通过。')
check('no_gene_for_GSH',all(r['target_gene']=='NOT_APPLICABLE' for r in evidence if r['PMID']=='11714376'),'GSH是代谢物，不写入蛋白基因栏。')
check('dose_atomic',all(not re.search(r'\d\s*[-–]\s*\d|\d[,;]\s*\d',r['dose']) for r in evidence),'PCA剂量不拼接不同模型或多个定量剂量。')

exp_rows=[r for r in evidence if r['source_verification_status']=='FULL_TEXT_VERIFIED' and r['target_experimental_support']=='YES_FULL_TEXT' and r['target_gene'] not in ['NOT_APPLICABLE','UNRESOLVED']]
exp_targets=sorted({(r['target_gene'],r['target_species']) for r in exp_rows})
pred=[r for r in evidence if r['evidence_relation_type']=='COMPUTATIONAL_PREDICTION']
predonly=sorted({r['target_gene'] for r in pred if r['target_gene'] not in {x[0].upper() for x in exp_targets} and r['target_gene'].upper() not in {x[0].upper() for x in exp_targets}})
counts={'included_unique_publications':len(included),'cross_publication_experiment_independence':'NOT_FULLY_VERIFIED','evidence_records':len(evidence),'fields':len(fields),'full_text_verified_publications':len(full),'abstract_only_publications':len(included)-len(full),'full_text_verified_observations':sum(r['source_verification_status']=='FULL_TEXT_VERIFIED' for r in evidence),'abstract_only_observations':sum(r['source_verification_status']=='ABSTRACT_ONLY' for r in evidence),'evidence_relation_counts':dict(Counter(r['evidence_relation_type'] for r in evidence)),'experimentally_supported_species_specific_gene_count_fulltext':len(exp_targets),'experimentally_supported_species_specific_genes_fulltext':exp_targets,'experimentally_supported_definition':'FULL_TEXT; YES_FULL_TEXT; resolved gene and species; includes readouts, not only causal/direct targets','predicted_only_named_genes':predonly,'predicted_only_gene_count':len(predonly),'prediction_observations':len(pred),'pathway_linked_observation_count':sum(r['pathway_name']!='NOT_APPLICABLE' for r in evidence),'distinct_author_named_axes_or_processes':len({r['pathway_name'] for r in evidence if r['pathway_name']!='NOT_APPLICABLE'}),'pathway_ontology_IDs_verified':0,'fulltext_verified_specific_direct_binding_targets':0,'direct_binding_report_observations':sum(r['evidence_relation_type']=='DIRECT_BINDING' for r in evidence),'EPMC01_hits':3809,'EPMC02_hits':514,'PUBMED01_hits':len(pmids),'discovery_records_deduplicated':len(screen),'screened_publications_in_discovery':sum(r['screening_decision']!='NOT_SCREENED' for r in screen),'not_screened_discovery_records':sum(r['screening_decision']=='NOT_SCREENED' for r in screen),'screening_decision_counts':dict(Counter(r['screening_decision'] for r in screen)),'QC_passes':sum(r['status']=='PASS' for r in checks),'QC_failures':sum(r['status']=='FAIL' for r in checks)}
coverage=[]
for r in t002:
 ispilot=r['candidate_id']=='AFF-0061'
 coverage.append(dict(candidate_id=r['candidate_id'],compound_name=r['canonical_name'],PubChem_CID=r['PubChem_CID'],InChIKey=r['InChIKey'],search_status='SEARCHED_PILOT_SCREENING_PARTIAL' if ispilot else 'NOT_SEARCHED',screening_status='PARTIAL_PRIORITY_SAMPLE' if ispilot else 'NOT_SEARCHED',extraction_status='PILOT_SELECTED_OBSERVATIONS' if ispilot else 'NOT_SEARCHED',included_unique_publication_count=len(included) if ispilot else '',evidence_record_count=len(evidence) if ispilot else '',evidence_count_status='OBSERVED_IN_PILOT_NOT_TOTAL_LITERATURE' if ispilot else 'NOT_ASSESSED_NOT_ZERO',human_review_status='NOT_REVIEWED',release_status='HOLD'))
check('coverage_index',len(coverage)==191 and sum(r['search_status']=='NOT_SEARCHED' for r in coverage)==190 and all(r['evidence_record_count']=='' for r in coverage if r['search_status']=='NOT_SEARCHED'),'190个未检索者不填虚假零证据；空计数字段由明确状态解释。')
changed=[p for p,h in baseline['tracked_file_sha256'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
check('protected_tracked_files_unchanged',not changed,'源表、字典、冻结资产、矩阵、Phase1B及其他既有跟踪文件SHA256比对。')
check('HEAD_unchanged',git('rev-parse','HEAD')==baseline['HEAD'],'未commit/push。')
counts['QC_passes']=sum(r['status']=='PASS' for r in checks);counts['QC_failures']=sum(r['status']=='FAIL' for r in checks)
assert not any(r['status']=='FAIL' for r in checks),checks
csvout('compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv',evidence)
csvout('master/Compound_Mechanism_Evidence_Master.csv',evidence)
csvout('indexes/Compound_Mechanism_Coverage.csv',coverage)
csvout('dictionaries/Mechanism_Evidence_Field_Dictionary.csv',dictionary)
csvout('master/Study_Register.csv',registry)
csvout('search_logs/Protocatechuic_Acid_Screening_Log.csv',screen)
csvout('qc/Programmatic_Checks.csv',checks)
logs=readjson(RAW/'Retrieval_Logs.json')+readjson(RAW/'Retrieval_Logs_Retry.json')+readjson(RAW/'PubMed_Targeted_Logs.json')
searchlog=[]
for k,r in enumerate(logs,1):
 searchlog.append(dict(log_event_id='SL-'+str(k).zfill(3),search_id=r['search_id'],database=r['database'],candidate_id=r.get('candidate_id','AFF-0061'),search_date_utc=r.get('search_date_utc',baseline['utc']),date_note='exact query timestamp retained where available; otherwise task retrieval session timestamp',query=r.get('query',''),status=r['status'],hit_count=r.get('hit_count',''),retrieved_count=r.get('retrieved_count',''),api_urls=j(r.get('api_urls',[])),error=r.get('error',''),screening_scope='priority-selected pilot only; complete decisions in screening log',included_publication_count='SEE Study_Register; do not sum overlapping queries',full_text_scope='6 included full texts; 4 abstract-only',retrieval_limitation='first EPMC attempt invalid sort returned503; corrected query succeeded; retained failed event'))
csvout('search_logs/Protocatechuic_Acid_Search_Log.csv',searchlog)
write('qc/Counts_and_Checks.json',{'counts':counts,'checks':checks,'protected_changed_paths':changed,'head':git('rev-parse','HEAD')})
write('qc/Compound_Identity_Check.json',{'source_table':'data/candidate_universe/Antioxidant_Class_Candidate_Master.csv','data_record':61,'physical_line':62,'actual_source_record':compound,'external_reference':ref,'source_URL':readjson(RAW/'PubChem_CID72.json')['url'],'reference_identifier_status':'CONSISTENT_NOT_HUMAN_APPROVED','experimental_form_status':'AUTHOR_REPORTED_PARENT_LINK; SALTS_ESTERS_GLYCOSIDES_CONJUGATES_NOT_AUTOMATICALLY_EQUIVALENT','phase1b_status_preserved':'IDENTIFIER_PRESENT_NOT_STRUCTURALLY_RECHECKED; mapping MATCH_PROVISIONAL; HOLDs unchanged'})
assert (OUT/'master/Compound_Mechanism_Evidence_Master.csv').read_bytes()==(OUT/'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv').read_bytes()
write('qc/Final_Integrity.json',{'start_HEAD':baseline['HEAD'],'end_HEAD':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'tracked_files_checked':len(baseline['tracked_file_sha256']),'protected_changed_paths':changed,'worktree_status_before_final_report_files':git('status','--short'),'original_data_modified':'NO','frozen_assets_modified':'NO','commit_push':'NOT_EXECUTED','scope':'SHA256 of all preexisting tracked files; untracked additions restricted to pilot directory'})

boundary='''所有记录为试点待审数据，不是人工批准的药物靶点目录。参考母体身份与每篇实验试剂鉴定分列，未改T002、T004、T110、既有字典、身份审核、临时映射、157×5矩阵或Frozen Top20。Phase1B的26/7/2、AFF-0082/AFF-0150缺失、155临时映射/2待审、21项字典缺口及Crosswalk/Phase2/Release HOLD均保持。

FULL_TEXT_VERIFIED表示已读正文方法、结果及相关图注/表注，不表示已独立逐像素核查图像、原始数据或补充材料；本版未做原始图像完整性审计。ABSTRACT_ONLY不填写推测剂量、对照、时长或Figure编号。需要具体剂量却尚未读出时保留UNRESOLVED，不填0。'''
summary=f'''原儿茶酸试点关联T002第61条（文件第62行）：CID72、YQUVCSBJEUQKSH-UHFFFAOYSA-N、C7H6O4与PubChem公共接口一致；这是参考标识核对，不是人工样品结构审核。未发现阻止参考母体关联的重大冲突。

检索截止2026-10-16。Europe PMC广义检索3809条，机制优先514条；PubMed广义检索3322条（保存全部PMID）。不同数据库/查询重叠，不相加。按PMID及DOI诊断去重后保留{len(screen)}条发现记录，实际审阅决策{counts['screened_publications_in_discovery']}条，未筛{counts['not_screened_discovery_records']}条。PubMed-only记录中部分只保留ID，未假称已读摘要。检索式、实际响应、失败503及修复后响应均保留。本轮是系统化检索后的优先样本试点，不是完成全部原儿茶酸文献的系统综述。筛选与逐实验提取均为PARTIAL。

纳入{len(included)}篇按DOI/PMID去重的原始研究，{len(evidence)}条观察，{len(fields)}字段；其中全文文本核查6篇/{counts['full_text_verified_observations']}条，摘要4篇/{counts['abstract_only_observations']}条。独立出版物数10不代表已证明跨论文样本或实验完全独立。关系分布：{j(counts['evidence_relation_counts'])}。实验支持的可物种定位基因/蛋白共{len(exp_targets)}个（{j(exp_targets)}），此口径包含表达/磷酸化读数，不等于直接靶点；组学单独列出，家族/物种未解决不强制映射。仅预测的命名基因{len(predonly)}个：{j(predonly)}。通路关联观察{counts['pathway_linked_observation_count']}条，作者命名轴/过程{counts['distinct_author_named_axes_or_processes']}类，标准通路ID核实0个，均不冒填KEGG/Reactome编号。

直接结合类别2条，但本版可确认的“全文核查且具体蛋白身份明确”的直接结合靶点为0：TRAF2论文只核查摘要，重组蛋白物种/剂量/对照待查；α-amylase ITC方法与Figure2B图注存在制备对象冲突，且物种/亚型未明确，保留HOLD。TAS2R16仅模拟；SIRT3和HDAC1的对接不能升级为实验结合。SIRT3、NRF2敲除支持模型内功能参与；Akt抑制剂支持药理参与但不能指定AKT1；HDAC1平行表型及非加和不等同必要性或救援。促氧化、高剂量GSH耗竭和无额外显著效应均保留，未筛掉阴性结果。

PMID26180584/DOI10.1155/2015/351827有2026撤稿关联（通知PMID41947015），两者不计有效研究。原儿茶酸乙酯PMID29129792不当作母体；LOX晶体中由quercetin生成PCA的研究PMID14705020暂缓形式/来源审查。Nature Food2021（10.1038/s43016-021-00243-7）仅作未来框架背景，未生成PPI、网络接近度或训练结果。

程序质控{counts['QC_passes']}项通过、{counts['QC_failures']}项失败；主表与单物质表字节一致，evidence_id唯一，191条覆盖索引中仅AFF-0061标为已检索但筛选部分，另190条NOT_SEARCHED且不填零证据。{len(baseline['tracked_file_sha256'])}个既有跟踪文件SHA256未变，开始/结束HEAD为{baseline['HEAD']}，main分支。只新增本工作区，未commit/push。'''
openitems='''未解决事项与人工顺序：先核查TRAF2原始全文、α-amylase方法/图注对象及试剂物种，随后复核遗传与药理因果界限、HDAC1非加和解释、KEAP1未逐浓度提取、旧促氧化研究的全文与对照，再核对蛋白/通路标准标识和所有逐图定位。随后确定原儿茶酸剩余筛选范围及跨研究实验独立性。尚不建议扩大到其他候选物；先完成本试点的Gate 2审查。

Gate 1：HOLD。附件未给出正式Gate 1判据，本轮只确认PROGRAMMATIC_QC=PASS，不替用户定义正式通过门槛；筛选/提取完整性、全文及关键身份问题仍开放。Gate 2：HUMAN_SCIENTIFIC_REVIEW_REQUIRED。Release：HOLD。Phase 2：HOLD。不可把程序通过解释为人工证据批准。'''
priority_files=[('P0','Sync_to_ChatGPT_Mechanism_Evidence_Pilot.md'),('P0','qc/Mechanism_Evidence_Pilot_QC_Report.md'),('P0','compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'),('P0','master/Study_Register.csv'),('P1','master/Compound_Mechanism_Evidence_Master.csv'),('P1','dictionaries/Mechanism_Evidence_Field_Dictionary.csv'),('P1','search_logs/Protocatechuic_Acid_Search_Log.csv'),('P1','search_logs/Protocatechuic_Acid_Screening_Log.csv'),('P1','indexes/Compound_Mechanism_Coverage.csv'),('P2','docs/Mechanism_Evidence_User_Guide_CN.md'),('P2','qc/Counts_and_Checks.json'),('P2','qc/Compound_Identity_Check.json')]
transfer='\n'.join(f'- {p}：`{Path(name).name}`；`workspaces/phase1c_mechanism_evidence_pilot/{name}`' for p,name in priority_files)
write('docs/Mechanism_Evidence_User_Guide_CN.md',f'''# 机制证据数据库试点使用说明 v0.1

{boundary}

一行表示一个候选物×一个明确对象关系×一个具体证据观察。多个模型、剂量或主要方向不得合并；同一论文由study_id链接。experiment_id表示本轮区分的实验/比较，同一动物材料上的不同检测不是独立研究。evidence_id一经分配不重排，后续更正保留ID并增加版本日志。引用源须用文章自身DOI/PMID，不能误取参考文献列表ID。

五类关系是DIRECT_BINDING、FUNCTIONAL_CAUSAL、PATHWAY_MODULATION、OMICS_ASSOCIATION、COMPUTATIONAL_PREDICTION。DIRECT_BINDING表示观察关系类型，还须结合source_verification_status、target_validation_status与direct_target_status判断是否验证。FUNCTIONAL_CAUSAL亦分遗传依赖、药理参与和仅摘要报告。表达变化、通路富集及对接均不证明直接结合；敲除/救援至多支持功能参与。阴性不等同等效性证明。所有定义均为新试点操作性草案，详见完整中英文字典，不修改T002旧字典。

NOT_REPORTED表示已读来源未报告，UNRESOLVED表示信息无法核实或未提取，NOT_APPLICABLE表示不适用，NOT_AVAILABLE表示公共标识不可得；不可混作0。覆盖索引中190个NOT_SEARCHED候选的计数字段留空，状态明确标为NOT_ASSESSED_NOT_ZERO。PubChem_CID/InChIKey为母体参考锚，不冒称每篇作者报告了此标识或实验溶液中的质子化形态。盐、酯、糖苷、结合物与衍生物须另行核实。

UniProt检索可返回同义名命中，程序只选主基因名与物种精确匹配且唯一的条目；这仅为标识映射。不从pan-Akt抗体指定AKT1，不从商业α-amylase指定人AMY1或AMY2，不由细胞物种推定重组构建物。作者轴/生物过程尚未本体映射，pathway_ID保持UNRESOLVED。

药物剂量保持原单位；ITC 12 mmol/L是注射器浓度，不是滴定池最终浓度。overnight不换算成假定小时。不得根据标题directly或作者的结合措辞升级证据。KEAP1多剂量阴性信息尚未逐浓度核实，因此本版不纳入证据行，保留待提取；不能用于剂量反应汇总。

本版纳入文献为优先证据类型样本，不是对全部发现文献的穷尽清单。查阅screening log区分NOT_SCREENED、暂缓、排除和试点纳入。Study_Register按出版物计数，不把同论文多行计为多个研究。全文XML/HTML保存在search_logs/raw供本地追溯；再分发或未来Git提交前应审查各篇许可与必要性，不默认将所有出版物全文作为发布包。所有脚本仅在隔离工作区写入，不执行网络医学算法。

{openitems}
''')
write('qc/Mechanism_Evidence_Pilot_QC_Report.md',f'''# 机制证据试点QC报告 v0.1

{summary}

{boundary}

程序检查明细见Programmatic_Checks.csv。科学开放项：TRAF2全文、amylase制备冲突、部分剂量/对照缺失、蛋白家族与物种未解决、通路ID未映射、跨论文实验复用及独立人工审查均尚未关闭。6篇全文均基于正文和图注文本；未假称逐图原始图像审核。没有因缺失而将摘要关系升级为全文确认。

{openitems}

## 转交清单

{transfer}
''')
write('Sync_to_ChatGPT_Mechanism_Evidence_Pilot.md',f'''# 同步ChatGPT：Phase1C机制证据数据库与原儿茶酸试点 v0.1

已读取Phase1B的T002_ReadOnly_Audit_Report_v0.1.md、Sync_to_ChatGPT_Phase1B_T002_v0.1_CN.md、527行T002_Identity_and_CrossTable_Match_Audit_v0.1.csv及14项T002_Scientific_Risk_Register_v0.1.csv。它们仅是审计结果，不是人工科学批准。

{summary}

{boundary}

{openitems}

## 需要上传/转交的完整相对路径

{transfer}

完成后停止，未向其他聊天自动发送；请用户转交并共同审查。未经本轮新授权不commit/push，不自动进入其他候选物或Phase2。
''')
csvout('docs/Transfer_to_ChatGPT_File_List.csv',[{'priority':p,'filename':Path(n).name,'relative_path':'workspaces/phase1c_mechanism_evidence_pilot/'+n} for p,n in priority_files])
print(json.dumps(counts,ensure_ascii=False,indent=2))
