"""Shared I/O and paths. Scientific decisions belong to individual numbered steps."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SOURCE_ROOT=ROOT/'02_identity_and_evidence/inputs/reference_collection'
FROZEN_ROOT=ROOT/'03_candidate_selection/inputs/frozen_reference'
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
def source(rel):
 rel=str(rel).replace('\\','/');name=Path(rel).name
 if rel.startswith('data/h_orac_stage25b/frozen/'):return FROZEN_ROOT/'tables'/name
 if rel=='docs/methods/h_orac_framework/H_ORAC_Evidence_Rubric_v2.0_CN.md':return FROZEN_ROOT/'rubric'/name
 if rel.startswith('figures/aqueous_antioxidant_atlas/') and name in {'HORAC_Primary_Top20_Frozen.png','HORAC_Primary_Top20_Frozen.svg','HORAC_Top20_B2_Sensitivity.png','HORAC_Top20_B2_Sensitivity.svg'}:return FROZEN_ROOT/'figures'/name
 if rel.startswith('identity/'):return ROOT/'02_identity_and_evidence/inputs/identity_reference'/name
 if rel.startswith('discovery/'):return ROOT/'01_candidate_discovery/inputs/curation_baseline'/name
 return SOURCE_ROOT/rel
def locator(rel):return source(rel).relative_to(ROOT).as_posix()
def number(value):
 try:return float(value) if str(value).strip() not in ('','NA','NOT_ESTIMABLE') else None
 except (ValueError,TypeError):return None
