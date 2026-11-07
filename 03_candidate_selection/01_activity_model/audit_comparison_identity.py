"""Check reference identity and food/form gates for source-local comparison rows."""
import csv,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
profiles={r['candidate_id']:r for r in read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')}
observations=[r for r in read(P/'results/Capacity_Analysis_Entry.csv') if r['comparison_scope'] in ['SOURCE_LOCAL_DESCRIPTIVE_SUBSET','SOURCE_IDENTITY_CONFLICT_DESCRIPTIVE_RANK_HELD']]
rows=[]
for i,r in enumerate(observations,1):
    p=profiles.get(r['candidate_id'],{})
    mismatch=bool(p) and r['compound'].strip().lower()!=p['compound_name'].strip().lower()
    rows.append(dict(comparison_row=i,candidate_id=r['candidate_id'],source_compound=r['compound'],reference_name=p.get('compound_name',''),doi=r['doi'],source_locator=r['source_locator'],source_scale=r['scale'],dose_uM=r['dose_uM'],reference_formula=p.get('molecular_formula',''),reference_CID=p.get('pubchem_cid',''),reference_InChIKey=p.get('inchi_key',''),reference_identity_url=p.get('identity_url',''),reference_identity_gate='REFERENCE_PRESENT' if all(p.get(k) for k in ['molecular_formula','pubchem_cid','inchi_key']) else 'REFERENCE_INCOMPLETE',source_name_match='EXACT_TEXT_MATCH' if p and not mismatch else 'NAME_OR_MAPPING_REVIEW_REQUIRED',food_occurrence_status=p.get('food_occurrence_status',''),food_source_locator=p.get('food_source_locator',''),exact_material_status=p.get('chemical_form_and_lot_status',''),source_form_review='SOURCE_FORM_AND_REFERENCE_EQUIVALENCE_PENDING',analysis_use='DESCRIPTIVE_SOURCE_VALUES_ONLY',panel_eligibility='NOT_ESTABLISHED',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==25
assert all(r['doi'] and r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in rows)
with (P/'results/Comparison_Identity_Audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(comparison_observations=len(rows),unique_candidates=len({r['candidate_id'] for r in rows}),reference_present=sum(r['reference_identity_gate']=='REFERENCE_PRESENT' for r in rows),name_review_rows=sum(r['source_name_match']=='NAME_OR_MAPPING_REVIEW_REQUIRED' for r in rows),food_status_counts=dict(collections.Counter(r['food_occurrence_status'] for r in rows)),exact_form_confirmed=0,formal_panel_approved=0)
(P/'results/comparison_identity_qc.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
