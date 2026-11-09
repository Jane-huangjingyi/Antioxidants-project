"""Separate original numeric verification, normalization and common-target eligibility."""
import csv, json, math, hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
specs={
 'ishimoto':('EXPLICIT_MOLAR_TE','Explicit molar ratio; development summary/material match pending','No numeric SD recovered','Development source stereo match pending','SOURCE_NAMED_STEREO_DEVELOPMENT_FORM_PENDING','RESEARCHER_AUTHORIZED_RETROSPECTIVE_PRESSURE_TEST'),
 'rothe':('MOLAR_NORMALIZATION_PENDING','Need pure-compound concentration denominator and normalization formula','Need pure-compound plus/minus definition; beer SD not transferable','Need hydrate concentration basis and epicatechin reagent identity','HYDRATE_OR_INDIVIDUAL_FORM_PENDING','HOLD_NORMALIZATION'),
 'carvalho':('MOLAR_SLOPE_RATIO_TRACED','Molar slope ratio traced; hydrate concentration basis pending','Ratio uncertainty and effective n unresolved','Dihydrate concentration basis and development-material match pending','DIHYDRATE_CONCENTRATION_BASIS_PENDING','HOLD_MATERIAL_AND_ESTIMAND'),
 'froldi':('EXPLICIT_MOLAR_TE','Explicit molar capacity; estimator detail pending','SEM known; row-specific n unknown; no SD conversion','Source standard reported; development-material match pending','SOURCE_STANDARD_MATCH_PENDING','HOLD_PROTOCOL_AND_ESTIMAND'),
 'paillat':('CONDITIONAL_PARENT_MW_CONVERSION','Conditional molar conversion; actual material form/purity basis pending','Microplate n/error not stated; online RSD/n not transferable','Verify actual material molecular weight and assay mass basis','PARENT_REFERENCE_ONLY_NOT_LOT_IDENTITY','HOLD_MICROPLATE_PROTOCOL_AND_MATERIAL')}
rows=[];conversions=[]
for stem,(gate,norm,error,material,mgate,challenge) in specs.items():
 c=json.loads((P/'inputs'/f'{stem}_external_source_check.json').read_text(encoding='utf-8'))
 for r in c['records']:
  conditional=''
  if stem=='carvalho':
   assert abs(r['auc_compound_slope']/r['auc_matched_trolox_slope']-r['mean'])<.01
   assert abs(r['auc_compound_slope']/r['wrong_buffer_trolox_slope']-r['mean'])>1
  if stem=='paillat':
   raw=P/'inputs/source_recovery/raw'/r['reference_cache_file']
   ref=json.loads(raw.read_text(encoding='utf-8'))['PropertyTable']['Properties'][0]
   assert ref['CID']==r['reference_CID'] and float(ref['MolecularWeight'])==r['parent_MW_g_mol']
   conditional=r['mean']*r['parent_MW_g_mol']/1e6
   conversions.append(dict(candidate_id=r['candidate_id'],doi=c['doi'],raw_value=r['mean'],raw_unit=r['unit'],reference_CID=r['reference_CID'],parent_MW_g_mol=r['parent_MW_g_mol'],reference_cache_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),formula='raw_umol_TE_per_g * reference_g_per_mol / 1000000',conditional_mol_TE_per_mol=conditional,interpretation='REFERENCE_PARENT_BASIS_ONLY_NOT_SOURCE_MOLAR_MEASUREMENT',numeric_SD='',external_label_released='NO',human_review_status='NOT_REVIEWED',change_applied='NO'))
  log=math.log(r['mean']) if gate in {'EXPLICIT_MOLAR_TE','MOLAR_SLOPE_RATIO_TRACED'} else ''
  rows.append(dict(candidate_id=r['candidate_id'],source_name=r['source_name'],doi=c['doi'],source_url=c['source_url'],source_locator=r['locator'],original_value=r['mean'],original_summary_statistic=r.get('summary_statistic','SOURCE_REPORTED_MEAN'),reported_plus_minus=r.get('reported_plus_minus',''),reported_error_type=r.get('error_type','NOT_DEFINED_OR_NOT_NUMERICALLY_RECOVERED'),replication_scope=c['protocol']['replication'],normalization_requirement=norm,error_requirement=error,material_requirement=material,reported_unit=r['unit'],unit_gate=gate,conditional_mol_TE_per_mol=conditional,ln_original_molar_summary_candidate=log,log_interpretation='Log source summary; not mean logged replicates' if log!='' else '',numeric_SD='',weighting_status='NO_VARIANCE_WEIGHT',material_gate=mgate,protocol_gate='SOURCE_PROTOCOL_AND_ESTIMATOR_MATCH_UNRESOLVED',common_target_validation='HOLD',shifted_condition_challenge=challenge,split_exposure='RETROSPECTIVE_PREVIOUSLY_ACCESSIBLE_NOT_BLIND',model_tuning_allowed='NO',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==8 and len(conversions)==2
assert all(r['common_target_validation']=='HOLD' and r['model_tuning_allowed']=='NO' for r in rows)
for filename,data in [('External_Comparability_Decisions.csv',rows),('Source_Normalization_Audit.csv',conversions)]:
 with (P/'results'/filename).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
print('QC PASS: eight source values; two conditional parent-mass conversions; zero test-label releases.')
