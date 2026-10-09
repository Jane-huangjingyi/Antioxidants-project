# Stage25B.6A 导师反馈证据审计与 Top20 修订模拟

**证据单位。** Publication 是原始论文；independent study 是独立开展且没有数据复用的研究；independent experiment 是独立实验运行；technical replicate 是同一次运行的重复测量；biological replicate 是独立生物样本；quantitative estimate 是一条可提取数值。本文的 68 条 A/B1 是 quantitative records，现有 `independent_experiment_id` 标签不能单独证明独立研究或独立实验运行。每个候选的不同 DOI 数可作为不同原始发表的线索，须核对方法、作者、材料和数据表后才能裁决 study independence。

**核心发现。** Frozen Top20 v1.0 保持不变。74 条 canonical 实验中 A=7、B1=61、B2=4、X=2；28 种可排序候选对应 68 条 A/B1 定量记录。`Eligible_experiment_N` 是当前数据表中的独立实验标签数，不能直接当作统计学独立样本数：study ID 和技术/生物重复层级均未系统记录。各候选的 A/B1 记录来自不同 DOI，但不同论文与独立研究不能画等号，故 scenario 2 当前无可确证的 20 人名单。

**误差与不确定性。** 68 条 A/B1 中，canonical SD 仅 3 条、SE 0、CI 0；本轮从 Carvalho 2023 原文 Table 3 额外核对 Quercetin、Caffeic acid、Gallic acid 的 ± 值，但原表未明示其误差类型，单独标为 `UNSPECIFIED_PLUS_MINUS_IN_ORIGINAL`。按“任何已报告数值误差信息”计 6/68（8.8%），按可确认 SD/SE/CI 类型计 3/68（4.4%）；候选层面及排名差异的可信 95%CI 均为 `CI_NOT_ESTIMABLE`。原文中的技术重复 n=3 不能替代独立研究 n=3。IQR/range 只作描述性分布，不能当作置信区间。

**研究历史。** 157 种候选均有 Stage25A metadata-deduplicated antioxidant/redox original-publication count；本轮按已纳入的 provenance 记录另算 2017–2026 十年出版数，并区分一般抗氧化文献年份与已裁决 H-ORAC 年份。7 个候选的主表 latest year 超出当前年份或无效，历史表已经标旗；第一/末年须核对元数据。导师汇报推荐首年、跨度、去重原始论文数及近五/十年数作为独立维度；H-ORAC 特定 DOI 数仅为来源代理，不是 study N。

**维生素。** VC（AFF-0104）是 Stage25A 第 2 名，已进入 Top50 和 47 种检索集；未进入 Top20 的直接流程原因是 Stage25B canonical 表尚无其 A/B1 定量记录。既有分类证据主表有 Ou 2001 0.95 与 Carvalho 2023 0.53 两条历史 B1，中位 0.74 mol TE/mol；当前最末可排序第 28 名为 1.25。VC 的原始来源核验与 canonical re-adjudication 是特定缺口，不能在本轮把分类证据直接接入 Frozen Top20。其他维生素形式参见专项表。

**排名模拟。** Scenario 0 为现行 Frozen Top20。Scenario 1 的 ≥2 A/B1 记录规则排除现行 Top20 中的 Rosmarinic acid, Daidzein, Fisetin, Hesperidin, Naringin；依原中位数顺延加入 Morin, Myricetin, Epigallocatechin, Gallic acid，结果仅 **19** 种符合门槛，缺第 20 名，未用 B2 补足。Scenario 2 要求 ≥2 经核实独立原始研究：9 种单记录候选按现有记录可确定不符合，其余 19 种均 `INDEPENDENCE_UNRESOLVED`，不能形成正式 Top20。

**方法适用性。**

