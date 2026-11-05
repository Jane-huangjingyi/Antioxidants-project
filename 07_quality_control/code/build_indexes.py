"""English navigation and role indexes, without copying the scientific tables they describe."""
from pathlib import Path
import sys,csv,subprocess,os,json
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
def walk(p):
 for q in p.iterdir():
  if q.name in {'node_modules','library','phase2_r_partial_library','__pycache__','.git','.q','previews','local'} or getattr(q,'is_junction',lambda:False)() or q.is_symlink():continue
  if q.is_dir():yield from walk(q)
  elif q.is_file():yield q
source_rows=[]
for p in walk(LEGACY):
 if p.suffix.lower()!='.csv':continue
 rel=p.relative_to(ROOT).as_posix()
 try:
  with p.open(encoding='utf-8-sig',newline='') as f:r=csv.reader(f);headers=next(r,[]);n=sum(1 for _ in r)
  role='PRESERVED_SCIENTIFIC_OR_PROCESS_TABLE'
  if '/archive/' in rel or '/checkpoints/' in rel:role='HISTORICAL_OR_CHECKPOINT_NOT_NEW_INDEPENDENT_EVIDENCE'
  if '/dryrun/' in rel or '/rebuild_check/' in rel:role='ISOLATED_REHEARSAL_OR_REBUILD_NOT_PRODUCTION'
  if '/provenance/Literature_Screening_Publication_' in rel:role='CANDIDATE_PUBLICATION_METADATA_NOT_FULLTEXT_EVIDENCE'
  source_rows.append({'source_file':rel,'record_count':n,'role':role,'sha256':sha(p),'field_names':'; '.join(headers)})
 except (UnicodeError,csv.Error) as e:source_rows.append({'source_file':rel,'record_count':'','role':'READ_ERROR_REQUIRES_REVIEW','sha256':sha(p),'field_names':type(e).__name__})
write_csv(ROOT/'02_identity_and_evidence/results/source_file_index.csv',source_rows)
files=[]
for p in walk(ROOT):
 rel=p.relative_to(ROOT).as_posix()
 if rel.startswith('90_archive/') or p.name.endswith('.log'):continue
 files.append({'path':rel,'role':'CODE' if p.suffix in {'.py','.R','.mjs'} else 'DOCUMENTATION' if p.suffix=='.md' else 'GENERATED_FIGURE' if p.suffix in {'.svg','.png'} else 'CONFIG_OR_SCIENTIFIC_TABLE','sha256':sha(p),'step':rel.split('/')[0]})
files=[r for r in files if r['path'] not in {'07_quality_control/file_role_inventory.csv','07_quality_control/workflow_qc.json','07_quality_control/Workflow_QC.md'}]
write_csv(ROOT/'07_quality_control/file_role_inventory.csv',files)
fig=[]
for p in sorted((ROOT/'06_manuscript/figures').rglob('*.png')):
 svg=Path(str(p).replace('/png/','/svg/').replace('\\png\\','\\svg\\')).with_suffix('.svg')
 assert svg.exists(),p
 role='MAIN_CURRENT_WORKFLOW' if 'supplementary' not in p.parts else 'SUPPLEMENTARY_PRESERVED_CONSTRUCT'
 fig.append({'figure_name':p.stem,'role':role,'png_path':p.relative_to(ROOT).as_posix(),'svg_path':svg.relative_to(ROOT).as_posix(),'generator':'05_analysis/R/render_manuscript_figures.R' if role.startswith('MAIN') else '05_analysis/render_historical_figures.R','png_sha256':sha(p),'svg_sha256':sha(svg)})
write_csv(ROOT/'07_quality_control/figure_export_registry.csv',fig)
def git(*args):
 try:return subprocess.check_output(['git',*args],cwd=ROOT,encoding='utf8',stderr=subprocess.DEVNULL).strip()
 except (OSError,subprocess.CalledProcessError):return ''
branches=[];base=read_json(ROOT/'07_quality_control/migration_manifest.json')['base_commit']
for line in git('for-each-ref','--format=%(refname:short)|%(objectname)|%(upstream:short)','refs/heads').splitlines():
 name,tip,upstream=line.split('|');contained=subprocess.run(['git','merge-base','--is-ancestor',tip,base],cwd=ROOT,stderr=subprocess.DEVNULL).returncode==0
 count=git('rev-list','--count',base+'..'+tip)
 branches.append({'branch':name,'tip_at_audit':tip,'upstream':upstream,'contained_in_layout_baseline':contained,'unique_commits_vs_layout_baseline':int(count) if count else None,'action':'KEEP_AS_TRACEABLE_ANCESTOR_NO_REPEAT_MERGE' if contained else 'ACTIVE_WORKFLOW_BRANCH_OR_NEW_WORK_REVIEW_REQUIRED'})
write_json(ROOT/'07_quality_control/branch_inventory.json',{'audit_date':AS_OF,'baseline_commit':base,'current_branch':git('branch','--show-current'),'main_tip_at_audit':git('rev-parse','main'),'branches':branches})
lines=['# Git workflow and branch interpretation','',f'The current working branch is `{git("branch","--show-current")}`. The reorganization starts from `{base}`; the earlier review, governance and Track B branches are contained in that baseline. Their approvals and HOLD states remain as recorded. A branch name is not a scientific approval.','', '## Current handling','', 'Use the current workflow branch as the single active checkout for this task. Do not merge each old branch again: the branch inventory reports whether its tip is already an ancestor. Preserve old branch names as traceable milestones; none is deleted automatically. The new organization is committed once after QC.','', f'At audit, local main pointed to `{git("rev-parse","main")}`. Main was older than the reviewed working chain. This task does not silently merge or reset main, change remote defaults, or authorize database migration. After explicit integration approval, a fast-forward is sufficient if main has not diverged:','', '```sh','git fetch origin','git switch main','git merge --ff-only codex/food-candidate-manuscript-workflow-20261105','git push origin main','```','', 'Those integration commands are instructions, not operations performed by this task. If `--ff-only` fails, inspect divergence and resolve deliberately; do not force-push. For a fresh clone before main integration:','', '```sh','git switch --track origin/codex/food-candidate-manuscript-workflow-20261105','python run_pipeline.py --tables-only','```','', 'Future changes should use one purpose-specific branch from the agreed current authority, retain source baselines, and commit only reviewed scope. See `07_quality_control/branch_inventory.json` for actual tips and containment.']
(ROOT/'00_project/Git_Workflow.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(f'Indexes: {len(source_rows)} source tables, {len(fig)} figure pairs; branch ancestry recorded.')
