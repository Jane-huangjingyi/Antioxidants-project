# Render the 12-compound pathway evidence report figures (step 02).
# Reads the committed inventory/dictionary/counts CSVs; emits PNG + editable SVG pairs.
# Run from repo root: Rscript 02_identity_and_evidence/code/05_render_pathway_figures.R

here <- normalizePath("02_identity_and_evidence/code", mustWork = TRUE)
root <- dirname(dirname(here))
.libPaths(c(file.path(root, "04_05_experimental_validation", "local_library"), .libPaths()))
suppressPackageStartupMessages({
  library(ggplot2)
  library(svglite)
  library(patchwork)
})

tbl <- file.path(root, "02_identity_and_evidence", "result", "table")
figdir <- file.path(root, "02_identity_and_evidence", "result", "figure")
dir.create(figdir, showWarnings = FALSE, recursive = TRUE)

dict <- read.csv(file.path(tbl, "audit", "Pathway_Dictionary.csv"), stringsAsFactors = FALSE)
inv <- read.csv(file.path(tbl, "05_compound_pathway_inventory.csv"), stringsAsFactors = FALSE)
cnt <- read.csv(file.path(tbl, "06_pathway_overlap_counts.csv"), stringsAsFactors = FALSE)
ranks <- read.csv(file.path(root, "03_candidate_selection", "result", "table", "04_figure1_candidate_ranks.csv"), stringsAsFactors = FALSE)

ret <- ranks[ranks$validation_review_status == "RETAIN_STABLE_WITHIN_10", ]
ret <- ret[order(as.integer(ret$conditional_rank)), ]
comp_order <- ret$compound
short <- c("Quercetin"="Quercetin","Catechin"="Catechin","Hesperetin"="Hesperetin","Genistein"="Genistein",
           "Hesperidin"="Hesperidin","Myricetin"="Myricetin","p-Coumaric acid"="p-Coumaric",
           "Chlorogenic acid"="Chlorogenic","Gallic acid"="Gallic","Syringic acid"="Syringic",
           "L-Ascorbic acid"="L-Ascorbic","Glutathione"="Glutathione")
comp_lab <- unname(short[comp_order])

SIGN <- dict$pathway_code[dict$pathway_class == "SIGNALING"]
REDOX <- dict$pathway_code[dict$pathway_class == "REDOX_PROCESS"]
ALLP <- dict$pathway_code
pname <- setNames(dict$pathway_name, dict$pathway_code)
pclass <- setNames(dict$pathway_class, dict$pathway_code)
plab <- setNames(paste0(dict$pathway_code, "  ", dict$pathway_name), dict$pathway_code)

grade_rank <- c(FUNCTIONAL = 3, BODY_READOUT = 2, ABSTRACT_ONLY = 1)
grade_levels <- c("FUNCTIONAL", "BODY_READOUT", "ABSTRACT_ONLY", "NONE")
grade_cols <- c(FUNCTIONAL = "#08519c", BODY_READOUT = "#6baed6", ABSTRACT_ONLY = "#fcae91", NONE = "#f4f4f4")

# ---- matrix (highest recorded grade per compound x pathway) ----
cells <- expand.grid(pathway_code = ALLP, compound = comp_order, stringsAsFactors = FALSE)
cells$grade <- "NONE"; cells$flag <- ""
for (i in seq_len(nrow(cells))) {
  sub <- inv[inv$pathway_code == cells$pathway_code[i] & inv$compound == cells$compound[i], ]
  if (nrow(sub)) {
    best <- sub$evidence_grade[which.max(grade_rank[sub$evidence_grade])]
    cells$grade[i] <- best
    if (any(sub$integrity_flag == "FIG8A_CONCERN")) cells$flag[i] <- "*"
  }
}
cells$grade <- factor(cells$grade, levels = grade_levels)
cells$pathway_code <- factor(cells$pathway_code, levels = rev(ALLP))
cells$compound <- factor(cells$compound, levels = comp_order)
cells$plab <- factor(plab[as.character(cells$pathway_code)], levels = rev(plab[ALLP]))
cells$cl <- ifelse(pclass[as.character(cells$pathway_code)] == "SIGNALING", "Signaling pathways", "Redox process families")
cells$cl <- factor(cells$cl, levels = c("Signaling pathways", "Redox process families"))
cells$xlab <- factor(unname(short[as.character(cells$compound)]), levels = comp_lab)

