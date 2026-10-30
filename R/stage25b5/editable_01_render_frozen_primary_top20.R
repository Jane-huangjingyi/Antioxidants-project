# Canonical Stage25B.5 primary figure. Input is the frozen CSV; ranking is A+B1 median H-ORAC.
args <- commandArgs(trailingOnly=FALSE); script_arg <- sub("--file=", "", args[grep("--file=", args)])
root <- normalizePath(".", winslash="/", mustWork=TRUE)
source(file.path(root,"R/common/bootstrap.R"))
input <- file.path(root, "data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv")
outdir <- file.path(root, "figures/editable/aqueous_antioxidant_atlas"); dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
d <- read.csv(input, check.names=FALSE, stringsAsFactors=FALSE)
stopifnot(nrow(d)==20, length(unique(d$candidate_id))==20, all(d$primary_rank == 1:20)); d$y <- rev(seq_len(nrow(d)))
cols <- c(High="#176B87", Moderate="#D97706", Low="#7C3AED")
draw <- function() {
  par(mar=c(5.5,17.5,4.2,2), family="sans")
  plot(NA, xlim=c(0,max(d$max_H_ORAC,na.rm=TRUE)*1.05), ylim=c(0.5,20.5), axes=FALSE, xlab="Median H-ORAC (mol Trolox equivalents / mol compound)", ylab="", main="Frozen Primary H-ORAC Top20 (A+B1)")
  abline(v=pretty(c(0,max(d$max_H_ORAC,na.rm=TRUE))), col="#E5E7EB", lwd=0.8); axis(1)
  axis(2, at=d$y, labels=paste0(d$primary_rank, ". ", d$canonical_name), las=1, tick=FALSE, cex.axis=0.78)
  for(i in seq_len(nrow(d))) if(d$eligible_A_B1_N[i] > 1) {
    segments(d$min_H_ORAC[i],d$y[i],d$max_H_ORAC[i],d$y[i],col="#9CA3AF",lwd=2)
    if(!is.na(d$IQR[i]) && d$IQR[i] > 0) segments(max(0,d$median_H_ORAC_mol_TE_per_mol[i]-d$IQR[i]/2),d$y[i],d$median_H_ORAC_mol_TE_per_mol[i]+d$IQR[i]/2,d$y[i],col="#374151",lwd=5)
  }
  points(d$median_H_ORAC_mol_TE_per_mol,d$y,pch=21,bg=cols[d$evidence_confidence],col="white",lwd=1.2,cex=0.9+0.25*sqrt(d$eligible_A_B1_N))
  legend("bottomright",legend=c("High confidence","Moderate confidence","Low confidence","Range (N>1)","Approx. IQR width"),pch=c(21,21,21,NA,NA),pt.bg=c(cols["High"],cols["Moderate"],cols["Low"],NA,NA),col=c("white","white","white","#9CA3AF","#374151"),lwd=c(NA,NA,NA,2,5),bty="n",cex=0.72)
  mtext("Point size = eligible A+B1 experiment N; singleton ranges are not drawn.",side=1,line=4.2,cex=0.72,col="#4B5563")
}
png(file.path(outdir,"HORAC_Primary_Top20_Frozen.png"),width=2400,height=1800,res=220); draw(); dev.off()
svglite::svglite(file.path(outdir,"HORAC_Primary_Top20_Frozen.svg"),width=11,height=8.2); draw(); dev.off()
