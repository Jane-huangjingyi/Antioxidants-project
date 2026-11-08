"""Exact-name identity crosswalk and an intercept-only reference, not QSAR."""
import csv,json,math,statistics
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
source=read(P/'results/Flavonoid_Log_Capacity_Extraction.csv')
profiles=read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')
rows=[]
for s in source:
    matches=[r for r in profiles if r['compound_name'].casefold()==s['compound'].casefold()]
    assert len(matches)<=1
    p=matches[0] if matches else {}
    rows.append(dict(source_row=s['source_row'],source_compound=s['compound'],doi=s['doi'],source_locator=s['source_locator'],experimental_ln_ORAC=s['reported_ln_orac'],reported_log_error=s['reported_plus_minus_log_scale'],error_definition=s['error_type'],candidate_id=p.get('candidate_id',''),reference_name=p.get('reference_name',''),CID=p.get('pubchem_cid',''),InChIKey=p.get('inchi_key',''),formula=p.get('molecular_formula',''),reference_url=p.get('identity_url',''),mapping_status='EXACT_NAME_REFERENCE_MATCH_NOT_SOURCE_FORM_APPROVAL' if p else 'OUTSIDE_EXACT_NAME_MATCH_NO_NEW_CANDIDATE_CREATED',food_scope=p.get('food_occurrence_status','NOT_ASSESSED_IN_CURRENT_UNIVERSE'),structure_graph_status='NOT_VALIDATED_FOR_DESCRIPTOR_GENERATION',human_review_status='NOT_REVIEWED',change_applied='NO'))
with (P/'results/Flavonoid_Candidate_Crosswalk.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# A null-model benchmark using all experimental source rows, including out-of-universe rows.
# Each observation is held out before estimating the training mean. No structural prediction claimed.
y=[float(r['experimental_ln_ORAC']) for r in rows];pred=[]
for i,v in enumerate(y):
    estimate=statistics.mean(y[:i]+y[i+1:]);pred.append(dict(source_row=rows[i]['source_row'],compound=rows[i]['source_compound'],observed_ln_ORAC=v,training_mean_prediction=estimate,residual=v-estimate,scope='INTERNAL_LEAVE_ONE_SOURCE_ROW_OUT_INTERCEPT_ONLY_NOT_EXTERNAL_VALIDATION'))
with (P/'results/Flavonoid_Null_Baseline.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(pred[0]));w.writeheader();w.writerows(pred)
out=dict(source_rows=len(rows),exact_name_matches=sum(bool(r['candidate_id']) for r in rows),unmatched_rows=sum(not r['candidate_id'] for r in rows),source_papers=1,null_baseline_scale='ln(ORAC)',null_MAE=statistics.mean(abs(r['residual']) for r in pred),null_RMSE=math.sqrt(statistics.mean(r['residual']**2 for r in pred)),structure_model_fitted=False,external_validation_performed=False,ranking_generated=False)
assert len(rows)==36 and len({r['source_row'] for r in rows})==36
(P/'results/flavonoid_mapping_qc.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
