"""Explicit online recovery of two overlap-source leads; no model eligibility upgrade."""
from pathlib import Path
import urllib.request,json,hashlib
P=Path(__file__).resolve().parent
raw=P/'inputs/source_recovery/raw';raw.mkdir(parents=True,exist_ok=True)
log=[]
for doi,pmcid in [('10.3390/antiox11091784','PMC9495677'),('10.3390/ijms20092328','PMC6539043')]:
    url=f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmcid}/unicode'
    row=dict(doi=doi,pmcid=pmcid,url=url,access_date='2026-11-06')
    try:
        b=urllib.request.urlopen(url,timeout=30).read();doc=json.loads(b)[0]['documents'][0]
        assert str(doc['id']).replace('PMC','')==pmcid.replace('PMC','')
        assert len(doc['passages'])>10
        (raw/(pmcid+'.json')).write_bytes(b)
        row.update(status='RECOVERED_ARTICLE_TEXT_AND_TABLE_XML',sha256=hashlib.sha256(b).hexdigest(),passages=len(doc['passages']))
    except Exception as ex:row.update(status='NOT_RECOVERED',error=str(ex))
    log.append(row)
(P/'inputs/overlap_source_access.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8')
print(json.dumps(log,indent=2))
