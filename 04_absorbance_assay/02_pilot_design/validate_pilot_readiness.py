"""Offline preparation checks; synthetic arrays are not experimental observations."""
from pathlib import Path
import csv, hashlib, importlib.util, json, math
from copy import deepcopy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def missing_fields(value,prefix=''):
    missing=[]
    for key,item in value.items():
        path=f'{prefix}.{key}' if prefix else key
        if isinstance(item,dict):missing.extend(missing_fields(item,path))
        elif item is None or item==[]:missing.append(path)
    return missing
def must_fail(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Invalid input unexpectedly accepted')
def run():
    audit=json.loads((HERE/'formula_source_audit.json').read_text())
    byid={r['id']:r for r in audit['records']}
    assert byid['CBA_2015_MICROPLATE']['access']=='ABSTRACT_READ_FULL_EQUATIONS_PENDING'
    assert byid['CBA_2015_PROTOCOL']['access']=='ABSTRACT_READ_FULL_EQUATIONS_PENDING'
    formula=load_module('capacity',HERE.parent/'01_endpoint_definition/capacity_formula.py')
    kinetics=load_module('kinetics',HERE.parent/'code/analyze_kinetics.py')
    # Synthetic observable orientation: each reaction minus its no-initiator blank.
    b0=0.2-1.0;bs=0.7-1.0
    assert math.isclose(100*(b0-bs)/b0,62.5)
    assert math.isclose(100*(0.2-0.7)/0.2,-250)
    # Matched no-probe background, retained-probe AUC and negative net response.
    rows=[]
    for well,role,values in [('A1','SAMPLE',[1.1,.9,.7]),('A2','MATCHED_NO_PROBE',[.1,.1,.1])]:
        for time,value in zip([0,1,2],values):
            rows.append(dict(batch_id='SYNTHETIC',plate_id='SYNTHETIC',well=well,candidate_id='SYNTHETIC',role=role,pair_id='PAIR',concentration_uM='1',counter_screen_pass='YES',time_min=str(time),absorbance=str(value),protocol_id='SYNTHETIC',preparation_id='PREP_TEST',vehicle_id='VEHICLE_TEST',time_origin='INITIATOR_ADDITION'))
    result=kinetics.analyze(rows)
    assert len(result)==1 and math.isclose(result[0]['normalized_auc_min'],1.6)
    assert math.isclose(result[0]['corrected_initial_absorbance'],1.0)
    assert math.isclose(result[0]['corrected_final_absorbance'],.6)
    assert result[0]['no_probe_well']=='A2' and result[0]['time_points']==3
    must_fail(lambda:kinetics.analyze([dict(r,counter_screen_pass='NO') for r in rows]))
    must_fail(lambda:kinetics.analyze([r for r in rows if r['role']!='MATCHED_NO_PROBE']))
    mismatch=[dict(r,concentration_uM='2') if r['role']=='MATCHED_NO_PROBE' else r for r in rows]
    must_fail(lambda:kinetics.analyze(mismatch))
    must_fail(lambda:kinetics.integrate([0,0],[1,1]))
    must_fail(lambda:kinetics.analyze([dict(r,time_min='-1') if r['time_min']=='0' else r for r in rows]))
    must_fail(lambda:kinetics.analyze([dict(r,role='SAMPEL') for r in rows]))
    must_fail(lambda:kinetics.analyze([dict(r,protocol_id=None) for r in rows]))
    must_fail(lambda:kinetics.analyze([dict(r,protocol_id='OTHER') if r['role']=='MATCHED_NO_PROBE' else r for r in rows]))
    must_fail(lambda:kinetics.analyze([dict(r,counter_screen_pass='NO') if r['role']=='MATCHED_NO_PROBE' else r for r in rows]))
    # Explicit shared-vehicle contrasts; no synthetic measurements are written out.
    comparison=load_module('comparison',HERE.parent/'code/compare_auc.py')
    vehicle=dict(result[0],well='V1',role='VEHICLE',normalized_auc_min=1.0)
    assignment=[{'sample':dict(batch_id='SYNTHETIC',plate_id='SYNTHETIC',well='A1'),
                 'vehicles':[dict(batch_id='SYNTHETIC',plate_id='SYNTHETIC',well='V1')]}]
    contrasted=comparison.compare(result+[vehicle],assignment)[0]
    assert math.isclose(contrasted['net_auc_min'],.6)
    assert json.loads(contrasted['vehicle_wells_json'])==['V1']
    negative=comparison.compare([dict(result[0],normalized_auc_min=.5),vehicle],assignment)[0]
    assert negative['net_auc_min']==-.5 and negative['response_sign']=='NONPOSITIVE'
    must_fail(lambda:comparison.compare(result+[dict(vehicle,protocol_id='OTHER')],assignment))
    must_fail(lambda:comparison.compare(result+[dict(vehicle,time_grid_sha256='OTHER')],assignment))
    must_fail(lambda:comparison.compare(result+[dict(vehicle,preparation_id='OTHER')],assignment))
    must_fail(lambda:comparison.compare(result+[dict(vehicle,vehicle_id='OTHER')],assignment))
    duplicate=deepcopy(assignment);duplicate[0]['vehicles']*=2
    must_fail(lambda:comparison.compare(result+[vehicle],duplicate))
    must_fail(lambda:comparison.compare(result+[vehicle],[]))
    must_fail(lambda:comparison.compare([dict(result[0],protocol_id=None),dict(vehicle,protocol_id=None)],assignment))
    formula.synthetic_checks()
    template=json.loads((HERE/'pilot_manifest_template.json').read_text())
    assert template['human_review_status']=='NOT_REVIEWED' and template['change_applied']=='NO'
    assert not template['experiment_executed'] and not template['formal_model_fitted']
    platform=json.loads((HERE.parent/'config/platform_decisions.json').read_text())
    assert platform['available_measurement_mode']=='ABSORBANCE_ONLY_RESEARCHER_CONFIRMED'
    assert platform['paired_ORAC_FL_available'] is False and platform['ORAC_FL_transfer_claim_allowed'] is False
    for key,value in platform.items():
        if key.startswith('approved_'):assert value is None,key
    with (HERE.parent/'inputs/experimental_data_schema.csv').open(encoding='utf-8-sig',newline='') as f:
        assert list(csv.DictReader(f))==[], 'Do not report absence of data after experiments have been added'
    required=missing_fields(template)
    assert required
    assignments=json.loads((HERE/'vehicle_assignments_template.json').read_text())
    assert assignments['contrasts']==[] and assignments['human_review_status']=='NOT_REVIEWED' and assignments['change_applied']=='NO'
    assert byid['CBA_2006_INHIBITION']['access']=='ORIGINAL_ABSTRACT_FORMULA_READ_FULL_PROTOCOL_PENDING'
    pending=[r['doi'] for r in audit['records'] if r.get('access')=='ABSTRACT_READ_FULL_EQUATIONS_PENDING']
    inputs=[HERE/'formula_source_audit.json',HERE/'pilot_manifest_template.json',HERE/'vehicle_assignments_template.json',HERE.parent/'inputs/experimental_data_schema.csv',HERE.parent/'config/platform_decisions.json',HERE.parent/'code/analyze_kinetics.py',HERE.parent/'code/compare_auc.py',HERE.parent/'01_endpoint_definition/capacity_formula.py',Path(__file__)]
    report={'preparation_checks':'PASS','check_scope':'SYNTHETIC_ALGEBRA_AND_DRAFT_BOUNDARIES_ONLY','assay_execution_readiness':'NOT_READY','unfilled_manifest_fields':required,'original_formula_sources_pending':pending,'additional_original_abstract_formula':'10.1021/jf052731u','synthetic_checks':['blank_subtraction_sign','corrected_initial_and_final_signal','positive_and_negative_net_AUC','reject_missing_QC','reject_mismatched_background','reject_negative_time','reject_unknown_role','reject_protocol_vehicle_preparation_or_grid_mismatch','reject_duplicate_or_empty_vehicle_assignments'],'experimental_rows':0,'formal_model_fitted':False,'human_review_status':'NOT_REVIEWED','change_applied':'NO','sha256':{x.relative_to(ROOT).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in inputs}}
    (HERE/'pilot_readiness.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(f'Preparation checks PASS; execution NOT_READY ({len(required)} unfilled fields); zero experimental rows.')
if __name__=='__main__':run()
