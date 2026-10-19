from pathlib import Path
import urllib.request,json,datetime,hashlib
OUT=Path(__file__).resolve().parent
ids='32520409,37482908,39589556,41594941,42170612,37025617,42413844,32007785,11023549,11714376'
url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id='+ids
with urllib.request.urlopen(url,timeout=40) as r:b=r.read()
p=OUT/'sources/Current_10_Study_PubMed.xml'
with p.open('xb') as f:f.write(b)
with (OUT/'Metadata_Refresh_Log.json').open('x',encoding='utf-8') as f:json.dump({'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'local_cache':'sources/Current_10_Study_PubMed.xml','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},f,indent=2)
print('CURRENT_PUBMED_BYTES',len(b))
