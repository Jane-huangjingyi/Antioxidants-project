# Antioxidant Functional Factor Atlas: Phase 2 universe + Phase 3A flavonoid figures
# Run from project root: source("R/plot_antioxidant_atlas.R")

# =====================================================
# USER-ADJUSTABLE PLOT SETTINGS
# =====================================================
WIDTH  <- 11                 # saved figure width (inches)
HEIGHT <- 8                  # saved figure height (inches)
DPI <- 300                   # raster resolution
BASE_FAMILY <- "sans"        # font family
BASE_SIZE <- 11              # base font size
TITLE_SIZE <- 15             # title font size
LABEL_SIZE <- 3.2            # node/data label size
LINE_WIDTH <- 0.7            # line/edge width
NODE_SIZE <- 3.5             # hierarchy node size
POINT_SIZE <- 3.2            # point size for ranking figures
LEGEND_POSITION <- "bottom"  # legend placement
LABEL_ANGLE <- 35            # axis-label angle
X_LIMITS <- NULL             # optional c(min,max) for H-ORAC plots; NULL = automatic
LABEL_REPEL <- TRUE          # repel labels in scatter plot
OUTPUT_FORMAT <- "png"       # output format
SUPERVISOR_TOP_N <- 5        # rank positions shown per completed panel; ties retained
SUPERVISOR_WIDTH <- 13       # supervisor overview width (inches)
SUPERVISOR_HEIGHT <- 10      # supervisor overview height (inches)
SUPERVISOR_LABEL_SIZE <- 3.1 # supervisor overview annotation size

SUBCLASS_COLORS <- c(
  "Flavan-3-ols"="#4C78A8", "Flavonols"="#F58518", "Flavonol glycosides"="#ECA82C",
  "Flavones"="#54A24B", "Flavone glycosides"="#8CD17D", "Flavanones"="#B279A2",
  "Flavanone glycosides"="#D4A6C8", "Anthocyanidins"="#E45756", "Anthocyanins"="#FF9DA6",
  "Isoflavones"="#79706E", "Isoflavone glycosides"="#BAB0AC",
  "Hydroxybenzoic acids"="#4C78A8", "Hydroxycinnamic acids"="#F58518",
  "Caffeoylquinic and related acids"="#54A24B", "Other defined phenolic conjugates"="#B279A2"
)

PANEL_ORDER <- c(            # facet/panel display order
  "Polyphenols - Flavonoids",
  "Polyphenols - Phenolic acids / conjugates",
  "Polyphenols - Stilbenes / lignans",
  "Vitamins / vitamin-like",
  "Carotenoids",
  "Organosulfur compounds",
  "Betalains / nitrogen-containing",
  "Other food-derived redox-active phytochemicals",
  "Antioxidant-related micronutrients / mineral cofactors"
)

CLASS_COLORS <- c(           # restrained parent-class palette
  "Polyphenols" = "#4C78A8",
  "Vitamins / vitamin-like antioxidants" = "#F58518",
  "Carotenoids" = "#ECA82C",
  "Organosulfur compounds" = "#B279A2",
  "Betalains / nitrogen-containing phytochemicals" = "#FF9DA6",
  "Other food-derived redox-active phytochemicals" = "#9D755D",
  "Antioxidant-related micronutrients / mineral cofactors" = "#79706E"
)

STATUS_COLORS <- c("eligible"="#4C956C","excluded"="#C95D63","unresolved"="#E6AA68")
CONFIDENCE_COLORS <- c("Low"="#D98C3F","Moderate"="#4C78A8","High"="#3A8D5D","Very low"="#A6A6A6")
STABILITY_COLORS <- c("Stable"="#3A8D5D","Moderately stable"="#4C78A8","Fragile"="#D98C3F")
CAROTENOID_COLORS <- c("Carotenes"="#D89000","Xanthophylls"="#2A9D8F")
ENVIRONMENT_COLORS <- c("homogeneous organic solvent"="#D89000","aqueous micelle"="#4C78A8","liposome"="#2A9D8F","membrane-like system"="#8E6C8A","biological membrane / lipoprotein"="#6B705C")
PRIMARY_CONSTRUCT_COLORS <- c("H-ORAC-FL"="#4C78A8","singlet-oxygen kq"="#D89000")
VITAMIN_C_COLOR <- "#4C78A8"
TOCOPHEROL_COLORS <- c(alpha="#3A8D5D",beta="#4C78A8",gamma="#D89000",delta="#8E6C8A")
TOCOTRIENOL_COLORS <- c(alpha="#79B69A",beta="#8CB6D9",gamma="#F2B84B",delta="#B6A0B5")
CONSTRUCT_COLORS <- c("H-ORAC-FL"="#4C78A8","peroxyl-radical k_inh"="#D89000","singlet-oxygen kq"="#2A9D8F")

# =====================================================
# DEPENDENCIES, INPUT AND THEME
# =====================================================
project_library <- normalizePath(file.path("R","library"),mustWork=FALSE)
if(dir.exists(project_library)) .libPaths(c(project_library,.libPaths()))
required <- c("ggplot2","dplyr","tidyr","readr","stringr","forcats","scales","igraph","ggraph","ggrepel","patchwork")
missing <- required[!vapply(required,requireNamespace,quietly=TRUE,FUN.VALUE=logical(1))]
if(length(missing)>0) stop("Missing R packages: ",paste(missing,collapse=", "),". Install before sourcing.")
suppressPackageStartupMessages({library(ggplot2);library(dplyr);library(tidyr);library(readr);library(stringr);library(forcats);library(scales);library(igraph);library(ggraph);library(ggrepel);library(patchwork)})

