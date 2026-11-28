# Run from the repository root. Edit the palette, text, and geometry here.
library(grid)
local_lib <- "04_05_experimental_validation/local_library"
if (dir.exists(local_lib)) .libPaths(c(normalizePath(local_lib), .libPaths()))

WIDTH <- 10
HEIGHT <- 14.7
DPI <- 300
FONT <- "sans"
INK <- "#25324A"
MUTED <- "#4D5A70"
PALETTE <- data.frame(
  dark = c("#644594", "#245994", "#28685C", "#9A4F21", "#993F66"),
  light = c("#F4F0FA", "#EDF5FC", "#EDF7F2", "#FCF3E9", "#FAEFF4"),
  line = c("#C4B4DF", "#ABC7E5", "#A9CDBF", "#E9C49C", "#DDB1C5")
)

audit <- "02_identity_and_evidence/result/table/audit"
screen <- jsonlite::read_json(file.path(audit, "Screening_QC.json"))
queue <- jsonlite::read_json(file.path(audit, "Fulltext_Batch_Summary.json"))
validation <- jsonlite::read_json("03_candidate_selection/result/model/02_whole_doi_validation.json")
fit <- validation$models$plus_2021_conditionally
ranks <- read.csv("03_candidate_selection/result/table/04_figure1_candidate_ranks.csv")
outcomes <- table(ranks$validation_review_status)
retained <- outcomes[["RETAIN_STABLE_WITHIN_10"]]
shifted <- outcomes[["HOLD_RANK_SHIFT_OVER_10"]]
lost <- outcomes[["HOLD_RANK_UNAVAILABLE_AFTER_DOI_DELETION"]]
pending <- sum(unlist(queue$pending_routes))
stopifnot(retained + shifted + lost == fit$compounds)
fmt <- function(x) format(x, big.mark = ",", trim = TRUE, scientific = FALSE)
count <- function(n, label) paste(fmt(n), label)

stages <- list(
  list(label = "Scope", title = "Define the food-derived compound scope",
       heads = c("Food and dietary sources", "Defined chemical entities", count(screen$candidate_profiles, "compound profiles")),
       body = c("Food occurrence and\ndietary origin evidence",
                "Formula, identifiers, structure\nand exact material form",
                "Identity and food-source status\nrecorded per candidate")),
  list(label = "Search", title = "Search by keyword, reconcile records and triage",
       heads = c("Database records", count(screen$provisional_intake_union, "records"), count(queue$priority_reports, "priority ORAC leads")),
       body = c("PubMed, Europe PMC and\navailable Web of Science export",
                "DOI/PMID reconciliation and\nautomated title/abstract triage",
                sprintf("%d with a logged review scope\n%d awaiting scope review",
                        queue$priority_reports - pending, pending))),
  list(label = "Verify", title = "Verify original measurements and harmonize units",
       heads = c("Source and experiment", "Comparable measurements", "Evidence disposition"),
       body = c("Original figure or table,\nmaterial identity and repeats",
                "Probe, pH, temperature, AUC,\nTrolox basis and dispersion",
                "Convert to mol TE/mol where valid.\nLog holds and other assay endpoints.")),
  list(label = "Model", title = "Estimate first-round conditional ORAC-FL capacity",
       heads = c(count(fit$rows, "observations"), "Weighted ridge regression",
                 count(fit$compounds, "ranked compounds")),
       body = c(sprintf("%d DOI reports | mol TE/mol", fit$dois),
                "Fit compound and block effects",
                "Sort compound effects high to low")),
  list(label = "Select", title = "Apply the \u00b110-position stability rule",
       heads = c(count(retained, "retained"), count(shifted, "held for rank shifts"), count(lost, "held for rank loss")),
       body = c("Rank available throughout and\nall shifts within ten positions",
                "At least one scenario moves\nbeyond ten positions",
                "Rank became unavailable after\ndeleting at least one DOI"))
)

search_terms <- list(
  titles = c("Assay terms", "Compound classes", "Compound names and aliases"),
  examples = c("ORAC (oxygen radical\nabsorbance capacity)\nPyrogallol red, crocin bleaching\nABTS, DPPH, FRAP, CUPRAC",
               "Phenolics, flavonoids, carotenoids,\nlignans, vitamins, thiols, alkaloids\n+ antioxidant / radical scavenging",
               "Quercetin, rosmarinic acid,\nL-ascorbic acid / vitamin C\npaired with assay terms")
)

