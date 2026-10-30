"""Read-only baseline inventory; excludes dependency/VCS internals, not research caches."""
from pathlib import Path
import csv, hashlib, json, subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'workspaces/repository_review_20261030'
OUT.mkdir(parents=True,exist_ok=True)
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8-sig').strip()
if (OUT/'Baseline.json').exists(): raise SystemExit('Baseline already exists; do not overwrite')
tracked=git('ls-files','-z').split('\0')
dates={}; date=''
for line in git('log','--format=DATE:%as','--name-only').splitlines():
 if line.startswith('DATE:'): date=line[5:]
 elif line.strip(): dates.setdefault(line.strip(),date)
skip={'.git','node_modules','library','.venv','venv','__pycache__','.Rproj.user'}
files=[]; sources=[]
def walk(folder):
 for p in folder.iterdir():
  if p.name in skip or p.is_symlink() or p.is_junction(): continue
  if p.is_dir(): yield from walk(p)
  elif p.is_file(): yield p
for p in walk(ROOT):
 rel=p.relative_to(ROOT).as_posix()
 if rel.startswith('workspaces/repository_review_20261030/'): continue
 b=p.read_bytes(); row={'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'tracked':rel in tracked,'last_git_date':dates.get(rel,''),'filesystem_date':__import__('datetime').datetime.fromtimestamp(p.stat().st_mtime).date().isoformat()}
 files.append(row)
 if p.suffix.lower()=='.csv':
  try:
   with p.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f); h=reader.fieldnames or []; n=sum(1 for _ in reader)
   sources.append({'path':rel,'rows':n,'headers':h})
  except Exception as e:sources.append({'path':rel,'error':str(e)})
groups={}
for r in files:groups.setdefault(r['sha256'],[]).append(r['path'])
result={'base_commit':git('rev-parse','HEAD'),'date':'2026-10-30','files':files,'csv_tables':sources,'duplicate_groups':[v for v in groups.values() if len(v)>1]}
(OUT/'Baseline.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files':len(files),'tracked':sum(r['tracked'] for r in files),'csv_tables':len(sources),'duplicates':result['duplicate_groups']},ensure_ascii=False,indent=2))
print('TABLE CANDIDATES:')
for r in sources:
 if any(k.lower() in ['doi','pmid','evidence_id','paper_title','reference'] for k in r.get('headers',[])):print(r['path'],r.get('rows'),','.join(r.get('headers',[])[:12]))
