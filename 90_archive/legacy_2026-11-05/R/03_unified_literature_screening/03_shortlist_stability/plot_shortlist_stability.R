# ============================================================
# Figure: Shortlist stability Top20 to Top60
# Scientific question: How stable is primary membership under supporting metrics?
# Project: Antioxidants Project
# Stage: 25A.1
# Input data: data/literature_screening/shortlist/Stage25A_Shortlist_Cutoff_Sensitivity.csv
# Required columns: cutoff_N and metric overlap counts
# Filtering: cutoffs 20,30,40,50,60
# Transformation: overlap count divided by cutoff N
# Statistical / ranking definition: candidate retention fraction
# Output: figures/.../03_shortlist_stability/Literature_Screening_Shortlist_Stability_Top20_to_Top60.png
# Scientific interpretation: rank robustness across literature dimensions
# Major caveat: metrics share underlying publication records
# User-editable settings: dimensions, DPI, font sizes, label size
# ============================================================
source(file.path("R","common","bootstrap.R"));FIG_WIDTH<-10;FIG_HEIGHT<-6
d<-read_project_csv("data","literature_screening","shortlist","Stage25A_Shortlist_Cutoff_Sensitivity.csv")%>%transmute(cutoff_N,Publication=citation_metric_overlap_N/cutoff_N,`Citation/year`=citation_per_year_overlap_N/cutoff_N,Recent=recent_5y_overlap_N/cutoff_N,Human=human_evidence_overlap_N/cutoff_N)%>%pivot_longer(-cutoff_N,names_to="metric",values_to="retention")
p<-ggplot(d,aes(factor(cutoff_N),metric,fill=retention))+geom_tile(color="white")+geom_text(aes(label=scales::percent(retention,accuracy=1)),size=LABEL_SIZE)+scale_fill_gradient(limits=c(0,1),low="#F2E8CF",high="#2A9D8F",labels=scales::percent)+theme_atlas+labs(title="Shortlist stability across literature metrics",subtitle="Retention of primary candidates at Top20–Top60",x="Shortlist size",y=NULL,fill="Retention")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","03_unified_literature_screening","03_shortlist_stability","Literature_Screening_Shortlist_Stability_Top20_to_Top60.png"),FIG_WIDTH,FIG_HEIGHT)