p_mat <- ggplot(cells, aes(x = xlab, y = plab)) +
  geom_tile(aes(fill = grade), color = "white", linewidth = 0.6) +
  geom_text(aes(label = flag), color = "#b2182b", size = 5, fontface = "bold") +
  scale_fill_manual(values = grade_cols, drop = FALSE,
                    labels = c("Functional participation (loss-of-function)", "Body readout (in vivo/ex vivo/human)",
                               "Abstract-only / unresolved", "No recorded association")) +
  facet_wrap(~ cl, scales = "free_y", ncol = 1) +
  scale_x_discrete(position = "top") +
  labs(title = "Pathway evidence matrix - 12 retained antioxidant candidates",
       subtitle = "Highest recorded evidence grade per compound x pathway; * = hesperetin Fig. 8a image-similarity concern (excluded from solid set)",
       x = NULL, y = NULL, fill = "Evidence grade",
       caption = "Source: 04_candidate_in_vivo_mechanism_evidence.csv (28 observations, 26 reports). All rows NOT_REVIEWED. Solid set = functional + body readout, excluding abstract-only and Fig. 8a-flagged rows.") +
  theme_minimal(base_size = 11, base_family = "sans") +
  theme(axis.text.x = element_text(angle = 45, hjust = 0, vjust = 0.5, size = 9),
        axis.text.y = element_text(size = 8.5),
        panel.grid = element_blank(),
        strip.text = element_text(face = "bold", size = 10),
        legend.position = "bottom", legend.box = "vertical",
        plot.caption = element_text(size = 7.5, color = "grey30"),
        plot.title = element_text(face = "bold"))

# ---- set sizes (all vs solid) ----
sz <- data.frame(pathway_code = rep(ALLP, 2),
                 scope = rep(c("All recorded", "Solid only"), each = length(ALLP)),
                 n = c(cnt$n_compounds_all_recorded, cnt$n_compounds_solid))
sz$plab <- factor(plab[sz$pathway_code], levels = rev(plab[ALLP]))
sz$scope <- factor(sz$scope, levels = c("All recorded", "Solid only"))
sz$cl <- ifelse(pclass[sz$pathway_code] == "SIGNALING", "Signaling pathways", "Redox process families")
sz$cl <- factor(sz$cl, levels = c("Signaling pathways", "Redox process families"))
p_sz <- ggplot(sz, aes(x = plab, y = n, fill = scope)) +
  geom_col(position = position_dodge(width = 0.7), width = 0.62) +
  geom_text(aes(label = n), position = position_dodge(width = 0.7), hjust = -0.25, size = 3.1) +
  coord_flip() + facet_wrap(~ cl, scales = "free_y", ncol = 1) +
  scale_fill_manual(values = c("All recorded" = "#bdbdbd", "Solid only" = "#08519c")) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.12)), breaks = 0:12) +
  labs(title = "How many candidates share each pathway",
       subtitle = "Number of the 12 retained compounds with a recorded association (all) vs solid evidence only",
       x = NULL, y = "Number of compounds", fill = NULL,
       caption = "P7 PGC-1alpha has no in vivo assignment (cell-only linkage). Solid excludes abstract-only and Fig. 8a-flagged rows.") +
  theme_minimal(base_size = 11, base_family = "sans") +
  theme(axis.text.y = element_text(size = 8.5), panel.grid.major.y = element_blank(),
        strip.text = element_text(face = "bold"), legend.position = "bottom",
        plot.caption = element_text(size = 7.5, color = "grey30"), plot.title = element_text(face = "bold"))

# ---- UpSet (solid signaling intersections; sets = pathways, elements = compounds) ----
comp_set <- list()
for (c in comp_order) {
  sub <- inv[inv$compound == c & inv$solid_included == "YES" & inv$pathway_code %in% SIGN, ]
  comp_set[[c]] <- sort(unique(sub$pathway_code))
}
keys <- sapply(comp_set, function(x) paste(x, collapse = "+"))
ukey <- unique(keys[keys != ""])
inters <- lapply(ukey, function(k) {
  ps <- strsplit(k, "\\+")[[1]]
  comps <- comp_order[keys == k]
  list(pathways = ps, size = length(comps), compounds = comps)
})
inters <- inters[order(-sapply(inters, function(x) x$size), sapply(inters, function(x) paste(x$pathways, collapse = "+")))]
K <- length(inters)
setsize <- sapply(SIGN, function(p) sum(sapply(comp_set, function(x) p %in% x)))