root <- normalizePath(".",mustWork=TRUE)
candidate_path <- file.path(root,"data","Antioxidant_Class_Candidate_Master.csv")
taxonomy_path <- file.path(root,"data","Antioxidant_Taxonomy_Relationships.csv")
exclusion_path <- file.path(root,"data","Antioxidant_Candidate_Exclusions.csv")
top20_path <- file.path(root,"data","Polyphenols_Flavonoids_Top20_v1.0.csv")
coverage_path <- file.path(root,"data","Flavonoid_Ranking_Coverage.csv")
phenolic_topn_path <- file.path(root,"data","Polyphenols_PhenolicAcids_TopN_v1.0.csv")
phenolic_coverage_path <- file.path(root,"data","PhenolicAcid_Ranking_Coverage.csv")
global_overview_path <- file.path(root,"data","Global_Top_Overview_Master_v0.1.csv")
global_overview_v02_path <- file.path(root,"data","Global_Top_Overview_Master_v0.2.csv")
comparability_path <- file.path(root,"data","Cross_Class_Comparability_Matrix_v0.1.csv")
carotenoid_topn_path <- file.path(root,"data","Carotenoids_TopN_v1.0.csv")
carotenoid_evidence_path <- file.path(root,"data","Carotenoid_Singlet_Oxygen_Evidence_Master.csv")
carotenoid_lipid_path <- file.path(root,"data","Carotenoid_LipidPhase_Evidence_Profile.csv")
vitamin_c_path <- file.path(root,"data","VitaminC_TopAvailable_v1.0.csv")
vitamin_e_path <- file.path(root,"data","VitaminE_TopN_v1.0.csv")
vitamin_e_evidence_path <- file.path(root,"data","VitaminE_LipidPhase_Evidence_Master.csv")
vitamin_e_lorac_path <- file.path(root,"data","VitaminE_LORAC_Secondary_Profile.csv")
vitamin_overview_path <- file.path(root,"data","Vitamins_ParentClass_Overview_v1.0.csv")
global_overview_v03_path <- file.path(root,"data","Global_Top_Overview_Master_v0.3.csv")
supervisor_overview_path <- file.path(root,"data","Supervisor_Class_Specific_Ranking_Overview.csv")
outdir <- file.path(root,"figures"); dir.create(outdir,showWarnings=FALSE,recursive=TRUE)

candidates <- read_csv(candidate_path,show_col_types=FALSE)
taxonomy <- read_csv(taxonomy_path,show_col_types=FALSE)
exclusions <- read_csv(exclusion_path,show_col_types=FALSE)
top20 <- read_csv(top20_path,show_col_types=FALSE)
coverage <- read_csv(coverage_path,show_col_types=FALSE)
phenolic_topn <- read_csv(phenolic_topn_path,show_col_types=FALSE)
phenolic_coverage <- read_csv(phenolic_coverage_path,show_col_types=FALSE)
global_overview <- read_csv(global_overview_path,show_col_types=FALSE)
global_overview_v02 <- read_csv(global_overview_v02_path,show_col_types=FALSE)
comparability <- read_csv(comparability_path,show_col_types=FALSE)
carotenoid_topn <- read_csv(carotenoid_topn_path,show_col_types=FALSE)
carotenoid_evidence <- read_csv(carotenoid_evidence_path,show_col_types=FALSE)
carotenoid_lipid <- read_csv(carotenoid_lipid_path,show_col_types=FALSE)
vitamin_c <- read_csv(vitamin_c_path,show_col_types=FALSE)
vitamin_e <- read_csv(vitamin_e_path,show_col_types=FALSE)
vitamin_e_evidence <- read_csv(vitamin_e_evidence_path,show_col_types=FALSE)
vitamin_e_lorac <- read_csv(vitamin_e_lorac_path,show_col_types=FALSE)
vitamin_overview <- read_csv(vitamin_overview_path,show_col_types=FALSE)
global_overview_v03 <- read_csv(global_overview_v03_path,show_col_types=FALSE)
supervisor_overview <- read_csv(supervisor_overview_path,show_col_types=FALSE)

theme_atlas <- theme_minimal(base_family=BASE_FAMILY,base_size=BASE_SIZE)+theme(plot.title=element_text(size=TITLE_SIZE,face="bold"),plot.subtitle=element_text(color="#555555"),panel.grid.minor=element_blank(),legend.position=LEGEND_POSITION,strip.text=element_text(face="bold"))
save_atlas <- function(p,name,w=WIDTH,h=HEIGHT){ggsave(file.path(outdir,paste0(name,".",OUTPUT_FORMAT)),p,width=w,height=h,dpi=DPI,bg="white")}

# Figure 1: deliberately limited to root → parent class → major analysis panel.
# Subclasses are omitted from the main tree to keep the scientific hierarchy legible.
nodes_parent <- candidates %>% distinct(parent_class)
poly_panels <- candidates %>% filter(parent_class=="Polyphenols") %>% distinct(analysis_panel)
edges <- bind_rows(
  nodes_parent %>% transmute(from="Antioxidant Functional Factors",to=parent_class),
  poly_panels %>% transmute(from="Polyphenols",to=analysis_panel)
)
graph <- graph_from_data_frame(edges,directed=TRUE)
node_df <- tibble(name=V(graph)$name) %>% mutate(parent_class=case_when(name %in% candidates$parent_class~name,name %in% poly_panels$analysis_panel~"Polyphenols",TRUE~"Root"))
V(graph)$parent_class <- node_df$parent_class
p1 <- ggraph(graph,layout="tree")+geom_edge_link(color="#B8B8B8",linewidth=LINE_WIDTH,alpha=.85)+geom_node_point(aes(color=parent_class),size=NODE_SIZE)+geom_node_text(aes(label=name),repel=TRUE,size=LABEL_SIZE,family=BASE_FAMILY)+scale_color_manual(values=c(CLASS_COLORS,"Root"="#333333"),drop=FALSE)+coord_flip(clip="off")+theme_void(base_family=BASE_FAMILY)+theme(legend.position="none",plot.title=element_text(size=TITLE_SIZE,face="bold"),plot.subtitle=element_text(color="#555555"),plot.margin=margin(25,120,25,120))+labs(title="Antioxidant Functional Factor Taxonomy",subtitle="Root -> parent class; Polyphenols -> three analysis panels. Subclasses are documented separately.")
save_atlas(p1,"Antioxidant_Taxonomy_Hierarchy",15,9)

