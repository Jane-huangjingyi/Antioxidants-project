"""One-time, reversible layout migration; run only before the numbered workflow exists."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'90_archive/legacy_2026-11-05'
MAN=ROOT/'07_quality_control/migration_manifest.json'
if MAN.exists() or DEST.exists():raise SystemExit('Migration already started/completed. Inspect the manifest; do not replay.')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8-sig').strip()
old_names=['archive','current_review','data','docs','figures','methods_qc','outputs','R','references','scripts','workspaces']
old_names += [p.name for p in ROOT.iterdir() if p.is_file() and p.name not in {'.gitignore','AGENTS.md','.gitattributes'}]
tracked=git('ls-files','-z').split('\0');entries=[]
def walk(p):
 if p.is_junction() or p.is_symlink() or p.name in {'node_modules','library','.git','phase2_r_partial_library','__pycache__'}:return
 if p.is_dir():
  for q in p.iterdir():yield from walk(q)
 elif p.is_file():yield p
for name in old_names:
 p=ROOT/name
 if not p.exists():continue
 for q in walk(p):
  rel=q.relative_to(ROOT).as_posix();entries.append({'old_path':rel,'new_path':(Path('90_archive/legacy_2026-11-05')/rel).as_posix(),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'tracked_before':rel in tracked})
MAN.parent.mkdir(exist_ok=True);DEST.mkdir(parents=True)
plan={'date':'2026-11-05','base_commit':git('rev-parse','HEAD'),'initial_status':git('status','--porcelain'),'entries':entries,'directory_moves':old_names,'policy':'All original scientific and process bytes preserved. Package/VCS internals excluded from file hashes.'}
MAN.write_text(json.dumps(plan,indent=2),encoding='utf8')
for name in old_names:
 p=ROOT/name;q=DEST/name
 if not p.exists():continue
 assert p.resolve().parent==ROOT.resolve() and q.resolve().is_relative_to(DEST.resolve())
 assert not q.exists();p.rename(q)
for r in entries:assert hashlib.sha256((ROOT/r['new_path']).read_bytes()).hexdigest()==r['sha256'],r['old_path']
print(json.dumps({'preserved_files':len(entries),'moved_roots':len(old_names),'base_commit':plan['base_commit']}))
