# Stage25B.6B 最终评估

状态：**STAGE25B.6B BLOCKED BY SPECIFIC EVIDENCE GAPS**。本轮完成 68 条 A/B1 的逐条来源登记、16 个 DOI 的来源索引、28 种候选物的保守研究计数和定点候选来源清单；未完成能证明跨论文数据独立性的原文对照，因此不构成 Top20 v1.1 冻结依据。

Q1–Q3：已确认至少 2 项独立原始研究 **3/28（Caffeic Acid、Quercetin、Gallic Acid）**；已确认恰好 1 项 **20/28**；其余 **5/28** 还没有可确认的独立原始来源。现有 canonical 中 9 种仅 1 个 DOI 代理、19 种至少 2 个 DOI 代理；单 DOI 者为 `FAIL_ON_AVAILABLE_EVIDENCE`，并不证明其他文献不存在；多 DOI 但不足 2 项已核实者为 `UNRESOLVED`。三项通过来自 [Žuvela 2019 原文 Methods 3.1–3.3 / Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/)、[Skroza 2022 原文 Methods 2.1 / Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/) 和 [Carvalho 2023 原文 Methods 2.1–2.2 / Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)：不同研究组、各自制备纯品并开展新实验；未把文中模型预测或同文技术重复算作第二研究。

Q4–Q6：明确 SD/SE/CI 3/68，任意数值误差由 6A 的 6/68 增至 26/68；新增 7 条 Skroza 2022 Table 2 的未定义 ±，另 13 条 Žuvela 2019 Table 3 的 `ln(ORAC) ±`，均不是新增可直接使用的 SD。19 种多记录候选物可报告记录间中位数、IQR、范围，不能无条件称为独立研究间分布。正式 95%CI 与入榜概率均不可估。

Q7–Q8：5 种单记录 Top20 仅找到 Daidzein、Hesperidin 等待查论文线索，未核实任何新增合格 H-ORAC-FL 定量研究；没有核实第 20 种符合拟议门槛的候选物。当前 **3** 种达到严格 `PASS_VERIFIED`；6A 的 19 种只是“至少两条记录”情景，不是独立研究达标数。

Q9：VC 2023 原文 Table 3 的 0.53±0.03 已核实，± 类型不明；2001 的 0.95 原表不可访问；独立性未证实。未入 canonical 属待批准的衔接/裁决缺口，不得静默迁移。

Q10：研究成熟度表继承 6A 的元数据去重结果，保留 7 个未来/无效年份标志，另有 13 个候选物缺少可解析的起止年份；原始论文与综述、重复 DOI、跨候选映射仍需逐项核实，因此不能称为全面通过元数据 QC。一般抗氧化研究数量不等于 H-ORAC 研究数量。

Q11–Q12：尚不能提出可执行 v1.1 冻结方案。变更请求包括独立研究门槛、单记录/边界候选来源全文裁决、VC 衔接；详见 CR 清单，均待人工批准。

Q13：建议继续定点检索 Daidzein（10.1021/jf053112o）、Hesperidin/Myricetin（10.1111/j.1750-3841.2010.01717.x）、Rosmarinic acid 与 Naringin 的纯品 H-ORAC-FL 原表，以及 Ferulic/Morin/Gallic 的边界补证；需先得到研究者对范围和资源的批准，不扩大至全部 pending。

Q14：可向导师明确解释：效力中位数、证据资格、研究独立性、测量精度、研究成熟度和排名不确定性是不同维度；描述性 IQR 不是 CI，High confidence 不是 95% 入榜概率。

Q15：建议进入 6C 的前提是取得关键全文、完成跨 DOI 数据集比对和误差定义定位，并批准正式门槛与 CR；本轮不自动启动。

## HUMAN DECISIONS REQUIRED

| ID | 推荐选项 | 依据/未解问题 | 影响 | 需批准 |
|---|---|---|---|---|
| D1 | 暂不正式启用 N≥2 门槛 | 3/28 通过严格核实；其余需原文比对 | v1.1 资格 | 是 |
| D2 | 批准定点原文进入 v2.0 裁决，不自动纳入 | 候选来源无已核实定量值 | 新证据 | 是 |
| D3 | 批准 VC 逐来源衔接 | 2001 原表不可访问，2023 已定位 | VC 资格 | 是 |
| D4 | 批准关键来源误差提取 | 类型仅 3/68 | CI 可行性 | 是 |
| D5 | 仅扩大上述点名候选物检索 | 5 个单记录和 cutoff 缺口 | 入选集合 | 是 |
| D6 | 接受不足 20 的候选集原则 | 门槛不可为凑数放宽 | 名单规模 | 是 |
| D7 | 暂不启动正式修订 | 独立性、误差与 VC 缺口 | v1.1 冻结 | 是 |

原始支持：[Carvalho 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/)、[Ou 2001 出版商摘要](https://pubs.acs.org/doi/10.1021/jf010586o)。
