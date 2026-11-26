# 工作区完整梳理（2026-11-26 快照）

> 性质：导航 / 盘点快照，保留早期工作区状态，供查阅历史。现行导航及科学进度见 [README.md](README.md) 和 [Latest_Results.md](Latest_Results.md)。
> 快照时点：分支 `codex/systematic-antioxidant-evidence-20261117`，HEAD `1c69056`（2026-11-24 "Publish editable screening workflow with search terms and model"）。
> 所有数字均取自仓库内当前文件与 git 实测，未做新的科学判断。

---

## 1. 项目定位

**食源性抗氧化候选物筛选**（Food-derived antioxidant candidate selection）：从食物 / 膳食来源中识别「定义明确、食物存在可溯源、预期水相抗氧化容量高、且有可重复原始证据」的单一化合物，为前瞻性吸光度法实验验证准备候选面板（目标预算 20 个材料）。

核心科学边界（见 [Protocol.md](00_project/Protocol.md)、[Decision_Register.md](00_project/Decision_Register.md)、[scope.json](00_project/scope.json)）：

- 发现（discovery）先于活性排序；191 个原始命名种子是可审计输入，不是穷尽式食物化学普查。
- 排除未定义混合物 / 提取物 / 聚合测定变量；仅药物 / 补充剂用途支持的物质排除；内源性出现本身不构成排除理由。
- 化学容量 ≠ 细胞 / 生物功效 ≠ 因果机制 ≠ 人体获益，四层证据严格分开。
- 期刊指标、论文数量不参与选择；不引入新的数值权重或综合评分。
- **尚未执行任何新测定实验**（QC：`new_assay_experiments_performed = 0`）；正式「实验室就绪面板」为 0 行，当前输出是评审队列与实验设计准备。
- 文件迁移 / 分支 / 重生成图表都不构成科学批准；历史 HOLD 与治理状态原样保留。

当前主交付：Part 1 论文（Nature Communications 风格 Word 稿）+ 条件 ORAC-FL 模型排序 + 按 ±10 名次稳定性规则保留的 **12 个候选物**。

---

## 2. 总体规模与目录地图

实测统计（含隐藏文件；MB 为十进制近似）：

| 目录 | 文件数 | 体积 | git 状态 | 角色 |
|---|---:|---:|---|---|
| `00_project/` | 378 | 19.4 MB | 跟踪 | 研究范围、协议、决策登记、环境 / 文件 / git 政策 + 历史研究记录档案 |
| `01_candidate_discovery/` | 5 | 0.1 MB | 跟踪 | 候选发现：191 种子重建 + 排除复筛 + 缺口补充 |
| `02_identity_and_evidence/` | 2,874 | 2,889 MB | 部分跟踪 | 身份认定与证据评估：检索、机筛、全文队列、来源清单（体积大头为本地检索缓存） |
| `03_candidate_selection/` | 386 | 50.8 MB | 跟踪 | 容量数据 harmonization、条件模型、排序与敏感性、12 个编号子研究 |
| `04_05_experimental_validation/` | 5,942 | 424 MB | 少量跟踪 | 实验验证设计（终点 / 试点 / 平台 / 应力测试）；其中 5,854 个文件是被忽略的本地 R 包库 |
| `06_manuscript/` | 161 | 8.7 MB | 跟踪 | 论文装配：Working Methods / Results、Figure 1 及组件图、Part 1 docx |
| `07_quality_control/` | 32 | 0.8 MB | 部分跟踪 | 科学不变量与可重复性校验、分支清单、QC 状态 |
| `download_raw/` | 2,947 | 199.5 MB | **整体忽略** | 用户提供的原始 PDF / 补充材料、迁移回放、机筛全量输出、WoS 机构导出 |
| `.venv/` | 3,678 | 137.8 MB | 忽略 | 本地 Python 3.12.10 虚拟环境 |
| `.git/` | 4,334 | 302.6 MB | — | 版本库（75 个提交，10 个本地分支） |
| 根部文件 | 5 | ~10 KB | 跟踪 | README.md、Latest_Results.md、run_pipeline.py、.gitignore、.gitattributes |

