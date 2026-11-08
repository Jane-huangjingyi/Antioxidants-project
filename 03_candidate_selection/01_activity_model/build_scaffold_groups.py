"""Compute provisional RDKit Murcko groups; source identity remains unapproved."""
import sys,csv,json,hashlib,collections
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'.runtime_chem'))
from rdkit import Chem,rdBase
from rdkit.Chem.Scaffolds import MurckoScaffold
with (P/'results/Flavonoid_Structure_Audit.csv').open(encoding='utf-8-sig') as f:source=list(csv.DictReader(f))
rows=[]
for r in source:
    mol=Chem.MolFromSmiles(r['candidate_isomeric_SMILES']) if r['candidate_isomeric_SMILES'] else None
    scaffold='';generic=''
    if mol:
        core=MurckoScaffold.GetScaffoldForMol(mol)
        scaffold=Chem.MolToSmiles(core,isomericSmiles=False)
        generic=Chem.MolToSmiles(MurckoScaffold.MakeScaffoldGeneric(core),isomericSmiles=False)
    rows.append(dict(source_row=r['source_row'],compound=r['compound'],CID=r['candidate_CID'],connectivity_group=r['connectivity_leakage_group'],murcko_scaffold=scaffold,generic_scaffold=generic,provisional_scaffold_group=hashlib.sha256(scaffold.encode()).hexdigest()[:12] if scaffold else '',graph_status='PARSED_DATABASE_CANDIDATE' if mol else 'MISSING_OR_INVALID',source_identity_status='NOT_REVIEWED',fold_status='PROVISIONAL_GROUP_ONLY_NOT_VALIDATED_SPLIT',rdkit_version=rdBase.rdkitVersion))
groups=collections.defaultdict(list)
for r in rows:
    if r['provisional_scaffold_group']:groups[r['provisional_scaffold_group']].append(r['compound'])
# Same constitutional structure must not split across scaffold groups.
same=collections.defaultdict(set)
for r in rows:
    if r['connectivity_group'] and r['provisional_scaffold_group']:same[r['connectivity_group']].add(r['provisional_scaffold_group'])
assert all(len(g)==1 for g in same.values())
with (P/'results/Flavonoid_Scaffold_Groups.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
out=dict(rdkit_version=rdBase.rdkitVersion,total_rows=len(rows),parsed_graphs=sum(r['graph_status']=='PARSED_DATABASE_CANDIDATE' for r in rows),murcko_group_sizes={k:len(v) for k,v in groups.items()},generic_scaffold_count=len({r['generic_scaffold'] for r in rows if r['generic_scaffold']}),source_identity_approved=0,formal_folds_generated=False)
(P/'results/scaffold_group_qc.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
