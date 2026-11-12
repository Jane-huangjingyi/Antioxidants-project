from pathlib import Path
import gzip,json,hashlib
HERE=Path(__file__).resolve().parent
for record in json.loads((HERE/'Snapshot_Manifest.json').read_text(encoding='utf8')):
 data=gzip.decompress((HERE/record['snapshot']).read_bytes())
 assert hashlib.sha256(data).hexdigest()==record['sha256'],record['path']
 (HERE/record['path']).write_bytes(data)
print('Bibliographic snapshots restored and SHA256 verified.')
