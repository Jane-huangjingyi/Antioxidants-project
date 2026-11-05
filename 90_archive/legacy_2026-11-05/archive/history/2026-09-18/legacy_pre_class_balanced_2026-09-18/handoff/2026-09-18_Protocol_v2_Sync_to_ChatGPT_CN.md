# Protocol v2.0 同步给 ChatGPT/研究者

## A. 最大的结构性变化

v2.0 将原先多维证据共同决定一个 Top20 的逻辑拆分为两套独立输出：Stage 1 以可比 ORAC-FL 排列 chemical antioxidant capacity；Stage 2 以人体、暴露、PK、biological redox、机制、靶点、可开发性和安全性评估 Translational Priority。两者不得互相改名或合成为一个无定义总分。

## B. 当前正式主排序指标

有条件采用 ORAC-FL。推荐单位为 mol Trolox equivalents/mol compound（mol TE/mol）。选择依据是其 AAPH-derived peroxyl-radical、fluorescein kinetic AUC、Trolox calibration 和摩尔归一构成了明确而可执行的 chemical chain-breaking construct；选择理由不是文献数量。

## C. Stage 1 定义

结构明确单体在锁定或方法学可比 ORAC-FL 条件下，对 AAPH-derived peroxyl radicals 引起的 fluorescein 氧化所表现的 kinetic integrated chain-breaking capacity。它不代表人体效果、临床获益、生物利用度、细胞 redox regulation 或实验优先级。

## D. Stage 2 定义

Stage 2 评价候选是否值得开展营养干预、机制和 target-protein 实验。最低八域是 human evidence、dietary exposure、bioavailability/dose translation、biological redox evidence、mechanistic evidence、direct-target evidence、experimental tractability、safety/prooxidant risk；major metabolites 与 context interactions 必须记录。

## E. ORAC literature eligibility 核心规则

Tier A 方法与身份信息完整，可进入主数值排名；Tier B 部分可比，只作定量支持；Tier C 存在已知不兼容，只作定性支持；Tier X 信息不足，等待补全。总等级由最弱的关键条件决定，而不是通过字段多数票。不得取最大值、不得使用 food-level ORAC、不得拼接不同 protocol、不得重复计算同一研究。

## F. H/L ORAC 处理

H-ORAC 与 L-ORAC 是不同 assay arms。未经预设桥接研究证明测量等价、校准一致和误差可接受，不得混排；应分别发布两个 rank table。Tocopherols 和 carotenoids 的 L-ORAC 还需专门检查增溶、聚集和光学干扰。

## G. Secondary assays 正式角色

CUPRAC 是首选 orthogonal secondary（ET/reducing power）；ABTS 是 broad-polarity artificial-radical response；DPPH 是 fixed-protocol mixed ET/HAT reactivity；FRAP 是 ferric reducing power；TRAP 是 peroxyl-radical trapping confirmation；lipid-peroxidation assays 是脂相/食品情境证据；HORAC、TOSC、superoxide、hydroxyl radical 和 metal chelation 仅 supportive。禁止默认 composite。

## H. v1.0 综合评分的处理

25/25/20/15/15 被更名为 legacy Translational Priority Score，停止用于 Chemical Antioxidant Capacity Top20。v2.0 提出八域 profile，并把 20/15/15/15/10/10/10/5 仅作为待 pilot 的敏感性分析起点，不作为已冻结真值。

## I. 尚未解决的方法学风险

1. 现有文献中真正达到 Tier A 的比例未知。
2. H/L arm 缺少可接受的跨臂桥接，可能无法形成跨类别单榜。
3. Carotenoids 的光学、溶解和聚集问题可能产生系统性低估或失真。
4. Organosulfur compounds 的主要 redox mechanism 可能不被 ORAC 构念捕获。
5. Stage 2 权重尚未通过敏感性分析和外部效度检查冻结。

## J. 是否可以开始 literature ORAC pilot

方法与数据结构已经具备启动 pilot 的条件，但应先由研究者/ChatGPT 审核 v2.0。审核后可开展 10–20 个代表性候选的有限 pilot；当前不建议直接扩大为全候选批量抓取。

## K. 推荐下一阶段步骤

1. 冻结 v2.0 与 Tier rubric。
2. 选取跨类别、可追溯的 10–20 个 pilot compounds。
3. 检索、去重并逐记录提取 ORAC-FL。
4. 双人或规则复核 A/B/C/X、单位换算与 H/L arm。
5. 评估 Tier A 覆盖、异质性、跨臂问题和 CUPRAC 覆盖。
6. 形成 provisional 分臂结果与 ORAC measurement priority list。
7. 决定是否扩大文献排名或先进行统一实验复测。

## L. Zotero 方法学文献

本轮未新增 Zotero 条目。v2.0 直接继承 assay methodology audit 已正式纳入 `antioxidants project` collection 的 ORAC 方法、验证、比较与局限性核心文献；进入 pilot 后只为实际纳入的原始 ORAC 数据源新增条目。

## 需要最终拍板的问题

研究者需确认：是否接受无法桥接时发布 H/L 双榜；是否接受 Chemical Top20 在覆盖不足时必须标记 provisional；以及 Stage 2 八域权重是在 pilot 前预注册一个主方案，还是保留多个权重场景仅做 rank-stability 分析。
