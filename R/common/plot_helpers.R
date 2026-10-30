project_root <- function(){
  root <- normalizePath(".",mustWork=TRUE)
  if(!file.exists(file.path(root,"Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md"))) stop("Run from project root")
  root
}
ensure_parent <- function(path){dir.create(dirname(path),recursive=TRUE,showWarnings=FALSE);path}
save_figure <- function(plot,path,width,height,dpi=FIG_DPI){
  # Colour bars are vector rectangles too, rather than embedded raster legends.
  for(aesthetic in c("fill","colour")) {
    sc <- plot$scales$get_scales(aesthetic)
    if(!is.null(sc) && inherits(sc,"ScaleContinuous"))
      plot <- plot + do.call(ggplot2::guides,stats::setNames(list(ggplot2::guide_colourbar(display="rectangles")),aesthetic))
  }
  # Keep all published/frozen legacy assets intact. New editable renders mirror figures/.
  rel <- sub("^.*?/figures/", "", gsub("\\\\", "/", path))
  target <- file.path(project_root(), FIGURE_OUTPUT_ROOT, rel)
  target <- sub("\\.[^.]+$", "", target)
  ggplot2::ggsave(ensure_parent(paste0(target,".png")),plot,width=width,height=height,dpi=dpi,bg=FIG_BACKGROUND)
  ggplot2::ggsave(ensure_parent(paste0(target,".svg")),plot,width=width,height=height,device=svglite::svglite,bg=FIG_BACKGROUND)
}