| 方法 | 数据需求及当前满足程度 | 结论 |
|---|---|---|
| 经确认独立研究 N≥2 | study ID、数据复用核查；当前未满足 | 推荐作为正式修订候选，先完成来源独立性审计 |
| IQR/range | 至少 2 个可比定量记录；19/28 满足记录数 | 推荐描述性报告；不可称 95%CI |
| 实验间 CV | ≥2 个可比、独立且具有适当尺度的估计；研究独立性未知 | 暂不推荐作为跨研究 precision 指标 |
| Bootstrap median CI | 经验证独立研究的原始估计，足够研究数；当前不足 | 不计算；两研究 bootstrap 不能弥补稀疏证据 |
| Random-effects meta-analysis | 每研究 effect/SE 与可比性、足够研究数；多数无误差 | 当前不执行；k=2 异质性极不稳定 |
| Leave-one-study-out | 至少 3 项经验证独立研究较有解释力；当前未知 | 定点复核后可做诊断，当前不可正式估计 |
| Rank stability | 研究级重抽样或合理误差模型；当前无 | 仅可做规则门槛情景模拟，不给概率 |
| Prediction interval | 稳定异质性估计及足够研究数；当前无 | 不估计 |

**修订方案比较。**

| 方案 | 优点 | 缺点与统计学合理性 | 数据可执行性、预计影响 | 需补数据与导师汇报适用性 |
|---|---|---|---|---|
| A：至少2条独立实验记录 | 可立即展示单记录剔除的方向，保留中位数 | 实验 ID 的独立性未证实；门槛是证据量规则，不是显著性检验 | 现有表可执行；只余19种，不能构成Top20 | 需核对批次/重复；适合作为诊断情景，不宜称正式名单 |
| B：至少2项独立原始研究 | 直接回应跨研究复现要求 | 2项研究仍无法稳定估计异质性或名次CI | study ID 缺失；9种单记录确定不符合，19种无法裁决 | 需逐篇核查作者、实验和数据复用；适合作为下一版候选门槛 |
| C：研究门槛＋精度和置信度审查＋研究历史单列 | 同时回应导师四点，保持效力、证据质量与研究历史的不同含义 | 工作量较大；需要预先批准规则，不能以简单加权总分替代 | 当前仅能提出框架；正式名单等待来源和误差核查 | 定点补充单记录、cutoff及VC原文；最适合完整导师汇报的最终结构 |

推荐 C 作为下一轮设计方向；本轮不选择正式修订方案。三案均不改变 H-ORAC 原数值，也不生成全局加权总分。现阶段不宣称不同候选名次差具有统计学显著性。

**HUMAN DECISIONS REQUIRED**

| 决策 | recommended_option | evidence_basis | remaining_uncertainty | impact_if_approved |
|---|---|---|---|---|
| D1 最低门槛 | 优先审查 ≥2 独立原始研究；N≥2 记录仅作过渡诊断 | 当前 9/28 仅一记录，19/28 有≥2记录 | study ID 均未核实 | 会触发 v1.1 change request；不能自动凑足20 |
| D2 95%CI | 当前不计算，标 CI_NOT_ESTIMABLE | 68 条 A/B1 的 error/replicate 结构不足 | 原文可能有尚未提取的数据 | 不会产生虚假的显著性结论 |
| D3 研究历史 | 单独展示 | 157 种均有 Stage25A 指标；与化学容量不同 | 元数据年值需 QC | 导师汇报增加历史维度，不改变中位排名 |
| D4 维生素 | 定点复核 VC 两原文并审计 canonical 缺口；其他维生素按方法适配另列 | VC 已在 Top50/retrieval，历史有 2 B1 | 2001 表格和统计误差需复核 | 可决定是否发起针对性 evidence change request |
| D5 v1.1 条件 | 暂不具备正式冻结条件 | ≥2记录情景仅19种；study 独立性未证实 | 门槛与补充检索范围未决 | 维持 v1.0，待研究者批准修订 |
| D6 优先回查 | Rosmarinic acid、Daidzein、Fisetin、Hesperidin、Naringin；再查 rank20/21 与 VC | 前五名为 Frozen Top20 单记录，cutoff 差 0.1575 | 原文重复/误差结构 | 决定最低门槛与排序可信度 |
| D7 补充 H-ORAC | 只对上述 cutoff/单点/VC 开展定点检索 | 1,641 pending 未全量裁决 | 新证据量未知 | 形成 change request 输入，不批量重开 Stage25B |

本轮状态：**STAGE25B.6A — SUPERVISOR FEEDBACK AUDIT COMPLETE**。Frozen Top20 v1.0 与 Stage25B canonical rubric/证据表保持不变；若研究者批准修订，先建立 CHANGE REQUEST，再按批准范围核对独立研究、误差与针对性证据，另行决定是否更新 v1.1。
