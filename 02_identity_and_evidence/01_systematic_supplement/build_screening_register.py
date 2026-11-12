"""Build article and candidate-hit registers from saved query responses."""
from pathlib import Path
import csv,json,collections
HERE=Path(__file__).resolve().parent

def run():
 articles={};links={};status=collections.Counter()
 parent={}
 def find(key):
  parent.setdefault(key,key)
  if parent[key]!=key:parent[key]=find(parent[key])
  return parent[key]
 def identifiers(record):
  doi=str(record.get('doi','')).strip().lower()
  pmid=str(record.get('pmid','')).strip()
  if not pmid and record.get('source')=='MED':pmid=str(record.get('id',''))
  tokens=[]
  if doi:tokens.append('DOI:'+doi)
  if pmid:tokens.append('PMID:'+pmid)
  tokens.append('SOURCE:'+str(record.get('source',''))+':'+str(record.get('id','')))
  return tokens
 paths=[p for p in sorted((HERE/'inputs').rglob('*.json')) if 'previous_queries' not in p.parts]
 for path in paths:
  payload=json.loads(path.read_text(encoding='utf8'))
  for record in payload.get('records',[]):
   roots={find(token) for token in identifiers(record)};chosen=min(roots)
   for root in roots:parent[root]=chosen

 for path in paths:
  if 'previous_queries' in path.parts:continue
  payload=json.loads(path.read_text(encoding='utf8'));status[payload['retrieval_status']]+=1
  for index,record in enumerate(payload.get('records',[])):
   doi=str(record.get('doi','')).strip().lower();pmid=str(record.get('pmid','')).strip()
   key=find(identifiers(record)[0])
   if not pmid and record.get('source')=='MED':pmid=str(record.get('id',''))
   if key not in articles:
    articles[key]=dict(article_key=key,doi=doi,PMID=pmid,PMCID=record.get('pmcid',''),title=record.get('title',''),ISSN=record.get('journalIssn',record.get('journalInfo',{}).get('journal',{}).get('issn','')),journal=record.get('journalTitle') or record.get('journalInfo',{}).get('journal',{}).get('title',''),year=record.get('pubYear',''),is_open_access=record.get('isOpenAccess',''),fulltext_locator='https://pmc.ncbi.nlm.nih.gov/articles/'+record.get('pmcid','')+'/' if record.get('pmcid') else '',publication_types=';'.join(record.get('pubTypeList',{}).get('pubType',[])) or record.get('pubType',''),abstract_available='YES' if record.get('abstractText') else 'NO',metadata_source_file=path.relative_to(HERE).as_posix(),source_record_index=index,screening_status='NOT_SCREENED',fulltext_status='NOT_CHECKED',IF_value='',IF_year='',IF_source='')
   link=(payload['candidate_id'],key,payload['route'],payload['query'])
   links[link]=dict(candidate_id=payload['candidate_id'],article_key=key,search_route=payload['route'],query=payload['query'],association_basis='CLASS_METHOD_CANDIDATE_ASSIGNMENT_PENDING' if not payload['candidate_id'] else 'KNOWN_REFERENCE_ANCHOR_REQUIRES_SOURCE_VERIFICATION' if payload['route']=='KNOWN_DOI_ANCHOR' else 'QUERY_MATCH_REQUIRES_IDENTITY_AND_RELEVANCE_SCREENING',human_review_status='NOT_REVIEWED',change_applied='NO')
 for name,data in [('Retrieved_Article_Register.csv',list(articles.values())),('Candidate_Search_Hit_Links.csv',list(links.values()))]:
  if not data:continue
  with (HERE/name).open('w',encoding='utf8',newline='') as handle:
   writer=csv.DictWriter(handle,fieldnames=list(data[0]),lineterminator='\n');writer.writeheader();writer.writerows(data)
 print(json.dumps(dict(saved_searches=sum(status.values()),search_status=dict(status),unique_identifier_keys=len(articles),candidate_route_links=len(links),journal_metadata_present=sum(bool(r['journal']) for r in articles.values()))))
if __name__=='__main__':run()
