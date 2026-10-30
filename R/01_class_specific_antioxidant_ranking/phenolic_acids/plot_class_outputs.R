# ============================================================
# Figure: Phenolic acids / conjugates canonical ranking, evidence depth, and literature coverage
# Scientific question: What is the current within-class antioxidant ranking and evidence robustness?
# Project: Antioxidants Project
# Stage: 24 / modularized in 25A.1
# Input data: data/class_specific_antioxidant/Polyphenols_PhenolicAcids_TopN_v1.0.csv; Aqueous_Antioxidant_Primary_Literature_Evidence.csv
# Required columns: compound, subclass, median_H_ORAC, eligible_record_count, confidence; evidence DOI/rank fields
# Filtering: existing frozen rank output; no candidate generation or re-ranking
# Transformation: reorder by existing value; count evidence records by DOI status
# Statistical / ranking definition: frozen class-specific construct; evidence depth kept separate
# Output: three canonical PNG files in the matching class figure folder
# Scientific interpretation: within-class only
# Major caveat: no cross-construct raw-value comparison; single-study estimates remain fragile
# User-editable settings: FIG_WIDTH, FIG_HEIGHT, FIG_DPI, font sizes, point/label sizes, SHOW_LABELS
# ============================================================
source(file.path("R","common","bootstrap.R"));FIG_WIDTH<-11;FIG_HEIGHT<-7
rank<-read_project_csv("data","class_specific_antioxidant","Polyphenols_PhenolicAcids_TopN_v1.0.csv")
ev<-read_project_csv("data","class_specific_antioxidant","Aqueous_Antioxidant_Primary_Literature_Evidence.csv")%>%filter(analysis_panel=="Polyphenols - Phenolic acids / conjugates",rank_eligible=="yes")
out<-file.path(project_root(),"figures","aqueous_antioxidant_atlas","01_class_specific_antioxidant_ranking","phenolic_acids")
p1<-rank%>%mutate(compound=fct_reorder(compound,median_H_ORAC))%>%ggplot(aes(median_H_ORAC,compound,color=subclass,shape=confidence))+geom_point(size=POINT_SIZE)+theme_atlas+labs(title="Phenolic acids / conjugates: current within-class ranking",subtitle="Frozen literature-derived class construct",x="Primary antioxidant value",y=NULL,color="Subclass",shape="Confidence")
if(SHOW_LABELS)p1<-p1+geom_text(aes(label=paste0("n=",eligible_record_count)),nudge_x=max(rank$median_H_ORAC,na.rm=TRUE)*.025,size=LABEL_SIZE,show.legend=FALSE)
p1 <- p1 + scale_color_discrete(labels=function(x) stringr::str_wrap(x,24),guide=guide_legend(nrow=2))
save_figure(p1,file.path(out,"PhenolicAcids_TopN.png"),FIG_WIDTH,FIG_HEIGHT)
p2<-ggplot(rank,aes(eligible_record_count,median_H_ORAC,label=compound,color=confidence))+geom_point(size=POINT_SIZE)+ggrepel::geom_text_repel(size=LABEL_SIZE,seed=20261030,max.overlaps=Inf,box.padding=0.4,min.segment.length=0,show.legend=FALSE)+scale_color_manual(values=CONFIDENCE_COLORS)+theme_atlas+labs(title="Phenolic acids / conjugates: evidence depth",subtitle="Magnitude and evidence depth remain separate",x="Eligible record count",y="Primary antioxidant value",color="Confidence")
p2 <- p2 + scale_x_continuous(expand=expansion(mult=c(.18,.18))) + scale_y_continuous(expand=expansion(mult=c(.08,.1)))
save_figure(p2,file.path(out,"PhenolicAcids_Evidence_Depth.png"),10,6)
cov<-ev%>%mutate(doi_status=if_else(is.na(DOI)|DOI=="","DOI missing","DOI recorded"))%>%count(compound,doi_status,name="records")
p3<-ggplot(cov,aes(records,fct_reorder(compound,records,.fun=sum),fill=doi_status))+geom_col()+theme_atlas+labs(title="Phenolic acids / conjugates: primary-literature coverage",subtitle="Every bar resolves to record-level provenance",x="Rank-eligible records",y=NULL,fill="Traceability")
save_figure(p3,file.path(out,"PhenolicAcids_Primary_Literature_Coverage.png"),11,max(5,.28*n_distinct(cov$compound)+2))