- 合计约 **20,700 个文件、~4.0 GB**；其中研究目录约 12,725 个文件、~3.5 GB。
- **git 实际跟踪 1,498 个文件**。其余 ~3.3 GB 为本地缓存 / 环境 / 原始下载（`.gitignore` 明确忽略），克隆后需按 [source_manifest.json](02_identity_and_evidence/source_manifest.json)（983 条 SHA256 登记）重新获取或另行传输；离线计算只依赖已捆绑来源。
- 文件政策（[File_Management.md](00_project/File_Management.md)）：按科学任务与执行步骤组织；编号目录表示研究顺序而非证据强度；原始来源字节不可变（`.gitattributes` 对来源目录 `-text`，活动文本统一 LF）；当前文档 / 代码 / 新叙述输出为英文，原始语言记录原样保存。

---

## 3. 研究主链：00 → 07 逐阶段

根命令 [run_pipeline.py](run_pipeline.py) 串起全链；`--literature` 走当前「检索 → 排序」10 步工作流，默认模式走历史描述性全链（含 R 图与可选 Node 工作簿）。

### 00_project — 研究范围与治理
- [Protocol.md](00_project/Protocol.md)：workflow v0.1（2026-11-05）+ 指向系统综述协议 v1.0 / 增补 v1.1（2026-11-17 起的六阶段任务）。
- [Decision_Register.md](00_project/Decision_Register.md)：关键在案决策——2026-11-23 研究者批准条件 ORAC-FL 排序 **±10 名次最大位移**保留规则；主目标为摩尔容量、速率单独报告；crocin 剂量-时间保护为第一方法验证候选；**无主要测定法获批**；800 mM AAPH 文献表述须先澄清。
- [Environment.md](00_project/Environment.md) / [Git_Workflow.md](00_project/Git_Workflow.md) / [File_Management.md](00_project/File_Management.md)：环境、分支与文件政策。
- `research_records/`（368 文件，19.3 MB）：历史科学档案，**不是当前执行入口**。含 `study_development/`（2026-09-18 / 09-20 / 10-15 / 10-16 四个日期批次，其中 09-18 为 legacy_pre_class_balanced 完整归档：协议 v1→v2.1、ORAC pilot / exploratory / Top20 证据整合、ChatGPT 交接文档等）、`source_assessments/methods/h_orac_framework/`（中英双语方法审计）、`decisions/2026-10-30/`、`phase1b_t002_readonly_audit/`、`track_b_robot_screening_v0.1/`、`evidence_build_scripts/`（stage25b 系列历史脚本）、`current_deliverables_phase1/`（治理 v0.1/v0.2 等）、`source_discrepancies/`（1 张历史图 22 vs 24 计数差异，待解释，见 Sources.md）。
- `exporters/build_review_workbook.mjs`：可选英文评审工作簿导出（Node + @oai/artifact-tool，非科学计算依赖）。

### 01_candidate_discovery — 候选发现（5 个文件）
- 入口 `code/01_build_universe.py`：只读取保留原始生成器中的字面策展声明（类别清单、名称、食物示例、排除），不执行遗留联网 / 排序代码；来源哈希写入每个重建种子行。
- 输出 [discovery_register.csv](01_candidate_discovery/results/discovery_register.csv)：**204 条发现记录 = 191 原始种子 + 12 保留排除复筛 + 1 麦角硫因缺口补充**；谷胱甘肽旧「仅内源」排除因 Jones 1992 食物分析摘要重新开放。
- 交接：稳定候选 ID → 02 身份与证据评审。

