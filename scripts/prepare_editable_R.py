"""One-time restoration of explicit supporting-figure recipes from preserved legacy R."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
if (root/'R/supporting/render_supporting_figures.R').exists():
 raise SystemExit('One-time restoration already complete. Edit canonical R scripts directly; do not overwrite them.')
source=root/'archive/R_legacy/plot_antioxidant_atlas_pre_modularization.R'
text=source.read_text(encoding='utf-8-sig').split('# STAGE 23')[0]
text=text[:text.rfind('# =====================================================')]
text=text.replace('GENERATE_LEGACY_FIGURES <- FALSE','GENERATE_LEGACY_FIGURES <- TRUE')
text=text.replace('BASE_FAMILY <- "sans"','BASE_FAMILY <- "Arial"')
text=text.replace('geom_node_text(aes(label=name),repel=TRUE','geom_node_text(aes(label=name),repel=FALSE')
for m in set(re.findall(r'file.path\(root,"data","([^"]+)"\)',text)):
 target=list((root/'data').rglob(m))
 if not target and m.startswith('Global_Top_Overview_Master_'):target=[root/'data/class_specific_antioxidant/Global_Top_Overview_Master_v0.3.csv']
 if not target and m.startswith('Cross_Class_Comparability_Matrix_'):target=[root/'data/class_specific_antioxidant/Cross_Class_Comparability_Matrix_v0.2.csv']
 if len(target)!=1:raise ValueError((m,target))
 text=text.replace(f'file.path(root,"data","{m}")',f'file.path(root,"{target[0].relative_to(root).as_posix()}")')
baseline=__import__('json').loads((root/'workspaces/repository_review_20261030/Baseline.json').read_text(encoding='utf8'))
paths={Path(r['path']).stem:r['path'] for r in baseline['files'] if r['path'].startswith(('figures/candidate_universe/','figures/cross_class_and_lipid_supporting/','figures/supervisor/')) and r['path'].endswith('.png')}
mapping='c('+','.join('"'+k+'"="'+v.removeprefix('figures/')+'"' for k,v in paths.items())+')'
old='save_atlas <- function(p,name,w=WIDTH,h=HEIGHT){ggsave(file.path(outdir,paste0(name,".",OUTPUT_FORMAT)),p,width=w,height=h,dpi=DPI,bg="white")}'
new='''# This map deliberately selects the 21 existing supporting assets only.
SUPPORT_OUTPUTS <- '''+mapping+'''
save_atlas <- function(p,name,w=WIDTH,h=HEIGHT){
 if(!name %in% names(SUPPORT_OUTPUTS)) return(invisible(NULL))
 target <- file.path(root,"figures/editable",SUPPORT_OUTPUTS[[name]])
 dir.create(dirname(target),recursive=TRUE,showWarnings=FALSE)
 set.seed(20261030)
 ggsave(target,p,width=w,height=h,dpi=DPI,bg="white")
 ggsave(sub("\\\\.png$",".svg",target),p,width=w,height=h,device=svglite::svglite,bg="white")
}'''
assert old in text
text=text.replace(old,new).replace('Eligible independent A/B1 records','Eligible historical A/B1 records (independence separately audited)')
text='# Explicit restored supporting recipes; derived from preserved pre-modularization code.\n# Uses current data paths; no scientific scores or ranking tables are rewritten.\nset.seed(20261030)\n'+text
(root/'R/supporting').mkdir(exist_ok=True)
(root/'R/supporting/render_supporting_figures.R').write_text(text,encoding='utf8')
for name in ['01_render_frozen_primary_top20.R','02_render_b2_sensitivity.R']:
 t=(root/'R/stage25b5'/name).read_text(encoding='utf8')
 t=t.replace('"figures/aqueous_antioxidant_atlas"','"figures/editable/aqueous_antioxidant_atlas"')
 t=t.replace('svg(file.path','svglite::svglite(file.path')
 t=t.replace('input <- file.path(root,','source(file.path(root,"R/common/bootstrap.R"))\ninput <- file.path(root,',1)
 if name.startswith('02'):t=t.replace('d <- read.csv','dir.create(outdir,recursive=TRUE,showWarnings=FALSE)\nd <- read.csv')
 (root/'R/stage25b5'/('editable_'+name)).write_text(t,encoding='utf8')
print('Restored 21 supporting recipes and two non-destructive frozen redraw scripts')
