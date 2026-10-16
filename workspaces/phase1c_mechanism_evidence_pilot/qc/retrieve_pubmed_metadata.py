from pathlib import Path
import json,urllib.request,urllib.parse,datetime,time
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'workspaces/phase1c_mechanism_evidence_pilot';RAW=OUT/'search_logs/raw'
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Antioxidants-project/0.1'}),timeout=45) as r:return r.read()
def put(name,value):
 with (RAW/name).open('x',encoding='utf-8') as f:f.write(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2))
logs=[];ids=set(['32520409','37482908','41594941','42170612','39589556','26180584','41947015','37117448'])
for name,q in [('PUBMED02','"protocatechuic acid"[Title] AND TRAF2[Title/Abstract]'),('PUBMED03','"Physiological concentration of protocatechuic acid"[Title]'),('PUBMED04','"protocatechuic acid"[Title] AND "SIRT1/NF"[Title]')]:
 url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','term':q,'retmode':'json','retmax':100})
 try:
  data=json.loads(get(url));put(name+'_esearch.json',data);ids.update(data['esearchresult']['idlist']);logs.append({'search_id':name,'database':'PubMed','candidate_id':'AFF-0061','query':q,'search_date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hit_count':int(data['esearchresult']['count']),'retrieved_count':len(data['esearchresult']['idlist']),'status':'TARGETED_RETRIEVAL','api_urls':[url]});print(name,data['esearchresult']['idlist'],flush=True)
 except Exception as e:logs.append({'search_id':name,'database':'PubMed','query':q,'status':'FAILED','error':str(e)})
 time.sleep(.4)
url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','id':','.join(sorted(ids)),'retmode':'xml'})
text=get(url).decode('utf-8');put('Selected_PubMed_Metadata.xml',text);put('PubMed_Targeted_Logs.json',logs)
print('FETCHED',sorted(ids),len(text),flush=True)
