# Editable black-text Figure 1. Run from the repository root.
local_lib <- "04_05_experimental_validation/local_library"
if (dir.exists(local_lib)) .libPaths(c(normalizePath(local_lib), .libPaths()))
suppressPackageStartupMessages({ library(ggplot2); library(patchwork); library(svglite) })
FONT <- "sans"
BLUE <- "#176382"
GREEN <- "#267457"
GRAY <- "#52606A"
PALE <- "#E9F2F6"
WIDTH <- 9.2
HEIGHT <- 7.8
DPI <- 300
ranks <- read.csv("03_candidate_selection/result/table/04_figure1_candidate_ranks.csv")
screen <- jsonlite::read_json("02_identity_and_evidence/result/table/audit/Screening_QC.json")
queue <- jsonlite::read_json("02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json")
fit <- jsonlite::read_json("03_candidate_selection/result/model/02_whole_doi_validation.json")$models$plus_2021_conditionally
keep <- ranks$validation_review_status == "RETAIN_STABLE_WITHIN_10"
show <- keep | ranks$candidate_id %in% c("AFF-0084", "AFF-0006")
d <- ranks[show, ]
d <- d[order(d$conditional_rank), ]
y <- rev(seq_len(nrow(d)))
fmt <- function(x) format(x, big.mark = ",", scientific = FALSE, trim = TRUE)
plot_panel <- function(xlim, ylim) {
  plot.new()
  plot.window(xlim, ylim, xaxs = "i", yaxs = "i")
}
panel_a <- function() {
  par(family = FONT, mar = c(0,0.4,0.2,0.4))
  plot_panel(c(0,100), c(0,34))
  text(0.5, 31, "a   Evidence screening and conditional model", adj = 0, font = 2, cex = 1.05)
  x <- c(12,37,62,87)
  titles <- c("Discovery and search", "Full-text triage", "Source verification", "Conditional ORAC-FL")
  bodies <- c(
    paste0(screen$candidate_profiles," chemical profiles\n",fmt(screen$provisional_intake_union)," screened records"),
    paste0(queue$priority_reports," priority ORAC leads\n",queue$priority_reports-sum(unlist(queue$pending_routes))," scoped reviews"),
    "Original values and units\nMaterial, protocol and errors\nEarlier sources retained",
    paste0(fit$rows," observations  |  ",fit$dois," DOI reports\n",fit$compounds," ranked compounds\nWhole-DOI validation")
  )
  rect(x-11.3, 5.0, x+11.3, 25.4, col = PALE, border = NA)
  text(x, 21, titles, font = 2, cex = 0.76)
  text(x, 12, bodies, cex = 0.72)
  arrows(x[-4]+11.4, 15, x[-1]-11.4, 15, length = 0.06, col = GRAY)
}
d$ypos <- y
# figure1_B panels as ggplot (reliable grob conversion for the composite).
panel_b_gg <- function() {
  db <- data.frame(ypos = d$ypos, compound = d$compound,
                   pct = sprintf("%.0f%%", 100 * d$observed_orac_within_block_percentile),
                   sd = paste0(d$typed_sd_doi_reports, "/", d$conditional_orac_doi_reports),
                   dois = d$conditional_orac_doi_reports)
  ggplot(db, aes(y = ypos)) +
    geom_hline(yintercept = d$ypos - 0.46, color = "#E2E8EC", linewidth = 0.3) +
    geom_text(aes(x = 0.02, label = compound), hjust = 0, size = 2.5) +
    geom_text(aes(x = 0.56, label = pct), size = 2.5) +
    geom_text(aes(x = 0.76, label = sd), size = 2.5) +
    geom_text(aes(x = 0.94, label = dois), size = 2.5) +
    annotate("text", x = c(0.56, 0.76, 0.94), y = nrow(d) + 0.9,
             label = c("ORAC\npercentile", "Reports\nwith SD", "Model\nDOIs"),
             size = 2.4, fontface = 2, lineheight = 0.9) +
    scale_x_continuous(limits = c(0, 1), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0.4, nrow(d) + 1.6), breaks = d$ypos, labels = NULL, expand = c(0, 0)) +
    labs(title = "b   Literature evidence by compound", x = NULL, y = NULL) +
    theme_minimal(base_size = 9, base_family = FONT) +
    theme(panel.grid = element_blank(), axis.ticks = element_blank(),
          plot.title = element_text(face = "bold", size = 10),
          plot.margin = margin(4, 6, 4, 6))
}
panel_c_gg <- function() {
  dc <- d
  dc$kept <- dc$validation_review_status == "RETAIN_STABLE_WITHIN_10"
  dc$ok <- !is.na(dc$max_absolute_rank_shift)
  dc$status <- ifelse(dc$kept, "Retain", ifelse(dc$ok, "Hold", "Rank lost"))
  dc$col <- ifelse(dc$kept, GREEN, GRAY)
  ggplot(dc, aes(y = ypos)) +
    geom_hline(yintercept = dc$ypos - 0.46, color = "#E2E8EC", linewidth = 0.3) +
    geom_rect(aes(xmin = pmax(1, conditional_rank - 10), xmax = pmin(fit$compounds, conditional_rank + 10),
                  ymin = ypos - 0.30, ymax = ypos + 0.30), fill = PALE, inherit.aes = FALSE) +
    geom_segment(data = dc[dc$ok, ], aes(x = best_rank_across_fits_and_deletions,
                 xend = worst_rank_across_fits_and_deletions, y = ypos, yend = ypos, color = col),
                 linewidth = 0.6, inherit.aes = FALSE) +
    geom_point(aes(x = conditional_rank, color = col, shape = kept), size = 1.9) +
    geom_text(aes(x = 57.5, label = status, color = col), hjust = 1, size = 2.2) +
    scale_color_identity() +
    scale_shape_manual(values = c("TRUE" = 16, "FALSE" = 1)) +
    scale_x_continuous(limits = c(0, 58), breaks = c(1, 10, 20, 30, 40, 51), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0.4, nrow(d) + 1.6), breaks = d$ypos, labels = NULL, expand = c(0, 0)) +
    labs(title = "c   Conditional rank and stability", x = "Rank (higher capacity at left)", y = NULL) +
    theme_minimal(base_size = 9, base_family = FONT) +
    theme(panel.grid.major.y = element_blank(), panel.grid.minor = element_blank(),
          axis.text.y = element_blank(), axis.ticks.y = element_blank(),
          plot.title = element_text(face = "bold", size = 10), legend.position = "none",
          plot.margin = margin(4, 6, 4, 6))
}
build_B <- function() { panel_b_gg() + panel_c_gg() + plot_layout(widths = c(1.18, 1)) }
if (!exists("FIG1_COMPOSITE_BUILD")) {
  out <- "06_manuscript/result/figure/figure1_B.evidence_screening_and_ranking"
  pB <- build_B()
  ggsave(paste0(out, ".png"), pB, width = 9.2, height = 5.6, dpi = DPI, bg = "white")
  svglite::svglite(paste0(out, ".svg"), width = 9.2, height = 5.6, bg = "white")
  print(pB); invisible(dev.off())
}
