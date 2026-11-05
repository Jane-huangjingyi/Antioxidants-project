"""Adapt the existing maintained R recipes in place in their new active module."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[2];old=ROOT/'90_archive/legacy_2026-11-05/R';new=ROOT/'05_analysis/legacy_modules'
if new.exists():raise SystemExit('Already activated. Edit the active R source directly; do not overwrite.')
for p in old.rglob('*.R'):
 rel=p.relative_to(old)
 if rel.parts[0]=='library' or rel.name=='reproduce_all_figures.R':continue
 if rel.parts[0]=='stage25b5' and not rel.name.startswith('editable_'):continue
 q=new/rel;q.parent.mkdir(parents=True,exist_ok=True)
 t=p.read_text(encoding='utf-8-sig')
 t=t.replace('"R/','"05_analysis/legacy_modules/')
 t=t.replace('file.path("R","common"','file.path("05_analysis","legacy_modules","common"')
 t=t.replace('file.path("R","library")','file.path("90_archive","legacy_2026-11-05","R","library")')
 t=t.replace('file.path(root, "data/','file.path(root, "90_archive/legacy_2026-11-05/data/').replace('file.path(root,"data/','file.path(root,"90_archive/legacy_2026-11-05/data/')
 t=t.replace('"figures/editable','"06_manuscript/figures/supplementary')
 t=t.replace('"Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md"','"run_pipeline.py"')
 if rel.name=='data_helpers.R':t=t.replace('file.path(project_root(),...)','file.path(project_root(),"90_archive","legacy_2026-11-05",...)')
 if rel.name=='plot_helpers.R':
  t=t.replace('ensure_parent(paste0(target,".png"))','ensure_parent(file.path(dirname(target),"analysis_v0.1","png",paste0(basename(target),".png")))')
  t=t.replace('ensure_parent(paste0(target,".svg"))','ensure_parent(file.path(dirname(target),"analysis_v0.1","svg",paste0(basename(target),".svg")))')
 if rel.parts[0]=='supporting':
  t=t.replace('dir.create(dirname(target),recursive=TRUE,showWarnings=FALSE)','png_target <- file.path(dirname(target),"analysis_v0.1","png",basename(target))\n svg_target <- file.path(dirname(target),"analysis_v0.1","svg",sub("\\\\.png$",".svg",basename(target)))\n dir.create(dirname(png_target),recursive=TRUE,showWarnings=FALSE)\n dir.create(dirname(svg_target),recursive=TRUE,showWarnings=FALSE)')
  t=t.replace('ggsave(target,p,','ggsave(png_target,p,').replace('ggsave(sub("\\\\.png$",".svg",target),p,','ggsave(svg_target,p,')
 if rel.parts[0]=='stage25b5':
  t=t.replace('png(file.path(outdir,','png(file.path(outdir,"analysis_v0.1/png",').replace('svglite::svglite(file.path(outdir,','svglite::svglite(file.path(outdir,"analysis_v0.1/svg",')
  t=t.replace('d <- read.csv','dir.create(file.path(outdir,"analysis_v0.1/png"),recursive=TRUE,showWarnings=FALSE)\ndir.create(file.path(outdir,"analysis_v0.1/svg"),recursive=TRUE,showWarnings=FALSE)\nd <- read.csv')
 q.write_text('# Supplementary historical construct; not the current review-panel result.\n'+t.rstrip()+'\n',encoding='utf8')
print('Activated existing R recipes with new input/output routing; numerical data remain immutable.')