# Figure 2: candidate size by analysis panel, colored by parent class.
counts <- candidates %>% count(parent_class,analysis_panel,name="candidate_count") %>% mutate(analysis_panel=factor(analysis_panel,levels=PANEL_ORDER)) %>% arrange(candidate_count)
p2 <- ggplot(counts,aes(candidate_count,fct_reorder(analysis_panel,candidate_count),fill=parent_class))+geom_col(width=.7)+geom_text(aes(label=candidate_count),hjust=-.2,size=LABEL_SIZE)+scale_fill_manual(values=CLASS_COLORS,drop=FALSE)+scale_x_continuous(expand=expansion(mult=c(0,.1)))+theme_atlas+theme(legend.position="none")+labs(title="Candidate universe size by analysis panel",subtitle="Candidate generation is independent of antioxidant performance",x="Candidate count",y=NULL)
save_atlas(p2,"Candidate_Universe_Size_By_Class",11,7)

# Figure 3: subclass composition within panels.
composition <- candidates %>% count(analysis_panel,subclass,name="candidate_count")
p3 <- ggplot(composition,aes(candidate_count,fct_reorder(subclass,candidate_count),fill=analysis_panel))+geom_col(width=.72)+facet_wrap(~analysis_panel,scales="free",ncol=2)+geom_text(aes(label=candidate_count),hjust=-.15,size=LABEL_SIZE-0.3)+scale_x_continuous(expand=expansion(mult=c(0,.2)))+theme_atlas+theme(legend.position="none",axis.text.y=element_text(size=BASE_SIZE-2),strip.text=element_text(size=BASE_SIZE,face="bold"))+labs(title="Subclass composition of the candidate universe",subtitle="Counts are candidates, not ranks or evidence scores",x="Candidate count",y=NULL)
save_atlas(p3,"Candidate_Universe_Subclass_Composition",15,14)

# Figure 4: eligible/unresolved candidates plus retained exclusions by proposed class.
status_candidates <- candidates %>% transmute(parent_class,status=if_else(candidate_eligible=="yes","eligible","unresolved"))
status_excluded <- exclusions %>% transmute(parent_class=case_when(str_detect(proposed_class,"Flavonoid|Polyphenol|Stilbene")~"Polyphenols",str_detect(proposed_class,"Carotenoid")~"Carotenoids",str_detect(proposed_class,"Endogenous|Other")~"Other food-derived redox-active phytochemicals",TRUE~proposed_class),status="excluded")
status <- bind_rows(status_candidates,status_excluded) %>% count(parent_class,status,name="count") %>% complete(parent_class,status=c("eligible","excluded","unresolved"),fill=list(count=0))
p4 <- ggplot(status,aes(count,fct_reorder(parent_class,count,.fun=sum),fill=status))+geom_col(position="stack",width=.72)+geom_text(aes(label=if_else(count>0,as.character(count),"")),position=position_stack(vjust=.5),size=LABEL_SIZE,color="white")+scale_fill_manual(values=STATUS_COLORS,drop=FALSE)+theme_atlas+labs(title="Candidate universe eligibility status",subtitle="Unresolved candidates are retained but cannot enter Phase 3 ranking",x="Count",y=NULL,fill=NULL)
save_atlas(p4,"Candidate_Universe_Eligibility_Status",11,7)

# Phase 3A Figure A: provisional Top20 magnitude; confidence is not encoded as magnitude.
top20_plot <- top20 %>% mutate(compound=fct_reorder(compound,median_H_ORAC), label_n=paste0("n=",eligible_record_count))
p5 <- ggplot(top20_plot,aes(median_H_ORAC,compound,color=subclass))+
  geom_errorbar(aes(xmin=min,xmax=max),width=.18,linewidth=LINE_WIDTH,alpha=.65,orientation="y")+
  geom_point(size=POINT_SIZE)+geom_text(aes(label=label_n),hjust=-.45,size=LABEL_SIZE-0.35,color="#333333")+
  scale_color_manual(values=SUBCLASS_COLORS,drop=FALSE)+theme_atlas+
  scale_x_continuous(limits=X_LIMITS,expand=expansion(mult=c(.03,.14)))+
  labs(title="Polyphenols - Flavonoids Top20 v1.0",subtitle="Literature-derived H-ORAC-FL medians; ranges reflect eligible historical records",x="H-ORAC-FL (mol TE/mol compound)",y=NULL,color="Subclass")
save_atlas(p5,"Flavonoid_Top20_H_ORAC",12,9)

# Phase 3A Figure B: evidence confidence shown separately from capacity.
confidence_levels <- c("Low","Moderate","High")
p6 <- top20 %>% mutate(confidence=factor(confidence,levels=confidence_levels),compound=fct_reorder(compound,rank,.desc=TRUE)) %>%
  ggplot(aes(confidence,compound,color=confidence))+
  geom_point(size=POINT_SIZE+1)+geom_text(aes(label=paste0("n=",eligible_record_count)),nudge_x=.18,size=LABEL_SIZE-0.3,color="#333333")+
  scale_color_manual(values=c(Low="#D98C3F",Moderate="#4C78A8",High="#3A8D5D"),drop=FALSE)+theme_atlas+theme(legend.position="none")+
  labs(title="Evidence confidence of Flavonoid Top20",subtitle="Confidence reflects independent eligible evidence depth and heterogeneity, not antioxidant magnitude",x="Evidence confidence",y=NULL)
save_atlas(p6,"Flavonoid_Top20_Evidence_Confidence",10,9)

