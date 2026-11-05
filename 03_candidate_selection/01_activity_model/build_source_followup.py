"""Traceable source follow-up and conditional linear conversion; no model fitting."""
from pathlib import Path
import sys,math
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
HERE=Path(__file__).resolve().parent
resolution=read_json(HERE/'inputs/source_resolution.json');paired=read_json(HERE/'inputs/paired_assay_evidence.json')
audit=read_csv(HERE/'results/Observation_Readiness.csv');byid={r['observation_id']:r for r in audit}
rows=[];converted=[]
for r in resolution['records']:
 assert r['observation_id'] in byid and r['doi']==byid[r['observation_id']]['doi']
 rows.append({'observation_id':r['observation_id'],'doi':r['doi'],'access_status':r['access_status'],'source_url':r['url'],'source_locator':r['locator'],'remaining_issue':r['remaining_issue'],'human_review_status':'NOT_REVIEWED','change_applied':'NO'})
 if 'raw_mean' not in r:continue
 # g TE / 100 g compound -> mol TE / mol compound. SD follows same linear factor.
 factor=r['compound_MW_g_mol']/(100*r['Trolox_MW_g_mol']) if r['unit']=='g Trolox per 100 g dry compound' else 1.0
 assert r['unit'] in {'g Trolox per 100 g dry compound','umol TE per umol compound'}
 mean=r['raw_mean']*factor;sd=r['raw_SD']*factor
 assert factor>0 and sd>0 and math.isclose(sd/mean,r['raw_SD']/r['raw_mean'],rel_tol=1e-12)
 converted.append({'observation_id':r['observation_id'],'raw_mean':r['raw_mean'],'raw_SD':r['raw_SD'],'original_unit':r['unit'],'compound_MW_g_mol':r.get('compound_MW_g_mol',''),'Trolox_MW_g_mol':r.get('Trolox_MW_g_mol',''),'linear_factor':factor,'derived_molar_mean':mean,'derived_molar_SD':sd,'derived_unit':'mol TE/mol compound','reported_determinations':r['determinations'],'replication_interpretation':r['replication_interpretation'],'variance_of_mean':'NOT_AUTOMATICALLY_ASSIGNED','model_status':'CONVERSION_CANDIDATE_NOT_MODEL_APPROVAL','source_url':r['url'],'human_review_status':'NOT_REVIEWED','change_applied':'NO'})
write_csv(HERE/'results/Targeted_Source_Followup.csv',rows)
write_csv(HERE/'results/Conditional_Unit_Conversion.csv',converted)
pairs=[]
for p in paired['pairs']:
 pairs.append(dict(p,reported_index_ratio_PGR_over_FL=p['PGR_index']/p['FL_index'],quantity=paired['reported_quantity'],plus_minus_type=paired['plus_minus_type'],doi=paired['doi'],source_url=paired['url'],calibration_status=paired['calibration_status'],human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(pairs)==3 and len({p['doi'] for p in pairs})==1
write_csv(HERE/'results/Paired_Assay_Source_Candidates.csv',pairs)
fl_order=[p['compound'] for p in sorted(pairs,key=lambda p:p['FL_index'],reverse=True)]
pgr_order=[p['compound'] for p in sorted(pairs,key=lambda p:p['PGR_index'],reverse=True)]
model_rows=[];recovered_path=HERE/'inputs/recovered_capacity_rows.json'
if recovered_path.exists():
 recovered=read_json(recovered_path)['records']
 for r in recovered:
  explicit_sd=r['error_type'].startswith('SD_EXPLICIT');n=r['independent_experiments_as_reported'];sd=r['reported_plus_minus'] if explicit_sd else ''
  model_rows.append({'candidate_id':r['candidate_id'],'compound':r['compound'],'doi':r['doi'],'source_observation_id':r['source_observation_id'],'molar_mean_candidate':r['reported_mean'],'molar_SD_candidate':sd,'reported_plus_minus':r['reported_plus_minus'],'reported_error_scale':'Molar Trolox-equivalent slope ratio','error_type':r['error_type'],'independent_experiments_as_reported':n or '','variance_of_mean_candidate':sd**2/n if explicit_sd and n else '', 'variance_assumptions':'Author-declared independent experiments; shared-calibration covariance unknown' if explicit_sd else 'No variance assigned; plus/minus definition and effective n unresolved','vehicle':r['vehicle'],'source_form':r['source_form'],'row_relationship':r['row_relationship'],'source_url':r['source_url'],'model_status':'SOURCE_VERIFIED_CANDIDATE_NOT_FORMAL_APPROVAL','human_review_status':'NOT_REVIEWED','change_applied':'NO'})
 for r in converted:
  if any(x['source_observation_id']==r['observation_id'] for x in model_rows):continue
  old=byid[r['observation_id']]
  model_rows.append({'candidate_id':old['candidate_id'],'compound':old['compound'],'doi':old['doi'],'source_observation_id':r['observation_id'],'molar_mean_candidate':r['derived_molar_mean'],'molar_SD_candidate':r['derived_molar_SD'],'reported_plus_minus':r['raw_SD'],'reported_error_scale':r['original_unit'],'error_type':'SD_ORIGINAL_TABLE_LINEAR_CONVERSION','independent_experiments_as_reported':'','variance_of_mean_candidate':'','variance_assumptions':'Three determinations; independence not established','vehicle':'Methanol dilution; final fraction unresolved','source_form':'Exact material form and purity require review','row_relationship':'RECHECK_OF_EXISTING_OBSERVATION_NOT_NEW_STUDY','source_url':r['source_url'],'model_status':'SOURCE_VERIFIED_CANDIDATE_NOT_FORMAL_APPROVAL','human_review_status':'NOT_REVIEWED','change_applied':'NO'})
 assert len({(r['candidate_id'],r['doi']) for r in model_rows})==len(model_rows)
 write_csv(HERE/'results/Model_Input_Candidates.csv',model_rows)
write_json(HERE/'results/source_followup_summary.json',{'status':'SOURCE_FOLLOWUP_COMPLETE_NO_MODEL_FITTED','priority_observations':len(rows),'original_numeric_SD_rows_rechecked':len(converted),'conditional_unit_conversions_or_identity_factors':len(converted),'recovered_model_input_candidates':len(model_rows),'conditional_sampling_variances':sum(r['variance_of_mean_candidate']!='' for r in model_rows),'paired_parent_compounds':len(pairs),'paired_independent_papers':1,'FL_reported_index_order':fl_order,'PGR_reported_index_order':pgr_order,'same_order':fl_order==pgr_order,'approved_calibration_rows':0,'new_model_or_top20_created':False})
print(f'Follow-up: {len(rows)} priority observations, {len(converted)} checked SD rows, {len(model_rows)} model-input candidates; no fitted ranking.')
