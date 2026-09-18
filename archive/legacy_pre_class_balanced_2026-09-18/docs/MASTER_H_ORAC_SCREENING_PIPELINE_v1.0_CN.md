# MASTER H-ORAC SCREENING PIPELINE v1.0

版本：1.0；状态：组内执行标准；适用对象：未参与本项目、需要独立完成人工筛选的研究生。本文是总入口。科学规则以 `Antioxidant_Screening_Protocol_v2.0_CN.md`、`Antioxidant_Screening_Protocol_v2.1_Addendum_CN.md` 和本 MASTER 为顺序解释；发生冲突时采用更新且范围更具体的文件，并将冲突登记到 `Pipeline_Gaps_and_Inconsistencies_CN.md`，禁止静默合并。

## 1. 目的、范围与边界

本流程比较正常膳食来源、结构明确、适用于 H-ORAC-FL 的食源性 phenolic/polyphenolic 单体的 literature-derived chemical antioxidant capacity。操作性定义为：单体在可比的 AAPH–fluorescein–Trolox H-ORAC 条件下，对 AAPH 衍生过氧自由基引起的 fluorescein 氧化所表现的 kinetic integrated chain-breaking capacity，以 mol Trolox equivalents/mol compound 表示。

本流程不回答人体抗氧化疗效、临床获益、生物利用度、疾病预防、细胞 redox regulation 或最终实验价值。L-ORAC、tocopherols、tocotrienols、carotenoids、organosulfur compounds 和 target mapping 不在当前 SOP 范围。维生素 C只能作为非多酚 benchmark，不占酚类排名名额。

核心术语：record 指一个化合物在一个独立实验和一个 assay arm 中的一项结果；eligible record 指 Tier A 或 B1；candidate universe 是先于结果建立的候选全集；provisional ranking 是历史文献探索性排名；confidence 描述证据深度，不描述容量大小；readiness 描述是否适合交接下游研究，不等同于排名。

## 2. 总流程

Scientific question → candidate universe → literature search → assay identity check → compound identity QC → record extraction → unit normalization → tier adjudication → independent experiment QC → compound aggregation → confidence → provisional ranking → evidence consolidation → before/after stability → Ready/Conditional/Not ready → downstream target-mapping handoff。

每一步实行“输入冻结—人工操作—规则判定—结构化输出—QC签名—停止条件”六段式。原始值永不覆盖；排除记录保留；任何影响名次的改动必须双人复核并写 change log。

## 3. 顺序化执行规范

### Step 0 — Define the scientific question

输入：研究目的和 protocol。操作：把比较对象、assay construct、单位和非目标写入项目说明。判断：若问题包含人体功效或跨 H/L 混排，停止并拆分问题。输出：带版本号的 scope statement。QC：第二人确认 chemical capacity 与 biological effect 已分开。自动化：manual only。下一步条件：一句话问题可被不同成员一致复述。

### Step 1 — Build candidate universe

输入：冻结范围、食品成分数据库和化学结构数据库。操作：逐项记录 canonical name、synonym、PubChem CID、InChIKey、subclass、food occurrence、parent/glycoside 和 stereochemistry。候选生成不得由 ORAC 高低反向决定。输出：candidate universe CSV。QC：结构唯一、膳食来源可追溯、糖苷/苷元不合并。脚本：`fetch_h_orac_pubchem.py`只辅助 PubChem 字段；人工确认仍必需。下一步条件：所有候选都有唯一结构或明确标为待解决。

### Step 2 — Literature search

输入：候选全集。人工检索模板：`"compound name" AND ORAC`；`"compound name" AND "oxygen radical absorbance capacity"`；`"compound name" AND AAPH AND fluorescein`；`"compound name" AND ORAC-FL`。依次查 PubMed、Google Scholar、Crossref/DOI、期刊页面和 supplement。Review 只用于发现原始来源：沿参考文献号定位 original article，再在原文核对数值和方法。输出：`Literature_Search_Log_Template.csv`。QC：每个候选留下检索日期、原式、筛选数和排除原因。自动化：manual only。下一步条件：能证明“未找到”来自已执行检索。

