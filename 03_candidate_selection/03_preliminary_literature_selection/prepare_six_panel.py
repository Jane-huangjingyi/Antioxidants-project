"""Prepare the researcher-accepted six-compound pilot proposal from current evidence."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
PANEL=[('AFF-0001','Multi-source flavanol; matched comparison with epicatechin','Exact stereochemistry, stock and final-well stability'),('AFF-0002','Multi-source flavanol; matched comparison with catechin','Exact stereochemistry, material identity and preparation'),('AFF-0009','Multi-source flavonol with high reference response','Hydrate/salt form, final solubility and optical/probe interference'),('AFF-0069','Phenolic-acid coverage and existing vehicle follow-up','Final vehicle matching, solution stability and calibration'),('AFF-0104','Researcher-prioritized nonphenolic ascorbate chemistry','L form, oxidation during preparation and read timing'),('NEW-GSH','Thiol/peptide coverage with existing food-source lead','Reduced form, oxidized fraction and assay response')]
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as handle:return list(csv.DictReader(handle))
def run():
 paths=[ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv',HERE/'results/Detection_Candidate_Assessment.csv',ROOT/'03_candidate_selection/05_model_robustness/results/Candidate_Model_Sensitivity.csv']
 profiles,assessment,model=[{r['candidate_id']:r for r in read(path)} for path in paths]
 rows=[]
 for candidate,rationale,issue in PANEL:
  r=profiles[candidate];a=assessment[candidate];m=model[candidate]
  rows.append(dict(candidate_id=candidate,compound=r['compound_name'],reference_formula=r['molecular_formula'],reference_CID=r['pubchem_cid'],identity_url=r['identity_url'],selection_rationale=rationale,priority_material_issue=issue,capacity_source_dois=a['source_dois'],capacity_reference_order=a['exploratory_capacity_reference_order'],capacity_source_papers=a['source_papers'],food_source_status=r['food_occurrence_status'],food_source_locator=r['food_source_locator'],model_component_order=m['OLS_component_order'],model_interpretation='EXPLORATORY_COMPONENT_LOG_LOCATION_WITH_UNRESOLVED_PROTOCOLS',material_supplier='',catalogue='',exact_form='',lot='',COA_locator='',purity_basis='',stock_preparation='',final_vehicle='',final_solubility_check='',stability_check='',no_probe_background_check='',probe_no_initiator_check='',source_review_decision='PENDING',material_review_decision='PENDING',assay_entry_decision='PENDING',human_review_status='NOT_REVIEWED',change_applied='NO'))
 assert len(rows)==6 and len({r['candidate_id'] for r in rows})==6
 out=HERE/'results/Six_Compound_Pilot_Preparation.csv'
 with out.open('w',encoding='utf8',newline='') as handle:
  writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 print('Six pilot candidates linked to existing identity, capacity, food and model records. Procurement and assay qualification pending.')
if __name__=='__main__':run()