# Phase 3A Figure C: coverage funnel by subclass.
subclass_levels <- coverage %>% arrange(universe_N) %>% pull(subclass)
coverage_long <- coverage %>% select(subclass,universe_N,ranking_eligible_N,Top20_N) %>%
  pivot_longer(-subclass,names_to="stage",values_to="N") %>%
  mutate(subclass=factor(subclass,levels=subclass_levels),stage=factor(stage,levels=c("universe_N","ranking_eligible_N","Top20_N"),labels=c("Universe","Eligibility lock","Top20")))
p7 <- ggplot(coverage_long,aes(N,subclass,fill=stage))+
  geom_col(position=position_dodge(width=.78),width=.72)+
  scale_fill_manual(values=c(Universe="#C9D5E3","Eligibility lock"="#4C78A8",Top20="#F58518"))+
  theme_atlas+labs(title="Flavonoid subclass coverage",subtitle="Subclass representation is audited but no quota changes the rank",x="Candidate count",y=NULL,fill=NULL)
save_atlas(p7,"Flavonoid_Subclass_Coverage",11,8)

# Phase 3A Figure D: evidence depth versus magnitude.
p8 <- ggplot(top20,aes(eligible_record_count,median_H_ORAC,color=subclass))+
  geom_point(size=POINT_SIZE,alpha=.9)+scale_color_manual(values=SUBCLASS_COLORS,drop=FALSE)+theme_atlas+
  scale_x_continuous(breaks=pretty_breaks())+
  labs(title="Evidence depth versus H-ORAC-FL",subtitle="Single-study high values require cautious interpretation",x="Eligible independent A/B1 records",y="Median H-ORAC-FL (mol TE/mol)",color="Subclass")
if(LABEL_REPEL) p8 <- p8+geom_text_repel(aes(label=compound),size=LABEL_SIZE-0.5,max.overlaps=25,box.padding=.35)
save_atlas(p8,"Flavonoid_Evidence_Depth_vs_ORAC",11,8)

# Phase 3B Figure A: all currently rankable phenolic acids/conjugates (Top available, N < 20).
pa_plot <- phenolic_topn %>% mutate(compound=fct_reorder(compound,median_H_ORAC),label_n=paste0("n=",eligible_record_count))
p9 <- ggplot(pa_plot,aes(median_H_ORAC,compound,color=subclass))+
  geom_errorbar(aes(xmin=min,xmax=max),width=.18,linewidth=LINE_WIDTH,alpha=.65,orientation="y")+
  geom_point(size=POINT_SIZE)+geom_text(aes(label=label_n),hjust=-.45,size=LABEL_SIZE-0.35,color="#333333")+
  scale_color_manual(values=SUBCLASS_COLORS,drop=FALSE)+theme_atlas+
  scale_x_continuous(limits=X_LIMITS,expand=expansion(mult=c(.03,.14)))+
  labs(title="Phenolic acids / conjugates Top available v1.0",subtitle="Exploratory literature-derived H-ORAC-FL medians; eligible compounds = 18, so no Top20 is claimed",x="H-ORAC-FL (mol TE/mol compound)",y=NULL,color="Subclass")
save_atlas(p9,"PhenolicAcid_TopN_H_ORAC",12,9)

# Phase 3B Figure B: confidence is deliberately separate from ORAC magnitude.
p10 <- phenolic_topn %>% mutate(confidence=factor(confidence,levels=confidence_levels),compound=fct_reorder(compound,rank,.desc=TRUE)) %>%
  ggplot(aes(confidence,compound,color=confidence))+geom_point(size=POINT_SIZE+1)+
  geom_text(aes(label=paste0("n=",eligible_record_count)),nudge_x=.18,size=LABEL_SIZE-0.3,color="#333333")+
  scale_color_manual(values=c(Low="#D98C3F",Moderate="#4C78A8",High="#3A8D5D"),drop=FALSE)+theme_atlas+theme(legend.position="none")+
  labs(title="Evidence confidence of phenolic-acid Top available",subtitle="Confidence reflects eligible independent evidence depth and heterogeneity",x="Evidence confidence",y=NULL)
save_atlas(p10,"PhenolicAcid_Evidence_Confidence",10,9)

# Phase 3B Figure C: subclass coverage funnel.
pa_subclass_levels <- phenolic_coverage %>% arrange(universe_N) %>% pull(subclass)
pa_cov_long <- phenolic_coverage %>% select(subclass,universe_N,ranking_eligible_N,TopN_N) %>%
  pivot_longer(-subclass,names_to="stage",values_to="N") %>%
  mutate(subclass=factor(subclass,levels=pa_subclass_levels),stage=factor(stage,levels=c("universe_N","ranking_eligible_N","TopN_N"),labels=c("Universe","Eligibility lock","Top available")))
p11 <- ggplot(pa_cov_long,aes(N,subclass,fill=stage))+geom_col(position=position_dodge(width=.78),width=.72)+
  scale_fill_manual(values=c(Universe="#C9D5E3","Eligibility lock"="#4C78A8","Top available"="#F58518"))+theme_atlas+
  labs(title="Phenolic-acid subclass coverage",subtitle="Coverage is audited without imposing subclass quotas",x="Candidate count",y=NULL,fill=NULL)
save_atlas(p11,"PhenolicAcid_Subclass_Coverage",11,7)

# Phase 3B Figure D: evidence depth versus capacity.
p12 <- ggplot(phenolic_topn,aes(eligible_record_count,median_H_ORAC,color=subclass))+geom_point(size=POINT_SIZE,alpha=.9)+
  scale_color_manual(values=SUBCLASS_COLORS,drop=FALSE)+theme_atlas+scale_x_continuous(breaks=pretty_breaks())+
  labs(title="Phenolic-acid evidence depth versus H-ORAC-FL",subtitle="High single-study estimates and heterogeneous medians require separate interpretation",x="Eligible independent A/B1 records",y="Median H-ORAC-FL (mol TE/mol)",color="Subclass")
