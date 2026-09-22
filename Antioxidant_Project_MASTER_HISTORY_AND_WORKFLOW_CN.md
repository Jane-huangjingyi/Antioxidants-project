# Antioxidants Project：MASTER HISTORY AND WORKFLOW（CN）

**版本：Atlas framework v1.0｜日期：2026-09-18｜用途：项目历史、当前状态与后续入口**

## 1. Project origin

项目最初希望从常见食源性抗氧化小分子中建立候选全集，并依据人体相关性、抗氧化生物学、食物暴露、机制、direct-target evidence 与实验可开发性形成 Top20。早期 framework 的重要贡献是定义正常膳食原型单体、保留 major human metabolites、区分人体 PK 与 efficacy、建立 T1–T5 target hierarchy，并明确论文数量不能替代证据质量。其不足是“综合科学价值”与“抗氧化能力”混在同一 100 分体系，无法给导师一个统一、可操作的主排序标准。

## 2. Major conceptual changes

### Change 1：综合多维评分 → chemical antioxidant capacity

导师要求用一句话说明“按什么能力排序”，触发了结构重构。Stage 1 被定义为 chemical capacity，Stage 2 被重新命名为 translational priority。原 Human 25 / Antioxidant biological 25 / Food exposure 20 / Mechanistic 15 / Target-tractability 15 仍可作为 Stage 2 的历史起点，但不再产生基础 antioxidant-capacity Top20。保留的是人体、暴露、安全、代谢物和 target evidence 的重要性；改变的是它们不再与化学能力混成同一概念。

### Change 2：multiple assays → ORAC-FL primary

系统 assay audit 表明 DPPH、ABTS、FRAP、CUPRAC、TRAP 和 ORAC 测量不同 constructs，不能简单平均。ORAC-FL 被有条件地选为酚类水相候选的 primary metric，操作性定义为 AAPH-derived peroxyl radicals 引起 fluorescein 氧化时的 kinetic integrated chain-breaking capacity，以 mol TE/mol compound 表示。CUPRAC、DPPH、ABTS、FRAP、TRAP 被降为机制互补证据。该改变由方法学审计而非文献数量触发。

### Change 3：H/L mixed candidates → H/L separation

Tocopherols 和 carotenoids 的溶解、聚集、光学行为与水相多酚不同，H-ORAC 和 L-ORAC 不能天然视为同尺度。项目因此分臂：水溶性酚类进入 H-arm，脂溶性维生素和类胡萝卜素进入 L-arm 或 special-case。保留统一的身份、暴露和证据字段，但停止强行混排。

### Change 4：strict Tier A → exploratory B1 framework

Tier A 要求足以支持正式高置信比较，但 17-compound pilot 中 Tier A=0，无法满足导师对历史趋势图的需求。项目保留 Tier A 不降级，同时把原 Tier B 拆为 B1 exploratory comparable 与 B2 quantitative/low-comparability。A+B1 可以进入明确标注的 exploratory literature-derived comparison；B2 仅用于补充。该变化改变用途层级，不改变正式标准。

### Change 5：small pilot → 50-candidate universe

17 个候选的 H-ORAC 数据不足以形成 20 个 eligible phenolics，项目扩展到 50 个 food-derived phenolic/polyphenolic compounds，并严格区分 aglycone/glycoside、立体异构体与 conjugate。保留候选生成不能按 ORAC 高低反向选择的原则。

### Change 6：provisional Top20 → evidence consolidation

初始 provisional Top20 中多数是 single-study estimates。针对 Top10 单研究候选和 EGCG、kaempferol、myricetin、anthocyanin、flavanone、lignan 等重要缺失项进行 targeted consolidation。新增独立 B1 后，排序前五从 quercetin、epicatechin、catechin、quercitrin、caffeic acid 更新为 epicatechin、catechin、quercetin、kaempferol、naringenin；quercetin、catechin、epicatechin 获得 High confidence。保留了 Tier A=0 和“无 eligible ORAC-FL 不等于低能力”的限制。

### Change 7：phenolic-only ranking → class-balanced dietary antioxidant factors

导师要求明确跨类别候选范围并避免多酚检索起点垄断，项目构建了 20 个有机因子加 5 个 mineral context nodes 的 class-balanced pilot。该面板覆盖多酚、酚酸、维生素、类胡萝卜素、有机硫和香辛料酚类；12 个 core candidates 的 intake range 为 3.5–65.4 µmol/day，约 18.62 倍。其用途是测试 taxonomy、暴露、机制矩阵和 visualization，现正式重命名为 **Cross-Class Pilot Panel v1.0**，不得解释为最终 20 种。

### Change 8：one total Top20 → class-specific Top-N + cross-class comparison

