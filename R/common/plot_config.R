# Shared aesthetics only. Scientific filtering and transformations stay in each figure script.
FIG_DPI <- 320
FIGURE_OUTPUT_ROOT <- "figures/editable"
FIG_BACKGROUND <- "white"
BASE_FONT_FAMILY <- "Arial"
if(.Platform$OS.type == "windows") grDevices::windowsFonts(Arial=grDevices::windowsFont("Arial"))
DISCRETE_COLORS <- c("#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756", "#72B7B2", "#ECA82C", "#79706E", "#FF9DA6", "#9D755D", "#5F9ED1", "#A0CBE8")
# All unassigned categorical colours have one editable, deterministic fallback.
options(ggplot2.discrete.colour=function(...) ggplot2::scale_colour_manual(...,values=grDevices::colorRampPalette(DISCRETE_COLORS)(60)),
        ggplot2.discrete.fill=function(...) ggplot2::scale_fill_manual(...,values=grDevices::colorRampPalette(DISCRETE_COLORS)(60)))
BASE_FONT_SIZE <- 11
TITLE_SIZE <- 15
AXIS_TITLE_SIZE <- 11
AXIS_TEXT_SIZE <- 10
LEGEND_TEXT_SIZE <- 9
POINT_SIZE <- 3.2
LABEL_SIZE <- 3.1
BAR_WIDTH <- 0.72
SHOW_LABELS <- TRUE
CLASS_COLORS <- c(
  "Polyphenols - Flavonoids"="#12A88A",
  "Polyphenols - Phenolic acids / conjugates"="#17A9D4",
  "Polyphenols - Stilbenes / lignans"="#8B78E6",
  "Vitamins / vitamin-like"="#EF56BF",
  "Organosulfur compounds"="#C89A00",
  "Betalains / nitrogen-containing"="#F27D77",
  "Other food-derived redox-active phytochemicals"="#49A800")
CONFIDENCE_COLORS <- c("Low"="#D98C3F","Moderate"="#4C78A8","High"="#3A8D5D","Very low"="#A6A6A6")
theme_atlas <- ggplot2::theme_minimal(base_family=BASE_FONT_FAMILY,base_size=BASE_FONT_SIZE)+ggplot2::theme(
  plot.title=ggplot2::element_text(size=TITLE_SIZE,face="bold"),
  plot.subtitle=ggplot2::element_text(color="#555555"),panel.grid.minor=ggplot2::element_blank(),
  legend.position="bottom",axis.title=ggplot2::element_text(size=AXIS_TITLE_SIZE),
  axis.text=ggplot2::element_text(size=AXIS_TEXT_SIZE),legend.text=ggplot2::element_text(size=LEGEND_TEXT_SIZE))
