"""Shared I/O and paths. Scientific decisions belong to individual numbered steps."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
LEGACY=ROOT/'90_archive/legacy_2026-11-05'
AS_OF='2026-11-05'
def read_csv(path):
 with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(path,rows,fields=None):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 fields=fields or list(rows[0])
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='raise',lineterminator='\n');w.writeheader();w.writerows(rows)
def write_json(path,obj):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def read_json(path):return json.loads(Path(path).read_text(encoding='utf8'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def source(rel):return LEGACY/rel
def locator(rel):return (Path('90_archive/legacy_2026-11-05')/rel).as_posix()
def number(value):
 try:return float(value) if str(value).strip() not in ('','NA','NOT_ESTIMABLE') else None
 except (ValueError,TypeError):return None
