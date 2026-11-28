# figure1_C.pathway_framework - top-down antioxidant pathway framework (provisional).
# Reads step-02 framework matrix + curated universe; emits PNG + editable SVG.
# Run from repo root: Rscript 06_manuscript/code/07_render_figure1_C_pathway.R
here <- normalizePath("06_manuscript/code", mustWork = TRUE)
root <- dirname(dirname(here))
.libPaths(c(file.path(root, "04_05_experimental_validation", "local_library"), .libPaths()))
suppressPackageStartupMessages({ library(ggplot2); library(svglite); library(patchwork) })

tbl02 <- file.path(root, "02_identity_and_evidence", "result", "table")
figdir <- file.path(root, "06_manuscript", "result", "figure")
supp <- file.path(figdir, "supplementary")
dir.create(figdir, showWarnings = FALSE, recursive = TRUE)
dir.create(supp, showWarnings = FALSE, recursive = TRUE)

mat <- read.csv(file.path(tbl02, "07_pathway_framework_matrix.csv"), stringsAsFactors = FALSE)
univ <- read.csv(file.path(tbl02, "audit", "Pathway_Universe_Curated.csv"), stringsAsFactors = FALSE)
ranks <- read.csv(file.path(root, "03_candidate_selection", "result", "table", "04_figure1_candidate_ranks.csv"), stringsAsFactors = FALSE)
ret <- ranks[ranks$validation_review_status == "RETAIN_STABLE_WITHIN_10", ]
ret <- ret[order(as.integer(ret$conditional_rank)), ]
comp_order <- ret$compound
short <- c("Quercetin"="Quercetin","Catechin"="Catechin","Hesperetin"="Hesperetin","Genistein"="Genistein",
           "Hesperidin"="Hesperidin","Myricetin"="Myricetin","p-Coumaric acid"="p-Coumaric",
           "Chlorogenic acid"="Chlorogenic","Gallic acid"="Gallic","Syringic acid"="Syringic",
           "L-Ascorbic acid"="L-Ascorbic","Glutathione"="Glutathione")
comp_lab <- unname(short[comp_order])
U <- univ$pathway_code
universe_label <- paste(U[1], tail(U, 1), sep = "-")
ulab <- setNames(paste0(univ$pathway_code, "  ", univ$pathway_name), univ$pathway_code)
uclass <- setNames(univ$pathway_class, univ$pathway_code)

states <- c("FUNCTIONAL","BODY_READOUT","ABSTRACT_ONLY","CELL_ONLY","NOT_REPORTED_IN_CHECKED_SET","PENDING_EXPANSION")
cols <- c(FUNCTIONAL="#08519c", BODY_READOUT="#6baed6", ABSTRACT_ONLY="#fcae91",
          CELL_ONLY="#c994c7", NOT_REPORTED_IN_CHECKED_SET="#ffffff", PENDING_EXPANSION="#efefef")
labs <- c(FUNCTIONAL="Functional participation (loss-of-function)",
          BODY_READOUT="Body readout (in vivo / ex vivo / human)",
          ABSTRACT_ONLY="Abstract-level candidate",
          CELL_ONLY="Cell-only evidence",
          NOT_REPORTED_IN_CHECKED_SET="No qualifying report in checked set",
          PENDING_EXPANSION="Pending search")
n_solid <- sum(mat$cell_state %in% c("FUNCTIONAL","BODY_READOUT"))
n_abs <- sum(mat$cell_state=="ABSTRACT_ONLY")
n_cell <- sum(mat$cell_state=="CELL_ONLY")
n_nr <- sum(mat$cell_state=="NOT_REPORTED_IN_CHECKED_SET")
n_pend <- sum(mat$cell_state=="PENDING_EXPANSION")

mat$compound <- factor(mat$compound, levels = comp_order)
mat$xlab <- factor(unname(short[as.character(mat$compound)]), levels = comp_lab)
mat$pathway_code <- factor(mat$pathway_code, levels = rev(U))
mat$plab <- factor(ulab[as.character(mat$pathway_code)], levels = rev(ulab[U]))
mat$cell_state <- factor(mat$cell_state, levels = states)
mat$cl <- ifelse(uclass[as.character(mat$pathway_code)]=="CORE_ANTIOXIDANT","Core antioxidant / redox defense","Broader redox-linked signaling")
mat$cl <- factor(mat$cl, levels=c("Core antioxidant / redox defense","Broader redox-linked signaling"))

