from pathlib import Path
import json,hashlib,subprocess,datetime,urllib.request,re,html
ROOT=Path(__file__).resolve().parents[3];PILOT=ROOT/'workspaces/phase1c_mechanism_evidence_pilot';OUT=PILOT/'gate2_review';SRC=OUT/'sources';SRC.mkdir(exist_ok=True)
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT).decode('utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,value):
 with p.open('x',encoding='utf-8') as f:f.write(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2))
if not (OUT/'Start_Baseline.json').exists():
 tracked=git('ls-files','-z').split('\0');put(OUT/'Start_Baseline.json',{'HEAD':git('rev-parse','HEAD'),'remote_main_checked':'f86aca02209d799367287082dea3d4438a224cd3','branch':git('branch','--show-current'),'initial_worktree':'CLEAN; verified before gate2_review creation','tracked_hashes':{x:sha(ROOT/x) for x in tracked if x},'existing_raw_cache_hashes':{x.relative_to(ROOT).as_posix():sha(x) for x in (PILOT/'search_logs/raw').iterdir() if x.is_file()},'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
events=[]
def fetch(name,url):
 p=SRC/name
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Antioxidants-project-scientific-review/0.1'}),timeout=40) as r:body=r.read();ctype=r.headers.get('Content-Type','')
  with p.open('xb') as f:f.write(body)
  events.append({'file':'sources/'+name,'url':url,'status':'RETRIEVED','bytes':len(body),'sha256':sha(p),'content_type':ctype,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});print(name,len(body),flush=True);return body
 except Exception as e:events.append({'file':'sources/'+name,'url':url,'status':'FAILED','error':str(e),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});print(name,str(e),flush=True);return None
fetch('RCSB_3GLS_entity1.json','https://data.rcsb.org/rest/v1/core/polymer_entity/3GLS/1')
fetch('RCSB_1JXJ_entity1.json','https://data.rcsb.org/rest/v1/core/polymer_entity/1JXJ/1')
fetch('TRAF2_repository.html','https://art.torvergata.it/handle/2108/470363')
fetch('TRAF2_publisher.html','https://www.sciencedirect.com/science/article/pii/S0003986126002080')
fetch('TRAF2_PubMed.xml','https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42413844&retmode=xml')
fetch('NRF2_Supplement.pdf','https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs10565-024-09953-7/MediaObjects/10565_2024_9953_MOESM1_ESM.pdf')
for pmc,label,fig in [('PMC11599353','NRF2','Fig6'),('PMC13187579','Amylase','gr2')]:
 body=fetch(label+'_PMC.html','https://pmc.ncbi.nlm.nih.gov/articles/'+pmc+'/')
 if body:
  text=body.decode('utf-8',errors='replace');imgs=re.findall(r'<img\b[^>]*?src=["\']([^"\']+)',text,re.I)
  found=[html.unescape(x) for x in imgs if fig.lower() in x.lower()]
  for idx,u in enumerate(found[:1]):
   if u.startswith('//'):u='https:'+u
   if u.startswith('/'):u='https://pmc.ncbi.nlm.nih.gov'+u
   fetch(label+'_Figure.png' if '.png' in u.lower() else label+'_Figure.jpg',u)
put(OUT/'Source_Access_Log.json',events)
