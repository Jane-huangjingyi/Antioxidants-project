"""Read-only public-source retrieval; writes exclusively to this pilot workspace."""
from pathlib import Path
import urllib.request, urllib.parse, json, csv, hashlib, subprocess, datetime, time
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'workspaces/phase1c_mechanism_evidence_pilot'
RAW=OUT/'search_logs/raw'; RAW.mkdir(parents=True,exist_ok=True)
def put(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x',encoding='utf-8') as f:f.write(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2))
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Antioxidants-project-scientific-pilot/0.1'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.read()
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT).decode().strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=OUT/'qc/Start_Baseline.json'
if not baseline.exists():
 paths=git('ls-files','-z').split('\0')
 put(baseline,{'HEAD':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'initial_worktree_before_pilot_creation':'CLEAN; recorded by initial terminal read','execution_status':git('status','--short'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tracked_file_sha256':{p:sha(ROOT/p) for p in paths if p}})
queries={
 'EPMC01':'(TITLE_ABS:"protocatechuic acid" OR TITLE_ABS:"3,4-dihydroxybenzoic acid" OR TITLE_ABS:"3,4 dihydroxybenzoic acid") AND FIRST_PDATE:[1900-01-01 TO 2026-10-16]',
 'EPMC02':'(TITLE_ABS:"protocatechuic acid" OR TITLE_ABS:"3,4-dihydroxybenzoic acid") AND (TITLE_ABS:knockdown OR TITLE_ABS:knockout OR TITLE_ABS:siRNA OR TITLE_ABS:rescue OR TITLE_ABS:binding OR TITLE_ABS:docking OR TITLE_ABS:inhibitor OR TITLE_ABS:target) AND FIRST_PDATE:[1900-01-01 TO 2026-10-16]',
 'EPMC03':'DOI:10.1038/s43016-021-00243-7',
 'EPMC04':'TITLE:"Protocatechuic acid promotes c-Myc-mediated cell proliferation by directly targeting TRAF2"',
}
logs=[]
for qid,query in queries.items():
 resultpath=RAW/(qid+'_results.json')
 if resultpath.exists():
  data=json.loads(resultpath.read_text(encoding='utf-8'));logs.append(data['log']);continue
 cursor='*'; results=[]; urls=[]; total=None
 try:
  while True:
   url='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':query,'format':'json','resultType':'core','pageSize':1000,'cursorMark':cursor})
   body=json.loads(get(url));urls.append(url);total=body['hitCount'];batch=body.get('resultList',{}).get('result',[]);results.extend(batch)
   nxt=body.get('nextCursorMark')
   if not batch or len(results)>=total or not nxt or nxt==cursor:break
   cursor=nxt
  log={'search_id':qid,'candidate_id':'AFF-0061' if qid not in ['EPMC03'] else 'NOT_APPLICABLE','database':'Europe PMC','search_date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cutoff_date':'2026-10-16','query':query,'hit_count':total,'retrieved_count':len(results),'api_urls':urls,'status':'RETRIEVED','purpose':'DISCOVERY_NOT_ALL_SCREENED' if qid in ['EPMC01','EPMC02'] else 'REFERENCE_METADATA_CHECK'}
  put(resultpath,{'log':log,'results':results});logs.append(log);print(qid,total,len(results),flush=True)
 except Exception as e:
  log={'search_id':qid,'database':'Europe PMC','query':query,'status':'FAILED','error':str(e),'search_date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};put(RAW/(qid+'_retry_error.json'),log);logs.append(log);print(log,flush=True)
query='("protocatechuic acid"[Title/Abstract] OR "3,4-dihydroxybenzoic acid"[Title/Abstract] OR "3,4 dihydroxybenzoic acid"[Title/Abstract]) AND ("1900/01/01"[Date - Publication] : "2026/10/16"[Date - Publication])'
pubpath=RAW/'PUBMED01_esearch.json'
if not pubpath.exists():
 url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','term':query,'retmode':'json','retmax':10000})
 try:
  body=json.loads(get(url));put(pubpath,body);logs.append({'search_id':'PUBMED01','candidate_id':'AFF-0061','database':'PubMed','search_date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'query':query,'hit_count':int(body['esearchresult']['count']),'retrieved_count':len(body['esearchresult']['idlist']),'api_urls':[url],'status':'IDS_RETRIEVED_NOT_ALL_SCREENED','cutoff_date':'2026-10-16'});print('PUBMED',body['esearchresult']['count'],flush=True)
 except Exception as e:logs.append({'search_id':'PUBMED01','database':'PubMed','query':query,'status':'FAILED','error':str(e)})
else:
 body=json.loads(pubpath.read_text(encoding='utf-8'));logs.append({'search_id':'PUBMED01','candidate_id':'AFF-0061','database':'PubMed','query':query,'hit_count':int(body['esearchresult']['count']),'retrieved_count':len(body['esearchresult']['idlist']),'status':'IDS_RETRIEVED_NOT_ALL_SCREENED','cutoff_date':'2026-10-16'})
if not (RAW/'PubChem_CID72.json').exists():
 url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/72/property/MolecularFormula,InChIKey,IUPACName/JSON'
 try:put(RAW/'PubChem_CID72.json',{'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'response':json.loads(get(url))});print('PUBCHEM_OK',flush=True)
 except Exception as e:put(RAW/'PubChem_error.json',{'url':url,'error':str(e)})
allres=[]
for qid in ['EPMC01','EPMC02','EPMC04']:
 p=RAW/(qid+'_results.json')
 if p.exists():allres.extend(json.loads(p.read_text(encoding='utf-8'))['results'])
selected=[]
for r in allres:
 title=r.get('title','').lower()
 if any(x in title for x in ['sirtuin 3','kynurenine-3','relieves ferroptosis','histone deacetylase 1/gata','astringency perception mechanism','physiological concentration of protocatechuic','promotes c-myc','prevents oxldl-induced apoptosis','inhibits inflammatory responses in lps-activated bv2']):
  if r.get('id') not in [x.get('id') for x in selected]:selected.append(r)
if not (RAW/'Selected_Metadata_Retry.json').exists():put(RAW/'Selected_Metadata_Retry.json',selected)
pmcs=set(['PMC10424289','PMC7443473','PMC12837532','PMC13187579']) | {r['pmcid'] for r in selected if r.get('pmcid')}
for pmc in sorted(pmcs):
 p=RAW/(pmc+'.xml')
 if p.exists():continue
 url=f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML'
 try:
  text=get(url).decode('utf-8');ET.fromstring(text);put(p,text);print('FULLTEXT',pmc,len(text),flush=True)
 except Exception as e:put(RAW/(pmc+'_retry_access_error.json'),{'url':url,'error':str(e)});print('FULLTEXT_FAILED',pmc,str(e),flush=True)
if not (RAW/'Retrieval_Logs_Retry.json').exists():put(RAW/'Retrieval_Logs_Retry.json',logs)
for r in selected:print(json.dumps({k:r.get(k) for k in ['id','pmcid','doi','firstPublicationDate','title']},ensure_ascii=True),flush=True)
