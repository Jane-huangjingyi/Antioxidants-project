# Run from project root after fit_verified_source_diagnostics.py.
# Edit the settings below to change every figure's typography, colors and dimensions.
if (.Platform$OS.type == "windows") Sys.setlocale("LC_CTYPE", "English_United States.utf8")
local_library <- "05_analysis/local_library"
if (dir.exists(local_library)) .libPaths(c(normalizePath(local_library), .libPaths()))
library(ggplot2)
stopifnot(requireNamespace("svglite", quietly = TRUE))

FONT <- "Arial"
if (.Platform$OS.type == "windows") windowsFonts(Arial = windowsFont("Arial"))
BASE_SIZE <- 11
TITLE_SIZE <- 15
POINT_SIZE <- 2.3
LINE_WIDTH <- 0.65
DPI <- 320
BACKGROUND <- "white"
GRID_COLOR <- "#E4E8EB"
BOUND_COLOR <- "#B9C2CA"
SOURCE_LOW_COLOR <- "#7D929E"
SOURCE_HIGH_COLOR <- "#007E87"
SOURCE_COLORS <- c(
  "2022" = "#8C564B",
  "2015" = "#E69F00", "2024" = "#56B4E9",
  "2009" = "#A6761D", "2001" = "#0072B2", "2004" = "#D55E00", "2013" = "#009E73",
  "2020" = "#CC79A7", "2023" = "#6A51A3"
)
HELDOUT_WIDTH <- 12
HELDOUT_HEIGHT <- 7.5
ORDER_WIDTH <- 10
ORDER_HEIGHT <- 12.5

STYLE <- theme_minimal(base_family = FONT, base_size = BASE_SIZE) +
  theme(
    panel.grid.minor = element_blank(), panel.grid.major = element_line(color = GRID_COLOR),
    plot.title = element_text(size = TITLE_SIZE, face = "bold"),
    plot.caption = element_text(hjust = 0), plot.margin = margin(12, 16, 12, 12),
    legend.position = "bottom"
  )

save_pair <- function(plot, name, width, height) {
  for (format in c("png", "svg")) {
    folder <- file.path("06_manuscript", "figures", name, "analysis_v0.1", format)
    dir.create(folder, recursive = TRUE, showWarnings = FALSE)
    filename <- file.path(folder, paste0(name, ".", format))
    if (format == "png") {
      ggsave(filename, plot, width = width, height = height, dpi = DPI, bg = BACKGROUND)
    } else {
      ggsave(filename, plot, width = width, height = height, device = svglite::svglite, bg = BACKGROUND)
    }
  }
}

arguments <- commandArgs(trailingOnly = TRUE)
input <- if (length(arguments) >= 1) arguments[1] else "03_candidate_selection/06_verified_source_update/results"
figure_prefix <- if (length(arguments) >= 2) arguments[2] else "Verified_Source"
predictions <- read.csv(file.path(input, "Leave_DOI_Out_Predictions.csv"))
predictions <- predictions[!is.na(predictions$predicted_log_location), ]
variant_labels <- c(
  CORE_REPORTED_PH74_37C = "Reported pH 7.4 / 37 C",
  EXTENDED_UNKNOWN_PH_NAME_BASED = "Extended names",
  EXTENDED_CONFLICT_EXCLUDED = "Recorded conflicts excluded"
)
predictions$variant_label <- factor(variant_labels[predictions$variant], levels = unname(variant_labels))
study_year <- c(
  "10.3390/antiox11091784" = "2022", "10.3390/foods11193131" = "2022",
  "10.3762/bjoc.11.151" = "2015", "10.3390/molecules29102370" = "2024",
  "10.1016/j.foodchem.2008.08.013" = "2009",
  "10.1021/jf010586o" = "2001", "10.1021/jf0305231" = "2004",
  "10.1021/jp307746c" = "2013", "10.1155/2020/4150897" = "2020",
  "10.3390/antiox12020505" = "2023"
)
predictions$study_year <- factor(study_year[predictions$heldout_doi], levels = names(SOURCE_COLORS))
long <- rbind(
  transform(predictions, model = "Source-summary baseline", predicted = baseline_log_location),
  transform(predictions, model = "Source-block model, lambda = 10", predicted = predicted_log_location)
)
plot <- ggplot(long, aes(observed_log_mean, predicted, color = study_year)) +
  geom_abline(slope = 1, intercept = 0, color = "#9DA6AD", linetype = "dashed", linewidth = LINE_WIDTH) +
  geom_point(size = POINT_SIZE, alpha = 0.85) +
  facet_grid(model ~ variant_label) + scale_color_manual(values = SOURCE_COLORS, drop = FALSE) +
  STYLE + labs(
    title = "Original-source prediction checks",
    subtitle = "Whole-paper holdout with matched estimable candidate identities",
    x = "Log reported molar capacity", y = "Training-centered log-location prediction", color = "Source year",
    caption = "Protocol and material alignment remain unresolved. Each panel uses its recorded analysis set.\nRepeated comparisons within papers share source dependence."
  )
save_pair(plot, paste0(figure_prefix, "_Heldout"), HELDOUT_WIDTH, HELDOUT_HEIGHT)

orders <- read.csv(file.path(input, "Diagnostic_Orders_and_Coverage.csv"))
orders <- orders[orders$variant == "EXTENDED_CONFLICT_EXCLUDED", ]
deletions <- read.csv(file.path(input, "Source_Deletion_Order_Sensitivity.csv"))
deletions <- deletions[deletions$variant == "EXTENDED_CONFLICT_EXCLUDED", ]
bounds <- aggregate(
  cbind(fixed_universe_best_possible_order, fixed_universe_worst_possible_order) ~ candidate_id,
  data = deletions,
  FUN = function(values) c(min = min(values), max = max(values))
)
orders$best <- bounds$fixed_universe_best_possible_order[match(orders$candidate_id, bounds$candidate_id), "min"]
orders$worst <- bounds$fixed_universe_worst_possible_order[match(orders$candidate_id, bounds$candidate_id), "max"]
orders$best <- pmin(orders$best, orders$diagnostic_component_order)
orders$worst <- pmax(orders$worst, orders$diagnostic_component_order)
orders <- orders[order(orders$diagnostic_component_order), ]
orders$label <- factor(orders$compound, levels = rev(orders$compound))
plot <- ggplot(orders, aes(y = label)) +
  geom_segment(aes(x = best, xend = worst, yend = label), color = BOUND_COLOR, linewidth = LINE_WIDTH) +
  geom_point(aes(x = diagnostic_component_order, color = source_DOIs), size = POINT_SIZE) +
  scale_color_gradient(low = SOURCE_LOW_COLOR, high = SOURCE_HIGH_COLOR, breaks = seq_len(max(orders$source_DOIs)),
                       guide = guide_colorbar(display = "rectangles")) +
  scale_x_continuous(breaks = c(1, 5, 10, 15, 20, 25, 30, 35, nrow(orders))) +
  STYLE + labs(
    title = "Source deletion and candidate order",
    subtitle = paste(nrow(orders), "candidates with recorded source conflicts excluded"),
    x = "Within-set diagnostic position", y = NULL, color = "Source DOIs",
    caption = "Points show the full fit. Segments enclose positions permitted by estimable contrasts across paper deletions.\nBounds describe model sensitivity and identification. Sampling coverage is unestimated."
  )
save_pair(plot, paste0(figure_prefix, "_Order_Sensitivity"), ORDER_WIDTH, ORDER_HEIGHT)
cat("Rendered original-source heldout and source-deletion PNG/SVG pairs.\n")
