"""Optional network refresh. Default pipeline is offline and uses committed reference snapshots."""
from pathlib import Path
import sys,urllib.request,urllib.parse,json,time
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
queue=read_csv(ROOT/'03_candidate_selection/results/top20_review_queue.csv')
cache={};log=[];raw=ROOT/'02_identity_and_evidence/inputs/pubchem_raw';raw.mkdir(parents=True,exist_ok=True)
ids=','.join(r['pubchem_cid'] for r in queue)
url=f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{ids}/property/Title,MolecularFormula,MolecularWeight,InChIKey/JSON'
requests=[('review_panel',url)]+[(name,'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+urllib.parse.quote(name,safe='')+'/property/Title,MolecularFormula,MolecularWeight,InChIKey/JSON') for name in ['Glutathione','L-Ergothioneine']]
for label,url in requests:
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AntioxidantsProject/1.0 (research identity verification)'})
  with urllib.request.urlopen(req,timeout=45) as response:data=response.read()
  filename=label.replace(' ','_')+'.json';(raw/filename).write_bytes(data);parsed=json.loads(data);props=parsed['PropertyTable']['Properties']
  if label=='review_panel':
   byid={str(p['CID']):p for p in props}
   for r in queue:
    p=byid[r['pubchem_cid']];cache[r['compound_name']]={'status':'SUCCESS','property':p,'url':url,'access_date':AS_OF,'raw_path':str((raw/filename).relative_to(ROOT))}
  elif len(props)==1:cache[label]={'status':'SUCCESS','property':props[0],'url':url,'access_date':AS_OF,'raw_path':str((raw/filename).relative_to(ROOT))}
  else:cache[label]={'status':'AMBIGUOUS_NAME_QUERY','returned_count':len(props),'url':url}
  log.append({'label':label,'url':url,'access_date':AS_OF,'status':'SUCCESS','returned_count':len(props),'raw_sha256':sha(raw/filename)})
 except Exception as e:
  log.append({'label':label,'url':url,'access_date':AS_OF,'status':'ACCESS_FAILED','error_type':type(e).__name__,'error':str(e)})
 time.sleep(.25)
write_json(ROOT/'02_identity_and_evidence/inputs/pubchem_refresh.json',cache)
write_json(ROOT/'02_identity_and_evidence/inputs/pubchem_access_log.json',log)
print(json.dumps({'successful_names':len(cache),'requests':len(log),'failed_requests':sum(r['status']!='SUCCESS' for r in log)}))