### Step 3 — Verify assay identity

输入：原文方法和 supplement。逐项确认 pure compound、AAPH、fluorescein、Trolox、H-arm。β-phycoerythrin、HORAC、L-ORAC、food/extract ORAC、figure-only无法精确提取、review-only 数值均不能成为 B1。输出：eligibility checklist 与 exclusion log。QC：探针名、radical generator、arm和样品类型必须从原文定位。自动化：manual only。下一步条件：assay identity 可明确判定或进入 X。

### Step 4 — Verify compound identity

输入：原文试剂信息、PubChem/ChEBI。核对 canonical name、synonym、CID、InChIKey、MW、salt/hydrate、stereochemistry、glycoside/aglycone。典型禁止合并：quercetin/quercitrin/rutin；catechin/epicatechin；genistein/genistin；cyanidin/cyanidin-3-O-glucoside。输出：身份字段和 identity QC 结论。QC：第二人逐项复核。下一步条件：可唯一映射；否则 C 或 X。

### Step 5 — Extract record-level evidence

输入：通过初筛的原文。规则：one independent experiment = one row，不是 one compound = one row；同论文不同化合物可各一行，同化合物不同 arm 或实质独立实验分行。完整字段使用 `ORAC_Record_Extraction_Template.csv`。必须记录 DOI/PMID、exact location、原值、原单位、关键方法、提取者和日期。输出：record-level CSV。QC：原值与原文逐字符复核。自动化：manual extraction；脚本不读取论文。

### Step 6 — Unit normalization

标准单位为 mol TE/mol compound。若原值为 µmol TE/g：`mol TE/mol = (µmol TE/g × MW g/mol) / 1,000,000`。例：14,272 µmol TE/g ferulic acid，MW 194.18 g/mol，结果为 14,272×194.18/1,000,000=2.771 mol TE/mol。始终保留 original value、unit、MW source、formula、converted value、reviewer 和 `conversion_verified`。盐/水合物必须使用实验所用 form 的MW。输出：标准化字段。QC：独立复算并控制有效数字。下一步条件：转换可解释；否则 B2/C/X。

### Step 7 — Evidence tier adjudication

Tier A：身份、ORAC-FL、H-arm、AAPH、fluorescein、Trolox、介质、温度、读数/AUC、线性、纯度、干扰和单位足以支持高置信正式比较。Tier B1：满足 pure defined compound、original ORAC-FL、H-arm、Trolox、可提取且可转换的原值、主要条件可识别、无明显未解决严重干扰、原文可追溯；可缺少少量非关键参数。Tier B2：有定量值但 metadata、兼容性或干扰控制不足，不进入主排名。Tier C：已知不兼容，例如错误探针、错误 arm、extract/food value 或不可统一单位。Tier X：信息不足，尚不能判定。Tier 衡量 comparability/eligibility，不是期刊质量。输出：tier+rationale。QC：双人独立判级。

### Step 8 — Independent experiment adjudication

输入：全部候选记录及引用链。same experiment reused、review citation、same dataset、同一表格重复发表均不独立；真正分开的实验研究才独立。创建稳定的 `independent_experiment_id`，建议 `FIRSTAUTHOR_YEAR_DOI_ASSAYARM_EXPERIMENT`。同一 ID 对同一 compound 只计一次。输出：independence 字段和排重日志。QC：比较作者、实验室、批次、方法、数值和引用来源。下一步条件：每项 eligible record 有经复核的ID。

### Step 9 — Compound-level aggregation

输入：去重后的 A/B1。一个候选有≥2项时报告 n、median、min、max；n≥4时报告 IQR；一项时标记 single-study。禁止最大值、选择“最好看”数值或对不兼容 protocol 任意均值。输出：compound summary。脚本：现有 `build_h_orac_top20.py` 和 `build_top20_consolidation.py`含项目特定聚合逻辑，运行前必须审查输入和硬编码来源。QC：人工用 Excel 抽查至少3项。

