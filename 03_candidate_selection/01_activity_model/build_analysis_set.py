"""Pin analysis inputs and distinguish exploratory use from primary model eligibility.

No source records, approvals, labels, weights or scientific ranks are changed.
"""
import csv, hashlib, json, math
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent

def read(name):
    with (P/'results'/name).open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

inventory=read('Capacity_Analysis_Entry.csv')
labels=read('Flavonoid_Log_Capacity_Extraction.csv')
crosswalk={r['source_row']:r for r in read('Flavonoid_Candidate_Crosswalk.csv')}
external=read('External_Source_Validation_Queue.csv')
checks={(r['doi'],r['candidate_id']):r for r in read('External_Comparability_Decisions.csv')}
protocol=json.loads((P/'inputs/model_protocol_v0.1.json').read_text(encoding='utf-8'))
unset=[k for k,v in protocol['target_conditions'].items() if v is None and k not in protocol.get('stratification_fields',[])]
assert protocol['target_conditions']['pH']==7.4 and protocol['target_conditions']['temperature_C']==37
from protocol_scope import scope_index,classify
scope_lookup=scope_index()

devpairs={(r['doi'],crosswalk[r['source_row']]['candidate_id']) for r in labels if crosswalk[r['source_row']]['candidate_id']}
pressure={(r['doi'],r['candidate_id']) for r in read('Retrospective_Pressure_Test.csv')}
lineage={(r['doi'],r['candidate_id']):r for r in read('Protocol_Lineage_Check.csv')}
rows=[]

def add(uid,origin,cid,name,doi,locator,value,scale,source,check=None):
    category='WAIT_FOR_EVIDENCE';role='NO_MODEL_USE';superseded='NO'
    reasons=['COMMON_TARGET_MATERIAL_PROTOCOL_ESTIMAND_NOT_CLOSED']+(['FIXED_PRIMARY_TARGET_FIELD_UNSET'] if unset else [])
    condition=classify(cid,doi,scope_lookup)
    ph=condition['pH'];temp=condition['temperature_C'];scope=condition['status']
    inherited=lineage.get((doi,cid))
    if inherited:reasons.append('EXECUTED_SOP_VARIANT_FINAL_VEHICLE_AND_ESTIMATOR_UNRESOLVED')
    model_value='';model_scale=''
    if origin=='DEVELOPMENT_ORIGINAL_LOG_COLUMN':
        category='SENSITIVITY_ANALYSIS';role='PREVIOUSLY_AUTHORIZED_EXPLORATORY_STRUCTURE_MODEL'
        model_value=value;model_scale='REPORTED_LN_ORAC'
        reasons=['SINGLE_STUDY_DEVELOPMENT_ONLY','DATABASE_GRAPH_NOT_SOURCE_MATERIAL_APPROVAL','NO_FINAL_RANKING_AUTHORIZATION']
    elif origin=='CAPACITY_REFERENCE' and (doi,cid) in devpairs:
        category='REFERENCE_ONLY';superseded='YES';role='REFERENCE_ONLY_ORIGINAL_LOG_COLUMN_CONTROLS_MODEL_INPUT'
        reasons=['REFERENCE_REPRESENTATION_NOT_A_SECOND_MEASUREMENT','RETAINED_FOR_TRACEABILITY_NOT_ADDITIONAL_TRAINING_ROW']
    elif (doi,cid) in pressure:
        category='SENSITIVITY_ANALYSIS';role='AUTHORIZED_TWO_OBSERVATION_PROTOCOL_SHIFT_DIAGNOSTIC'
        reasons=['KNOWN_COMPOUND_RETROSPECTIVE_DIAGNOSTIC_ONLY','NO_TUNING_OR_FORMAL_EXTERNAL_VALIDATION']
    if check and check['unit_gate']=='CONDITIONAL_PARENT_MW_CONVERSION':
        reasons.append('CONDITIONAL_PARENT_MW_VALUE_NOT_RELEASED_AS_LABEL')
    rows.append(dict(analysis_record_id=uid,input_origin=origin,candidate_id=cid,compound=name,doi=doi,
        source_locator=locator,input_reference_value=value,input_reference_scale=scale,
        latest_verified_original_value=check['original_value'] if check else value if origin=='DEVELOPMENT_ORIGINAL_LOG_COLUMN' else '',
        latest_verified_original_unit=check['reported_unit'] if check else scale if origin=='DEVELOPMENT_ORIGINAL_LOG_COLUMN' else '',
        conditional_molar_value=check.get('conditional_mol_TE_per_mol','') if check else '',
        evidence_source=source,analysis_category=category,allowed_analysis_role=role,
        primary_model_eligible='NO',primary_core_scope_match=scope,source_pH=ph if ph is not None else '',source_temperature_C=temp if temp is not None else '',temperature_evidence_status=condition['basis'],vehicle_stratum=condition['vehicle_stratum'],integration_stratum=condition['window_stratum'],protocol_stratum_status='NOT_FULLY_CLOSED',secondary_reference_representation=superseded,
        reference_representation_match='',
        model_training_value=model_value,model_training_scale=model_scale,
        decision_reasons=';'.join(reasons),numeric_sampling_variance='',
        analysis_decision_status='CODEX_REPRODUCIBLE_DISPOSITION_NOT_HUMAN_APPROVAL',
        human_review_status='NOT_REVIEWED',change_applied='NO'))

