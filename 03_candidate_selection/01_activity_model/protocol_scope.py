"""Source-specific core-condition lookup shared by analysis and fold diagnostics."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent

def read_json(name):return json.loads((P/'inputs'/name).read_text(encoding='utf-8'))

def scope_index():
    index={}
    for r in read_json('recovered_capacity_rows.json')['records']:
        index[(r['doi'],r['candidate_id'])]=dict(pH=r['pH'],temperature_C=r['temperature_C'],basis='DIRECT_SOURCE_RECORD')
    r=next(r for r in read_json('source_resolution.json')['records'] if r['observation_id']=='HORAC_EXP_0068')
    index[(r['doi'],'AFF-0085')]=dict(pH=r['pH'],temperature_C=r['temperature_C'],basis='DIRECT_SOURCE_RECORD')
    for stem in ['ishimoto','rothe','carvalho','froldi','paillat']:
        c=read_json(stem+'_external_source_check.json')
        for r in c['records']:
            index[(c['doi'],r['candidate_id'])]=dict(pH=c['protocol'].get('pH'),temperature_C=c['protocol'].get('temperature_C'),basis='DIRECT_SOURCE_RECORD_OR_UNRESOLVED')
    with (P/'results/Protocol_Lineage_Check.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            index[(r['doi'],r['candidate_id'])]=dict(pH=float(r['directly_reported_pH']),temperature_C=float(r['inherited_shared_temperature_C']),basis='SHARED_CITED_SOP_RUN_PENDING')
    return index

def classify(cid,doi,index):
    r=dict(index.get((doi,cid),dict(pH=None,temperature_C=None,basis='UNRESOLVED')))
    if doi=='10.3390/ijms20092328':r=dict(pH=7.4,temperature_C=37,basis='DIRECT_SOURCE_METHODS')
    ph=r['pH'];t=r['temperature_C']
    if (ph is not None and ph!=7.4) or (t is not None and t!=37):status='OUTSIDE_PRIMARY_CORE_CONDITIONS'
    elif ph==7.4 and t==37:
        status='CORE_CONDITIONS_SUPPORTED_BY_SHARED_SOP_RUN_CONFIRMATION_PENDING' if r['basis']=='SHARED_CITED_SOP_RUN_PENDING' else 'MATCH_CORE_CONDITIONS_PROTOCOL_STRATUM_PENDING'
    else:status='CORE_CONDITIONS_NOT_FULLY_VERIFIED'
    r['status']=status
    r['vehicle_stratum']='UNRESOLVED'
    if doi=='10.3390/antiox12020505':
        if cid in {'AFF-0009','AFF-0069'}:r['vehicle_stratum']='FINAL_ETHANOL_5_PERCENT_MATCHED_TROLOX'
        elif cid in {'AFF-0104','NEW-GSH'}:r['vehicle_stratum']='AQUEOUS_PREPARATION_NO_ADDED_ORGANIC_REPORTED'
        elif cid=='AFF-0060':r['vehicle_stratum']='GALLIC_STOCK_SOLVENT_DESCRIPTIONS_CONFLICT'
    # Recording duration is not silently substituted for the estimator's integration window.
    r['window_stratum']='SOURCE_SPECIFIC_WINDOW_NOT_CLOSED'
    return r
