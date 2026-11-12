"""OLS/Huber comparison and positive paper-weight sensitivity under fixed design."""
from pathlib import Path
import csv,json,sys,collections,hashlib
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'.runtime_chem'))
import numpy as np
HERE=Path(__file__).resolve().parent
def read(p):
 with p.open(encoding='utf8') as f:return list(csv.DictReader(f))
def fit(X,y,robust=False,weights=None):
 w=np.ones(len(y)) if weights is None else weights.copy();beta=np.linalg.lstsq(X*np.sqrt(w[:,None]),y*np.sqrt(w),rcond=None)[0]
 if robust:
  for _ in range(100):
   residual=y-X@beta;scale=1.4826*np.median(abs(residual-np.median(residual)))
   if scale<1e-10:break
   rw=np.minimum(1,1.345*scale/np.maximum(abs(residual),1e-15));updated=np.linalg.lstsq(X*np.sqrt(rw[:,None]),y*np.sqrt(rw),rcond=None)[0]
   if np.max(abs(updated-beta))<1e-8:beta=updated;break
   beta=updated
 return beta

def fit_shrunk_paper_effects(X,y,candidate_count,strength):
 paper_count=X.shape[1]-candidate_count
 penalty=np.zeros((paper_count,X.shape[1]))
 penalty[:,candidate_count:]=np.linalg.cholesky(np.eye(paper_count)+np.ones((paper_count,paper_count))).T
 return np.linalg.lstsq(np.vstack([X,np.sqrt(strength)*penalty]),np.concatenate([y,np.zeros(paper_count)]),rcond=None)[0]

