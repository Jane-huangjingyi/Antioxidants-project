# ============================================================
# Figure: Four aqueous Atlas overview figures
# Scientific question: What is the current class ranking, coverage, provenance, and metal-redox framework?
# Project: Antioxidants Project
# Stage: 23–24 / modularized 25A.1
# Input data: supervisor overview, aqueous candidate master, paper summary
# Required columns: panel ranks/percentiles/confidence; candidate panels; paper roles
# Filtering: rankable top five per panel where applicable
# Transformation: counts and within-panel display only
# Statistical / ranking definition: frozen class-specific outputs; no global score
# Output: four overview PNG files
# Scientific interpretation: project coverage and class-specific position
# Major caveat: within-panel percentiles do not form a global antioxidant scale
# User-editable settings: dimensions, DPI, fonts, point/bar/label sizes, class colors
# ============================================================
source(file.path("R","common","bootstrap.R"));out<-file.path(project_root(),"figures","aqueous_antioxidant_atlas","00_overview")
o<-read_project_csv("data","supervisor","Supervisor_Aqueous_Class_Ranking_Overview.csv");c<-read_project_csv("data","candidate_universe","Aqueous_Antioxidant_Candidate_Master.csv");pa<-read_project_csv("data","class_specific_antioxidant","Aqueous_Antioxidant_Paper_Summary.csv")
d1<-o%>%filter(!is.na(within_class_percentile),within_class_rank<=5)%>%mutate(compound=factor(compound,levels=rev(unique(compound[order(analysis_subpanel,within_class_rank)]))))
p1<-ggplot(d1,aes(within_class_percentile,compound,color=confidence))+geom_point(size=POINT_SIZE)+facet_wrap(~analysis_subpanel,scales="free_y",ncol=2)+scale_color_manual(values=CONFIDENCE_COLORS)+scale_x_continuous(limits=c(0,100))+theme_atlas+labs(title="Aqueous class-specific ranking overview",subtitle="Top five per rankable panel; no global score",x="Within-panel percentile",y=NULL,color="Confidence")
cov<-c%>%count(analysis_panel,name="candidate_N")%>%left_join(o%>%group_by(analysis_panel)%>%summarise(rankable_N=max(rankable_N),displayed_N=n(),.groups="drop"),by="analysis_panel")%>%mutate(rankable_N=replace_na(rankable_N,0),displayed_N=replace_na(displayed_N,0))%>%pivot_longer(c(candidate_N,rankable_N,displayed_N),names_to="measure",values_to="N")
p2<-ggplot(cov,aes(N,fct_reorder(analysis_panel,N,.fun=max),fill=measure))+geom_col(position="dodge",width=BAR_WIDTH)+theme_atlas+labs(title="Aqueous class coverage overview",subtitle="Frozen universe: 157 candidates",x="Count",y=NULL,fill="Coverage")
pc<-pa%>%count(class_coverage,primary_or_supporting,name="papers")
p3<-ggplot(pc,aes(papers,fct_reorder(class_coverage,papers,.fun=sum),fill=primary_or_supporting))+geom_col(width=BAR_WIDTH)+theme_atlas+labs(title="Aqueous primary-literature coverage",subtitle="Paper count documents provenance; it is not antioxidant strength",x="Original-paper units",y=NULL,fill="Paper role")
nodes<-tibble(label=c("Aqueous small molecule","Direct radical scavenging","Fe/Cu chelation","Fe/Cu-mediated ROS suppression","Micronutrient","Antioxidant-enzyme cofactor","GPX / TXNRD / SOD","Excess Fe/Cu","Prooxidant / Fenton chemistry"),x=c(1,3,3,5,1,3,5,1,3),y=c(3.5,4.4,2.7,2.7,1.5,1.5,1.5,.3,.3),type=c("small molecule","outcome","metal mechanism","outcome","micronutrient","cofactor","enzyme","excess metal","prooxidant"));edges<-tibble(x=c(1.5,1.5,3.5,1.5,3.5,1.5),y=c(3.5,3.5,2.7,1.5,1.5,.3),xend=c(2.5,2.5,4.5,2.5,4.5,2.5),yend=c(4.4,2.7,2.7,1.5,1.5,.3))
p4<-ggplot()+geom_segment(data=edges,aes(x=x,y=y,xend=xend,yend=yend),color="#777777",arrow=arrow(length=unit(.15,"inches")))+geom_point(data=nodes,aes(x=x,y=y,color=type),size=7)+geom_text(data=nodes,aes(x=x,y=y,label=label),nudge_y=-.28,size=LABEL_SIZE,fontface="bold")+coord_cartesian(xlim=c(.5,5.5),ylim=c(-.1,4.9),clip="off")+theme_void()+theme(legend.position="none",plot.title=element_text(size=TITLE_SIZE,face="bold"))+labs(title="Metal-dependent redox mechanisms in the aqueous Atlas",subtitle="Small-molecule chelation and micronutrient cofactor biology remain distinct")
save_figure(p1,file.path(out,"Aqueous_All_Classes_Ranking_Overview.png"),14,12);save_figure(p2,file.path(out,"Aqueous_Class_Coverage_Overview.png"),14,8);save_figure(p3,file.path(out,"Aqueous_Primary_Literature_Coverage.png"),14,8);save_figure(p4,file.path(out,"Aqueous_Metal_Redox_Framework.png"),12,6.5)
