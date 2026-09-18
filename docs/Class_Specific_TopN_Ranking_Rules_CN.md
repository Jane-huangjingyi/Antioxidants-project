# Class-specific Top-N Ranking Rules（v1.0）

所有类别共用的 eligibility gate 是：正常膳食来源、结构唯一、PubChem CID/InChIKey 可核对、非未表征提取物、非默认补充剂来源、原始证据可追溯。类内排名使用该类适配的 primary construct；secondary evidence 用于解释与置信度，不和 primary value 简单相加。缺失不记为零，`Not reviewed` 与 `No eligible evidence after systematic search` 必须分开。

| Class | Candidate eligibility | Primary metric | Secondary evidence | Exposure / human role | Confidence | Missing handling | Top-N rule |
|---|---|---|---|---|---|---|---|
| Flavonoids | 定义单体；glycoside/aglycone 与 stereoisomer 分开；H-arm compatible | A/B1 H-ORAC-FL median，mol TE/mol | CUPRAC、lipid oxidation、causal NRF2/NOX | exposure 用于跨类与实验剂量；human efficacy 不改写 chemical rank | independent records + heterogeneity | 无 H-ORAC → measurement priority，不排除 | N eligible≥20 才 Top20，否则 Top available |
| Phenolic acids/conjugates | 游离体与 conjugate/isomer 分开 | H-ORAC-FL median | CUPRAC、metal chelation、lipid oxidation | 标注 free/total/hydrolysed intake definition | 同上并增加 definition confidence | definition mismatch → non-poolable | Top10–20，按 N eligible |
| Other polyphenols | subclass-specific identity 与 food occurrence | H-ORAC 或适配 lipid assay | mechanism、CUPRAC、PK | 暴露用于 representative selection | assay-arm specific | 不跨 subclass 强合并 | subclass Top-N；总体 profile 不做总分 |
| Vitamin C | L-ascorbic acid identity | H-ORAC/reducing/regeneration profile | human oxidative biomarkers | DRI/observed intake 与 Cmax 分开 | protocol + intervention design | 不与 E vitamer 单值混排 | all eligible vitamers，profile 展示 |
| Vitamin E | tocopherol/tocotrienol vitamer 与 stereoform 明确 | L-ORAC 或 validated lipid chain-termination metric | lipid peroxidation/F2-isoprostanes | dietary vs supplement dose 分开 | human biomarker + lipid assay | H-ORAC 缺失不构成惩罚 | vitamer-specific all eligible/Top10 |
| Carotenoids | cis/trans、carotene/xanthophyll 分开；optical QC | singlet-oxygen quenching或 validated lipid-phase metric | lipid oxidation、L-ORAC（适配时）、human biomarkers | food matrix/formulation/PK 必须保留 | optical/solubility QC + independent studies | optical unresolved → supportive only | Top10 或 all eligible |
| Organosulfur | parent identity、加工生成、正常食物来源 | causal KEAP1/NRF2、thiol/GSH/redox modulation evidence profile | PK、oxidative endpoints、chemical reactivity | parent/metabolite exposure决定转化意义 | causal perturbation > association | 未系统检索标 Not reviewed | 按 evidence tier 与 dietary relevance 分层；不以 ORAC 排 |
| Betalains/N-containing | defined pigment；pH/form identity | fixed-protocol redox/radical assay with optical QC | cellular/human redox endpoints | 暴露/稳定性决定实验代表性 | interference QC 是硬条件 | 无 QC 不进入 numerical rank | Top10 或 all eligible |
| Other phytochemicals | dietary gate 严格，排除主要药用/补充剂来源 | subclass-specific | mechanism、PK、安全性 | 暴露用于控制知名度偏倚 | subclass-specific | 不跨 assay 填补 | subclass Top-N |
| Minerals | essential nutrient form/context | 不做 capacity rank；按 cofactor relevance 与 requirement | deficiency/supplementation、enzyme dependency、toxicity | 核心维度 | evidence design + status dependence | 未审阅标 gap | 无 antioxidant Top-N；功能矩阵/all relevant |

排名输出必须同时给出 primary value、unit、eligible record count、confidence、provisional rank、TopN status、version 与 caveat。任何类只有完成候选宇宙、系统检索、eligibility adjudication 和重复/独立性检查后，才允许从 `Not completed` 更新为 provisional Top-N。

