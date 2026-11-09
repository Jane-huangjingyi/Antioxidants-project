# Run from the project root after simulate_endpoint.py. All styles are editable.
if (.Platform$OS.type == "windows") Sys.setlocale("LC_CTYPE", "English_United States.utf8")
lib <- file.path("05_analysis", "local_library")
if (dir.exists(lib)) .libPaths(c(normalizePath(lib), .libPaths()))
stopifnot(requireNamespace("ggplot2", quietly=TRUE), requireNamespace("svglite", quietly=TRUE))
library(ggplot2)
FONT <- "Arial"
BASE_SIZE <- 11
TITLE_SIZE <- 15
LINE_WIDTH <- 0.8
POINT_SIZE <- 2.4
WIDTH_IN <- 11.5
HEIGHT_IN <- 6.0
PNG_DPI <- 320
BACKGROUND <- "white"
GRID_COLOR <- "#E5E7EB"
COLORS <- c(REFERENCE="#747474", EQUAL_SLOW="#0072B2", EQUAL_FAST="#D55E00",
            HIGH_SLOW="#009E73", LOW_FAST="#CC79A7")
LINE_TYPES <- c(REFERENCE="dashed", EQUAL_SLOW="solid", EQUAL_FAST="solid",
                HIGH_SLOW="dotdash", LOW_FAST="dotted")
TITLE <- "Capacity and kinetics affect the AUC slope ratio"
SUBTITLE <- "Dimensionless simulation only; no compound measurements or fitted assay model"
CAPTION <- paste("Capacity and capture-rate values are assumed toy parameters, not measured properties.",
                 "Ratios are not molar TE. No candidate order or experimental setting is inferred.", sep="\n")
if (.Platform$OS.type == "windows") windowsFonts(Arial=windowsFont("Arial"))

data <- read.csv("04_absorbance_assay/04_endpoint_stress_test/results/Synthetic_Endpoint_Sensitivity.csv",
                 check.names=FALSE)
stopifnot(all(data$simulation_only == "YES"), nrow(data)==45)
order <- names(COLORS)
labels <- vapply(order, function(id) unique(data$label[data$scenario==id]), character(1))
data$scenario <- factor(data$scenario, levels=order)
data$start_panel <- factor(paste("First read:", data$read_start),
                           levels=paste("First read:", sort(unique(data$read_start))))
plot <- ggplot(data, aes(window_end, diagnostic_slope_ratio, color=scenario,
                         linetype=scenario, group=scenario)) +
  geom_line(linewidth=LINE_WIDTH) + geom_point(size=POINT_SIZE) +
  facet_wrap(~start_panel, nrow=1) +
  scale_color_manual(values=COLORS, labels=labels) +
  scale_linetype_manual(values=LINE_TYPES, labels=labels) +
  scale_x_continuous(breaks=c(2,4,8)) +
  theme_minimal(base_family=FONT, base_size=BASE_SIZE) +
  theme(plot.title=element_text(size=TITLE_SIZE, face="bold"),
        panel.grid.minor=element_blank(), panel.grid.major=element_line(color=GRID_COLOR),
        legend.position="bottom", plot.margin=margin(12,15,12,12),
        plot.caption=element_text(hjust=0)) +
  guides(color=guide_legend(nrow=2, byrow=TRUE), linetype=guide_legend(nrow=2, byrow=TRUE)) +
  labs(title=TITLE, subtitle=SUBTITLE, caption=CAPTION,
       x="Integration end (arbitrary time units)", y="Diagnostic AUC slope ratio to synthetic reference",
       color=NULL, linetype=NULL)

name <- "Capacity_Kinetics_Toy_Diagnostic"
base <- file.path("06_manuscript", "figures", name, "simulation_v0.1")
for (format in c("png","svg")) {
  folder <- file.path(base,format)
  dir.create(folder,recursive=TRUE,showWarnings=FALSE)
  output <- file.path(folder,paste0(name,".",format))
  if (format=="png") ggsave(output,plot,width=WIDTH_IN,height=HEIGHT_IN,dpi=PNG_DPI,bg=BACKGROUND)
  else ggsave(output,plot,width=WIDTH_IN,height=HEIGHT_IN,device=svglite::svglite,bg=BACKGROUND)
}
cat("Rendered one simulation-only PNG/SVG pair with editable text/vector elements.\n")
