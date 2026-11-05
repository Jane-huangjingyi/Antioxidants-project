"""Create a review queue and an explicitly separate, gated laboratory-ready panel."""
from pathlib import Path
import sys,collections
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
rows=read_csv(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')
rules=read_json(ROOT/'03_candidate_selection/config/selection_rules.json')
decision_path=ROOT/'03_candidate_selection/config/researcher_decisions.csv'
fields=['candidate_id','food_source_verified','food_source_locator','reagent_form_and_procurement_verified','aqueous_solubility_stability_pass','absorbance_counter_screen_pass','researcher_decision','decision_source','reviewer','review_date']
if not decision_path.exists():write_csv(decision_path,[dict.fromkeys(fields,'')|{'candidate_id':r['candidate_id']} for r in rows],fields)
manual=read_csv(decision_path);assert len({r['candidate_id'] for r in manual})==len(manual)
decisions={r['candidate_id']:r for r in manual}
audit=[];queue=[];ready=[]
def stratum(r):return (0 if (number(r['confirmed_independent_horac_studies']) or 0)>=2 else 1,0 if (number(r['typed_sd_record_count']) or 0)>0 else 1)
for r in rows:
 reasons=[]
 if r['scope_disposition']!='RETAIN_FOR_IDENTITY_AND_FOOD_VERIFICATION':reasons.append('UNSPECIFIED_CHEMICAL_FORM_OUTSIDE_MOLECULAR_PANEL')
 if r['identity_reference_status']!='REFERENCE_IDENTIFIERS_AND_FORMULA_PRESENT':reasons.append('REFERENCE_IDENTITY_OR_FORMULA_MISSING')
 if r['legacy_food_occurrence_uncertain']=='YES':reasons.append('SPECIFIC_FOOD_OCCURRENCE_FLAG_REQUIRES_REVIEW')
 n=number(r['confirmed_independent_horac_studies'])
 if n is None or n<1:reasons.append('NO_CONFIRMED_STUDY_IN_THIS_CLOSURE_NOT_PROOF_OF_INACTIVITY')
 include=not reasons
 if include:queue.append(r)
 d=decisions.get(r['candidate_id'],{})
 gate=[d.get(k)=='YES' for k in ['food_source_verified','reagent_form_and_procurement_verified','aqueous_solubility_stability_pass','absorbance_counter_screen_pass']]
 formal=all(gate) and d.get('researcher_decision')=='INCLUDE' and all(d.get(k) for k in ['food_source_locator','decision_source','reviewer','review_date']) and r['identity_reference_status']=='REFERENCE_IDENTIFIERS_AND_FORMULA_PRESENT' and r['scope_disposition']=='RETAIN_FOR_IDENTITY_AND_FOOD_VERIFICATION'
 if formal:ready.append(r)
 audit.append({'candidate_id':r['candidate_id'],'compound_name':r['compound_name'],'review_queue_eligible':'YES' if include else 'HOLD','review_queue_gate_reason':'; '.join(reasons) or 'REFERENCE_IDENTITY_AND_CONFIRMED_CHEMICAL_SOURCE_PRESENT','food_source_gate':d.get('food_source_verified') or 'NOT_VERIFIED','procurement_gate':d.get('reagent_form_and_procurement_verified') or 'NOT_VERIFIED','solubility_gate':d.get('aqueous_solubility_stability_pass') or 'NOT_TESTED','absorbance_gate':d.get('absorbance_counter_screen_pass') or 'NOT_TESTED','formal_panel_eligible':'YES' if formal else 'NO','human_review_status':'RESEARCHER_DECISION_RECORDED' if formal else 'NOT_REVIEWED','change_applied':'NO'})
queue.sort(key=lambda r:(*stratum(r),r['candidate_id']))
short=queue[:rules['target_size']]
cut=stratum(short[-1]) if short else None
tied=[r for r in queue if stratum(r)==cut] if cut else []
for i,r in enumerate(short,1):
 r['review_slot']=i;r['slot_interpretation']='ADMINISTRATIVE_REVIEW_SLOT_NOT_POTENCY_RANK';r['shortlist_status']='PROVISIONAL_SOURCE_AND_LAB_FEASIBILITY_REVIEW';r['cutoff_stratum_tied_count']=len(tied)
write_csv(ROOT/'03_candidate_selection/results/top20_review_queue.csv',short)
write_csv(ROOT/'03_candidate_selection/results/all_candidate_decisions.csv',audit)
write_csv(ROOT/'03_candidate_selection/results/cutoff_tied_candidates.csv',[{'candidate_id':r['candidate_id'],'compound_name':r['compound_name'],'confirmed_studies':r['confirmed_independent_horac_studies'],'typed_sd_records':r['typed_sd_record_count'],'currently_in_preview':'YES' if r in short else 'NO','interpretation':'Evidence-stratum tie; researcher adjudication required'} for r in tied])
write_csv(ROOT/'03_candidate_selection/results/formal_lab_ready_panel.csv',[{k:r[k] for k in ['candidate_id','compound_name','molecular_formula','pubchem_cid','inchi_key']} for r in ready],['candidate_id','compound_name','molecular_formula','pubchem_cid','inchi_key'])
scenarios=[{'scenario':'ONE_CONFIRMED_STUDY_REVIEW_QUEUE','eligible_count':len(queue),'preview_count':len(short),'interpretation':'20-slot review preview; all lab and food-source gates still apply'}, {'scenario':'TWO_CONFIRMED_STUDIES_ONLY','eligible_count':sum((number(r['confirmed_independent_horac_studies']) or 0)>=2 for r in queue),'preview_count':min(20,sum((number(r['confirmed_independent_horac_studies']) or 0)>=2 for r in queue)),'interpretation':'Reliability sensitivity; never fill with unsupported zeros'}, {'scenario':'FORMAL_LAB_READY_PANEL','eligible_count':len(ready),'preview_count':min(20,len(ready)),'interpretation':'Actual researcher/material/counter-screen gates; no auto-approval'}]
write_csv(ROOT/'03_candidate_selection/results/selection_sensitivity.csv',scenarios)
write_json(ROOT/'03_candidate_selection/results/selection_summary.json',{'profile_count':len(rows),'queue_eligible':len(queue),'review_slots':len(short),'formal_lab_ready':len(ready),'cutoff_tied_count':len(tied),'rules':rules})
print(f'03: {len(queue)} review-eligible, {len(short)} provisional slots, {len(ready)} laboratory-ready; cutoff ties disclosed.')
