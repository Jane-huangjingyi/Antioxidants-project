# 主抗氧化能力指标建议

建议有条件采用 ORAC-FL 作为本项目唯一的 primary chemical antioxidant capacity metric。准确含义是：结构明确单体在锁定实验条件下，对 AAPH 衍生过氧自由基引起的 fluorescein 氧化的竞争性、动力学积分链终止能力；纯单体用 `mol Trolox equivalents/mol compound` 表示。该指标只描述特定化学反应体系，不代表人体抗氧化作用、健康获益、吸收、生物利用度或细胞 redox regulation。

选择 ORAC-FL 的理由是其 peroxyl-radical chain-breaking 机制比人工持久自由基脱色或单纯金属还原更接近传播链终止；完整动力学曲线和 net AUC 同时捕捉抑制强度与持续时间；Trolox 校准支持纯单体摩尔归一化；H-ORAC 和已有实验室间验证的 L-ORAC 可覆盖亲水和脂溶化合物。文献数量不是选择依据。

该推荐有严格限制。不同论文 ORAC 值不得直接拼接；H-ORAC 与 L-ORAC 不得默认视为同一数值尺度。主排序应优先来自同一实验室、同一锁定 SOP 的复测数据。只有化合物形式、纯度、AAPH/fluorescein/Trolox、buffer/pH、温度、溶剂/RMCD、浓度线性、读取时间、AUC 公式和 QC 全部等价，并由共同 bridging standards 验证实验室偏差后，外部值才可合并。

DPPH 不作为主指标，因为其非生理持久自由基、立体可接近性、溶剂和反应时间会显著改变排序。ABTS•+ 同样是人工自由基且生成方式、pH、溶剂和 endpoint 不统一。FRAP 只测酸性条件下 ferric reducing power，不测 radical chain-breaking。CUPRAC 是较好的近中性 ET 补充，但仍是 reducing power。TRAP 机制相关性高，但检测格式和计算缺乏统一，不适合大规模主排序。

正式结构为：ORAC-FL 为 primary；CUPRAC、ABTS、DPPH、FRAP、TRAP 和预设 lipid-peroxidation model 为 secondary；HORAC、TOSC、superoxide/hydroxyl/metal-chelation assays 为 supportive。不同 assay 不做默认 z-score 加权或简单平均。没有 ORAC 数据的候选标记 `not_measured` 并进入补测队列，不计零分、不排除；其他证据继续保留。下一阶段若获批准，应先冻结 ORAC-FL SOP 和 QC 标准，再开展统一实验测定，而不是立即汇总异质文献数值。
