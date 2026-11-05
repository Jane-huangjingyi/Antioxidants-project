"""Bounded source/metadata retrieval only: no raw sequence or analysis execution."""
import concurrent.futures,hashlib,json,pathlib,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'local_sources';OUT.mkdir(exist_ok=True)
TARGETS={
'HDAC1_publisher.html':'https://www.mdpi.com/2079-7737/15/2/206',
'HDAC1_supplement.zip':'https://mdpi-res.com/d_attachment/biology/biology-15-00206/article_deploy/biology-15-00206-s001.zip',
'eNOS_publisher.html':'https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2023.1060226/full',
'Kmo_publisher.html':'https://onlinelibrary.wiley.com/doi/10.1111/jcmm.17869',
'Kmo_DataS1.doc':'https://onlinelibrary.wiley.com/doi/suppl/10.1111/jcmm.17869/supinfo/jcmm17869-sup-0006-supinfo.doc',
'DRA014580_DDBJ.html':'https://ddbj.nig.ac.jp/resource/sra-submission/DRA014580',
'DRA014580_ENA.xml':'https://www.ebi.ac.uk/ena/browser/api/xml/DRA014580',
'DRA014580_runs.tsv':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=DRA014580&result=read_run&fields=run_accession,study_accession,sample_accession,experiment_accession,scientific_name,sample_title,experiment_title,library_strategy&format=tsv',
}
def get(item):
 name,url=item
 try:
  try:
   with urllib.request.urlopen(url,timeout=30) as r: status,ctype,data=r.status,r.headers.get('Content-Type',''),r.read(15_000_001)
  except urllib.error.HTTPError as e:status,ctype,data=e.code,e.headers.get('Content-Type',''),e.read(100000)
  if len(data)>15_000_000:return {'name':name,'url':url,'status':status,'result':'SIZE_LIMIT_NOT_SAVED'}
  binary_ok=(name.endswith('.zip') and data[:2]==b'PK') or (name.endswith('.doc') and data[:8]==bytes.fromhex('d0cf11e0a1b11ae1'))
  usable=status==200 and (binary_ok if name.endswith(('.zip','.doc')) else True)
  # Keep failed HTML responses local too, never call them valid supplement contents.
  (OUT/name).write_bytes(data)
  return {'name':name,'url':url,'status':status,'content_type':ctype,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'usable_response':usable,'binary_signature_valid':binary_ok if name.endswith(('.zip','.doc')) else None,'local_path':'local_sources/'+name}
 except Exception as e:return {'name':name,'url':url,'result':'ACCESS_FAILED','error':str(e)}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:entries=list(pool.map(get,TARGETS.items()))
 (ROOT/'qc/Targeted_Access_Log.json').write_text(json.dumps({'date':'2026-10-26','scope':'THREE_TARGETED_QUESTIONS_ONLY','entries':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(entries,ensure_ascii=False))
