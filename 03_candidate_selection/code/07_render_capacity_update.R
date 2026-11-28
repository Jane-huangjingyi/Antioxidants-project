# Independent, modifiable figure code for the capacity evidence update (Carthamus 2026-11-27).
# Outputs PNG + SVG. Run: Rscript 03_candidate_selection/code/07_render_capacity_update.R [run_dir]
args <- commandArgs(trailingOnly = TRUE)
root <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE))), "..", ".."))
run <- if (length(args) >= 1) args[1] else "run_carthamus_2026-11-27"
rundir <- file.path(root, "03_candidate_selection/12_evidence_expansion", run)
figdir <- file.path(root, "03_candidate_selection/result/figure")
.libPaths(c(file.path(root, "04_05_experimental_validation", "local_library"), .libPaths()))
dir.create(figdir, showWarnings = FALSE, recursive = TRUE)
suppressPackageStartupMessages({ library(ggplot2); library(svglite); library(patchwork); library(jsonlite) })

mp <- read.csv(file.path(rundir, "Model_Positions.csv"), stringsAsFactors = FALSE)
rep <- fromJSON(file.path(rundir, "Evidence_Change_Report.json"))
release_file <- file.path(rundir, "Release_Record.json")
release <- if (file.exists(release_file)) fromJSON(release_file) else NULL
release_status <- if (isTRUE(release$released)) {
  paste("Researcher-approved release", release$release_date)
} else {
  "Review run pending release"
}
membership <- if (isFALSE(release$top20_membership_changed)) "unchanged" else if (
  isTRUE(release$top20_membership_changed)) "changed" else "pending release verification"
model_rows <- if (is.null(release$model_rows)) "" else paste0(" | Model rows ", release$model_rows)
affected <- rep$affected_candidates
mp$affected <- ifelse(mp$candidate_id %in% affected, "New evidence (Carthamus)", "Existing")

p_pos <- ggplot(mp, aes(x = baseline_position, y = next_position, color = affected)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "grey50") +
  geom_point(aes(size = affected), alpha = 0.85) +
  scale_color_manual(values = c("New evidence (Carthamus)" = "#d95f02", "Existing" = "#08519c")) +
  scale_size_manual(values = c("New evidence (Carthamus)" = 3, "Existing" = 1.6)) +
  labs(title = "Connected ORAC-FL model positions: baseline vs +Carthamus",
       subtitle = paste0(rep$added_observations, " added observations", model_rows,
                         " | Top 20 ", membership),
       x = "Baseline position", y = "Next position", color = NULL, size = NULL) +
  theme_minimal(base_size = 11) + theme(legend.position = "bottom", plot.title = element_text(face = "bold"))

met <- data.frame(stage = rep(c("old", "new"), each = 2),
                  type = rep(c("model", "baseline"), 2),
                  rmse = c(rep$old_model_metrics$model_RMSE, rep$old_model_metrics$baseline_RMSE,
                           rep$new_model_metrics$model_RMSE, rep$new_model_metrics$baseline_RMSE))
met$stage <- factor(met$stage, levels = c("old", "new"))
p_rmse <- ggplot(met, aes(x = stage, y = rmse, fill = type)) +
  geom_col(position = position_dodge(width = 0.7), width = 0.6) +
  geom_text(aes(label = sprintf("%.2f", rmse)), position = position_dodge(width = 0.7), vjust = -0.3, size = 3) +
  scale_fill_manual(values = c(model = "#08519c", baseline = "#9ecae1")) +
  labs(title = "Leave-one-DOI-out RMSE",
       subtitle = sprintf("Scored observations: old %d, new %d",
                          rep$old_model_metrics$scored, rep$new_model_metrics$scored),
       x = NULL, y = "RMSE of log capacity", fill = NULL) +
  theme_minimal(base_size = 11) + theme(legend.position = "bottom", plot.title = element_text(face = "bold"))

p <- p_pos | p_rmse
p <- p + plot_annotation(caption = paste(release_status,
                                         "Within each cohort, compare the model with its matched baseline.",
                                         paste("Source:", run),
                                         sep = "\n"),
                         theme = theme(plot.caption = element_text(size = 7.5, color = "grey30")))
out <- file.path(figdir, "capacity_update_carthamus_2026-11-27")
ggsave(paste0(out, ".png"), p, width = 12, height = 6, dpi = 300, bg = "white")
svglite(paste0(out, ".svg"), width = 12, height = 6, bg = "white"); print(p); dev.off()
cat("saved", out, ".png/.svg\n")