p_mat <- ggplot(mat, aes(x=xlab, y=plab)) +
  geom_tile(aes(fill=cell_state), color="white", linewidth=0.5) +
  scale_fill_manual(values=cols, labels=labs, guide=guide_legend(nrow=2, byrow=TRUE)) +
  facet_wrap(~cl, scales="free_y", ncol=1) +
  scale_x_discrete(position="top") +
  labs(x=NULL, y=NULL, fill="Evidence grade") +
  theme_minimal(base_size=11, base_family="sans") +
  theme(axis.text.x=element_text(angle=40,hjust=0,vjust=0.5,size=8,margin=margin(b=6)),
        axis.text.y=element_text(size=8), panel.grid=element_blank(),
        strip.text=element_text(face="bold",size=10), legend.position="bottom",
        legend.key=element_rect(colour="grey75"),
        legend.text=element_text(size=8), legend.title=element_text(size=8))

# right-margin: compounds with any evidence (incl. abstract) vs solid, per pathway
any_ev <- mat$cell_state %in% c("FUNCTIONAL","BODY_READOUT","ABSTRACT_ONLY","CELL_ONLY")
cnt <- data.frame(pathway_code=rep(U,2),
                  scope=rep(c("Any evidence (incl. abstract)","Solid only"), each=length(U)),
                  n=c(sapply(U, function(p) sum(any_ev & mat$pathway_code==p)),
                      sapply(U, function(p) sum(mat$solid_included=="YES" & mat$pathway_code==p))))
cnt$plab <- factor(ulab[cnt$pathway_code], levels=rev(ulab[U]))
cnt$cl <- ifelse(uclass[cnt$pathway_code]=="CORE_ANTIOXIDANT","Core antioxidant / redox defense","Broader redox-linked signaling")
cnt$cl <- factor(cnt$cl, levels=c("Core antioxidant / redox defense","Broader redox-linked signaling"))
cnt$scope <- factor(cnt$scope, levels=c("Any evidence (incl. abstract)","Solid only"))
p_cnt <- ggplot(cnt, aes(x=n, y=plab, fill=scope)) +
  geom_col(position=position_dodge(width=0.7), width=0.62, orientation="y") +
  geom_text(aes(label=n), position=position_dodge(width=0.7), hjust=-0.3, size=2.5) +
  facet_wrap(~cl, scales="free_y", ncol=1) +
  scale_fill_manual(values=c("Any evidence (incl. abstract)"="#fcae91","Solid only"="#08519c")) +
  scale_x_continuous(expand=expansion(add=c(0,1)), breaks=seq(0,length(comp_order),3)) +
  labs(x="Compounds per pathway", y=NULL, fill=NULL) +
  theme_minimal(base_size=10, base_family="sans") +
  theme(axis.text.y=element_blank(), panel.grid.major.y=element_blank(),
        strip.text=element_text(face="bold",size=10,colour="transparent"),
        legend.position="none")

p_C <- (p_mat | p_cnt) + plot_layout(widths=c(3.2,1)) +
  plot_annotation(
    title="Figure 1C  Antioxidant pathway evidence",
    subtitle=sprintf("%s  |  %d pathways x %d retained compounds", universe_label,length(U),length(comp_order)),
    caption=sprintf(paste0("%d full-text supported  |  %d abstract-level  |  %d cell-only  |  %d no qualifying report  |  %d pending\n",
                          "Coverage bars: dark blue = full-text supported; orange = all mapped evidence, including abstract and cell-only."),
                    n_solid,n_abs,n_cell,n_nr,n_pend),
    theme=theme(plot.title=element_text(face="bold",size=14),
                plot.subtitle=element_text(margin=margin(b=10)),
                plot.caption=element_text(size=8,hjust=0,colour="grey30"),
                plot.margin=margin(10,16,10,16)))

save_pair <- function(plot, path, w, h) {
  ggsave(paste0(path,".png"), plot, width=w, height=h, dpi=300, bg="white")
  svglite::svglite(paste0(path,".svg"), width=w, height=h, bg="white"); print(plot); dev.off()
  cat("saved", path, "\n")
}
save_pair(p_C, file.path(figdir,"figure1_C.pathway_framework"), 13, 9)