for i,r in enumerate(inventory,1):
    check=checks.get((r['doi'],r['candidate_id']))
    add(f'CAPACITY-{i:03d}','CAPACITY_REFERENCE',r['candidate_id'],r['compound'],r['doi'],r['source_locator'],r['value'],r['scale'],'results/Capacity_Analysis_Entry.csv',check)
    if rows[-1]['secondary_reference_representation']=='YES':
        dev=next(x for x in labels if x['doi']==r['doi'] and crosswalk[x['source_row']]['candidate_id']==r['candidate_id'])
        assert 'Table 3' in r['source_locator'] and not r['dose_uM']
        v=float(r['value']);log=float(dev['reported_ln_orac'])
        relation='DIRECT_LOG_COLUMN_REFERENCE' if abs(v-log)<1e-9 else 'EXP_LOG_LOCATION_ROUNDED_REFERENCE' if abs(v-math.exp(log))<.001 else ''
        assert relation, 'Reference-to-original numeric relationship unresolved'
        rows[-1].update(reference_representation_match=relation,latest_verified_original_value=dev['reported_ln_orac'],latest_verified_original_unit='ln(ORAC)')
    if r['comparison_scope']=='SOURCE_IDENTITY_CONFLICT_DESCRIPTIVE_RANK_HELD':
        rows[-1].update(analysis_category='WAIT_FOR_EVIDENCE',allowed_analysis_role='SOURCE_IDENTITY_HOLD',
            decision_reasons='EXISTING_SOURCE_IDENTITY_HOLD;'+rows[-1]['decision_reasons'])
for r in labels:
    cw=crosswalk[r['source_row']]
    add('DEV-'+r['source_row'],'DEVELOPMENT_ORIGINAL_LOG_COLUMN',cw['candidate_id'],r['compound'],r['doi'],r['source_locator'],r['reported_ln_orac'],'ln(ORAC)','results/Flavonoid_Log_Capacity_Extraction.csv')
existing={(r['doi'],r['candidate_id']) for r in inventory}
for r in external:
    if (r['doi'],r['candidate_id']) in existing:continue
    add('EXTERNAL-'+r['candidate_id']+'-'+r['doi'],'ADDITIONAL_RECOVERED_SOURCE_ROW',r['candidate_id'],r['compound'],r['doi'],r['verified_original_locator'],r['original_value_verified'],r['original_verified_unit'],r['verified_source_url'],checks.get((r['doi'],r['candidate_id'])))

expansion_path=P.parent/'02_cross_study_expansion/results/Cross_Structure_Evidence_Expansion.csv'
with expansion_path.open(encoding='utf-8-sig') as f:expansion=list(csv.DictReader(f))
assert len(expansion)==16
for r in expansion:
    check=dict(original_value=r['reported_value'],reported_unit=r['unit'],conditional_mol_TE_per_mol='',unit_gate='NEW_STRUCTURE_SOURCE_REVIEW_PENDING')
    add('EXPANSION-'+r['expansion_record_id'],'CROSS_STRUCTURE_SOURCE_REFERENCE',r['candidate_id'],r['compound'],r['doi'],r['source_locator'],r['reported_value'],r['unit'],r['source_url'],check)
    rows[-1].update(primary_core_scope_match=r['core_scope_status'],source_pH=r['source_pH'],source_temperature_C=r['source_temperature_C'],temperature_evidence_status='NEW_ORIGINAL_SOURCE_RECORD',vehicle_stratum=r['vehicle'],source_value_qualifier=r['value_qualifier'],decision_reasons=rows[-1]['decision_reasons']+';'+r['material_identity_status']+';'+r['value_qualifier'])
