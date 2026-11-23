# Working manuscript panels. Run from the repository root with Rscript.
local_library <- "04_05_experimental_validation/local_library"
if (dir.exists(local_library)) .libPaths(c(normalizePath(local_library), .libPaths()))
library(ggplot2)

FONT <- "sans"
FONT_SIZE <- 12
WIDTH <- 8
HEIGHT <- 4.5
RANK_PANEL_HEIGHT <- 7
DPI <- 300
COLOR <- c(evidence = "#165A7C", candidate = "#236B58", prior = "#64748B",
           sensitivity = "#AA6329", ink = "#183143", line = "#CBD5E1")
OUT <- "06_manuscript/result/figure"
dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
theme_set(theme_minimal(base_family = FONT, base_size = FONT_SIZE) +
            theme(panel.grid.minor = element_blank(), text = element_text(color = COLOR[["ink"]]),
                  plot.caption.position = "plot", plot.caption = element_text(hjust = 0)))
export_panel <- function(plot, name, height = HEIGHT) {
  ggsave(file.path(OUT, paste0(name, ".png")), plot,
         width = WIDTH, height = height, dpi = DPI, bg = "white")
  ggsave(file.path(OUT, paste0(name, ".svg")), plot,
         width = WIDTH, height = height, device = svglite::svglite, bg = "white")
}

evidence <- "02_identity_and_evidence"
model <- "03_candidate_selection"
discover <- read.csv("01_candidate_discovery/results/discovery_register.csv")
profiles <- read.csv(file.path(evidence, "results/candidate_evidence_profiles.csv"))
summary <- jsonlite::read_json(file.path(evidence, "result/table/audit/Screening_QC.json"))
batches <- jsonlite::read_json(file.path(evidence, "result/table/audit/Fulltext_Batch_Summary.json"))

count_plot <- function(frame, caption, color) {
  frame$stage <- factor(frame$stage, levels = rev(frame$stage))
  ggplot(frame, aes(count, stage)) +
    geom_col(width = 0.64, fill = color) +
    geom_text(aes(label = format(count, big.mark = ",", trim = TRUE)), hjust = -0.14, size = 3.5) +
    facet_wrap(~group, ncol = 1, scales = "free") +
    scale_x_continuous(expand = expansion(mult = c(0, 0.22))) +
    labs(x = "Records", y = NULL, caption = caption) +
    theme(strip.text = element_text(face = "bold"), panel.grid.major.y = element_blank())
}

discovery <- data.frame(stage = c("Discovery register", "Identity profiles"),
                        count = c(nrow(discover), nrow(profiles)), group = "Compound discovery")
export_panel(count_plot(discovery, "Source-bounded candidate records and review profiles.",
                        COLOR[["candidate"]]), "figure1-1_candidate_discovery")

recorded <- batches$review_status
text_counts <- c(recorded$CACHED_XML_SCOPE_RECORDED, recorded$REUSE_RECORDED_SCOPE,
                 recorded$SCOPED_REVIEW_THIS_BATCH)
literature <- data.frame(stage = c("Title and abstract", "Title only", "Priority leads", "Recorded review scope"),
                         count = c(summary$abstract_checked, summary$title_only,
                                   batches$priority_reports, sum(unlist(text_counts))),
                         group = c(rep("Deduplicated screen", 2), rep("Priority ORAC follow-up", 2)))
export_panel(count_plot(literature, "Recorded review scopes are targeted checks. Final inclusion has not been adjudicated.",
                        COLOR[["evidence"]]), "figure1-2_literature_screening")

validation <- jsonlite::read_json(file.path(model, "result/model/02_whole_doi_validation.json"))$models
series <- c("Prior fit", "Plus 2021 conditional source", "Plus both sources (sensitivity)")
model_metrics <- data.frame(
  analysis = factor(series, levels = rev(series)),
  rmse = vapply(validation[c("prior", "plus_2021_conditionally", "plus_both_sensitivity")],
                function(x) x$same_prior_test_rmse, numeric(1))
)
export_panel(ggplot(model_metrics, aes(rmse, analysis)) +
               geom_col(fill = COLOR[["evidence"]], width = 0.64) +
               geom_text(aes(label = sprintf("%.3f", rmse)), hjust = -0.14, size = 3.5) +
               scale_x_continuous(expand = expansion(mult = c(0, 0.22))) +
               labs(x = "Held-out log-capacity RMSE", y = NULL,
                    caption = paste("Comparison on the same", validation$prior$same_prior_test_rows,
                                    "estimable observations using whole-DOI holdouts.")),
             "figure2-1_model_validation")

ranks <- read.csv(file.path(model, "result/table/03_rank_sensitivity.csv"))
selected <- ranks$plus_both_sensitivity <= 20 | ranks$candidate_id == "AFF-0104"
plot_ranks <- ranks[selected, ]
plot_ranks <- plot_ranks[order(plot_ranks$plus_both_sensitivity), ]
plot_ranks$compound <- factor(plot_ranks$compound, levels = rev(plot_ranks$compound))
export_panel(ggplot(plot_ranks, aes(y = compound)) +
               geom_segment(aes(x = plus_both_sensitivity, xend = worst_doi_deletion_both,
                                yend = compound), linewidth = 0.5, color = COLOR[["line"]]) +
               geom_point(aes(x = prior, color = "Prior fit"), shape = 1, size = 2.6) +
               geom_point(aes(x = plus_both_sensitivity, color = "Two-source sensitivity"), size = 2.1) +
               scale_color_manual(values = c("Prior fit" = COLOR[["prior"]],
                                             "Two-source sensitivity" = COLOR[["sensitivity"]])) +
               labs(x = "Conditional rank (smaller values indicate higher capacity)", y = NULL,
                    color = NULL, caption = paste("Top 20 in the two-source sensitivity and L-ascorbic acid.",
                                                  "Line ends mark worst whole-DOI deletion bounds.")) +
               theme(legend.position = "bottom"),
             "figure2-2_candidate_rank_stability", RANK_PANEL_HEIGHT)