def run():
 source=ROOT/'03_candidate_selection/03_preliminary_literature_selection/results/Paper_Specific_Reference_Order.csv'
 estimates=read(ROOT/'03_candidate_selection/04_first_evidence_model/results/Candidate_Diagnostic_Estimates.csv');cids=sorted(r['candidate_id'] for r in estimates)
 rows=[r for r in read(source) if r['candidate_id'] in cids];papers=sorted({r['doi'] for r in rows});y=np.log([float(r['paper_reference_median']) for r in rows])
 def design(items,active):
  X=np.zeros((len(items),len(cids)+len(active)-1))
  for i,row in enumerate(items):
   X[i,cids.index(row['candidate_id'])]=1;j=active.index(row['doi'])
   if j==len(active)-1:X[i,len(cids):]=-1
   else:X[i,len(cids)+j]=1
  return X
 X=design(rows,papers);ols=fit(X,y);huber=fit(X,y,True)
 full_shrink1=fit_shrunk_paper_effects(X,y,len(cids),1.0)
 full_shrink10=fit_shrunk_paper_effects(X,y,len(cids),10.0)
 predictions=[]
 omission_records=[]
 pair_records=[]
 for omitted in papers:
  train=np.array([r['doi']!=omitted for r in rows]);active=[p for p in papers if p!=omitted];T=design([r for r in rows if r['doi']!=omitted],active);projection=np.linalg.pinv(T)@T
  beta=fit(T,y[train]);robust=fit(T,y[train],True)
  shrunk1=fit_shrunk_paper_effects(T,y[train],len(cids),1.0)
  shrunk10=fit_shrunk_paper_effects(T,y[train],len(cids),10.0)
  for left in range(len(cids)):
   for right in range(left+1,len(cids)):
    contrast=np.zeros(T.shape[1]);contrast[left]=1;contrast[right]=-1
    estimable=np.linalg.norm(contrast-contrast@projection)<1e-8
    pair_records.append(dict(candidate_left=cids[left],candidate_right=cids[right],omitted_doi=omitted,contrast_estimable='YES' if estimable else 'NO',log_capacity_difference=float(contrast@beta) if estimable else ''))
  locations={}
  for index,candidate in enumerate(cids):
   contrast=np.zeros(T.shape[1]);contrast[index]=1
   if np.linalg.norm(contrast-contrast@projection)<1e-8:locations[candidate]=float(contrast@beta)
  for candidate in cids:
   if candidate in locations:
    lower=1+sum(value>locations[candidate] for value in locations.values())
    upper=lower+len(cids)-len(locations)
   else:lower,upper=1,len(cids)
   omission_records.append(dict(candidate_id=candidate,omitted_doi=omitted,location_estimable='YES' if candidate in locations else 'NO',fixed_universe_best_order=lower,fixed_universe_worst_order=upper))
  for i,row in enumerate(rows):
   if train[i]:continue
   target=np.zeros(T.shape[1]);target[cids.index(row['candidate_id'])]=1
   if np.linalg.norm(target-target@projection)>1e-8:continue
   baseline=np.mean([y[j] for j,r in enumerate(rows) if train[j] and r['candidate_id']==row['candidate_id']])
   arithmetic_baseline=float(np.mean([np.exp(y[j]) for j,r in enumerate(rows) if train[j] and r['candidate_id']==row['candidate_id']]))
   smear=float(np.mean(np.exp(y[train]-T@beta)))
   predictions.append(dict(PAPER_SHRINK_1=float(target@shrunk1),PAPER_SHRINK_10=float(target@shrunk10),arithmetic_baseline=arithmetic_baseline,OLS_smearing_factor=smear,candidate_id=row['candidate_id'],heldout_doi=omitted,observed_log=float(y[i]),baseline=float(baseline),OLS=float(target@beta),Huber=float(target@robust)))
 rng=np.random.default_rng(20261111);draws=[]
 for _ in range(300):
  pw=rng.exponential(size=len(papers));weights=np.array([pw[papers.index(r['doi'])] for r in rows]);draws.append(fit(X,y,weights=weights)[:len(cids)])
 draws=np.array(draws);ranks=np.array([[1+sum(v>value) for value in v] for v in draws]);results=[]
 for i,candidate in enumerate(cids):
  q=np.quantile(draws[:,i],[.025,.975]);rq=np.quantile(ranks[:,i],[.025,.975])
  candidate_omissions=[r for r in omission_records if r['candidate_id']==candidate]
  results.append(dict(shrink1_component_order=1+sum(full_shrink1[:len(cids)]>full_shrink1[i]),shrink10_component_order=1+sum(full_shrink10[:len(cids)]>full_shrink10[i]),shrink1_log_location=float(full_shrink1[i]),shrink10_log_location=float(full_shrink10[i]),source_DOI_count=sum(r['candidate_id']==candidate for r in rows),omission_estimable_scenarios=sum(r['location_estimable']=='YES' for r in candidate_omissions),omission_total_scenarios=len(papers),omission_best_possible_order=min(r['fixed_universe_best_order'] for r in candidate_omissions),omission_worst_possible_order=max(r['fixed_universe_worst_order'] for r in candidate_omissions),candidate_id=candidate,OLS_log_location=float(ols[i]),Huber_log_location=float(huber[i]),OLS_component_order=1+sum(ols[:len(cids)]>ols[i]),Huber_component_order=1+sum(huber[:len(cids)]>huber[i]),paper_weight_log_q025=float(q[0]),paper_weight_log_q975=float(q[1]),paper_weight_order_q025=float(rq[0]),paper_weight_order_q975=float(rq[1]),interpretation='CONDITIONAL_PAPER_WEIGHT_SENSITIVITY_QUANTILES',human_review_status='NOT_REVIEWED',change_applied='NO'))
 metrics={}
 for name in ['baseline','OLS','Huber','PAPER_SHRINK_1','PAPER_SHRINK_10']:
  errors=np.array([r[name]-r['observed_log'] for r in predictions]);metrics[name]={'MAE':float(np.mean(abs(errors))),'RMSE':float(np.sqrt(np.mean(errors**2)))}
 pair_summary=[]
 for left in range(len(cids)):
  for right in range(left+1,len(cids)):
   records=[r for r in pair_records if r['candidate_left']==cids[left] and r['candidate_right']==cids[right]]
   differences=[float(r['log_capacity_difference']) for r in records if r['contrast_estimable']=='YES']
   pair_summary.append(dict(candidate_left=cids[left],candidate_right=cids[right],baseline_log_difference=float(ols[left]-ols[right]),estimable_omission_scenarios=len(differences),total_omission_scenarios=len(papers),minimum_estimable_difference=min(differences) if differences else '',maximum_estimable_difference=max(differences) if differences else '',stable_direction_all_scenarios='YES' if len(differences)==len(papers) and (min(differences)>1e-8 and ols[left]>ols[right] or max(differences)<-1e-8 and ols[left]<ols[right]) else 'NO',interpretation='MODEL_CONDITIONAL_SOURCE_REMOVAL_PAIRWISE_SENSITIVITY'))
 partial=[]
 for candidate in cids:
  higher=0;lower=0
  for pair in pair_summary:
   if pair['stable_direction_all_scenarios']!='YES':continue
   left=pair['candidate_left'];right=pair['candidate_right']
   winner=left if pair['baseline_log_difference']>0 else right
   loser=right if winner==left else left
   if candidate==winner:lower+=1
   if candidate==loser:higher+=1
  partial.append(dict(candidate_id=candidate,baseline_component_order=1+sum(ols[:len(cids)]>ols[cids.index(candidate)]),stable_higher_candidates=higher,stable_lower_candidates=lower,partial_order_best_position=1+higher,partial_order_worst_position=len(cids)-lower,interpretation='DIRECT_STABLE_PAIRWISE_CONSTRAINT_BOUNDS_CONDITIONAL_ON_MODEL',human_review_status='NOT_REVIEWED',change_applied='NO'))
 out=HERE/'results';out.mkdir(exist_ok=True)
 for name,data in [('Candidate_Model_Sensitivity.csv',results),('Heldout_Model_Comparison.csv',predictions),('Model_Source_Omission.csv',omission_records),('Pairwise_Source_Omission.csv',pair_records),('Pairwise_Order_Summary.csv',pair_summary),('Candidate_Partial_Order.csv',partial)]:
  with (out/name).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
 summary={'scope':'EXPLORATORY_EXISTING_COMPONENT_MODEL_ROBUSTNESS','candidates':len(cids),'papers':len(papers),'matched_heldout_rows':len(predictions),'metrics':metrics,'candidate_pairs':len(pair_summary),'pairs_estimable_in_every_omission':sum(r['estimable_omission_scenarios']==len(papers) for r in pair_summary),'pairs_stable_direction_every_omission':sum(r['stable_direction_all_scenarios']=='YES' for r in pair_summary),'weight_perturbations':300,'random_seed':20261111,'quantile_interpretation':'SENSITIVITY_TO_POSITIVE_PAPER_WEIGHTS_CONDITIONAL_ON_OBSERVED_DESIGN','clinical_or_sampling_CI_estimated':False,'Top20_probability_estimated':False,'quality_adjustment_fitted':False,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (out/'robustness_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(summary))
if __name__=='__main__':run()
