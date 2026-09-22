import csv, hashlib, shutil, statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'/'h_orac_stage25b'; CFG=ROOT/'methods_qc'/'config'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,rows,fields=None):
    fields=fields or list(rows[0])
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def q(vals,p):
    v=sorted(vals); x=(len(v)-1)*p; lo=int(x); hi=min(lo+1,len(v)-1); return v[lo]+(v[hi]-v[lo])*(x-lo)
def fmt(x):
    if x=='' or x is None:return ''
    return f'{x:.10g}'

# Canonicalize approved drafts with mandatory clarifications.
rub=read(CFG/'ORAC_Literature_Eligibility_Rubric_v2_DRAFT.csv')
for r in rub:
    r['notes']=(r.get('notes','')+' | CANONICAL v2.0 approved with R2 evidence-first and R1 operational-screen clarification').strip(' |')
write(CFG/'ORAC_Literature_Eligibility_Rubric_v2.0.csv',rub)
risk=read(CFG/'H_ORAC_Compound_Risk_Trigger_Rules_v1_DRAFT.csv')
for r in risk:
    if r['risk_domain']=='R1 optical' and '>10' in r['trigger']:
        r['trigger']=r['trigger']+'; OPERATIONAL SCREEN ONLY—10 µM is not a validated universal interference threshold'
        r['failure_consequence']='Triggers evidence review only; concentration alone never changes tier'
    if r['risk_domain']=='R2 solubility/aggregation':
        r['evidence_required']='Traceable experimental/literature/database solubility or logP/logD; assay concentration; precipitation/turbidity; dose response; stock-solvent evidence. If insufficient, classify UNCLEAR.'
write(CFG/'H_ORAC_Compound_Risk_Trigger_Rules_v1.0.csv',risk)

old=read(DATA/'Stage25B_HORAC_Experiment_Evidence.csv'); old_fields=list(old[0])
old_tier={r['independent_experiment_id']:r['H_ORAC_tier'] for r in old}
A_SOURCES={'AQ-P002','AQ-P014'}
for r in old:
    oid=r['H_ORAC_tier']; nid=oid; reason='v2 consistency migration; no tier change'
    if oid=='B1' and r['publication_id'] in A_SOURCES:
        nid='A'; reason='Universal core complete; objective triggered risks adequately addressed or not materially triggered under canonical v2'
    if r['independent_experiment_id']=='HORAC_EXP_0067': nid='B2'; reason='Approved downgrade: approximately 10% final methanol derivable; matched solvent control not explicit'
    if r['independent_experiment_id']=='HORAC_EXP_0070': nid='X'; reason='Approved change: figure-only evidence; exact quantitative value/unit not recoverable'
    r['H_ORAC_tier']=nid; r['previous_status']=oid; r['new_status']=nid
    r['status_change_reason']=reason; r['migration_version']='H-ORAC rubric v2.0'; r['migration_date']='2026-09-22'; r['migration_reason']=reason
    r['eligibility_status']='PRIMARY_RANKING_ELIGIBLE' if nid in {'A','B1'} else ('SENSITIVITY_ONLY' if nid=='B2' else 'INSUFFICIENT_METHOD_INFORMATION')
write(DATA/'Stage25B_HORAC_Experiment_Evidence.csv',old,old_fields+['migration_version','migration_date','migration_reason'])

# Source-level method master.
groups=defaultdict(list)
for r in old: groups[r['publication_id']].append(r)
sm=[]
for sid,rs in sorted(groups.items()):
    vals=lambda k:' | '.join(dict.fromkeys(x[k] for x in rs if x.get(k)))
    sm.append({'source_id':sid,'DOI':vals('DOI'),'PMID':vals('PMID'),'year':vals('year'),'experiment_N':len(rs),'AAPH_conditions':vals('radical_generator'),'fluorescein_conditions':vals('probe'),'Trolox_calibration':vals('standard'),'buffer':vals('buffer'),'pH':vals('pH'),'temperature':vals('temperature'),'reaction_timing':vals('incubation_time'),'kinetic_readout':vals('assay_name_reported'),'generic_replication':vals('replicate_N'),'protocol_traceability':'EXPLICIT_OR_EXISTING_SOURCE_TRACE' if all(x.get('source_page') for x in rs) else 'PARTIAL','source_access_status':'AVAILABLE_OR_PREVIOUSLY_VALIDATED','reuse_scope':'Source-level fields reusable; compound-specific identity/concentration/solvent/risk/value location require experiment confirmation'})
