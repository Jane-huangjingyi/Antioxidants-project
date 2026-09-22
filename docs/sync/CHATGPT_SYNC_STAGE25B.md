# CHATGPT SYNC — Stage25B 当前审计停点

Stage25B 尚未完整完成。冻结的 47 candidates 已全部执行 Europe PMC 检索；publication screening ledger 3,115 行，其中 1,387 行元数据排除、1,657 行待全文 adjudication、71 条候选×publication 行已核查，对应 20 篇唯一来源。Experiment evidence 共 71 行：A 0、B1 66、B2 4、C 0、X 1；当前基于已核查 A/B1 的 rankable candidate N = 26。

Interim H-ORAC 前 20 为 Rosmarinic acid、Epicatechin、Catechin、Caffeic acid、Apigenin、Naringenin、Kaempferol、Daidzein、Hesperetin、Protocatechuic acid、Genistein、Quercetin、Fisetin、Rutin、Sinapic acid、p-Coumaric acid、Hesperidin、Luteolin、Naringin、Ferulic acid。加入 B2 后 Cyanidin 3-O-glucoside、Baicalein、Cyanidin 进入 sensitivity Top20，因此 `TOP20 CUTOFF UNSTABLE`，不得冻结。High heterogeneity：Quercetin、Gallic acid、Caffeic acid、Ferulic acid、Catechin、Protocatechuic acid、Sinapic acid。

Baicalein 新增全文证据为 5.41 ± 0.33 mol TE/mol，但因 chromophore optical blank/correction 与 solubility/aggregation QC 不足判为 B2，不进入 primary ranking。Curcumin 检索到的开放全文没有本文原始 curcumin quantitative value，未纳入。Conditional candidates 不因 candidate inclusion 自动升级 evidence。

完整性检查：aqueous universe 157、Top50 50、retrieval input 47；Stage25A rank/count 未变；指定 3 个 Not suitable 未进入 retrieval；指定 4 个 researcher-adjudicated candidates 保持 INCLUDE + Conditional；Stage25B experiment ID 无重复；B2/C/X 未进入 primary ranking；missing 未编码为 0；没有 publication/citation × ORAC composite score。

新增 canonical work products 位于 `data/h_orac_stage25b/`，构建脚本为 `scripts/stage25b_retrieve_europepmc.ps1` 和 `scripts/build_stage25b_outputs.ps1`。本停点未生成正式图，因为全文 adjudication 尚未完成，现阶段绘图会制造虚假的完成感。Zotero helper 因本机无可用 Python runtime 未能执行，待导入来源见 `Stage25B_Zotero_Pending_Import.csv`，未伪造 Zotero key。

HUMAN REVIEW REQUIRED：继续 1,657 条全文方法筛查、第二 reviewer 复核、rank-changing B2 与 cutoff 15–25 稳定性审查。在完成前状态为 `STAGE25B BLOCKED — METHOD / IDENTITY / PROVENANCE ISSUE`。

完成 commit + push 后，通知 ChatGPT：`Antioxidants Project 已推送 GitHub，请读取最新版本并审核 Stage25B。`

优先级 1：`docs/sync/CHATGPT_SYNC_STAGE25B.md`、`docs/qc/Stage25B_HORAC_Retrieval_and_Adjudication_Report_CN.md`、`data/h_orac_stage25b/Stage25B_HORAC_Candidate_Summary.csv`、`data/h_orac_stage25b/Stage25B_HORAC_Quantitative_Ranking.csv`、`data/h_orac_stage25b/Stage25B_HORAC_Experiment_Evidence.csv`。

优先级 2：publication screening、source provenance、sensitivity analysis、exclusion log，以及有新增时的 Human Review Log。

优先级 3：Zotero pending import、详细 search log、specific full-text audit tables；当前没有 canonical figures 或 figure QC 需要同步。
