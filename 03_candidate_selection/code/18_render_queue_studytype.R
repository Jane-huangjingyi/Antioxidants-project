# Independent figure code: refined study type of ORAC-ready queue (PNG+SVG).
# Run: Rscript 03_candidate_selection/code/18_render_queue_studytype.R
root <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE))), "..", ".."))
d <- read.csv(file.path(root, "03_candidate_selection/12_evidence_expansion/queue_studytype_refined_2026-11-27.csv"), stringsAsFactors = FALSE)
figdir <- file.path(root, "03_candidate_selection/result/figure"); dir.create(figdir, showWarnings = FALSE, recursive = TRUE)
suppressPackageStartupMessages({ library(ggplot2); library(svglite) })
cnt <- as.data.frame(table(d$study_type)); names(cnt) <- c("type", "n")
cnt$type <- factor(cnt$type, levels = cnt$type[order(-cnt$n)])
cols <- c(PURE_STANDARD = "#2ca02c", MATRIX_FOOD = "#d95f02", EPIDEMIOLOGY_HUMAN = "#9467bd", METHOD = "#7f7f7f", UNCLEAR = "#9ecae1")
p <- ggplot(cnt, aes(x = type, y = n, fill = type)) +
  geom_col(width = 0.6) + geom_text(aes(label = n), vjust = -0.3, size = 4) +
  scale_fill_manual(values = cols, guide = "none") +
  labs(title = "ORAC-ready leads: refined study type",
       subtitle = paste0("admissible pure standards=", sum(d$admissible_for_intake == "YES"), " of ", nrow(d)),
       x = NULL, y = "Leads",
       caption = "Matrix/food/epidemiology/method not admissible for single-compound intake. Source: queue_studytype_refined_2026-11-27.csv (17_refine_queue_studytype.py).") +
  theme_minimal(base_size = 11) + theme(axis.text.x = element_text(angle = 20, hjust = 1), plot.title = element_text(face = "bold"),
        plot.caption = element_text(size = 7.5, color = "grey30"))
out <- file.path(figdir, "capacity_queue_studytype_2026-11-27")
ggsave(paste0(out, ".png"), p, width = 9, height = 6, dpi = 300, bg = "white")
svglite(paste0(out, ".svg"), width = 9, height = 6, bg = "white"); print(p); dev.off()
cat("saved", out, ".png/.svg\n")
