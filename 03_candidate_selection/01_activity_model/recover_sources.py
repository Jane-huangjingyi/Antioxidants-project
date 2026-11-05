"""Recover original article text through the public NCBI BioC API; keep text local."""
from pathlib import Path
import urllib.request,urllib.parse,json,hashlib,datetime,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;OUT=HERE/'inputs/source_recovery';RAW=OUT/'raw';RAW.mkdir(parents=True,exist_ok=True)
doi_ids={'10.3390/antiox12020505':'PMC9951910','10.3390/foods10081807':'PMC8392586','10.3390/antiox14040479':'PMC12024297'}
old={r['doi']:r for r in json.loads((OUT/'access_log.json').read_text(encoding='utf8'))} if (OUT/'access_log.json').exists() else {}
log=[]
for doi,pmcid in doi_ids.items():
 entry={'doi':doi,'access_date':'2026-11-05','provider':'NCBI public BioC API'}
 if doi in old:
  prior=old[doi];entry['prior_attempts']=prior.get('prior_attempts',[])
  if prior.get('status')=='NOT_RECOVERED':entry['prior_attempts'].append({k:v for k,v in prior.items() if k!='prior_attempts'})
 try:
  url=f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmcid}/unicode'
  b=urllib.request.urlopen(url,timeout=30).read();data=json.loads(b);doc=data[0]['documents'][0]
  assert str(doc['id']).replace('PMC','')==pmcid.replace('PMC',''),'Article identity mismatch'
  assert len(doc['passages'])>10,'Incomplete article text'
  (RAW/(pmcid+'.json')).write_bytes(b)
  entry.update(status='RECOVERED_PUBLIC_ARTICLE_BIOC',pmcid=pmcid,url=url,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),local_file='raw/'+pmcid+'.json',scope='Article text and text-encoded tables; not visual figure or supplementary-file inspection')
 except Exception as ex:
  entry.update(status='NOT_RECOVERED',error=type(ex).__name__)
  if getattr(ex,'code',None):entry['HTTP_status']=ex.code
 log.append(entry)
(OUT/'access_log.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf8')
print(json.dumps(log,indent=2))
