project_root <- function(){
  root <- normalizePath(".",mustWork=TRUE)
  if(!file.exists(file.path(root,"Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md"))) stop("Run from project root")
  root
}
ensure_parent <- function(path){dir.create(dirname(path),recursive=TRUE,showWarnings=FALSE);path}
save_figure <- function(plot,path,width,height,dpi=FIG_DPI){ggplot2::ggsave(ensure_parent(path),plot,width=width,height=height,dpi=dpi,bg="white")}
