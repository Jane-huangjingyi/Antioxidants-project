# ============================================================
# Figure: Evidence-domain breadth Top30
# Scientific question: How broad are the evidence domains of high-density candidates?
# Project: Antioxidants Project
# Stage: 25A.1
# Input data: candidate master and publication provenance
# Required columns: candidate name/rank; primary inclusion and domain flags
# Filtering: included publications; primary Top30
# Transformation: domain counts and log10(N+1) fill
# Statistical / ranking definition: metadata-domain publication counts
# Output: figures/.../05_evidence_breadth/Literature_Screening_Evidence_Domain_Breadth_Top30.png
# Scientific interpretation: domain breadth separate from publication magnitude
# Major caveat: metadata labels are not evidence-quality grades
# User-editable settings: dimensions, DPI, font sizes, TOP_N_DISPLAY
# ============================================================
source(file.path("R","common","bootstrap.R"));FIG_WIDTH<-11;FIG_HEIGHT<-10;TOP_N_DISPLAY<-30
m<-read_project_csv("data","literature_screening","master","Literature_Screening_Candidate_Master.csv")
p0<-read_project_csv("data","literature_screening","provenance","Literature_Screening_Publication_Provenance.csv")
d<-p0%>%filter(include_primary_metric=="yes")%>%mutate(across(c(chemical_assay,cellular,animal,human,redox_mechanism),~.x=="yes"))%>%group_by(canonical_name)%>%summarise(Chemical=sum(chemical_assay),Cellular=sum(cellular),Animal=sum(animal),Human=sum(human),Mechanism=sum(redox_mechanism),.groups="drop")%>%inner_join(m%>%filter(primary_rank<=TOP_N_DISPLAY)%>%select(canonical_name,primary_rank),by="canonical_name")%>%pivot_longer(c(Chemical,Cellular,Animal,Human,Mechanism),names_to="domain",values_to="N")
p<-ggplot(d,aes(domain,fct_reorder(canonical_name,-primary_rank),fill=log10(N+1)))+geom_tile(color="white")+scale_fill_gradient(low="#F2E8CF",high="#5F0F40")+theme_atlas+labs(title="Evidence-domain breadth of primary Top30",subtitle="Fill is log10(publication count + 1)",x=NULL,y=NULL,fill="log10(N+1)")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","03_unified_literature_screening","05_evidence_breadth","Literature_Screening_Evidence_Domain_Breadth_Top30.png"),FIG_WIDTH,FIG_HEIGHT)
