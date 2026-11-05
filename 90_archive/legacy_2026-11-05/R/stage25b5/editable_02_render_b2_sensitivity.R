# Canonical B2 qualification figure. Shows only membership changes, not a second formal ranking.
args <- commandArgs(trailingOnly=FALSE); script_arg <- sub("--file=", "", args[grep("--file=", args)])
root <- normalizePath(".", winslash="/", mustWork=TRUE)
source(file.path(root,"R/common/bootstrap.R"))
input <- file.path(root,"data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv")
outdir <- file.path(root,"figures/editable/aqueous_antioxidant_atlas")
dir.create(outdir,recursive=TRUE,showWarnings=FALSE)
d <- read.csv(input,check.names=FALSE,stringsAsFactors=FALSE); stopifnot(sum(d$membership_change=="ENTER")==3,sum(d$membership_change=="LEAVE")==3)
draw <- function(){
 par(mar=c(2,2,4,2),family="sans"); plot.new(); plot.window(xlim=c(0,10),ylim=c(0,10)); title("B2 Sensitivity Qualification: Top20 Membership Changes")
 rect(0.5,1.5,4.5,9,col="#FEF2F2",border="#B91C1C",lwd=2); rect(5.5,1.5,9.5,9,col="#ECFDF5",border="#047857",lwd=2)
 text(2.5,8.2,"LEAVE sensitivity Top20",font=2,col="#991B1B",cex=1.05); text(7.5,8.2,"ENTER sensitivity Top20",font=2,col="#065F46",cex=1.05)
 lv <- d[d$membership_change=="LEAVE",]; en <- d[d$membership_change=="ENTER",]
 text(2.5,c(6.5,5,3.5),paste0(lv$candidate,"\nPrimary rank ",c(18,19,20)),cex=0.95)
 text(7.5,c(6.5,5,3.5),paste0(en$candidate,"\nSensitivity rank ",en$sensitivity_rank),cex=0.95)
 arrows(4.7,5,5.3,5,length=0.12,angle=25,lwd=2,col="#6B7280")
 text(5,0.65,"B2 is sensitivity-only because of predefined unresolved material-comparability risks.\nThis is not a second formal ranking and does not alter the frozen A+B1 primary set.",cex=0.72,col="#374151")
}
png(file.path(outdir,"HORAC_Top20_B2_Sensitivity.png"),width=2200,height=1400,res=220); draw(); dev.off()
svglite::svglite(file.path(outdir,"HORAC_Top20_B2_Sensitivity.svg"),width=10,height=6.4); draw(); dev.off()
