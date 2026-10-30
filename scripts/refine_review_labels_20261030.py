"""Plot-label layout only, retaining all point coordinates and scientific inputs."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for folder in ['flavonoids','phenolic_acids','stilbenes_lignans','other_aqueous_phytochemicals']:
 p=root/'R/01_class_specific_antioxidant_ranking'/folder/'plot_class_outputs.R';s=p.read_text(encoding='utf8')
 s=s.replace('geom_text(vjust=-.7,size=LABEL_SIZE,check_overlap=TRUE)','ggrepel::geom_text_repel(size=LABEL_SIZE,seed=20261030,max.overlaps=Inf,box.padding=0.4,min.segment.length=0,show.legend=FALSE)')
 s=s.replace('save_figure(p1,','p1 <- p1 + scale_color_discrete(labels=function(x) stringr::str_wrap(x,24),guide=guide_legend(nrow=2))\nsave_figure(p1,') if 'str_wrap(x,24)' not in s else s
 s=s.replace('save_figure(p2,','p2 <- p2 + scale_x_continuous(expand=expansion(mult=c(.18,.18))) + scale_y_continuous(expand=expansion(mult=c(.08,.1)))\nsave_figure(p2,') if 'expand=expansion(mult=c(.18,.18))' not in s else s
 p.write_text(s,encoding='utf8')
