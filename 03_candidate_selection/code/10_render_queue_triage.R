# Independent figure code: ORAC queue scope triage (PNG+SVG).
# Run: Rscript 03_candidate_selection/code/10_render_queue_triage.R
root <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE))), "..", ".."))
d <- read.csv(file.path(root, "03_candidate_selection/12_evidence_expansion/queue_scope_triage_2026-11-27.csv"), stringsAsFactors = FALSE)
figdir <- file.path(root, "03_candidate_selection/result/figure"); dir.create(figdir, showWarnings = FALSE, recursive = TRUE)
suppressPackageStartupMessages({ library(ggplot2); library(svglite) })
cnt <- as.data.frame(table(d$scope))
names(cnt) <- c("scope", "n")
cnt$scope <- factor(cnt$scope, levels = cnt$scope[order(-cnt$n)])
cols <- c(SINGLE_COMPOUND_CANDIDATE = "#2ca02c", MIXTURE_EXTRACT_FOOD = "#d95f02",
          MULTI_COMPOUND_UNCLEAR = "#9ecae1", METHOD_DEVELOPMENT = "#7f7f7f")
p <- ggplot(cnt, aes(x = scope, y = n, fill = scope)) +
  geom_col(width = 0.65) +
  geom_text(aes(label = n), vjust = -0.3, size = 4) +
  scale_fill_manual(values = cols, guide = "none") +
  labs(title = "ORAC full-text review queue: scope triage",
       subtitle = paste0("total leads=", nrow(d), "; single-compound eligible=", sum(d$scope == "SINGLE_COMPOUND_CANDIDATE")),
       x = NULL, y = "Leads",
       caption = "Title-based triage; only single-compound leads eligible for extraction + six-gate intake. Source: queue_scope_triage_2026-11-27.csv (09_triage_capacity_queue.py).") +
  theme_minimal(base_size = 11) +
  theme(axis.text.x = element_text(angle = 20, hjust = 1), plot.title = element_text(face = "bold"),
        plot.caption = element_text(size = 7.5, color = "grey30"))
out <- file.path(figdir, "capacity_queue_scope_triage_2026-11-27")
ggsave(paste0(out, ".png"), p, width = 9, height = 6, dpi = 300, bg = "white")
svglite(paste0(out, ".svg"), width = 9, height = 6, bg = "white"); print(p); dev.off()
cat("saved", out, ".png/.svg\n")
