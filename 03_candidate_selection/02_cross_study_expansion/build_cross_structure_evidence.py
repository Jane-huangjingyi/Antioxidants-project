"""Recover independent source observations without changing candidate membership or models."""
import csv,hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
def write(name,rows):
    with (P/'results'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

c=json.loads((P/'inputs/carrasco_source_check.json').read_text(encoding='utf-8'))
rows=[]
for i,r in enumerate(c['records'],1):
    rows.append(dict(expansion_record_id=f'CARRASCO-{i:02d}',candidate_id=r['candidate_id'],compound=r['compound'],
        chemical_class_scope='MONOTERPENE_COMPONENT_PANEL',doi=c['doi'],source_url=c['source_url'],source_locator='Table 5 ORAC column; ORAC/statistical Methods',
        reported_value=r['mean'],reported_error=r['sd'] if r['sd'] is not None else '',error_type=c['error_type'],
        unit=c['unit'],value_qualifier=r['qualifier'],independent_n='',replication_scope=c['replication'],
        source_pH=c['pH'],source_temperature_C=c['temperature_C'],vehicle='1 percent ethanol',
        core_scope_status='OUTSIDE_PRIMARY_CORE_CONDITIONS',material_identity_status=c['material_limit'],
        existing_candidate_membership='YES' if r['candidate_id'] else 'NO_MEMBERSHIP_CHANGE_SOURCE_REFERENCE_ONLY',
        primary_model_eligible='NO',numeric_sampling_variance='',source_cache_sha256='',
        human_review_status='NOT_REVIEWED',change_applied='NO'))

raw=P/'inputs/PMC12534199_original_BioC.json'
d=json.loads(raw.read_text(encoding='utf-8'))[0]['documents'][0]
passages={r['offset']:r for r in d['passages']}
doi=d['passages'][0]['infons']['article-id_doi'];assert doi=='10.1002/fsn3.71092'
body=passages[18241]['text'].replace('\\u2009',' ')
caption=passages[18889]['text'];methods=passages[10443]['text']
assert 'four independent experiments' in caption and 'standard deviation' in caption
assert '37' in methods and '90' in methods
pattern=r'\b(GYDTQ|GY|VY|DTDYKKY|WYS|WY|LDQW|YW|GSH)\s*\(([0-9.]+)\s*±\s*([0-9.]+)'
values=re.findall(pattern,body)
assert len(values)==9 and len({r[0] for r in values})==9
sha=hashlib.sha256(raw.read_bytes()).hexdigest()
for name,mean,sd in values:
    rows.append(dict(expansion_record_id='SUZUKI-'+name,candidate_id='NEW-GSH' if name=='GSH' else '',compound='Glutathione' if name=='GSH' else name,
        chemical_class_scope='PEPTIDE_SOURCE_REFERENCE',doi=doi,source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC12534199/',
        source_locator='BioC offsets 18241,18889 (Fig 3 Results/caption); 10443 Methods; 5728 materials',
        reported_value=float(mean),reported_error=float(sd),error_type='SD_FIGURE_CAPTION',unit='umol TE/umol compound',value_qualifier='NUMERIC',
        independent_n=4,replication_scope='Four independent experiments as stated; shared calibration covariance unresolved',
        source_pH='',source_temperature_C=37,vehicle='Reported 10 percent methanol/water/acetic acid dilution; final well fraction unresolved',
        core_scope_status='CORE_CONDITIONS_NOT_FULLY_VERIFIED',material_identity_status='Reduced GSH catalogue reported; material basis pending' if name=='GSH' else 'Sequence reported; purity above 90 percent; termini/stereochemistry/material basis pending',
        existing_candidate_membership='YES' if name=='GSH' else 'NO_MEMBERSHIP_CHANGE_SOURCE_REFERENCE_ONLY',
        primary_model_eligible='NO',numeric_sampling_variance='',source_cache_sha256=sha,human_review_status='NOT_REVIEWED',change_applied='NO'))
assert 'VL did not exhibit' in body
row=rows[-1].copy();row.update(expansion_record_id='SUZUKI-VL',candidate_id='',compound='VL',reported_value='',reported_error='',
    value_qualifier='REPORTED_NO_ACTIVITY_NUMERIC_VALUE_NOT_GIVEN',independent_n='',
    replication_scope='No row-specific numeric estimate recovered',existing_candidate_membership='NO_MEMBERSHIP_CHANGE_SOURCE_REFERENCE_ONLY',
    material_identity_status='Sequence reported; termini/stereochemistry/material basis pending')
rows.append(row)
assert len(rows)==16 and len({r['expansion_record_id'] for r in rows})==16
assert sum(r['reported_value']!='' for r in rows)==15
assert all(r['primary_model_eligible']=='NO' for r in rows)
write('Cross_Structure_Evidence_Expansion.csv',rows)
summary=dict(original_papers_rechecked=2,source_observations=16,numeric_source_values=15,
    positive_numeric_values=sum(r['reported_value']!='' and r['reported_value']>0 for r in rows),
    reported_zero_values=1,reported_no_activity_without_numeric_value=1,existing_candidate_observations=3,
    observations_outside_current_candidate_membership=13,primary_labels_released=0,new_candidates_added=0,
    original_candidate_profiles_changed=0,new_records_used_for_model_refitting=False,
    statistical_independence='Original study observations reported; no cross-source raw-data reuse closure inferred from DOI',
    source_cache_sha256=sha)
(P/'results/cross_structure_expansion_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary))
