"""Join capacity-reference priority with explicitly documented method coverage."""
from pathlib import Path
import csv,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as handle:return list(csv.DictReader(handle))
def run():
 profiles=read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')
 references={r['candidate_id']:r for r in read(HERE/'results/Exploratory_Literature_Reference_Order.csv')}
 influence={r['candidate_id']:r for r in read(HERE/'results/Source_Omission_Order_Diagnostic.csv')}
 panel=json.loads((ROOT/'03_candidate_selection/02_cross_study_expansion/inputs/bridge_panel.json').read_text())
 coverage={r['candidate_id']:r['bridge_reason'] for r in panel['panel']}
 rows=[]
 for profile in profiles:
  candidate=profile['candidate_id'];ref=references.get(candidate,{})
  diagnostic=influence.get(candidate,{})
  high=bool(ref) and int(ref['exploratory_reference_order'])<=20
  role='CAPACITY_AND_CHEMISTRY_COVERAGE_REVIEW' if high and candidate in coverage else 'CHEMISTRY_COVERAGE_REVIEW' if candidate in coverage else 'HIGH_REFERENCE_CAPACITY_REVIEW' if high else 'ADDITIONAL_EVIDENCE_REVIEW'
  rows.append(dict(candidate_id=candidate,compound=profile['compound_name'],reference_formula=profile['molecular_formula'],reference_CID=profile['pubchem_cid'],review_role=role,coverage_reason=coverage.get(candidate,''),exploratory_capacity_reference_order=ref.get('exploratory_reference_order',''),source_papers=ref.get('source_papers',''),capacity_reference_median=ref.get('exploratory_reference_median_molar_TE',''),source_dois=ref.get('source_dois',''),food_source_status=profile['food_occurrence_status'],material_status=profile['chemical_form_and_lot_status'],procurement_status=profile['current_procurement_status'],absorbance_compatibility=profile['current_absorbance_compatibility'],source_omission_unsupported_scenarios=diagnostic.get('scenarios_without_remaining_source',''),source_omission_fixed_universe_best=diagnostic.get('fixed_universe_best_possible_order',''),source_omission_fixed_universe_worst=diagnostic.get('fixed_universe_worst_possible_order',''),model_expected_capacity='',model_interval='',model_top20_probability='',detection_suitability_decision='PENDING_MATERIAL_AND_ASSAY_QUALIFICATION',human_review_status='NOT_REVIEWED',change_applied='NO'))
 assert len(rows)==193 and len(coverage)==12
 with (HERE/'results/Detection_Candidate_Assessment.csv').open('w',encoding='utf8',newline='') as handle:
  writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 print('193 detection assessments; 12 explicit chemistry-coverage proposals; model fields await valid estimates.')
if __name__=='__main__':run()
