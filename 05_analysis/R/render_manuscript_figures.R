# Run from the project root. Every style and geometry is editable here.
if(.Platform$OS.type=="windows") Sys.setlocale("LC_CTYPE","English_United States.utf8")
options(encoding="UTF-8")
lib <- file.path("90_archive","legacy_2026-11-05","R","library")
if(dir.exists(lib)) .libPaths(c(normalizePath(lib),.libPaths()))
required <- c("ggplot2","svglite")
if(any(!vapply(required,requireNamespace,quietly=TRUE,FUN.VALUE=logical(1)))) stop("Install ggplot2 and svglite from CRAN before rendering")
library(ggplot2)
FONT <- "Arial"; BASE_SIZE <- 11; TITLE_SIZE <- 15; POINT_SIZE <- 3.3
PNG_DPI <- 320; BACKGROUND <- "white"; GRID_COLOR <- "#E5E7EB"
if(.Platform$OS.type=="windows") windowsFonts(Arial=windowsFont("Arial"))
COLORS <- c(Discovery="#496D89",Identity="#3C8D8A",Evidence="#668B42",Review="#A46B32",Ready="#76658C")
theme_project <- theme_minimal(base_family=FONT,base_size=BASE_SIZE)+theme(plot.title=element_text(size=TITLE_SIZE,face="bold"),panel.grid.minor=element_blank(),panel.grid.major=element_line(color=GRID_COLOR),legend.position="bottom",plot.margin=margin(12,20,12,12))
save_pair <- function(p,name,width,height){
 for(format in c("png","svg")){
  out <- file.path("06_manuscript","figures",name,"analysis_v0.1",format)
  dir.create(out,recursive=TRUE,showWarnings=FALSE)
  if(format=="png")ggsave(file.path(out,paste0(name,".png")),p,width=width,height=height,dpi=PNG_DPI,bg=BACKGROUND)
  else ggsave(file.path(out,paste0(name,".svg")),p,width=width,height=height,device=svglite::svglite,bg=BACKGROUND)
 }
}
d <- read.csv("06_manuscript/tables/Table_1_Discovery_and_Selection_Flow.csv",check.names=FALSE)
selected <- d[c(1,2,3,5,7,8,9,10),];selected$stage<-factor(selected$stage,levels=rev(selected$stage))
selected$role<-factor(c("Discovery","Identity","Identity","Identity","Evidence","Review","Evidence","Ready"),levels=names(COLORS))
p1<-ggplot(selected,aes(count,stage,fill=role))+geom_col(width=.65)+geom_text(aes(label=count),hjust=-.15,size=3.6)+scale_fill_manual(values=COLORS)+scale_x_continuous(expand=expansion(mult=c(0,.13)))+theme_project+labs(title="Food-chemical discovery and screening preparation",subtitle="Source-bounded register; counts are stage-specific, not independent study totals",x="Records or candidate profiles",y=NULL,fill="Stage")
save_pair(p1,"Figure_1_Discovery_Flow",12,7)
q<-read.csv("03_candidate_selection/results/top20_review_queue.csv",check.names=FALSE,na.strings=c("","NA"));q$compound_name<-factor(q$compound_name,levels=rev(q$compound_name))
q$support<-ifelse(q$confirmed_independent_horac_studies>=2,"At least two checked studies","One checked study")
p2<-ggplot(q,aes(confirmed_independent_horac_studies,compound_name,color=support))+geom_point(size=POINT_SIZE)+scale_color_manual(values=c("At least two checked studies"="#3C8D8A","One checked study"="#A46B32"))+scale_x_continuous(breaks=0:3,limits=c(.5,2.5))+theme_project+labs(title="Twenty provisional review slots",subtitle="Checked chemical-study support; no efficacy or new-assay ranking",x="Candidate-specific confirmed studies",y=NULL,color=NULL)
save_pair(p2,"Figure_2_Review_Panel_Evidence",12,9)
sc<-read.csv("03_candidate_selection/results/selection_sensitivity.csv",check.names=FALSE)
sc$label<-factor(c("One-study review pool","Two-study sensitivity","Lab-ready gates"),levels=rev(c("One-study review pool","Two-study sensitivity","Lab-ready gates")))
p3<-ggplot(sc,aes(eligible_count,label))+geom_col(width=.6,fill="#496D89")+geom_text(aes(label=eligible_count),hjust=-.2,size=4)+scale_x_continuous(expand=expansion(mult=c(0,.15)))+theme_project+labs(title="Selection sensitivity and remaining readiness gap",subtitle="Unknown food-source, reagent and interference fields are not approvals",x="Eligible candidate profiles",y=NULL)
save_pair(p3,"Figure_3_Selection_Sensitivity",11,5)
dir.create("07_quality_control",showWarnings=FALSE)
writeLines(sub("[[:blank:]]+$","",capture.output(sessionInfo())),"07_quality_control/R_session_info.txt")
message("Rendered three manuscript figures in PNG and editable text/vector SVG.")
