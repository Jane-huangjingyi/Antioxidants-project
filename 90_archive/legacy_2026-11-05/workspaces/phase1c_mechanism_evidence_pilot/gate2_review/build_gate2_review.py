"""Proposal-only review of the existing 21 observations; never writes original tables."""
from pathlib import Path
import csv,json,hashlib,datetime,subprocess,re,xml.etree.ElementTree as ET
from collections import Counter
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'workspaces/phase1c_mechanism_evidence_pilot';O=P/'gate2_review'
def j(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def load(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f,strict=True);rows=list(reader)
 assert rows and all(None not in r and all(x is not None for x in r.values()) for r in rows)
 return rows
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT).decode('utf-8').strip()
def text(name,v):
 with (O/name).open('x',encoding='utf-8') as f:f.write(v if isinstance(v,str) else j(v))
def csvout(name,rows):
 with (O/name).open('x',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (O/'AFF-0061_Gate2_Evidence_Review_Matrix.csv').exists(),'existing outputs: stop'
base=json.loads((O/'Start_Baseline.json').read_text(encoding='utf-8'))
a=load(P/'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv');master=load(P/'master/Compound_Mechanism_Evidence_Master.csv');dictionary=load(P/'dictionaries/Mechanism_Evidence_Field_Dictionary.csv');studies=load(P/'master/Study_Register.csv')
risk1b=load(ROOT/'workspaces/phase1b_t002_readonly_audit/T002_Scientific_Risk_Register_v0.1.csv');identity1b=load(ROOT/'workspaces/phase1b_t002_readonly_audit/T002_Identity_and_CrossTable_Match_Audit_v0.1.csv')
assert len(a)==21 and len(a[0])==66 and len(dictionary)==66 and a==master
pub={}
for article in ET.parse(O/'sources/Current_10_Study_PubMed.xml').findall('./PubmedArticle'):
 pmid=article.findtext('./MedlineCitation/PMID');ids={x.get('IdType'):x.text for x in article.findall('./PubmedData/ArticleIdList/ArticleId')}
 pub[pmid]={'DOI':ids.get('doi',''),'title':''.join(article.find('./MedlineCitation/Article/ArticleTitle').itertext()),'retraction_links':[x.get('RefType') for x in article.findall('./MedlineCitation/CommentsCorrectionsList/CommentsCorrections') if x.get('RefType') in ['RetractionIn','RetractionOf','ExpressionOfConcernIn']]}
assert len(pub)==10
for r in a:assert r['DOI'].lower()==pub[r['PMID']]['DOI'].lower() and not pub[r['PMID']]['retraction_links'],r['evidence_id']
R={}
def review(pmid,n,confirmation,relevance,reason,**kw):
 eid=f'ME-AFF0061-{pmid}-{n:03d}'
 R[eid]=dict(confirmation=confirmation,relevance=relevance,reason=reason,**kw)
review('32520409',1,'FUNCTIONAL_PARTICIPATION_SUPPORTED','OTHER_BIOLOGICAL_FUNCTION','全身Sirt3缺失下PCA改善肝脂肪变的响应减弱/丧失，支持该模型内功能参与；本行终点为组织脂肪变，不是直接氧化还原测量。',causal='CONTEXT_SPECIFIC_KNOCKOUT_SUPPORT; NOT_DIRECT_BINDING; NO_ROW_LEVEL_REEXPRESSION_RESCUE',rescue='未在本行动物实验中核实Sirt3敲除后的同背景补回救援。论文其他细胞过表达/ACSF3突变不移用于本行。',target='小鼠Sirt3；参考Q8R104；敲除背景与蛋白结合是不同维度。',redox='NONE_MEASURED_IN_THIS_OBSERVATION',further='定量基因型×PCA交互与盲法/全身敲除基线效应需人工审核；给药途径未明确，保持NOT_REPORTED。')
review('32520409',2,'COMPUTATIONAL_ONLY','OTHER_BIOLOGICAL_FUNCTION','PCA–SIRT3仅为对接，不是生物物理结合实验；PDB3GLS的源物种现可核为Homo sapiens。',target='RCSB 3GLS entity1: Homo sapiens/9606，参考UniProt Q9NTG7；E. coli为表达宿主，不是蛋白来源物种。',proposed_species='Homo sapiens',proposed_uniprot='Q9NTG7',redox='NONE_MEASURED',causal='DOCKING_CANNOT_ESTABLISH_BINDING_OR_CAUSALITY',rescue='NOT_APPLICABLE',further='仅建议补足计算模型物种与参考accession；不改原行，不升级验证程度。')
review('37482908',1,'OMICS_ASSOCIATED','OTHER_BIOLOGICAL_FUNCTION','转录组候选Kmo关联可保留；RNA-seq既不是蛋白实测，也不是PCA直接靶点证明。',target='Kmo转录本；参考Q91WN4仅标识映射，不证明蛋白含量或结合。',redox='NONE; Kmo transcript discovery',causal='OMICS_ASSOCIATION_ONLY',rescue='NOT_TESTED_IN_THIS_OBSERVATION',further='应定位Kmo对应差异基因结果及多重校正；不将同论文Figure8的DHE结果写入本行。')
review('37482908',2,'READOUT_ONLY','OTHER_BIOLOGICAL_FUNCTION','Figure5D为Kmo mRNA qPCR，不能计为直接蛋白验证；原分类PATHWAY_MODULATION可按转录响应子类保留。',target='Kmo mRNA，不等于KMO蛋白实测。',redox='NONE; Kmo mRNA',causal='EXPRESSION_RESPONSE_NOT_NECESSITY',rescue='本行未做救援；论文平行Kmo siRNA表型不能替代PCA×Kmo必要性检验。',further='建议增加读数层级transcript/protein标签；与同动物RNA-seq检测保持关联，不重复计独立研究。')
review('39589556',1,'FUNCTIONAL_PARTICIPATION_SUPPORTED','DIRECT_REDOX_OUTCOME','Figure6L直接对应BODIPY脂质过氧化染色；PCA效果在Nrf2缺失背景受限，支持情境性功能参与。',target='小鼠Nfe2l2/NRF2；参考Q60795；全身敲除并非直接结合。',redox='BODIPY lipid-peroxidation signal; qualitative image-level review',secondary='ANTIOXIDANT_FUNCTIONAL_MECHANISM',causal='KNOCKOUT_DEPENDENCE_SUPPORTED_WITH_CONTEXT; NO_DIRECT_BINDING; NO_NUMERIC_IMAGE_REEXTRACTION',rescue='同论文SupplementaryFigure2/pdf第3页存在NRF2缺失细胞补回；已读图及图注，但非本行动物实验救援，且同页无完整空载体/基因型×PCA析因比较。',figure='已查看Figure6原图：L为染色图，M标签4-HNE，N标签MDA；正文/图注对M/N不一致。保留6L，不猜测底层实验标签。',further='需原始/盲法染色量化及析因交互审查；补回实验若未来纳入须独立evidence_id与细胞模型，不在本行扩写。')
review('39589556',2,'NOT_APPLICABLE_NO_PROTEIN_TARGET','INDIRECT_OXIDATIVE_STRESS_ASSOCIATION','RNA-seq基因集富集属于组学关联；氧化应激GO术语不是ROS或脂质过氧化的直接测量。',target='本行无具体蛋白；不得从富集生成NRF2直接结合靶点。',redox='GO oxidative-stress-related enriched terms, not measured redox analyte',causal='ENRICHMENT_DOES_NOT_IMPLY_PATHWAY_ACTIVATION',rescue='NOT_APPLICABLE',further='需补充术语/基因集ID、比较方向、背景基因集及校正p值；不把富集解释为激活。')
for n,gene in [(1,'HDAC1'),(2,'GATA4'),(3,'RELA')]:
 review('41594941',n,'READOUT_ONLY','OTHER_BIOLOGICAL_FUNCTION',f'{gene}表达或定位变化支持细胞响应；本行未直接测量氧化还原终点，不等同直接结合或基因必要性。',target=gene+'，Homo sapiens；原有参考标识仅作对象定位。',redox='NONE; protein abundance/localization response',causal='READOUT_CHANGE_NOT_DIRECT_BINDING_NOT_NECESSITY',rescue='未核实该比较有siRNA耐受性补回或独立救援设计。',further='保留100µM/24h这一已提取条件；其他剂量不在本行合并。抗炎响应不能自动称为抗氧化机制。')
review('41594941',4,'COMPUTATIONAL_ONLY','OTHER_BIOLOGICAL_FUNCTION','对接/MD仅预测HDAC1–PCA相互作用；HDAC1/GATA4的Co-IP是蛋白–蛋白关系，不是PCA–蛋白结合。',target='HDAC1对接模型物种/构建物在当前来源未独立核实；保持UNRESOLVED。',redox='NONE_MEASURED',causal='MD_STABILITY_NOT_EXPERIMENTAL_BINDING',rescue='NOT_APPLICABLE',further='需明确PDB/构建物、物种、计算条件与对照；不能用同论文siRNA表型升级本行。')
review('41594941',5,'READOUT_ONLY','OTHER_BIOLOGICAL_FUNCTION','联合PCA+si-HDAC1相较单独干预未检出显著额外改变；NS不证明等效或真正无效应。',status='RECLASSIFICATION_PROPOSED',target='本行读数GATA4，不应因操纵HDAC1就把GATA4升级为功能必要蛋白。',proposed_direction='NO_STATISTICALLY_SIGNIFICANT_INCREMENT_DETECTED',redox='NONE; GATA4 abundance',causal='PHENOCOPY_OR_NONADDITIVITY_NOT_NECESSITY_NOT_EQUIVALENCE',rescue='未见HDAC1耐受siRNA回补或PCA作用的因果救援；不将非加和称为救援。',direction='原NO_ADDITIONAL_CHANGE建议收窄为未检出显著增量，避免把NS写成零效应。',further='人工复核Figure5C-D、完整时间线、联合与单独组统计、siRNA特异性及功效；关系类别PATHWAY_MODULATION可保留。')
review('42170612',1,'UNRESOLVED_PROTEIN_OR_EVIDENCE','OTHER_BIOLOGICAL_FUNCTION','Methods2.7.2、结果与Table3指α-amylase；Figure2B图注指saliva。原图热曲线本身不能确认制备物。',status='HOLD_SOURCE_VERIFICATION',target='供应商Yuanye、活性9.4U/mg已报告，但货号、来源物种/亚型未核实；不能赋AMY1/AMY2。1JXJ为人源模型也不证明商业试剂同源。',redox='NONE; ITC binding heat',causal='CALORIMETRIC_ASSOCIATION_REPORT_WITH_PREPARATION_CONFLICT',rescue='NOT_APPLICABLE',dose='12mmol/L为注射器浓度，7.6µmol/L为方法中的蛋白浓度；不是样品最终暴露浓度。',duration='原时长栏实际含滴定次数/每针时长/间隔，建议另存protocol而非换算生物暴露时长。',controls='已报告PCA→PBS稀释热校准；仍需蛋白来源、缓冲基质、拟合模型与制备物核对。',figure='已查看原Figure2；Table3量热参数按表标题归α-amylase；三处内容并列，不代作者更正图注。',further='需原始实验记录/供应商货号及作者澄清；荧光与ITC文中称同一蛋白名，但不能证明同批制备物，对接是结构模型而非试剂。')
review('42170612',2,'COMPUTATIONAL_ONLY','OTHER_BIOLOGICAL_FUNCTION','hTAS2R16的对接/100ns MD为涩感相关预测，不是受体结合或功能测定，也非抗氧化机制。',target='人TAS2R16，参考Q9NYV7；有标准ID不增加实验证据。',redox='NONE',causal='COMPUTATIONAL_ONLY',rescue='NOT_APPLICABLE',further='如将来提实验靶点，需受体功能/正交结合及特异性对照；不因抗氧化无关而删除真实预测。')
review('37025617',1,'READOUT_ONLY','INDIRECT_OXIDATIVE_STRESS_ASSOCIATION','eNOS磷酸化/总蛋白比值变化是信号响应；本行不含直接ROS或脂质过氧化终点。',target='小鼠Nos3/eNOS，参考P70313；不是PCA结合靶点。',redox='NONE_IN_THIS_ROW; eNOS phosphorylation ratio',causal='PHOSPHORYLATION_RESPONSE_NOT_BINDING',rescue='未在此行检验遗传救援。',duration='overnight保留原词，不换算小时。',further='同论文DHE测量是其他观察，不能迁移到本行；需保留NO信号与直接抗氧化的边界。')
review('37025617',2,'UNRESOLVED_PROTEIN_OR_EVIDENCE','INDIRECT_OXIDATIVE_STRESS_ASSOCIATION','单一Akt inhibitor IV药理阻断支持通路参与，但未定位具体Akt亚型或证明其蛋白必要性。',status='RECLASSIFICATION_PROPOSED',proposed_relation='PATHWAY_MODULATION',target='pan-Akt家族，具体基因/亚型未解决；不自动赋AKT1或UniProt。',redox='NONE_IN_THIS_ROW; p-eNOS/eNOS response',causal='SINGLE_PHARMACOLOGICAL_PERTURBATION_NOT_PROTEIN_SPECIFIC_NECESSITY',rescue='未见第二正交抑制剂、遗传必要性及回补救援；不推断抑制剂绝对特异。',duration='overnight未具体小时；保持原文。',further='建议主关系收窄为PATHWAY_MODULATION并保留药理参与子标签；属拟议保守分级规则，不宣称原作者药理观察错误。')
review('42413844',1,'UNRESOLVED_PROTEIN_OR_EVIDENCE','OTHER_BIOLOGICAL_FUNCTION','摘要报告TRAF2结构域结合及荧光/量热法，但未取得可核查完整方法、构建物、剂量及对照。',status='HOLD_SOURCE_VERIFICATION',target='重组TRAF2的物种、边界、标签、纯度和寡聚状态未核实；不从HAP1推定重组蛋白物种。',redox='NONE; reported binding',causal='ABSTRACT_REPORTED_BINDING_NOT_VERIFIED_DIRECT_TARGET',rescue='NOT_ASSESSABLE_ABSTRACT_ONLY',further='出版社403/摘要预览；作者机构库2108/470363无关联文件；不使用摘要之外猜测Kd、ITC类型或具体蛋白构建。')
review('42413844',2,'UNRESOLVED_PROTEIN_OR_EVIDENCE','OTHER_BIOLOGICAL_FUNCTION','HAP1存活增加与TRAF2依赖为摘要报告；具体遗传或药理干预未核实，不能写成敲除/救援已验证。',status='HOLD_SOURCE_VERIFICATION',target='HAP1细胞人源背景与功能蛋白参考TRAF2分开；具体依赖设计未明。',redox='NONE; HAP1 viability',causal='ABSTRACT_REPORTED_DEPENDENCE_ONLY',rescue='UNRESOLVED_FULL_TEXT_REQUIRED',further='保留ABSTRACT_ONLY及剂量UNRESOLVED；细胞增殖不等于抗氧化获益，也不直接定为临床不利。')
review('32007785',1,'UNRESOLVED_PROTEIN_OR_EVIDENCE','OTHER_BIOLOGICAL_FUNCTION','摘要支持BV2炎症介质与SIRT1/NF-κB关联，缺剂量、时长、对照及具体干预；不推断蛋白方向。',status='HOLD_SOURCE_VERIFICATION',target='SIRT1为摘要命名对象；实验验证方法和标准标识仍待查。',redox='NONE_REPORTED_IN_THIS_OBSERVATION',causal='ABSTRACT_PATHWAY_ASSOCIATION_NOT_DIRECT_BINDING',rescue='UNRESOLVED',further='需要原始全文/补充材料；BV2与下游PC12模型不可压成同一实验观察。')
review('11023549',1,'UNRESOLVED_PROTEIN_OR_EVIDENCE','PROOXIDANT_OR_ADVERSE_RESPONSE','摘要中20000nmol局部PCA、3h皮肤GSH降低及arbutin对抗支持促氧化情境；不证明特定TYR直接结合或必要性。',status='HOLD_SOURCE_VERIFICATION',proposed_relation='PATHWAY_MODULATION',target='Tyr为药理归因对象，尚缺全文具体酶学/特异性验证。',redox='skin GSH depletion',secondary='DIRECT_REDOX_OUTCOME',causal='ABSTRACT_PHARMACOLOGICAL_ATTRIBUTION_NOT_PROTEIN_SPECIFIC_CAUSALITY',rescue='抑制剂对抗不等于遗传回补救援。',further='优先补全文、arbutin剂量、时序和对照；可建议降为通路/红氧响应关系，但总体先HOLD来源。不可外推正常膳食。')
for n,tissue in [(1,'liver'),(2,'kidney')]:
 review('11714376',n,'NOT_APPLICABLE_NO_PROTEIN_TARGET','PROOXIDANT_OR_ADVERSE_RESPONSE','摘要直接报告组织GSH耗竭；这是代谢物终点，不是蛋白靶点验证。',status='HOLD_SOURCE_VERIFICATION',target='NOT_APPLICABLE；GSH不能填为基因/蛋白。',redox=tissue+' GSH depletion',secondary='DIRECT_REDOX_OUTCOME',causal='REDOX_OUTCOME_NOT_PROTEIN_MECHANISM',rescue='本行不加入其他BSO实验的机制归因。',further='全文/对照与检测法仍待核实；500mg/kg腹腔单次与0.1%饮水60日分开；不把饮水百分比转换为假定mg/kg。')
assert set(R)=={x['evidence_id'] for x in a}
matrix=[]
for pos,r in enumerate(a,1):
 q=R[r['evidence_id']];abstract=r['source_verification_status']=='ABSTRACT_ONLY';status=q.get('status','KEEP_PROVISIONAL')
 row=dict(evidence_id=r['evidence_id'],source_table_path='workspaces/phase1c_mechanism_evidence_pilot/compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv',source_data_record=pos,source_locator_original=r['source_locator'],original_record_json=j(r),study_id=r['study_id'],DOI=r['DOI'],PMID=r['PMID'],article_url=r['article_url'],original_relation_type=r['evidence_relation_type'],proposed_relation_type=q.get('proposed_relation',r['evidence_relation_type']),original_target_validation_status=r['target_validation_status'],protein_target_confirmation_proposed=q['confirmation'],antioxidant_relevance_proposed=q['relevance'],antioxidant_relevance_secondary_proposed=q.get('secondary','NONE'),redox_endpoint_review=q['redox'],review_status=status,review_reason_CN=q['reason'],identity_and_form_check='PARENT_REFERENCE_CONSISTENT_AUTHOR_REPORTED; 非独立实验样品鉴定；盐/酯/结合物不可默认等同。',bibliography_check='CURRENT_PUBMED_DOI_PMID_MATCH; 题名已读；当前响应无撤稿/关注声明关联，非永久有效性保证。',experimental_model_check=r['experimental_model']+'; '+r['species']+'; '+r['cell_line_or_tissue']+'; '+('ABSTRACT_ONLY_MODEL_DEPTH_LIMITED' if abstract else '与正文方法和图注对照，未声称原始数据复现。'),dose_and_unit_check=q.get('dose',r['dose']+' '+r['dose_unit']+'; '+('摘要级，未解决值不补造。' if abstract else '保留原报告剂量，不转换为膳食可达性。')),duration_check=q.get('duration',r['treatment_duration']+'; '+('仅摘要可支持的时长；缺项仍待核。' if abstract else 'PCA时长与挑战/转染时序分列；不合并其他模型。')),controls_check=q.get('controls',r['control_group']+'; '+('摘要未核实具体对照。' if abstract else '按所列比较核对；不推断未报告控制。')),assay_method_check=r['assay_method']+'; '+('ABSTRACT_ONLY，精确方法仍待核。' if abstract else '不以方法名称本身升级因果/结合程度。'),target_identity_check=q['target'],direction_check=q.get('direction',r['target_effect_direction']+'; 相对原有指定对照解释，非临床效力。'),functional_outcome_check=r['functional_outcome']+'; 仅本行终点，不挪用同论文其他模型。',figure_table_check=q.get('figure',r['source_figure_or_table']+'; '+('仅摘要，不声称逐图核实。' if abstract else '与正文/图注核对；除关键NRF2及amylase图外，本轮未逐像素审图。')),relation_type_check='PROPOSAL_CHANGE_NOT_APPLIED' if q.get('proposed_relation',r['evidence_relation_type'])!=r['evidence_relation_type'] else 'RELATION_CLASS_RETAINED_WITH_SUPPORT_LIMITS',causal_scope_check=q['causal'],rescue_experiment_review=q['rescue'],proposed_target_species=q.get('proposed_species',r['target_species']),proposed_UniProt_ID=q.get('proposed_uniprot',r['UniProt_ID']),proposed_effect_direction=q.get('proposed_direction',r['target_effect_direction']),further_source_or_human_review=q['further'],source_local_path_original=r['source_local_path'],additional_source_URL='https://www.rcsb.org/structure/3GLS' if r['evidence_id']=='ME-AFF0061-32520409-002' else 'https://link.springer.com/article/10.1007/s10565-024-09953-7' if r['PMID']=='39589556' else 'https://art.torvergata.it/handle/2108/470363' if r['PMID']=='42413844' else r['article_url'],reviewer_type='CODEX_SOURCE_BASED_REVIEW_NOT_INDEPENDENT_HUMAN',human_review_status='NOT_REVIEWED',proposal_applied='NO')
 matrix.append(row)

issues=[]
def issue(code,priority,kind,title,ids,needed,proposal):
 issues.append(dict(issue_id=code,priority=priority,issue_class=kind,question_CN=title,evidence_ids=j(ids),required_evidence_CN=needed,proposed_decision_CN=proposal,decision_status='HUMAN_DECISION_REQUIRED',applied='NO'))
def ids(pmid):return [r['evidence_id'] for r in a if r['PMID']==pmid]
issue('G2-01','P0','SOURCE_LIMITATION','TRAF2直接结合及功能依赖的完整原始数据是否支持作者主张？',ids('42413844'),'合法全文、蛋白构建物物种/域/纯度、剂量、量热类型、对照及依赖干预设计。','继续HOLD及ABSTRACT_ONLY，不指定亲和常数或直接靶点已确认。')
issue('G2-02','P0','SOURCE_CONFLICT','ITC对象α-amylase还是saliva，是否为同一制备物？',[ids('42170612')[0]],'作者澄清、原始ITC文件、供应商货号、物种/亚型及批次；Figure2B、Table3、Methods对应。','继续HOLD；PDB1JXJ人源不能决定商业蛋白身份。')
issue('G2-03','P1','SOURCE_CONFLICT','NRF2 Figure6M/N正文/图注/原图标签冲突如何处理？',ids('39589556'),'原图标签已见M=4-HNE/N=MDA；仍需底层数据/作者勘误或澄清。','保留6L观察；并列三处冲突，不替作者更正底层标签。')
issue('G2-04','P1','CAUSAL_BOUNDARY','NRF2补回是否足以称完全救援，是否适用于动物6L？',[ids('39589556')[0]],'补充PDF第3页S2及完整空载体/基因型/剂量/时序、正式交互检验。','细胞补回为额外研究层支持；不移植到动物证据行，不新增原21条。')
issue('G2-05','P1','CLASSIFICATION_PROPOSAL','单一Akt抑制剂是否足以列为蛋白级FUNCTIONAL_CAUSAL？',[ids('37025617')[1]],'遗传/回补或正交药理与靶点选择性证据、Akt亚型。','建议改PATHWAY_MODULATION并保留药理参与标签；原值不变。')
issue('G2-06','P1','DIRECTION_PROPOSAL','HDAC1联合组NS能否写NO_ADDITIONAL_CHANGE？',[ids('41594941')[4]],'Figure5完整比较、效应量/区间及设计功效；若称等效须等效性设计。','建议未检出显著增量；不宣称零效应、等效或必要性。')
issue('G2-07','P1','IDENTITY_PROPOSAL','SIRT3对接模型物种可否补全？',[ids('32520409')[1]],'RCSB3GLS实体1的来源物种与Q9NTG7映射，已获取。','建议Homo sapiens/Q9NTG7；仅元数据修订提案，仍COMPUTATIONAL_ONLY。')
issue('G2-08','P1','SOURCE_LIMITATION','SIRT1、TYR及GSH摘要行缺哪些决定性实验信息？',ids('32007785')+ids('11023549')+ids('11714376'),'原始全文、方法、对照、剂量/时间、抑制剂特异性和原图。','这些记录保持来源HOLD；TYR关系建议降为响应关联但不因促氧化而排除。')
issue('G2-09','P1','SCHEMA_GOVERNANCE','是否批准独立的靶点确认与抗氧化相关性维度？',[r['evidence_id'] for r in a],'用户/人工审核分类规则、适用边界和复核事件模型。','先批准规则，不直接修改66字段或既有等级。')
issue('G2-10','P1','SCALE_UP_BLOCKER','是否允许把表达/代谢终点计为直接抗氧化机制？',[r['evidence_id'] for r in a],'逐观察终点与因果比较；禁止借用同论文其他实验终点。','区分直接红氧终点、间接关联、其他功能与促氧化；保留真实但非抗氧化观察。')
issue('G2-11','P1','INDEPENDENCE','experiment_id是否误把同一实验每个读数当成独立实验？',[r['evidence_id'] for r in a],'实验设计/样本批次、同图多蛋白共享材料和跨论文复用核对。','观察ID保留，建议独立实验实体及观察多对一关联，不自动合并。')
issue('G2-12','P1','GATE_DEFINITION','Gate1正式标准与Gate2人工审查责任尚未批准。',[],'用户与人工科学审核者书面判据及签署。','Gate1 HOLD；Gate2 HUMAN_SCIENTIFIC_REVIEW_REQUIRED；Release HOLD；不扩大候选。')

schema=[]
must={'compound_form','PubChem_CID','InChIKey','target_role','target_validation_status','direct_target_status','functional_outcome','effect_context','evidence_relation_type','dose','dose_unit','experiment_id','target_experimental_support','source_verification_status','human_review_status','publication_status','publication_date_precision'}
recommended={'target_gene','target_protein','UniProt_ID','target_species','target_identifier_status','pathway_name','pathway_ID','pathway_database','pathway_effect_direction','target_effect_direction','observation_endpoint','control_group','treatment_duration','pretreatment_duration','challenge_agent','challenge_dose','challenge_duration','source_figure_or_table','source_locator','experiment_independence_status','evidence_status'}
for d in dictionary:
 f=d['field_name'];priority='MUST_CHANGE_BEFORE_SCALE_UP' if f in must else 'RECOMMENDED' if f in recommended else 'OPTIONAL_FUTURE'
 note='保留字段；只细化语义与允许规则，不按当前观察值自动冻结合法词汇。'
 if f in ['PubChem_CID','InChIKey','compound_form']:note='区分候选母体参考锚与实验试剂结构；不得将盐/酯/结合物无条件映射为母体。'
 elif f in ['dose','dose_unit']:note='剂量值/单位与dose_basis分开；注射器浓度、最终浓度及饮水百分比不混淆。'
 elif f=='experiment_id':note='定义真实实验/材料或预先声明的比较实体；一个实验可关联多条观察，不按每行新造独立实验。'
 elif f in ['target_role','target_validation_status','direct_target_status','target_experimental_support','evidence_relation_type']:note='保持关系类别与靶点确认、来源层级正交；单一抑制剂及同论文其他实验不能跨级。'
 elif f in ['functional_outcome','effect_context','observation_endpoint']:note='复用已有终点字段；加入抗氧化相关性与结局方向独立标记，保留阴性/促氧化，不把NS写成零。'
 elif f in ['publication_status','human_review_status','publication_date_precision']:note='允许规则不能只取当前已观察值；撤稿/更正/年份精度/真实人工事件需支持，未审仍未审。'
 elif f in ['target_gene','target_protein','target_species','UniProt_ID']:note='允许家族/转录本/物种未决状态；记录测量层级，不从参考映射推断实验验证。'
 schema.append(dict(field_name=f,review_priority=priority,definition_original_CN=d['definition_cn'],allowed_rule_original=d['allowed_values_or_rule'],proposal_CN=note,new_field_required='NO_REUSE_EXISTING_FIELD',applied='NO'))

counts={'reviewed_records':len(matrix),'review_status_counts':dict(Counter(r['review_status'] for r in matrix)),'protein_confirmation_counts':dict(Counter(r['protein_target_confirmation_proposed'] for r in matrix)),'antioxidant_relevance_primary_counts':dict(Counter(r['antioxidant_relevance_proposed'] for r in matrix)),'relation_change_proposals':[r['evidence_id'] for r in matrix if r['proposed_relation_type']!=r['original_relation_type']],'direction_change_proposals':[r['evidence_id'] for r in matrix if r['proposed_effect_direction']!=json.loads(r['original_record_json'])['target_effect_direction']],'direct_specific_protein_confirmed_by_this_review':0,'existing_fields_reviewed':len(schema),'open_issues':len(issues),'original_evidence_or_schema_changed':False}
csvout('AFF-0061_Gate2_Evidence_Review_Matrix.csv',matrix)
csvout('Gate2_Open_Issues_and_Decisions.csv',issues)
csvout('Existing_66_Field_Review_Coverage.csv',schema)

classification='''# 机制证据分级与抗氧化相关性提案 v0.1

本提案不是批准规则，也未更改原21条或66字段。研究任务为定向科学复核，执行者为Codex，不是独立人工审稿人。五类关系保持DIRECT_BINDING、FUNCTIONAL_CAUSAL、PATHWAY_MODULATION、OMICS_ASSOCIATION、COMPUTATIONAL_PREDICTION；它们描述观察关系，不是单轴证据分数。必须同时读取来源层级、特定蛋白确认程度和具体模型，不能以标题或类别名自动认定验证。

## 独立的蛋白靶点确认维度

DIRECT_BINDING_SUPPORTED：明确物种、亚型、构建物和化合物形式的具体蛋白，具有可追溯的实验结合结果及适当阴性/背景控制、剂量与模型拟合。候选方法可包括ITC、SPR、MST或结构证据；方法名称不是充分条件，热稳定性/光谱变化须审查聚集、内滤效应、非特异及正交证据。只有摘要报告、未明制备物或仅对接不进入此类。本轮无记录达到此类。

FUNCTIONAL_PARTICIPATION_SUPPORTED：已定位蛋白/基因，在具体实验中有遗传丧失功能、回补/救援或充分正交干预支持其参与。此类不证明小分子直接结合；全身敲除与基线表型、发育适应及相互作用统计仍有适用边界。回补须核对同一基因背景、空载体、剂量、时序及结局，不能从不同模型搬运。

READOUT_ONLY：仅观察表达、磷酸化、定位或特定读数改变。须注明transcript/protein/activity/localization层级，qPCR不能被计作蛋白实测。蛋白–蛋白Co-IP不能替代PCA–蛋白结合。

OMICS_ASSOCIATED：转录组、蛋白组等关联候选，需统计对照和多重校正；不自动获得功能验证。通路富集不能生成已验证蛋白靶点。

COMPUTATIONAL_ONLY：对接、MD及结构预测；有UniProt/PDB标识也不升级实验。UNRESOLVED_PROTEIN_OR_EVIDENCE：身份、物种、制备物、来源或关键设计不足；可同时保留作者报告的关系，不声称其已证实。另用NOT_APPLICABLE_NO_PROTEIN_TARGET处理GSH/通路富集等真正无蛋白对象的观察，不将不适用与未解决混同。

这些是名义分类，不是可直接加总的1–6分。更强的来源不能从同论文其他行借用。对于单一抑制剂，建议保留药理参与子标签，默认不足以支持特定蛋白的必要性；Akt与摘要TYR行提出收窄关系建议。这是拟议保守规则，不是断言药理观察本身错误。

## 抗氧化相关性：逐观察判定

DIRECT_REDOX_OUTCOME：本行实际测ROS、脂质过氧化、GSH或其他明确红氧终点，并记录具体指标及方向；不是抗氧化蛋白机制已验证。ANTIOXIDANT_FUNCTIONAL_MECHANISM：本行对红氧结局有可核查的干预–机制关系；单纯命中Nrf2/SIRT家族名不够。INDIRECT_OXIDATIVE_STRESS_ASSOCIATION：与氧化应激有研究情境或组学关联，但本行没有充分功能红氧验证。OTHER_BIOLOGICAL_FUNCTION：涩感、脂肪变、增殖、单纯炎症/定位等其他观察；不因与抗氧化无直接关系而删除。PROOXIDANT_OR_ADVERSE_RESPONSE：实测促氧化或不利响应，保留剂量/时序/模型；不可把肿瘤细胞存活增加自动外推成临床危害。UNRESOLVED：原始信息不足，不能由通路名称推断。

建议一个primary值，加可选secondary标签。原图6L可primary=DIRECT_REDOX_OUTCOME、secondary=ANTIOXIDANT_FUNCTIONAL_MECHANISM；GSH耗竭可primary=PROOXIDANT_OR_ADVERSE_RESPONSE、secondary=DIRECT_REDOX_OUTCOME。分类归属与来源可核查度分列：摘要明确报告GSH耗竭，可提出相关性分类，但记录仍HOLD，不能因此声称全文已验证。

SIRT3脂肪变及Kmo转录观察不借用同论文其他ROS读数；eNOS磷酸化只作间接关联。NRF2补回细胞实验不移用于动物行。DPPH/ORAC化学实验若另有数据，只能支持化学结局，不自动成为蛋白机制。高剂量体内给药或高浓度体外暴露均不能直接标为正常膳食可达。未检出显著差异不是等效、无作用或零效应。

来源、直接结合、功能参与、抗氧化相关性与人工批准必须正交记录。本轮只提出分类和验证边界，不执行任何重新分级写回。
'''
text('Mechanism_Evidence_Classification_Proposal_v0.1.md',classification)

schema_doc=f'''# 66字段扩展性与修改建议 v0.1

已逐项检查现有66字段，结果见Existing_66_Field_Review_Coverage.csv。保留一行“候选物×关系×具体观察”的粒度；原21行和字典未变。无需把数据库扩为不断增加的宽表，优先细化既有字段语义，并用关联表承载重复结构。逐字段的OPTIONAL_FUTURE只表示目前没有必须修改的定义，不表示该字段可以删除或不再必填；三个优先级仅针对修改建议。

MUST_CHANGE_BEFORE_SCALE_UP：增加独立target_confirmation_class与antioxidant_relevance_primary，允许受控secondary标签；必须经人工批准后实施。复用已有observation_endpoint而不再新增同义终点字段。对终点建立旁表定义redox endpoint/非红氧、测量层级、方向与统计解释；GSH为代谢物，不填成蛋白。dose_unit保留纯单位，建议单独dose_basis区分给药量、培养最终浓度、注射器浓度和饮水百分比。原形式/参考CID必须明确是母体锚还是实验样品鉴定，先修订语义，不自动新增结构ID或补值。

MUST_CHANGE_BEFORE_SCALE_UP：experiment_id须可将同一实验/样本多个检测关联，不能每行一个ID就称独立实验；多个剂量、时间点、模型分别观察，重复实验与同一样本不同readout分开。CONTROL/挑战参数若多值复杂，建议实验实体/干预关联表，不把不同处理拼成一个可计算字段。基因型×药物、单一药理、平行表型和真正回补分开标注；可用现有target_validation_status受控词汇及review旁表，不强制再加多列。target_effect_direction不能混合变化方向、是否依赖、是否有结合及显著性，至少先通过规则将这些语义分开，不把NS编码为真实NO_CHANGE。

MUST_CHANGE_BEFORE_SCALE_UP：现有枚举多为观察值集合，不足以覆盖未来合法状态。例如publication_date_precision当前仅DAY/MONTH、publication_status仅无撤稿链接、human_review_status仅未审；扩展规则应容纳YEAR、更正/关注声明/撤稿及真实有据的人工事件，绝不能自动置HUMAN_APPROVED。审核历史及更正采用独立Review_Event/Change_Log旁表，保留对象ID、旧值/新值、理由、来源、审核者类型、日期及批准状态，不覆盖旧证据。来源层级须区分仅摘要、正文、图像、补充材料及局部冲突；FULL_TEXT_VERIFIED不能暗示原始图像已验。

RECOMMENDED：复用UniProt_ID、target_species、pathway_ID/database，但增加可追溯映射依据/版本于受控旁表；家族/物种未决不得强制指定accession。作者命名轴与KEGG/Reactome标准通路明确分开；富集过程不直接冒用通路ID。补充结构化效应量、单位、n含义、区间及检验，放Endpoint_Result旁表，仅在来源确有信息时填入。浓度/剂量可达性作为独立exposure_relevance判定，缺人体PK/摄入证据时UNRESOLVED，不能仅凭nM/µM或标题physiological宣称膳食可达。

OPTIONAL_FUTURE：标准单位换算、标准术语本体及跨论文实验/队列关联需要成熟原始数据和明确规则后再做；不要求本轮算法、网络分析或增加未核实的ID。样品批次、抗体、补充材料和原始图像的详细资产管理可放实验/来源实体，不把全部内容塞入每个观察行。

本轮字段审查优先级计数：{j(dict(Counter(r['review_priority'] for r in schema)))}。此计数是现有字段治理审查优先级，不是要求新增相同数量字段。所有建议未应用。先解决TRAF2/ITC来源问题和审核规则，再考虑扩大其他候选物。
'''
text('Mechanism_Evidence_Schema_Change_Proposal_v0.1.md',schema_doc)

critical='''# 原儿茶酸关键来源核查报告

本报告为Codex定向来源复核，不替代独立人工科学审核。原21条不改，以下建议均Proposal。仅使用原始论文、作者机构库和结构数据库；未运行文献中的网络分析方法。

## TRAF2：未解决，维持摘要层级

PMID42413844、DOI10.1016/j.abb.2026.110937的文章自身元数据已在PubMed刷新核对。摘要报告荧光光谱、量热检测及TRAF结构域相互作用，并报告HAP1存活的TRAF2相关性。不能据此指定量热法必为ITC、构建物边界、蛋白物种、浓度、对照或敲除/救援设计。出版社入口本轮返回403，网页检索仅可见摘要/预览；作者机构库https://art.torvergata.it/handle/2108/470363明确无关联文件。机构库程序请求证书校验失败，网页工具独立读取了该记录，未绕过证书或权限。两条记录HOLD_SOURCE_VERIFICATION、ABSTRACT_ONLY；不是排除真实报告，也不是确认直接靶点。

## α-amylase：证据仍冲突，Table3不能独立裁决

PMID42170612、DOI10.1016/j.crfs.2026.101435的Methods2.1称Yuanye商业α-amylase，活性9.4U/mg，未给可独立定位的物种/亚型/批号。2.7.1与2.7.2均使用α-amylase名称，后者写蛋白7.6µM、PCA注射器12mmol/L、25°C及PCA→PBS稀释热对照。Results及Table3也称α-amylase；原Figure2B图注却称saliva。原图2B可见热曲线，但不能从曲线识别蛋白制备物。文字一致性倾向不能代替作者澄清，不宣布图注错误已更正。

已核对PDB1JXJ为人源结构，参考映射P0DUB6；这只说明计算模板，不能证明荧光、ITC商业蛋白同物种、同亚型或同批。对接不使用“同一商业试剂制备物”，它使用结构模型。保持HOLD，不赋AMY1/AMY2。需原始ITC及试剂货号/来源和Figure2B、Table3对应。涩感相互作用归OTHER_BIOLOGICAL_FUNCTION，真实机制观察保留，不列作抗氧化蛋白机制。

## SIRT3：功能参与与对接分开

PMID32520409、DOI10.1111/bph.15159的Methods2.1及Results3.3/Figure2l支持全身Sirt3缺失背景中PCA对HFD肝脂肪变的保护响应丧失/减弱；可保留模型内功能参与，但全身敲除基线与交互统计仍待人工评议。本行未见敲除动物同背景基因补回；论文的细胞过表达、ACSF3突变及蛋白–蛋白Co-IP不等于PCA直接结合或本行动物救援。Figure2c-d仅对接；RCSB3GLS实体1确认人源/Q9NTG7，建议补其计算物种，不升级实验证据。脂肪变观察不借用讨论中的ROS叙述作为本行直接红氧测量。

## NRF2：6L定位保留，补回单独解释

PMID39589556、DOI10.1007/s10565-024-09953-7已查看Figure6原图和相关方法：L为BODIPY脂质过氧化染色，模型为WT/全身Nrf2缺失小鼠、PCA100mg/kg/day口服10周。现有6L观察可保留为直接红氧终点及情境性功能参与；未从图像重提数值或宣称原始数据完整性已验。

原图可读标签M=4-HNE、N=MDA，正文相应引用与图注的M=MDA/N=4-HNE不同。该图文矛盾仍是来源问题：可客观记录标签，不能替作者判断底层检测数据命名是否正确或发布勘误；本轮不把M/N值加入数据库，也不改原6L行。

已读补充PDF第3页S2图像及图注：NRF2缺失细胞转入NRF2表达载体，A有蛋白恢复图，B/C报告补回背景下MDA与ATP结局。它提供细胞补回支持，不是单纯平行siRNA表型；但图内比较及完整载体/时序仍需审核，不能称完全证明唯一机制。此细胞实验不移用于动物6L，也不新增到21条母表。若日后提取，须另行分配观察与实验ID。

## HDAC1与Akt：不把药理或NS升级为必要性

PMID41594941、DOI10.3390/biology15020206的Figure4是表达/定位变化；Figure5 HDAC1 knockdown与PCA平行改善及联合组无显著额外改变，不能独立证明PCA必须依赖HDAC1。未核到siRNA耐受回补救援；Figure4K Co-IP是HDAC1–GATA4而非小分子结合。Figure6为对接/MD。现有分类总体未把对接升级成实验结合，但NO_ADDITIONAL_CHANGE建议改成“未检出显著增量”，不解释为等效或零效应。

PMID37025617、DOI10.3389/fnut.2023.1060226的Akt inhibitor IV阻断可支持药理参与，但pan-Akt/单一药理实验不能定位AKT1或证明某特定蛋白必要性。建议将该行主关系收窄PATHWAY_MODULATION，同时保留药理参与子标签；eNOS磷酸化本身不是本行直接ROS读数。论文标题directly指直接孵育语境，不证明PCA直接结合eNOS/Akt。

其余摘要SIRT1、TYR及GSH记录见逐条矩阵。促氧化/毒性结果不因方向不利而排除；缺全文/对照等关键来源仍HOLD。完整核查覆盖21条，但没有任何记录获人工批准，没有新增确定的具体直接结合靶点。
'''
text('AFF-0061_Critical_Source_Verification_Report.md',critical)

changed=[p for p,h in base['tracked_hashes'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
rawchanged=[p for p,h in base['existing_raw_cache_hashes'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
assert not changed and not rawchanged,(changed,rawchanged)
checks={'21_records_reviewed':len(matrix)==21,'same_evidence_id_set':{r['evidence_id'] for r in matrix}=={r['evidence_id'] for r in a},'unique_review_ids':len({r['evidence_id'] for r in matrix})==21,'all_66_fields_reviewed':len(schema)==66,'all_14_review_dimensions_nonempty':all(all(r[f] for f in ['identity_and_form_check','bibliography_check','experimental_model_check','dose_and_unit_check','duration_check','controls_check','assay_method_check','target_identity_check','direction_check','functional_outcome_check','figure_table_check','relation_type_check','causal_scope_check','further_source_or_human_review']) for r in matrix),'original_source_tables_unchanged':not changed,'existing_local_cache_unchanged':not rawchanged,'no_proposals_applied':all(r['proposal_applied']=='NO' for r in matrix),'no_human_approval':all(r['human_review_status']=='NOT_REVIEWED' for r in matrix),'current_10_articles_bibliography_verified':len(pub)==10,'head_unchanged_before_authorized_commit':git('rev-parse','HEAD')==base['HEAD'],'all_output_statuses_valid':all(r['review_status'] in ['KEEP_PROVISIONAL','RECLASSIFICATION_PROPOSED','HOLD_SOURCE_VERIFICATION','EXCLUDE_PROPOSED','UNRESOLVED'] for r in matrix)}
assert all(checks.values()),checks
text('Review_Counts_and_Integrity.json',{'counts':counts,'checks':checks,'start_HEAD':base['HEAD'],'review_end_HEAD_before_authorized_commit':git('rev-parse','HEAD'),'remote_main_at_start':base['remote_main_checked'],'branch':git('branch','--show-current'),'tracked_files_checked':len(base['tracked_hashes']),'existing_raw_files_checked':len(base['existing_raw_cache_hashes']),'original_changed_paths':changed,'existing_raw_changed_paths':rawchanged,'worktree':git('status','--short'),'Gate1':'HOLD','Gate2':'HUMAN_SCIENTIFIC_REVIEW_REQUIRED','Release':'HOLD'})
manifest=[]
for p in sorted((O/'sources').iterdir()):
 if p.is_file():manifest.append({'local_path':'sources/'+p.name,'bytes':p.stat().st_size,'sha256':sha(p),'git_distribution':'LOCAL_ONLY_EXCLUDED','URL_source':'Source_Access_Log.json or Metadata_Refresh_Log.json','verification_scope':'Raw source retained locally; see critical report for actually inspected images/pages'})
csvout('Local_Gate2_Source_Manifest.csv',manifest)
names=[('P0','AFF-0061_Gate2_Evidence_Review_Matrix.csv'),('P0','AFF-0061_Critical_Source_Verification_Report.md'),('P0','Sync_to_ChatGPT_Phase1C_Gate2.md'),('P1','Mechanism_Evidence_Classification_Proposal_v0.1.md'),('P1','Mechanism_Evidence_Schema_Change_Proposal_v0.1.md'),('P1','Gate2_Open_Issues_and_Decisions.csv'),('P2','Gate2_Review_QC_Report.md')]
transfer='\n'.join(f'- {p}：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/{name}`' for p,name in names)
summary=f'''共复核21/21条、10篇原始出版物。审核状态为{j(counts['review_status_counts'])}；EXCLUDE_PROPOSED=0、UNRESOLVED=0（无整体无法判断行，但多个具体属性仍UNRESOLVED）。蛋白确认提案为{j(counts['protein_confirmation_counts'])}。抗氧化相关性primary为{j(counts['antioxidant_relevance_primary_counts'])}；NRF2行另有ANTIOXIDANT_FUNCTIONAL_MECHANISM secondary，促氧化GSH行另有DIRECT_REDOX_OUTCOME secondary。没有强制让每类都非零。

未发现把现有对接/MD行写为实验直接结合的错误。提出2个主关系收窄建议（Akt药理行、摘要TYR行）；TYR因来源不足总体先HOLD，不能将关系变更提案数与RECLASSIFICATION_PROPOSED状态数混为同一统计。另1个HDAC1联合组方向措辞需收窄，避免把NS当零效应。SIRT3对接物种可建议补为人源，但仍是计算预测。原行、原关系和字典均未修改。

TRAF2合法全文未恢复，两条保持ABSTRACT_ONLY/HOLD；α-amylase的Table3及原图核查未解决制备物矛盾，仍HOLD。NRF2实际读到补充S2细胞补回；不得移用于动物6L。Figure6M/N原图标签可读，但图文冲突仍待作者/底层数据裁决，保留6L不猜测改值。未发现10篇当前元数据中的DOI/PMID实质冲突或撤稿链接；这不是永久有效性保证。参考母体身份未发现新冲突，商业amylase及重组TRAF2具体身份仍待解决。

66字段逐项评估完成，建议先批准独立靶点确认、抗氧化相关性、剂量基准及审核事件/实验粒度规则；不要求无差别加列。抗氧化相关性独立于靶点强度，非抗氧化机制仍保留。暂不建议批量扩展其他候选物。

Gate1：HOLD（正式标准仍待批准）。Gate2：HUMAN_SCIENTIFIC_REVIEW_REQUIRED，未宣布通过。Release：HOLD。Phase1B风险、155临时映射/2待审、缺失身份及冻结资产均未被本轮关闭。'''
protection=f'''起始分支main，实际HEAD与GitHub main只读核对均为{base['HEAD']}。本轮审核产物生成时HEAD仍相同，工作树仅新增gate2_review目录。{len(base['tracked_hashes'])}个原有跟踪文件及{len(base['existing_raw_cache_hashes'])}个既有本地来源缓存哈希均不变；保护对象含原21条/机制Master、T002/T004/T110、两套字典、Phase1B、矩阵与冻结结果。本轮新来源在sources/，通过本目录.gitignore排除上传，清单与URL日志可追溯。没有越权科学写回。

用户已持续授权合适任务的提交前整理与选择性commit/push，因此本轮仅将新增审核Proposal和QC提交，不提交sources、不改科学源表；这不表示Gate2或Release批准。上述HEAD是审核前/提交前快照，提交后的哈希由最终回复及Git记录报告，不改写历史基线。'''
text('Gate2_Review_QC_Report.md',f'''# Gate2定向审核质控

{summary}

程序检查{len(checks)}项通过、0项失败，明细见Review_Counts_and_Integrity.json。逐行矩阵同时保留完整original_record_json及14类审查维度。KEEP_PROVISIONAL仅为待人工批准；HOLD不是判作者报告虚假；RECLASSIFICATION_PROPOSED仅提出规则/措辞修订，不自动写回。

{protection}

本轮人工科学批准数0。完整图像检查仅针对NRF2 Figure6、其补充PDF第3页S2以及amylase Figure2；其余按正文/方法/图注复读，不冒称全部原图和原始数据已审。来源可访问性与图文矛盾分别报告，不用格式检查替代科学验证。未产生PPI、网络接近度、排名或其他候选物数据。

## 转交清单

{transfer}
''')
text('Sync_to_ChatGPT_Phase1C_Gate2.md',f'''# 同步ChatGPT：Phase1C Gate2原儿茶酸定向科学复核

{summary}

保留建议12行、重分类状态2行及来源HOLD7行均详见稳定evidence_id矩阵，禁止把这些自动审核状态当HUMAN_APPROVED。先审TRAF2与ITC具体制备物，再审因果/非加和规则与细胞补回适用性，之后决定字段方案和扩展范围。所有原66字段及原21条未改，未新增机制观察。

{protection}

## 需要上传/转交的完整相对路径

{transfer}

补充可追溯文件：Existing_66_Field_Review_Coverage.csv、Review_Counts_and_Integrity.json、Source_Access_Log.json、Metadata_Refresh_Log.json与Local_Gate2_Source_Manifest.csv，均位于本gate2_review目录。sources原图/PDF/完整元数据仅本地保留，未作为发布附件。完成后停止，等待用户与人工科学审查，不自动启动下一阶段。
''')
print(json.dumps(counts,ensure_ascii=False,indent=2))
