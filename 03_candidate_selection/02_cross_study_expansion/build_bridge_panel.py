"""Prepare a class/source bridge panel, never a potency ranking or executed experiment."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
with (ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as f:
    profiles={r['candidate_id']:r for r in csv.DictReader(f)}
config=json.loads((P/'inputs/bridge_panel.json').read_text(encoding='utf-8'))
platform=json.loads((ROOT/'04_absorbance_assay/config/platform_decisions.json').read_text(encoding='utf-8'))
with (ROOT/'03_candidate_selection/01_activity_model/results/Capacity_Analysis_Entry.csv').open(encoding='utf-8-sig') as f:
    refs=list(csv.DictReader(f))
rows=[]
for item in config['panel']:
    r=profiles[item['candidate_id']]
    assert r['molecular_formula'] and r['pubchem_cid']
    dois=sorted({x['doi'] for x in refs if x['candidate_id']==r['candidate_id'] and x['doi']})
    rows.append(dict(candidate_id=r['candidate_id'],compound=r['compound_name'],reference_formula=r['molecular_formula'],reference_CID=r['pubchem_cid'],
        bridge_reason=item['bridge_reason'],source_dois_for_followup_not_all_verified=';'.join(dois),
        candidate_food_source_status=r['food_occurrence_status'],material_identity_status=r['chemical_form_and_lot_status'],
        exact_material_form='',supplier_catalogue='',lot='',purity_fraction='',stock_concentration='',final_vehicle='',dose_series='',
        independent_batch_plan='',instrument=platform['instrument_model'],instrument_configuration_status=platform['local_configuration']['researcher_reply'],literature_reference_scope='ORAC_FL_PH7.4_37C_PROTOCOL_STRATIFIED',active_measurement_route=config['measurement_route'],ORAC_FL_paired_measurement_available='NO',ORAC_FL_transfer_claim_allowed='NO',
        standalone_absorbance_method='',experimental_status='NOT_STARTED_PARAMETER_APPROVAL_REQUIRED',
        selection_status=config['status'],potency_score='',formal_rank='',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==12 and len({r['candidate_id'] for r in rows})==12
with (P/'results/Bridge_Panel_Preparation.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Bridge panel: 12 existing profiles; zero new candidates, potency ranks, approved parameters or experiments.')
