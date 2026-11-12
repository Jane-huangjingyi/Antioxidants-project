"""Evaluate within-heldout-paper ordering on matched candidate predictions."""
from pathlib import Path
import csv,json,itertools,collections,math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def run():
 rows=read(HERE/'results/Heldout_Model_Comparison.csv');groups=collections.defaultdict(list)
 for row in rows:groups[row['heldout_doi']].append(row)
 output=[]
 for doi,items in groups.items():
  pairs=[(a,b) for a,b in itertools.combinations(items,2) if a['candidate_id']!=b['candidate_id'] and abs(float(a['observed_log'])-float(b['observed_log']))>1e-8]
  if not pairs:continue
  for model in ['baseline','OLS','Huber','PAPER_SHRINK_1','PAPER_SHRINK_10']:
   correct=0;ties=0;difference_errors=[]
   for a,b in pairs:
    observed=float(a['observed_log'])-float(b['observed_log']);predicted=float(a[model])-float(b[model])
    difference_errors.append(predicted-observed)
    if abs(predicted)<=1e-8:ties+=1
    elif observed*predicted>0:correct+=1
   output.append(dict(heldout_doi=doi,model=model,comparable_pairs=len(pairs),correct_direction=correct,predicted_ties=ties,direction_accuracy=correct/len(pairs),log_ratio_MAE=sum(abs(v) for v in difference_errors)/len(pairs),log_ratio_RMSE=math.sqrt(sum(v*v for v in difference_errors)/len(pairs))))
 with (HERE/'results/Heldout_Relative_Order.csv').open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(output[0]),lineterminator='\n');w.writeheader();w.writerows(output)
 summary={}
 for model in ['baseline','OLS','Huber','PAPER_SHRINK_1','PAPER_SHRINK_10']:
  selected=[r for r in output if r['model']==model]
  summary[model]={'papers_with_pairs':len(selected),'dependent_pairs':sum(r['comparable_pairs'] for r in selected),'pooled_log_ratio_MAE':sum(r['log_ratio_MAE']*r['comparable_pairs'] for r in selected)/sum(r['comparable_pairs'] for r in selected),'pooled_log_ratio_RMSE':math.sqrt(sum(r['log_ratio_RMSE']**2*r['comparable_pairs'] for r in selected)/sum(r['comparable_pairs'] for r in selected)),'pooled_direction_accuracy':sum(r['correct_direction'] for r in selected)/sum(r['comparable_pairs'] for r in selected),'mean_paper_direction_accuracy':sum(r['direction_accuracy'] for r in selected)/len(selected)}
 (HERE/'results/relative_order_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n')
 profiles=read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')
 estimates={r['candidate_id']:r for r in read(HERE/'results/Candidate_Model_Sensitivity.csv')}
 partial={r['candidate_id']:r for r in read(HERE/'results/Candidate_Partial_Order.csv')}
 coverage={r['candidate_id']:r for r in read(ROOT/'03_candidate_selection/04_first_evidence_model/results/Component_Coverage.csv')}
 joined=[]
 for row in profiles:
  candidate=row['candidate_id'];m=estimates.get(candidate,{});p=partial.get(candidate,{});c=coverage.get(candidate,{})
  joined.append(dict(candidate_id=candidate,compound=row['compound_name'],reference_formula=row['molecular_formula'],reference_CID=row['pubchem_cid'],component=c.get('component',''),model_coverage='FITTED_COMPONENT' if m else 'OTHER_COMPONENT' if c else 'NO_MODEL_REFERENCE',OLS_component_order=m.get('OLS_component_order',''),Huber_component_order=m.get('Huber_component_order',''),source_DOI_count=m.get('source_DOI_count',''),partial_order_best=p.get('partial_order_best_position',''),partial_order_worst=p.get('partial_order_worst_position',''),source_omission_estimable_scenarios=m.get('omission_estimable_scenarios',''),source_omission_total_scenarios=m.get('omission_total_scenarios',''),global_rank='',human_review_status='NOT_REVIEWED',change_applied='NO'))
 assert len(joined)==193
 with (HERE/'results/Model_Ranking_Review.csv').open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(joined[0]),lineterminator='\n');w.writeheader();w.writerows(joined)
 print(json.dumps(summary))
if __name__=='__main__':run()
