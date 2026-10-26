# Batch A三项定点来源补核

日期2026-10-26。基线分支codex/phase1c-aff0061-batch-a-review、提交48b34a7314b1d5914c4bb70f770e7e6d2fe939fe已与远端核对；起始工作区干净。新分支codex/phase1c-aff0061-batch-a-targeted-followup，仅新增本目录。依据已批准Governance v0.2，原记录、既有审核材料和治理规则不回写。此次新增检索仅覆盖HDAC1计算、p-eNOS归一化和两条Kmo观察；其余A组条目显式沿用既有建议，不冒称重新读过全部论文。

三项结论是“来源部分恢复，关键推断仍未闭合”：HDAC1与Kmo补充资料现已合法取得；HDAC1能量单位和结构参数未解决；p-eNOS完整计算算法未解决；DRA014580现有可定位的样本/实验/run元数据，但不能确定生物重复或与qPCR的复用。没有下载FASTQ、计数矩阵或执行RNA-seq重分析，没有联络作者或发送外部消息。

所有来源文件及失败响应本地忽略不入Git。qc/Targeted_Access_Log.json、qc/Metadata_and_Alternative_Access_Log.json、qc/Kmo_Final_Access_Log.json记录实际URL、访问结果、内容类型与SHA256；qc/Followup_Source_Manifest.json区分有效来源、失败响应、DDBJ网页应用壳与已读旧来源。HTTP200不等于有效补充文件。MDPI/Wiley直达尝试遇403，PMC部分附件返回HTML；Europe PMC公开supplementaryFiles接口取得有效ZIP，不绕过访问控制。

## A1：HDAC1 docking/MD，ME-AFF0061-41594941-004

重新核对既有原始XML、Methods2.14–2.16、Results3.6及Fig6原图：[论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12837532/)，DOI10.3390/biology15020206。正文MM-PBSA结果写-12.21 kJ/mol，Fig6G纵轴写Energy(kcal/mol)；不能按数值相同推定单位相同，也不能从通常软件单位推定哪一处正确。两种标签作为来源冲突分别保留，规范化MM-PBSA数值和单位不赋值，不换算、不用来作跨研究能量或亲和比较。Fig6A约-5.6 kcal/mol是独立的作者docking score，不能拿它替换冲突的MM-PBSA量值或当实验自由能/Kd。

可定位参数为：配体三维结构来自PubChem，HDAC1结构称来自PDB；AutoDock Tools1.5.6、AutoDock Vina1.2.3，Gromacs2022、AMBER ff14SB/TIP3P，十二面体溶剂盒，蛋白至盒边最小距离1.2nm，steepest-descent最小化阈值1000 kJ·mol^-1·nm^-1；Fig6B–D时间轴0–100ns，MM-PBSA使用末20ns。参数仅按作者报告归档，不称复现或验证。

结构PDB编号、链/版本、蛋白物种、构建体、金属保留与配位模型、配体质子化/电荷/拓扑等未从相关来源恢复。正文“each trajectory”不等于独立重复数已给，单条体系曲线不证明没有重复，也不证明有重复；apo/已知配体对照、随机种子、重复轨迹及收敛误差分析均待补。不得根据HUVEC物种、HDAC1名称、图中残基或引用论文反推本研究实际采用的模板和金属参数。

本轮通过[Europe PMC补充接口](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12837532/supplementaryFiles)取得外层ZIP，内含biology-15-00206-s001.zip；其唯一文件为“File S1 Full-length, uncropped Western Blots.pdf”，7页。已检查完整成员清单和逐页文本标签，视觉核对PDF第2页Fig4I；其余页未进行科学评估，未展开B组记录。附件没有结构文件、MD参数文件或能量单位更正。因此“补充资料未取得”在新报告中更新为“附件已取得但不解决计算问题”，原Batch A文件保留原时点记录。

