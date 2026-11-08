"""Explicit PubChem graph recovery; name hits are candidates, not identity approvals."""
import csv,json,urllib.request,urllib.parse,hashlib,time,concurrent.futures,sys
from pathlib import Path
P=Path(__file__).resolve().parent
with (P/'results/Flavonoid_Candidate_Crosswalk.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
raw=P/'inputs/source_recovery/raw';raw.mkdir(exist_ok=True,parents=True)
previous=json.loads((P/'inputs/flavonoid_structure_candidates.json').read_text(encoding='utf-8')) if (P/'inputs/flavonoid_structure_candidates.json').exists() else []
prior={r['source_row']:r for r in previous}
def recover(r):
    old=prior.get(r['source_row'])
    if '--retry-failed' in sys.argv and old and old['status']=='RECOVERED':return old
    name=r['source_compound'].replace('′',"'")
    override='145826' if r['source_row']=='14' else ''  # PubChem official synonym record, still candidate mapping
    query='cid/'+(r['CID'] or override) if (r['CID'] or override) else 'name/'+urllib.parse.quote(name,safe='')
    url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'+query+'/property/Title,MolecularFormula,MolecularWeight,InChIKey,InChI,IsomericSMILES,CanonicalSMILES,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount/JSON'
    if override:url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/'+override+'/property/IsomericSMILES,InChIKey/JSON'
    entry=dict(source_row=r['source_row'],compound=r['source_compound'],query_url=url,access_date='2026-11-08',identity_review='NOT_REVIEWED')
    try:
        time.sleep(.4)
        for attempt in range(3):
            try:
                b=urllib.request.urlopen(url,timeout=12).read();break
            except Exception:
                if attempt==2:raise
                time.sleep(1)
        d=json.loads(b);props=d['PropertyTable']['Properties']
        (raw/('flavonoid_structure_'+r['source_row']+'.json')).write_bytes(b)
        entry.update(status='RECOVERED',sha256=hashlib.sha256(b).hexdigest(),property_candidates=props,query_basis='REFERENCE_CID' if r['CID'] else 'SOURCE_NAME_ONLY_PENDING_MANUAL_MAPPING')
        if r['InChIKey']:entry['reference_key_agreement']=all(p['InChIKey']==r['InChIKey'] for p in props)
    except Exception as e:entry.update(status='NOT_RECOVERED',error=str(e))
    if old:entry['prior_attempts']=old.get('prior_attempts',[])+[{k:v for k,v in old.items() if k not in ['prior_attempts','property_candidates']}]
    return entry
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    result=list(ex.map(recover,rows))
(P/'inputs/flavonoid_structure_candidates.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(total=len(result),recovered=sum(x['status']=='RECOVERED' for x in result))))
