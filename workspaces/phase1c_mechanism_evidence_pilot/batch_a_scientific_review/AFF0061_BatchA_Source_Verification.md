# AFF-0061 A组来源核查

核查日期2026-10-23，来源基准提交8177aebfa22d68945254ee836ec662985e5da265。仅针对A组9条观察、5篇论文核查相关方法、结果、图注和图像。原始XML为既有本地缓存；本轮另外取得5份公开PMC HTML及7张相关主图。浏览工具初访PMC遇验证码，但普通公开HTTP请求取得有效正文与图像；未绕过验证码、付费墙或身份限制。3个补充附件链接返回HTTP200的HTML而不是目标文件，均判定未取得，不能以200当作全文/附件成功。

`qc/Reviewed_Source_Manifest.json`逐文件记录路径、SHA256、用途与LOCAL_ONLY_EXCLUDED。访问结果见`qc/Source_Access_Log.json`和`qc/Supplement_Access_Log.json`；原文、图像、PDF及依赖缓存均不提交Git。重取网页内容/哈希不保证与旧缓存字节一致，结论绑定具体文件。相关图像核查指阅读已发表面板、轴标、比较与图注，不包含图像操纵鉴定、原始blot质量认证或数据再分析。未从柱图估算效应量或把图上点数当已确认实验单位。

本轮检索了四篇DOI的更正/撤稿关键词，未得到足以确认更正或撤稿的结果；Frontiers原文亦重新访问。但未完成五篇论文逐一PubMed/Crossmark完整通知关联复核，故原`publication_status`只作为历史值保留，本轮不写“截至今日无撤稿”。采用范围内原始论文而非其他期刊综述替代实际实验。

## PMID37482908：Kmo RNA-seq与qPCR

[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10424289/)，DOI10.1111/jcmm.17869，本地`../search_logs/raw/PMC10424289.xml`。本轮读Methods2.1/2.2/2.5/2.11、Table1、Results3.4，视觉核对Fig4、Fig5（两行分别定位Fig4A/C、Fig5D）。Methods明确PCA100 mg/kg/day肌内给药，ISO第6天开始9天，ISO80 mg/kg/day泵入14天；RNA-seq为sham/ISO/ISO+PCA三组的全心室组织。原文动物设计每组n=8不能直接作为RNA-seq或qPCR每图n。

Results3.4明确Kmo为ISO提高、PCA降低的候选之一；Fig4是全局热图和火山图，不提供可直接提取的Kmo特异统计。正文采用fold change>2及显著p，Fig4C图例显示raw p，未核得Kmo特异校正p、效应量和逐样本设计。DDBJ DRA014580指针已见，未下载原始测序或重新运行差异分析。Fig5D轴为Kmo mRNA/Gapdh，方法给2^(-ΔΔCt)，Table1含小鼠Kmo/Gapdh引物；主要ISO+PCA vs ISO比较标###p<0.001，无ISO两组标NS。未把NS写成零效应或等效。未取得/阅读补充S1–S5 TIFF和DataS1文档；同文Fig8 DHE不迁移为这两行的红氧终点。Kmo-specific FDR和RNA-seq/qPCR样本是否复用仍未决。

## PMID39589556：氧化应激相关富集

[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC11599353/)，DOI10.1007/s10565-024-09953-7，本地`../search_logs/raw/PMC11599353.xml`。读Reagents、Cell culture、RNA sequencing及对应结果，视觉核对Fig2。5µM PCA、16h，MHCC97-H与未处理细胞比较；不是PA诱导脂毒条件，也不将PCA与同文palmitic acid的PA混同。Fig2A标padj，Fig2D包含氧水平、氧化应激及ROS相关术语；富集没有给出这些过程整体激活/抑制方向。

复用既有`../gate2_review/sources/NRF2_Supplement.pdf`，49页，SHA256见清单。做页级文本检索和表定位；视觉核对PDF第14、17页（Supplementary Table5起于14页，表延续至37页）。第14页可见GO:0070482、Reactome R-HSA-211859、总库基因30293、命中列表1644及Log(q-value)列；第17页可见GO:0006979、GO:2000377，表中分别列LogP=-4.7及Log(q-value)=-2.8等作者输出。不将取整后的对数值换算成新精确p/q值，也未重新验证其计算。