if(LABEL_REPEL) p12 <- p12+geom_text_repel(aes(label=compound),size=LABEL_SIZE-0.5,max.overlaps=25,box.padding=.35)
save_atlas(p12,"PhenolicAcid_Evidence_Depth_vs_ORAC",11,8)

# Phase 3B Figure E: simple rank sensitivity without constructing a composite score.
s_primary <- phenolic_topn %>% transmute(compound,scenario="Primary A/B1",scenario_rank=rank)
s_n2 <- phenolic_topn %>% filter(eligible_record_count>=2) %>% arrange(desc(median_H_ORAC)) %>% mutate(scenario_rank=row_number()) %>% transmute(compound,scenario="n >= 2 only",scenario_rank)
s_hetero <- phenolic_topn %>% filter(heterogeneity_flag!="high") %>% arrange(desc(median_H_ORAC)) %>% mutate(scenario_rank=row_number()) %>% transmute(compound,scenario="Exclude high heterogeneity",scenario_rank)
sensitivity <- bind_rows(s_primary,s_n2,s_hetero) %>% mutate(scenario=factor(scenario,levels=c("Primary A/B1","n >= 2 only","Exclude high heterogeneity")))
p13 <- ggplot(sensitivity,aes(scenario,scenario_rank,group=compound,color=compound))+geom_line(linewidth=LINE_WIDTH,alpha=.55)+geom_point(size=POINT_SIZE-0.4)+
  scale_y_reverse(breaks=pretty_breaks())+theme_atlas+theme(legend.position="none",axis.text.x=element_text(angle=15,hjust=1))+
  labs(title="Phenolic-acid Top-N sensitivity",subtitle="Rank trajectories under evidence-depth and heterogeneity restrictions; missing points indicate exclusion",x=NULL,y="Scenario-specific rank")
p13 <- p13+geom_text(data=sensitivity %>% filter(scenario=="Primary A/B1"),aes(label=compound),hjust=1.08,nudge_x=-.02,size=LABEL_SIZE-0.75,show.legend=FALSE)
save_atlas(p13,"PhenolicAcid_TopN_Sensitivity",11,8)

# Stage 20 Figure 1: class leaders shown on a within-class percentile axis, never on a mixed capacity axis.
global_leaders <- global_overview %>% group_by(analysis_panel) %>% arrange(within_class_rank,.by_group=TRUE) %>% slice_head(n=5) %>% ungroup() %>%
  mutate(compound=factor(compound,levels=rev(unique(compound[order(analysis_panel,within_class_rank)]))))
p14 <- ggplot(global_leaders,aes(within_class_percentile,compound,color=confidence,shape=evidence_stability))+
  geom_point(size=POINT_SIZE+1)+facet_wrap(~analysis_panel,scales="free_y",ncol=1)+
  scale_color_manual(values=CONFIDENCE_COLORS,drop=FALSE)+scale_shape_manual(values=c(Stable=16,`Moderately stable`=17,Fragile=18),drop=FALSE)+
  scale_x_continuous(limits=c(0,100),breaks=seq(0,100,20))+theme_atlas+
  labs(title="Global Overview class leaders",subtitle="Top five per panel; x-axis is within-class percentile, not a cross-class antioxidant magnitude",x="Within-class percentile",y=NULL,color="Confidence",shape="Evidence stability")
save_atlas(p14,"Global_Overview_Class_Leaders",12,8)

# Stage 20 Figure 2: evidence stability across all 38 schema rows.
global_stability <- global_overview %>% arrange(analysis_panel,desc(within_class_rank)) %>% mutate(compound=factor(compound,levels=unique(compound)))
p15 <- ggplot(global_stability,aes(within_class_rank,compound,color=evidence_stability))+
  geom_point(size=POINT_SIZE)+facet_wrap(~analysis_panel,scales="free_y",ncol=2)+
  scale_color_manual(values=STABILITY_COLORS,drop=FALSE)+scale_x_continuous(breaks=pretty_breaks())+theme_atlas+
  theme(axis.text.y=element_text(size=BASE_SIZE-2))+labs(title="Evidence stability in the Global Overview schema",subtitle="Stability describes estimate robustness and remains separate from H-ORAC magnitude",x="Within-class rank",y=NULL,color="Stability")
save_atlas(p15,"Global_Overview_Evidence_Stability",15,10)

# Stage 20 Figure 3: one categorical tile per comparison dimension.
comparability <- comparability %>% mutate(comparison_type=factor(comparison_type,levels=c("Directly comparable","Profile comparable","Not directly comparable")),dimension=factor(dimension,levels=rev(dimension)))
p16 <- ggplot(comparability,aes(comparison_type,dimension,fill=comparison_type))+geom_tile(width=.9,height=.82,color="white",linewidth=LINE_WIDTH)+
  geom_text(label="APPLIES",color="white",size=LABEL_SIZE-0.35,fontface="bold")+
  scale_fill_manual(values=c(`Directly comparable`="#3A8D5D",`Profile comparable`="#4C78A8",`Not directly comparable`="#C95D63"),drop=FALSE)+
  theme_atlas+theme(legend.position="none",axis.text.x=element_text(angle=18,hjust=1))+labs(title="Cross-class comparability matrix",subtitle="The matrix defines valid comparison types; it does not create a global score",x=NULL,y=NULL)
save_atlas(p16,"Cross_Class_Comparability_Matrix",12,9)

