"""Check search recall against existing DOI references without approving those references."""
from pathlib import Path
import csv,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as handle:return list(csv.DictReader(handle))
def run():
 links=read(HERE/'Candidate_Search_Hit_Links.csv')
 found={(r['candidate_id'],r['article_key']) for r in links if r['search_route']!='KNOWN_DOI_ANCHOR'}
 anchors={r['article_key'] for r in links if r['search_route']=='KNOWN_DOI_ANCHOR'}
 class_hits={r['article_key'] for r in links if r['search_route']=='CLASS_METHOD_CANDIDATE_ASSIGNMENT_PENDING'}
 references=read(ROOT/'03_candidate_selection/01_activity_model/results/Capacity_Analysis_Entry.csv')
 rows=[];seen=set()
 for r in references:
  if not r['doi']:continue
  key=(r['candidate_id'],r['doi'].strip().lower())
  if key in seen:continue
  seen.add(key)
  rows.append(dict(class_method_article_recovered='YES' if 'DOI:'+key[1] in class_hits else 'NO',known_anchor_metadata_recovered='YES' if 'DOI:'+key[1] in anchors else 'NO',candidate_id=key[0],reference_doi=key[1],retrieved_for_candidate='YES' if (key[0],'DOI:'+key[1]) in found else 'NO',reference_status='EXISTING_REFERENCE_NOT_INDEPENDENT_ELIGIBILITY_APPROVAL',next_action='SCREEN_RETRIEVED_RECORD' if (key[0],'DOI:'+key[1]) in found else 'CHECK_DATABASE_INDEXING_ALIASES_AND_CITATION_SEARCH'))
 with (HERE/'Known_Source_Recall_Audit.csv').open('w',encoding='utf8',newline='') as handle:
  writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 print(json.dumps(dict(existing_candidate_DOI_pairs=len(rows),retrieved_pairs=sum(r['retrieved_for_candidate']=='YES' for r in rows))))
if __name__=='__main__':run()