PDF第2页同时展示HDAC1/GATA4及各自标注的GAPDH原图，只更新两个A组丰度行的来源可用性。它不构成图像真实性、逐样本配对或生物重复认证；不因拿到blot就接受计算结合。允许定性描述作者预测的pose/接触及所画轨迹；必须暂缓MM-PBSA量值比较、强亲和、自发结合、充分收敛、具体物种结构和实验结合结论。三维分类仍建议COMPUTATIONAL_PREDICTION / COMPUTATIONAL_ONLY / OTHER_BIOLOGICAL_FUNCTION；本轮候选为SOURCE_PENDING_CANDIDATE，表示需补来源，不修改正式状态。

## A2：p-eNOS，ME-AFF0061-37025617-001

核对既有PMC XML及Fig4原图，并重新读取[Frontiers原文](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2023.1060226/full)，Methods2.4/2.7/2.9、Results3.4和Fig4B/D图注。Fig4B明确为p-eNOS/eNOS，Fig4D同时列p-eNOS Ser1177、总eNOS和GAPDH。主要比较为IL-1β背景下PCA100nM vs IL-1β单独组；保留作者报告的比值恢复方向和图注阈值，不从柱图提取新数值。

Methods2.7说明电泳、转膜、BSA封闭、抗体和ChemiDoc化学发光检测，但未给densitometry软件、背景扣除、条带配对、具体分子分母、GAPDH进入公式的位置或CTL缩放方式。全文检索densitometry相关词并核对方法，未取得足以确认完整算法的说明。总图注仍写p-eNOS/eNOS等蛋白量relative to GAPDH，不能忽略，也不能自行解释为比值再次除GAPDH。总eNOS及GAPDH条带可见只说明有这些读数，不揭示实际计算流水线；不能用数学上可行的某种公式冒充作者采用的公式。

结论：完整公式UNRESOLVED。保留原始assay/endpoint及图注，补充“作者报告比值、算法待明”；不补算、不从图像测量条带。n=6–7的生物/技术单位及overnight精确小时仍未解决。可保留PATHWAY_MODULATION / READOUT_ONLY / INDIRECT_OXIDATIVE_STRESS_ASSOCIATION建议，但应修订任何“精确归一化算法已核实”陈述。候选为REVISION_REQUIRED_CANDIDATE；精确效应量和公式定量用途待作者或原始densitometry澄清。未审核B组Akt阻断、未将其他DHE终点搬入本行。

## A3：Kmo，ME-AFF0061-37482908-001与002

重新核对[论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10424289/)，Methods2.2/2.5/2.11/2.15、Table1、Results3.4、Fig4A/C及Fig5D原图。动物设计每组n=8并不自动成为RNA-seq或qPCR每图生物重复数。Fig4为全局谱，图例显示raw p阈值；正文为fold change>2与显著p筛选及候选方向，没有可定位的Kmo特异fold change、raw p和校正p。未由qPCR反算RNA-seq，也未把通用ANOVA/Bonferroni说明当作RNA-seq FDR证据。

通过[Europe PMC补充接口](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10424289/supplementaryFiles)取得有效ZIP，检查全部成员：主图JPEG/GIF、S1–S5 TIFF、Data S1（JCMM-27-2290-s006.doc），无独立DEG/计数表成员。以禁用宏的独立隐藏Word实例只读提取Data S1全文，未保存或修改来源文档；该文档是作者信息与S1–S5图注，没有Kmo基因级差异结果表，也未说明本行RNA-seq/qPCR的个体ID、重复或复用。S1–S5 TIFF没有逐图开展新的科学评估；不能把取得文件等同已核完所有图或原始数据。

Fig5D明确为Kmo mRNA/Gapdh，方法给2^(-ΔΔCt)及mouse引物；ISO+PCA vs ISO标###p<0.001，无ISO时PCA vs vehicle标NS。可保留阈值，不填精确p、精确FC或等效结论。图上散点数量不是已确认独立动物数；Data S1中其他细胞实验的n=6不能搬到本行。RNA-seq与qPCR是否同批动物、同份RNA或独立验证队列仍UNRESOLVED_REUSE，不把两检测计作两项独立研究。

