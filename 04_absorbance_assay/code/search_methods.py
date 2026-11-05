"""Optional bounded primary-discovery refresh; never silently update reviewed method decisions."""
from pathlib import Path
import sys,urllib.request,urllib.parse,json,time
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
queries={
 'recent_pgr':'"pyrogallol red" AND (ORAC OR antioxidant) AND FIRST_PDATE:[2024-01-01 TO 2026-11-05]',
 'recent_crocin':'"crocin bleaching" AND FIRST_PDATE:[2024-01-01 TO 2026-11-05]',
 'absorbance_automation':'(ORAC AND (absorbance OR colorimetric OR spectrophotometric)) AND (microplate OR automation)'
}
out=ROOT/'04_absorbance_assay/inputs/searches';out.mkdir(parents=True,exist_ok=True);log=[];hits=[]
for key,query in queries.items():
 url='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':query,'format':'json','pageSize':100,'resultType':'core'})
 try:
  with urllib.request.urlopen(url,timeout=45) as resp:b=resp.read()
  (out/(key+'.json')).write_bytes(b);d=json.loads(b);results=d.get('resultList',{}).get('result',[])
  log.append({'search_id':key,'query':query,'date':AS_OF,'url':url,'hit_count':d.get('hitCount',0),'retrieved':len(results),'complete_first_page':'YES' if d.get('hitCount',0)<=100 else 'NO_FIRST_PAGE_ONLY','sha256':sha(out/(key+'.json')),'status':'SUCCESS'})
  for r in results:hits.append({'search_id':key,'title':r.get('title',''),'doi':r.get('doi',''),'pmid':r.get('id','') if r.get('source')=='MED' else '','year':r.get('pubYear',''),'publication_type':'; '.join(r.get('pubTypeList',{}).get('pubType',[])),'source_url':'https://europepmc.org/article/'+r.get('source','')+'/'+r.get('id',''),'review_status':'DISCOVERY_ONLY_NOT_SCIENTIFIC_APPROVAL'})
 except Exception as e:log.append({'search_id':key,'query':query,'date':AS_OF,'url':url,'status':'ACCESS_FAILED','error':str(e)})
 time.sleep(.3)
write_json(out/'search_log.json',log)
if hits:write_csv(ROOT/'04_absorbance_assay/results/method_search_hits.csv',hits)
print(json.dumps({'queries':len(log),'successful':sum(r['status']=='SUCCESS' for r in log),'discovery_hits_with_repeated_query_matches':len(hits)}))
