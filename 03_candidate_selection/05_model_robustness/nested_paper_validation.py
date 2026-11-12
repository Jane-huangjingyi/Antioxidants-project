"""Nested paper-held-out selection among baseline and two paper-ridge strengths."""
from pathlib import Path
import csv,json,math,collections
from compare_models import ROOT,HERE,read,fit_shrunk_paper_effects,np
OPTIONS=['BASELINE','SHRINK_1','SHRINK_10']
def predict(train,test,cids,option):
 papers=sorted({r['doi'] for r in train})
 X=np.zeros((len(train),len(cids)+len(papers)-1));y=np.log([float(r['paper_reference_median']) for r in train])
 for i,row in enumerate(train):
  X[i,cids.index(row['candidate_id'])]=1;j=papers.index(row['doi'])
  if j==len(papers)-1:X[i,len(cids):]=-1
  else:X[i,len(cids)+j]=1
 projection=np.linalg.pinv(X)@X
 beta=None if option=='BASELINE' else fit_shrunk_paper_effects(X,y,len(cids),1 if option=='SHRINK_1' else 10)
 output=[]
 for row in test:
  target=np.zeros(X.shape[1]);target[cids.index(row['candidate_id'])]=1
  if np.linalg.norm(target-target@projection)>1e-8:continue
  value=np.mean([y[i] for i,r in enumerate(train) if r['candidate_id']==row['candidate_id']]) if beta is None else target@beta
  output.append((row,float(value)))
 return output

def select(train,cids):
 scores={}
 for option in OPTIONS:
  errors=[]
  for doi in sorted({r['doi'] for r in train}):
   inner_train=[r for r in train if r['doi']!=doi];inner_test=[r for r in train if r['doi']==doi]
   for row,value in predict(inner_train,inner_test,cids,option):errors.append((value-math.log(float(row['paper_reference_median'])))**2)
  scores[option]=sum(errors)/len(errors) if errors else None
 if any(v is None for v in scores.values()):return 'BASELINE',scores
 return min(OPTIONS,key=lambda name:scores[name]),scores

def run():
 cids=sorted(r['candidate_id'] for r in read(ROOT/'03_candidate_selection/04_first_evidence_model/results/Candidate_Diagnostic_Estimates.csv'))
 source=ROOT/'03_candidate_selection/03_preliminary_literature_selection/results/Paper_Specific_Reference_Order.csv'
 rows=[r for r in read(source) if r['candidate_id'] in cids];predictions=[];folds=[]
 for doi in sorted({r['doi'] for r in rows}):
  train=[r for r in rows if r['doi']!=doi];test=[r for r in rows if r['doi']==doi]
  chosen,scores=select(train,cids)
  matched={r['candidate_id']:v for r,v in predict(train,test,cids,'BASELINE')}
  for row,value in predict(train,test,cids,chosen):predictions.append(dict(heldout_doi=doi,candidate_id=row['candidate_id'],observed_log=math.log(float(row['paper_reference_median'])),prediction=value,baseline=matched[row['candidate_id']],selected_model=chosen))
  folds.append(dict(inner_selection_status='BASELINE_FALLBACK_NO_INNER_ESTIMABLE_ROWS' if scores['BASELINE'] is None else 'INNER_CV_SELECTED',heldout_doi=doi,selected_model=chosen,inner_baseline_MSE=scores['BASELINE'],inner_shrink1_MSE=scores['SHRINK_1'],inner_shrink10_MSE=scores['SHRINK_10']))
 metrics={}
 for label in ['prediction','baseline']:
  errors=[r[label]-r['observed_log'] for r in predictions];metrics[label]={'MAE':sum(abs(v) for v in errors)/len(errors),'RMSE':math.sqrt(sum(v*v for v in errors)/len(errors))}
 chosen,scores=select(rows,cids)
 sensitivity=read(HERE/'results/Candidate_Model_Sensitivity.csv')
 profiles={r['candidate_id']:r for r in read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')}
 selected=[]
 for r in sensitivity:
  candidate=r['candidate_id']
  if chosen=='BASELINE':location=float(np.mean([math.log(float(x['paper_reference_median'])) for x in rows if x['candidate_id']==candidate]))
  else:location=float(r['shrink1_log_location' if chosen=='SHRINK_1' else 'shrink10_log_location'])
  selected.append(dict(candidate_id=candidate,compound=profiles[candidate]['compound_name'],selected_model=chosen,selected_log_location=location,source_DOI_count=r['source_DOI_count'],interpretation='EXPLORATORY_COMPONENT_ORDER_FULL_DATA_INNER_SELECTION',human_review_status='NOT_REVIEWED',change_applied='NO'))
 for r in selected:r['selected_component_order']=1+sum(x['selected_log_location']>r['selected_log_location'] for x in selected)
 selected.sort(key=lambda r:(r['selected_component_order'],r['candidate_id']))
 for name,data in [('Nested_Paper_Predictions.csv',predictions),('Nested_Paper_Selections.csv',folds),('Selected_Model_Component_Order.csv',selected)]:
  with (HERE/'results'/name).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
 summary={'scope':'EXPLORATORY_NESTED_PAPER_SELECTION_PREVIOUSLY_INSPECTED_DATA','options':OPTIONS,'inner_objective':'POOLED_LOG_CAPACITY_MSE_ON_COMMON_ESTIMABLE_ROWS','outer_rows':len(predictions),'outer_folds':len(folds),'metrics':metrics,'outer_selection_counts':dict(collections.Counter(r['selected_model'] for r in folds)),'full_data_selection':chosen,'full_data_inner_scores':scores,'independent_confirmation':False}
 (HERE/'results/nested_validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(summary))
if __name__=='__main__':run()
