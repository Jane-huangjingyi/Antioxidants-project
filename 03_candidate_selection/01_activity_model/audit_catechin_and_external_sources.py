"""Reconcile catechin log labels and build a retrospective external-source queue."""
import csv,json,math
from pathlib import Path
P=Path(__file__).resolve().parent
def read(n):
    with (P/'results'/n).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
base=read('Observation_Readiness.csv');labels=read('Flavonoid_Log_Capacity_Extraction.csv');out=[]
for name in ['Catechin','Epicatechin','Epigallocatechin']:
    s=next(r for r in labels if r['compound']==name)
    b=next(r for r in base if r['compound']==name and r['doi']==s['doi'])
    recovered=math.exp(float(s['reported_ln_orac']));legacy=float(b['value_as_reported'])
    assert abs(recovered-legacy)<.001
    out.append(dict(compound=name,candidate_id=b['candidate_id'],doi=s['doi'],original_locator=s['source_locator'],original_ln_ORAC=s['reported_ln_orac'],reported_error_on_log_scale=s['reported_plus_minus_log_scale'],exp_log_location=recovered,legacy_value=legacy,legacy_unit=b['unit_as_reported'],finding='BACK_TRANSFORMED_NUMBER_WITH_LOG_UNIT_LABEL',model_label_status='Original log column already used; no training label changed',material_stereo_status='UNRESOLVED_SOURCE_DRAWING_AND_LOT',human_review_status='NOT_REVIEWED',change_applied='NO'))
with (P/'results/Catechin_Label_Reconciliation.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
mapped={r['candidate_id'] for r in read('Flavonoid_Candidate_Crosswalk.csv') if r['candidate_id']}
external=[]
for r in base:
    if r['candidate_id'] not in mapped or r['doi']=='10.3390/ijms20092328':continue
    external.append(dict(candidate_id=r['candidate_id'],compound=r['compound'],doi=r['doi'],doi_url='https://doi.org/'+r['doi'],legacy_observation_id=r['observation_id'],claimed_original_locator=r['source_location'],source_independence_status=r['source_independence_status'],legacy_value_for_audit_only=r['value_as_reported'],legacy_unit_for_audit_only=r['unit_as_reported'],external_validation_label='',eligibility='SOURCE_SCALE_PROTOCOL_AND_REUSE_REVIEW_PENDING',exposure_status='RETROSPECTIVE_PROJECT_DATA_PREVIOUSLY_ACCESSIBLE_NOT_BLIND',split_lock_status='NOT_LOCKED_NOT_USED_FOR_MODEL_SELECTION',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert all(r['doi']!='10.3390/ijms20092328' for r in external)
check=json.loads((P/'inputs/ishimoto_external_source_check.json').read_text(encoding='utf-8'))
checks=[check,json.loads((P/'inputs/rothe_external_source_check.json').read_text(encoding='utf-8')),json.loads((P/'inputs/carvalho_external_source_check.json').read_text(encoding='utf-8'))]
checks.append(json.loads((P/'inputs/froldi_external_source_check.json').read_text(encoding='utf-8')))
verified={(c['doi'],r['candidate_id']):(c,r) for c in checks for r in c['records']}
for r in external:
    pair=verified.get((r['doi'],r['candidate_id']));c,s=pair if pair else ({},None)
    r.update(original_mean_verified=s['mean'] if s else '',original_verified_unit=s['unit'] if s else '',verified_original_locator=s['locator'] if s else '',verified_source_url=c.get('source_url',''),source_named_stereoisomer=s['source_name'] if s else '',original_reported_plus_minus=s.get('reported_plus_minus','') if s else '',original_numeric_SD='',original_error_type=s.get('error_type','UNDEFINED_OR_NOT_NUMERICALLY_RECOVERED') if s else '',source_check_status='ORIGINAL_EXPERIMENTAL_MEAN_VERIFIED_OTHER_GATES_PENDING' if s else 'SOURCE_REVIEW_PENDING')
    if s:r['eligibility']='ORIGINAL_MEAN_VERIFIED_NOT_YET_COMMON_TARGET_TEST_LABEL'
with (P/'results/External_Source_Validation_Queue.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(external[0]));w.writeheader();w.writerows(external)
summary=dict(catechin_log_labels_checked=3,legacy_scale_label_conflicts=3,training_labels_changed=0,external_source_rows=len(external),external_papers=len({r['doi'] for r in external}),external_compounds=len({r['candidate_id'] for r in external}),original_means_rechecked=len(verified),approved_external_labels=0,blind_test_set=False)
(P/'results/catechin_external_source_qc.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
