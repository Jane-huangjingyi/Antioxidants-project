# Protocol v1.0 至 v2.0 变更日志（中文）

| v1.0 内容 | v2.0 处理 | 理由 |
|---|---|---|
| 正常膳食、天然原型、结构明确的小分子主榜 | 保留并冻结 | 保证化学身份、膳食相关性和可复现抽取 |
| 多酚优先生成但无类别配额 | 保留 | 避免预设类别结论并允许跨类别竞争 |
| 代谢物与母体分榜 | 保留；代谢物成为 Stage 2 必填注释 | 防止化学实体混级，同时反映人体真实暴露 |
| 证据质量高于论文数量 | 保留 | 防止 publication-popularity bias |
| Direct target 非早期硬门槛 | 保留 | 避免排除重要但靶点研究不足的食源成分 |
| T1–T5 靶点体系 | 原样保留 | 防止把 pathway regulation 和预测靶点误写成直接结合 |
| Safety/dose window 独立维度 | 保留并纳入 Stage 2 风险修饰 | 化学容量不能替代剂量可行性与安全性 |
| 协同/拮抗与 food matrix | 保留为 context layer | 联合作用不定义单体基础容量 |
| PK 与 efficacy 分开 | 保留并强化 | 暴露不能作为临床获益证据 |
| 25/25/20/15/15 综合评分可能决定最终榜单 | 修改为 legacy Translational Priority Score；不再产生化学 Top20 | 导师要求统一、可解释的化学主排序构念 |
| 多种抗氧化证据共同影响“抗氧化排名” | 拆为 Stage 1 ORAC-FL 与 Stage 2 转化优先级 | 消除 chemical capacity 与 biological relevance 的构念混淆 |
| Cell-free assays 为低级支持证据 | ORAC-FL 在 Stage 1 成为有条件主指标；仍不提升为人体证据 | 任务目标改变为先比较化学容量，不能外推人体效果 |
| DPPH/ABTS/FRAP 可作为抗氧化证据 | 降为 secondary；不得共同生成默认总分 | 三者分别受人工自由基、介质、位阻或还原力构念限制 |
| CUPRAC 为补充 assay | 提升为首选 orthogonal secondary | 提供 ET/reducing-power 维度，与 ORAC 的过氧自由基 chain-breaking 互补 |
| TRAP 为补充 assay | 保留为 peroxyl-trapping confirmation | 与 ORAC 接近但方法与计算不等价 |
| 未规定文献 ORAC 的可比准入 | 新增 A/B/C/X eligibility framework | 防止跨 protocol、跨 arm 和信息不足的数值拼接 |
| 未明确 ORAC 聚合统计 | 新增 median、range/IQR、分层和 rank-band 规则 | 防止最大值选择与伪精确排序 |
| H/L ORAC 可能被视为同类数值 | 明确分臂，除非桥接验证否则不混排 | 两臂溶剂、增溶和校准条件不同 |
| ORAC 缺失可能影响候选资格 | 统一编码 missing，不记零、不排除；建立 measurement-priority list | 数据缺失不等于生物学低值 |
| 一个 Top20 名称 | 分为 Chemical Antioxidant Capacity Top20 与 Translational Priority Top20 | 保证结论与推断问题一一对应 |
| 跨类别统一比较原则较宽泛 | 新增 polyphenol、tocopherol、carotenoid、organosulfur 的专门 QC 与分臂策略 | 避免亲脂性、光学干扰或机制不匹配造成系统偏倚 |
| 无默认 multi-assay 合成禁令 | 明确禁止平均或默认 z-score；采用 profile/concordance | 不同 assay 测量不同构念，合成会制造无效尺度 |

v2.0 没有废除人体、暴露、机制或靶点证据，而是将它们放回其正确的 Stage 2 推断层。此次重构不生成任何候选名次。
