"""Exploratory nested leave-scaffold-out ridge regression on one source's log labels."""
import sys,csv,json
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'.runtime_chem'))
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors,Crippen,rdMolDescriptors,Lipinski,rdFingerprintGenerator
def read(n):
    with (P/'results'/n).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
labels={r['source_row']:float(r['reported_ln_orac']) for r in read('Flavonoid_Log_Capacity_Extraction.csv')}
structures={r['source_row']:r for r in read('Flavonoid_Structure_Audit.csv')}
groups=read('Flavonoid_Scaffold_Groups.csv');assert len(groups)==36
augmented='--augmented' in sys.argv
fingerprint='--fingerprint' in sys.argv
assert not (augmented and fingerprint)
generator=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=1024,includeChirality=False)
X=[]
for r in groups:
    m=Chem.MolFromSmiles(structures[r['source_row']]['candidate_isomeric_SMILES']);assert m is not None
    features=[Descriptors.MolWt(m),Crippen.MolLogP(m),rdMolDescriptors.CalcTPSA(m),Lipinski.NumHDonors(m)]
    if augmented:features += [len(m.GetSubstructMatches(Chem.MolFromSmarts('[OX2H][c]'))),len(m.GetSubstructMatches(Chem.MolFromSmarts('[CH3][OX2][c]')))]
    if fingerprint:features=generator.GetFingerprintAsNumPy(m).tolist()
    X.append(features)
X=np.array(X);y=np.array([labels[r['source_row']] for r in groups]);g=np.array([r['provisional_scaffold_group'] for r in groups]);unique=sorted(set(g))
def predict(train,test,alpha):
    mean=X[train].mean(0);sd=X[train].std(0);sd[sd==0]=1
    a=(X[train]-mean)/sd;b=(X[test]-mean)/sd;ym=y[train].mean()
    coef=a.T@np.linalg.solve(a@a.T+alpha*np.eye(len(train)),y[train]-ym) if X.shape[1]>len(train) else np.linalg.solve(a.T@a+alpha*np.eye(X.shape[1]),a.T@(y[train]-ym))
    return b@coef+ym
predictions=[];folds=[]
for held in unique:
    train=np.where(g!=held)[0];test=np.where(g==held)[0];scores={}
    assert not set(g[train])&set(g[test])
    for alpha in [.1,1.,10.,100.]:
        errors=[]
        for inner in sorted(set(g[train])):
            it=train[g[train]!=inner];iv=train[g[train]==inner]
            errors.extend((predict(it,iv,alpha)-y[iv])**2)
        scores[alpha]=float(np.mean(errors))
    alpha=min(scores,key=lambda a:(scores[a],a));p=predict(train,test,alpha);null=np.repeat(y[train].mean(),len(test))
    folds.append(dict(held_scaffold=held,train_n=len(train),test_n=len(test),selected_alpha=alpha,ridge_MAE=float(np.mean(abs(p-y[test]))),ridge_RMSE=float(np.sqrt(np.mean((p-y[test])**2))),null_MAE=float(np.mean(abs(null-y[test]))),null_RMSE=float(np.sqrt(np.mean((null-y[test])**2)))))
    for i,v,n in zip(test,p,null):predictions.append(dict(source_row=groups[i]['source_row'],compound=groups[i]['compound'],held_scaffold=held,observed_ln_ORAC=float(y[i]),ridge_prediction=float(v),null_prediction=float(n),identity_status='DATABASE_CANDIDATE_SOURCE_FORM_UNREVIEWED'))
for name,rows in [('Scaffold_Fold_Metrics.csv',folds),('Scaffold_Heldout_Predictions.csv',predictions)]:
    if augmented:name='Augmented_'+name
    if fingerprint:name='Fingerprint_'+name
    with (P/'results'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert len(predictions)==36 and len({r['source_row'] for r in predictions})==36
summary=dict(status='EXPLORATORY_SINGLE_PAPER_DATABASE_GRAPH_VALIDATION',n=36,folds=5,descriptors=['MolWt','MolLogP','TPSA','HBD'],target='Experimental ln(ORAC)',alpha_grid=[.1,1,10,100],selection='Nested leave-scaffold-out pooled inner MSE',metrics={})
if augmented:summary.update(descriptors=summary['descriptors']+['Phenolic_OH_count','Aryl_methoxy_count'],analysis_status='POST_HOC_FEATURE_SENSITIVITY_NOT_NEW_INDEPENDENT_VALIDATION')
if fingerprint:summary.update(descriptors=['Morgan radius 2, 1024 bits, no chirality'],analysis_status='POST_HOC_FINGERPRINT_SENSITIVITY_NOT_INDEPENDENT_VALIDATION',unique_feature_vectors=len({tuple(v) for v in X}),feature_scaling='Training-fold mean and SD; zero-SD scale one')
for model,key in [('ridge','ridge_prediction'),('null','null_prediction')]:
    errors=np.array([r[key]-r['observed_ln_ORAC'] for r in predictions]);summary['metrics'][model]=dict(MAE=float(np.mean(abs(errors))),RMSE=float(np.sqrt(np.mean(errors**2))))
summary.update(external_study_validation=False,source_identity_approved=False,final_ranking_generated=False)
filename='fingerprint_scaffold_validation_summary.json' if fingerprint else 'augmented_scaffold_validation_summary.json' if augmented else 'scaffold_validation_summary.json'
(P/'results'/filename).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
