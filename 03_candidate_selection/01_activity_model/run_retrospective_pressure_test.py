"""Two-observation shifted-protocol diagnostic, explicitly not independent validation."""
import sys,csv,json,hashlib,math
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'.runtime_chem'))
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
def read(n):
    with (P/'results'/n).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
labels=read('Flavonoid_Log_Capacity_Extraction.csv');structures={r['source_row']:r for r in read('Flavonoid_Structure_Audit.csv')};groups={r['source_row']:r['provisional_scaffold_group'] for r in read('Flavonoid_Scaffold_Groups.csv')}
fp=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=1024,includeChirality=False)
X=np.array([fp.GetFingerprintAsNumPy(Chem.MolFromSmiles(structures[r['source_row']]['candidate_isomeric_SMILES'])) for r in labels],dtype=float);y=np.array([float(r['reported_ln_orac']) for r in labels]);g=np.array([groups[r['source_row']] for r in labels])
def fit_predict(tr,te,alpha):
    mu=X[tr].mean(0);sd=X[tr].std(0);sd[sd==0]=1
    a=(X[tr]-mu)/sd;b=(X[te]-mu)/sd;ym=y[tr].mean()
    coef=a.T@np.linalg.solve(a@a.T+alpha*np.eye(len(tr)),y[tr]-ym)
    return b@coef+ym
scores={}
for alpha in [.1,1.,10.,100.]:
    e=[]
    for held in sorted(set(g)):
        tr=np.where(g!=held)[0];te=np.where(g==held)[0];e.extend((fit_predict(tr,te,alpha)-y[te])**2)
    scores[alpha]=float(np.mean(e))
alpha=min(scores,key=lambda a:(scores[a],a));allrows=np.arange(len(y));pred=fit_predict(allrows,allrows,alpha)
# External source means are read only after all fitting and penalty selection.
source=json.loads((P/'inputs/ishimoto_external_source_check.json').read_text());rows=[]
for r in source['records']:
    name={'AFF-0001':'Catechin','AFF-0002':'Epicatechin'}[r['candidate_id']];i=next(i for i,x in enumerate(labels) if x['compound']==name);obs=math.log(r['mean'])
    rows.append(dict(candidate_id=r['candidate_id'],compound=name,doi=source['doi'],observed_molar_mean=r['mean'],ln_reported_mean=obs,model_log_prediction=float(pred[i]),training_mean_log_prediction=float(y.mean()),model_log_residual=float(pred[i]-obs),null_log_residual=float(y.mean()-obs),interpretation='KNOWN_COMPOUND_DIFFERENT_STUDY_PROTOCOL_SHIFT_NOT_NEW_STRUCTURE_VALIDATION',human_review_status='NOT_REVIEWED',change_applied='NO'))
with (P/'results/Retrospective_Pressure_Test.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
out=dict(scope='RESEARCHER_AUTHORIZED_RETROSPECTIVE_PROTOCOL_SHIFT_DIAGNOSTIC',n=2,selected_alpha=alpha,training_cv_mse=scores,external_labels_used_for_tuning=False,external_study_formal_validation=False,new_structure_validation=False,prediction_scale='log location compared with log reported arithmetic mean; different summaries',metrics={})
for model,col in [('model','model_log_residual'),('null','null_log_residual')]:out['metrics'][model]=dict(MAE=float(np.mean([abs(r[col]) for r in rows])),RMSE=float(np.sqrt(np.mean([r[col]**2 for r in rows]))))
out['source_input_sha256']=hashlib.sha256((P/'inputs/ishimoto_external_source_check.json').read_bytes()).hexdigest()
(P/'results/pressure_test_summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