### 02_identity_and_evidence — 身份认定与证据评估（最大目录，2.9 GB）
- 主 README：[02 README](02_identity_and_evidence/README.md)；来源总指南：[Sources.md](02_identity_and_evidence/Sources.md)；来源哈希清单：[source_manifest.json](02_identity_and_evidence/source_manifest.json)（437 KB，983 条）。
- 编号子模块：
  - `01_systematic_supplement/`（2,119 文件，2.26 GB）：全候选公共补充检索模块。**inputs/（2.0 GB）与 fulltext_xml/ 被 git 忽略**：`stage2_v1_1/pubmed_v1`（572 文件，1.64 GB 原始 PubMed XML）、`minimum20_abstracts`（229 文件，149 MB）、`expanded_capacity`（193 文件，37 MB）等；跟踪部分为检索 / 恢复 / 快照脚本与 Master_Article_Register 等登记 CSV 的生成逻辑。
  - `02_user_supplied_sources/`（9 文件）：研究者提供的 7 份原始文献（含 60 黄酮补充材料），138 条唯一测定行；含来源冲突、参考修正（2004 槲皮素值更正、山奈酚关联排除）。
  - `03_date_scoped_review/`（48 文件，48.9 MB）：日期范围来源恢复日志、来源决策、精确糖苷提取。
  - `04_systematic_protocol_v1/`（18 文件）：[Systematic_Review_Protocol_v1.0.md](02_identity_and_evidence/04_systematic_protocol_v1/Systematic_Review_Protocol_v1.0.md) + [Protocol_Addendum_v1.1.md](02_identity_and_evidence/04_systematic_protocol_v1/Protocol_Addendum_v1.1.md)（GO WITH REVISIONS 后 governs Stage2 检索与筛选）、检索策略 / 资格规则 / 字段字典 / 决策登记。
  - `05_multidatabase_retrieval/`（67 文件，119 MB）：PubMed / Europe PMC / WoS 三库检索日志、导出清单、标识符对账、锚点召回、机构访问状态与导出交接说明（[Stage2_Manual_Export_Handoff.md](02_identity_and_evidence/05_multidatabase_retrieval/Stage2_Manual_Export_Handoff.md)）。
  - `06_machine_screening/`（3 文件）：机筛 README 与入口说明；全量输出写入被忽略的 `download_raw/stage2_machine_screening/`。
- `code/`（6 个脚本）：01_build_evidence_profiles → 02_screen_public_snapshot → 03_summarize_screening → 04_build_fulltext_batches（+ refresh_pubchem 等）。
- `inputs/`（587 文件，463 MB）：`mechanism_evidence/`（251 文件，88 MB，AFF-0061 机制证据与治理，跟踪且字节不可变）、`source_corpus/`（327 MB，stage25a 本地语料被忽略）、`reference_collection/`（37 MB，157 候选框架 D1–D5 快照与来源闭合）、`catalogue_reference/Evidence_Catalog_2026-10-30.xlsx`（9.3 MB）、`provenance/`（**冻结 Results 1 v1.0 参考**：304 条原始观测、225 条测定内参考排序、证据快照、数据字典；原发布可从 commit `5ee3bc8` 回放）、`identity_reference/` + PubChem 刷新（20 评审候选 + 2 缺口化合物的官方属性响应）。
- `result/table/`（14 个文件）：候选报告覆盖、证据角色线索、定量 DOI 交叉表、**新增（未提交）12 候选体内机制证据图**、候选证据 profiles、化学观测索引、最新来源闭合、来源文档 / 文件索引；audit/ 下机筛 QC、全文批次摘要、锚点召回。

### 03_candidate_selection — 容量建模与排序（386 文件，50.8 MB）
- 主 README：[03 README](03_candidate_selection/README.md)。当前主链：`code/01_fit_orac_fl.py` → `code/02_validate_and_rank.py`；证据轮次表 `code/05_build_evidence_round_tables.py`；更新入口 `code/03_update_evidence.py --intake …`（只接受六门全过且 `APPROVED_FOR_NEXT_ANALYSIS` 的行，连接分析另需 `APPROVED_CONNECTED_FL`）。
- 12 个编号子研究（历史递进）：`01_activity_model`（192 文件，结构模型 / 审计 / 桥接协议）、`02_cross_study_expansion`、`03_preliminary_literature_selection`、`04_first_evidence_model`、`05_model_robustness`、`06_verified_source_update`、`07_all_reference_integration`（含 45 MB 全参考考虑登记 CSV）、`08_capacity_review_validation`、`09_aqueous_candidate_priority_v0.1`、`10_orac_evidence_increment`、`11_orac_fulltext_followup`、`12_evidence_expansion`（**当前定向证据更新**，见 §5）。
- `config/`：selection_rules.json + researcher_decisions.csv（研究者可编辑决策表，空白 = 未知，代码不代填）。
- `result/`：model/（ORAC-FL 拟合摘要、whole-DOI 验证 JSON）；table/（连接模型输入、harmonized 观测、排序敏感性、**Figure 1 候选排序（193 行）**、化合物证据纳入、轮次排序对比、top20 评审队列、cutoff 并列 12 候选、正式面板（空）、选择敏感性）；table/audit/（外部 ORAC 诊断、观测权重、排序与变异等）。
- 旧「实验评审面板」链（select_candidates.py）保留为历史准备基线：20 个评审槽是准备预算，不是科学排序；`formal_lab_ready_panel.csv` 在材料 / 采购 / 溶解度 / counter-screen / 研究者决策门未记录前保持为空。

