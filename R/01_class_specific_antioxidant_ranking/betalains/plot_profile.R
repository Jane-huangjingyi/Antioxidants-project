# ============================================================
# Figure: Betalain assay-specific evidence profile
# Scientific question: What assay-specific betalain evidence exists without forcing a common raw scale?
# Project: Antioxidants Project
# Stage: 24 / modularized 25A.1
# Input data: data/class_specific_antioxidant/Betalains_Nitrogen_Profile_Evidence.csv
# Required columns: compound, assay, construct, evidence_tier, DOI
# Filtering: records with DOI
# Transformation: distinct compound-assay-construct-tier units
# Statistical / ranking definition: profile only; no ranking
# Output: Betalains_Profile_Comparison.png
# Scientific interpretation: assay coverage by compound
# Major caveat: optical/pH interference and incompatible constructs
# User-editable settings: dimensions, DPI, fonts, point size
# ============================================================
source(file.path("R","common","bootstrap.R"));d<-read_project_csv("data","class_specific_antioxidant","Betalains_Nitrogen_Profile_Evidence.csv")%>%filter(!is.na(DOI))%>%distinct(compound,assay,construct,evidence_tier)%>%mutate(label=paste(compound,assay,sep=" | "))
p<-ggplot(d,aes(evidence_tier,fct_reorder(label,evidence_tier),color=assay))+geom_point(size=POINT_SIZE)+theme_atlas+labs(title="Betalain assay-specific evidence profile",subtitle="LOX-FL and MPO/HOCl kinetics remain separate",x="Evidence tier / role",y=NULL,color="Assay")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","01_class_specific_antioxidant_ranking","betalains","Betalains_Profile_Comparison.png"),12,6)
