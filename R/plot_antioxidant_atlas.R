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

SUBCLASS_COLORS <- c(
  "Flavan-3-ols"="#4C78A8", "Flavonols"="#F58518", "Flavonol glycosides"="#ECA82C",
  "Flavones"="#54A24B", "Flavone glycosides"="#8CD17D", "Flavanones"="#B279A2",
  "Flavanone glycosides"="#D4A6C8", "Anthocyanidins"="#E45756", "Anthocyanins"="#FF9DA6",
  "Isoflavones"="#79706E", "Isoflavone glycosides"="#BAB0AC"
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
outdir <- file.path(root,"figures"); dir.create(outdir,showWarnings=FALSE,recursive=TRUE)

candidates <- read_csv(candidate_path,show_col_types=FALSE)
taxonomy <- read_csv(taxonomy_path,show_col_types=FALSE)
exclusions <- read_csv(exclusion_path,show_col_types=FALSE)
top20 <- read_csv(top20_path,show_col_types=FALSE)
coverage <- read_csv(coverage_path,show_col_types=FALSE)

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

message("Generated Phase 2 universe and Phase 3A flavonoid figures in: ",outdir)
