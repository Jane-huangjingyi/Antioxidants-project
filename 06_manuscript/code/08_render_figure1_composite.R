# figure1_composite - detailed A (flow) + B (evidence screening and ranking), stacked.
# C (pathway framework) is deferred until expansion fills enough cells; this composite
# reserves a tall layout so C can be appended later. Vector-only (base/grid grobs).
# Run from repo root: Rscript 06_manuscript/code/08_render_figure1_composite.R
here <- normalizePath("06_manuscript/code", mustWork = TRUE)
root <- dirname(dirname(here))
.libPaths(c(file.path(root, "04_05_experimental_validation", "local_library"), .libPaths()))
FIG1_COMPOSITE_BUILD <- TRUE
source(file.path(root, "06_manuscript/code/04_render_figure1.R"))
source(file.path(root, "06_manuscript/code/06_render_screening_workflow.R"))
suppressPackageStartupMessages({ library(grid); library(gridExtra); library(svglite); library(ggplot2); library(patchwork) })

gA <- grid.grabExpr(draw())     # detailed screening workflow (grid viewports)
gB <- ggplotGrob(build_B())     # ggplot evidence + rank panels (reliable grob)

W <- 10
H <- 21.3
comp <- arrangeGrob(gA, gB, ncol = 1, heights = unit(c(14.7, 6.3), "in"),
                    top = textGrob("Figure 1. Evidence screening, conditional ranking and candidate priorities",
                                   gp = gpar(fontface = "bold", fontsize = 13, fontfamily = "sans")),
                    bottom = textGrob("Provisional working figure; pathway framework (figure1_C) appended after evidence expansion. All mechanism observations NOT_REVIEWED.",
                                      gp = gpar(fontsize = 8, col = "grey30", fontfamily = "sans")))
out <- file.path(root, "06_manuscript/result/figure/figure1_composite")
png(paste0(out, ".png"), width = W, height = H, units = "in", res = 300, bg = "white")
grid.draw(comp); invisible(dev.off())
svglite::svglite(paste0(out, ".svg"), width = W, height = H, bg = "white")
grid.draw(comp); invisible(dev.off())
cat("saved figure1_composite\n")