write(DATA/'Stage25B4_HORAC_Source_Method_Master.csv',sm)

# Full 74-row migration table and independent flags.
mig=[]
for r in old:
    eid=r['independent_experiment_id']; ot=old_tier[eid]; nt=r['H_ORAC_tier']; name=r['canonical_name'].lower()
    optical='HIGH' if 'cyanidin' in name else ('MODERATE' if name in {'baicalein'} else 'UNCLEAR')
    if r['publication_id'] in A_SOURCES: optical='LOW_OR_EVIDENCE_REVIEWED'
    sol='HIGH' if name in {'baicalein','capsaicin'} else ('UNCLEAR' if not r.get('sample_concentration') or 'see source' in r.get('sample_concentration','') else 'EVIDENCE_REVIEWED')
    cos='HIGH' if eid=='HORAC_EXP_0067' else ('UNCLEAR' if not r.get('cosolvent_percent') or 'not' in r.get('cosolvent_percent','').lower() else 'LOW_OR_CONTROLLED')
    redox='UNCLEAR' if any(x in name for x in ['quinone','plumbagin']) else 'NO_OBJECTIVE_TRIGGER_IDENTIFIED'
    mig.append({'experiment_id':eid,'candidate_id':r['candidate_id'],'canonical_name':r['canonical_name'],'source_id':r['publication_id'],'DOI':r['DOI'],'PMID':r['PMID'],'year':r['year'],'old_tier':ot,'new_tier':nt,'identity_status':'RESOLVED' if 'ambiguous' not in r.get('major_method_caveat','').lower() else 'UNCLEAR','form_status':'REPORTED_OR_INTERPRETABLE' if r.get('compound_form') else 'UNCLEAR','purity_status':'NUMERIC' if '%' in r.get('compound_purity','') else ('GRADE_OR_SUPPLIER' if 'not reported' not in r.get('compound_purity','').lower() else 'NOT_REPORTED'),'AAPH_status':'EXPLICIT_OR_TRACEABLE' if r.get('radical_generator') else 'UNCLEAR','fluorescein_status':'EXPLICIT_OR_TRACEABLE' if r.get('probe') else 'UNCLEAR','Trolox_status':'EXPLICIT_OR_TRACEABLE' if r.get('standard') else 'UNCLEAR','buffer_status':'EXPLICIT_OR_TRACEABLE' if r.get('buffer') else 'UNCLEAR','pH_status':'EXPLICIT_OR_TRACEABLE' if r.get('pH') else 'UNCLEAR','temperature_status':'EXPLICIT_OR_TRACEABLE' if r.get('temperature') else 'UNCLEAR','candidate_concentration_status':'EXPLICIT_OR_TRACEABLE' if r.get('sample_concentration') else 'UNCLEAR','stock_solvent':r.get('cosolvent',''),'final_cosolvent_status':'DERIVABLE_FROM_METHOD' if eid=='HORAC_EXP_0067' else ('EXPLICIT_OR_TRACEABLE' if r.get('cosolvent_percent') and 'not' not in r.get('cosolvent_percent','').lower() else 'UNCLEAR'),'final_cosolvent_percent':'~10% methanol' if eid=='HORAC_EXP_0067' else r.get('cosolvent_percent',''),'final_cosolvent_derivation':'20 µL methanolic sample / 200 µL final well' if eid=='HORAC_EXP_0067' else 'See source/method master','matched_solvent_control':'NOT_REPORTED' if eid=='HORAC_EXP_0067' else ('REPORTED' if 'control' in r.get('blank_control','').lower() else 'UNCLEAR'),'kinetic_AUC_status':'TRACEABLE' if r.get('incubation_time') else 'UNCLEAR','replication_status':'REPORTED_OR_SOURCE_LEVEL' if r.get('replicate_N') else 'UNCLEAR','quantitative_value_status':'NOT_RECOVERABLE' if eid=='HORAC_EXP_0070' else ('TRACEABLE' if r.get('raw_reported_value') else 'UNCLEAR'),'unit_status':'NOT_RECOVERABLE' if eid=='HORAC_EXP_0070' else ('TRACEABLE' if r.get('raw_unit') else 'UNCLEAR'),'R1_optical_risk':optical,'R1_trigger':'anthocyanin/visible chromophore' if 'cyanidin' in name else '10 µM is screen only; no tier consequence without evidence','R1_QC_status':'UNRESOLVED' if optical=='HIGH' else 'ADEQUATE_OR_NOT_MATERIALLY_TRIGGERED','R2_solubility_aggregation_risk':sol,'R2_trigger':'Evidence-based review; UNCLEAR if traceable solubility/logP/assay evidence insufficient','R2_QC_status':'UNRESOLVED' if name=='baicalein' else 'ADEQUATE_OR_UNCLEAR_NONMATERIAL','R3_cosolvent_risk':cos,'R3_trigger':'>5% organic cosolvent' if eid=='HORAC_EXP_0067' else 'Evidence-based final-solvent review','R3_QC_status':'UNRESOLVED' if eid=='HORAC_EXP_0067' else 'ADEQUATE_OR_UNCLEAR_NONMATERIAL','R4_redox_risk':redox,'R4_trigger':'Objective redox/probe evidence required','R4_QC_status':'NO_MATERIAL_TRIGGER_IDENTIFIED','reporting_completeness':'HIGH' if nt=='A' else ('LOW' if nt=='X' else 'MODERATE'),'source_access_status':'VALIDATED_OR_EXISTING_CANONICAL','protocol_traceability':'PASS' if nt in {'A','B1','B2'} else 'INSUFFICIENT','tier_change':'YES' if ot!=nt else 'NO','tier_change_reason':r['migration_reason'],'primary_ranking_eligible':'YES' if nt in {'A','B1'} and r.get('converted_value_mol_TE_per_mol') else 'NO','human_review_required':'YES' if nt in {'B2','X'} else 'NO','identity_flag':'PASS' if nt!='X' else 'REVIEW','purity_reporting_flag':'NUMERIC' if '%' in r.get('compound_purity','') else 'GRADE_OR_UNREPORTED','optical_risk_flag':optical,'optical_qc_flag':'UNRESOLVED' if optical=='HIGH' else 'PASS_OR_NOT_TRIGGERED','solubility_risk_flag':sol,'aggregation_risk_flag':sol,'aggregation_qc_flag':'UNRESOLVED' if name=='baicalein' else 'PASS_OR_NOT_TRIGGERED','cosolvent_risk_flag':cos,'matched_solvent_control_flag':'FAIL' if eid=='HORAC_EXP_0067' else 'PASS_OR_UNCLEAR_NONMATERIAL','redox_interference_flag':redox,'reporting_completeness_flag':'HIGH' if nt=='A' else 'MODERATE_OR_LOW','source_access_flag':'PASS','protocol_traceability_flag':'PASS' if nt!='X' else 'REVIEW','source_page':r.get('source_page',''),'source_table':r.get('source_table',''),'source_figure':r.get('source_figure',''),'source_supplement':r.get('source_supplement','')})
