"""Approved archive organization: preserve bytes and map every rename/deletion."""
from pathlib import Path
import json,subprocess,hashlib,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'workspaces/repository_review_20261030'
base=json.loads((OUT/'Baseline.json').read_text(encoding='utf8'))
ledger=OUT/'File_Actions.json'
if ledger.exists():raise SystemExit('Already organized; use saved map, never replay blindly')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
actions=[]; deleted={
 'archive/superseded_outputs/figures/Flavonoid_Top20_Evidence_Confidence.png':'archive/figure_redundancy_stage24/01_flavonoids/Flavonoids_Evidence_Confidence.png',
 'archive/superseded_outputs/figures/PhenolicAcid_Evidence_Confidence.png':'archive/figure_redundancy_stage24/02_phenolic_acids/PhenolicAcids_Evidence_Confidence.png'}
for old,retained in deleted.items():
 p=ROOT/old;q=ROOT/retained;assert p.resolve().is_relative_to(ROOT.resolve());assert digest(p)==digest(q)
 p.unlink();actions.append({'old_path':old,'new_path':retained,'action':'DELETE_BYTE_IDENTICAL_REDUNDANT_FIGURE_COPY','sha256':digest(q),'reason':'保留同字节历史图；引用仅见旧治理清单，由本映射保留路径解释；无独立实验/审核/过程信息'})
for row in base['files']:
 old=row['path'];p=ROOT/old
 if not row['tracked'] or not old.startswith('archive/') or old in deleted:continue
 if any(x in old for x in ['/stage25a_local_cache/','/phase2_r_partial_library/','/phase2_local_cache/']):continue
 if p.name.startswith('README') or p.name=='HISTORY_NAVIGATION_CN.md':continue
 log=subprocess.check_output(['git','log','--follow','--diff-filter=AM','-1','--format=%as','--',old],cwd=ROOT).decode().strip()
 date=log or row['last_git_date'];assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',date),old
 parent=Path(old).parent.relative_to('archive')
 new=(Path('archive/history')/date/parent/(date+'_'+p.name)).as_posix();q=ROOT/new
 assert q.resolve().is_relative_to((ROOT/'archive').resolve());assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True);p.rename(q)
 actions.append({'old_path':old,'new_path':new,'action':'RENAME_HISTORY_WITH_LAST_CONTENT_GIT_DATE','sha256':row['sha256'],'date':date,'date_basis':'git log --follow --diff-filter=AM; content tracked date, not move date'})
# Previous review governance/status records are a process snapshot, not deleted.
keep={'README_CURRENT_REVIEW.md','LATEST_PROJECT_STATUS_CN.md','CURRENT_DECISIONS_AND_GAPS.md','PROJECT_NAVIGATION.md','CURRENT_DELIVERABLES_INDEX.csv','Repository_File_Inventory_Current.csv','HISTORICAL_VERSION_INDEX.csv'}
for row in base['files']:
 old=row['path'];p=ROOT/old
 if not old.startswith('current_review/') or not row['tracked']:continue
 date=row['last_git_date']
 new=f'archive/history/{date}/review_governance/{date}_{p.name}';q=ROOT/new;q.parent.mkdir(parents=True,exist_ok=True)
 if p.name in keep:
  q.write_bytes(p.read_bytes());action='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY'
 else:p.rename(q);action='ARCHIVE_SUPERSEDED_REVIEW_REPORT'
 actions.append({'old_path':old,'new_path':new,'action':action,'sha256':row['sha256'],'date':date,'date_basis':'last Git update of review entry'})
mapping={r['old_path']:r['new_path'] for r in actions if r['action']!='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY'}
# Resolve deletion destinations through subsequent renames.
for r in actions:
 if r['action'].startswith('DELETE'):r['new_path']=mapping.get(r['new_path'],r['new_path'])
mapping={r['old_path']:r['new_path'] for r in actions if r['action']!='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY'}
# Repair executable current paths and active navigation only; immutable historical text stays byte-identical.
for row in base['files']:
 p=ROOT/row['path'];rel=row['path']
 if not p.exists() or rel.startswith(('archive/','data/','methods_qc/','workspaces/')):continue
 if p.suffix.lower() not in ('.md','.r','.py','.ps1'):continue
 t=p.read_text(encoding='utf-8-sig');out=t
 for old,new in mapping.items():
  out=out.replace(old,new)
  if rel.count('/')==0:out=out.replace(old.replace('archive/','archive\\',1),new)
 if out!=t:p.write_text(out,encoding='utf8')
ledger.write_text(json.dumps(actions,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'actions':len(actions),'deleted':len(deleted),'renamed':sum(r['action'].startswith('RENAME') for r in actions)},ensure_ascii=False))
