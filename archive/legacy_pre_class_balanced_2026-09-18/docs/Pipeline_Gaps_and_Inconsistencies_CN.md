# Pipeline Gaps and Inconsistencies Audit

已完全可复现的部分：在给定结构化record和硬编码来源的前提下，现有脚本可重建pilot、exploratory图、50项candidate表、provisional ranking、consolidation before/after、confidence图和shortlist。单位公式、median/range、排名方向和输出文件均可检查。

依赖人工判断的部分：文献检索完整性、ORAC构念识别、H/L分臂、化合物form、光学/溶解干扰、A/B1/B2/C/X、独立性和outlier解释。当前没有自动化全文解析，也不应把这些判断完全自动化。

冲突与最新冻结解释：v2.0的A/B/C/X被v2.1的A/B1/B2/C/X补充替代；旧`ORAC_Literature_Eligibility_Rubric.csv`仍以`Tier_B_requirement`单列B，未结构化拆成B1/B2，执行时以v2.1为准。早期Candidate Scope覆盖H/L和非酚类；当前MASTER仅适用H-arm phenolic/polyphenolic。`H_ORAC_Provisional_Ranking.csv`是consolidation前版本；当前结果见`Top20_Ranking_Before_After.csv`，旧文件不得覆盖。High confidence的科学定义包含“≥3且低/中等异质性”，但当前`build_top20_consolidation.py`实现按n≥3直接赋High，尚未把异质性降级自动写入confidence；正式发布须人工复核，这是最重要的未自动化差异。

结构化不足：部分早期记录的exact location、purity、linearity、optical QC和完整assay参数缺失；consolidation文件的新增记录使用概括性exact location，未全部保存页码/表号的PDF证据副本。检索日志、exclusion log、reviewer initials和第二复核签名此前不完整。本次创建空白模板但没有回填历史全过程，因为本轮禁止自动重分类旧记录。

脚本缺失：没有通用的模板验证器、CSV schema validator、独立性重复报警、文件哈希/run manifest、通用聚合CLI或自动版本归档。现有构建脚本硬编码候选与文献，不能直接用于新项目。

Zotero缺口：本地API此前不可用；Tabart 2009、Zhang 2013、Rothe 2023、Sakurai 2022、Ishimoto 2012和Paillat 2023等存在`pending_local_import`，未取得真实item key。不能将pending当已入库。

未来需要补充：结构化B1/B2 rubric；明确heterogeneity阈值或只保留人工判定；anthocyanin optical QC最低标准；cyclodextrin/共溶剂桥接规则；通用脚本schema；完整历史search/exclusion日志；Zotero回填；原文文件哈希和受控存档。

无AI执行的最大困难是从二手综述追到原始实验并正确辨认probe/arm，以及判断相似数值是否来自同一数据集。其次是有色、低溶解度化合物的干扰判断。这些需要训练、双人复核和可访问全文，不应由简单脚本替代。
