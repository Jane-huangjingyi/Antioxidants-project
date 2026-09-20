# ============================================================
# Figure: Vitamin C primary-literature coverage
# Scientific question: What rank-eligible primary evidence supports the aqueous vitamin subpanel?
# Project: Antioxidants Project
# Stage: 23–24 / modularized 25A.1
# Input data: data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv
# Required columns: analysis_panel, rank_eligible, compound, DOI
# Filtering: Vitamin C aqueous; rank eligible
# Transformation: DOI status counts
# Statistical / ranking definition: coverage only
# Output: VitaminC_Primary_Literature_Coverage.png
# Scientific interpretation: provenance completeness
# Major caveat: singleton panel percentile is not informative
# User-editable settings: dimensions, DPI, fonts, bar width
# ============================================================
source(file.path("R","common","bootstrap.R"));d<-read_project_csv("data","class_specific_antioxidant","Aqueous_Antioxidant_Primary_Literature_Evidence.csv")%>%filter(analysis_panel=="Vitamin C — aqueous",rank_eligible=="yes")%>%mutate(doi_status=if_else(is.na(DOI)|DOI=="","DOI missing","DOI recorded"))%>%count(compound,doi_status,name="records")
p<-ggplot(d,aes(records,fct_reorder(compound,records),fill=doi_status))+geom_col(width=BAR_WIDTH)+theme_atlas+labs(title="Vitamin C primary-literature coverage",subtitle="Aqueous subpanel; percentile not informative for a single eligible candidate",x="Rank-eligible records",y=NULL,fill="Traceability")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","01_class_specific_antioxidant_ranking","water_soluble_vitamins","VitaminC_Primary_Literature_Coverage.png"),10,5)
