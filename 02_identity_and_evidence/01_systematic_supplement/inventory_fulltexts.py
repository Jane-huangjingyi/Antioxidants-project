"""Locate recovered full-text tables and literal candidate-name hits for extraction."""
from pathlib import Path
import csv,xml.etree.ElementTree as ET,re,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def run():
 with (ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as f:profiles=list(csv.DictReader(f))
 with (HERE/'Method_Fulltext_Queue.csv').open(encoding='utf8') as f:queue=list(csv.DictReader(f))
 articles=[];tables=[]
 for row in queue:
  if row['fulltext_recovery']!='PUBLIC_XML_RECOVERED_PENDING_READING':continue
  tree=ET.fromstring((HERE/row['source_file']).read_bytes());body=tree.find('.//body');text=' '.join(body.itertext()) if body is not None else ''
  hits=[p['candidate_id'] for p in profiles if any(re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',text,re.I) for name in {p['compound_name'],p['reference_name']} if name)]
  nodes=tree.findall('.//table-wrap')
  articles.append(dict(article_key=row['article_key'],doi=row['doi'],PMCID=row['PMCID'],xml_article_type=tree.get('article-type',''),body_text_present='YES' if text else 'NO',table_count=len(nodes),literal_candidate_name_hits=';'.join(hits),name_hit_interpretation='SURFACE_MENTION_REQUIRES_FORM_AND_EXPERIMENT_VERIFICATION',source_file=row['source_file'],source_sha256=row['sha256'],human_review_status='NOT_REVIEWED',change_applied='NO'))
  for node in nodes:
   tables.append(dict(article_key=row['article_key'],doi=row['doi'],PMCID=row['PMCID'],xml_table_id=node.get('id',''),row_count=len(node.findall('.//tr')),source_file=row['source_file'],extraction_status='PENDING_ORIGINAL_VALUES_UNITS_ERRORS_AND_EXPERIMENTAL_UNIT_CHECK'))
 for name,data in [('Fulltext_Extraction_Readiness.csv',articles),('Fulltext_Table_Locators.csv',tables)]:
  if not data:continue
  with (HERE/name).open('w',encoding='utf8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');writer.writeheader();writer.writerows(data)
 print(json.dumps(dict(recovered_articles=len(articles),located_tables=len(tables),articles_with_candidate_name_hits=sum(bool(r['literal_candidate_name_hits']) for r in articles))))
if __name__=='__main__':run()