for r in rows:r.setdefault('source_value_qualifier','AS_RECORDED_IN_INPUT')

assert len(inventory)==99 and len(labels)==36
assert len(rows)==len({r['analysis_record_id'] for r in rows})
assert sum(r['model_training_value']!='' for r in rows)==36
assert sum(r['allowed_analysis_role']=='AUTHORIZED_TWO_OBSERVATION_PROTOCOL_SHIFT_DIAGNOSTIC' for r in rows)==2
assert sum(r['allowed_analysis_role']=='SOURCE_IDENTITY_HOLD' for r in rows)==2
assert not any(r['primary_model_eligible']=='YES' for r in rows)
with (P/'results/Analysis_Set_Decisions.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
deps=['results/Capacity_Analysis_Entry.csv','results/Flavonoid_Log_Capacity_Extraction.csv',
      'results/Flavonoid_Candidate_Crosswalk.csv','results/External_Source_Validation_Queue.csv',
      'results/External_Comparability_Decisions.csv','results/Retrospective_Pressure_Test.csv',
      'results/Flavonoid_Scaffold_Groups.csv','results/Flavonoid_Structure_Audit.csv','results/Protocol_Lineage_Check.csv',
      'inputs/sakurai_targeted_recheck.json','inputs/recovered_capacity_rows.json','inputs/source_resolution.json','audit_protocol_lineage.py',
      'inputs/model_protocol_v0.1.json','requirements_structure.txt',
      'build_analysis_set.py','protocol_scope.py','check_model_protocol.py','build_extended_model_inputs.py','validate_scaffold_baseline.py','run_retrospective_pressure_test.py']
deps.extend(['../02_cross_study_expansion/results/Cross_Structure_Evidence_Expansion.csv','../02_cross_study_expansion/inputs/carrasco_source_check.json','../02_cross_study_expansion/inputs/PMC12534199_original_BioC.json','../02_cross_study_expansion/build_cross_structure_evidence.py'])
deps.extend('inputs/'+n for n in ['ishimoto_external_source_check.json','rothe_external_source_check.json',
    'carvalho_external_source_check.json','froldi_external_source_check.json','paillat_external_source_check.json'])
manifest=dict(version='0.1',scope='REPRODUCIBLE_ANALYSIS_DISPOSITION_NOT_SCIENTIFIC_APPROVAL',
    input_sha256={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in deps},
    inventory_reference_rows=len(inventory),development_original_rows=len(labels),
    additional_recovered_rows=len(rows)-len(inventory)-len(labels),
    cross_structure_expansion_rows=len(expansion),disposition_rows=len(rows),category_counts={c:sum(r['analysis_category']==c for r in rows) for c in ['PRIMARY_ANALYSIS','SENSITIVITY_ANALYSIS','WAIT_FOR_EVIDENCE','REFERENCE_ONLY']},
    role_counts=dict(Counter(r['allowed_analysis_role'] for r in rows)),
    superseded_reference_representations=sum(r['secondary_reference_representation']=='YES' for r in rows),
    primary_model_rows=0,primary_target_fields_unset=unset,confirmed_core_conditions={'pH':7.4,'temperature_C':37},stratification_fields=protocol['stratification_fields'],core_scope_counts=dict(Counter(r['primary_core_scope_match'] for r in rows)),
    missing_variance_policy='Undefined variance is not invented; it is not by itself a ban on unweighted modelling',
    primary_release_requirements=['Resolve source-specific vehicle, AUC estimator and integration strata under confirmed pH 7.4 and 37 C scope',
        'Verify numeric source, material/structure match, scale, data-generation independence and duplicate mapping',
        'Set validation acceptance criteria before evaluating new validation outcomes'],
    formal_human_approval_inferred=False,training_labels_changed=0,ranking_generated=False)
(P/'results/analysis_set_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in manifest.items() if k!='input_sha256'}))
