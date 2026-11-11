"""Separate existing food-source leads from newly checked source passages."""
from pathlib import Path
import csv,json,collections
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def run():
 with (ROOT/'03_candidate_selection/01_activity_model/results/Capacity_Analysis_Entry.csv').open(encoding='utf-8-sig') as f:source=list(csv.DictReader(f))
 groups=collections.defaultdict(list)
 for r in source:
  if r['food_followup_doi']:groups[r['candidate_id']].append(r)
 with (ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as f:profiles={r['candidate_id']:r for r in csv.DictReader(f)}
 checks=json.loads((HERE/'inputs/positional_identity_check.json').read_text())
 crosswalk={r['candidate_id']:r for r in checks['records']}
 rows=[]
 for candidate,items in sorted(groups.items()):
  r=items[0];status=r['food_followup_status'];checked='EXISTING_ANNOTATION_ONLY_NOT_NEW_SOURCE_READING'
  url='https://doi.org/'+r['food_followup_doi'];locator=r['food_followup_locator']
  issue=r['food_followup_boundary'];action='VERIFY_ORIGINAL_METHODS_AND_EXACT_FOOD_FORM'
  if candidate=='AFF-0032':
   checked='PUBLISHER_ABSTRACT_RECHECKED';url='https://www.jstage.jst.go.jp/article/jnsv/52/1/52_1_54/_article';locator='Abstract: preparation of FG and FA'
   issue='The aglycone preparation was enzyme-derived. This source does not establish native free eriodictyol in the food.';action='LOCATE_NATIVE_FREE_FORM_SOURCE_OR_ADJUDICATE_DERIVED_DIETARY_FORM_SCOPE'
  elif candidate in {'AFF-0077','AFF-0078','AFF-0079','AFF-0080','AFF-0081'}:
   checked='ORIGINAL_HTML_SELECTED_PASSAGES_RECHECKED';url='https://pmc.ncbi.nlm.nih.gov/articles/PMC6526205/';locator='Chemicals and reagents; sample preparation; Figure 1; Table 2'
   issue='Food analyte positions are explicitly reported. Match candidate identifiers to source positional nomenclature before releasing exact-form eligibility; food concentration is not antioxidant capacity.';action='MATCH_POSITIONAL_STRUCTURE_TO_CANDIDATE_AND_MATERIAL'
  elif status=='PRIMARY_SOURCE_LEAD_PENDING_FULL_CHECK':action='RECOVER_FULL_METHODS_RESOLVE_HYDROLYSIS_AND_IDENTITY'
  mapping=crosswalk.get(candidate,{})
  if mapping:assert profiles[candidate]['pubchem_cid']==mapping['expected_CID']
  rows.append(dict(reference_CID=profiles[candidate]['pubchem_cid'],source_analyte=mapping.get('source_analyte',''),source_CAS=mapping.get('source_CAS',''),reference_identity_url=mapping.get('identity_url',''),positional_identity_status=mapping.get('finding','SOURCE_TO_STRUCTURE_MAPPING_PENDING'),positional_identity_boundary=mapping.get('boundary',''),candidate_id=candidate,compound=r['compound'],source_doi=r['food_followup_doi'],source_url=url,access_this_round=checked,source_locator=locator,existing_status=status,form_issue=issue,next_action=action,food_scope_decision='PENDING_FORM_SPECIFIC_ADJUDICATION',procurement_eligibility='NOT_RELEASED',human_review_status='NOT_REVIEWED',change_applied='NO'))
 assert len(rows)==17 and len({r['candidate_id'] for r in rows})==17
 with (HERE/'results/Food_Form_Review.csv').open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 print('17 form-review records; six candidate links rechecked in two original sources; no eligibility or approval released.')
if __name__=='__main__':run()
