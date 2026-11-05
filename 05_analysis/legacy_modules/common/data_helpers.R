# Supplementary historical construct; not the current review-panel result.
read_project_csv <- function(...){readr::read_csv(file.path(project_root(),"90_archive","legacy_2026-11-05",...),show_col_types=FALSE)}