跨类别统一用 ORAC 排名在科学上不可成立：vitamin E 是脂相 chain terminator，carotenoids 依赖 singlet-oxygen/lipid-phase construct，organosulfur 主要是 KEAP1/thiol/GSH regulation，minerals 是状态依赖的 enzyme cofactors。当前项目升级为 **Antioxidant Functional Factor Atlas**：各类先用 class-specific construct 产生 Top-N/Top available，再用不加总的 profile matrix 做跨类比较，最后依据暴露、机制互补、PK、安全和 tractability 选择实验代表。

## 3. Stage 0–16 总表

| Stage | Question | Input | Method | Key Output | Main Finding | Limitation | Next Step |
|---:|---|---|---|---|---|---|---|
| 0 | 研究问题是什么？ | 初始目标 | protocol definition | Phase 0–1 protocol | 化学能力、人体/转化与 target 必须分层 | 无数值 ranking | 建候选框架 |
| 1 | 如何筛“综合科学价值”？ | protocol、数据库审计 | 100 分框架与数据字典 | Evidence rubric | 建立可追溯字段和 T1–T5 | 综合分不够统一 | assay audit |
| 2 | assays 各测什么？ | 方法学文献 | HAT/ET 与 assay audit | Assay audit | assays 不可简单平均 | 不产生 compound rank | 选 primary metric |
| 3 | 是否采用 ORAC？ | audit | v2.0 two-stage design | ORAC-FL decision | 酚类 chemical capacity 用 ORAC-FL | 不适配所有类别 | H/L 分臂 |
| 4 | H/L 能否混排？ | physicochemical/QC rules | arm separation | H/L framework | 未桥接不混排 | L 数据少 | eligibility |
| 5 | 历史数据如何判级？ | protocol metadata | A/B1/B2/C/X | Eligibility rubric | A formal；A+B1 exploratory | A=0 | pilot |
| 6 | 排哪些候选？ | food/identity scope | taxonomy + H/L compatibility | Candidate scope | 正常膳食定义单体 | ORAC-centric | 17-compound pilot |
| 7 | 历史 ORAC 能否作图？ | 17 candidates | original-value extraction | 11 initial records | Tier A=0 | 9 candidates missing | B1 policy |
| 8 | B1 后能否探索比较？ | 16 reclassified records | exploratory aggregation | H-ORAC exploratory plots | 有限趋势可见 | 非标准化真值 | expand universe |
| 9 | 多酚 universe 是否充分？ | scope + identities | systematic candidate generation | 50 candidates | 覆盖主要 phenolic subclasses | publication bias | provisional Top20 |
| 10 | 可否形成 phenolic Top20？ | A/B1 records | median + confidence | provisional Top20 | 历史数据支持有限榜单 | single-study 多 | consolidate |
| 11 | Top20 稳定吗？ | targeted searches | independent B1 + before/after | consolidated ranking | 前五更新；3 个 High | Tier A=0 | readiness |
| 12 | 谁可进入 target pilot？ | rank + assay risk | Ready/Conditional/Not ready | 20-row shortlist | readiness 与 rank 分开 | 尚未 mapping | SOP |
| 13 | 能否无 AI 重现？ | 全部 H-ORAC files | master SOP + templates | H-ORAC pipeline | phenolic workflow 可复现 | 只适用于 H-arm | cross-class pilot |
| 14 | 如何覆盖多类别？ | shortlist + exposure | class coverage → exposure → mechanism | 20 organic + 5 minerals | core exposure 18.62-fold | pilot，非最终 | mechanism ledger |
| 15 | 机制证据如何组织？ | pilot panel + selected literature | compound×mechanism ledger | 25 evidence rows | 最小可审计 ledger | 未系统穷尽；blank=not reviewed | Atlas framework |
| 16 | 如何继续扩展所有类别？ | Stage 0–15 | class-specific rules + profile comparison | Atlas v1.0 framework | one Top20 被 class Top-N 替代 | 分类别 Top-N 未执行 | roadmap Phase 1–4 |

## 4. Current Atlas workflow

`Functional class → Candidate universe → Class-specific Top-N → Mechanism profile → Dietary exposure → Evidence strength → Cross-class comparison → Representative experimental panel → Target mapping`。每个箭头都有 stop condition：身份和 food occurrence 未核实不得进入 universe；primary construct 未冻结不得排名；系统检索未完成不得把空白写成 no evidence；class-specific Top-N 未完成不得冻结跨类实验 panel；T1/T2 与 pathway effects 未完成 pilot 不得批量 target mapping。

## 5. Output 与 Interpretation 的统一规则

Stage 10 的 output 是 H-ORAC provisional Top20；它说明历史 ORAC-FL 文献可支持有限 phenolic ranking，不说明跨类别最强 Top20。Stage 14 的 output 是 Cross-Class Pilot Panel v1.0；它说明 taxonomy、暴露窗口和机制可视化可以在共同结构中测试，不说明这 20 个是最终实验因子。Stage 15 的 output 是 pilot mechanism evidence ledger；它说明证据可以按实验设计分级并连接到 compound/pathway，不说明空白 cell 无证据。

## 6. File status and provenance

