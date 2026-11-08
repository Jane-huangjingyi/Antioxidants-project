"""Audit retrieved candidate graphs; distinguish database agreement from source stereo."""
import csv,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent
data=json.loads((P/'inputs/flavonoid_structure_candidates.json').read_text(encoding='utf-8'))
fallback=json.loads((P/'inputs/flavonoid_structure_145826_verified_response.json').read_text(encoding='utf-8'))
for r in data:
    if r['source_row']==fallback['source_row'] and r['status']!='RECOVERED':
        r.update(status='RECOVERED_CURATED_SUCCESSFUL_API_OUTPUT',property_candidates=[fallback['property']],query_url=fallback['query_url'],query_basis='OFFICIAL_SYNONYM_CID_PENDING_SOURCE_MAPPING')
rows=[]
for r in data:
    props=r.get('property_candidates',[]);p=props[0] if len(props)==1 else {}
    smiles=p.get('SMILES',p.get('IsomericSMILES',''))
    key=p.get('InChIKey','')
    rows.append(dict(source_row=r['source_row'],compound=r['compound'],retrieval_status=r['status'],query_basis=r.get('query_basis',''),query_url=r['query_url'],returned_candidates=len(props),candidate_CID=p.get('CID',''),candidate_InChIKey=key,candidate_InChI=p.get('InChI',''),candidate_isomeric_SMILES=smiles,connectivity_SMILES=p.get('ConnectivitySMILES',p.get('CanonicalSMILES','')),defined_atom_stereocentres=p.get('DefinedAtomStereoCount',''),undefined_atom_stereocentres=p.get('UndefinedAtomStereoCount',''),reference_key_agreement=r.get('reference_key_agreement','NOT_APPLICABLE_NAME_QUERY'),connectivity_leakage_group=key.split('-')[0] if key else '',source_stereochemistry_status='NOT_VERIFIED_AGAINST_ORIGINAL_STRUCTURE',graph_mapping_status='DATABASE_CANDIDATE_NOT_SOURCE_IDENTITY_APPROVAL' if p else 'UNRESOLVED',scaffold_status='NOT_COMPUTED_REQUIRES_VALIDATED_GRAPH_TOOL',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==36
with (P/'results/Flavonoid_Structure_Audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
out=dict(rows=36,recovered=sum(r['retrieval_status'].startswith('RECOVERED') for r in rows),unique_single_hit_graphs=sum(bool(r['candidate_CID']) for r in rows),isomeric_smiles_present=sum(bool(r['candidate_isomeric_SMILES']) for r in rows),reference_key_conflicts=sum(r['reference_key_agreement'] is False for r in rows),source_stereochemistry_approved=0,scaffold_folds_generated=False)
(P/'results/flavonoid_structure_qc.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
