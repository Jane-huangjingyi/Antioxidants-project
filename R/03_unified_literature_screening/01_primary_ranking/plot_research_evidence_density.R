# ============================================================
# Figure: Literature screening research-evidence density Top50
# Scientific question: Which frozen candidates have the densest antioxidant/redox original-publication record?
# Project: Antioxidants Project
# Stage: 25A.1
# Input data: data/literature_screening/master/Literature_Screening_Candidate_Master.csv
# Required columns: canonical_name, class, primary_rank, metadata_deduplicated_original_publication_N
# Filtering: primary_rank <= TOP_N_DISPLAY
# Transformation: reorder by publication count; no scale transformation
# Statistical / ranking definition: metadata-deduplicated original-publication count
# Output: figures/aqueous_antioxidant_atlas/03_unified_literature_screening/01_primary_ranking/Literature_Screening_Research_Evidence_Density_Top50.png
# Scientific interpretation: research maturity only
# Major caveat: not potency, quality, efficacy, or true same-study adjudication
# User-editable settings: dimensions, DPI, font sizes, point size, TOP_N_DISPLAY, class colors
# ============================================================
source(file.path("R","common","bootstrap.R"))
FIG_WIDTH<-14;FIG_HEIGHT<-13;TOP_N_DISPLAY<-50
d<-read_project_csv("data","literature_screening","master","Literature_Screening_Candidate_Master.csv") %>% filter(primary_rank<=TOP_N_DISPLAY) %>% mutate(canonical_name=fct_reorder(canonical_name,metadata_deduplicated_original_publication_N))
p<-ggplot(d,aes(metadata_deduplicated_original_publication_N,canonical_name,color=class))+geom_point(size=POINT_SIZE)+scale_color_manual(values=CLASS_COLORS)+theme_atlas+labs(title="Research-evidence density of frozen aqueous candidates",subtitle="Top 50; metadata-deduplicated original-publication proxy",x="Metadata-deduplicated antioxidant/redox original publications",y=NULL,color="Class")
save_figure(p,file.path(project_root(),"figures","aqueous_antioxidant_atlas","03_unified_literature_screening","01_primary_ranking","Literature_Screening_Research_Evidence_Density_Top50.png"),FIG_WIDTH,FIG_HEIGHT)