# Stage 20 Figure 4: proportion of schema rows still marked Not reviewed / NA.
missingness <- global_overview %>% transmute(analysis_panel,
  Exposure=dietary_exposure_umol_day=="NA" | exposure_quality=="Not reviewed",
  Bioavailability=bioavailability_summary=="Not reviewed",
  `Human evidence`=human_evidence_level=="Not reviewed",
  Mechanism=endogenous_defense_profile=="Not reviewed" | NRF2_GSH_GPX_profile=="Not reviewed",
  `Direct target`=direct_target_level=="Not reviewed",
  Safety=safety_prooxidant_context=="Not reviewed") %>%
  pivot_longer(-analysis_panel,names_to="domain",values_to="missing") %>% group_by(analysis_panel,domain) %>% summarise(missing_pct=mean(missing)*100,.groups="drop")
p17 <- ggplot(missingness,aes(domain,analysis_panel,fill=missing_pct))+geom_tile(color="white",linewidth=LINE_WIDTH)+geom_text(aes(label=paste0(round(missing_pct),"%")),size=LABEL_SIZE,color="#333333")+
  scale_fill_gradient(low="#E8F0F7",high="#D98C3F",limits=c(0,100))+theme_atlas+theme(axis.text.x=element_text(angle=25,hjust=1))+
  labs(title="Global Overview schema missingness",subtitle="Percentage of included compounds not yet systematically reviewed; Not reviewed is not No evidence",x=NULL,y=NULL,fill="Missing")
save_atlas(p17,"Global_Overview_Schema_Missingness",12,5.5)

# Phase 3C Figure A: environment-stratified direct singlet-oxygen kq.
car_top_plot <- carotenoid_topn %>% mutate(compound=fct_reorder(compound,median_kq))
p18 <- ggplot(car_top_plot,aes(median_kq,compound,color=subclass))+
  geom_errorbar(aes(xmin=min,xmax=max),width=.18,linewidth=LINE_WIDTH,alpha=.65,orientation="y")+
  geom_point(size=POINT_SIZE)+geom_text(aes(label=paste0("n=",eligible_record_count)),hjust=-.35,size=LABEL_SIZE-0.35,color="#333333")+
  scale_color_manual(values=CAROTENOID_COLORS,drop=FALSE)+scale_x_continuous(expand=expansion(mult=c(.02,.14)))+theme_atlas+
  labs(title="Carotenoid Top available: direct singlet-oxygen quenching",subtitle="Exploratory organic-solvent kq; environments are not pooled and N=9 does not support a Top10 claim",x=expression(paste("Median ",k[q]," (",10^9," ",M^{-1}," ",s^{-1},")")),y=NULL,color="Subclass")
save_atlas(p18,"Carotenoid_TopN_Primary_Construct",12,7.5)

# Phase 3C Figure B: confidence kept separate from magnitude.
p19 <- carotenoid_topn %>% mutate(confidence=factor(confidence,levels=confidence_levels),compound=fct_reorder(compound,rank,.desc=TRUE)) %>%
  ggplot(aes(confidence,compound,color=confidence))+geom_point(size=POINT_SIZE+1)+
  geom_text(aes(label=paste0("n=",eligible_record_count)),nudge_x=.18,size=LABEL_SIZE-0.3,color="#333333")+
  scale_color_manual(values=CONFIDENCE_COLORS,drop=FALSE)+theme_atlas+theme(legend.position="none")+
  labs(title="Carotenoid evidence confidence",subtitle="Confidence reflects independent eligible records and heterogeneity, not kq magnitude",x="Evidence confidence",y=NULL)
save_atlas(p19,"Carotenoid_Evidence_Confidence",10,7.5)

# Phase 3C Figure C: all record environments, including the secondary membrane profile.
env_counts <- bind_rows(
  carotenoid_evidence %>% count(micelle_or_liposome,name="record_count") %>% rename(environment=micelle_or_liposome),
  carotenoid_lipid %>% count(lipid_system,name="record_count") %>% transmute(environment="liposome",record_count)
) %>% group_by(environment) %>% summarise(record_count=sum(record_count),.groups="drop")
p20 <- ggplot(env_counts,aes(record_count,fct_reorder(environment,record_count),fill=environment))+geom_col(width=.7)+
  geom_text(aes(label=record_count),hjust=-.25,size=LABEL_SIZE)+scale_fill_manual(values=ENVIRONMENT_COLORS,drop=FALSE)+
  scale_x_continuous(expand=expansion(mult=c(0,.14)))+theme_atlas+theme(legend.position="none")+
  labs(title="Carotenoid assay-environment coverage",subtitle="Only homogeneous organic-solvent direct kq currently supports a class list",x="Record/profile rows",y=NULL)
save_atlas(p20,"Carotenoid_Environment_Coverage",10,5.5)

# Phase 3C Figure D: profile-only comparison; values remain on separate facets/scales.
profile_primary <- carotenoid_topn %>% transmute(compound,profile="Organic-solvent direct kq",value=median_kq,label=paste0(round(median_kq,3)," x10^9"))
profile_lipid <- carotenoid_lipid %>% filter(compound %in% c("all-trans-Lycopene","all-trans-beta-Carotene")) %>%
  separate_rows(value,sep=" / ") %>% mutate(value=as.numeric(value)) %>% group_by(compound) %>% summarise(value=median(value),.groups="drop") %>%
  transmute(compound,profile="DPPC-liposome kq",value,label=paste0(round(value,2)," x10^9"))
profile <- bind_rows(profile_primary,profile_lipid)
p21 <- ggplot(profile,aes(value,fct_reorder(compound,value),color=profile))+geom_point(size=POINT_SIZE+1)+geom_text(aes(label=label),hjust=-.2,size=LABEL_SIZE-0.4)+
  facet_wrap(~profile,scales="free",ncol=2)+scale_color_manual(values=c(`Organic-solvent direct kq`="#D89000",`DPPC-liposome kq`="#2A9D8F"))+
  scale_x_continuous(expand=expansion(mult=c(.02,.24)))+theme_atlas+theme(legend.position="none")+
  labs(title="Carotenoid primary and lipid-phase profiles",subtitle="Facets have independent axes; membrane and organic-solvent values are not pooled",x=expression(paste(k[q]," (",10^9," ",M^{-1}," ",s^{-1},")")),y=NULL)
