"""Resumable public Europe PMC search with complete capacity-route pagination."""
from pathlib import Path
import csv,json,urllib.request,urllib.parse,time,threading,concurrent.futures,hashlib,datetime,sys,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
LOCK=threading.Lock();NEXT=[0.0]
EXPANDED="--expanded-capacity" in sys.argv
ALIASES={}
OUTPUT=HERE/"inputs"/"expanded_capacity" if EXPANDED else HERE/"inputs"
OUTPUT.mkdir(parents=True,exist_ok=True)
def request(query,cursor,size):
 params=urllib.parse.urlencode(dict(query=query,format='json',resultType='lite',pageSize=size,cursorMark=cursor))
 url='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+params
 with LOCK:
  delay=max(0,NEXT[0]-time.monotonic())
  if delay:time.sleep(delay)
  NEXT[0]=time.monotonic()+.35
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=35) as response:return json.load(response)
  except Exception:
   if attempt==2:raise
   time.sleep(2*(attempt+1))
def work(item):
 candidate=item['candidate_id'];names=sorted({item['compound_name'],item['reference_name']}-{''})
 if EXPANDED:names=sorted(set(names+ALIASES.get(item['pubchem_cid'],[])))
 chemical='('+' OR '.join('TITLE_ABS:"'+name.replace('"','')+'"' for name in names)+')'
 routes={'broad':chemical+' AND (antioxidant OR antioxidative OR redox OR radical)','capacity':chemical+' AND (ORAC OR "oxygen radical absorbance" OR "crocin bleaching" OR "pyrogallol red" OR ABTS OR "Trolox equivalent")','food':chemical+' AND (food OR dietary OR edible OR nutrition OR fruit OR vegetable)'}
 if EXPANDED:routes={'capacity':routes['capacity']}
 for route,query in routes.items():
  path=OUTPUT/f'{candidate}_{route}.json'
  if path.exists():
   existing=json.loads(path.read_text(encoding='utf-8'))
   if existing.get('retrieval_status')=='SUCCESS' and existing.get('query')==query:continue
   history=HERE/'inputs/previous_queries';history.mkdir(exist_ok=True)
   previous=history/(path.stem+'_'+hashlib.sha256(existing.get('query','').encode()).hexdigest()[:12]+'.json')
   if not previous.exists():previous.write_bytes(path.read_bytes())
  records=[];cursor='*';pages=0;hit_count=None
  try:
   while True:
    data=request(query,cursor,1000 if route=='capacity' else 100);pages+=1;hit_count=data['hitCount'];batch=data.get('resultList',{}).get('result',[]);records.extend(batch)
    next_cursor=data.get('nextCursorMark')
    if route!='capacity' or not batch or not next_cursor or next_cursor==cursor or len(records)>=hit_count:break
    cursor=next_cursor
   payload=dict(candidate_id=candidate,route=route,query=query,database='Europe PMC',retrieved_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),hit_count=hit_count,records_retrieved=len(records),pages=pages,complete_result_retrieval=len(records)>=hit_count,metadata_mode='LITE',query_alias_scope='PUBCHEM_TOP12_SHORT_SYNONYMS_REVIEW_PENDING' if EXPANDED else 'CANONICAL_AND_REFERENCE_NAMES_ONLY_SYNONYM_EXPANSION_PENDING',retrieval_status='SUCCESS',records=records)
  except Exception as error:payload=dict(candidate_id=candidate,route=route,query=query,retrieval_status='FAILED',error=str(error),hit_count=hit_count,records_retrieved=len(records),records=records)
  temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(payload,ensure_ascii=False)+'\n',encoding='utf8',newline='\n');temporary.replace(path)
 return candidate

def audit(profiles):
 historical=ROOT/'02_identity_and_evidence/inputs/reference_collection/data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv'
 counts={}
 with historical.open(encoding='utf-8-sig') as handle:
  for row in csv.DictReader(handle):counts[row['candidate_id']]=counts.get(row['candidate_id'],0)+1
 rows=[]
 for item in profiles:
  for route in (['capacity'] if EXPANDED else ['broad','capacity','food']):
   path=OUTPUT/f"{item['candidate_id']}_{route}.json"
   data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
   rows.append(dict(candidate_id=item['candidate_id'],compound=item['compound_name'],route=route,historical_associations=counts.get(item['candidate_id'],0),query=data.get('query',''),status=data.get('retrieval_status','NOT_RUN'),hits=data.get('hit_count',''),retrieved=data.get('records_retrieved',0),complete_result_retrieval=data.get('complete_result_retrieval',False),alias_scope=data.get('query_alias_scope','QUERY_PENDING'),source_file=path.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ''))
 with (HERE/('Expanded_Capacity_Coverage_Audit.csv' if EXPANDED else 'Search_Coverage_Audit.csv')).open('w',encoding='utf8',newline='') as handle:
  writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 print(json.dumps(dict(candidates=len(profiles),searches=len(rows),success=sum(r['status']=='SUCCESS' for r in rows),failed=sum(r['status']=='FAILED' for r in rows))),flush=True)
def run():
 with (ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as handle:profiles=list(csv.DictReader(handle))
 if EXPANDED:
  synonym_data=json.loads((HERE/'PubChem_Synonym_Records.json').read_text(encoding='utf8'))
  for batch in synonym_data['batches']:
   for record in batch['records']:
    names=[]
    for name in record.get('Synonym',[]):
     if 2<=len(name)<=80 and name.lower() not in {'mg','ca','se','zn','cu','fe'} and not name.upper().startswith(('CHEBI:','SCHEMBL','DTXSID','CID ')) and not re.fullmatch(r'\d+',name):names.append(name)
     if len(names)==12:break
    ALIASES[str(record['CID'])]=names
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for number,candidate in enumerate(pool.map(work,profiles),1):
   if number%10==0:print('Completed candidates',number,flush=True)
 audit(profiles)
if __name__=='__main__':run()
