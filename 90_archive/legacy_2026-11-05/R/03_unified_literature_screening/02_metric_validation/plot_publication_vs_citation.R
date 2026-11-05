# ============================================================
# Figure: Publication count versus OpenAlex citations
# Scientific question: Does research-density ranking align with citation attention?
# Project: Antioxidants Project
# Stage: 25A.1
# Input data: data/literature_screening/master/Literature_Screening_Candidate_Master.csv
# Required columns: canonical_name, class, primary_rank, citation_rank, metadata_deduplicated_original_publication_N, total_citation_N
# Filtering: positive x/y values; labels for primary Top15 or citation Top10
# Transformation: log10 axes once; no exponentiation
# Statistical / ranking definition: metadata publication proxy versus OpenAlex citations
# Output: figures/.../02_metric_validation/Literature_Screening_Publication_Count_vs_Citations.png
# Scientific interpretation: convergence/divergence of maturity metrics
# Major caveat: citations reflect attention and age, not evidence quality
# User-editable settings: dimensions, DPI, font sizes, point/label sizes, SHOW_LABELS, class colors
# ============================================================
source(file.path("R","common","bootstrap.R"));FIG_WIDTH<-13;FIG_HEIGHT<-9
d<-read_project_csv("data","literature_screening","master","Literature_Screening_Candidate_Master.csv") %>% filter(metadata_deduplicated_original_publication_N>0,total_citation_N>0)
lab<-d %>% filter(primary_rank<=15|citation_rank<=10)
p<-ggplot(d,aes(metadata_deduplicated_original_publication_N,total_citation_N,color=class))+geom_point(alpha=.7,size=POINT_SIZE)+scale_color_manual(values=CLASS_COLORS)+scale_x_log10(labels=scales::label_number())+scale_y_log10(labels=scales::label_number())+theme_atlas+labs(title="Publication density versus OpenAlex citations",subtitle="Single log10 transformation; OpenAlex is the sole citation source",x="Metadata-deduplicated original publications (log10)",y="OpenAlex citations (log10)",color="Class")
if(SHOW_LABELS)p<-p+geom_text(data=lab,aes(label=canonical_name),vjust=-.7,size=LABEL_SIZE,check_overlap=TRUE,show.legend=FALSE)
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","03_unified_literature_screening","02_metric_validation","Literature_Screening_Publication_Count_vs_Citations.png"),FIG_WIDTH,FIG_HEIGHT)