save_atlas(p21,"Carotenoid_Primary_vs_LipidPhase_Profile",13,7)

# Phase 3C Figure E: mixed constructs appear only as within-class percentiles.
global3 <- global_overview_v02 %>% group_by(analysis_panel) %>% arrange(within_class_rank,.by_group=TRUE) %>% slice_head(n=5) %>% ungroup() %>%
  mutate(compound=factor(compound,levels=rev(unique(compound[order(analysis_panel,within_class_rank)]))))
p22 <- ggplot(global3,aes(within_class_percentile,compound,color=confidence,shape=evidence_stability))+geom_point(size=POINT_SIZE+1)+
  facet_wrap(~analysis_panel,scales="free_y",ncol=1)+scale_color_manual(values=CONFIDENCE_COLORS,drop=FALSE)+
  scale_shape_manual(values=c(Stable=16,`Moderately stable`=17,Fragile=18),drop=FALSE)+scale_x_continuous(limits=c(0,100),breaks=seq(0,100,20))+theme_atlas+
  labs(title="Global Overview with carotenoids",subtitle="Within-class percentile only; H-ORAC-FL and singlet-oxygen kq are never placed on one raw scale",x="Within-class percentile",y=NULL,color="Confidence",shape="Evidence stability")
save_atlas(p22,"Global_Overview_With_Carotenoids",12,10)

# Phase 3D Figure A: singleton evidence summary, explicitly without a percentile claim.
vc_long <- tibble(record=c("Ou et al. 2001","Carvalho et al. 2023"),value=c(.95,.53))
p23 <- ggplot(vc_long,aes(value,record))+geom_segment(aes(x=0,xend=value,y=record,yend=record),color="#C9D5E3",linewidth=LINE_WIDTH)+
  geom_point(color=VITAMIN_C_COLOR,size=POINT_SIZE+1)+geom_vline(xintercept=vitamin_c$primary_value[1],linetype=2,color="#333333")+
  annotate("text",x=vitamin_c$primary_value[1],y=2.35,label=paste0("median = ",vitamin_c$primary_value[1]),size=LABEL_SIZE,hjust=-.1)+
  scale_x_continuous(limits=c(0,1.1),expand=expansion(mult=c(0,.08)))+theme_atlas+
  labs(title="Vitamin C aqueous primary construct",subtitle="Two historical H-ORAC-FL records; one eligible candidate, so percentile is not informative",x="H-ORAC-FL (mol TE/mol compound)",y=NULL)
save_atlas(p23,"VitaminC_Primary_Construct",10,5)

# Phase 3D Figure B: tied homologues retain the same primary k_inh value.
vit_e_plot <- vitamin_e %>% mutate(compound=fct_reorder(compound,primary_value),family=if_else(tocopherol_or_tocotrienol=="tocopherol","Tocopherol","Tocotrienol"))
p24 <- ggplot(vit_e_plot,aes(primary_value,compound,color=vitamer,shape=family))+geom_point(size=POINT_SIZE+1)+
  scale_color_manual(values=TOCOPHEROL_COLORS,drop=FALSE)+scale_shape_manual(values=c(Tocopherol=16,Tocotrienol=17))+
  scale_x_continuous(labels=function(x)x/1e6)+theme_atlas+
  labs(title="Vitamin E Top available: chain-breaking kinetics",subtitle="Corresponding tocopherol/tocotrienol homologues are tied; homogeneous organic-system k_inh",x=expression(paste(k[inh]," (",10^6," ",M^{-1}," ",s^{-1},")")),y=NULL,color="Vitamer",shape="Family")
save_atlas(p24,"VitaminE_TopN_Primary_Construct",11,7)

# Phase 3D Figure C: confidence is deliberately separate from magnitude.
p25 <- vitamin_e %>% mutate(compound=fct_reorder(compound,primary_value)) %>% ggplot(aes(confidence,compound,color=confidence))+
  geom_point(size=POINT_SIZE+1)+geom_text(aes(label=paste0("n=",eligible_record_count)),nudge_x=.15,size=LABEL_SIZE-0.3,color="#333333")+
  scale_color_manual(values=CONFIDENCE_COLORS,drop=FALSE)+theme_atlas+theme(legend.position="none")+
  labs(title="Vitamin E evidence confidence",subtitle="All current primary estimates remain single evidence chains and Fragile",x="Evidence confidence",y=NULL)
save_atlas(p25,"VitaminE_Evidence_Confidence",10,7)

# Phase 3D Figure D: coverage by environment/construct, not a pooled score.
ve_env <- tibble(environment=c("Homogeneous chain-breaking kinetics","L-ORAC (vitamer-resolved)","L-ORAC (generic mixture)","Liposome/membrane qualitative profile"),candidate_coverage=c(8,3,1,8),role=c("Primary","Secondary","Secondary / unresolved","Secondary"))
p26 <- ggplot(ve_env,aes(candidate_coverage,fct_reorder(environment,candidate_coverage),fill=role))+geom_col(width=.7)+geom_text(aes(label=candidate_coverage),hjust=-.25,size=LABEL_SIZE)+
  scale_fill_manual(values=c(Primary="#D89000",Secondary="#4C78A8",`Secondary / unresolved`="#A6A6A6"))+scale_x_continuous(limits=c(0,9),breaks=0:9)+theme_atlas+
  labs(title="Vitamin E assay-environment coverage",subtitle="Coverage count does not imply cross-environment comparability",x="Candidates or unresolved group reported",y=NULL,fill="Role")
save_atlas(p26,"VitaminE_Assay_Environment_Coverage",11,5.8)