### 04_05_experimental_validation — 实验验证与分析（设计阶段）
- 主 README：[04_05 README](04_05_experimental_validation/README.md)。研究内容约 88 个文件；`local_library/`（5,854 文件，422 MB）是**被忽略的本地 R 包库**（ggplot2、svglite、jsonlite、dplyr、igraph、ggraph、patchwork 等 ~110 包），渲染脚本可自动识别。
- 子模块：`01_endpoint_definition`（crocin 漂白剂量-时间容量终点为第一方法开发候选；ABTS 独立互补；ORAC-PGR 反应性敏感比较器）、`02_pilot_design`（公式来源审计、原始 trace 元数据与诊断对比、未填写的准备模板）、`03_platform_compatibility`（已识别 Flex 酶标仪限定：crocin 450 nm 为光学开发候选；ABTS/PGR 与默认通道不直接兼容；不假定内置温控 / 振荡）、`04_endpoint_stress_test`（无量纲模拟，与实验数据和排序分离）。
- `code/`（16 脚本）：01_build_endpoint_comparison、02_capacity_formula、**03_analyze_kinetics**（透明梯形 AUC，要求同时间网格剂量匹配无探针背景，拒绝缺失清除 / 元数据不匹配 / 非正校正初始吸光度；不插补、不强拟合 IC50、无验证校准不报 Trolox 当量）、04_compare_auc（拒绝不相容网格 / 分层）等。
- `input/method_reference/`（48 文件）：测定法参考配置 CSV（证据分级评分、ORAC 文献资格 / 提取字典、测定比较与选择 rubric 等）——是参考书目，不是测定批准。
- **当前没有任何真实实验行**；schema CSV 为空模板；AUC 代码仅通过合成内存 trace 测试。

### 06_manuscript — 论文装配（161 文件，8.7 MB）
- 主 README：[06 README](06_manuscript/README.md)。
- 工作文档：[01_methods_working.md](06_manuscript/01_methods_working.md)（Working Methods）、[04_part1_manuscript_sections.md](06_manuscript/04_part1_manuscript_sections.md)、[03_figure1_panel_order.md](06_manuscript/03_figure1_panel_order.md)、[Figure_Captions.md](06_manuscript/Figure_Captions.md)；历史描述性 [Methods.md](06_manuscript/Methods.md)（80 KB）与 [Results.md](06_manuscript/Results.md)。
- `code/`（6 脚本）：01_build_manuscript_outputs（历史描述链）、02_render_manuscript_panels.R（组件预览）、03_build_working_results.py（生成 Results 1）、04_render_figure1.R、05_build_part1_manuscript.py（python-docx 装配）、06_render_screening_workflow.R（300 dpi PNG + 可编辑 SVG）。
- `result/`：**[Manuscript_Part1_Nature_Communications.docx](06_manuscript/result/Manuscript_Part1_Nature_Communications.docx)**（154 KB，2026-11-23）、[02_results_working.md](06_manuscript/result/02_results_working.md)；figure/（6 组主图 PNG+SVG 对：figure1 总图、figure1a 筛选流程、figure1-1 发现、figure1-2 文献筛选、figure2-1 模型验证、figure2-2 排序稳定性 + supplementary/ 128 个文件）；table/（Candidate_Review_Workbook.xlsx、Table 1–3、Table S1、audit/Manuscript_Claim_Map.csv 声明-输入-代码-输出链映射）。
- 纪律：不得把计划步骤写成过去时「已做实验」；实验剂量反应 / 细胞获益 / 因果机制 Results 需要真实数据与科学评审。

