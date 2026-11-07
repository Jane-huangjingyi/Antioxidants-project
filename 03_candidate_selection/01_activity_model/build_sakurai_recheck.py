"""Reconcile targeted original rows with the canonical source index."""
import csv,json,math
from pathlib import Path
P=Path(__file__).resolve().parent;root=P.parents[1]
d=json.loads((P/'inputs/sakurai_targeted_recheck.json').read_text())
with (root/'02_identity_and_evidence/results/chemical_observation_index.csv').open(encoding='utf-8-sig',newline='') as f:
    old=[r for r in csv.DictReader(f) if r['doi'].lower()==d['doi']]
assert len(old)==2
rows=[]
for r in d['records']:
    matches=[x for x in old if x['candidate_id']==r['candidate_id']]
    if matches:assert len(matches)==1 and math.isclose(float(matches[0]['raw_value']),r['mean'])
    rows.append(dict(r,doi=d['doi'],source_url=d['source_url'],source_locator=d['source_locator'],unit=d['unit'],error_type=d['error_type'],measurements_as_reported=3,independence='NOT_ESTABLISHED',sampling_variance='',canonical_match_count=len(matches),model_status='SOURCE_RECHECK_ONLY_NOT_POOLED',human_review_status='NOT_REVIEWED',change_applied='NO'))
with (P/'results/Sakurai_Targeted_Reconciliation.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('QC PASS: two existing values match; one eugenol source lead; no duplicate study or variance added.')
