"""Deterministic leave-one-DOI-out influence of the descriptive reference order."""
from pathlib import Path
import csv,statistics,collections
HERE=Path(__file__).resolve().parent
def run():
 with (HERE/'results/Paper_Specific_Reference_Order.csv').open(encoding='utf8') as f:papers=list(csv.DictReader(f))
 with (HERE/'results/Exploratory_Literature_Reference_Order.csv').open(encoding='utf8') as f:baseline=list(csv.DictReader(f))
 dois=sorted({r['doi'] for r in papers});positions=collections.defaultdict(list);unsupported=collections.Counter();bounds=collections.defaultdict(list)
 for omitted in dois:
  groups=collections.defaultdict(list)
  for row in papers:
   if row['doi']!=omitted:groups[row['candidate_id']].append(float(row['paper_reference_median']))
  estimates={key:statistics.median(values) for key,values in groups.items()}
  for row in baseline:
   key=row['candidate_id']
   if key not in estimates:
    unsupported[key]+=1;bounds[key].append((1,len(baseline)));continue
   position=1+sum(value>estimates[key] for value in estimates.values())
   positions[key].append(position)
   bounds[key].append((position,position+len(baseline)-len(estimates)))
 rows=[]
 for row in baseline:
  ranks=positions[row['candidate_id']]
  rows.append(dict(candidate_id=row['candidate_id'],compound=row['compound'],baseline_reference_order=row['exploratory_reference_order'],source_DOI_count=row['source_papers'],omission_scenarios=len(dois),scenarios_without_remaining_source=unsupported[row['candidate_id']],fixed_universe_best_possible_order=min(x[0] for x in bounds[row['candidate_id']]),fixed_universe_worst_possible_order=max(x[1] for x in bounds[row['candidate_id']]),minimum_supported_reference_order=min(ranks),maximum_supported_reference_order=max(ranks),supported_scenarios_in_reference_top20=sum(rank<=20 for rank in ranks),interpretation='DETERMINISTIC_SOURCE_OMISSION_DIAGNOSTIC_VARIABLE_CANDIDATE_COVERAGE',human_review_status='NOT_REVIEWED',change_applied='NO'))
 with (HERE/'results/Source_Omission_Order_Diagnostic.csv').open('w',encoding='utf8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 print('Source-omission diagnostics:',len(rows),'candidates;',len(dois),'DOI omissions')
if __name__=='__main__':run()
