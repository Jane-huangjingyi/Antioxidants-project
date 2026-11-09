"""Complete source-specific exploratory modelling; no global food-candidate ranking.

Model-family and penalty selection are nested inside scaffold folds. Prior inspection
of these same data means this remains post-hoc development, not fresh validation.
"""
import csv,hashlib,json,sys
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'.runtime_chem'))
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors,Crippen,rdMolDescriptors,Lipinski,rdFingerprintGenerator

def read(name):
    with (P/'results'/name).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (P/'results'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def ranks(values):
    # Average ranks, descending; numerical ties are never broken by candidate ID.
    v=np.round(np.asarray(values),10)
    return np.array([1+sum(v>x)+(sum(v==x)-1)/2 for x in v],dtype=float)
def spearman(a,b):
    a=ranks(a);b=ranks(b)
    return float(np.corrcoef(a,b)[0,1]) if np.std(a)>0 and np.std(b)>0 else None
def metrics(pred,obs):
    e=np.asarray(pred)-obs
    return dict(MAE=float(np.mean(abs(e))),RMSE=float(np.sqrt(np.mean(e**2))),
        R2=1-float(np.sum(e**2)/np.sum((obs-obs.mean())**2)),Spearman=spearman(pred,obs))

labels=read('Flavonoid_Log_Capacity_Extraction.csv')
structures={r['source_row']:r for r in read('Flavonoid_Structure_Audit.csv')}
crosswalk={r['source_row']:r for r in read('Flavonoid_Candidate_Crosswalk.csv')}
scaffolds={r['source_row']:r for r in read('Flavonoid_Scaffold_Groups.csv')}
y=np.array([float(r['reported_ln_orac']) for r in labels])
g=np.array([scaffolds[r['source_row']]['provisional_scaffold_group'] for r in labels])
connectivity=np.array([scaffolds[r['source_row']]['connectivity_group'] for r in labels])
assert len(y)==36 and len(set(g))==5
mols=[Chem.MolFromSmiles(structures[r['source_row']]['candidate_isomeric_SMILES']) for r in labels]
assert all(m is not None for m in mols)
four=np.array([[Descriptors.MolWt(m),Crippen.MolLogP(m),rdMolDescriptors.CalcTPSA(m),Lipinski.NumHDonors(m)] for m in mols])
six=np.column_stack([four,[len(m.GetSubstructMatches(Chem.MolFromSmarts('[OX2H][c]'))) for m in mols],
                         [len(m.GetSubstructMatches(Chem.MolFromSmarts('[CH3][OX2][c]'))) for m in mols]])
fp=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=1024,includeChirality=False)
features={'DESC4':four,'DESC6':six,'MORGAN':np.array([fp.GetFingerprintAsNumPy(m) for m in mols],dtype=float)}
options=[('NULL',0.)]+[(family,a) for family in features for a in [.1,1.,10.,100.]]

def predict(train,test,option,return_state=False):
    family,alpha=option;ym=float(y[train].mean())
    if family=='NULL':
        pred=np.repeat(ym,len(test));state=dict(family=family,alpha=alpha,intercept=ym)
    else:
        X=features[family];mu=X[train].mean(0);sd=X[train].std(0);sd[sd==0]=1
        a=(X[train]-mu)/sd;b=(X[test]-mu)/sd
        # Identical dual formulation for every representation; intercept unpenalized.
        beta=a.T@np.linalg.solve(a@a.T+alpha*np.eye(len(train)),y[train]-ym)
        pred=b@beta+ym
        state=dict(family=family,alpha=alpha,intercept=ym,feature_mean=mu.tolist(),feature_sd=sd.tolist(),coefficients=beta.tolist())
    return (pred,state) if return_state else pred

def select(train):
    scores=[]
    for option in options:
        e=[]
        for held in sorted(set(g[train])):
            tr=train[g[train]!=held];te=train[g[train]==held]
            assert not set(g[tr])&set(g[te]) and not set(connectivity[tr])&set(connectivity[te])
            e.extend((predict(tr,te,option)-y[te])**2)
        scores.append(float(np.mean(e)))
    best=min(range(len(options)),key=lambda i:(scores[i],i))
    return options[best],scores

oof=np.full(len(y),np.nan);null=np.full(len(y),np.nan)
fold_rows=[];prediction_rows=[];refit_predictions=[];selections=[]
for held in sorted(set(g)):
    tr=np.where(g!=held)[0];te=np.where(g==held)[0]
    assert not set(connectivity[tr])&set(connectivity[te])
    option,scores=select(tr);selections.append(option)
    oof[te]=predict(tr,te,option);null[te]=y[tr].mean()
    m=metrics(oof[te],y[te]) if len(te)>1 and np.std(y[te])>0 else dict(MAE=float(np.mean(abs(oof[te]-y[te]))),RMSE=float(np.sqrt(np.mean((oof[te]-y[te])**2))))
    fold_rows.append(dict(held_scaffold=held,training_n=len(tr),test_n=len(te),selected_family=option[0],selected_alpha=option[1],selected_MAE=m['MAE'],selected_RMSE=m['RMSE'],null_MAE=float(np.mean(abs(null[te]-y[te]))),null_RMSE=float(np.sqrt(np.mean((null[te]-y[te])**2)))))
    # Influence diagnostic: refit predictions for all known graphs. Not a new test set.
    refit_predictions.append(predict(tr,np.arange(len(y)),option))
    for i in te:
        prediction_rows.append(dict(source_row=labels[i]['source_row'],compound=labels[i]['compound'],held_scaffold=held,observed_ln_ORAC=y[i],nested_selected_prediction=oof[i],matched_null_prediction=null[i],selected_family=option[0],selected_alpha=option[1]))
