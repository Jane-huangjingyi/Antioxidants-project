# Run from project root after compare_models.py.
if (.Platform$OS.type == "windows") Sys.setlocale("LC_CTYPE", "English_United States.utf8")
lib <- "05_analysis/local_library"
if (dir.exists(lib)) .libPaths(c(normalizePath(lib),.libPaths()))
library(ggplot2)
stopifnot(requireNamespace("svglite",quietly=TRUE))
FONT <- "Arial"; BASE_SIZE <- 11; TITLE_SIZE <- 14
POINT_SIZE <- 2.4; LINE_WIDTH <- 0.7; DPI <- 320
COLORS <- c(OLS="#0072B2",Huber="#D55E00",baseline="#777777",sensitivity="#A5B5BF")
BACKGROUND <- "white"
if (.Platform$OS.type=="windows") windowsFonts(Arial=windowsFont("Arial"))
STYLE <- theme_minimal(base_family=FONT,base_size=BASE_SIZE)+theme(panel.grid.minor=element_blank(),plot.title=element_text(size=TITLE_SIZE,face="bold"),plot.caption=element_text(hjust=0),plot.margin=margin(12,15,12,12))
save_pair <- function(plot,name,width,height) {
 for (format in c("png","svg")) {
  folder <- file.path("06_manuscript","figures",name,"analysis_v0.1",format)
  dir.create(folder,recursive=TRUE,showWarnings=FALSE)
  path <- file.path(folder,paste0(name,".",format))
  if (format=="png") ggsave(path,plot,width=width,height=height,dpi=DPI,bg=BACKGROUND)
  else ggsave(path,plot,width=width,height=height,device=svglite::svglite,bg=BACKGROUND)
 }
}
input <- "03_candidate_selection/05_model_robustness/results"
d <- read.csv(file.path(input,"Heldout_Model_Comparison.csv"))
long <- do.call(rbind,lapply(c("baseline","OLS","Huber"),function(model) data.frame(observed=d$observed_log,predicted=d[[model]],model=model)))
p <- ggplot(long,aes(observed,predicted,color=model))+geom_abline(intercept=0,slope=1,color="#AAAAAA",linetype="dashed")+geom_point(size=POINT_SIZE,alpha=.8)+facet_wrap(~model,nrow=1)+scale_color_manual(values=COLORS)+STYLE+guides(color="none")+labs(title="Leave-paper-out model comparison",subtitle="35 matched observations; previously observed candidate identities",x="Observed log reference capacity",y="Held-out log-location prediction",caption="Exploratory cross-protocol references; new-paper effect assumed to equal the training mean.")
save_pair(p,"Evidence_Model_Heldout",11,4.5)
r <- read.csv(file.path(input,"Candidate_Model_Sensitivity.csv"))
profiles <- read.csv("02_identity_and_evidence/results/candidate_evidence_profiles.csv")
r$compound <- profiles$compound_name[match(r$candidate_id,profiles$candidate_id)]
stopifnot(nrow(r)==34,!anyNA(r$compound))
r <- r[order(r$OLS_component_order,r$candidate_id),]
first <- read.csv("03_candidate_selection/04_first_evidence_model/results/Candidate_Diagnostic_Estimates.csv")
r$source_count <- first$source_DOI_count[match(r$candidate_id,first$candidate_id)]
r$compound <- paste0(r$compound," (",r$source_count," sources)")
r$compound <- factor(r$compound,levels=rev(r$compound))
p <- ggplot(r,aes(y=compound))+geom_segment(aes(x=paper_weight_order_q025,xend=paper_weight_order_q975,yend=compound),color=COLORS[["sensitivity"]],linewidth=LINE_WIDTH)+geom_point(aes(x=OLS_component_order,color="OLS"),size=POINT_SIZE)+geom_point(aes(x=Huber_component_order,color="Huber"),shape=17,size=POINT_SIZE)+scale_color_manual(values=COLORS[c("OLS","Huber")])+scale_x_continuous(breaks=c(1,5,10,15,20,25,30,34))+STYLE+theme(legend.position="bottom")+labs(title="Candidate order and source-weight sensitivity",subtitle="34 candidates in one connected component; additive log-capacity models",x="Within-component diagnostic position",y=NULL,color="Model",caption="Segments show 2.5%-97.5% paper-weight perturbation quantiles over 300 fits.\nAll sources remain present in each weighted fit. Sampling confidence coverage is unestimated.")
save_pair(p,"Evidence_Model_Order_Sensitivity",10,10.5)
cat("Rendered two evidence-model PNG/SVG pairs.\n")