rounded <- function(x, y, w, h, fill, border = NA, lwd = 0.8) {
  grid.roundrect(unit(x, "native"), unit(y, "native"), unit(w, "native"), unit(h, "native"),
                 r = unit(2.4, "mm"), gp = gpar(fill = fill, col = border, lwd = lwd))
}
label <- function(x, y, value, size, color = INK, bold = FALSE, align = "centre") {
  grid.text(value, unit(x, "native"), unit(y, "native"), just = c(align, "centre"),
            gp = gpar(fontfamily = FONT, fontsize = size, col = color,
                      fontface = if (bold) "bold" else "plain", lineheight = 1.11))
}
line <- function(x, y, color, width = 1.6, tip = FALSE) {
  grid.lines(unit(x, "native"), unit(y, "native"),
             arrow = if (tip) grid::arrow(length = unit(2.6, "mm"), type = "closed"),
             gp = gpar(col = color, fill = color, lwd = width, lineend = "round"))
}
dot <- function(x, y, radius, fill, border = NA) {
  grid.circle(unit(x, "native"), unit(y, "native"), unit(radius, "mm"),
              gp = gpar(fill = fill, col = border, lwd = 1.5))
}

stage_icon <- function(stage, x, y, color) {
  if (stage == 1) {
    line(x + c(-2, 0, 2), y + c(1, -1, 1), color)
    dot(x + c(-2, 0, 2), y + c(1, -1, 1), 1.8, "white", color)
  } else if (stage == 2) {
    dot(x - 0.6, y + 0.55, 3.4, NA, color)
    line(x + c(0.5, 2.1), y + c(-0.55, -2.0), color)
  } else if (stage == 3) {
    rounded(x, y, 3.8, 4.1, NA, color)
    line(x + c(-0.9, -0.3, 1.2), y + c(0.1, -0.6, 0.8), color)
  } else if (stage == 4) {
    line(x + c(-2, -2, 2.1), y + c(2, -1.6, -1.6), color)
    line(x + c(-1.3, -0.3, 0.6, 1.9), y + c(-0.8, 0.25, 0.05, 1.45), color)
  } else {
    dot(x, y, 4.0, NA, color)
    dot(x, y, 2.5, NA, color)
    dot(x, y, 0.95, color)
  }
}

model_icon <- function(kind, x, y, color) {
  if (kind == "data") {
    rounded(x, y, 3.9, 3.5, "white", color)
    for (offset in c(-0.62, 0.62)) line(x + c(-1.3, 1.3), y + offset, color, 1.2)
    line(x + 0.25, y + c(-1.45, 1.45), color, 1.2)
  } else if (kind == "weights") {
    offsets <- c(-1.2, 0, 1.2)
    for (i in seq_along(offsets)) {
      yy <- y + offsets[i]
      line(x + c(-1.8, 1.8), rep(yy, 2), color, 1.2)
      dot(x + c(1, -0.9, 0.3)[i], yy, 1.15, "white", color)
    }
  } else if (kind == "rank") {
    for (i in 1:3) {
      yy <- y + c(1.25, 0, -1.25)[i]
      line(x + c(-1.45, c(1.9, 1.05, 0.1)[i]), rep(yy, 2), color, 2)
    }
  } else if (kind == "plate") {
    rounded(x, y, 5, 3.8, "white", color)
    wells <- expand.grid(x = x + c(-1.45, 0, 1.45), y = y + c(-0.88, 0.88))
    dot(wells$x, wells$y, 0.85, "#E7EDF8", color)
  }
}

draw_model <- function(y, stage, color, border) {
  xs <- c(30.2, 56.2, 82.2)
  icons <- c("data", "weights", "rank")
  for (j in seq_along(xs)) {
    x <- xs[j]
    rounded(x, y + 8.2, 23.1, 9.2, "white", border)
    model_icon(icons[j], x, y + 10.6, color)
    label(x, y + 7.2, stage$heads[j], 10.8, color, TRUE)
    label(x, y + 4.9, stage$body[j], 8.8)
    if (j < length(xs)) line(c(x + 11.7, xs[j + 1] - 11.7),
                             rep(y + 8.2, 2), color, 1.2, TRUE)
  }

  rounded(56.25, y - 2.9, 75.2, 10.3, "#FFFDFB", border)
  label(56.25, y - 0.2,
        "log(C\u1d62) = \u03b2[compound] + \u03b3[study \u00d7 protocol] + \u03b5\u1d62",
        16.2, color, TRUE)
  label(56.25, y - 3.5,
        "C\u1d62 = positive molar ORAC-FL mean   |   Block effects centered at zero",
        10.0, INK)
  label(56.25, y - 5.7,
        "Minimize weighted squared error + ridge penalty (\u03bb = 10) on block effects",
        9.7, MUTED)

  label(19.8, y - 10.1,
        "Raw weight = (1 / rows per DOI) \u00d7 max(0.10, 1 / [1 + (CV / 0.25)\u00b2])",
        10.4, color, TRUE, "left")
  label(19.8, y - 12.35,
        "CV = reported SD / mean. Use multiplier 1 without a typed SD. Normalize weights to mean 1.",
        9.4, INK, align = "left")
  label(19.8, y - 14.5, sprintf(
    "Whole-DOI holdout   |   %d matched observations   |   Log-RMSE %.3f",
    fit$same_prior_test_rows, fit$same_prior_test_rmse
  ), 9.3, MUTED, align = "left")
}

