"""Recover additional compound-comparison articles through the existing XML fetcher."""
from pathlib import Path
import csv
import re
import json
import concurrent.futures
import hashlib
import urllib.request
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
TITLE_PATTERN = (
    r'pure (?:chemical )?compounds|structure.{0,2}activity|'
    r'individual (?:phenolic|antioxidant)|selected flavonoids|'
    r'comparative evaluation.{0,45}polyphenols|antioxidant interactions|'
    r'glutathione.{0,55}binary|high.throughput screening|'
    r'comparison of antioxidant properties'
)


def recover(row):
    pmcid = row['PMCID']
    path = HERE / 'fulltext_xml' / (pmcid + '.xml')
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/' + pmcid + '/fullTextXML'
    status = 'PUBLIC_XML_RECOVERED_PENDING_READING'
    error = ''
    try:
        if not path.exists():
            with urllib.request.urlopen(url, timeout=35) as response:
                data = response.read()
            ET.fromstring(data)
            temporary = path.with_suffix('.tmp')
            temporary.write_bytes(data)
            temporary.replace(path)
        ET.fromstring(path.read_bytes())
    except Exception as exc:
        status = 'PUBLIC_XML_FETCH_FAILED'
        error = str(exc)
    return dict(article_key=row['article_key'], doi=row['doi'], PMID=row['PMID'],
                PMCID=pmcid, title=row['title'], journal=row['journal'],
                title_priority='COMPOUND_COMPARISON_TITLE_PENDING_ASSAY_SCREEN',
                fulltext_recovery=status, source_url=url,
                source_file=path.relative_to(HERE).as_posix() if path.exists() else '',
                sha256=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else '',
                error=error, scientific_screening='PENDING',
                human_review_status='NOT_REVIEWED', change_applied='NO')


def run():
    with (HERE / 'Master_Article_Register.csv').open(encoding='utf8') as file:
        articles = list(csv.DictReader(file))
    selected = [row for row in articles if row['PMCID']
                and re.search(r'antiox|radical scaveng', row['title'], re.I)
                and re.search(TITLE_PATTERN, row['title'], re.I)
                and not re.search(r'\bORAC\b|oxygen radical absorbance|crocin bleaching|pyrogallol red', row['title'], re.I)]
    selected.sort(key=lambda row: (row['doi'], row['PMCID']))
    (HERE / 'fulltext_xml').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(recover, selected))
    with (HERE / 'Compound_Comparison_Fulltext_Queue.csv').open('w', encoding='utf8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(dict(selected=len(rows), recovered=sum(row['fulltext_recovery'] == 'PUBLIC_XML_RECOVERED_PENDING_READING' for row in rows))))


if __name__ == '__main__':
    run()
