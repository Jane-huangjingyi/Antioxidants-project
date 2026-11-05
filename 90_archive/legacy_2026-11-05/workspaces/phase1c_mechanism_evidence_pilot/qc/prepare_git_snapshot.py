"""Prepare a source-cache manifest without publishing source texts or changing evidence."""
from pathlib import Path
import csv,json,hashlib,datetime,xml.etree.ElementTree as ET
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'workspaces/phase1c_mechanism_evidence_pilot';RAW=OUT/'search_logs/raw'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def writecsv(name,rows):
 with (OUT/name).open('x',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
manifest=[]
for p in sorted(RAW.iterdir()):
 if not p.is_file():continue
 url='';kind='RECONSTRUCTED_RETRIEVAL_URL';name=p.name
 if name.startswith('PMC'):
  pmc=name.split('_')[0].split('.')[0]
  url='https://pmc.ncbi.nlm.nih.gov/articles/'+pmc+'/' if 'browser' in name else 'https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML'
 if name.endswith('.json'):
  obj=json.loads(p.read_text(encoding='utf-8'))
  if isinstance(obj,dict):
   if obj.get('url'):url=obj['url'];kind='EXACT_RETAINED_URL'
   elif obj.get('log',{}).get('api_urls'):url=json.dumps(obj['log']['api_urls']);kind='EXACT_RETAINED_URL_LIST'
   elif obj.get('esearchresult',{}).get('querytranslation'):
    url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'+urlencode({'db':'pubmed','term':obj['esearchresult']['querytranslation'],'retmode':'json','retmax':10000})
 if name in ['Selected_PubMed_Metadata.xml','Additional_PubMed_Metadata.xml']:
  ids=[a.findtext('./MedlineCitation/PMID') for a in ET.parse(p).findall('./PubmedArticle')]
  url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'+urlencode({'db':'pubmed','id':','.join(ids),'retmode':'xml'})
 manifest.append(dict(local_cache_relative_path='search_logs/raw/'+name,bytes=p.stat().st_size,sha256=sha(p),git_distribution_status='LOCAL_ONLY_EXCLUDED',source_url=url or 'SEE_SEARCH_LOG_AND_RETRIEVAL_SCRIPTS',url_provenance=kind if url else 'NOT_INDIVIDUALLY_RECORDED',redistribution_license_status='NOT_CLEARED_FOR_THIS_GIT_SNAPSHOT',fresh_clone_status='NOT_BUNDLED_RETRIEVAL_REQUIRED',notes_CN='哈希标识本轮实际下载版本；重新检索响应可能改变，须记录新版本，不能默认为哈希一致。'))
writecsv('search_logs/Local_Source_Cache_Manifest.csv',manifest)
lookup={r['local_cache_relative_path']:r for r in manifest}
with (OUT/'master/Compound_Mechanism_Evidence_Master.csv').open(encoding='utf-8-sig',newline='') as f:evidence=list(csv.DictReader(f))
index=[]
for r in evidence:
 m=lookup[r['source_local_path']]
 index.append(dict(evidence_id=r['evidence_id'],study_id=r['study_id'],DOI=r['DOI'],PMID=r['PMID'],article_url=r['article_url'],source_local_path=r['source_local_path'],source_sha256=m['sha256'],source_locator=r['source_locator'],source_verification_status_at_extraction=r['source_verification_status'],cache_availability_in_git='NOT_BUNDLED',fresh_clone_verification_status='SOURCE_RETRIEVAL_REQUIRED',retrieval_url=m['source_url'],retrieval_url_provenance=m['url_provenance']))
writecsv('indexes/Evidence_Source_Provenance_Index.csv',index)
baseline=json.loads((OUT/'qc/Start_Baseline.json').read_text(encoding='utf-8'))
changed=[p for p,h in baseline['tracked_file_sha256'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
assert not changed,changed
assert (OUT/'master/Compound_Mechanism_Evidence_Master.csv').read_bytes()==(OUT/'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv').read_bytes()
v=json.loads((OUT/'qc/Final_Validation.json').read_text(encoding='utf-8'))
for rel,info in v['csv_counts'].items():assert sha(OUT/rel)==info['sha256'],rel
assert len(index)==21 and len({x['evidence_id'] for x in index})==21
with (OUT/'qc/Git_Snapshot_Preparation_Check.json').open('x',encoding='utf-8') as f:
 json.dump({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_tracked_files_checked':len(baseline['tracked_file_sha256']),'original_changed_paths':changed,'all_previously_validated_csv_sha256_unchanged':True,'source_cache_files_retained_locally':len(manifest),'source_cache_bytes_excluded':sum(r['bytes'] for r in manifest),'evidence_source_index_rows':len(index),'evidence_data_changed':False,'human_scientific_review':'NOT_REVIEWED','Gate1':'HOLD','Gate2':'HUMAN_SCIENTIFIC_REVIEW_REQUIRED','Release':'HOLD','authorization':'User authorized precommit organization and selective commit/push after initial extraction; earlier NOT_EXECUTED logs are historical snapshots.'},f,ensure_ascii=False,indent=2)
print('SOURCE_FILES',len(manifest),'EXCLUDED_BYTES',sum(r['bytes'] for r in manifest),'PROVENANCE_ROWS',len(index),'ORIGINAL_CHANGES',changed)
