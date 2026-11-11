"""Join current candidate and observation references without assigning potency scores."""
from pathlib import Path
import csv,json,hashlib,collections
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(path,rows):
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def run():
 paths=[ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv',ROOT/'03_candidate_selection/01_activity_model/results/Capacity_Analysis_Entry.csv',ROOT/'03_candidate_selection/02_cross_study_expansion/results/Bridge_Panel_Preparation.csv']
 profiles,observations,panel=map(read,paths)
 byid=collections.defaultdict(list)
 for i,row in enumerate(observations,2):byid[row['candidate_id']].append((i,row))
 panel_ids={r['candidate_id'] for r in panel}
 candidates=[];evidence=[]
 for r in profiles:
  refs=byid[r['candidate_id']]
  food_refs=sorted({(x['food_followup_status'],x['food_followup_doi'],x['food_followup_locator'],x['food_followup_boundary']) for _,x in refs if x['food_followup_doi']})
  material_refs=sorted({(x['source_material_CAS'],x['source_material_reported_purity'],x['material_property_source_doi'],x['material_property_scope']) for _,x in refs if x['source_material_CAS'] or x['source_material_reported_purity']})
  candidates.append(dict(candidate_id=r['candidate_id'],compound=r['compound_name'],reference_formula=r['molecular_formula'],reference_CID=r['pubchem_cid'],reference_InChIKey=r['inchi_key'],food_source_status=r['food_occurrence_status'],food_followup_statuses=';'.join(sorted({x[0] for x in food_refs})),food_followup_dois=';'.join(sorted({x[1] for x in food_refs})),food_followup_records_json=json.dumps([dict(zip(['status','doi','locator','boundary'],x)) for x in food_refs],ensure_ascii=False),source_material_records_json=json.dumps([dict(zip(['CAS','reported_purity','source_doi','scope'],x)) for x in material_refs],ensure_ascii=False),food_followup_review='EXISTING_SOURCE_ANNOTATIONS_REQUIRE_FORM_SPECIFIC_REVIEW' if food_refs else 'NO_LINKED_FOLLOWUP_NOT_EVIDENCE_OF_ABSENCE',food_source_locator=r['food_source_locator'],reported_food_examples=r['reported_food_examples'],scope_disposition=r['scope_disposition'],exact_material_status=r['chemical_form_and_lot_status'],procurement_status=r['current_procurement_status'],absorbance_compatibility=r['current_absorbance_compatibility'],capacity_reference_rows=len(refs),capacity_source_dois=';'.join(sorted({x['doi'] for _,x in refs if x['doi']})),legacy_confirmed_study_count=r['confirmed_independent_horac_studies'],legacy_confirmed_source_dois=r['confirmed_horac_source_dois'],method_development_panel='YES' if r['candidate_id'] in panel_ids else 'NO',next_review_action='CHECK_EXISTING_SOURCE_VALUES_AND_COMPARABILITY' if refs else 'LOCATE_CAPACITY_SOURCE_NOT_EVIDENCE_OF_INACTIVITY',potency_score='',potency_rank='',selection_status='PRELIMINARY_EVIDENCE_ORGANIZATION_NOT_INCLUSION_APPROVAL',human_review_status='NOT_REVIEWED',change_applied='NO'))
  for line,x in refs:
   evidence.append(dict(candidate_id=r['candidate_id'],compound=r['compound_name'],source_table=paths[1].relative_to(ROOT).as_posix(),source_csv_line=line,**{k:x[k] for k in ['doi','doi_url','source_locator','value','scale','error','error_type','provenance','pooling_status','comparison_scope','food_followup_status','food_followup_doi','food_followup_locator','source_material_CAS','source_material_reported_purity','material_property_source_doi','material_property_scope','food_followup_scope','food_followup_boundary','exact_procurement_lot_status']},human_review_status='NOT_REVIEWED',change_applied='NO'))
 assert len(candidates)==193 and len({r['candidate_id'] for r in candidates})==193
 assert len(evidence)==len(observations),'Unmapped evidence would be silently lost'
 assert all(r['potency_score']==r['potency_rank']=='' for r in candidates)
 out=HERE/'results';out.mkdir(exist_ok=True)
 write(out/'Preliminary_Candidate_Review.csv',candidates)
 write(out/'Linked_Capacity_Source_References.csv',evidence)
 summary={'status':'PRELIMINARY_NOT_POTENCY_RANKING','candidate_rows':len(candidates),'candidates_with_capacity_references':sum(bool(byid[r['candidate_id']]) for r in profiles),'capacity_reference_rows':len(evidence),'method_panel_members':len(panel_ids),'candidates_with_existing_food_followup':sum(r['food_followup_records_json']!='[]' for r in candidates),'candidates_with_source_material_annotations':sum(r['source_material_records_json']!='[]' for r in candidates),'new_sources_verified':0,'formal_ranks_generated':0,'human_review_status':'NOT_REVIEWED','change_applied':'NO','input_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
 (out/'preselection_qc.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps(summary))
if __name__=='__main__':run()
