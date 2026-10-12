# Stage25B.6B 误差回查

68 条 A/B1 记录中，明确 SD/SE/CI 类型 3/68；原文有数值 ± 但类型未明者 23 条；任意误差信息 26/68。新增的 7 条来自 [Skroza 2022 原文 Table 2 / Methods 2.2.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/)：每个化合物在 2.5 和 5 µM 两列各有一个 ± 值，Methods 写 3 replicates，但未定义 ± 是 SD 还是 SE。另 13 条来自 [Žuvela 2019 原文 Table 3 / Methods 3.3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/)的 `ln(ORAC) ±`，不能直接作为 mol TE/mol 尺度的 SD。两文重复类型均未证实为独立研究。Carvalho 2023 Table 3 的 3 个 ± 值仍为 `UNSPECIFIED_PLUS_MINUS`。其余未报告的误差保持缺失，不置零。独立实验次数、95%CI 均未取得足以可靠推断的数据。逐条见 `Stage25B6B_Error_Recovery_Master.csv`。