历史 protocol、原始抽取、ranking、change logs、SOP、Python scripts 和旧 figures 全部保存在 `archive/legacy_pre_class_balanced_2026-09-18/`。Phase 2 的 active data 是统一 candidate master、taxonomy relationships 和 exclusion log；Phase 3A 新增 flavonoid eligibility lock、record-level H-ORAC evidence master、Top20 v1.0 与 coverage audit。原始 class-balanced panel、旧 phenolic ranking 和机制表保留为历史输入，未删除或静默覆盖。R 脚本是正式图的唯一主入口。

## 7. Current project status

### Completed

Stage 0–13 的 protocol、assay audit、H/L 分臂、A/B1/B2/C/X、17-compound pilot、50-candidate H-arm universe、phenolic provisional Top20、evidence consolidation、readiness shortlist 和无 AI H-ORAC SOP 均有结构化文件；Atlas taxonomy、class-specific ranking rules、cross-class profile framework 和未来四阶段 roadmap 已完成框架冻结。

### Provisional

Cross-Class Pilot Panel v1.0、25-row mechanism evidence ledger、所有基于 B1 的 H-ORAC 数值和 target readiness 均为 provisional/pilot。R 4.5.3 已可用，Phase 2 universe 图与 Phase 3A flavonoid 图均已在本机渲染并完成视觉检查。

### Superseded

100 分综合框架不再产生 chemical capacity rank；ORAC 不再承担 all-class ranking；phenolic Top20 不再称为项目最终 Top20；旧 Python 图不再作为正式 Atlas 绘图主流程。

### Not yet completed

除 Flavonoids 外的 class-specific Top-N、完整机制系统综述、正式 cross-class comparison、Global Top Overview、最终 experimental representative panel、批量 target mapping、pathway knowledge graph 及统一实验复测均未完成。

## 8. Stage 17 — Phase 2 Candidate Universe Construction

**Purpose：**为 Atlas 的 9 个 analysis panels 建立统一、结构明确、正常膳食来源且与 antioxidant performance 无关的候选宇宙。**Input：**taxonomy v1.0、历史 50-candidate phenolic universe、Cross-Class Pilot Panel、PubChem 身份信息和权威食物数据库优先级。**Method：**先按 chemical class 和 normal dietary relevance 生成候选，再批量核对 PubChem CID、InChIKey、分子式和分子量；glycoside/aglycone、cis/trans isomer、parent/conjugate、dietary parent/metabolite 分开；无法唯一解析或食物证据薄弱者标记 unresolved，失败者保留 exclusion log。ORAC、DPPH、ABTS、FRAP、CUPRAC、NRF2 potency、target/publication count 和期刊影响因子均未用于 candidate generation。

**Output：**`data/candidate_universe/Antioxidant_Class_Candidate_Master.csv` 收录 191 个候选，其中 178 eligible、13 unresolved；`data/candidate_universe/Antioxidant_Taxonomy_Relationships.csv` 有 36 条 panel/subclass relationship；`data/candidate_universe/Antioxidant_Candidate_Exclusions.csv` 保留 12 个排除项；`docs/class_specific_antioxidant/Phase2_Candidate_Universe_Summary_CN.md` 完成 coverage/bias audit。9 个 analysis panels 的候选数为 Flavonoids 59、Phenolic acids/conjugates 29、Stilbenes/lignans 15、Vitamins 10、Carotenoids 19、Organosulfur 15、Betalains/nitrogen-containing 11、Other phytochemicals 26、Minerals 7。

**Interpretation：**taxonomy 已从 pilot 结构升级为可供 Phase 3 使用的统一 candidate universe。Flavonoids、phenolic acids 和 other phytochemicals 可支持 Top20 起始筛选；其余类别应采用 Top10 或 all eligible，除非后续食物数据库审计新增足够候选。**Limitation：**多数 food-occurrence references 仍是 class/source-level 初筛，Phase 3 前必须完成 candidate-level 第二研究者核验；数据库存在明显地域偏倚。**Next step：**进入 Phase 3，在完成 candidate-level food-occurrence second review 和 identity/form lock 后，按 class-specific primary construct 开始 Top-N ranking。第一批从 Polyphenols–Flavonoids 开始。

### Future phases frozen in the workflow

Phase 3 是 class-specific Top-N ranking；Phase 4A 是 Global Top Overview，只并列展示 class-specific rank、within-class percentile、primary metric、confidence、dietary exposure 和 mechanism profile；Phase 4B 是 Cross-Class Comparability Matrix，明确可直接比较、仅可 profile 比较和不可数值混排的维度；Phase 4C 才从各类 Top-N 选择 Representative Cross-Class Experimental Panel。任何阶段都不得创建 ORAC z-score + carotenoid score + NRF2 score、assay simple average、ORAC × exposure 或 journal-IF-weighted global score。

## 9. Updated current project status