### 07_quality_control — 科学与可重复性校验（32 文件）
- 主 README：[07 README](07_quality_control/README.md)；状态：[workflow_qc.json](07_quality_control/workflow_qc.json)（as_of 2026-11-05，含 2026-11-12 来源扩展评估）+ [Workflow_QC.md](07_quality_control/Workflow_QC.md)：**PASS**。
- 校验覆盖：983 登记来源 SHA256、191 字面种子重建、157 框架覆盖、参考分子式、候选/来源连接、选择门、cutoff 并列、10 个冻结资产、69 个 SVG 文本矢量无栅格、活动英文 Markdown 链接、合成 trace AUC 测试。
- `code/`：01_build_indexes、02_validate_workflow（+1）；`result/table/audit/`：branch_inventory.json、descriptive_summary.json、determinism_qc.json、figure_export_registry.csv、workbook 导出 QC。
- `R_session_info.txt` 记录 R 会话 / 包版本；`local/`、`previews/` 被忽略。

### download_raw — 本地原始与过程数据（整体 git 忽略，199.5 MB）
- 根部：用户提供的原始 PDF（Food Chemistry、zhang2013、DPPH revisited、ORAC-FL 扩展适用性等）+ 60 黄酮补充材料 docx；Repository_Cleanup_Local_Inventory.csv（1.9 MB 清理盘点）；Results1 清理前快照 / 合成更新 / 预览。
- `layout_migration/`（2,874 文件，134 MB）：布局迁移回放（results1_replay / merge / retirement 系列）、retired_runtime_chem、source_review_derivatives、path_map.json、迁移脚本与日志。
- `stage2_machine_screening/`（33.5 MB）：**机筛全量输出** Report_Screening.csv（24 MB）、Candidate_Report_Links.csv（9 MB）、ORAC_Fulltext_Batches.csv、Recall_Audit_Sample.csv。
- `stage2_institutional/`（6.7 MB）：WoS 机构导出规范化记录（500 条）与本地 QC / 对账。
- `manuscript_part1_qa/`、`Results1_post_cleanup_*`、`Results1_update_dry_check/`：论文 QA 与更新演练产物。

---

## 4. 当前科学进展快照（数字均来自仓库文件）

**发现与身份**
- 204 条发现记录 → 193 个候选 profiles；191 个参考分子式；20 个评审候选 + 2 个缺口化合物有官方 PubChem 刷新，其余为显式标注日期的遗留缓存。

**检索与机器筛选**（[Screening_QC.json](02_identity_and_evidence/result/table/audit/Screening_QC.json)，窗口 2020-01-01 → 2026-11-17）
- PubMed 唯一 PMID 65,248；Europe PMC 路径键 62,458；WoS 本地 500；标识符对账后 provisional union **76,383**。
- 摘要检查 65,424 + 仅标题 10,959；185/193 候选至少 linked 一条报告；候选-报告链接 55,527。
- 机器分流：高优先 ORAC 全文队列 **567**；全文证据角色队列 19,446；上下文评审 / 引文追踪 7,913；仅标题待摘要 10,721；低优先 / 未决 36,654；标识符 / 更正 HOLD 889；撤稿记录 HOLD 193。**自动排除 = 0**；最终系统综述纳入未完成。

**全文评审进度**（[12_evidence_expansion README](03_candidate_selection/12_evidence_expansion/README.md)、[Fulltext_Batch_Summary.json](02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json)）
- 567 优先报告中 **88 条已有来源评审范围记录，479 待处理**（待处理批次 21 × 25）；访问路径：PMC XML 待获取 274、出版商 / 仓储查找 204、来源 ID 冲突 1。
- 注意：生成的 [02_results_working.md](06_manuscript/result/02_results_working.md) 仍写 86/481，为上一检查点数字（见 §7 建议 2）。

