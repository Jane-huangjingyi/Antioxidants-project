"""Exploratory literature reference order using explicit molar entries only."""
from pathlib import Path
import csv,statistics,collections,math,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,rows):
 with p.open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def run():
 source=read(ROOT/'03_candidate_selection/01_activity_model/results/Capacity_Analysis_Entry.csv')
 profiles={r['candidate_id']:r for r in read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')}
 groups=collections.defaultdict(list);excluded=[]
 for r in source:
  reason=''
  if r['scale'] not in {'mol TE/mol compound','µmol Trolox/µmol compound'}:reason='SCALE_NOT_DIRECT_EXPLICIT_MOLAR_CAPACITY'
  elif not r['doi']:reason='SOURCE_DOI_MISSING'
  elif 'HOLD' in (r['pooling_status']+' '+r['comparison_scope']):reason='SOURCE_HOLD'
  try:value=float(r['value'])
  except ValueError:value=float('nan')
  if not math.isfinite(value) or value<0:reason='NONNUMERIC_OR_INVALID_CAPACITY'
  if reason:excluded.append(dict(candidate_id=r['candidate_id'],doi=r['doi'],value=r['value'],scale=r['scale'],reason=reason));continue
  groups[(r['candidate_id'],r['doi'])].append(value)
 papers=[dict(candidate_id=candidate,doi=doi,paper_reference_median=statistics.median(values),reference_rows=len(values)) for (candidate,doi),values in groups.items()]
 aggregate=collections.defaultdict(list)
 for r in papers:aggregate[r['candidate_id']].append(r)
 rows=[]
 for candidate,refs in aggregate.items():
  p=profiles[candidate];values=[r['paper_reference_median'] for r in refs]
  rows.append(dict(candidate_id=candidate,compound=p['compound_name'],reference_formula=p['molecular_formula'],reference_CID=p['pubchem_cid'],exploratory_reference_median_molar_TE=statistics.median(values),paper_min=min(values),paper_max=max(values),source_papers=len(refs),source_dois=';'.join(sorted(r['doi'] for r in refs)),food_source_status=p['food_occurrence_status'],material_status=p['chemical_form_and_lot_status'],interpretation='CROSS_PROTOCOL_DESCRIPTIVE_REFERENCE_ORDER_REQUIRES_SOURCE_AND_ASSAY_VALIDATION',human_review_status='NOT_REVIEWED',change_applied='NO'))
 rows.sort(key=lambda r:(-r['exploratory_reference_median_molar_TE'],r['candidate_id']))
 values=[r['exploratory_reference_median_molar_TE'] for r in rows]
 for r in rows:r['exploratory_reference_order']=1+sum(v>r['exploratory_reference_median_molar_TE'] for v in values)
 for r in papers:r['within_paper_reference_order']=1+sum(s['paper_reference_median']>r['paper_reference_median'] for s in papers if s['doi']==r['doi'])
 write(HERE/'results/Exploratory_Literature_Reference_Order.csv',rows)
 write(HERE/'results/Paper_Specific_Reference_Order.csv',papers)
 write(HERE/'results/Reference_Order_Excluded_Rows.csv',excluded)
 print(json.dumps({'ranked_candidates':len(rows),'candidate_paper_summaries':len(papers),'excluded_rows':len(excluded),'top_five':[r['compound'] for r in rows[:5]]}))
if __name__=='__main__':run()