因此Gate2旧未决项“术语ID、背景基因集、校正值”已部分恢复，不再笼统称这些完全缺失；仍缺完整可复现基因映射、实际测序重复、阈值/算法版本及库选择理由。正文612上调+1188下调与表中1644命中数差异未获得映射说明。表5是混合数据库集合，不是单一NRF2蛋白或全部单一GO词表；不是所有列出的术语都已被本轮确认达到某预设FDR。未视觉审核全部49页，未复核B组动物因果、S2救援或M/N标签争议，也未读取原始测序文件。

## PMID41594941：HUVEC读数与HDAC1计算

[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12837532/)，DOI10.3390/biology15020206，本地`../search_logs/raw/PMC12837532.xml`。读Methods2.1/2.8–2.11/2.14–2.16、Results3.4/3.6，视觉核对Fig4、Fig6。Fig4I/J中HDAC1与GATA4分别以GAPDH作比值，100µM/24h PCA在1µM AngII预处理24h后给药；AngII对照在第二阶段更换正常培养液。Fig4E为p65/DAPI定位图，未见专门核/胞质比值定量。图注n=3，未确定生物与技术重复单位。

两项报告差异必须保留：Methods2.8称6组却只编号列出5组，与Fig4五列相对照，不能补造第六组；Results3.6 MM-PBSA写-12.21 kJ/mol，Fig6G纵轴写Energy(kcal/mol)，不能按数值相同擅自选单位或换算。Fig4B/Results3.4的500µM细胞毒性属于不同剂量背景，不能据此宣称100µM不利，也不能宣称所有浓度安全。Fig4J不支持全部剂量均显著；本轮只保留原行100µM。

HDAC1计算方法给AutoDock Vina1.2.3、Gromacs2022、ff14SB/TIP3P与末20ns MM-PBSA；Fig6时间轴0–100ns。相关正文未恢复具体PDB ID、物种/构建体、apo/已知配体/独立轨迹对照及完整配体/金属参数。Fig4K CoIP为HDAC1–GATA4蛋白互作，不是PCA结合。补充ZIP链接返回HTML，未取得附件、未读未裁切blot或原始轨迹。本轮不处理该文B组非加和观察。

## PMID42170612：TAS2R16模拟

[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13187579/)，DOI10.1016/j.crfs.2026.101435，本地`../search_logs/raw/PMC13187579.xml`。读Materials、Methods2.8.5、hTAS2R16相关结果与Table4，视觉核对Fig6。Desmond、OPLS4/SPCE、0.15mol/L盐、300K/1bar和100ns可定位；Table4十受体docking筛选是MD对象选择背景，不是十项功能实验。

Fig6A配体RMSD中途出现明显偏移；正文称70ns后相对稳定。单条轨迹末段趋稳不等于完成收敛、测得亲和常数或证明受体激活。受体具体模型模板/版本、膜环境设置及重复轨迹未恢复；hTAS2R16命名及既有Q9NYV7参考映射不替代计算模型身份。补充mmc1.docx链接返回HTML，未取得/读取其内容。未审核同论文C组α-amylase来源HOLD；PDB1JXJ不能作为TAS2R16结构，更不能把amylase实验结合移到受体模拟行。

## PMID37025617：p-eNOS归一化

[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10070727/)，[出版社原文](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2023.1060226/full)，DOI10.3389/fnut.2023.1060226，本地`../search_logs/raw/PMC10070727.xml`。读Methods2.4/2.7/2.8、Results3.4及Fig4B/D，原图已视觉核对。mBMEC、PCA100nM、IL-1β0.5ng/mL overnight；方法为共孵育描述，精确小时不填。抗体p-eNOS Ser1177与总eNOS可定位。

Fig4B轴为p-eNOS/eNOS，显著比较包括CTL vs IL-1β和IL-1β vs 100nM PCA；1/10nM未标相应显著，不能据此判无效。Fig4D有总eNOS和GAPDH条带，总图注又称各蛋白量relative to GAPDH。建议保留比值读数和该算法歧义，不能自造“再除一次GAPDH”；需作者或原始densitometry说明。图注n=6–7，实验单位未核。Supplementary Image2链接未取到图像，未独立核查Thr308叙述；Fig3 DHE不作为本行直接redox终点。未扩大到B组Akt阻断观察。