**条件 ORAC-FL 模型与排序**（[02_results_working.md](06_manuscript/result/02_results_working.md)、[04_figure1_candidate_ranks.csv](03_candidate_selection/result/table/04_figure1_candidate_ranks.csv)）
- 主模型：125 条观测 / 14 个 DOI 报告 / 51 个化合物；协议敏感性 130 条 / 15 DOI。
- 同一 81 条可估计 whole-report holdout：log-RMSE 旧模型 0.595 → 扩展条件模型 **0.518**（协议敏感性 0.521）。
- ±10 名次规则（2026-11-23 批准）：**12/51 保留**；21 个位移超 10；18 个在至少一次 DOI 删除后失去名次。
- 保留名单（条件名次）：Quercetin (2)、Catechin (3)、Hesperetin (5)、Genistein (14)、Hesperidin (22)、Myricetin (33)、p-Coumaric acid (36)、Chlorogenic acid (37)、Gallic acid (48)、Syringic acid (49)、L-Ascorbic acid (50)、Glutathione (51)。
- 示例：Rosmarinic acid 条件第 1，但组合区间达第 23 → HOLD；L-抗坏血酸第 50 但有 7 个条件模型报告支持 → 保留。观测容量、报告覆盖、模型稳定性是三个不同维度。
- 结构模型单报告分析：scaffold-holdout RMSE 0.945（Ridge）vs 0.953（基线），out-of-fold R² −0.24 → 无跨报告结构预测验证。

**定向证据扩展与试验**（12_evidence_expansion）
- 16 条数值观测 HOLD（单位 / 浓度基准 / 分散度未决，如 Moldoveanu & Oden 2021 µM TE/g、Nguyen & Karboune 2023）；1 条支持外部诊断；4 条进入隔离条件试验。
- 外部 fisetin 诊断：模型估计 5.973 mol TE/mol vs Moon 2022 观测 12.17（2.04 倍）——单化合物比较，不验证排序。
- 四酚酸试验（Wang 2025，Table 1 单位假设下）：129 观测 / 15 DOI / 51 化合物；holdout log-RMSE 0.735 → 0.728；原儿茶酸 6→24、p-香豆酸 36→26、阿魏酸 42→40、没食子酸 48→47。**主分析与正式更新名次字段保持第一轮状态**，待表格/正文单位澄清与可采纳新观测后 refit。

**新增（未提交）：12 候选体内机制证据图**（[04_candidate_in_vivo_mechanism_evidence.md](02_identity_and_evidence/result/table/04_candidate_in_vivo_mechanism_evidence.md) + 同名 CSV）
- 28 条观测 / 26 篇原始文献（19 动物体内、8 人体体内、1 离体）；人体记录覆盖 6 个化合物；24 篇有 DOI；5 条仅摘要级。
- 全部 `NOT_REVIEWED`、`change_applied=NO`；定位为临时证据图，不得用于估计流行率或给机制打分。
- 已列出研究者评审检查点：P0——槲皮素 Fig.7/8 对比归属、绿原酸体内 vs 离体主动脉环区分、**橙皮素 Aβ 小鼠论文 Fig.8a 图像来源核查（关联撤稿图像相似性关切，核实前不得入稿）**；P1——橙皮苷 / 没食子酸人体试验摘要级提取核实、谷胱甘肽 4 周 vs 6 个月试验对比类型、儿茶素 / p-香豆酸原始方法核实。

**实验验证（04–05）**：纯设计阶段。crocin 漂白（450 nm，Flex 酶标仪）为第一方法开发候选；ABTS 互补、ORAC-PGR 比较器与默认通道不直接兼容；800 mM AAPH 表述待来源澄清；仪器 / 试剂 / 浓度 / 时序 / 阈值均未批准；无真实 trace。

**QC**：PASS（983 来源哈希、10 冻结资产、191 种子、69 SVG、链接完整、合成 AUC 测试通过）；正式实验室就绪 0；新测定实验 0；全局 193 排序仍未解决（`updated_model_global_rank_supported=false`）。

---

## 5. 数据资产与可重复性结构

