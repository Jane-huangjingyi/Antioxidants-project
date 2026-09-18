# Stage 1 与 Stage 2 框架（中文）

## 核心区分

Stage 1 与 Stage 2 是两个不同的推断任务，不是同一总分的前后步骤。

| 项目 | Stage 1：Chemical Antioxidant Capacity Ranking | Stage 2：Translational Prioritization |
|---|---|---|
| 核心问题 | 在可比化学条件下，哪个单体更能终止 AAPH-derived peroxyl-radical chain oxidation？ | 哪些候选更值得做人群、机制和靶点实验？ |
| 主输入 | Tier A ORAC-FL；Tier B 仅支持 | 人体、暴露、PK、biological redox、机制、靶点、可开发性、安全性 |
| 主单位 | mol TE/mol compound | 分域等级或经敏感性分析的优先级分数 |
| 输出名称 | Chemical Antioxidant Capacity rank | Translational Priority |
| 缺失处理 | `not_measured` / `insufficiently_comparable`，进入测量优先清单 | 逐域标记 missing，不自动记零 |
| 禁止外推 | 人体疗效、生物利用度、细胞调控、临床获益 | 不得反向改写化学 ORAC 值 |

## Stage 1 决策流程

候选先通过食源性、原型小分子和结构唯一性规则。随后抽取 ORAC-FL 记录，判定 H-ORAC/L-ORAC，并按 A/B/C/X 分级。Tier A 可进入主数值排序；Tier B 只提供支持；Tier C 和 X 不进入数值排序。多条合格记录先检查同质性，再报告 median 与 range/IQR；不取最大值。H/L 无桥接验证时分臂输出。无 ORAC 数据的候选保留并进入 measurement-priority list。

## Stage 2 决策流程

Stage 2 可覆盖 Stage 1 高位候选、ORAC 缺失但具重要证据的候选，以及需解决跨类别偏倚的候选。八个最低必评域为：human evidence、dietary exposure、bioavailability/dose translation、biological redox evidence、mechanistic evidence、direct-target evidence、experimental tractability、safety/prooxidant risk。Major human metabolites 和 context interactions 是强制结构化注释。

原 25/25/20/15/15 方案改名为 legacy Translational Priority Score，不再决定化学 Top20。v2.0 建议以 20/15/15/15/10/10/10/5 作为待 pilot 的初始敏感性场景，同时展示逐域 profile。任何加权总分均需报告缺失处理、权重替代情景和 rank stability。

## 输出与命名

只有 Stage 1 可生成 `Chemical Antioxidant Capacity Top20`；证据覆盖不完整时写作 `provisional`。只有 Stage 2 可生成 `Translational Priority Top20`。不得发布含义不清的“综合抗氧化能力 Top20”。多维信息优先以 profile、证据矩阵和风险旗标呈现。
