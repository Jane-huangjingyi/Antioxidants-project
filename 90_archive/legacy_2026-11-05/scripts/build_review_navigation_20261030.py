"""Generate bounded topic navigation and current inventory, using unique source locations."""
from pathlib import Path
import json,csv,hashlib,re,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'workspaces/repository_review_20261030';REVIEW=ROOT/'current_review'
base=json.loads((OUT/'Baseline.json').read_text(encoding='utf8'));actions=json.loads((OUT/'File_Actions.json').read_text(encoding='utf8'))
move={r['old_path']:r['new_path'] for r in actions if r['action']!='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY'}
date={move.get(r['path'],r['path']):r['last_git_date'] or r['filesystem_date'] for r in base['files']}
def link(p,fromdir=REVIEW):return '<'+os.path.relpath(ROOT/p,fromdir).replace('\\','/')+'>'
def cat(p):
 if p.startswith('archive/') or '/checkpoints/' in p:return '07_历史版本'
 if p.startswith('R/') or p.startswith('figures/'):return '06_图片与R复现'
 if 'phase1c_' in p:return '04_机制证据与治理'
 if 'track_b_' in p:return '05_机器人实验准备'
 if 'current_deliverables_' in p or 'phase1b_' in p:return '03_交付草稿与字段核查'
 if 'framework' in p or 'dual_track' in p or 'candidate_universe' in p:return '01_候选物与五维框架'
 if p.startswith(('data/','docs/','methods_qc/')):return '02_活性证据与排名审核'
 return '00_项目管理与工具'
def role(p):
 if p.startswith('archive/') or '/checkpoints/' in p:return '历史过程；不作最新结论'
 if '/frozen/' in p:return '冻结正式资产；保持原名原字节'
 if any(k in p.lower() for k in ['dryrun','rebuild_check','gate2_review']):return '过程/演练；保留追溯'
 if '/editable/' in p:return '本轮可编辑重绘；非科学数据修订'
 if any(k in p for k in ['DRAFT','draft','Proposal','proposal','Preparation','preparation']):return '草稿/建议；待批准'
 if '/local_sources/' in p or '/raw/' in p:return '本地来源缓存；不保证Git分发'
 return '按文件内审核状态解释；更新时间不代表批准'
def walk(folder):
 for p in folder.iterdir():
  if p.name in {'.git','node_modules','library','phase2_r_partial_library','__pycache__','.venv','venv'} or p.is_symlink() or p.is_junction():continue
  if p.is_dir():yield from walk(p)
  elif p.is_file():yield p
files=[]
for p in walk(ROOT):
 rel=p.relative_to(ROOT).as_posix()
 if rel.startswith('current_review/navigation/') or rel.endswith('.log') or '/previews/' in rel or rel.endswith('Catalog_Input.json'):continue
 files.append({'path':rel,'category':cat(rel),'role':role(rel),'last_update_date':date.get(rel,'2026-10-30'),'date_basis':'Git内容记录或原文件系统日期（未跟踪）' if rel in date else '本轮新建/更新','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
nav=REVIEW/'navigation';nav.mkdir(exist_ok=True)
groups={}
for r in files:
 if r['path'].startswith('current_review/'):continue
 groups.setdefault(r['category'],[]).append(r)
index=['# 全部现有文件分类导航','', '更新时间2026-10-30。每个链接指向唯一原始位置；日期是查找线索，批准状态仍以文件内记录为准。每页最多40项，包含源数据、工作稿、过程记录及本地缓存；R依赖、版本库内部文件与临时预览不作为科研文件列入。','']
pages=[]
for group,items in sorted(groups.items()):
 items.sort(key=lambda r:(r['path'].startswith('archive/'),r['path']))
 index.append('## '+group.replace('_',' ',1));index.append('')
 for start in range(0,len(items),40):
  chunk=items[start:start+40];name=group+'_'+str(start//40+1).zfill(2)+'.md';dest=nav/name
  lines=['# '+group.replace('_',' ',1)+' · '+str(start//40+1),'','[返回总导航](../PROJECT_NAVIGATION.md)','','|最后更新日期|文件（唯一位置）|角色|','|---|---|---|']
  for r in chunk:lines.append('|'+r['last_update_date']+'|['+Path(r['path']).name+']('+link(r['path'],nav)+')|'+r['role']+'|')
  dest.write_text('\n'.join(lines)+'\n',encoding='utf8');pages.append(dest)
  index.append('- ['+str(start+1)+'–'+str(start+len(chunk))+'项：'+Path(chunk[0]['path']).parent.as_posix()+'](navigation/'+name+')')
 index.append('')
(REVIEW/'PROJECT_NAVIGATION.md').write_text('\n'.join(index),encoding='utf8')
# History is searchable by date even for immutable snapshots with stable filenames.
history=[r for r in files if r['path'].startswith('archive/') or '/checkpoints/' in r['path']]
for name,items in [('Repository_File_Inventory_Current.csv',files),('CURRENT_DELIVERABLES_INDEX.csv',[r for r in files if not r['path'].startswith('archive/')]),('HISTORICAL_VERSION_INDEX.csv',history)]:
 with (REVIEW/name).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
(OUT/'Navigation_Stats.json').write_text(json.dumps({'indexed_files':len(files),'pages':len(pages),'history_files':len(history)},indent=2),encoding='utf8')
print(json.dumps({'indexed_files':len(files),'pages':len(pages),'history_files':len(history)}))
