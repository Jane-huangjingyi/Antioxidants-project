"""Audit existing evidence for molar-capacity modelling; never fit or approve a model."""
from pathlib import Path
import sys,collections,re,math
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
HERE=Path(__file__).resolve().parent
master=source('data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv')
error_path=source('data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv')
ind_path=source('data/h_orac_stage25b/stage25b6d/Stage25B6D_Study_Independence_Adjudication.csv')
errors={r['experiment_id']:r for r in read_csv(error_path)}
ind={r['experiment_id']:r for r in read_csv(ind_path)}
def numeric(x):
 try:
  n=float(str(x).strip());return n if math.isfinite(n) else None
 except (ValueError,TypeError):return None
def positive(x):
 n=numeric(x);return n is not None and n>0
observations=[]
for r in read_csv(master):
 key=r['independent_experiment_id'];e=errors.get(key,{});i=ind.get(key,{})
 observations.append({'candidate_id':r['candidate_id'],'compound':r['canonical_name'],'observation_id':key,'doi':r['DOI'],'value_as_reported':r['raw_reported_value'],'unit_as_reported':r['raw_unit'],'molar_value_in_existing_table':r['converted_value_mol_TE_per_mol'],'assay':r['assay_name_reported'],'probe':r['probe'],'pH_as_reported':r['pH'],'temperature_as_reported':r['temperature'],'time_as_reported':r['incubation_time'],'concentration_as_reported':r['sample_concentration'],'cosolvent_as_reported':r['cosolvent'],'replicate_N_as_reported':e.get('replicate_N',r['replicate_N']),'replicate_type':e.get('replicate_type','NOT_IN_LATER_AUDIT'),'error_type':e.get('error_type_verified','NOT_IN_LATER_AUDIT'),'error_value_as_reported':e.get('error_value',''),'error_scale':e.get('error_scale','NOT_IN_LATER_AUDIT'),'error_conversion_status':e.get('conversion_validity','NOT_IN_LATER_AUDIT'),'source_independence_status':i.get('independence_decision','NOT_IN_LATER_AUDIT'),'source_location':'; '.join(r.get(k,'') for k in ['source_page','source_table','source_figure']),'source_file':master.relative_to(ROOT).as_posix(),'later_error_audit':error_path.relative_to(ROOT).as_posix() if e else ''})
# These source rows were outside the canonical closure, rather than evidence of inactivity.
vc=source('data/class_specific_antioxidant/VitaminC_Aqueous_Evidence_Master.csv')
for r in read_csv(vc):
 observations.append({'candidate_id':'AFF-0104','compound':r['compound'],'observation_id':r['evidence_id'],'doi':r['DOI'],'value_as_reported':r['original_value'],'unit_as_reported':r['original_unit'],'molar_value_in_existing_table':r['normalized_value'],'assay':r['assay'],'probe':'fluorescein','pH_as_reported':r['pH'],'temperature_as_reported':r['temperature'],'time_as_reported':'NOT_EXTRACTED_AT_RECORD_LEVEL','concentration_as_reported':r['concentration_range'],'cosolvent_as_reported':r['solvent'],'replicate_N_as_reported':'NOT_EXTRACTED_AT_RECORD_LEVEL','replicate_type':'NOT_EXTRACTED_AT_RECORD_LEVEL','error_type':'NOT_EXTRACTED_AT_RECORD_LEVEL','error_value_as_reported':'','error_scale':'NOT_VERIFIED','error_conversion_status':'NOT_VERIFIED','source_independence_status':'OUTSIDE_CURRENT_CLOSURE_REQUIRES_SOURCE_REVIEW','source_location':r['exact_location'],'source_file':vc.relative_to(ROOT).as_posix(),'later_error_audit':''})
