"""Retrieve PubMed method and class routes via official E-utilities."""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
CACHE = ROOT / '02_identity_and_evidence/01_systematic_supplement/inputs/stage2_v1_1/pubmed_v1'
ENDPOINT = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
CUTOFF = dt.date(2026, 11, 17)

def terms(values):
    return '(' + ' OR '.join(f'"{value}"[Title/Abstract]' for value in values) + ')'

METHOD = terms(['ORAC', 'oxygen radical absorbance capacity', 'pyrogallol red',
                'crocin bleaching', 'ABTS', 'DPPH', 'FRAP', 'CUPRAC',
                'ferric reducing antioxidant', 'cupric reducing antioxidant'])
CLASS = terms(['phenolic', 'phenolics', 'flavonoid', 'flavonoids', 'carotenoid',
               'carotenoids', 'lignan', 'vitamin', 'thiol', 'alkaloid']) + ' AND ' + terms(['antioxidant', 'antioxidants', 'radical scavenging'])

def cached_request(filename, service, **parameters):
    path = CACHE / filename
    if path.exists():
        return path.read_bytes()
    query = urllib.parse.urlencode(dict(db='pubmed', tool='antioxidant_stage2', **parameters))
    for attempt in range(4):
        try:
            time.sleep(0.4 + attempt)
            request = urllib.request.Request(ENDPOINT + service + '.fcgi', data=query.encode())
            with urllib.request.urlopen(request, timeout=55) as response:
                result = response.read()
            temporary = path.with_suffix('.tmp')
            temporary.write_bytes(result)
            temporary.replace(path)
            return result
        except (OSError, TimeoutError):
            if attempt == 3:
                raise

def publication_query(query, start, end):
    return f'{query} AND ("{start:%Y/%m/%d}"[dp] : "{end:%Y/%m/%d}"[dp])'

def search(label, query, start, end, audit):
    identifier = f'{label}_{start}_{end}'
    dated_query = publication_query(query, start, end)
    raw = cached_request(identifier+'.json', 'esearch', term=dated_query, retmode='json', retmax=9999)
    result = json.loads(raw)['esearchresult']
    count = int(result['count'])
    if count >= 10000:
        if start == end:
            raise RuntimeError(f'PubMed partition exceeds limit: {identifier}')
        midpoint = start + (end-start)//2
        return search(label, query, start, midpoint, audit) | search(label, query, midpoint+dt.timedelta(days=1), end, audit)
    ids = set(result['idlist'])
    if len(ids) != count:
        raise RuntimeError(f'PubMed identifier count mismatch: {identifier}')
    audit.append(dict(route=label, search_start=start, publication_cutoff=end, query=dated_query,
                      retrieved_utc=dt.datetime.fromtimestamp((CACHE/(identifier+'.json')).stat().st_mtime,dt.timezone.utc).isoformat(),
                      query_translation=result.get('querytranslation',''), hit_count=count,
                      unique_pmids=len(ids), raw_file=identifier+'.json', sha256=hashlib.sha256(raw).hexdigest()))
    print(identifier, count, flush=True)
    return ids

def write(filename, rows):
    with (HERE/filename).open('w',encoding='utf8',newline='') as handle:
        writer = csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    audit = []
    routes = {}
    for label, query in [('METHOD_ONLY', METHOD), ('COMPOUND_CLASS', CLASS)]:
        window = publication_query(query, dt.date(2020, 1, 1), CUTOFF)
        cached_request(label+'_whole_window_count.json', 'esearch', term=window, retmode='json', retmax=0)
        routes[label] = set()
        for year in range(2020, 2027):
            routes[label].update(search(label, query, dt.date(year,1,1), min(dt.date(year,12,31), CUTOFF), audit))
    write('PubMed_Search_Partitions.csv',audit)
    ids = sorted(set.union(*routes.values()), key=int)
    write('PubMed_Route_PMIDs.csv',[dict(PMID=pmid, routes=';'.join(k for k,v in routes.items() if pmid in v)) for pmid in ids])
    export_records(ids, 'efetch', 'PubMed_Export_Manifest.csv')

def export_records(ids, prefix, manifest):
    batches = []
    for offset in range(0,len(ids),400):
        expected = set(ids[offset:offset+400])
        name = f'{prefix}_{offset//400+1:04d}.xml'
        raw = cached_request(name,'efetch',id=','.join(sorted(expected,key=int)),retmode='xml')
        root = ET.fromstring(raw)
        observed = {node.findtext('MedlineCitation/PMID') or node.findtext('BookDocument/PMID') for node in root}
        if expected != observed:
            raise RuntimeError(f'EFetch mismatch: {name}; missing {len(expected-observed)}, unexpected {len(observed-expected)}')
        batches.append(dict(raw_file=name,PMIDs=len(observed),sha256=hashlib.sha256(raw).hexdigest()))
        write(manifest, batches)
        print(name,offset+len(observed),len(ids),flush=True)
    print('Export verified',len(ids),flush=True)

if __name__ == '__main__':
    main()