assert np.isfinite(oof).all()
full_option,full_scores=select(np.arange(len(y)))
full_pred,state=predict(np.arange(len(y)),np.arange(len(y)),full_option,return_state=True)
mapped=np.array([i for i,r in enumerate(labels) if crosswalk[r['source_row']]['candidate_id']])
assert len(mapped)==16
positions=ranks(full_pred[mapped]);refit_ranks=np.array([ranks(v[mapped]) for v in refit_predictions])
candidate_rows=[]
for j,i in enumerate(mapped):
    r=labels[i];cw=crosswalk[r['source_row']]
    candidate_rows.append(dict(candidate_id=cw['candidate_id'],compound=r['compound'],source_row=r['source_row'],doi=r['doi'],source_locator=r['source_locator'],reference_formula=cw['formula'],observed_source_ln_ORAC=y[i],full_development_fit_log_location=full_pred[i],held_scaffold_prediction=oof[i],diagnostic_position_within_16=positions[j],refit_position_min=float(refit_ranks[:,j].min()),refit_position_max=float(refit_ranks[:,j].max()),refit_position_median=float(np.median(refit_ranks[:,j])),interpretation='IN_SAMPLE_MODEL_ORDER_AND_FIVE_REFIT_INFLUENCE_NOT_FINAL_POTENCY_RANK',food_scope=cw['food_scope'],source_material_match='NOT_APPROVED',global_rank='',human_review_status='NOT_REVIEWED',change_applied='NO'))
candidate_rows.sort(key=lambda r:(r['diagnostic_position_within_16'],r['candidate_id']))
with (P.parents[1]/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as f:
    profiles=list(csv.DictReader(f))
mapped_ids={r['candidate_id'] for r in candidate_rows}
coverage=[dict(candidate_id=r['candidate_id'],compound=r['compound_name'],reference_formula=r['molecular_formula'],
    development_coverage='MAPPED_IN_36_ROW_SOURCE' if r['candidate_id'] in mapped_ids else 'NOT_SUPPORTED_BY_THIS_MODEL',
    activity_interpretation='NO_ACTIVITY_INFERENCE_FROM_ABSENCE',global_rank='',human_review_status='NOT_REVIEWED',change_applied='NO') for r in profiles]
assert len(mapped_ids)==16 and len(profiles)==193 and len(mapped_ids&{r['candidate_id'] for r in profiles})==16
write('Candidate_Model_Coverage.csv',coverage)
write('Completed_Model_Heldout_Predictions.csv',prediction_rows)
write('Completed_Model_Fold_Metrics.csv',fold_rows)
write('Mapped_Candidate_Model_Diagnostics.csv',candidate_rows)
write('Model_Selection_Development_CV.csv',[dict(family=o[0],alpha=o[1],development_scaffold_CV_MSE=s,selected='YES' if o==full_option else 'NO') for o,s in zip(options,full_scores)])
state.update(target='SOURCE_REPORTED_LOG_LOCATION_NOT_ARITHMETIC_MEAN_CAPACITY',feature_specification='DESC4 or DESC6 as scripted; MORGAN radius2/1024/no chirality',training_source_rows=[r['source_row'] for r in labels],source_doi='10.3390/ijms20092328',scope='EXPLORATORY_DEVELOPMENT_ONLY',source_material_approved=False)
(P/'results/completed_exploratory_model.json').write_text(json.dumps(state,indent=2,allow_nan=False)+'\n',encoding='utf-8')
summary=dict(status='EXPLORATORY_MODELLING_COMPLETED_PRIMARY_RANKING_NOT_ESTABLISHED',n=36,scaffold_groups=5,mapped_candidates=16,
    current_candidate_profiles=len(profiles),unsupported_candidate_profiles=len(profiles)-len(mapped_ids),
    target='SOURCE_REPORTED_LN_ORAC',selection='Nested joint family/penalty selection; pooled inner MSE; deterministic candidate order resolves exact ties',
    model_options=len(options),metrics=dict(selected=metrics(oof,y),matched_null=metrics(null,y)),
    macro_group_MAE=dict(selected=float(np.mean([r['selected_MAE'] for r in fold_rows])),matched_null=float(np.mean([r['null_MAE'] for r in fold_rows]))),
    full_development_selection=dict(family=full_option[0],alpha=full_option[1]),outer_family_counts=dict(Counter(o[0] for o in selections)),
    full_fit_vs_refit_order_spearman=[spearman(full_pred[mapped],v[mapped]) for v in refit_predictions],
    inference_boundary='Post-hoc reuse of one previously inspected source; no independent-study validation, arithmetic-mean recovery, prediction intervals or global Top20',
    external_values_used_for_tuning=False,global_ranking_generated=False,formal_primary_model_completed=False,
    analysis_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),model_artifact_sha256=hashlib.sha256((P/'results/completed_exploratory_model.json').read_bytes()).hexdigest(),input_sha256={n:hashlib.sha256((P/'results'/n).read_bytes()).hexdigest() for n in ['Flavonoid_Log_Capacity_Extraction.csv','Flavonoid_Structure_Audit.csv','Flavonoid_Scaffold_Groups.csv','Flavonoid_Candidate_Crosswalk.csv']})
(P/'results/completed_model_summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n',encoding='utf-8')
print(json.dumps(summary,allow_nan=False))
