# ============================================================
# Figure: Class representation Top20 to Top60
# Scientific question: Which classes remain under publication-density cutoffs without quotas?
# Project: Antioxidants Project
# Stage: 25A.1
# Input data: data/literature_screening/qc/Literature_Screening_Class_Representation_Sensitivity.csv
# Required columns: class, Top20_N ... Top60_N
# Filtering: none
# Transformation: wide-to-long only
# Statistical / ranking definition: retained candidate count
# Output: figures/.../04_class_representation/Literature_Screening_Class_Representation_Top20_to_Top60.png
# Scientific interpretation: observed representation; no balancing quota
# Major caveat: publication density differs systematically by class
# User-editable settings: dimensions, DPI, font sizes, bar width, class colors
# ============================================================
source(file.path("R","common","bootstrap.R"));FIG_WIDTH<-13;FIG_HEIGHT<-8
d<-read_project_csv("data","literature_screening","qc","Literature_Screening_Class_Representation_Sensitivity.csv")%>%select(class,starts_with("Top"))%>%pivot_longer(-class,names_to="cutoff",values_to="retained_N")%>%mutate(cutoff=factor(cutoff,levels=paste0("Top",c(20,30,40,50,60),"_N"),labels=paste0("Top",c(20,30,40,50,60))))
p<-ggplot(d,aes(cutoff,retained_N,fill=class))+geom_col(width=BAR_WIDTH)+scale_fill_manual(values=CLASS_COLORS)+theme_atlas+labs(title="Class representation across shortlist cutoffs",subtitle="Observed retention without class quotas",x="Primary shortlist cutoff",y="Candidates retained",fill="Class")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","03_unified_literature_screening","04_class_representation","Literature_Screening_Class_Representation_Top20_to_Top60.png"),FIG_WIDTH,FIG_HEIGHT)