# Phase 3D Figure E: independent facets prevent raw-value mixing inside the parent class.
vit_parent_plot <- vitamin_overview %>% mutate(value_num=as.numeric(primary_value),label=if_else(grepl("aqueous",vitamin_subpanel,fixed=TRUE),paste0(round(value_num,2)," mol TE/mol"),paste0(round(value_num/1e6,2)," x10^6")))
p27 <- ggplot(vit_parent_plot,aes(value_num,fct_reorder(compound,value_num),color=vitamin_subpanel))+geom_point(size=POINT_SIZE+1)+geom_text(aes(label=label),hjust=-.2,size=LABEL_SIZE-0.3)+
  facet_wrap(~vitamin_subpanel,scales="free",ncol=2)+scale_color_manual(values=c(`Vitamins–aqueous antioxidant`=VITAMIN_C_COLOR,`Vitamins–lipid-phase antioxidant`="#D89000"))+
  scale_x_continuous(expand=expansion(mult=c(.02,.28)))+theme_atlas+theme(legend.position="none")+
  labs(title="Vitamins parent-class overview",subtitle="Independent subpanel axes; no overall vitamin rank or parent-class percentile",x="Subpanel-specific primary value",y=NULL)
save_atlas(p27,"Vitamins_ParentClass_Overview",13,7.5)

# Phase 3D Figure F: shared view uses only informative within-subpanel percentiles.
global_vit <- global_overview_v03 %>% filter(!grepl("single eligible candidate",within_class_status,fixed=TRUE)) %>%
  mutate(analysis_subpanel=droplevels(factor(analysis_subpanel))) %>% group_by(analysis_subpanel) %>% arrange(within_class_rank,.by_group=TRUE) %>% slice_head(n=5) %>% ungroup() %>% mutate(compound=factor(compound,levels=rev(unique(compound[order(analysis_subpanel,within_class_rank)]))))
p28 <- ggplot(global_vit,aes(within_class_percentile,compound,color=confidence,shape=evidence_stability))+geom_point(size=POINT_SIZE+1)+
  facet_wrap(~analysis_subpanel,scales="free_y",ncol=1)+scale_color_manual(values=CONFIDENCE_COLORS,drop=FALSE)+scale_shape_manual(values=c(Stable=16,`Moderately stable`=17,Fragile=18),drop=FALSE)+
  scale_x_continuous(limits=c(0,100),breaks=seq(0,100,20))+theme_atlas+
  labs(title="Global Overview with vitamin subpanels",subtitle="Percentiles are computed only within mechanistically coherent subpanels; vitamin C singleton is omitted",x="Within-subpanel percentile",y=NULL,color="Confidence",shape="Stability")
save_atlas(p28,"Global_Overview_With_Vitamins",12,12)

# Supervisor overview: a presentation layer over frozen class/subpanel outputs.
# Raw H-ORAC, singlet-oxygen kq and peroxyl-radical k_inh values are never pooled.
supervisor_panel_labels <- c(
  "Polyphenols - Flavonoids"="Flavonoids",
  "Polyphenols - Phenolic acids / conjugates"="Phenolic acids / conjugates",
  "Carotenoids"="Carotenoids",
  "Vitamins–aqueous antioxidant"="Vitamin C (aqueous)",
  "Vitamins–lipid-phase antioxidant"="Vitamin E (lipid phase)"
)
supervisor_plot <- supervisor_overview %>%
  filter(within_class_rank<=SUPERVISOR_TOP_N | analysis_subpanel=="Vitamins–aqueous antioxidant") %>%
  mutate(panel=case_when(
           analysis_subpanel=="Polyphenols - Flavonoids" ~ "Flavonoids",
           analysis_subpanel=="Polyphenols - Phenolic acids / conjugates" ~ "Phenolic acids / conjugates",
           analysis_subpanel=="Carotenoids" ~ "Carotenoids",
           grepl("aqueous",analysis_subpanel,fixed=TRUE) ~ "Vitamin C (aqueous)",
           grepl("lipid-phase",analysis_subpanel,fixed=TRUE) ~ "Vitamin E (lipid phase)",
           TRUE ~ NA_character_),
         panel=factor(panel,levels=unname(supervisor_panel_labels)),
         compound=factor(compound,levels=rev(unique(compound[order(panel,within_class_rank)]))))
supervisor_points <- supervisor_plot %>% filter(!is.na(within_class_percentile))
supervisor_singleton <- supervisor_plot %>% filter(is.na(within_class_percentile)) %>% mutate(plot_x=50)
p29 <- ggplot(supervisor_plot,aes(y=compound))+
  geom_point(data=supervisor_points,aes(x=within_class_percentile,color=confidence,shape=evidence_stability),size=POINT_SIZE+0.8)+
  geom_text(data=supervisor_singleton,aes(x=plot_x,label="Single eligible candidate; percentile not informative"),
            size=SUPERVISOR_LABEL_SIZE,color="#555555",fontface="italic")+
  facet_wrap(~panel,scales="free_y",ncol=2)+
  scale_color_manual(values=CONFIDENCE_COLORS,drop=FALSE)+
  scale_shape_manual(values=c(Stable=16,`Moderately stable`=17,Fragile=18),drop=FALSE)+
  scale_x_continuous(limits=c(0,100),breaks=seq(0,100,20))+
  theme_atlas+theme(axis.text.y=element_text(size=BASE_SIZE-1),strip.text=element_text(size=BASE_SIZE+0.5,face="bold"))+
  labs(title="Current class-specific rankings of dietary antioxidant functional factors",
       subtitle="Each class uses a mechanism-appropriate primary construct; percentiles are within-class and not cross-class antioxidant magnitudes",
       x="Within-class / within-subpanel percentile",y=NULL,color="Confidence",shape="Stability")
save_atlas(p29,"Supervisor_Class_Specific_Ranking_Overview",SUPERVISOR_WIDTH,SUPERVISOR_HEIGHT)

message("Generated Phase 2 through Stage 22 Phase 3D figures in: ",outdir)
