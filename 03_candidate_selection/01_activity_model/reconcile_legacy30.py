"""Audit exactly 30 legacy rows; integrate source checks without approving pooling."""
import csv,json,math,collections
from pathlib import Path
P=Path(__file__).resolve().parent
def read(n):
    with (P/'results'/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(n,r):
    with (P/'results'/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(r[0]));w.writeheader();w.writerows(r)
targets=[r for r in read('Legacy_Quantitative_Coverage.csv') if r['coverage_status']=='NOT_MATCHED_IN_CURRENT_QUANTITATIVE_SUBSET' and r['assay']=='H-ORAC-FL']
assert len(targets)==30
# Original Table 1 targeted HTML rechecks; Table 2 BioC; Table 4 BioC.
verified={
'71':(5.475,.123,'Table 1','SD'), '74':(3.299,.235,'Table 1','SD'),
'112':(2.107,.070,'Table 1','SD'),'123':(1.811,.118,'Table 1','SD'),
'124':(.829,.259,'Table 1','SD'),'125':(.545,.152,'Table 1','SD'),'130':(1.131,.167,'Table 1','SD'),
'76':(2.17,.18,'Table 2 ORAC column','UNDEFINED_PLUS_MINUS'),
'77':(3.44,.19,'Table 2 ORAC column','UNDEFINED_PLUS_MINUS'),
'78':(1.52,.11,'Table 2 ORAC column','UNDEFINED_PLUS_MINUS'),
'94':(1.47,.10,'Table 4 ORAC column; 3-CQA (1)','SD_N_AT_LEAST_3'),
'95':(3.54,.11,'Table 4 ORAC column; 4-CQA (3)','SD_N_AT_LEAST_3'),
'97':(3.26,.10,'Table 4 ORAC column; 3,4-diCQA (4)','SD_N_AT_LEAST_3'),
'98':(2.13,.07,'Table 4 ORAC column; 3,5-diCQA (5)','SD_N_AT_LEAST_3'),
'99':(3.70,.34,'Table 4 ORAC column; 4,5-diCQA (6)','SD_N_AT_LEAST_3')}
doses={'84':[(29,1),(53,0)],'86':[(26,1),(56,1)],'87':[(29,2),(40,1)]}
base=read('Traceable_Capacity_Evidence.csv')
fields=['candidate_id','compound','doi','source_locator','value','scale','error','error_type','dose_uM','provenance','pooling_status','human_review_status','change_applied']
integrated=[dict(zip(fields,[r['candidate_id'],r['compound'],r['doi'],r['source_location'],r['molar_value_in_existing_table'],r['unit_as_reported'],r['error_value_as_reported'],r['error_type'],'','BASELINE_WITH_RECHECK_LINKS_IN_TRACEABLE_TABLE','NOT_APPROVED_FOR_POOLING','NOT_REVIEWED','NO'])) for r in base]
audit=[]
for r in targets:
    k=r['legacy_csv_row'];new=[];status='SOURCE_PENDING';locator=r['source_locator'];reason='Original numerical table unavailable this round; retain legacy value without verification'
    if k in verified:
        v,e,locator,et=verified[k];assert math.isclose(v,float(r['original_value']),abs_tol=1e-9)
        new=[(v,e,'mol TE/mol compound',et,'')];status='ORIGINAL_VALUE_RECHECKED';reason='Original value matches; independent batches and protocol equivalence remain unresolved'
    elif k in doses:
        locator='Table 2 ORAC columns at 2.5 and 5 micromolar compound'
        new=[(v/d,e/d,'conditional mol TE/mol compound','UNDEFINED_PLUS_MINUS',d) for d,(v,e) in zip([2.5,5],doses[k])]
        status='DOSE_SPECIFIC_RECHECKED';reason='Two concentrations in one study; no averaging; zero rounded error is not zero variance'
    elif k=='37':
        a=next(x for x in read('Flavonoid_Log_Capacity_Extraction.csv') if x['compound']=='Eriodictyol')
        new=[(float(a['reported_ln_orac']),float(a['reported_plus_minus_log_scale']),'ln(ORAC)','UNDEFINED_PLUS_MINUS','')]
        status='SCALE_CONFLICT_RESOLVED_IN_DERIVED_ROW';locator='Table 3 experimental ln(ORAC), Eriodictyol';reason='Legacy 7.486 approximately exp(2.013); retain original 2.013 log location, do not exponentiate legacy value'
    for v,e,scale,et,dose in new:
        integrated.append(dict(zip(fields,[r['proposed_current_candidate_id'],r['compound'],r['doi'],locator,v,scale,e,et,dose,'LEGACY30_ORIGINAL_RECHECK','NOT_APPROVED_FOR_POOLING','NOT_REVIEWED','NO'])))
    audit.append(dict(r,verification_status=status,verified_locator=locator,derived_rows=len(new),duplicate_relationship='Existing legacy source contribution; never count extraction as a new study',decision_reason=reason,human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(audit)==30 and len(integrated)==99
assert len({(r['candidate_id'],r['doi'],str(r['dose_uM'])) for r in integrated[77:]})==22
write('Legacy30_Verification.csv',audit);write('Integrated_Capacity_Evidence.csv',integrated)
# Connectivity is provenance-only; methods and scales are deliberately not pooled.
edges={(r['candidate_id'],r['doi'].lower()) for r in integrated if r['provenance']=='LEGACY30_ORIGINAL_RECHECK'}
edges|={(r['candidate_id'],r['doi'].lower()) for r in read('Model_Input_Candidates.csv')}
edges|={(r['candidate_id'],r['doi'].lower()) for r in read('Overlap_Dose_Diagnostic.csv')}
edges|={(r['candidate_id'],r['doi'].lower()) for r in read('Quercetin_Cross_Paper_Compatibility.csv')}
g=collections.defaultdict(set)
for c,d in edges:g['C:'+c].add('D:'+d);g['D:'+d].add('C:'+c)
seen={};component=0
for node in sorted(g):
    if node in seen:continue
    component+=1;stack=[node]
    while stack:
        x=stack.pop()
        if x in seen:continue
        seen[x]=component;stack.extend(g[x]-seen.keys())
write('Integrated_Source_Connectivity.csv',[dict(node=n,component=seen[n],degree=len(g[n]),interpretation='SOURCE_OVERLAP_ONLY_NOT_COMMON_EFFECT_ELIGIBILITY') for n in sorted(g)])
summary=dict(target_records=30,original_rechecked_records=sum(r['derived_rows']>0 for r in audit),source_pending_records=sum(r['derived_rows']==0 for r in audit),integrated_observations=len(integrated),new_verified_derived_rows=22,source_overlap_components=component,source_overlap_compounds=sum(n.startswith('C:') for n in g),source_overlap_papers=sum(n.startswith('D:') for n in g),model_input_candidates_unchanged=9,formal_ranking_generated=False)
(P/'results/legacy30_qc.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