- **冻结参考**：[results1_v1.0](02_identity_and_evidence/inputs/provenance/results1_v1.0/README.md)——304 条原始观测 + 225 条测定内参考排序 + 证据快照 + 数据字典；原 Results 1 发布从 commit `5ee3bc8`（2026-11-20）独立 checkout 回放。第一轮排序基线锚定 commit `e4c300c`（2026-11-23）。
- **来源登记**：source_manifest.json 记录 983 条 SHA256 与是否捆绑；本地语料（source_corpus/stage25a、systematic_supplement inputs、download_raw）在克隆上是可选的，不进入离线计算。
- **不可变来源**：`.gitattributes` 对 research_records、curation_baseline、reference_collection、identity_reference、mechanism_evidence、source_corpus、bibliography、journal_metrics、frozen_reference、method_reference 设 `-text`，PNG/XLSX  likewise；活动文本 `eol=lf`。
- **本地环境**：`.venv` Python 3.12.10；系统 R 4.5.3（C:\Program Files\R）；`04_05_experimental_validation/local_library` 提供 ~110 个 R 包（忽略，渲染器自动识别；冻结回放可用 R_LIBS_USER 指向它）。
- **历史档案**：00_project/research_records 保留 2026-09-18 起的四个研究批次、h_orac_framework 中英方法审计、治理 v0.1/v0.2、Track B 机器人筛选可行性、stage25b 构建脚本——均为历史记录，不是当前入口。

---

## 6. Git 状态

- 远程：`origin = https://github.com/Jane-huangjingyi/Antioxidants-project.git`。
- 提交：**75 个**（2026-09-18 起）；最近提交集中在 2026-11-05 → 11-24（系统综述范围冻结 → Stage2 检索 → Results 1 可重复发布 → Part 1 论文与第一轮证据检查点 → 化合物证据账本 → 定向 ORAC 证据与酚酸试验 → 可编辑筛选流程图）。
- 本地分支 10 个；当前 `codex/systematic-antioxidant-evidence-20261117`（与 origin 同步）。按 [branch_inventory.json](07_quality_control/result/table/audit/branch_inventory.json)（2026-11-05 审计）：phase1c 治理 / AFF-0061 批次 / Track B / repository-review 等 7 个分支已包含在布局基线 `c6bca4d` 中，保留为可追溯里程碑，不重复合并；`codex/food-candidate-manuscript-workflow-20261105` 与当前分支为活动工作链。
- **main = `d29a693`，是较旧祖先**；[Git_Workflow.md](00_project/Git_Workflow.md) 给出经显式批准后的 `--ff-only` 集成路径（指令而非已执行操作；不强制推送、不改远程默认）。
- **未提交改动（3 项）**：
  1. `Latest_Results.md` 修改（+2 行：链接新体内机制证据图）；
  2. 未跟踪 `02_identity_and_evidence/result/table/04_candidate_in_vivo_mechanism_evidence.csv`；
  3. 未跟踪同名 `.md`。
- 配置注意：`core.autocrlf=true` 且 `core.longpaths` **未设置**（Environment.md 建议启用）；Latest_Results.md 出现 CRLF→LF 警告（提交时按 .gitattributes 归一化，无实质影响）。

---

## 7. 复现命令速查

```powershell
# 环境（已就绪：.venv Python 3.12.10；R 4.5.3）
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r 03_candidate_selection/01_activity_model/requirements_structure.txt

# 当前文献主链（发现→身份→机筛→模型→排序→全文批次→working Results→QC）
.venv/Scripts/python.exe run_pipeline.py --literature

# 历史描述性全链（表 + R 图；--tables-only 跳过 R；--legacy-figures 历史图；--workbook 需 Node）
python run_pipeline.py --tables-only

# 论文产物
python 06_manuscript/code/03_build_working_results.py
Rscript 06_manuscript/code/04_render_figure1.R
python 06_manuscript/code/05_build_part1_manuscript.py
Rscript 06_manuscript/code/06_render_screening_workflow.R   # jsonlite + svglite

# 证据更新循环（六门评审后）
python 03_candidate_selection/code/03_update_evidence.py --intake reviewed.csv --out download_raw/results1_next_review --cutoff 2026-11-17
python 03_candidate_selection/code/05_build_evidence_round_tables.py   # 更新后 --updated-ref <commit>

# 网络刷新（显式、与离线复现分离；刷新后须评审再提交）
python 02_identity_and_evidence/code/refresh_pubchem.py
python 04_05_experimental_validation/code/search_methods.py
```

---

## 8. 发现与建议（按优先级）