### DRA014580元数据：已解决可定位性，未解决生物独立性

DDBJ网页响应是JavaScript应用壳，不能当作已读记录详情。实际可读记录由ENA的INSDC镜像API取得：[DRA014580 submission](https://www.ebi.ac.uk/ena/browser/api/xml/DRA014580)、[PRJDB14081 project](https://www.ebi.ac.uk/ena/browser/api/xml/PRJDB14081)以及各样本/实验XML；DRP011843映射同一项目。DRA014580与PRJDB14081两个run查询均返回同一3条记录。项目描述中的三组、ISO80mg/kg/day和PCA肌内9天与论文相符，支持存档关联，不等于证实原始设计完整。

| 组别 | BioSample | Experiment | Run |
| --- | --- | --- | --- |
| sham | SAMD00517030 | DRX381960 | DRR396181 |
| ISO | SAMD00517031 | DRX381959 | DRR396180 |
| ISO+PCA | SAMD00517032 | DRX381958 | DRR396179 |

3个样本均标Mus musculus、male、heart、C57BL/6、9 weeks；不据粗粒度strain覆盖论文C57BL/6NTac。实验为RNA-Seq、paired、Illumina NovaSeq6000，设计说明空白，样本属性未给pooling、biological replicate或individual animal ID，也无qPCR对应键。每组1个存档样本/实验/run不能推出每组1只动物、未混样、三份彼此独立生物重复或qPCR独立验证。元数据里的库构建指针与测序读段字段不构成对实际序列质量的验证，本轮未读FASTQ。

RNA-seq行候选SOURCE_PENDING_CANDIDATE：需DEG表/统计方法与样本设计才能作正式统计支持。qPCR行候选ACCEPT_PROPOSAL_CANDIDATE仅限已定位的转录响应方向与图注阈值，样本n、精确p及复用问题仍开放，不是批准。本轮不重跑RNA-seq。若作者无现成结果，未来需单独授权：先确认混样和生物重复是否支持分析，再制定参考基因组、计数、对比和多重检验方案；原始数据再分析不能补救未记录的生物重复或自动复现原p值。

## 9条裁决建议及适用范围

candidate不是正式decision，也不保证未来接受。ACCEPT表示可将已有、明确限制的建议送交人工；REVISION_REQUIRED表示先收窄文字/用途；SOURCE_PENDING表示关键来源仍阻断当前推断。非定点行只沿用Batch A，不宣称本轮重新解决其全部问题。三维分类没有改变，所有human_review_status=NOT_REVIEWED、change_applied=NO，审核人/决定/批准日期留空。

| evidence_id | Codex候选建议 |
| --- | --- |
| ME-AFF0061-37482908-001 | SOURCE_PENDING_CANDIDATE |
| ME-AFF0061-37482908-002 | ACCEPT_PROPOSAL_CANDIDATE |
| ME-AFF0061-39589556-002 | ACCEPT_PROPOSAL_CANDIDATE |
| ME-AFF0061-41594941-001 | ACCEPT_PROPOSAL_CANDIDATE |
| ME-AFF0061-41594941-002 | ACCEPT_PROPOSAL_CANDIDATE |
| ME-AFF0061-41594941-003 | REVISION_REQUIRED_CANDIDATE |
| ME-AFF0061-41594941-004 | SOURCE_PENDING_CANDIDATE |
| ME-AFF0061-42170612-002 | REVISION_REQUIRED_CANDIDATE |
| ME-AFF0061-37025617-001 | REVISION_REQUIRED_CANDIDATE |

15项剩余不确定性在独立CSV登记，带来源、用途限制及所需补证，含已部分解决和未重新审核的继承项。不解除既有7条HOLD，不应用257项历史提案，不处理B/C组、生产迁移或H-ORAC冻结排名。技术QC与Git归档不构成人工科学批准。
