"""Build the Stage1 technical protocol and audit from existing project records."""
from pathlib import Path
import csv
import hashlib
import json

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]
CUTOFF='2026-11-17'

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))

def write(name,rows):
    for row in rows:
        row.update(human_review_status='NOT_REVIEWED',change_applied='NO')
    with (HERE/name).open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)

def main():
    checks=[]
    for folder in ['00_project','01_candidate_discovery','02_identity_and_evidence/01_systematic_supplement',
                   '02_identity_and_evidence/03_date_scoped_review','03_candidate_selection',
                   '04_05_experimental_validation','06_manuscript','07_quality_control']:
        path=ROOT/folder
        assert path.is_dir()
        checks.append(dict(module=folder,files=sum(p.is_file() for p in path.rglob('*')),status='INVENTORIED'))
    write('Existing_Module_Audit.csv',checks)
    audit=read(ROOT/'02_identity_and_evidence/01_systematic_supplement/Known_Source_Recall_Audit.csv')
    for i,row in enumerate(audit,1):
        row.update(recall_id=f'RECALL-{i:04d}',test_scope='REUSED_HISTORICAL_SEARCH_RESULTS',
                   new_strategy_recall_test='PENDING_STAGE2_EXECUTION',
                   eligibility_scope='HISTORICAL_ANCHOR;CHECK_CURRENT_WINDOW_OR_METHOD_REFERENCE')
    write('Known_Study_Recall_Audit.csv',audit)
    criteria=[
        ('S01','Identity','Individually defined compound with resolvable structure/form','RETAIN_IF_DEFINED','MIXTURE_CONTEXT_ONLY'),
        ('S02','Food source','Analytical food occurrence, documented food database entry or traceable culinary ingredient evidence','FOOD_ELIGIBILITY_PENDING_UNTIL_VERIFIED','DRUG_OR_SUPPLEMENT_ONLY_REFERENCE_ROLE'),
        ('S03','Date','First public publication2020-01-01 through2026-11-17','PRIMARY_WINDOW','CHECK_EXTENSION_OR_METHOD_REFERENCE'),
        ('S04','Extension','2016-2019 and predefined endpoint,identity,source-independence or structural-coverage gap','GAP_TRIGGER_RECORDED','OUTSIDE_ACTIVE_WINDOW'),
        ('S05','Originality','Measured experiment attributable to article authors with original figure/table/data','CORE_EXTRACTION_CANDIDATE','SECONDARY_REFERENCE_TRACE'),
        ('S06','Material','Pure standard or isolated defined chemical with documented material identity','CORE_CAPACITY_CANDIDATE','MATRIX_OR_FRACTION_SUPPLEMENTARY_EVIDENCE'),
        ('S07','Endpoint','Chemical capacity,cell function,mechanism or computation assigned distinct level','ENDPOINT_SPECIFIC_EXTRACTION','RELEVANCE_PENDING'),
        ('S08','Access','Full text and required supplement available for field-specific appraisal','RECORD_ACTUAL_SCOPE','FULLTEXT_OR_SUPPLEMENT_PENDING'),
        ('S09','Units','Original value and denominator explicit; conversion reproducible','NORMALIZATION_CHECK','UNIT_HOLD'),
        ('S10','Independence','Version family,experiment cluster and nested observations identified','STUDY_GROUP_CHECK','INDEPENDENCE_HOLD'),
        ('S11','Quality','Identity,method,result completeness,comparability and water applicability assessed separately','QUALITY_PROFILE','QUALITY_FIELDS_PENDING'),
        ('S12','Review','Two independent researcher assessments and adjudication of disagreement','FINAL_DECISION_AFTER_ADJUDICATION','PENDING_HUMAN_REVIEW'),
    ]
    write('Eligibility_and_Screening_Rules.csv',[dict(rule_id=i,domain=d,criterion=c,pass_action=a,unresolved_or_fail_action=f) for i,d,c,a,f in criteria])
    endpoints=[('CHEM01','CHEMICAL','ORAC-FL','Molar net-AUC or calibrated capacity','mol TE/mol','PROBE_VEHICLE_PH_TEMPERATURE_INTEGRATION'),
        ('CHEM02','CHEMICAL','ORAC-PGR','Probe-bleaching response or calibrated capacity','SOURCE_SPECIFIC','PROBE_REACTIVITY_AND_KINETICS'),
        ('CHEM03','CHEMICAL','Crocin bleaching','Time/dose protection or calibrated capacity','SOURCE_SPECIFIC','CROCIN_BASELINE_RADICAL_AND_TIME'),
        ('CHEM04','CHEMICAL','ABTS','Radical decolorization capacity or IC50','SOURCE_SPECIFIC','CAPACITY_AND_IC50_SEPARATE'),
        ('CHEM05','CHEMICAL','DPPH','Radical response,EC50 or capacity','SOURCE_SPECIFIC','SOLVENT_TIME_AND_CONCENTRATION'),
        ('CHEM06','CHEMICAL','FRAP','Ferric reducing response','SOURCE_SPECIFIC','PH_TIME_METAL_CALIBRANT'),
        ('CHEM07','CHEMICAL','CUPRAC','Cupric reducing response','SOURCE_SPECIFIC','LIGAND_PH_TIME_CALIBRANT'),
        ('BIO01','CELL_FUNCTION','CAA,ROS,damage,function','Biological response','SOURCE_SPECIFIC','MODEL_DOSE_TOXICITY_AND_UNIT'),
        ('MEC01','MECHANISM','Binding,localization,expression,perturbation','Evidence-relation-specific finding','SOURCE_SPECIFIC','RELATION_AND_TARGET_CONFIRMATION'),
        ('CMP01','COMPUTATIONAL','Docking,MD,calculation','Predicted interaction or descriptor','SOURCE_SPECIFIC','COMPUTATIONAL_EVIDENCE_ONLY')]
    write('Evidence_Endpoint_Taxonomy.csv',[dict(endpoint_id=i,level=l,assay=a,estimand=e,unit_scope=u,stratification=s) for i,l,a,e,u,s in endpoints])
    identity=[('ID01','Canonical identity','CID,CAS,InChIKey,isomeric structure and formula recorded with database version','Exact form remains separate from parent'),
        ('ID02','Aliases','Canonical names plus verified English/Chinese synonyms,CAS and structure identifiers','Short ambiguous names require context'),
        ('ID03','Stereochemistry','Maintain geometric/absolute stereoisomers and racemates','Unspecified source form retains identity HOLD'),
        ('ID04','Conjugates','Separate glycosides,aglycones,salts,hydrates and oxidation states','Parent mapping remains conditional'),
        ('ID05','Identity sources','PubChem and ChEBI support identity; food records require occurrence provenance','Literature discovery uses bibliographic databases'),
        ('ID06','Missingness','UNKNOWN,NOT_SEARCHED,INACCESSIBLE,NOT_REPORTED,CONFLICT,NOT_APPLICABLE','Empty fields carry missing_reason in subsequent master tables')]
    write('Chemical_Synonym_and_Identity_Rules.csv',[dict(rule_id=i,domain=d,rule=r,interpretation=b) for i,d,r,b in identity])
    assay='(antioxidan* OR ORAC OR "oxygen radical absorbance" OR ABTS OR DPPH OR FRAP OR CUPRAC OR "crocin bleaching" OR "pyrogallol red")'
    food='(food* OR diet* OR edible OR beverage* OR phytochemical* OR "food processing")'
    strategies=[]
    syntax={
        'PubMed/MEDLINE':('PubMed','[Title/Abstract]','("2020/01/01"[Date - Publication] : "2026/11/17"[Date - Publication])'),
        'Europe PMC':('Europe PMC','TITLE_ABS','FIRST_PDATE:[2020-01-01 TO 2026-11-17]'),
        'Web of Science Core Collection':('Institution platform','TS','PY=(2020-2026); manually verify first-online cutoff2026-11-17'),
        'Scopus':('Institution platform','TITLE-ABS-KEY','PUBYEAR > 2019 AND PUBYEAR < 2027; manually verify first-online cutoff'),
        'CNKI':('Advanced search','Subject','2020-01-01 through2026-11-17; record collection and platform filters'),
        'Google Scholar':('Scholar web','Quoted phrases and short Boolean expressions','Custom2020-2026; verify individual publication date'),
    }
    def block(database,terms):
        if database=='PubMed/MEDLINE':return '('+' OR '.join(x.strip()+'[Title/Abstract]' for x in terms.strip('()').split(' OR '))+')'
        if database=='Europe PMC':return 'TITLE_ABS:'+terms
        if database=='Web of Science Core Collection':return 'TS='+terms
        if database=='Scopus':return 'TITLE-ABS-KEY'+terms
        return terms
    for database,(platform,field,date) in syntax.items():
        for route in ['TOPIC_DISCOVERY','COMPOUND_EVIDENCE']:
            terms=food if route=='TOPIC_DISCOVERY' else '("{canonical_name}" OR "{verified_synonym}" OR "{CAS}")'
            query=block(database,terms)+' AND '+block(database,assay)
            if database=='CNKI':query='Subject: (抗氧化 OR 自由基清除 OR 氧自由基吸收能力 OR ORAC OR ABTS OR DPPH OR FRAP OR CUPRAC OR 藏红花素) AND Subject: '+(' (食物 OR 膳食 OR 食品 OR 食源 OR 食用 OR 植物化学物)' if route=='TOPIC_DISCOVERY' else '({Chinese_name} OR {English_name} OR {verified_synonyms} OR {CAS})')
            if database=='Google Scholar':query='"{canonical_name}" "{assay_phrase}"' if route=='COMPOUND_EVIDENCE' else '"food" "{assay_phrase}" antioxidant compound'
            strategies.append(dict(search_id=f'SRCH-{len(strategies)+1:03d}',database=database,platform=platform,route=route,fields=field,query_template=query,date_filter=date,extension_filter='2016-01-01 through2019-12-31 for registered gaps',execution_status='NOT_EXECUTED_STAGE1',translation_status='ADAPT_TO_PLATFORM_AND_TEST_RECALL_STAGE2',logging='Exact expanded query,UTC/local date,hits,exported count,pages,raw file hash,license',coverage='Complete export or explicit partial range; Scholar records actual inspected range'))
    write('Search_Strategy_By_Database.csv',strategies)
    protocol='''# Systematic Review Protocol v1.0

Technical execution version frozen2026-11-17. Researcher adjudication remains pending for the listed decisions. This protocol governs the new six-stage evidence workflow and references the preserved historical analysis modules.

## Research question and population

Identify individually defined food/dietary chemicals through broad discovery, integrate original assay-specific antioxidant evidence, and estimate interpretable candidate priorities for future aqueous absorbance testing. The193 profiles are a historical starting collection. Topic-driven discovery can add compounds following identity and food-occurrence review. Aqueous solubility enters later feasibility appraisal. Panel size follows evidence and feasibility.

Food occurrence requires a traceable analytical publication or a versioned food-composition entry, with food identity,chemical form and source location. FooDB and Phenol-Explorer support occurrence tracing. PubChem and ChEBI support identity. Non-food standards,synthetic controls and mechanism references retain separate roles. Processing products need a defined identity and documented food occurrence. Supplement-only or endogenous-only occurrence requires a reference-role decision.

## Time scope and legacy reuse

The primary first-publication window is2020-01-01 through2026-11-17. The prior retrieval cutoff is2026-11-16. Stage2 must execute and log the one-day update plus revised multi-assay searches. Existing snapshot counts retain their original cutoff. Unknown first-publication dates remain unresolved. Extension2016-01-01 through2019-12-31 requires a logged compound/endpoint gap,missing independent replication,structural coverage gap or missing common comparator. Fewer than20 located relevant leads triggers a coverage investigation; twenty papers is a coverage target. Eligibility and potency depend on the actual experiments. Pre2016 classic original methods are methodology references. Older numerical analyses remain historical diagnostics with their original scope.

## Search and recall validation

Use the dual topic/compound routes in Search_Strategy_By_Database.csv. Resolve aliases through Chemical_Synonym_and_Identity_Rules.csv. Expand each verified alias as a separate quoted term. CAS supports targeted recovery when indexed. Execute assay phrases separately where platform query limits apply. Chinese translations appear in the database query fields while documentation is English. Add backward/forward citations and document provenance. Preserve full queries,dates,hits,exports,limits and raw hashes. Licensed institutional records remain local according to their terms.

Recall audit reuses Known_Source_Recall_Audit.csv. Name-query,class-route and DOI-anchor recovery are separate measures. Before freezing Stage2 execution, test the revised query against in-window known originals spanning assays,chemical classes and naming forms. Record each miss and revise wording or retain an explained miss. A DOI lookup establishes retrieval of that anchor. New-query recall remains pending execution. Historical out-of-window anchors support method/identity testing with separate denominators.

## Screening and adjudication

Use stable record_id,report_id,study_family_id,experiment_id,observation_id and compound_id. Link every database occurrence to its retained report. Duplicate identifiers enter conflict review. Publisher-declared preprint versions share a family key; overlap across reports requires experiment-level checking.

Every deduplicated record receives PENDING,AI_PREDICT_INCLUDE,AI_PREDICT_EXCLUDE,AI_UNCERTAIN,HUMAN_INCLUDE,HUMAN_EXCLUDE or DISAGREEMENT. AI output retains model/rule version,input hash and actual inspected scope. Two independent researcher reviews produce final eligibility; a researcher adjudicates disagreement with reasons. Reviewer names and dates stay blank until actual review. Technical protocol adoption records no scientific approval.

Retrieve full texts and required supplements for eligible/uncertain leads. Record access route,reading scope and source hash. Pure-compound original quantitative studies enter capacity extraction. Mixtures,food matrices,cell/function and mechanism/computation enter their corresponding evidence levels. Secondary numeric claims trigger original-source tracing. Missing access or unclear methods retain PENDING/HOLD.

PRISMA counts separate database hits,exported records,duplicates,unique records screened,reports sought,reports unavailable,full texts assessed,reason-specific exclusions and included studies/reports. Only actual completed transitions enter counts. Use one primary exclusion reason per excluded report plus secondary reasons. Cohorts and version families remain distinct from report counts. Reporting references are PRISMA2020 DOI10.1136/bmj.n71 and PRISMA-S DOI10.1186/s13643-020-01542-z.

## Extraction and analysis gates

Compound→Article→Experiment→Observation links retain original materials,source values,units,mean/error,n hierarchy,protocol,comparators,calculation and locations. Raw AUC,net AUC,capacity,rate and IC50 have distinct endpoint IDs. Maintain original and standardized fields separately. Unit,identity,independence and source conflicts retain HOLD. Quality dimensions cover identity,originality/independence,methods,result completeness,comparability and aqueous applicability. Journal metrics remain dated context variables.

ORAC-FL,ORAC-PGR,crocin,ABTS,DPPH,FRAP and CUPRAC receive method-specific analysis sets. Protocol and material strata govern comparisons. D1–D5 remain available with weights pending validation. First establish simple baselines and study-level validation; structural prediction adds scaffold validation. Existing conditional models retain diagnostic status. Future absorbance validation requires actual equipment-specific data. Stage5 formal input release and Stage6 candidate approval require researcher decisions.

## Execution and handoff

Reproduce Stage1 with `python 02_identity_and_evidence/04_systematic_protocol_v1/code/build_stage1.py`, then run project QC. Existing_Module_Audit.csv and Stage1_Baseline.json document reuse. This module is the technical protocol authority for this task. Legacy00_project/Protocol.md,scope.json and earlier ORAC workflows retain their dated context. Later stages reference this version and log amendments. Stage1 completion is a technical deliverable gate. Stage2 begins after researcher stage review.
'''
    (HERE/'Systematic_Review_Protocol_v1.0.md').write_text(protocol,encoding='utf8')
    decisions='''# Protocol decisions and stage gate

Researcher instructions dated2026-11-17 establish food-derived defined chemicals,multi-assay evidence,three evidence levels,assay-specific synthesis,late feasibility appraisal and evidence-determined panel size. These instructions authorize the technical protocol. Human scientific review fields remain NOT_REVIEWED.

The new window ends2026-11-17. Existing retrieval and source-count snapshots end2026-11-16. Stage2 must bridge this date difference and execute the revised strategies. The existing20-slot queue,ORAC-prioritized diagnostics and historical weights retain historical roles. The new protocol governs subsequent stages. Earlier frozen rankings and governance records retain their original authority.

Pending researcher decisions include reviewer assignment and independent second review,food-occurrence disputes,unusual processing products,eligibility disagreements,quantitative data release,formal model adoption and experimental panel approval. Stage2 requires actual institutional exports or explicit approval of a restricted coverage scope. Scopus access remains to be established. WoS/CNKI access and exports require researcher participation when automated lawful access is unavailable. Search templates require platform syntax and known-study recall testing at Stage2 execution.

The technical extension triggers cover sparse assay evidence,missing independent sources,structural imbalance and common-comparator gaps. Case-specific extensions require a recorded justification. Formal ranking,variance assignment and source-HOLD release remain researcher decisions.
'''
    (HERE/'Protocol_Decision_Register.md').write_text(decisions,encoding='utf8')
    snapshots={}
    for key,relative in [('triage','02_identity_and_evidence/03_date_scoped_review/results/triage_summary.json'),
                         ('queue','02_identity_and_evidence/03_date_scoped_review/results/orac_queue_progress_summary.json'),
                         ('integration','03_candidate_selection/07_all_reference_integration/integration_summary.json')]:
        path=ROOT/relative
        snapshots[key]=dict(path=relative,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),data=json.loads(path.read_bytes()))
    (HERE/'Stage1_Baseline.json').write_text(json.dumps(dict(protocol_cutoff=CUTOFF,existing_retrieval_cutoff='2026-11-16',snapshots=snapshots),indent=2)+'\n',encoding='utf8')
    assert len(strategies)==12 and len(criteria)==12 and len(endpoints)==10
    (HERE/'Stage1_QC_Report.md').write_text(f'''# Stage1 QC

Technical protocol gate PASS. Researcher scientific decisions remain pending. Eight required modules inventoried. Twelve database/route templates cover six bibliographic platforms. Twelve screening rules,ten endpoint categories and six identity rules generated. {len(audit)} prior candidate–DOI recall anchors retain separate route-specific outcomes. New strategy recall testing remains scheduled for Stage2.

The2026-11-17 protocol cutoff and prior2026-11-16 snapshot cutoff are explicitly distinct. Baseline values and source hashes are recorded in Stage1_Baseline.json. Extraction remains compound/article/experiment/observation linked. Original observations,frozen assets and scientific approval states are preserved. Stage2 retrieval has not started in this stage. Reproduction uses code/build_stage1.py followed by the project QC script.
''',encoding='utf8')
    write('Screening_Decision_Dictionary.csv',[dict(code=code,meaning=meaning,decision_authority=authority) for code,meaning,authority in [
        ('PENDING','Assessment outstanding','SYSTEM_STATE'),('AI_PREDICT_INCLUDE','Assistive inclusion prediction','AI_ONLY'),
        ('AI_PREDICT_EXCLUDE','Assistive exclusion prediction','AI_ONLY'),('AI_UNCERTAIN','Assistive uncertainty','AI_ONLY'),
        ('HUMAN_INCLUDE','Inclusion after documented researcher review','RESEARCHER'),
        ('HUMAN_EXCLUDE','Exclusion after documented researcher review','RESEARCHER'),
        ('DISAGREEMENT','Independent reviews differ','RESEARCHER_ADJUDICATION'),
        ('E01','Outside applicable date window','RESEARCHER'),('E02','Identity or material outside review scope','RESEARCHER'),
        ('E03','Secondary report lacking eligible original experiment','RESEARCHER'),
        ('E04','Endpoint outside relevant evidence levels','RESEARCHER'),
        ('E05','Duplicate report represented by retained study/version','RESEARCHER'),
        ('ACCESS_PENDING','Report sought but access unresolved','SYSTEM_STATE'),
        ('HOLD','Required identity/unit/source/independence field unresolved','SCIENTIFIC_REVIEW_PENDING')]])
    with (HERE/'Fulltext_Review_Template.csv').open('w',encoding='utf8',newline='') as handle:
        csv.writer(handle).writerow(['report_id','study_family_id','doi','source_file','source_sha256','reading_scope','reviewer1','review1_date','review1_decision','reviewer2','review2_date','review2_decision','adjudicator','adjudication_date','final_decision','primary_exclusion_reason','secondary_reasons','originality','material_type','evidence_level','endpoint_ids','supplement_status','human_review_status','change_applied'])
    dictionary=[]
    for path in sorted(HERE.glob('*.csv')):
        if path.name=='Field_Dictionary.csv':continue
        with path.open(encoding='utf-8-sig',newline='') as handle:fields=next(csv.reader(handle))
        for field in fields:
            dictionary.append(dict(table=path.name,field=field,meaning=field.replace('_',' '),missing_value_rule='Blank means unavailable or pending; consult status and next_action',provenance='Stage1 curated rule,template or explicitly cited existing registry'))
    with (HERE/'Field_Dictionary.csv').open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(dictionary[0]),lineterminator='\n');writer.writeheader();writer.writerows(dictionary)
    print('Stage1 technical protocol QC PASS; scientific decisions and Stage2 execution remain pending.')

if __name__=='__main__':main()
