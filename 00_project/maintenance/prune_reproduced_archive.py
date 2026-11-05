"""Remove only archived graphics identical to a registered current export.

Run without arguments to inspect the plan; --apply performs the logged cleanup.
Scientific inputs, frozen assets and process documents are excluded.
"""
from pathlib import Path
import sys, argparse, subprocess
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *

p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');args=p.parse_args()
registry=read_csv(ROOT/'07_quality_control/figure_export_registry.csv')
retained={}
for row in registry:
 for kind in ['png','svg']:
  target=ROOT/row[kind+'_path'];expected=row[kind+'_sha256']
  assert target.is_file() and sha(target)==expected,target
  retained[expected]=(row[kind+'_path'],row['generator'])
frozen={str(source(r['asset_path']).relative_to(ROOT).as_posix()) for r in read_csv(source('data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv'))}
manifest=read_json(ROOT/'07_quality_control/migration_manifest.json')
original={r['new_path']:r for r in manifest['entries']}
log_path=ROOT/'07_quality_control/redundant_cleanup.json'
log=read_json(log_path) if log_path.exists() else []
prior={r['path']:r for r in log};plan=[];conflicts=[]
archive_figures=(LEGACY/'figures').resolve()
for entry in manifest['entries']:
 rel=entry['new_path'];target=(ROOT/rel).resolve()
 if not target.is_relative_to(archive_figures) or target.suffix.lower() not in ['.png','.svg']:continue
 if rel in prior:continue
 assert target.is_file() and sha(target)==entry['sha256'],rel
 if rel in frozen:
  conflicts.append({'path':rel,'disposition':'KEEP_FROZEN_ASSET','reason':'Referenced by approved frozen asset SHA256 manifest.'});continue
 if entry['sha256'] not in retained:
  conflicts.append({'path':rel,'disposition':'KEEP_DIFFERENT_OR_UNREPRODUCED','reason':'No byte-identical current export; an equivalent filename alone is insufficient.'});continue
 replacement,generator=retained[entry['sha256']]
 plan.append({'path':rel,'sha256':entry['sha256'],'retained_path':replacement,'replacement_sha256':entry['sha256'],'generator':generator,'reason':'Archived generated graphic is byte-identical to the registered current reproducible export.','kind':'EXACT_REPRODUCED_FIGURE_DUPLICATE','date':AS_OF,'size_bytes':target.stat().st_size})
write_csv(ROOT/'07_quality_control/Archive_Cleanup_Conflicts.csv',conflicts,['path','disposition','reason'])
if args.apply:
 # Write a recovery manifest before deleting any exact file. No recursive deletion.
 write_json(log_path,log+plan)
 for entry in plan:
  target=(ROOT/entry['path']).resolve();replacement=ROOT/entry['retained_path']
  assert target.is_relative_to(archive_figures) and entry['path'] not in frozen
  assert sha(target)==sha(replacement)==entry['sha256']
  target.unlink()
 # Remove empty figure directories only; source and process directories stay intact.
 for folder in sorted(archive_figures.rglob('*'),key=lambda x:len(x.parts),reverse=True):
  if folder.is_dir() and not folder.is_symlink() and not any(folder.iterdir()):folder.rmdir()
all_deleted=[r for r in read_json(log_path) if r.get('kind')=='EXACT_REPRODUCED_FIGURE_DUPLICATE'] if args.apply else plan
write_csv(ROOT/'07_quality_control/Archive_Removal_Map.csv',all_deleted,['path','retained_path','sha256','replacement_sha256','generator','reason','kind','date','size_bytes'])
summary={'mode':'APPLIED' if args.apply else 'PLAN','exact_figures_in_batch':len(plan),'bytes_in_batch':sum(r['size_bytes'] for r in plan),'frozen_figures_retained':sum(r['disposition']=='KEEP_FROZEN_ASSET' for r in conflicts),'different_or_unreproduced_figures_retained':sum(r['disposition']=='KEEP_DIFFERENT_OR_UNREPRODUCED' for r in conflicts),'scientific_inputs_or_process_records_deleted':0}
write_json(ROOT/'07_quality_control/archive_cleanup_summary.json',summary)
print(summary)
