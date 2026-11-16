"""Recover publicly hosted supplements and retain access attempts and hashes."""
from pathlib import Path
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import io
import json
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
SOURCES = [
    ('BJOC_11_151_S1.pdf', 'https://www.beilstein-journals.org/bjoc/content/supplementary/1860-5397-11-151-S1.pdf'),
    ('PMC7525318_supplementary.zip', 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7525318/supplementaryFiles'),
    ('PMC7525318_TableS1.docx', 'https://onlinelibrary.wiley.com/doi/suppl/10.1155/2020/4150897/supinfo/4150897.f1.docx'),
]


def recover(item):
    filename, url = item
    path = HERE / 'inputs' / filename
    record = dict(url=url, attempted_utc=datetime.now(timezone.utc).isoformat())
    try:
        if path.exists():
            data = path.read_bytes()
        else:
            with urllib.request.urlopen(url, timeout=40) as response:
                data = response.read()
        if filename.endswith('.pdf'):
            assert data.startswith(b'%PDF'), 'Response is not PDF'
        else:
            assert zipfile.is_zipfile(io.BytesIO(data)), 'Response is not a complete ZIP/DOCX'
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                assert archive.testzip() is None, 'Archive checksum failure'
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(data)
        record.update(file=path.relative_to(HERE).as_posix(), status='RECOVERED',
                      bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        record.update(file='', status='FETCH_FAILED', error=str(exc))
    return record


def run():
    manifest = HERE / 'Supplement_Access.json'
    records = json.loads(manifest.read_text(encoding='utf8')) if manifest.exists() else []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(recover, SOURCES))
    records.extend(results)
    manifest.write_text(json.dumps(records, indent=2) + '\n', encoding='utf8')
    print(json.dumps(results))


if __name__ == '__main__':
    run()
