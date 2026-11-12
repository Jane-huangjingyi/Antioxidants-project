"""Merge historical and supplemental metadata using explicit DOI/PMID links."""
from pathlib import Path
import csv,json,hashlib,collections
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as handle:return list(csv.DictReader(handle))
def run():
 current=read(HERE/'Retrieved_Article_Register.csv')
 legacy_path=ROOT/'02_identity_and_evidence/inputs/reference_collection/data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv'
 legacy=read(legacy_path);parent={}
 def find(key):
  parent.setdefault(key,key)
  if parent[key]!=key:parent[key]=find(parent[key])
  return parent[key]
 def identifiers(row,historical=False):
  doi=row.get('DOI' if historical else 'doi','').strip().lower().replace('https://doi.org/','');pmid=row.get('PMID','').strip()
  tokens=[]
  if doi:tokens.append('DOI:'+doi)
  if pmid:tokens.append('PMID:'+pmid)
  if not tokens:
   if historical:tokens=['TITLE:'+hashlib.sha256(' '.join(row['paper_title'].lower().split()).encode()).hexdigest()]
   else:tokens=[row['article_key']]
  return tokens
 for data,historical in [(current,False),(legacy,True)]:
  for row in data:
   roots={find(key) for key in identifiers(row,historical)};chosen=min(roots)
   for key in roots:parent[key]=chosen
 master={};key_map={};source_types=collections.defaultdict(set)
 for row in current:
  root=find(identifiers(row)[0]);key_map[row['article_key']]=root
  if root not in master:master[root]=dict(row,article_key=root)
  source_types[root].add('PUBLIC_SUPPLEMENT')
 links=collections.defaultdict(set)
 for row in read(HERE/'Candidate_Search_Hit_Links.csv'):
  if row['candidate_id']:links[(row['candidate_id'],key_map[row['article_key']])].add('PUBLIC_QUERY_OR_REFERENCE_ANCHOR')
 for row in legacy:
  root=find(identifiers(row,True)[0]);source_types[root].add('HISTORICAL_PROVENANCE')
  if root not in master:
   item={key:'' for key in current[0]};item.update(article_key=root,doi=row['DOI'],PMID=row['PMID'],PMCID=row['PMCID'],title=row['paper_title'],journal=row['journal'],year=row['year'],metadata_source_file=legacy_path.relative_to(ROOT).as_posix(),screening_status='HISTORICAL_DECISIONS_RETAINED_IN_SOURCE_REQUIRE_SCOPE_RECONCILIATION',fulltext_status='NOT_VERIFIED_IN_SUPPLEMENT',IF_value='',IF_year='',IF_source='');master[root]=item
  links[(row['candidate_id'],root)].add('HISTORICAL_PROVENANCE')
 for key,item in master.items():item['retrieval_sources']=';'.join(sorted(source_types[key]))
 for name,data in [('Master_Article_Register.csv',list(master.values())),('Master_Candidate_Article_Links.csv',[dict(candidate_id=candidate,article_key=key,retrieval_sources=';'.join(sorted(sources)),human_review_status='NOT_REVIEWED',change_applied='NO') for (candidate,key),sources in sorted(links.items())])]:
  with (HERE/name).open('w',encoding='utf8',newline='') as handle:
   writer=csv.DictWriter(handle,fieldnames=list(data[0]),lineterminator='\n');writer.writeheader();writer.writerows(data)
 summary={'historical_associations':len(legacy),'supplement_identifier_groups':len(current),'merged_identifier_groups':len(master),'candidate_article_links':len(links),'overlap_identifier_groups':sum(len(v)==2 for v in source_types.values()),'journal_metadata_present':sum(bool(r['journal']) for r in master.values()),'deduplication_scope':'EXPLICIT_DOI_PMID_TITLE_FALLBACK_REQUIRES_CONFLICT_AND_NEAR_DUPLICATE_REVIEW','new_scientific_labels_approved':0}
 (HERE/'Retrieval_Summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(summary))
if __name__=='__main__':run()
