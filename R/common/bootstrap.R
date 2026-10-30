project_library <- normalizePath(file.path("R","library"),mustWork=FALSE)
if(dir.exists(project_library)) .libPaths(c(project_library,.libPaths()))
required <- c("ggplot2","dplyr","tidyr","readr","stringr","forcats","scales","grid","svglite")
missing <- required[!vapply(required,requireNamespace,quietly=TRUE,FUN.VALUE=logical(1))]
if(length(missing)) stop("Missing R packages: ",paste(missing,collapse=", "))
suppressPackageStartupMessages({library(ggplot2);library(dplyr);library(tidyr);library(readr);library(stringr);library(forcats);library(scales);library(grid)})
source(file.path("R","common","plot_config.R"))
source(file.path("R","common","plot_helpers.R"))
source(file.path("R","common","data_helpers.R"))