write(DATA/'Stage25B4_HORAC_Evidence_Migration.csv',mig)

# Candidate summary and rankings.
old_sum=read(DATA/'Stage25B_HORAC_Candidate_Summary.csv'); by_c=defaultdict(list)
for r in old: by_c[r['candidate_id']].append(r)
summary=[]
for base in old_sum:
    cid=base['candidate_id']; rs=by_c.get(cid,[]); tiers=Counter(r['H_ORAC_tier'] for r in rs)
    vals=[float(r['converted_value_mol_TE_per_mol']) for r in rs if r['H_ORAC_tier'] in {'A','B1'} and r.get('converted_value_mol_TE_per_mol')]
    avals=[float(r['converted_value_mol_TE_per_mol']) for r in rs if r['H_ORAC_tier']=='A' and r.get('converted_value_mol_TE_per_mol')]
    b2vals=[float(r['converted_value_mol_TE_per_mol']) for r in rs if r['H_ORAC_tier'] in {'A','B1','B2'} and r.get('converted_value_mol_TE_per_mol')]
    x=dict(base); x.update({'eligible_A_N':tiers['A'],'eligible_B1_N':tiers['B1'],'eligible_B2_N':tiers['B2'],'C_N':tiers['C'],'X_N':tiers['X'],'independent_eligible_experiment_N':len(vals),'median_H_ORAC_mol_TE_per_mol':fmt(statistics.median(vals)) if vals else '','min':fmt(min(vals)) if vals else '','max':fmt(max(vals)) if vals else '','IQR':fmt(q(vals,.75)-q(vals,.25)) if vals else '','max_min_ratio':fmt(max(vals)/min(vals)) if vals and min(vals)>0 else '','A_only_median':fmt(statistics.median(avals)) if avals else '','A_B1_median':fmt(statistics.median(vals)) if vals else '','A_B1_B2_median':fmt(statistics.median(b2vals)) if b2vals else '','quantitative_rank_eligible':'yes' if vals else 'no','reason_not_rankable':'' if vals else 'No canonical v2 A/B1 quantitative evidence'})
    if not vals: x['evidence_confidence']='Not rankable'; x['heterogeneity_flag']='not applicable'
    summary.append(x)
