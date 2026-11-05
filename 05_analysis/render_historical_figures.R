# Optional supplementary exports from the preserved evidence constructs.
if(.Platform$OS.type=="windows") Sys.setlocale("LC_CTYPE","English_United States.utf8")
options(encoding="UTF-8");set.seed(20261030)
warnings_log<-character()
for(script in c("05_analysis/legacy_modules/render_all_active_figures.R","05_analysis/legacy_modules/supporting/render_supporting_figures.R","05_analysis/legacy_modules/stage25b5/editable_01_render_frozen_primary_top20.R","05_analysis/legacy_modules/stage25b5/editable_02_render_b2_sensitivity.R")){
 withCallingHandlers(source(script,local=new.env(parent=globalenv()),encoding="UTF-8"),warning=function(w){warnings_log<<-c(warnings_log,paste(script,conditionMessage(w)));invokeRestart("muffleWarning")})
}
writeLines(warnings_log,"07_quality_control/supplementary_render_warnings.txt")
message("Supplementary exports complete; warnings: ",length(warnings_log))
