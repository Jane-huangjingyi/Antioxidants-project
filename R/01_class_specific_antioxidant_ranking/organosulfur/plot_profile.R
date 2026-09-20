# ============================================================
# Figure: Organosulfur redox-mechanism profile
# Scientific question: Which distinct redox mechanisms are supported for organosulfur compounds?
# Project: Antioxidants Project
# Stage: 24 / modularized 25A.1
# Input data: data/class_specific_antioxidant/Organosulfur_Redox_Profile.csv
# Required columns: compound, assay, construct, evidence_tier, DOI
# Filtering: records with DOI
# Transformation: distinct evidence units
# Statistical / ranking definition: mechanism profile only
# Output: Organosulfur_Redox_Mechanism_Profile.png
# Scientific interpretation: construct-specific coverage
# Major caveat: KEAP1, thiol and radical kinetics are not interchangeable
# User-editable settings: dimensions, DPI, fonts, point size
# ============================================================
source(file.path("R","common","bootstrap.R"));d<-read_project_csv("data","class_specific_antioxidant","Organosulfur_Redox_Profile.csv")%>%filter(!is.na(DOI))%>%distinct(compound,assay,construct,evidence_tier)%>%mutate(label=paste(compound,assay,sep=" | "))
p<-ggplot(d,aes(evidence_tier,fct_reorder(label,evidence_tier),color=compound))+geom_point(size=POINT_SIZE)+theme_atlas+labs(title="Organosulfur redox-mechanism profile",subtitle="KEAP1 sensing, thiol chemistry, Fenton and radical kinetics remain separate",x="Evidence tier / role",y=NULL,color="Compound")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","01_class_specific_antioxidant_ranking","organosulfur","Organosulfur_Redox_Mechanism_Profile.png"),13,7)