**Completed：**taxonomy v1.0、Stage 0–16 历史整理、Phase 2 candidate universe、taxonomy relationships、exclusion audit，以及 Phase 3A Flavonoid Top20 v1.0。**Provisional：**Flavonoid榜基于 A/B1 历史 ORAC-FL；Tier A=0，且11个Top20候选为单研究估计。**Not completed：**其余类别 Top-N、Global Top Overview、cross-class comparability result、final experimental panel、target mapping 和完整机制 ledger。

## 10. Stage 18 — Phase 3A Flavonoid Top20 Ranking

**Purpose：**在完整 59-candidate Polyphenols–Flavonoids universe 中完成候选级 eligibility lock，并按 literature-derived H-ORAC-FL 建立当前 class-specific Top20。**Input：**Phase 2 candidate master、历史 H-ORAC evidence、A/B1/B2/C/X rubric，以及系统补检得到的原始 pure-compound records。**Method：**逐项锁定 identity/form/food occurrence；只用 AAPH–fluorescein–Trolox H-arm；保留 original value、单位、转换、independent experiment ID 和 exact location；A/B1 按 compound median 排序，confidence 独立标注；anthocyanins因未解决 optical interference 最高 B2。

**Output：**57 eligible_for_ranking、2 hold；evidence master 94 rows（A=0、B1=53、B2=5、C=7、X=29）；25 compounds具有A/B1数值，形成不降标准的 Top20。前五为 epicatechin、catechin、gallocatechin、apigenin、isorhamnetin。Top20 confidence 为 High=4、Moderate=5、Low=11。**Interpretation：**该榜只表示 broadly comparable historical H-ORAC-FL chemical capacity；高位单研究值不等于稳健，且不能外推人体效果。**Limitation：**Tier A仍为0；11个单研究估计；quercetin/catechin异质性高；anthocyanins及多类glycosides覆盖不足；新增来源待 Zotero local import。**Next step：**研究者完成第二人复核后进入 Phase 3B Phenolic acids/conjugates Top-N。

## 11. Stage 19 — Phase 3B Phenolic Acids / Conjugates Top-N

**Purpose：**在完整 29-candidate `Polyphenols - Phenolic acids / conjugates` universe 中完成候选身份与 positional-isomer lock，并按 literature-derived H-ORAC-FL 生成 class-specific Top-N。**Input：**Phase 2 candidate master、历史 audited phenolic-acid records、A/B1/B2/C/X rubric 和 Phase 3B original-paper targeted search。**Method：**free acids、esters/conjugates 和 caffeoylquinic positional isomers 分开；只纳入 identity-resolved pure-compound AAPH–fluorescein–Trolox H-arm；one independent experiment=one row；统一到 mol TE/mol；A/B1 用 compound median 排序，confidence 与 magnitude 分开；generic chlorogenic records 不静默映射。

**Output：**25 eligible_for_ranking、4 hold；evidence master 47 rows（A=0、B1=34、B2=1、C=0、X=12）；18 compounds 有 A/B1，因此输出 Top available 18，不声称 Top20。前五为 rosmarinic、caffeic、gentisic、protocatechuic、vanillic acid；confidence 为 High=1、Moderate=9、Low=8。**Interpretation：**该榜仅表示 broadly comparable historical H-ORAC-FL chemical capacity；rosmarinic 的首位是 single-study estimate，不能解释为“最强抗氧化剂”。**Limitation：**Tier A=0；8个single-study；7个候选呈高历史异质性；4个candidate locks和1条chlorogenic mapping待人工裁决；单实验室覆盖集中。**Next step：**完成 Human Review Log 与第二研究者复核，优先补 single-study/high-heterogeneity/missing candidates；当前只可设计 Global Top Overview schema，不生成跨类排名。

## 12. Stage 20 — Global Top Overview Schema Pilot

**Purpose：**验证未来所有 class-specific Top-N 能否在不统一 assay 数值、不建立 global score 的前提下进入同一并列展示结构。**Input：**Phase 3A Flavonoids Top20 v1.0 和 Phase 3B Phenolic acids / conjugates Top available 18。**Method：**一行一个 compound；保留 identity、analysis panel、within-class rank、rankable N、类内 percentile、原始 primary construct/value/unit、evidence depth、confidence、heterogeneity、stability、assay/identity caveat 和 provenance；未来 exposure、PK、human、mechanism、target、安全与 tractability 字段统一使用 `Not reviewed`/`NA`，禁止把 missing 写成 no evidence。类内 percentile 定义为 `100 × (N-rank+1)/N`，只表示各自类内位置。

**Output：**`Global_Top_Overview_Master_v0.1.csv` 含 38 行；`Cross_Class_Comparability_Matrix_v0.1.csv` 定义 16 个维度，其中 6 个在共同单位/rubric 下可较直接比较、5 个只能 profile comparison、5 个不得直接数值混排。Evidence stability 为 Stable=5、Moderately stable=5、Fragile=28。四张 schema 图展示 class leaders、stability、comparability 和 future-field missingness。**Interpretation：**统一数据结构可行，但它是 side-by-side overview，不是统一排行榜。**Limitation：**两个输入都是 H-ORAC-based polyphenol panels，不能验证 schema 对 singlet-oxygen、lipid-phase、NRF2-regulatory 或 cofactor constructs 的适配性；未来字段尚未review。**Next step：**建议先完成 Carotenoids class-specific ranking，作为首个 non-H-ORAC construct stress test；本阶段不自动执行。

