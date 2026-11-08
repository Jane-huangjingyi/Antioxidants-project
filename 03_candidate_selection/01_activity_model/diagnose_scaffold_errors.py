"""Inspect outer-fold coverage and descriptor collisions; no label changes."""
import sys,csv,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'.runtime_chem'))
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors,Crippen,rdMolDescriptors,Lipinski
def read(n):
    with (P/'results'/n).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
s={r['source_row']:r for r in read('Flavonoid_Structure_Audit.csv')};r=read('Scaffold_Heldout_Predictions.csv');X=[]
for x in r:
    m=Chem.MolFromSmiles(s[x['source_row']]['candidate_isomeric_SMILES'])
    X.append([Descriptors.MolWt(m),Crippen.MolLogP(m),rdMolDescriptors.CalcTPSA(m),Lipinski.NumHDonors(m)])
X=np.array(X);features=['MW','LogP','TPSA','HBD'];out=[];collisions=collections.defaultdict(list)
for i,x in enumerate(r):
    train=np.array([j for j,z in enumerate(r) if z['held_scaffold']!=x['held_scaffold']]);low=X[train].min(0);high=X[train].max(0)
    outside=[features[j] for j in range(4) if X[i,j]<low[j]-1e-9 or X[i,j]>high[j]+1e-9]
    out.append(dict(x,descriptor_range_violations='; '.join(outside),range_check_scope='Univariate bounds only, not a calibrated applicability domain',absolute_error=abs(float(x['ridge_prediction'])-float(x['observed_ln_ORAC']))))
    collisions[tuple(np.round(X[i],8))].append(x)
with (P/'results/Scaffold_Error_Diagnostics.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
pairs=[dict(compounds=[x['compound'] for x in a],observed_log_values=[float(x['observed_ln_ORAC']) for x in a]) for a in collisions.values() if len(a)>1]
summary=dict(test_rows=len(r),rows_outside_training_univariate_bounds=sum(bool(x['descriptor_range_violations']) for x in out),descriptor_collision_sets=pairs,interpretation='Identical four-descriptor vectors cannot distinguish their source labels; this does not establish stereochemical causation or a source error')
(P/'results/scaffold_error_diagnostics.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
