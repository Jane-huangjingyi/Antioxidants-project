"""Recover known DOI anchors and a broad method/class search for screening."""
from pathlib import Path
import csv,json,collections,hashlib,concurrent.futures
from retrieve import HERE,ROOT,request

def run():
 with (ROOT/'03_candidate_selection/01_activity_model/results/Capacity_Analysis_Entry.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
 groups=collections.defaultdict(set)
 for row in rows:
  if row['doi']:groups[row['doi'].lower()].add(row['candidate_id'])
 out=HERE/'inputs/known_anchors';out.mkdir(exist_ok=True)
 def recover(item):
  doi,candidates=item;query='DOI:"'+doi+'"'
  data=request(query,'*',100)
  for candidate in candidates:
   path=out/(candidate+'_'+hashlib.sha256(doi.encode()).hexdigest()[:12]+'.json')
   payload=dict(candidate_id=candidate,route='KNOWN_DOI_ANCHOR',query=query,retrieval_status='SUCCESS',hit_count=data['hitCount'],records_retrieved=len(data.get('resultList',{}).get('result',[])),records=data.get('resultList',{}).get('result',[]))
   path.write_text(json.dumps(payload,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(recover,groups.items()))
 print('Known DOI anchors queried',len(groups),flush=True)
 query='(flavonoid OR polyphenol OR phenolic OR vitamin OR carotenoid OR tocopherol OR thiol OR peptide) AND (ORAC OR "oxygen radical absorbance" OR "crocin bleaching" OR "pyrogallol red" OR "Trolox equivalent")'
 path=HERE/'inputs/class_method.json';records=[];cursor='*';pages=0
 while True:
  data=request(query,cursor,1000);batch=data.get('resultList',{}).get('result',[]);records.extend(batch);pages+=1
  next_cursor=data.get('nextCursorMark')
  if not batch or not next_cursor or next_cursor==cursor or len(records)>=data['hitCount']:break
  cursor=next_cursor
 payload=dict(candidate_id='',route='CLASS_METHOD_CANDIDATE_ASSIGNMENT_PENDING',query=query,retrieval_status='SUCCESS',hit_count=data['hitCount'],records_retrieved=len(records),pages=pages,complete_result_retrieval=len(records)>=data['hitCount'],records=records)
 path.write_text(json.dumps(payload,ensure_ascii=False)+'\n',encoding='utf8',newline='\n');print('Broad class/method records',len(records),flush=True)
if __name__=='__main__':run()
