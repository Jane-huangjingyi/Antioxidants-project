# Run from repository root. All 51 current scientific assets are rendered to figures/editable.
# This entry point does not overwrite frozen or legacy image bytes.
stopifnot(file.exists("R/common/bootstrap.R"))
if(.Platform$OS.type == "windows") Sys.setlocale("LC_CTYPE","English_United States.utf8")
options(encoding="UTF-8")
dir.create("workspaces/repository_review_20261030",showWarnings=FALSE,recursive=TRUE)
warnings_log <- data.frame(script=character(),warning=character())
set.seed(20261030)
run <- function(script){
 message("Rendering ",script)
 withCallingHandlers(source(script,local=new.env(parent=globalenv())),warning=function(w){
   warnings_log <<- rbind(warnings_log,data.frame(script=script,warning=conditionMessage(w)))
   invokeRestart("muffleWarning")
 })
}
run("R/render_all_active_figures.R")
run("R/supporting/render_supporting_figures.R")
run("R/stage25b5/editable_01_render_frozen_primary_top20.R")
run("R/stage25b5/editable_02_render_b2_sensitivity.R")
write.csv(unique(warnings_log),"workspaces/repository_review_20261030/R_Render_Warnings.csv",row.names=FALSE,fileEncoding="UTF-8")
writeLines(sub("[[:blank:]]+$","",capture.output(sessionInfo())),"workspaces/repository_review_20261030/R_Session_Info.txt")
message("Reproduction finished; warnings retained: ",nrow(warnings_log))
