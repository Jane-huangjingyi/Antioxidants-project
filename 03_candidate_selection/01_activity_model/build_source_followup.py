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
 factor=r['compound_MW_g_mol']/(100*r['Trolox_MW_g_mol'])
 mean=r['raw_mean']*factor;sd=r['raw_SD']*factor
 assert factor>0 and sd>0 and math.isclose(sd/mean,r['raw_SD']/r['raw_mean'],rel_tol=1e-12)
 converted.append({'observation_id':r['observation_id'],'raw_mean':r['raw_mean'],'raw_SD':r['raw_SD'],'original_unit':r['unit'],'compound_MW_g_mol':r['compound_MW_g_mol'],'Trolox_MW_g_mol':r['Trolox_MW_g_mol'],'linear_factor':factor,'derived_molar_mean':mean,'derived_molar_SD':sd,'derived_unit':'mol TE/mol compound','reported_determinations':r['determinations'],'replication_interpretation':r['replication_interpretation'],'variance_of_mean':'NOT_ASSIGNED_PENDING_REPLICATION_REVIEW','model_status':'CONVERSION_CANDIDATE_NOT_MODEL_APPROVAL','source_url':r['url'],'human_review_status':'NOT_REVIEWED','change_applied':'NO'})
write_csv(HERE/'results/Targeted_Source_Followup.csv',rows)
write_csv(HERE/'results/Conditional_Unit_Conversion.csv',converted)
pairs=[]
for p in paired['pairs']:
 pairs.append(dict(p,reported_index_ratio_PGR_over_FL=p['PGR_index']/p['FL_index'],quantity=paired['reported_quantity'],plus_minus_type=paired['plus_minus_type'],doi=paired['doi'],source_url=paired['url'],calibration_status=paired['calibration_status'],human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(pairs)==3 and len({p['doi'] for p in pairs})==1
write_csv(HERE/'results/Paired_Assay_Source_Candidates.csv',pairs)
fl_order=[p['compound'] for p in sorted(pairs,key=lambda p:p['FL_index'],reverse=True)]
pgr_order=[p['compound'] for p in sorted(pairs,key=lambda p:p['PGR_index'],reverse=True)]
write_json(HERE/'results/source_followup_summary.json',{'status':'SOURCE_FOLLOWUP_COMPLETE_NO_MODEL_FITTED','priority_observations':len(rows),'original_numeric_SD_rows_rechecked':len(converted),'conditional_linear_conversions':len(converted),'paired_parent_compounds':len(pairs),'paired_independent_papers':1,'FL_reported_index_order':fl_order,'PGR_reported_index_order':pgr_order,'same_order':fl_order==pgr_order,'approved_calibration_rows':0,'new_model_or_top20_created':False})
print('Follow-up: 6 priority observations, 1 checked SD conversion, 3 paired parent indices; no calibration or ranking fitted.')