## 13. Next step

下一步有两个可选方向：Option A 为 Vitamins ranking，需先处理 vitamin C 与 tocopherol/tocotrienol 的 H/L 与 construct 分层；Option B 为 Carotenoids ranking，可直接测试 singlet-oxygen/lipid-phase metric、光学干扰和溶解聚集风险。为验证 Global Overview 对 non-H-ORAC constructs 的兼容性，优先推荐 Option B。开始前仍需研究者审核 Stage 20 schema；不生成 global rank、跨类总分、实验 panel 或 target mapping。

## 14. Stage 21 — Phase 3C Carotenoids Top-N

**Purpose：**完成首个 non-H-ORAC class-specific ranking，并检验 Global Overview 能否容纳不同 primary construct。**Input：**Phase 2 中 19 个 Carotenoids candidates、direct singlet-oxygen quenching 原始研究、膜模型研究和既有 A/B1/B2/C/X 证据治理结构。**Primary construct decision：**carotenoids 以直接 singlet-oxygen physical quenching rate constant `kq` 为主，H-ORAC-FL 不作为主指标；不同 organic-solvent、micelle、liposome 与 membrane systems 不默认 pooled。

**Evidence and method：**candidate lock 后有 17 个可继续审计，astaxanthin 与 fucoxanthin 因 dietary gate hold。环境审计显示 homogeneous organic-solvent `kq` 的覆盖足以产生 9-compound Top available，而 membrane/liposome quantitative evidence 仍太稀疏，故 organic-solvent layer 被选为 provisional primary environment；该选择是 chemical-quenching construct，不代表生物膜效能。只有 isomer-resolved、原始 `kq` 可追溯且环境清楚的 A/B1 records 聚合；generic names 不映射到 defined cis isomers。

**Output：**`data/candidate_universe/Carotenoid_Phase3_Eligibility_Lock.csv`、`data/class_specific_antioxidant/Carotenoid_Singlet_Oxygen_Evidence_Master.csv`、`data/class_specific_antioxidant/Carotenoids_TopN_v1.0.csv`、secondary lipid profile 与 `Global_Top_Overview_Master_v0.2.csv`。当前 rankable N=9，故输出 Top available 9 而不声称 Top10；前列为 all-trans-lycopene、canthaxanthin、alpha-carotene、all-trans-beta-carotene 与 zeaxanthin。英文方法学文件正式说明 unified framework 不等于 unified assay。

**Limitation and interpretation：**Tier A=0；4 个候选为 single-study；有机溶剂、温度、viscosity 与生成方法仍存在差异；xanthophyll aggregation 和 membrane localization 会显著改变观察值；phytofluene 还存在 UVA photosensitization。所有结果仅表示历史环境分层 direct `kq`，不得外推人体获益或建立 global antioxidant score。**Next step：**完成第二研究者对 dietary gate、cis/trans identity 和 full-text values 的复核；随后建议进入 Vitamins class，并先拆分 vitamin C aqueous construct 与 vitamin E lipid-phase construct。

## 15. Stage 22 — Phase 3D Vitamins / Vitamin-like Antioxidants

**Purpose：**验证同一营养 parent class 内是否可以并存多个 mechanistically coherent ranking subpanels。**Input：**Phase 2 的 10 个 vitamin candidates、历史 ascorbate H-ORAC-FL records、tocopherol/tocotrienol chain-breaking kinetics、L-ORAC 与 membrane/liposome studies。**Primary construct decisions：**Vitamin C aqueous 暂以可追溯 H-ORAC-FL 为 primary；Vitamin E lipid-phase 由研究者确认采用 vitamer-specific peroxyl-radical chain-breaking `k_inh`，L-ORAC 与 membrane assays 为 secondary profiles。

**Output：**`Vitamin_Phase3_Eligibility_Lock.csv` 将 10 个候选拆为 aqueous N=2 与 lipid-phase N=8；dehydroascorbic acid 因缺少可比 primary record 且不能替代 ascorbate 而 hold。L-ascorbic acid 的两条 B1 值 median=0.74 mol TE/mol，输出 all eligible 1；singleton percentile 依研究者决定写为 NA。Vitamin E 以 α、γ、β、δ chain-breaking rate tiers 形成 Top available 8，tocopherol 与对应 tocotrienol homologues 当前并列。`Global_Top_Overview_Master_v0.3.csv` 新增 `analysis_subpanel`，只计算 subpanel percentile，不生成 Vitamins parent-class percentile。