1. **未提交的新证据图待处置**：12 候选体内机制证据（28 条观测）全部 NOT_REVIEWED，且含 P0 图像来源核查点（橙皮素 Fig.8a）。按项目治理，应先完成研究者评审检查点，再决定是否提交 / 是否入稿；当前 Latest_Results.md 已链接它，提交时三者应同批。
2. **生成 Results 与最新检查点数字滞后**：02_results_working.md 写 86/481，而 12_evidence_expansion 与 Latest_Results 为 88/479。重跑 `python 06_manuscript/code/03_build_working_results.py`（及下游 QC）即可同步；Part 1 docx 若引用该段也需随之重建。
3. **QC 快照日期早于最新提交**：workflow_qc.json as_of 2026-11-05（含 11-12 扩展评估），最新证据提交在 11-23/24。建议重跑 `python 07_quality_control/code/02_validate_workflow.py` 刷新状态后再发布。
4. **main 集成未执行**：main 落后于活动链；按 Git_Workflow.md 的 ff-only 路径在显式批准后集成（先 `git fetch origin` 确认无分叉）。
5. **启用 core.longpaths**：仓库存在很深的历史路径（legacy 归档 / 检索缓存），Environment.md 已建议；当前未设置，跨机器克隆 / 检出有长路径风险（`git config core.longpaths true`）。
6. **本地缓存迁移注意**：~3.3 GB 被忽略内容（检索 XML/PDF 缓存、download_raw 原件、R 库、.venv）不随克隆传递；换机时按 source_manifest 哈希校验重新获取，或整体拷贝这些目录；离线科学计算本身只需捆绑来源。

---

## 9. 快速导航

| 想找什么 | 去哪里 |
|---|---|
| 项目总览 / 最新结果入口 | [README.md](README.md) · [Latest_Results.md](Latest_Results.md) |
| 研究边界与在案决策 | [Protocol.md](00_project/Protocol.md) · [Decision_Register.md](00_project/Decision_Register.md) |
| 系统综述协议 | [Systematic_Review_Protocol_v1.0.md](02_identity_and_evidence/04_systematic_protocol_v1/Systematic_Review_Protocol_v1.0.md) · [Protocol_Addendum_v1.1.md](02_identity_and_evidence/04_systematic_protocol_v1/Protocol_Addendum_v1.1.md) |
| 候选名单 / 覆盖 | [discovery_register.csv](01_candidate_discovery/results/discovery_register.csv) · [01_candidate_report_coverage.csv](02_identity_and_evidence/result/table/01_candidate_report_coverage.csv) |
| 当前排序与保留决策 | [04_figure1_candidate_ranks.csv](03_candidate_selection/result/table/04_figure1_candidate_ranks.csv) · [03_rank_sensitivity.csv](03_candidate_selection/result/table/03_rank_sensitivity.csv) |
| 模型诊断 | [02_whole_doi_validation.json](03_candidate_selection/result/model/02_whole_doi_validation.json) |
| 证据扩展 / 酚酸试验 | [12_evidence_expansion README](03_candidate_selection/12_evidence_expansion/README.md) |
| 体内机制证据图（新，未提交） | [04_candidate_in_vivo_mechanism_evidence.md](02_identity_and_evidence/result/table/04_candidate_in_vivo_mechanism_evidence.md) |
| 论文与图 | [Part 1 docx](06_manuscript/result/Manuscript_Part1_Nature_Communications.docx) · [Figure 1 PNG](06_manuscript/result/figure/figure1_evidence_screening_and_ranking.png) · [Working Methods](06_manuscript/01_methods_working.md) |
| 实验设计 | [04_05 README](04_05_experimental_validation/README.md) · [01_endpoint_definition](04_05_experimental_validation/01_endpoint_definition/README.md) |
| QC 状态 | [workflow_qc.json](07_quality_control/workflow_qc.json) · [Workflow_QC.md](07_quality_control/Workflow_QC.md) |
| 来源哈希 / 冻结参考 | [source_manifest.json](02_identity_and_evidence/source_manifest.json) · [results1_v1.0 README](02_identity_and_evidence/inputs/provenance/results1_v1.0/README.md) |
| 历史档案 | [research_records README](00_project/research_records/README.md) |
| 环境 / 分支 / 文件政策 | [Environment.md](00_project/Environment.md) · [Git_Workflow.md](00_project/Git_Workflow.md) · [File_Management.md](00_project/File_Management.md) |
