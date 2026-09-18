# Phase 0–1 决策日志

版本 1.0，2026-09-17。

## 已冻结

1. 主榜评估全球正常膳食来源，暴露按地区/人群保存，不把局部摄入外推到全球。
2. 一般成年人和膳食可达暴露是主评价基准；患者、高风险人群和补充剂证据单独标记。
3. 主榜只允许结构唯一的食物原型小分子；人体代谢物、内源性物质、矿物和药用/补充剂主来源实体进入 secondary/extended 层。
4. 不设多酚配额；polyphenol-first 只是候选生成顺序，不是排名优势。
5. 抗氧化包含 direct、redox regulatory 和 indirect redox-related；间接通路必须落到可信 redox endpoint。
6. 证据质量优先于数量；同层论文数饱和，低层证据不能靠数量越级。
7. 人体效应与人体 PK 分开；H5 证明暴露，不能替代临床/生物标志物效应。
8. T1/T2、T3、T4、T5 分层输出；任何数据库或作者用词均不能替代 assay 级判定。
9. 安全性/剂量窗口作为风险与转化维度，Phase 2 初筛不作硬排除或简单加总。
10. 描述性联合处理只能标记 possible synergy/antagonism；正式协同需零模型。
11. 缺失状态区分 not_searched、searched_none、conflicting、not_applicable。
12. 排名前必须冻结评分代码、检索日期、缺失值规则，并进行多权重 rank stability。

## 主动补充的规则

- 增加 evidence family，防止同一试验多篇论文重复计数。
- 增加 assay validity 与 polyphenol interference 检查，避免非特异反应被判为靶点。
- 增加 parent–form–metabolite 图和可比较分子种类要求，防止用母体体外浓度比较结合物 Cmax。
- 食物暴露拆为含量、消费量和估计摄入；只检出时食物域最高 0.20。
- T2 设置 directness qualifier；完整细胞 TPP/CETSA 未经竞争或正交复核时可降级。
- 加入跨类别遗漏检查：betalains、quinones、含氮植物小分子等，但不保证其入榜。

## 尚未冻结、需研究者决定

1. 是否确认原始 25/25/20/15/15 为唯一主方案，并接受人体优先、暴露平衡、实验转化优先三套敏感性方案。
2. Food exposure 域五个分项的精确权重及“meaningful exposure”数值阈值；建议在 Phase 2A 用真实分布校准，不预设单一全球阈值。
3. `dose_translation_gap` 的 10×/100× 边界是否按总 Cmax、游离 Cmax、组织暴露或代谢物暴露分别实现。
4. 冲突证据和安全风险作为总分惩罚、tie-breaker，还是独立二维决策矩阵；当前建议后二者。
5. Top20 稳定性合格标准，例如四套方案中入选至少 3 次、名次 IQR 不超过 5。
6. Phase 2 的区域最低覆盖：建议至少中国、北美、欧洲，并在数据允许时加入东亚其他地区、南亚、拉美和非洲。
7. 是否预注册 protocol 与代码版本，以及双人复核的资源配置。

## 内部质量审计结论

未发现循环定义：候选资格不依赖最终得分，得分不反向定义证据层级。热门分子偏倚由 evidence-family 去重与饱和上限控制。靶点混级由 relation_type、directness 和 T-tier 三字段约束。人体效应与 PK、体外 redox 与 cell-free chemistry 已拆开。生物利用度、主要代谢物、食物含量与消费量均有独立字段。字段可自动化程度总体足够，但食物形态映射、assay 干扰、T2 directness、redox endpoint validity 和风险偏倚仍需人工复核。评分中最主观部分是 food exposure 分项与质量降级，Phase 2 应通过双人试标和一致性统计校准。没有设置 direct-target、人体验证或安全性的过早硬门槛。框架可支持后续批量候选生成与 target extraction，但在审核未完成前不得执行正式排名。