### Step 10 — Evidence confidence

High：≥3 independent A/B1 且无高异质性或重大方法冲突；Moderate：2 independent A/B1；Low：1 A/B1；Very low：只有 B2，不进入主榜。若≥3但异质性高，不能自动 High，须降级或人工说明。Confidence 与 ORAC magnitude 不合成总分。输出：confidence 与理由。

### Step 11 — Provisional ranking

按 median mol TE/mol 降序。保留 rank、A/B1数、confidence、single-study、heterogeneity和special-case flag。相同中位数不得用论文数量伪造差异，可并列或按预设稳定规则并记录。输出：版本化排名 CSV 和图。脚本：`build_h_orac_top20.py`；当前实现含项目数据硬编码，仅适合复现本项目版本，不是通用引擎。QC：重新排序、检查20项、确认 benchmark不占名额。

### Step 12 — Evidence consolidation

触发条件：Top candidate仅一篇；重要候选缺失；subclass低覆盖；异常值；排名不稳定。执行定向原始文献追溯，不降低B1标准。记录新增、排除、纠错和未找到。输出：consolidation records、missing-important list和change log。脚本：`build_top20_consolidation.py`可复现当前 consolidation，但文献判断是人工的。

### Step 13 — Before/after stability check

输入：两个冻结排名版本。输出 rank_before、rank_after、rank_change、B1 count change、confidence change、entered/exited Top20；说明变化来自新增独立证据、纠错还是补强。QC：新旧文件只读，禁止覆盖。脚本：`build_top20_consolidation.py`。

### Step 14 — Freeze shortlist

Ready：Top20内，≥2 independent B1或有明确稳定性证据，身份清楚，无重大未解决 assay concern。Conditionally ready：single-study B1、排名合理但证据薄。Not ready：无B1、重大光学/溶解/身份问题。Ranking 与 readiness 是两种输出，绝不合成。输出：版本化 shortlist 与签字冻结记录。

### Step 15 — Handoff to downstream target mapping

交接前必须具备 canonical name、CID、InChIKey、form/stereochemistry、rank、median、eligible count、confidence、assay risk、readiness、key DOI/PMID、Zotero key或明确 pending 状态、record IDs和provenance路径。本 SOP 到此停止，不执行 target extraction。

## 4. QC、人工复核与常见错误

身份、tier、原始数值、换算、独立性及任何改名次的纠错必须双人复核。常见错误详见 `Common_Failure_Modes_H_ORAC_CN.md`；可打印筛查表为 `ORAC_Eligibility_Checklist_CN.md`。程序可以进行单位计算、分组统计、排序、制图和字段完整性检查；assay identity、光学干扰、化合物 form、文献独立性和 tier 必须人工判断。

## 5. 文件、命名与版本

原始文件进入 `raw/`，人工抽取进入 `extracted/`，派生结果进入 `processed/`，正式发布副本进入 `data/`。推荐命名：`H_ORAC_<artifact>_vMAJOR.MINOR_YYYYMMDD.csv`。Protocol科学规则变化升 major；数据追加且规则不变升 minor；排版修订升 patch。禁止 silent overwrite；旧版移入 `archive/`但不删除。每个派生文件记录生成脚本版本、输入文件哈希或文件名、时间、提取者和复核者。

## 6. 数据溯源与进入下一阶段

最终 rank 必须能够逆向到 compound summary → eligible record → independent experiment ID → original paper → DOI/PMID → exact table/page → original value/unit → MW与公式 → standardized value。任何一环缺失都必须标为 gap。只有完成双人复核、排除日志、change log、before/after稳定性和shortlist冻结，才能移交 target mapping。详细逆向示例见 `Data_Provenance_Chain_CN.md`。
