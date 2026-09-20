# ============================================================
# Figure: Recent versus historical publication evidence
# Scientific question: Which candidates combine accumulated and recent research activity?
# Project: Antioxidants Project
# Stage: 25A.1
# Input data: data/literature_screening/master/Literature_Screening_Candidate_Master.csv
# Required columns: canonical_name, class, primary_rank, antioxidant_publication_N, recent_5y_publication_N
# Filtering: positive x/y values
# Transformation: log10 axes once; labels use vjust, not numeric nudge on transformed scale
# Statistical / ranking definition: all included publications versus 2022–2026 publications
# Output: figures/.../02_metric_validation/Literature_Screening_Recent_vs_Historical_Evidence.png
# Scientific interpretation: historic accumulation versus current activity
# Major caveat: publication activity is not potency or quality
# User-editable settings: dimensions, DPI, font sizes, point/label sizes, SHOW_LABELS, class colors
# ============================================================
source(file.path("R","common","bootstrap.R"));FIG_WIDTH<-13;FIG_HEIGHT<-9
d<-read_project_csv("data","literature_screening","master","Literature_Screening_Candidate_Master.csv") %>% filter(antioxidant_publication_N>0,recent_5y_publication_N>0)
lab<-d%>%filter(primary_rank<=15)
p<-ggplot(d,aes(antioxidant_publication_N,recent_5y_publication_N,color=class))+geom_point(alpha=.7,size=POINT_SIZE)+scale_color_manual(values=CLASS_COLORS)+scale_x_log10(labels=scales::label_number())+scale_y_log10(labels=scales::label_number())+theme_atlas+labs(title="Recent versus historical research evidence",subtitle="Recent window: 2022–2026; single log10 transformation",x="All included original publications (log10)",y="Recent five-year publications (log10)",color="Class")
if(SHOW_LABELS)p<-p+geom_text(data=lab,aes(label=canonical_name),vjust=-.7,size=LABEL_SIZE,check_overlap=TRUE,show.legend=FALSE)
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","03_unified_literature_screening","02_metric_validation","Literature_Screening_Recent_vs_Historical_Evidence.png"),FIG_WIDTH,FIG_HEIGHT)