assert len({(r['candidate_id'],r['observation_id']) for r in observations})==len(observations)
for r in observations:
 gaps=[]
 if not positive(r['molar_value_in_existing_table']):gaps.append('MOLAR_VALUE_UNRESOLVED')
 if r['source_independence_status']!='ONE_VERIFIED_ORIGINAL_STUDY_CONTRIBUTION':gaps.append('ORIGINAL_SOURCE_AND_INDEPENDENCE_NOT_CLOSED')
 if not positive(r['error_value_as_reported']):gaps.append('NO_USABLE_POSITIVE_NUMERIC_ERROR')
 if 'SD_VERIFIED' not in r['error_type'] and 'SE_VERIFIED' not in r['error_type']:gaps.append('ERROR_TYPE_NOT_VERIFIED')
 if not positive(r['replicate_N_as_reported']):gaps.append('REPLICATE_N_NOT_EXTRACTED_AS_NUMBER')
 if r['replicate_type'] in {'REPLICATE_TYPE_UNCLEAR','TECHNICAL_OR_RUN_TYPE_UNRESOLVED','NOT_IN_LATER_AUDIT','NOT_EXTRACTED_AT_RECORD_LEVEL'}:gaps.append('REPLICATION_UNIT_UNRESOLVED')
 gaps.append('COMMON_EFFECT_SCALE_AND_TARGET_CONDITIONS_REQUIRE_REVIEW')
 r['capacity_value_present']='YES' if positive(r['molar_value_in_existing_table']) else 'NO'
 r['numeric_N_present']='YES' if positive(r['replicate_N_as_reported']) else 'NO'
 r['numeric_error_present']='YES' if positive(r['error_value_as_reported']) else 'NO'
 r['modelling_gaps']='; '.join(gaps);r['model_use_status']='NOT_APPROVED_FOR_INVERSE_VARIANCE_MODEL'
 r['human_review_status']='NOT_REVIEWED';r['change_applied']='NO'
out=HERE/'results';write_csv(out/'Observation_Readiness.csv',observations)
profiles=read_csv(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv');coverage=[]
for p in profiles:
 rows=[r for r in observations if r['candidate_id']==p['candidate_id']]
 coverage.append({'candidate_id':p['candidate_id'],'compound':p['compound_name'],'existing_observation_count':len(rows),'distinct_DOI_count_not_independent_study_count':len({r['doi'] for r in rows if r['doi']}),'positive_molar_value_rows':sum(r['capacity_value_present']=='YES' for r in rows),'typed_SD_rows':sum('SD_VERIFIED' in r['error_type'] for r in rows),'coverage_status':'SOURCE_ROWS_PRESENT_REVIEW_REQUIRED' if rows else 'NO_ROWS_IN_THIS_EXTRACTION_NOT_EVIDENCE_OF_INACTIVITY','next_action':'VERIFY_ORIGINAL_SOURCE_AND_ERROR_SCALE' if rows else 'TARGETED_EVIDENCE_RETRIEVAL_REQUIRED','human_review_status':'NOT_REVIEWED'})
write_csv(out/'Candidate_Capacity_Coverage.csv',coverage)
summary={'status':'AUDIT_COMPLETE_MODEL_NOT_FITTED','candidate_count':len(profiles),'observation_count':len(observations),'candidates_with_rows':sum(r['existing_observation_count']>0 for r in coverage),'later_error_audit_rows':len(errors),'later_audit_typed_SD_rows':sum('SD_VERIFIED' in r['error_type_verified'] for r in errors.values()),'rows_with_positive_numeric_N':sum(r['numeric_N_present']=='YES' for r in observations),'rows_with_positive_numeric_error':sum(r['numeric_error_present']=='YES' for r in observations),'vitamin_C_source_rows':sum(r['candidate_id']=='AFF-0104' for r in observations),'approved_model_rows':0,'input_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in [master,error_path,ind_path,vc]}}
write_json(out/'readiness_summary.json',summary)
print({k:v for k,v in summary.items() if k!='input_sha256'})
