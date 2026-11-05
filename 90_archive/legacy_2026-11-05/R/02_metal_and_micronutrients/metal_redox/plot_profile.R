# ============================================================
# Figure: Metal chelation or Fenton evidence profile
# Scientific question: How do binding, reduction and net oxidative endpoints differ by metal context?
# Project: Antioxidants Project
# Stage: 24 / modularized 25A.1
# Input data: data/metal_and_micronutrients/Aqueous_Metal_Redox_Evidence.csv
# Required columns: compound, oxidation_state, evidence_strength, chelation_or_reduction
# Filtering: none
# Transformation: preserve source-table compound order; no numeric aggregation of categorical evidence labels
# Statistical / ranking definition: mechanism profile only
# Output: Metal_Chelation_or_Fenton_Evidence_Profile.png
# Scientific interpretation: Fe/Cu context-specific evidence
# Major caveat: not an ORAC competitor ranking
# User-editable settings: dimensions, DPI, fonts, point/label size
# ============================================================
source(file.path("R","common","bootstrap.R"));d<-read_project_csv("data","metal_and_micronutrients","Aqueous_Metal_Redox_Evidence.csv")%>%mutate(compound=factor(compound,levels=rev(unique(compound))))
p<-ggplot(d,aes(oxidation_state,compound,color=evidence_strength))+geom_point(size=POINT_SIZE)+geom_text(aes(label=chelation_or_reduction),nudge_y=.18,size=LABEL_SIZE-0.6,color="#333333")+scale_color_manual(values=CONFIDENCE_COLORS)+theme_atlas+theme(axis.text.x=element_text(angle=20,hjust=1))+labs(title="Fe/Cu chelation and Fenton-context profile",subtitle="Binding, reduction and net oxidative endpoints are not interchangeable",x="Oxidation-state context",y=NULL,color="Evidence")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","02_metal_and_micronutrients","metal_redox","Metal_Chelation_or_Fenton_Evidence_Profile.png"),15,8)
