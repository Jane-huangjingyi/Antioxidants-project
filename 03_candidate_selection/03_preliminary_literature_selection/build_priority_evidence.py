"""Expose existing protocol dispositions for the detection-review subset."""
from pathlib import Path
import csv,json,collections
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as handle:return list(csv.DictReader(handle))
def run():
 candidates=read(HERE/'results/Detection_Candidate_Assessment.csv')
 priority={r['candidate_id']:r for r in candidates if r['review_role']!='ADDITIONAL_EVIDENCE_REVIEW'}
 decisions=read(ROOT/'03_candidate_selection/01_activity_model/results/Analysis_Set_Decisions.csv')
 rows=[]
 for r in decisions:
  if r['candidate_id'] not in priority:continue
  rows.append(dict(review_role=priority[r['candidate_id']]['review_role'],**r))
 assert len({r['analysis_record_id'] for r in rows})==len(rows)
 with (HERE/'results/Priority_Source_Comparability.csv').open('w',encoding='utf8',newline='') as handle:
  writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 covered={r['candidate_id'] for r in rows}
 summary={'priority_candidates':len(priority),'mapped_priority_candidates':len(covered),'priority_provenance_rows':len(rows),'analysis_categories':dict(collections.Counter(r['analysis_category'] for r in rows)),'primary_eligible_rows':sum(r['primary_model_eligible']=='YES' for r in rows),'priority_candidates_without_disposition':[key for key in priority if key not in covered],'new_source_checks':0,'human_review_status':'NOT_REVIEWED','change_applied':'NO'}
 (HERE/'results/priority_evidence_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n')
 print(json.dumps(summary))
if __name__=='__main__':run()