**Interpretation and limitation：**“Vitamin”是营养分类，不是统一 redox mechanism。H-ORAC-FL 与 `k_inh` 不共用 raw axis；regeneration 不进入 capacity rank。Vitamin E 的八个候选目前均 Low confidence/Fragile，原因是 eligible kinetics 集中于少量经典研究，tocotrienol values 依赖 corresponding-homologue equivalence，且天然 stereochemistry 与 generic/synthetic records 必须继续分开。**Next step：**完成全文与第二研究者 identity review；建议下一类进入 Organosulfur，以测试 causal KEAP1/NRF2 和 thiol-reactivity construct。

## Supervisor Scope Reset — Aqueous Focus (Stage 23)

**Purpose：**按导师要求把当前 active mainline 收束为 aqueous antioxidant atlas，并把既有排名值的原始文献溯源集中到统一 record-level master。**Scope decision：**Flavonoids、Phenolic acids/conjugates 和 Vitamin C 进入完整 evidence consolidation；Stilbenes/lignans、Betalains、Organosulfur、Other aqueous phytochemicals、metal-ion mechanisms 与 micronutrients 本轮只建立 candidate framework、construct proposal、assay-risk、preliminary anchor literature 和 evidence-gap list。**Paused by supervisor scope decision: current active project restricted to aqueous-phase antioxidant evidence.** Existing carotenoid and vitamin E outputs remain valid historical class-specific results and are retained as supporting/non-active results.

**Method：**从既有 class masters 和 provenance IDs 重建 `Aqueous_Antioxidant_Primary_Literature_Evidence.csv`，保留 original value、unit、conversion formula、molecular weight、normalized value、DOI/PMID、exact table/figure/page、independent experiment ID 与 Zotero key；新增 anchor records 明确标为 preliminary/non-ranking。candidate generation 不按数值反向筛选，micronutrients 不进入小分子 capacity ranking，Fe/Cu chelation 与 Fenton context 作为机制维度单列。

**Output：**aqueous candidate master 157 行；统一证据表 109 行；paper summary 25 个去重论文单元，其中 24 个有 DOI；micronutrient redox profile 7 行；建立水相 Atlas 分层图目录及 5 张 overview 图。当前数值排名没有重算或改名次，脂相数据没有删除。

**Interpretation：**本阶段完成的是 active-scope reset 与 provenance consolidation，不是新的跨类别排名。只有 flavonoids、phenolic acids/conjugates 和 vitamin C 的 current ranking 可以由 record-level 数据逆向追溯；其余水相类别仍是 future staged review。**Limitation：**一个历史 figure-only supporting source 仍缺 DOI；若干 Zotero keys 仍为 `pending_local_import`；preliminary anchor literature 不等于 systematic coverage。**Next step：**完成双人复核和 Zotero 补录后，再按 class 分阶段开展 systematic primary-literature extraction。

## Stage 24 — Complete Aqueous Class-Specific Ranking

**Purpose：**在不改变 Stage 23 冻结候选宇宙的前提下，为所有 active aqueous classes 完成可审计的 class-specific ranking 或科学合理的 profile-only 输出，并形成统一图包。**Scope：**固定 157 个 candidates；本阶段不得新增候选，检索发现的潜在漏项仅写入 `Future_Candidate_Additions_Log.csv`。Flavonoids、phenolic acids/conjugates 与 Vitamin C 沿用已冻结主构念和排名；stilbenes/lignans 与 other aqueous phytochemicals 的方法学一致 H-ORAC subpanel允许数值排序；betalains、organosulfur、metal-ion mechanisms 与 micronutrients 保留独立 profile。暂停的 carotenoid、Vitamin E 和其他 lipid-phase outputs继续保留，但不扩展。

**Primary constructs and systematic status：**H-ORAC-FL只用于方法学可比的水相direct-capacity records；betalain pigments采用 LOX-FL 与 MPO/HOCl assay-specific profile；organosulfur采用 KEAP1/NRF2、thiol chemistry、Fenton 与 radical-kinetic profile；metal层严格区分binding/chelation、metal reduction、Fenton/Fenton-like suppression与net oxidative endpoint；micronutrients按cofactor、人体验证和促氧化/毒性context呈现。Stage 24 对67个尚未完成panel candidates逐一记录检索，另外90个已完成panel candidates继承Stage23结构化证据，最终形成157行检索日志。Review只用于发现原始研究，不直接决定rank。

**Ranking and figure outputs：**stilbenes/lignans仅2个候选具有B1数值，输出 trans-resveratrol、sesamol 的Top available 2；other aqueous phytochemicals仅在mechanistically coherent H-ORAC subpanel输出 zingerone、eugenol、tyrosol、carvacrol、thymol 的Top available 5。两榜均为Low/Fragile single-study evidence。Betalains与organosulfur不强制生成虚假统一榜。统一evidence master扩展至130行，paper summary扩展至34个DOI/source units。Atlas目录00–09及99_methods_qc均有图或状态说明；overview只显示within-panel位置，不产生global antioxidant scale。

