# Stage25B H-ORAC 检索与裁决报告（当前审计停点）

本轮已对冻结的 47 个候选执行统一 Europe PMC 题名/摘要检索，检索日期为 2026-09-21。冻结完整性检查通过：aqueous candidate universe = 157、Provisional Top50 = 50、Stage25B retrieval input = 47；Stage25A 排名和计数字段未修改，rank 51+ 未进入检索集，Sulforaphane、Caffeine、Allicin 未进入 quantitative retrieval，Thymoquinone、Baicalein、Chrysin、Plumbagin 保持 candidate-universe INCLUDE + H-ORAC Conditional。

检索返回 3,056 条候选×publication 元数据行；补入 59 条未被校准题名/摘要式重新发现、但已存在于 canonical evidence master 的候选×publication provenance 后，publication screening ledger 共 3,115 行。元数据筛查排除 1,387 行，1,657 行仍需全文方法 adjudication。现已核查 71 条候选×publication 行，对应 20 篇唯一全文来源；形成 71 条 experiment rows，其中 B1 = 66、B2 = 4、X = 1、A = 0。当前 A/B1 quantitative-rankable candidates = 26，但这是基于既有 full-text evidence revalidation 的 interim ranking，不能视为完成的 Stage25B Top20。

新增全文核查确认 Baicalein 原始论文（DOI 10.3390/pharmaceutics14102141）使用 AAPH、fluorescein、Trolox、37 °C、动力学读数，并报告 5.41 ± 0.33 µmol TE/µmol compound；参考标准纯度为 97%。由于 Baicalein 为 chromophoric Conditional candidate，而论文未报告 compound-specific optical blank/correction，也未充分报告溶剂与聚集控制，依 frozen rubric 判为 B2，仅进入 sensitivity，不进入 primary ranking。Curcumin 开放全文 DOI 10.3762/bjoc.11.151 虽采用 ORAC-FL construct，但本文表格未提供本文原始 curcumin quantitative result，不能生成 curcumin evidence row。

当前 interim primary ranking 的前 20 位依次为 Rosmarinic acid、Epicatechin、Catechin、Caffeic acid、Apigenin、Naringenin、Kaempferol、Daidzein、Hesperetin、Protocatechuic acid、Genistein、Quercetin、Fisetin、Rutin、Sinapic acid、p-Coumaric acid、Hesperidin、Luteolin、Naringin、Ferulic acid。该序列仅使用 A/B1；没有 Tier A，所以 A-only ranking 不可计算。加入 B2 后，Cyanidin 3-O-glucoside、Baicalein 和 Cyanidin 进入前 20 sensitivity set，导致 cutoff membership 改变，故当前结论为 `TOP20 CUTOFF UNSTABLE`。这不是最终 Top20，也不代表 human efficacy、dietary importance 或 clinical benefit。

High heterogeneity（max/min > 2）候选为 Quercetin、Gallic acid、Caffeic acid、Ferulic acid、Catechin、Protocatechuic acid、Sinapic acid。现阶段 Ready 与 Conditional 的系统差异不能作可靠统计解释，因为大量未决全文在两组间分布不均。现有 `independent_experiment_id` 已重编为唯一的 `HORAC_EXP_####`；legacy ID 单独保留，duplicate experiment ID = 0。所有正式数值均有 source provenance；唯一无 DOI/PMID 的 legacy figure-only Sinapic acid 记录保持 B2、不可提取和非排名状态。

必须逐项回答的 QC 结论如下：47 个候选均完成数据库检索，但未全部完成全文 adjudication；候选级检索数、筛查数、全文数和 compatible 数见 `Stage25B_HORAC_Search_Log.csv`；A = 0、B1 = 66、B2 = 4、X = 1；当前 26 个候选可作 interim quantitative rank；数量达到 20，但不能冻结 Top20；存在 figure-only evidence、positional-identity X record、same-experiment legacy labeling risk（已通过 Stage25B row-level ID 修复）、7 个 high-heterogeneity candidates；A-only 不可计算，A+B1 与加入 B2 的 Top20 membership 不稳定；没有结果要求修改 frozen rubric；Stage25A rank、157 universe、47 input 均未改变。

`HUMAN REVIEW REQUIRED — FULL-TEXT COMPLETION AND RANK-CHANGING B2 EVIDENCE`：当前 1,657 条元数据命中尚未完成全文方法核查，且 B2 sensitivity 已实际改变 Top20 cutoff。可能选项是继续逐篇全文筛查并执行第二审核，或由研究者先批准一个预定义的优先全文队列（cutoff 15–25、Conditional chromophores、现无 eligible evidence 的候选），但不得把未核查摘要值纳入排名。Codex 建议继续完整全文筛查并由第二审核者复核 identity、tier、单位与 independence；在此之前不冻结 Top20。

当前终止状态：`STAGE25B BLOCKED — METHOD / IDENTITY / PROVENANCE ISSUE`。阻塞点不是检索失败，而是未完成的大规模全文方法裁决、第二审核以及已观察到的 cutoff sensitivity。
