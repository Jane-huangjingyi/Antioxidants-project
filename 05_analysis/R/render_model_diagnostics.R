# Run from project root; all visual choices remain editable.
if (.Platform$OS.type == "windows") Sys.setlocale("LC_CTYPE", "English_United States.utf8")
options(encoding = "UTF-8")
lib <- file.path("05_analysis", "local_library")
if (dir.exists(lib)) .libPaths(c(normalizePath(lib), .libPaths()))
stopifnot(requireNamespace("ggplot2", quietly=TRUE), requireNamespace("svglite", quietly=TRUE))
library(ggplot2)
FONT <- "Arial"; BASE_SIZE <- 11; TITLE_SIZE <- 14
POINT_SIZE <- 3; LINE_WIDTH <- 0.8; PNG_DPI <- 320
COLORS <- c(Selected="#246B93", Baseline="#7A7A7A", Position="#90663A")
BACKGROUND <- "white"; GRID_COLOR <- "#E5E7EB"
if (.Platform$OS.type == "windows") windowsFonts(Arial=windowsFont("Arial"))
theme_model <- theme_minimal(base_family=FONT, base_size=BASE_SIZE) +
  theme(plot.title=element_text(size=TITLE_SIZE, face="bold"), panel.grid.minor=element_blank(),
        panel.grid.major=element_line(color=GRID_COLOR), plot.margin=margin(12,18,12,12))
save_pair <- function(plot, name, width, height) {
  for (format in c("png", "svg")) {
    folder <- file.path("06_manuscript", "figures", name, "analysis_v0.1", format)
    dir.create(folder, recursive=TRUE, showWarnings=FALSE)
    path <- file.path(folder, paste0(name, ".", format))
    if (format == "png") ggsave(path, plot, width=width, height=height, dpi=PNG_DPI, bg=BACKGROUND)
    else ggsave(path, plot, width=width, height=height, device=svglite::svglite, bg=BACKGROUND)
  }
}
input <- file.path("03_candidate_selection", "01_activity_model", "results")
d <- read.csv(file.path(input,"Completed_Model_Heldout_Predictions.csv"), check.names=FALSE)
p <- ggplot(d,aes(observed_ln_ORAC,nested_selected_prediction)) +
  geom_abline(intercept=0,slope=1,color=COLORS[["Baseline"]],linetype="dashed",linewidth=LINE_WIDTH) +
  geom_point(color=COLORS[["Selected"]],size=POINT_SIZE,alpha=0.85) + theme_model +
  labs(title="Nested scaffold-held-out predictions",subtitle="36 labels from one study; exploratory model development",
       x="Source-reported ln(ORAC)",y="Held-out prediction of log location")
save_pair(p,"Model_Heldout_Predictions",6.8,5.4)
f <- read.csv(file.path(input,"Completed_Model_Fold_Metrics.csv"),check.names=FALSE)
f$group <- paste0("G",seq_len(nrow(f))," (n=",f$test_n,")")
long <- rbind(data.frame(group=f$group,model="Selected",MAE=f$selected_MAE),
              data.frame(group=f$group,model="Baseline",MAE=f$null_MAE))
long$group <- factor(long$group,levels=f$group)
p <- ggplot(long,aes(group,MAE,color=model,group=model)) +
  geom_line(linewidth=LINE_WIDTH) + geom_point(size=POINT_SIZE) +
  scale_color_manual(values=COLORS[c("Selected","Baseline")]) + theme_model +
  labs(title="Performance differs across scaffold groups",subtitle="Selected pipeline versus matched training-mean baseline",
       x="Scaffold group and held-out size",y="Mean absolute error on log scale",color="Model")
save_pair(p,"Model_Scaffold_Errors",7.5,5.2)
r <- read.csv(file.path(input,"Mapped_Candidate_Model_Diagnostics.csv"),check.names=FALSE)
r$compound <- factor(r$compound,levels=rev(r$compound))
p <- ggplot(r,aes(y=compound)) +
  geom_segment(aes(x=refit_position_min,xend=refit_position_max,yend=compound),color=COLORS[["Baseline"]],linewidth=LINE_WIDTH) +
  geom_point(aes(x=diagnostic_position_within_16),color=COLORS[["Position"]],size=POINT_SIZE) +
  scale_x_continuous(breaks=c(1,4,8,12,16),limits=c(1,16)) + theme_model +
  labs(title="Model order is sensitive to scaffold-group omission",
       subtitle="16 mapped candidates only; ranges from five refits are not confidence intervals",
       x="Diagnostic position (lower means higher fitted log location)",y=NULL,
       caption="Points: full-development fit. Segments: refit ranges. No global Top20 is inferred.")
save_pair(p,"Model_Order_Stability",9.4,7.0)
cat("Rendered three PNG/SVG pairs with editable text and vectors.\n")
