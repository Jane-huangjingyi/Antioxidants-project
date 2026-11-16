"""Retry failed Europe PMC XML recovery through public NCBI BioC text."""
from pathlib import Path
import concurrent.futures
import csv
import hashlib
import json
import urllib.request

HERE = Path(__file__).resolve().parent


def recover(row):
    pmcid = row['PMCID']
    url = f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmcid}/unicode'
    path = HERE / 'inputs' / (pmcid + '_BioC.json')
    record = dict(doi=row['doi'], PMCID=pmcid, url=url, retrieval_date='2026-11-12')
    try:
        data = path.read_bytes() if path.exists() else urllib.request.urlopen(url, timeout=35).read()
        document = json.loads(data)[0]['documents'][0]
        assert str(document['id']).replace('PMC', '') == pmcid.replace('PMC', '')
        assert len(document['passages']) > 10
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(data)
        record.update(status='PUBLIC_BIOC_RECOVERED_PENDING_READING', source_file=path.relative_to(HERE).as_posix(),
                      sha256=hashlib.sha256(data).hexdigest(), passages=len(document['passages']),
                      scope='Text and text-encoded tables; figures and supplements require separate inspection')
    except Exception as exc:
        record.update(status='FETCH_FAILED', error=str(exc))
    return record


def run():
    rows = []
    for filename in ['Method_Fulltext_Queue.csv', 'Compound_Comparison_Fulltext_Queue.csv']:
        with (HERE / filename).open(encoding='utf8') as file:
            rows.extend(row for row in csv.DictReader(file) if row['fulltext_recovery'] == 'PUBLIC_XML_FETCH_FAILED')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(recover, rows))
    (HERE / 'Alternative_Fulltext_Access.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf8')
    print(json.dumps(results))


if __name__ == '__main__':
    run()