mx <- expand.grid(pathway_code = SIGN, int_id = seq_len(K), stringsAsFactors = FALSE)
mx$present <- mapply(function(p, i) p %in% inters[[i]]$pathways, mx$pathway_code, mx$int_id)
mx$y <- match(mx$pathway_code, SIGN)
mx$x <- mx$int_id
seg <- do.call(rbind, lapply(seq_len(K), function(i) {
  ys <- mx$y[mx$int_id == i & mx$present]
  if (length(ys) >= 2) data.frame(x = i, y = min(ys), yend = max(ys)) else NULL
}))
size_df <- data.frame(int_id = seq_len(K), size = sapply(inters, function(x) x$size),
                      lab = sapply(inters, function(x) paste(x$pathways, collapse = "+")))
set_df <- data.frame(pathway_code = SIGN, y = seq_along(SIGN), n = unname(setsize[SIGN]),
                     plab = plab[SIGN])

th <- theme_minimal(base_size = 10, base_family = "sans") +
  theme(panel.grid = element_blank(), axis.ticks = element_blank(), legend.position = "none")
p_isize <- ggplot(size_df, aes(x = int_id, y = size)) +
  geom_col(fill = "#08519c", width = 0.6) +
  geom_text(aes(label = size), vjust = -0.3, size = 3.4) +
  scale_x_continuous(limits = c(0.5, K + 0.5), expand = c(0, 0)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.18))) +
  labs(y = "Intersection size") + th +
  theme(axis.title.x = element_blank(), axis.text.x = element_blank(), axis.line.y = element_line(color = "grey60"))
p_matrix <- ggplot(mx, aes(x = x, y = y)) +
  geom_segment(data = seg, aes(x = x, y = y, xend = x, yend = yend), color = "#08519c", linewidth = 0.8, inherit.aes = FALSE) +
  geom_point(aes(fill = present), shape = 21, size = 4.2, stroke = 0.4, color = "grey40") +
  scale_fill_manual(values = c("TRUE" = "#08519c", "FALSE" = "#e8e8e8")) +
  scale_x_continuous(limits = c(0.5, K + 0.5), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0.5, length(SIGN) + 0.5), expand = c(0, 0), breaks = seq_along(SIGN), labels = SIGN) +
  labs(x = "Intersection (shared pathway set)", y = NULL) + th +
  theme(axis.line.x = element_line(color = "grey60"), axis.text.y = element_text(size = 9))
p_sets <- ggplot(set_df, aes(x = n, y = y)) +
  geom_col(fill = "#6baed6", width = 0.6, orientation = "y") +
  geom_text(aes(label = n), hjust = -0.3, size = 3.2) +
  scale_y_continuous(limits = c(0.5, length(SIGN) + 0.5), expand = c(0, 0), breaks = seq_along(SIGN), labels = plab[SIGN]) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.2))) +
  labs(x = "Set size", y = NULL) + th +
  theme(axis.text.y = element_text(size = 8), axis.line.x = element_line(color = "grey60"))
spacer <- ggplot() + theme_void()
p_upset <- (spacer + p_isize + p_sets + p_matrix) +
  plot_layout(design = "AB\nCD", widths = c(2.4, 3), heights = c(1, 2.6)) +
  plot_annotation(title = "UpSet - shared signaling pathways among the 12 candidates (solid evidence)",
                  subtitle = "Sets = 8 signaling pathways; elements = compounds. Bars = compounds sharing each exact pathway combination; left bars = compounds per pathway.",
                  caption = "Solid = functional + body readout, excluding abstract-only and Fig. 8a-flagged rows. Catechin, p-Coumaric acid and L-Ascorbic acid have no solid signaling-pathway assignment. All rows NOT_REVIEWED.",
                  theme = theme(plot.title = element_text(face = "bold", size = 12),
                                plot.subtitle = element_text(size = 8.5), plot.caption = element_text(size = 7.5, color = "grey30")))

save_pair <- function(plot, name, w, h) {
  ggsave(file.path(figdir, paste0(name, ".png")), plot, width = w, height = h, dpi = 300, bg = "white")
  svglite::svglite(file.path(figdir, paste0(name, ".svg")), width = w, height = h, bg = "white")
  print(plot)
  dev.off()
  cat("saved", name, "\n")
}
save_pair(p_mat, "pathway_evidence_matrix", 11.5, 9)
save_pair(p_sz, "pathway_set_sizes", 11, 8)
save_pair(p_upset, "pathway_upset_signaling", 11, 7.5)
cat("done\n")
