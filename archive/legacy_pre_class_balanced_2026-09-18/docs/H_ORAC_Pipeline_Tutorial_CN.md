# H-ORAC Pipeline 教学版

先理解问题：我们比较的是试管中纯酚类分子对AAPH产生的过氧自由基保护fluorescein的能力，不是人体疗效。第一天先建立候选表，不看谁的ORAC高；第二天开始逐个检索并留下搜索日志。看到“ORAC”不能立即抄数值，必须打开方法确认AAPH、fluorescein、Trolox、H-arm和纯单体。

案例1 quercetin：它有多项独立B1。每项原值分别成行并有experiment ID，去重后取median；研究数量和异质性决定confidence，再按median进入排名。不能取16.62这一最大值代表quercetin。

案例2 EGCG：早期搜索同时出现β-phycoerythrin、HORAC、L-ORAC和只有图形的结果。这些不能成为H-ORAC-FL B1。继续沿参考文献追到使用AAPH–fluorescein–Trolox且报告精确数值的原始研究后，才形成合格记录。缺数据期间不能写“EGCG能力低”。

案例3 cyanidin-3-O-glucoside：原文可以有精确数值，但它是有色分子；若未处理inner-filter、光谱重叠、自发荧光、quenching和pH结构转化，仍只能B2，不进入主排名。

案例4 secoisolariciresinol：没有可用膳食parent lignan ORAC-FL时，记录“检索完成、未找到”，不可用人体代谢物enterodiol或enterolactone替代。Missing不是零，也不是低活性。

做完抽取后，第二个人复核身份、原值、单位、tier和独立性。Excel按compound筛选A/B1，计算MEDIAN、MIN、MAX和COUNT；n≥4再报告IQR。排序后检查benchmark未占名额，再做consolidation和before/after。最后按Ready、Conditionally ready、Not ready分层，至此停止并交接下游。