**Metal/mineral handling：**metal evidence master包含8条机制记录，micronutrient v2 profile包含Se、Zn、Mn、Cu、Fe、Mg、Mo共7个节点；两者均不进入ORAC排序。**Limitations：**新增可排名类别没有Tier A，且全部数值记录为single-study B1；betalain存在光学与pH依赖，organosulfur不同构念不可合并；metal oxidation state和net endpoint需要第二研究者核对；一个legacy figure-only source仍无DOI，部分Zotero key仍待本地导入。

**HUMAN REVIEW REQUIRED：**Podophyllotoxin的正常膳食与aqueous-scope gate、Probetanin缺失的PubChem CID/InChIKey、Ubiquinone-10的aqueous-scope合理性均未被Codex静默修改；betalain optical QC、organosulfur dietary gates以及Fe/Cu oxidation-state annotations也需人工裁决。**Next step：**研究者先审核上述事项、single-study榜与图包，再决定是否扩充原始文献或冻结下游实验/target-mapping输入；Stage 24不自动进入target mapping、global score或lipid expansion。

## Stage 25A — Unified Literature-Evidence Screening

**Purpose：**在冻结的157个aqueous candidates中，用统一、与抗氧化强度分离的文献指标描述research maturity，为后续Stage 25B H-ORAC检索缩小工作范围。**Method：**Europe PMC执行候选标题identity anchor与antioxidant/redox题名/摘要检索；排除review及非original类型、docking-only、不可归因extract和重复索引；DOI/PMID/规范化标题去重后的publication count作为当前independent-publication proxy。OpenAlex前置coverage audit为37/37 matched、37/37 citation metadata available，因而冻结为sole citation source。

**Output：**157行screening master、45,643行candidate×publication provenance（其中41,967条纳入primary metric）、检索日志、cutoff/class sensitivity、OpenAlex unmatched与分层coverage表，以及6张R图。全量有标识符记录40,233条，OpenAlex matched 40,193条，matching rate 99.90%；matched-work citation availability为100%，class/年代/identity strata均通过95%。主榜前五为Curcumin、L-Ascorbic acid、Quercetin、Epigallocatechin、Gallic acid；这表示research density，不表示抗氧化能力。

**Cutoff recommendation：**Top50累计覆盖91.42%的publication proxy，primary-vs-citation重叠49/50、primary-vs-recent重叠46/50，并保留七个aqueous panels，因此建议作为provisional Stage25B retrieval frame。该建议没有class quota，且不自动使不适合H-ORAC的候选获得资格。Stage25B readiness为Ready 86、Conditional 45、Not suitable 24、Insufficient identity 2；11个candidate-universe问题继续标记HUMAN REVIEW REQUIRED。

**Limitations and stop point：**元数据自动筛选不能完全确认candidate experimental exposure、same cohort/experiment拆分发表或全文redox endpoint，因此`antioxidant_independent_publication_N`仍是provisional metadata-level proxy。进入Stage25B前应对Top50进行双人分层抽样和rank-changing error audit。本阶段不启动H-ORAC批量抽取，不建立composite score，也不把publication/citation density解释为potency、quality或human efficacy。

## Stage 25A.1 — Pre-Stage25B QC, Top50 Freeze Audit and Full-project Reorganization

**Purpose：**在不启动Stage25B检索的前提下，完成Top50 targeted metadata QC、冻结可进入H-ORAC retrieval的候选集合、修复Stage25A图形轴错误，并把Stage0–25A全部科学资产从以Stage为主的分散结构重组为按当前科学功能组织的可审计项目。**Inventory-first rule：**实际迁移前登记362个文件并逐项分类：ACTIVE_CANONICAL 110、ACTIVE_SUPPORTING 85、SUPERSEDED 49、HISTORICAL_ONLY 118；完整old→new path、canonical replacement、reason和dependency risk保存在`PROJECT_FILE_MIGRATION_MAP.csv`。仍在使用的早期assay methodology、H-ORAC framework、candidate scope、T1–T5 target framework、SOP、模板与checklist保留为active supporting；旧版本只迁入archive，不删除、不重算。

**Metric correction and QC：**Stage25A主计数字段正式表述为`metadata_deduplicated_original_publication_N`；旧字段仅为向后兼容，不再作为正式名称。Top50逐候选targeted QC得到include-ready 31、include-conditional 12、hold-human-review 4、exclude-not-suitable 3；因此Stage25B H-ORAC retrieval-eligible集合当前为43个，且明确不从第51名开始递补。Thymoquinone、Baicalein、Chrysin和Plumbagin保留scope/dietary gate人工裁决；Sulforaphane、Caffeine和Allicin不适合当前H-ORAC retrieval construct。该审计是metadata-level targeted review，不替代41,967条记录的全文独立实验核验。

