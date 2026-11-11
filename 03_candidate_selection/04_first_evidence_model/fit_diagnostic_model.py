"""Exploratory additive candidate/paper model with estimability-aware validation."""
from pathlib import Path
import csv,json,sys,math,hashlib,collections
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.runtime_chem'))
import numpy as np
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'03_candidate_selection/03_preliminary_literature_selection/results/Paper_Specific_Reference_Order.csv'
def write(name,rows):
 with (HERE/'results'/name).open('w',encoding='utf8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
def run():
 with SOURCE.open(encoding='utf8') as f:rows=list(csv.DictReader(f))
 graph=collections.defaultdict(set)
 for row in rows:
  c='C:'+row['candidate_id'];p='P:'+row['doi'];graph[c].add(p);graph[p].add(c)
 components=[];seen=set()
 for node in sorted(graph):
  if node in seen:continue
  queue=[node];component=set()
  while queue:
   current=queue.pop()
   if current in component:continue
   component.add(current);queue.extend(graph[current]-component)
  seen|=component;components.append(component)
 components.sort(key=lambda c:(-sum(n.startswith('C:') for n in c),sorted(c)))
 cids=sorted(node[2:] for node in components[0] if node.startswith('C:'))
 papers=sorted(node[2:] for node in components[0] if node.startswith('P:'))
 data=[r for r in rows if r['candidate_id'] in cids]
 assert all(float(r['paper_reference_median'])>0 for r in data)
 def design(items,study=True,active_papers=None):
  active_papers=papers if active_papers is None else active_papers
  matrix=np.zeros((len(items),len(cids)+(len(active_papers)-1 if study else 0)))
  for i,row in enumerate(items):
   matrix[i,cids.index(row['candidate_id'])]=1
   if study:
    j=active_papers.index(row['doi'])
    if j==len(active_papers)-1:matrix[i,len(cids):]=-1
    else:matrix[i,len(cids)+j]=1
  return matrix
 X=design(data);y=np.log([float(r['paper_reference_median']) for r in data])
 rank=int(np.linalg.matrix_rank(X));assert rank==X.shape[1]
 coefficients=np.linalg.lstsq(X,y,rcond=None)[0];residual=y-X@coefficients
 predictions=[];folds=[]
 for paper in papers:
  train=np.array([r['doi']!=paper for r in data]);test=np.where(~train)[0]
  # Unseen paper effect cannot be identified. Evaluate candidate location with study effect set to zero.
  training=design([data[i] for i in np.where(train)[0]],active_papers=[p for p in papers if p!=paper]);beta=np.linalg.lstsq(training,y[train],rcond=None)[0];projection=np.linalg.pinv(training)@training
  B=design(data,False);base_beta=np.linalg.lstsq(B[train],y[train],rcond=None)[0]
  candidate_seen={data[i]['candidate_id'] for i in np.where(train)[0]}
  count=0
  for i in test:
   target=np.zeros(training.shape[1]);target[cids.index(data[i]['candidate_id'])]=1
   estimable=np.linalg.norm(target-target@projection)<1e-8
   # Training-only paper centering assumes a new paper has mean-zero effect.
   if estimable:count+=1
   baseline=float(B[i]@base_beta) if data[i]['candidate_id'] in candidate_seen else None
   predictions.append(dict(candidate_id=data[i]['candidate_id'],heldout_doi=paper,observed_log_capacity=float(y[i]),candidate_location_estimable='YES' if estimable else 'NO',adjusted_prediction=float(target@beta) if estimable else '',candidate_mean_baseline=baseline if baseline is not None else '',interpretation='PAPER_SHIFT_TARGET_UNOBSERVED_PROTOCOL_EFFECT'))
  folds.append(dict(heldout_doi=paper,test_rows=len(test),estimable_candidate_locations=count,training_rank=int(np.linalg.matrix_rank(training)),training_parameters=training.shape[1]))
 estimates=[];values=coefficients[:len(cids)]
 for i,candidate in enumerate(cids):
  estimates.append(dict(candidate_id=candidate,component=1,diagnostic_log_location=float(values[i]),exponentiated_log_location=float(np.exp(values[i])),within_component_diagnostic_order=1+sum(values>values[i]),source_DOI_count=sum(r['candidate_id']==candidate for r in data),uncertainty_status='NOT_ESTIMATED_WITHOUT_JUSTIFIED_ERROR_AND_INDEPENDENCE_MODEL',interpretation='EXPLORATORY_CROSS_PROTOCOL_LOG_LOCATION_CONDITIONAL_ON_ADDITIVE_PAPER_MODEL',human_review_status='NOT_REVIEWED',change_applied='NO'))
 out=HERE/'results';out.mkdir(exist_ok=True)
 write('Candidate_Diagnostic_Estimates.csv',estimates);write('Leave_Paper_Out_Diagnostics.csv',predictions);write('Paper_Fold_Identifiability.csv',folds)
 write('Component_Coverage.csv',[dict(candidate_id=node[2:],component=i+1,model_estimate_available='YES' if i==0 else 'NO') for i,component in enumerate(components) for node in sorted(component) if node.startswith('C:')])
 eligible=[r for r in predictions if r['candidate_location_estimable']=='YES' and r['candidate_mean_baseline']!='']
 metrics={}
 if eligible:
  for label,field in [('adjusted','adjusted_prediction'),('baseline','candidate_mean_baseline')]:
   errors=np.array([float(r[field])-r['observed_log_capacity'] for r in eligible]);metrics[label]={'MAE':float(np.mean(abs(errors))),'RMSE':float(np.sqrt(np.mean(errors**2)))}
 summary={'status':'FIRST_EXPLORATORY_FIT_PROTOCOL_AND_QUALITY_ALIGNMENT_PENDING','input_candidate_paper_rows':len(rows),'components':[{'candidates':sum(n.startswith('C:') for n in c),'papers':sum(n.startswith('P:') for n in c)} for c in components],'fitted_candidates':len(cids),'fitted_papers':len(papers),'fitted_rows':len(data),'design_rank':rank,'parameters':X.shape[1],'residual_degrees_freedom':len(data)-rank,'training_RMSE_log':float(np.sqrt(np.mean(residual**2))),'strictly_estimable_heldout_rows':len(eligible),'heldout_metrics':metrics,'global_ranking_supported':False,'quality_adjustment_fitted':False,'formal_absorbance_model_fitted':False,'input_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (out/'model_diagnostics.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(summary))
if __name__=='__main__':run()
