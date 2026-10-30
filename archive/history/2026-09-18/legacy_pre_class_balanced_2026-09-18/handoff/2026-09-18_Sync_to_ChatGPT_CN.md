# Phase 0–1 同步说明

## A. 本轮实际完成了什么

完成了中英文筛选 protocol、H/A/M/T/F/S 证据分级与建议分值、candidate universe 字段字典、compound–target 字段字典、context interaction 字段字典、中英文靶点规则、数据库与文献来源审计、中英文决策日志及本交接文件。完成内部方法审计并把 8 篇正式采用的核心方法学/数据库论文加入 Zotero `antioxidants project` collection。本轮没有生成候选名单、Top20 或批量靶点表。

## B. 最重要的 10 条科学决策

1. 全球膳食作为候选来源，暴露按地区和人群分层。
2. 一般成年人、膳食可达剂量是主转化基准。
3. 主榜仅含结构唯一的正常食物原型小分子；代谢物独立成 secondary layer。
4. 多酚优先生成但无类别配额。
5. direct antioxidant、redox regulatory、indirect redox-related 分层，间接机制必须有 redox endpoint。
6. 证据质量优先，独立 evidence family 数量饱和，低层证据不能越级。
7. Human efficacy 与 PK/bioavailability 分开，H5 不等价于获益。
8. T1/T2 才可能进入 direct layer，T2 仍需 directness QC；T3/T4/T5 分层输出。
9. 食物出现、定量含量、消费量和实际摄入分开；检出不等于有意义暴露。
10. 安全性与剂量窗口暂作独立风险维度；所有正式排名必须做权重与缺失数据敏感性分析。

## C. 最可能的 5 个偏倚或风险

1. 数据库和人类研究对热门多酚的研究密度偏倚仍可能影响证据完整度。
2. 全球膳食数据库在中国以外地区及低中收入国家覆盖不均，跨地区暴露可比性有限。
3. 食物含量受品种、加工、储存和分析方法影响，聚合值可能掩盖真实变异。
4. 多酚 assay 易受聚集、光学干扰、金属螯合、氧化共价和非特异结合影响，T1/T2 仍需专家复核。
5. 母体体外效应经常与人体结合代谢物暴露不匹配，若只用总 Cmax 可能高估转化性。

## D. 对原始框架的修改或补充及原因

增加 `evidence family` 防止一项试验多篇报告重复加分；把 H5 PK 与人体效应分离；把完整细胞 TPP/CETSA 设置为需要 directness qualifier 的 T2 候选，因为热稳定变化可能来自间接细胞状态；把食物域拆成含量、消费和估计摄入；为缺失状态建立四种编码；将安全性保留为独立二维风险而非早期总分；增加 betalain、quinone、含氮植物小分子等跨类别检查；增加 polyphenol assay interference 字段。上述修改用于控制重复计数、暴露错配和直接靶点假阳性。

## E. 仍需研究者/ChatGPT 决策

需要冻结：是否确认 25/25/20/15/15 为唯一主方案并接受三套替代权重；food exposure 五分项的精确权重和阈值；dose gap 使用总/游离/组织/代谢物暴露的规则；安全和冲突证据作为 penalty 还是二维矩阵；Top20 rank stability 合格标准；最低区域覆盖；是否预注册以及双人复核资源。建议在 Phase 2A 小规模试标后再锁定数值阈值。

## F. 下一阶段最合理的执行顺序

先冻结开放决策和机器可执行规则；Phase 2A 建立多酚候选并进行结构去重与食物证据审查；Phase 2B 用同一规则加入 carotenoids、tocopherols/tocotrienols、organosulfur compounds 和遗漏类别；Phase 2C 按候选盲法提取证据；Phase 2D 做缺失值、权重和名次稳定性；Phase 2E 形成 provisional Top20；Phase 3 用 EGCG 做完整 target pilot，复核后再扩展。

## G. 是否已具备建立 candidate universe 的条件

有条件具备。实体资格、结构标准化、来源优先级、去重、暴露状态、代谢物分层和审计字段均已定义。开始前只需研究者审核开放决策；候选生成本身可先执行而不进行正式评分。

## H. 是否建议修改 25/25/20/15/15

暂不建议直接修改主权重。它合理地保持人体/生物 redox 证据优先，同时不排斥机制和靶点。建议把它作为预注册主分析，并用人体优先 35/25/20/10/10、暴露平衡 25/20/30/15/10、实验转化优先 20/20/15/20/25 做敏感性分析。需要特别监测 Human 与 Antioxidant 两域对同一人体试验的重复奖励；实现时分别评分“研究设计/人体相关性”和“redox endpoint 质量”，并做去重敏感性分析。

## I. 新的重要数据库或方法学论文

新增/强调 Exposome-Explorer（人体饮食 biomarker 和肠菌代谢物）、EFSA Comprehensive Food Consumption Database/FoodEx2（区域暴露）、ChEBI 2.0（2025 后 REST 与月度产品）、GtoPdb 2026.3、BindingDB 2026-09 bulk、ROBINS-I V2（2025-11）、Murphy et al. 2022 redox measurement guideline、Mateus et al. 2022 TPP 综述以及 SynergyFinder 3.0。另确认 DrugBank academic bulk 当前暂停，不能作为必要依赖。

## J. Zotero 本轮实际新增的核心文献

collection：`antioxidants project`。新增 8 条：

| 文献 | DOI | Zotero item key | BibTeX key |
|---|---|---|---|
| Murphy et al., ROS/oxidative damage guidelines (2022) | 10.1038/s42255-022-00591-z | QHGVX2E5 | murphy_guidelines_2022 |
| Rethlefsen et al., PRISMA-S (2021) | 10.1186/s13643-020-01542-z | H6H4RHLK | rethlefsen_prisma_s_2021 |
| Mateus et al., tissue TPP review (2022) | 10.1146/annurev-pharmtox-052120-013205 | APZ5KUE2 | mateus_tpp_2022 |
| Franken et al., TPP protocol (2015) | 10.1038/nprot.2015.101 | GDXLSHA6 | franken_tpp_2015 |
| Ianevski et al., SynergyFinder 3.0 (2022) | 10.1093/nar/gkac382 | DAAES5RM | ianevski_synergyfinder_2022 |
| Rothwell et al., Phenol-Explorer 3.0 (2013) | 10.1093/database/bat070 | NXGQC4EI | rothwell_phenolexplorer_2013 |
| Daina et al., SwissTargetPrediction (2019) | 10.1093/nar/gkz382 | H8IEDHD8 | daina_swisstargetprediction_2019 |
| Kim et al., PubChem 2025 update | 10.1093/nar/gkae1059 | QL33FQ4U | kim_pubchem_2025 |

注意：Zotero item key 与 BibTeX key 是两种不同标识。上述记录通过 Zotero connector 导入当前选中的 collection；未把所有搜索结果无差别保存。

## 审核结论

Phase 0–1 已达到“可提交审核”的停止条件。建议研究者先审阅 protocol、评分表、决策日志和本文件，对 E 节问题作出冻结决定；在此之前不要运行正式 Top20 排名。
