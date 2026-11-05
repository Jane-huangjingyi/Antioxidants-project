# ============================================================
# Figure: Three micronutrient redox profiles
# Scientific question: What cofactor, enzyme and prooxidant contexts apply to micronutrients?
# Project: Antioxidants Project
# Stage: 24 / modularized 25A.1
# Input data: data/metal_and_micronutrients/Antioxidant_Micronutrient_Redox_Profile_v2.csv
# Required columns: nutrient, evidence_strength, key_antioxidant_enzyme, prooxidant_context
# Filtering: none
# Transformation: preserve source-table nutrient order; no numeric aggregation of categorical labels
# Statistical / ranking definition: profile only
# Output: three micronutrient PNG files
# Scientific interpretation: cofactor/context evidence, not antioxidant capacity
# Major caveat: minerals do not compete in ORAC ranking
# User-editable settings: dimensions, DPI, fonts, point size
# ============================================================
source(file.path("R","common","bootstrap.R"));d<-read_project_csv("data","metal_and_micronutrients","Antioxidant_Micronutrient_Redox_Profile_v2.csv")%>%mutate(nutrient=factor(nutrient,levels=rev(unique(nutrient))));out<-file.path(project_root(),"figures","aqueous_antioxidant_atlas","02_metal_and_micronutrients","micronutrients")
p1<-ggplot(d,aes(evidence_strength,nutrient,color=evidence_strength))+geom_point(size=POINT_SIZE)+scale_color_manual(values=CONFIDENCE_COLORS)+theme_atlas+theme(legend.position="none")+labs(title="Micronutrient redox profile",subtitle="Evidence support, not antioxidant capacity",x="Evidence strength",y=NULL)
p2<-ggplot(d,aes(key_antioxidant_enzyme,nutrient,color=nutrient))+geom_point(size=POINT_SIZE)+theme_atlas+theme(legend.position="none",axis.text.x=element_text(angle=30,hjust=1))+labs(title="Micronutrient antioxidant-enzyme map",subtitle="Cofactor systems are separate from ORAC",x="Enzyme / redox system",y=NULL)
p3<-ggplot(d,aes(prooxidant_context,nutrient,color=evidence_strength))+geom_point(size=POINT_SIZE)+scale_color_manual(values=CONFIDENCE_COLORS)+theme_atlas+theme(axis.text.x=element_text(angle=25,hjust=1))+labs(title="Micronutrient prooxidant and toxicity context",subtitle="Dose and baseline status can reverse interpretation",x="Risk context",y=NULL,color="Evidence")
save_figure(p1,file.path(out,"Micronutrient_Redox_Profile.png"),10,6);save_figure(p2,file.path(out,"Micronutrient_Antioxidant_Enzyme_Map.png"),12,7);save_figure(p3,file.path(out,"Micronutrient_Prooxidant_Context.png"),13,7)
