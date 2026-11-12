"""English navigation and role indexes, without copying the scientific tables they describe."""
from pathlib import Path
import sys,csv,subprocess,os,json
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
def walk(p):
 for q in p.iterdir():
  if q.name in {'node_modules','.runtime_chem','.venv','library','local_library','phase2_r_partial_library','__pycache__','.git','.q','previews','local'} or getattr(q,'is_junction',lambda:False)() or q.is_symlink():continue
  if q.is_dir():yield from walk(q)
  elif q.is_file():yield q
def build_file_index():
 files=[]
 for p in walk(ROOT):
  rel=p.relative_to(ROOT).as_posix()
  if p.name.endswith('.log'):continue
  files.append({'path':rel,'role':'CODE' if p.suffix in {'.py','.R','.mjs'} else 'DOCUMENTATION' if p.suffix=='.md' else 'GENERATED_FIGURE' if p.suffix in {'.svg','.png'} else 'CONFIG_OR_SCIENTIFIC_TABLE','sha256':sha(p),'step':rel.split('/')[0]})
 files=[r for r in files if r['path'] not in {'current_review/FILE_INDEX.csv','07_quality_control/workflow_qc.json','07_quality_control/Workflow_QC.md'}]
 files.sort(key=lambda r:r['path'])
 write_csv(ROOT/'current_review/FILE_INDEX.csv',files)
 return len(files)

if '--files-only' in sys.argv:
 print(f'Current file navigation rebuilt: {build_file_index()} files; local runtimes excluded.')
 raise SystemExit(0)

source_rows=[]
source_manifest=read_json(ROOT/'02_identity_and_evidence/source_manifest.json')
def source_priority(role):
 for index,prefix in enumerate(['SCIENTIFIC_SOURCE_TABLE','FROZEN_REFERENCE','MECHANISM_SOURCE','ORIGINAL_LITERAL','IDENTITY_REFERENCE','METHOD_QC','BIBLIOGRAPHIC','DATED_JOURNAL','DATED_FULL','SCIENTIFIC_ASSESSMENT','SCIENTIFIC_PREPARATION','DATED_SCIENTIFIC_DEVELOPMENT','LOCAL_SOURCE']):
  if role.startswith(prefix):return index
 return 20
source_manifest['records'].sort(key=lambda r:(source_priority(r['role']),r['path']))
roles={r['path']:r['role'] for r in source_manifest['records']}
write_csv(ROOT/'02_identity_and_evidence/results/source_document_index.csv',[{'source_file':r['path'],'scientific_role':r['role'],'sha256':r['sha256'],'bundled':r['bundled'],'available_here':(ROOT/r['path']).exists(),'interpretation':r['interpretation']} for r in source_manifest['records']])
for entry in source_manifest['records']:
 p=ROOT/entry['path']
 if not p.exists():continue
 if p.suffix.lower()!='.csv':continue
 rel=p.relative_to(ROOT).as_posix()
 try:
  with p.open(encoding='utf-8-sig',newline='') as f:r=csv.reader(f);headers=next(r,[]);n=sum(1 for _ in r)
  role=roles[rel]
  if '/archive/' in rel or '/checkpoints/' in rel:role='HISTORICAL_OR_CHECKPOINT_NOT_NEW_INDEPENDENT_EVIDENCE'
  if '/dryrun/' in rel or '/rebuild_check/' in rel:role='ISOLATED_REHEARSAL_OR_REBUILD_NOT_PRODUCTION'
  if '/provenance/Literature_Screening_Publication_' in rel:role='CANDIDATE_PUBLICATION_METADATA_NOT_FULLTEXT_EVIDENCE'
  source_rows.append({'source_file':rel,'record_count':n,'role':role,'sha256':sha(p),'field_names':'; '.join(headers)})
 except (UnicodeError,csv.Error) as e:source_rows.append({'source_file':rel,'record_count':'','role':'READ_ERROR_REQUIRES_REVIEW','sha256':sha(p),'field_names':type(e).__name__})
