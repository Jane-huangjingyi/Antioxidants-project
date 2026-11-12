"""Compare held-out reference capacities on their original molar scale."""
from pathlib import Path
import csv,json,math,statistics,collections
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def read(path):
 with path.open(encoding='utf8',newline='') as handle:return list(csv.DictReader(handle))
def run():
 tests=read(HERE/'results/Heldout_Model_Comparison.csv');errors=collections.defaultdict(list)
 for r in tests:
  observed=math.exp(float(r['observed_log']))
  values={'ARITHMETIC_SOURCE_MEAN':float(r['arithmetic_baseline']),'GEOMETRIC_SOURCE_MEAN':math.exp(float(r['baseline'])),'OLS_LOG_LOCATION':math.exp(float(r['OLS'])),'OLS_TRAINING_RESIDUAL_SMEARING':math.exp(float(r['OLS']))*float(r['OLS_smearing_factor'])}
  for model,value in values.items():errors[model].append(value-observed)
 metrics={model:dict(MAE=statistics.mean(abs(v) for v in values),RMSE=math.sqrt(statistics.mean(v*v for v in values)),heldout_rows=len(values)) for model,values in errors.items()}
 references=read(ROOT/'03_candidate_selection/03_preliminary_literature_selection/results/Paper_Specific_Reference_Order.csv')
 model=read(ROOT/'03_candidate_selection/04_first_evidence_model/results/Candidate_Diagnostic_Estimates.csv')
 profiles={r['candidate_id']:r for r in read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')}
 groups=collections.defaultdict(list)
 for r in references:groups[r['candidate_id']].append(float(r['paper_reference_median']))
 rows=[]
 for r in model:
  values=groups[r['candidate_id']]
  rows.append(dict(candidate_id=r['candidate_id'],compound=profiles[r['candidate_id']]['compound_name'],reference_formula=profiles[r['candidate_id']]['molecular_formula'],source_DOI_count=len(values),arithmetic_source_mean=statistics.mean(values),geometric_source_mean=math.exp(statistics.mean(math.log(v) for v in values)),OLS_component_order=r['within_component_diagnostic_order'],interpretation='EXPLORATORY_CROSS_PROTOCOL_REFERENCE_CAPACITY',human_review_status='NOT_REVIEWED',change_applied='NO'))
 for r in rows:r['arithmetic_reference_component_order']=1+sum(x['arithmetic_source_mean']>r['arithmetic_source_mean'] for x in rows)
 rows.sort(key=lambda r:(r['arithmetic_reference_component_order'],r['candidate_id']))
 with (HERE/'results/Capacity_Scale_Order_Comparison.csv').open('w',encoding='utf8',newline='') as handle:
  writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 (HERE/'results/capacity_scale_validation.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf8',newline='\n')
 print(json.dumps(metrics));print('First five reference means:',[r['compound'] for r in rows[:5]])
if __name__=='__main__':run()
