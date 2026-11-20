# Run from the repository root; numerical inputs come from build_results1.py.
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "06_manuscript/Results1_v1.0"
local_lib <- "05_analysis/local_library"
if (dir.exists(local_lib)) .libPaths(c(normalizePath(local_lib), .libPaths()))
data <- read.csv(file.path(out, "Figure1_Data.csv"))
FONT <- "sans"
SIZE <- c(11, 8)
DPI <- 300
PALETTE <- c(blue = "#165A7C", muted = "#ACB9C2", green = "#236B58",
             amber = "#BB7723", grey = "#74808B", ink = "#142836")
plot_bars <- function(code, title, ylab, colors, ylim_factor = 1.23, digits = 0) {
  part <- data[data$panel == code, ]
  par(mar = c(if (code == "C") 7 else 5, 4.7, 3.7, 1))
  positions <- barplot(part$value, names.arg = part$label, las = if (code %in% c("B", "C")) 2 else 1,
      col = colors, border = NA, cex.names = 0.72, ylim = c(0, max(part$value) * ylim_factor),
      ylab = ylab, cex.lab = 0.92, cex.axis = 0.8, axes = TRUE)
  text(positions, part$value, sprintf(paste0("%.", digits, "f"), part$value),
      pos = 3, cex = 0.78, col = PALETTE[["ink"]], xpd = TRUE)
  title(main = paste0(code, "  ", title), adj = 0, cex.main = 1, col.main = PALETTE[["ink"]])
}
draw <- function() {
  par(mfrow = c(2, 2), family = FONT, col.axis = PALETTE[["ink"]], col.lab = PALETTE[["ink"]])
  plot_bars("A", "Discovery and chemical identity", "Records or compounds", PALETTE[c("blue","blue","green")])
  plot_bars("B", "Assay-specific comparison", "Ranked observations", PALETTE[["blue"]])
  par(mar = c(5, 4.7, 3.7, 1))
  errors <- matrix(data$value[data$panel == "C"], nrow = 2)
  positions <- barplot(errors, beside = TRUE, names.arg = c("Expanded DOI", "Core DOI", "Scaffold Ridge"),
      ylim = c(0, 1.17), col = PALETTE[c("blue","muted")], border = NA,
      ylab = "Held-out log-scale RMSE", cex.names = 0.76)
  text(positions, errors, sprintf("%.3f", errors), pos = 3, cex = 0.68)
  legend("topleft", legend = c("Model", "Matched baseline"), fill = PALETTE[c("blue","muted")],
      bty = "n", cex = 0.75)
  title(main = "C  Model and matched baseline", adj = 0, cex.main = 1, col.main = PALETTE[["ink"]])
  plot_bars("D", "Proposed experiment priorities", "Compounds", PALETTE[c("green","amber","grey")])
}
svglite::svglite(file.path(out, "Figure1.svg"), width = SIZE[1], height = SIZE[2])
draw()
invisible(dev.off())
png(file.path(out, "Figure1.png"), width = SIZE[1], height = SIZE[2], units = "in", res = DPI,
    type = if (capabilities("cairo")) "cairo" else getOption("bitmapType"))
draw()
invisible(dev.off())