draw <- function() {
  grid.newpage()
  pushViewport(viewport(xscale = c(0, 100), yscale = c(0, 147)))
  rounded(50, 137.5, 93, 12.5, PALETTE$light[1], PALETTE$line[1])
  label(50, 139.1, "Screening food-derived antioxidants", 25, PALETTE$dark[1], TRUE)
  label(50, 134.9, "From literature evidence to candidates for aqueous testing", 12.8, MUTED)
  centers <- c(121.5, 99, 76.5, 48.5, 20.5)
  heights <- c(13.4, 24.4, 13.4, 35.4, 13.4)
  line(c(8.5, 8.5), range(centers), "#D2D8E3", 1)
  for (i in seq_along(stages)) {
    y <- centers[i]
    s <- stages[[i]]
    color <- PALETTE$dark[i]
    rounded(8.5, y, 10, 13.4, PALETTE$light[i])
    dot(8.5, y + 3.4, 3.9, color)
    label(8.5, y + 3.4, as.character(i), 12.2, "white", TRUE)
    stage_icon(i, 8.5, y - 0.1, color)
    label(8.5, y - 4.5, s$label, 10.7, color, TRUE)
    line(c(13.5, 16), c(y, y), PALETTE$line[i], 1)
    rounded(56.25, y, 80.5, heights[i], PALETTE$light[i], PALETTE$line[i])
    label(18.5, y + heights[i] / 2 - 2.25, s$title, 14.1, color, TRUE, "left")
    if (i == 4) {
      draw_model(y, s, color, PALETTE$line[i])
    } else {
      for (j in seq_along(s$heads)) {
        x <- c(30.2, 56.2, 82.2)[j]
        card_y <- y - 1.4 + if (i == 2) 5.5 else 0
        rounded(x, card_y, 24.75, 7.65, "white", PALETTE$line[i])
        label(x, card_y + 1.75, s$heads[j], 10.8, color, TRUE)
        label(x, card_y - 1.1, s$body[j], 9.5)
        if (i == 2) {
          rounded(x, y - 5.9, 24.75, 9.2, "white", PALETTE$line[i])
          label(x, y - 3.1, search_terms$titles[j], 10.3, color, TRUE)
          label(x, y - 6.8, search_terms$examples[j], 8.9)
        }
      }
    }
    if (i < length(stages)) {
      line(c(56, 56), c(y - heights[i] / 2 - 0.2,
                        centers[i + 1] + heights[i + 1] / 2 + 0.3), color, 1.5, TRUE)
    }
  }
  line(c(56, 56), c(13.6, 10.8), PALETTE$dark[5], 1.5, TRUE)
  rounded(56.25, 6.25, 80.5, 7.5, "#F2F6FA", "#BDCADA")
  model_icon("plate", 21.4, 6.25, "#35476A")
  label(56, 7.8, "Next step  |  Aqueous absorbance validation", 13.3, "#35476A", TRUE)
  label(56, 4.95, "Prospective experimental qualification of the retained candidates", 10.1, MUTED)
  popViewport()
}

if (!exists("FIG1_COMPOSITE_BUILD")) {
  output <- "06_manuscript/result/figure/figure1_A.flow_chart"
  png(paste0(output, ".png"), width = WIDTH, height = HEIGHT, units = "in", res = DPI, bg = "white")
  draw()
  invisible(dev.off())
  svglite::svglite(paste0(output, ".svg"), width = WIDTH, height = HEIGHT, bg = "white")
  draw()
  invisible(dev.off())
}
