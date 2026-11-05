"""Recover public Europe PMC source XML; keep source text local and hash each response."""
from pathlib import Path
import urllib.request,urllib.parse,json,hashlib,datetime,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;OUT=HERE/'inputs/source_recovery';RAW=OUT/'raw';RAW.mkdir(parents=True,exist_ok=True)
doi_list=['10.3390/antiox12020505','10.3390/foods10081807','10.3390/antiox14040479']
log=[]
for doi in doi_list:
 entry={'doi':doi,'access_date':'2026-11-05','provider':'Europe PMC public API'}
 try:
  query='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':'DOI:'+doi,'format':'json'})
  metadata=json.loads(urllib.request.urlopen(query,timeout=30).read());hits=metadata['resultList']['result'];pmcid=next(x['pmcid'] for x in hits if x.get('doi','').lower()==doi.lower() and x.get('pmcid'))
  url=f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML';b=urllib.request.urlopen(url,timeout=30).read();root=ET.fromstring(b)
  assert root.tag=='article','Unexpected response: not article XML'
  (RAW/(pmcid+'.xml')).write_bytes(b)
  entry.update(status='RECOVERED_PUBLIC_ARTICLE_XML',pmcid=pmcid,url=url,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),local_file='raw/'+pmcid+'.xml')
 except Exception as ex:
  entry.update(status='NOT_RECOVERED',error=type(ex).__name__)
  if getattr(ex,'code',None):entry['HTTP_status']=ex.code
 log.append(entry)
(OUT/'access_log.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf8')
print(json.dumps(log,indent=2))
