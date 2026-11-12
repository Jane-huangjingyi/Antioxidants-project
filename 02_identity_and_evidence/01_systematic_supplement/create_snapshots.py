from pathlib import Path
import json,gzip,hashlib
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'Snapshot_Manifest.json').read_text(encoding='utf8'))
for record in manifest:
 data=(HERE/record['path']).read_bytes()
 (HERE/record['snapshot']).write_bytes(gzip.compress(data,mtime=0))
 record['sha256']=hashlib.sha256(data).hexdigest();record['bytes']=len(data)
(HERE/'Snapshot_Manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
print('Bibliographic snapshots refreshed.')
