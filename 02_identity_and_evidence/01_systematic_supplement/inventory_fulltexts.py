"""Locate recovered full-text tables and literal candidate-name hits for extraction."""
from pathlib import Path
import csv,xml.etree.ElementTree as ET,re,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def run():
 with (ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as f:profiles=list(csv.DictReader(f))
 with (HERE/'Method_Fulltext_Queue.csv').open(encoding='utf8') as f:queue=list(csv.DictReader(f))
 comparison_queue=HERE/'Compound_Comparison_Fulltext_Queue.csv'
 if comparison_queue.exists():
  with comparison_queue.open(encoding='utf8') as f:queue.extend(csv.DictReader(f))
 articles=[];tables=[];licenses=[];seen=set()
 for row in queue:
  if row['fulltext_recovery']!='PUBLIC_XML_RECOVERED_PENDING_READING':continue
  if row['PMCID'] in seen:continue
  seen.add(row['PMCID'])
  tree=ET.fromstring((HERE/row['source_file']).read_bytes());body=tree.find('.//body');text=' '.join(body.itertext()) if body is not None else ''
  hits=[p['candidate_id'] for p in profiles if any(re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',text,re.I) for name in {p['compound_name'],p['reference_name']} if name)]
  nodes=tree.findall('.//table-wrap')
  license_nodes=tree.findall('.//license')
  license_urls=sorted({value for node in license_nodes for child in node.iter() for key,value in child.attrib.items() if key.endswith('href')})
  licenses.append(dict(file=row['source_file'],license_type=';'.join(sorted({node.get('license-type','') for node in license_nodes})),license_urls=';'.join(license_urls),storage='LOCAL_CACHE_RETRIEVABLE_FROM_RECORDED_PUBLIC_URL',sha256=row['sha256']))
  articles.append(dict(article_key=row['article_key'],doi=row['doi'],PMCID=row['PMCID'],xml_article_type=tree.get('article-type',''),body_text_present='YES' if text else 'NO',table_count=len(nodes),literal_candidate_name_hits=';'.join(hits),name_hit_interpretation='SURFACE_MENTION_REQUIRES_FORM_AND_EXPERIMENT_VERIFICATION',source_file=row['source_file'],source_sha256=row['sha256'],human_review_status='NOT_REVIEWED',change_applied='NO'))
  for node in nodes:
   tables.append(dict(article_key=row['article_key'],doi=row['doi'],PMCID=row['PMCID'],xml_table_id=node.get('id',''),row_count=len(node.findall('.//tr')),source_file=row['source_file'],extraction_status='PENDING_ORIGINAL_VALUES_UNITS_ERRORS_AND_EXPERIMENTAL_UNIT_CHECK'))
 for name,data in [('Fulltext_Extraction_Readiness.csv',articles),('Fulltext_Table_Locators.csv',tables),('Fulltext_License_Inventory.csv',licenses)]:
  if not data:continue
  with (HERE/name).open('w',encoding='utf8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');writer.writeheader();writer.writerows(data)
 print(json.dumps(dict(recovered_articles=len(articles),located_tables=len(tables),articles_with_candidate_name_hits=sum(bool(r['literal_candidate_name_hits']) for r in articles))))
if __name__=='__main__':run()
