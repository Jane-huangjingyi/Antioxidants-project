"""Unify reviewed annotations and expose source-local descriptive order only."""
import csv,collections,json,math
from pathlib import Path
P=Path(__file__).resolve().parent
def read(n):
    with (P/'results'/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(n,r):
    with (P/'results'/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(r[0]));w.writeheader();w.writerows(r)
latest={(r['candidate_id'],r['doi']):r for r in read('Model_Input_Candidates.csv')}
rows=[]
for original in read('Integrated_Capacity_Evidence.csv'):
    r=dict(original);m=latest.get((r['candidate_id'],r['doi']))
    verified=r['provenance']=='LEGACY30_ORIGINAL_RECHECK'
    if m and not verified:
        r.update(value=m['molar_mean_candidate'],scale='mol TE/mol compound',error=m['reported_plus_minus'],error_type=m['error_type'])
        locators={'10.3390/foods10081807':'Table 5; Methods 2.5.4 (supplementary calibration figures not inspected)','10.3390/antiox12020505':'Table 3; ORAC Methods','10.1016/j.foodchem.2010.11.092':'Table 1; statistical methods'}
        r['source_locator']=locators.get(r['doi'],r['source_locator'])
        verified=True
    comparable=verified and (r['provenance']=='LEGACY30_ORIGINAL_RECHECK' or r['doi']=='10.3390/foods10081807')
    r.update(doi_url='https://doi.org/'+r['doi'] if r['doi'] else '',latest_annotation_applied='YES' if m else 'NO',comparison_scope='SOURCE_LOCAL_DESCRIPTIVE_SUBSET' if comparable else 'SOURCE_RECHECKED_PROTOCOL_REVIEW' if verified else 'BASELINE_SOURCE_REVIEW_PENDING',global_capacity_score='',global_rank='',source_subset_rank='',ranking_interpretation='Point-estimate order only; no significance or global potency conclusion')
    rows.append(r)
groups=collections.defaultdict(list)
for r in rows:
    if r['comparison_scope']=='SOURCE_LOCAL_DESCRIPTIVE_SUBSET':
        try:v=float(r['value'])
        except (ValueError,TypeError):continue
        if math.isfinite(v):groups[(r['doi'],r['scale'],str(r['dose_uM']))].append(r)
ranked=[]
for key,group in groups.items():
    if len(group)<2:continue
    values=sorted({float(r['value']) for r in group},reverse=True)
    for r in group:
        r['source_subset_rank']=values.index(float(r['value']))+1
        ranked.append(dict(r,comparison_group=' | '.join(key),compounds_in_checked_subset=len(group),subset_warning='Not a complete source panel; not final experimental Top20'))
assert len(rows)==99
assert all(r['global_rank']=='' and r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in rows)
write('Capacity_Analysis_Entry.csv',rows)
write('Within_Source_Descriptive_Order.csv',ranked)
summary=dict(observations=len(rows),scope_counts=dict(collections.Counter(r['comparison_scope'] for r in rows)),ranked_subset_rows=len(ranked),ranked_subset_groups=len({r['comparison_group'] for r in ranked}),global_ranking_generated=False)
(P/'results/analysis_entry_qc.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
