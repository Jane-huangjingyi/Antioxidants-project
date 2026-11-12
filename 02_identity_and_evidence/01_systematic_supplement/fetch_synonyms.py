"""Retrieve PubChem synonym metadata by the current reference CIDs."""
from pathlib import Path
import csv,json,urllib.request,concurrent.futures,datetime
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def run():
 with (ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as handle:rows=list(csv.DictReader(handle))
 cids=sorted({r['pubchem_cid'] for r in rows if r['pubchem_cid']})
 def fetch(chunk):
  url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/'+','.join(chunk)+'/synonyms/JSON'
  try:
   with urllib.request.urlopen(url,timeout=35) as response:data=json.load(response)
   return dict(status='SUCCESS',url=url,records=data.get('InformationList',{}).get('Information',[]))
  except Exception as error:return dict(status='FAILED',url=url,error=str(error),records=[])
 chunks=[cids[i:i+40] for i in range(0,len(cids),40)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:batches=list(pool.map(fetch,chunks))
 data=dict(retrieved_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),batches=batches)
 (HERE/'PubChem_Synonym_Records.json').write_text(json.dumps(data,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
 print('Synonym batches',len(batches),'successful',sum(r['status']=='SUCCESS' for r in batches))
if __name__=='__main__':run()