**Reproducibility and output：**旧的monolithic plotting script迁入`archive/R_legacy/plot_antioxidant_atlas_pre_modularization.R`，active绘图改为common helpers、按科学模块分拆的R scripts和薄入口`R/render_all_active_figures.R`。29/29张active canonical figures均由登记输入成功重建。两张异常图的根因是log10坐标下数值型label nudge造成二次尺度失真；错误版本保留在`archive/figure_qc_stage25A1/`，canonical replacements仅使用一次log transform。当前active组织以candidate universe、class-specific antioxidant、literature screening、metal/micronutrients、methods/QC、supervisor、sync与references为主；Stage编号继续保留在本文件、`docs/PROJECT_STAGE_INDEX_CN.md`和provenance metadata中。

**Stop point：**Stage25B未启动。下一步必须先由研究者处理4个HUMAN REVIEW scope/dietary gates并确认43-candidate retrieval frame，再按冻结的H-ORAC eligibility规则开展定量文献检索。

## Stage 25A.2 — Final Project Information Architecture Audit

本阶段只审计logic、redundancy、canonicality、traceability与archive hygiene，不改变科学结果。审计基线为411个tracked files（active 239、archive 172）；active exact与normalized-text semantic duplicate均为0。发现的一个canonicality conflict是micronutrient v1/v2同时active，另有三个已被Stage25A.1取代的历史sync assets仍在active区；四项均可逆归档并更新migration map。当前62项canonical registry路径唯一存在，29张canonical figures分别承担独立的magnitude、robustness、coverage、mechanism、risk或screening-sensitivity信息，没有新增figure/R redundancy。

Archive保留177个tracked files，其中5组byte-identical pairs标记`HUMAN REVIEW REQUIRED — ARCHIVE RETENTION`，未自动删除。Figure→R→direct Data为29/29完整；candidate food occurrence缺逐行authority identifier以及Stage25A未完成全文same-experiment adjudication继续作为科学provenance limitation保留。结论是active project architecture可以冻结；Stage25B仍未启动。

## Stage 25A.1 Human Review Resolution

研究者确认candidate-universe采用宽food-source provenance gate：明确化学身份与可追溯food-derived origin足以纳入；暴露量、habitual intake、dose realism、药用植物主导、安全性、促氧化风险和translation value均转入下游评价。Thymoquinone、Baicalein、Chrysin和Plumbagin因此由`HUMAN REVIEW REQUIRED — CANDIDATE UNIVERSE`全部更新为INCLUDE，冻结的157-candidate membership没有增删。

本轮不新增检索，只依据既有canonical records与H-ORAC rubric裁决方法适用性。四者均为Conditional：Baicalein与Chrysin需解决aglycone identity、有限水溶性/cosolvent及fluorescence interference；Thymoquinone与Plumbagin需受控cosolvent、浓度、聚集和光学QC，Plumbagin另保留redox cycling、促氧化、细胞毒性及dose-translation风险。四者进入Stage25B retrieval set但不被改写为Ready。Stage25A ranking/count hash前后完全一致，Top20/30/40/50/60 membership不变；retrieval set由43增至47（Ready 31、Conditional 16、Not suitable 3、unresolved review 0）。Stage25B状态为READY但尚未执行。

## Stage 25B — Systematic H-ORAC-FL Retrieval（current audit stop）

2026-09-21对冻结的47个候选执行统一Europe PMC检索，并将既有H-ORAC evidence master迁移为publication-level与experiment-level两层数据。当前形成3,115条candidate×publication screening rows和71条experiment rows；A=0、B1=66、B2=4、X=1，基于已核查A/B1的interim rankable candidate N=26。新增Baicalein全文证据数值为5.41±0.33 mol TE/mol，但因chromophore optical blank/correction及solubility/aggregation QC不足按冻结rubric判为B2，不进入primary rank。加入B2会改变Top20 membership，且仍有1,657条命中待全文方法裁决与第二审核，因此当前`TOP20 CUTOFF UNSTABLE`，Stage25B不得冻结。冻结的157 candidate universe、Top50、47 retrieval input及Stage25A rank/count均保持不变；当前停止状态为`STAGE25B BLOCKED — METHOD / IDENTITY / PROVENANCE ISSUE`。

## Stage 25B.1 — Rank-Relevant Full-Text Adjudication

Stage25B checkpoint以九个文件副本和SHA-256 manifest冻结后，对1,657条pending records建立互斥Priority 1–5。两个高信息增益batch实际改变16条原queue rows的adjudication status，并对Baicalein等已出queue但rank-changing的记录复核。开放全文`10.3390/foods10081807`新增Eugenol、Capsaicin、Vanillin三条B1，experiment rows 71→74、B1 66→69、rankable candidates 26→29；三者均低于Top20 cutoff，primary membership不变，但Eugenol进入rank25并使Ellagic acid移至26。Baicalein维持B2；若单独纳入会替换primary rank20 Ferulic acid，完整B2 sensitivity仍改变3个Top20成员。共享cutoff来源仍有SOURCE_NOT_RECOVERED，A=0的feasibility需研究者判断且rubric未修改。停止规则未满足，状态为`STAGE25B.1 HUMAN REVIEW REQUIRED`；不生成正式Top20 figure。
