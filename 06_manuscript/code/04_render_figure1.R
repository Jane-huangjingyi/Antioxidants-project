# Editable black-text Figure 1. Run from the repository root.
local_lib <- "04_05_experimental_validation/local_library"
if (dir.exists(local_lib)) .libPaths(c(normalizePath(local_lib), .libPaths()))
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
draw <- function() {
  layout(matrix(c(1,1,2,3), nrow = 2, byrow = TRUE), widths = c(1.18,1), heights = c(0.32,0.68))
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

  par(mar = c(3.2, 0.4, 2.6, 0.5))
  plot_panel(c(0,100), c(0.4,nrow(d)+1.25))
  title(main = "b   Literature evidence by compound", adj = 0, cex.main = 1.05)
  text(c(54,74,92), nrow(d)+0.65, c("ORAC\npercentile", "Reports\nwith SD", "Model\nDOIs"), cex = 0.73, font = 2)
  abline(h = y-0.46, col = "#E2E8EC")
  text(0.8,y,d$compound,adj=0,cex=0.72)
  text(54,y,sprintf("%.0f%%",100*d$observed_orac_within_block_percentile),cex=0.74)
  text(74,y,paste0(d$typed_sd_doi_reports,"/",d$conditional_orac_doi_reports),cex=0.74)
  text(92,y,d$conditional_orac_doi_reports,cex=0.74)

  par(mar = c(3.2,0,2.6,0.9))
  plot_panel(c(0,58), c(0.4,nrow(d)+1.25))
  title(main = "c   Conditional rank and stability", adj = 0, cex.main = 1.05)
  axis(1, at = c(1,10,20,30,40,51), cex.axis = 0.77)
  mtext("Rank (higher capacity at left)", side = 1, line = 2.2, cex = 0.76)
  abline(h = y-0.46, col = "#E2E8EC")
  ok <- !is.na(d$max_absolute_rank_shift)
  kept <- d$validation_review_status == "RETAIN_STABLE_WITHIN_10"
  rect(pmax(1,d$conditional_rank-10),y-0.30,pmin(fit$compounds,d$conditional_rank+10),y+0.30,col=PALE,border=NA)
  segments(d$best_rank_across_fits_and_deletions[ok],y[ok],
           d$worst_rank_across_fits_and_deletions[ok],y[ok],col=ifelse(kept[ok],GREEN,GRAY),lwd=1.5)
  points(d$conditional_rank,y,pch=ifelse(kept,16,1),col=ifelse(kept,GREEN,GRAY),cex=0.78)
  text(57,y,ifelse(kept,"Retain",ifelse(ok,"Hold","Rank lost")),adj=1,cex=0.63,col=ifelse(kept,GREEN,GRAY))
}
out <- "06_manuscript/result/figure/figure1_evidence_screening_and_ranking"
png(paste0(out,".png"),width=WIDTH,height=HEIGHT,units="in",res=DPI,bg="white")
draw()
invisible(dev.off())
svglite::svglite(paste0(out,".svg"),width=WIDTH,height=HEIGHT,bg="white")
draw()
invisible(dev.off())