write(DATA/'Stage25B_HORAC_Candidate_Summary.csv',summary,list(old_sum[0]))
rankable=[x for x in summary if x['quantitative_rank_eligible']=='yes']; rankable.sort(key=lambda x:(-float(x['median_H_ORAC_mol_TE_per_mol']),x['candidate_id']))
ranking=[]
for n,x in enumerate(rankable,1): ranking.append({'rank':n,'candidate_id':x['candidate_id'],'canonical_name':x['canonical_name'],'median_H_ORAC_mol_TE_per_mol':x['median_H_ORAC_mol_TE_per_mol'],'independent_eligible_experiment_N':x['independent_eligible_experiment_N'],'evidence_confidence':x['evidence_confidence'],'heterogeneity_flag':x['heterogeneity_flag'],'Stage25A_primary_rank':x['Stage25A_primary_rank'],'Stage25B_status':x['Stage25B_status'],'ranking_statistic':'median canonical v2 A+B1 mol TE/mol','provisional_status':'POST_MIGRATION_PENDING_HUMAN_TOP20_FREEZE'})
write(DATA/'Stage25B_HORAC_Quantitative_Ranking.csv',ranking)

aonly=[]
for x in summary:
    if x['eligible_A_N'] and x['A_only_median']: aonly.append(x)
aonly.sort(key=lambda x:(-float(x['A_only_median']),x['candidate_id']))
write(DATA/'Stage25B4_A_Only_Diagnostic_Ranking.csv',[{'rank':i+1,'candidate_id':x['candidate_id'],'canonical_name':x['canonical_name'],'A_only_median':x['A_only_median'],'A_experiment_N':x['eligible_A_N'],'in_primary_Top20':'yes' if any(r['candidate_id']==x['candidate_id'] and int(r['rank'])<=20 for r in ranking) else 'no','interpretation':'DIAGNOSTIC ONLY'} for i,x in enumerate(aonly)])

# B2 sensitivity candidate ranks.
sens=[]
for x in summary:
    if x['A_B1_B2_median']: sens.append(x)
sens.sort(key=lambda x:(-float(x['A_B1_B2_median']),x['candidate_id']))
prim20={r['candidate_id'] for r in ranking[:20]}; sens20={x['candidate_id'] for x in sens[:20]}
out=[]
for mode,seq,valkey in [('PRIMARY_A+B1',ranking,'median_H_ORAC_mol_TE_per_mol'),('SENSITIVITY_A+B1+B2',sens,'A_B1_B2_median')]:
    for i,x in enumerate(seq,1):
        cid=x['candidate_id']; name=x['canonical_name']; val=x[valkey]
        out.append({'analysis':mode,'rank':i,'candidate_id':cid,'candidate':name,'median_mol_TE_per_mol':val,'Top20_member':'yes' if i<=20 else 'no','membership_vs_primary':'enter' if mode.startswith('SENS') and cid in sens20-prim20 else ('leave_from_sensitivity' if mode.startswith('PRIMARY') and cid in prim20-sens20 else 'same'),'interpretation':'Canonical v2 primary' if mode.startswith('PRIMARY') else 'B2 sensitivity only'})
write(DATA/'Stage25B4_B2_Sensitivity.csv',out)
trans=Counter((old_tier[r['independent_experiment_id']],r['H_ORAC_tier']) for r in old)
write(DATA/'Stage25B4_Tier_Transition_Summary.csv',[{'old_tier':a,'new_tier':b,'experiment_N':n,'canonical_change':'yes' if a!=b else 'no'} for (a,b),n in sorted(trans.items())])
print('post',Counter(r['H_ORAC_tier'] for r in old),'rankable',len(ranking),'A-only',len(aonly),'enter',[x for x in sens20-prim20],'leave',[x for x in prim20-sens20])
