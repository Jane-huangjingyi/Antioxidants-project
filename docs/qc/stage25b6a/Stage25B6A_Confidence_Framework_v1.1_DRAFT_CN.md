# Confidence Framework v1.1 DRAFT

现行 Stage25B v2.0 将 eligibility、A/B1/B2 及 High/Moderate/Low 分开，但现有 confidence 未系统纳入经核实的独立研究数量、实验精度覆盖及排名不确定性。本草案不改变 canonical rubric 或 Frozen Top20 v1.0。

拟议框架先保留五个独立判断：**eligibility** 决定哪些记录进入 A+B1；**effect magnitude** 是这些记录的中位 H-ORAC；**evidence confidence** 评价独立来源、重复、precision、assay comparability 和异质性；**ranking uncertainty** 报告名次稳定性；**research maturity** 单独展示 Stage25A 历史与出版密度。不得相乘、加权或合并为一个总分。

| 维度 | 现有规则/数据 | v1.1 拟议规则 | 原因及预期影响 |
|---|---|---|---|
| 独立来源 | `independent_experiment_id`，但无验证 study ID | 先核实研究团队、实验批次和数据复用；至少 2 项独立原始研究才考虑高置信度 | 当前 28 种的 study N 均不能被证实，故不能直接按 DOI 升级 confidence |
| 重复与精度 | 68 条 A/B1 中仅 3 条有 canonical SD；CI 为 0 | 原文逐项提取 replicate type、n、SD/SE/CI 及所在位置；缺失记 unknown | 缺失误差不等于零；排名 precision 暂不可量化 |
| 异质性 | canonical IQR/range/flag | N≥2 时报告跨记录分布；单记录记不可估计；研究间分布须以核实独立研究为单位 | 防止把技术重复当成跨研究稳定性 |
| 方法可比性 | Rubric v2.0 A/B1/B2 | 保持 eligibility 不变，confidence 另记录 assay protocol 差异 | 不因排名变化回调 tier |
| 研究历史 | Stage25A metadata count/first-last year | 作为独立画像与导师汇报列，不自动进入 H-ORAC 排名 | 历史长度与化学效力不同 |

拟议 High：至少两项经确认独立研究、可审计 precision 和可接受的方法一致性，且无无法解释的重大异质性；Moderate：至少两项确认独立研究但 precision 或一致性存在报告缺口；Low/Uncertain：单一来源或来源独立性尚未确认。阈值和类别名称均须研究者审批，不得在本轮回写现有 confidence。若另设最低门槛，当前 v1.0 的 Rosmarinic acid、Daidzein、Fisetin、Hesperidin、Naringin 首先受影响；按记录 N≥2 顺延后仅 19 种，不能凑足 Top20。正式 v1.1 修订须先发 CHANGE REQUEST 并批准 unfreeze/version update。