# Supplementary UpSet of full-text-supported pathway sets.
comp_set <- list()
for (c in comp_order) {
  sub <- mat[mat$compound==c & mat$solid_included=="YES", ]
  comp_set[[c]] <- sort(unique(sub$pathway_code))
}
keys <- sapply(comp_set, function(x) paste(x, collapse="+"))
ukey <- unique(keys[keys!=""])
inters <- lapply(ukey, function(k) { ps <- strsplit(k,"\\+")[[1]]; list(pathways=ps, size=sum(keys==k), compounds=comp_order[keys==k]) })
inters <- inters[order(-sapply(inters,function(x)x$size), sapply(inters,function(x)paste(x$pathways,collapse="+")))]
K <- length(inters)
setsize <- sapply(U, function(p) sum(sapply(comp_set, function(x) p %in% x)))
mx <- expand.grid(pathway_code=U, int_id=seq_len(K), stringsAsFactors=FALSE)
mx$present <- mapply(function(p,i) p %in% inters[[i]]$pathways, mx$pathway_code, mx$int_id)
display_U <- rev(U)
mx$y <- match(mx$pathway_code, display_U); mx$x <- mx$int_id
seg <- do.call(rbind, lapply(seq_len(K), function(i){ ys<-mx$y[mx$int_id==i & mx$present]; if(length(ys)>=2) data.frame(x=i,y=min(ys),yend=max(ys)) else NULL }))
size_df <- data.frame(int_id=seq_len(K), size=sapply(inters,function(x)x$size))
set_df <- data.frame(pathway_code=display_U, y=seq_along(display_U), n=unname(setsize[display_U]))
th <- theme_minimal(base_size=9, base_family="sans") + theme(panel.grid=element_blank(), axis.ticks=element_blank(), legend.position="none")
p_isize <- ggplot(size_df,aes(x=int_id,y=size))+geom_col(fill="#08519c",width=0.6)+geom_text(aes(label=size),vjust=-0.3,size=3)+
  scale_x_continuous(limits=c(0.5,K+0.5),expand=c(0,0))+scale_y_continuous(breaks=0:max(size_df$size),expand=expansion(mult=c(0,0.3)))+labs(y="Compounds")+th+
  theme(axis.title.x=element_blank(),axis.text.x=element_blank(),axis.line.y=element_line(color="grey60"))
p_matrix <- ggplot(mx,aes(x=x,y=y))+
  geom_segment(data=seg,aes(x=x,y=y,xend=x,yend=yend),color="#08519c",linewidth=0.7,inherit.aes=FALSE)+
  geom_point(aes(fill=present),shape=21,size=3.4,stroke=0.3,color="grey40")+
  scale_fill_manual(values=c("TRUE"="#08519c","FALSE"="#e8e8e8"))+
  scale_x_continuous(limits=c(0.5,K+0.5),breaks=seq_len(K),expand=c(0,0))+
  scale_y_continuous(limits=c(0.5,length(U)+0.5),expand=c(0,0),breaks=seq_along(U),labels=display_U)+
  labs(x="Intersection (shared pathway set)",y=NULL)+th+theme(axis.line.x=element_line(color="grey60"),axis.text.y=element_text(size=8))
p_sets <- ggplot(set_df,aes(x=n,y=y))+geom_col(fill="#6baed6",width=0.6,orientation="y")+geom_text(aes(label=n),hjust=-0.3,size=2.8)+
  scale_y_continuous(limits=c(0.5,length(U)+0.5),expand=c(0,0),breaks=seq_along(U),labels=ulab[display_U])+
  scale_x_continuous(expand=expansion(mult=c(0,0.2)))+labs(x="Set size",y=NULL)+th+theme(axis.text.y=element_text(size=7),axis.line.x=element_line(color="grey60"))
spacer <- ggplot()+theme_void()
p_upset <- (spacer+p_isize+p_sets+p_matrix)+plot_layout(design="AB\nCD",widths=c(2.6,3),heights=c(0.6,4))+
  plot_annotation(title="Supplementary - top-down UpSet of shared antioxidant pathways (solid evidence)",
                  subtitle=sprintf("%s  |  %d retained compounds  |  exact combinations of full-text-supported pathways",
                                   universe_label,length(comp_order)),
                  theme=theme(plot.title=element_text(face="bold",size=11),plot.subtitle=element_text(size=8)))
save_pair(p_upset, file.path(supp,"figure1_C_pathway_upset"), 12, 10)
cat("done\n")
