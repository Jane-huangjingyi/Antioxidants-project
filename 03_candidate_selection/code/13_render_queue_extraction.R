# Independent figure code: OA extraction readiness for single-compound ORAC queue (PNG+SVG).
# Run: Rscript 03_candidate_selection/code/13_render_queue_extraction.R
root <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE))), "..", ".."))
d <- read.csv(file.path(root, "03_candidate_selection/12_evidence_expansion/queue_oa_extraction_2026-11-27.csv"), stringsAsFactors = FALSE)
figdir <- file.path(root, "03_candidate_selection/result/figure"); dir.create(figdir, showWarnings = FALSE, recursive = TRUE)
suppressPackageStartupMessages({ library(ggplot2); library(svglite); library(patchwork) })
d$status <- ifelse(d$oa == "NO", "Paywalled / no OA",
            ifelse(d$ready_for_review == "YES", "OA + ORAC evidence", "OA, no ORAC snippet"))
cnt <- as.data.frame(table(d$status)); names(cnt) <- c("status", "n")
p1 <- ggplot(cnt, aes(x = status, y = n, fill = status)) +
  geom_col(width = 0.6) + geom_text(aes(label = n), vjust = -0.3, size = 4) +
  scale_fill_manual(values = c("OA + ORAC evidence" = "#2ca02c", "OA, no ORAC snippet" = "#9ecae1", "Paywalled / no OA" = "#d95f02"), guide = "none") +
  labs(title = "Single-compound ORAC leads: OA extraction readiness", x = NULL, y = "Leads") +
  theme_minimal(base_size = 11) + theme(axis.text.x = element_text(angle = 15, hjust = 1), plot.title = element_text(face = "bold"))
sig <- data.frame(signal = c("unit", "error", "protocol"),
                  yes = c(sum(d$unit_sig == "YES"), sum(d$err_sig == "YES"), sum(d$prot_sig == "YES")))
p2 <- ggplot(sig, aes(x = signal, y = yes)) + geom_col(fill = "#08519c", width = 0.5) +
  geom_text(aes(label = yes), vjust = -0.3, size = 4) +
  labs(title = "OA leads with signal present", x = NULL, y = "Leads") +
  theme_minimal(base_size = 11) + theme(plot.title = element_text(face = "bold"))
p <- p1 | p2
p <- p + plot_annotation(caption = "Snippets for researcher review; NOT auto-approved. Six-gate intake required before refit. Source: queue_oa_extraction_2026-11-27.csv (12_extract_queue_oa.py).",
                         theme = theme(plot.caption = element_text(size = 7.5, color = "grey30")))
out <- file.path(figdir, "capacity_queue_oa_extraction_2026-11-27")
ggsave(paste0(out, ".png"), p, width = 12, height = 6, dpi = 300, bg = "white")
svglite(paste0(out, ".svg"), width = 12, height = 6, bg = "white"); print(p); dev.off()
cat("saved", out, ".png/.svg\n")
