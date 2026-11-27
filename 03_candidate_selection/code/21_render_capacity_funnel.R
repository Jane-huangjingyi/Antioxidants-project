# Independent figure code: capacity-line evidence funnel (PNG+SVG).
# Run: Rscript 03_candidate_selection/code/21_render_capacity_funnel.R
root <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE))), "..", ".."))
E <- file.path(root, "03_candidate_selection/12_evidence_expansion")
figdir <- file.path(root, "03_candidate_selection/result/figure"); dir.create(figdir, showWarnings = FALSE, recursive = TRUE)
suppressPackageStartupMessages({ library(ggplot2); library(svglite); library(jsonlite) })
q <- fromJSON(file.path(E, "queue_scope_triage_2026-11-27_qc.json"))
x <- fromJSON(file.path(E, "queue_oa_extraction_2026-11-27_qc.json"))
s <- fromJSON(file.path(E, "queue_studytype_refined_2026-11-27_qc.json"))
m <- fromJSON(file.path(E, "queue_pure_manual_review_2026-11-27_qc.json"))
fun <- data.frame(stage = c("Priority queue", "Single-compound", "OA available", "ORAC-ready", "Pure standard", "Clean admissible (OA)"),
                  n = c(q$total, q$eligible_single_compound, x$oa$YES, x$ready_for_review, s$admissible, m$clean_admissible_now))
fun$stage <- factor(fun$stage, levels = fun$stage)
p <- ggplot(fun, aes(x = stage, y = n)) +
  geom_col(fill = "#08519c", width = 0.6) +
  geom_text(aes(label = n), vjust = -0.3, size = 4) +
  labs(title = "Capacity line: ORAC queue evidence funnel",
       subtitle = "Held line: Carthamus n=6 intake+refit (Top20 unchanged); Wang kept held. 111 paywalled need institutional access.",
       x = NULL, y = "Leads",
       caption = "OA-side exhausted; 2 borderline pure standards pending researcher; no clean OA addition. Sources: 09/12/17/20 qc jsons.") +
  theme_minimal(base_size = 11) + theme(axis.text.x = element_text(angle = 20, hjust = 1), plot.title = element_text(face = "bold"),
        plot.caption = element_text(size = 7.5, color = "grey30"))
out <- file.path(figdir, "capacity_evidence_funnel_2026-11-27")
ggsave(paste0(out, ".png"), p, width = 10, height = 6, dpi = 300, bg = "white")
svglite(paste0(out, ".svg"), width = 10, height = 6, bg = "white"); print(p); dev.off()
cat("saved", out, ".png/.svg\n")
