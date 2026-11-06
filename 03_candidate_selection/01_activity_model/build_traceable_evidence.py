"""Link baseline observations to newer source checks without duplicating studies."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
def read(name):
    with (P/'results'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (P/'results'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
base=read('Observation_Readiness.csv')
models=read('Model_Input_Candidates.csv')
recovered=json.loads((P/'inputs/recovered_capacity_rows.json').read_text(encoding='utf-8-sig'))['records']
updates={(r['candidate_id'],r['doi']):r for r in recovered}
model={(r['candidate_id'],r['doi']):r for r in models}
rows=[]
for b in base:
    key=(b['candidate_id'],b['doi']);u=updates.get(key,{})
    rows.append(dict(b,doi_url='https://doi.org/'+b['doi'],latest_source_locator=u.get('source_locator',''),latest_source_url=u.get('source_url',''),latest_recheck_mean=u.get('reported_mean',''),latest_recheck_error_type=u.get('error_type',''),latest_recheck_scope='ARTICLE_TEXT_AND_TABLE_XML_NOT_SUPPLEMENTS' if u else 'BASELINE_INVENTORY',capacity_score='',capacity_rank='',score_status='NOT_FITTED_TARGET_CONDITIONS_AND_COMPARABILITY_PENDING'))
for u in recovered:
    if not any(r['candidate_id']==u['candidate_id'] and r['doi']==u['doi'] for r in rows):
        r={k:'' for k in rows[0]};r.update(candidate_id=u['candidate_id'],compound=u['compound'],doi=u['doi'],doi_url='https://doi.org/'+u['doi'],latest_source_locator=u['source_locator'],latest_source_url=u['source_url'],latest_recheck_mean=u['reported_mean'],latest_recheck_error_type=u['error_type'],latest_recheck_scope='ARTICLE_TEXT_AND_TABLE_XML_NOT_SUPPLEMENTS',score_status='NOT_FITTED_TARGET_CONDITIONS_AND_COMPARABILITY_PENDING',human_review_status='NOT_REVIEWED',change_applied='NO');rows.append(r)
assert len(rows)==len(base)+1
assert all(r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in rows)
for r in rows:
    if not r['doi']:r['doi_url']=''
write('Traceable_Capacity_Evidence.csv',rows)
summary=[]
for cid in sorted({r['candidate_id'] for r in rows}):
    group=[r for r in rows if r['candidate_id']==cid];m=[r for r in models if r['candidate_id']==cid]
    summary.append(dict(candidate_id=cid,compound=group[0]['compound'],observation_count=len(group),distinct_doi_count=len({r['doi'] for r in group}),doi_list='; '.join(sorted({r['doi'] for r in group})),rechecked_model_rows=len(m),conditional_variance_rows=sum(bool(r['variance_of_mean_candidate']) for r in m),independent_study_count='UNRESOLVED_NOT_EQUAL_TO_DOI_COUNT',predicted_molar_capacity='',standard_error='',capacity_score='',capacity_rank='',score_status='NOT_FITTED',human_review_status='NOT_REVIEWED',change_applied='NO'))
write('Candidate_Capacity_Summary.csv',summary)
print(f'Traceability PASS: {len(rows)} observations; {len(summary)} compounds; no scores invented.')