source_rows.sort(key=lambda r:(source_priority(r['role']),r['source_file']))
write_csv(ROOT/'02_identity_and_evidence/results/source_file_index.csv',source_rows)
build_file_index()
fig=[]
for p in sorted((ROOT/'06_manuscript/figures').rglob('*.png')):
 svg=Path(str(p).replace('/png/','/svg/').replace('\\png\\','\\svg\\')).with_suffix('.svg')
 assert svg.exists(),p
 role='EVIDENCE_MODEL_DIAGNOSTIC' if p.stem in {'Evidence_Model_Heldout','Evidence_Model_Order_Sensitivity'} else 'SIMULATED_ENDPOINT_DIAGNOSTIC' if p.stem=='Capacity_Kinetics_Toy_Diagnostic' else 'EXPLORATORY_MODEL_DIAGNOSTIC' if p.stem in {'Model_Heldout_Predictions','Model_Scaffold_Errors','Model_Order_Stability'} else 'MAIN_CURRENT_WORKFLOW' if 'supplementary' not in p.parts else 'SUPPLEMENTARY_PRESERVED_CONSTRUCT'
 fig.append({'figure_name':p.stem,'role':role,'png_path':p.relative_to(ROOT).as_posix(),'svg_path':svg.relative_to(ROOT).as_posix(),'generator':'05_analysis/R/render_evidence_model.R' if role=='EVIDENCE_MODEL_DIAGNOSTIC' else '05_analysis/R/render_endpoint_simulation.R' if role=='SIMULATED_ENDPOINT_DIAGNOSTIC' else '05_analysis/R/render_model_diagnostics.R' if role=='EXPLORATORY_MODEL_DIAGNOSTIC' else '05_analysis/R/render_manuscript_figures.R' if role.startswith('MAIN') else '05_analysis/render_historical_figures.R','png_sha256':sha(p),'svg_sha256':sha(svg)})
write_csv(ROOT/'07_quality_control/figure_export_registry.csv',fig)
def git(*args):
 try:return subprocess.check_output(['git',*args],cwd=ROOT,encoding='utf8',stderr=subprocess.DEVNULL).strip()
 except (OSError,subprocess.CalledProcessError):return ''
branches=[];base='c6bca4d13e33cf2ce7d1bae7e3d45e69cf4b23b4'
for line in git('for-each-ref','--format=%(refname:short)|%(objectname)|%(upstream:short)','refs/heads').splitlines():
 name,tip,upstream=line.split('|');contained=subprocess.run(['git','merge-base','--is-ancestor',tip,base],cwd=ROOT,stderr=subprocess.DEVNULL).returncode==0
 count=git('rev-list','--count',base+'..'+tip)
 branches.append({'branch':name,'tip_at_audit':tip,'upstream':upstream,'contained_in_layout_baseline':contained,'unique_commits_vs_layout_baseline':int(count) if count else None,'action':'KEEP_AS_TRACEABLE_ANCESTOR_NO_REPEAT_MERGE' if contained else 'ACTIVE_WORKFLOW_BRANCH_OR_NEW_WORK_REVIEW_REQUIRED'})
write_json(ROOT/'07_quality_control/branch_inventory.json',{'audit_date':AS_OF,'baseline_commit':base,'current_branch':git('branch','--show-current'),'main_tip_at_audit':git('rev-parse','main'),'branches':branches})
lines=['# Git workflow and branch interpretation','',f'The current working branch is `{git("branch","--show-current")}`. The reorganization starts from `{base}`; the earlier review, governance and Track B branches are contained in that baseline. Their approvals and HOLD states remain as recorded. A branch name is not a scientific approval.','', '## Current handling','', 'Use the current workflow branch as the single active checkout for this task. Do not merge each old branch again: the branch inventory reports whether its tip is already an ancestor. Preserve old branch names as traceable milestones; none is deleted automatically. The new organization is committed once after QC.','', f'At audit, local main pointed to `{git("rev-parse","main")}`. Main was older than the reviewed working chain. This task does not silently merge or reset main, change remote defaults, or authorize database migration. After explicit integration approval, a fast-forward is sufficient if main has not diverged:','', '```sh','git fetch origin','git switch main','git merge --ff-only codex/food-candidate-manuscript-workflow-20261105','git push origin main','```','', 'Those integration commands are instructions, not operations performed by this task. If `--ff-only` fails, inspect divergence and resolve deliberately; do not force-push. For a fresh clone before main integration:','', '```sh','git switch --track origin/codex/food-candidate-manuscript-workflow-20261105','python run_pipeline.py --tables-only','```','', 'Future changes should use one purpose-specific branch from the agreed current authority, retain source baselines, and commit only reviewed scope. See `07_quality_control/branch_inventory.json` for actual tips and containment.']
(ROOT/'00_project/Git_Workflow.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(f'Indexes: {len(source_rows)} source tables, {len(fig)} figure pairs; branch ancestry recorded.')
