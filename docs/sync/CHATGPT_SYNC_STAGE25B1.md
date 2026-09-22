# CHATGPT SYNC — Stage25B.1

Stage25B.1 已按 rank relevance 执行，而非无差别处理全部 1,657 条记录。Frozen Stage25B checkpoint 已完整保存在 `data/h_orac_stage25b/checkpoints/stage25b_initial_2026-09-21/` 并附 SHA-256 manifest。

Priority table 覆盖 1,657/1,657 pending records：Priority 1=380、Priority 2=437、Priority 3=755、Priority 4=0、Priority 5=85；Priority 4=0 是因为 Conditional records 已按最高适用优先级进入 Priority 1–3。实际从 pending queue 完成/尝试 adjudication 16 rows：Priority 1=12、Priority 3=4，remaining low/other-priority unreviewed = 1,641。Source-level adjudication log 有 15 decisions，并另外覆盖已 adjudicated 的 Baicalein focused second review 和新发现 Conditional pure-compound source。

新增证据：Eugenol 2.12 ± 0.08、Capsaicin 1.60 ± 0.25、Vanillin 1.81 ± 0.19 mol TE/mol，均来自 DOI `10.3390/foods10081807`，判 B1。Experiment rows 71→74；B1 66→69；B2仍4、X仍1、A仍0；rankable candidate N 26→29。Primary Top20 membership 未改变，但 rank 25 从 Ellagic acid 变为 Eugenol，故 rank 15–25 membership 尚未稳定。

Baicalein 5.41 ± 0.33 维持 B2。Primary A/B1 不纳入；若单独纳入该 B2 值，会替换 primary rank 20 Ferulic acid。完整 A+B1+B2 sensitivity 的 Top20 增加 Cyanidin 3-O-glucoside、Baicalein、Cyanidin，并移出 Luteolin、Naringin、Ferulic acid。因此 `TOP20 CUTOFF UNSTABLE TO B2 EVIDENCE`。

Batch 1 没有新增 A/B1。多个 cutoff-critical shared sources仍为 `SOURCE_NOT_RECOVERED`，包括 DOI `10.1089/jmf.2009.0024` 和 `10.1021/jf0208132`；Myricetin HPβCD 原始论文仓储失效。Pyrogallol-red ORAC 与 ORAC-EPR records 已明确判 C。Tyrosol、Pterostilbene、Sesamol 和旧 Vanillin source 仍有不可恢复或不可提取问题；Curcumin 不存在本文 original quantitative curcumin value。

A-only ranking仍不可计算。69/69 B1 records 均缺至少一项 compound blank、optical control、aggregation 或 final cosolvent reporting，66/69 在 consolidated master 中未展开 purity。已登记 `HUMAN REVIEW REQUIRED — TIER A FEASIBILITY`；rubric 未修改。

Stopping rule：无 A/B1 改变 primary Top20 membership通过；rank 15–25 stability、B2-insensitivity、无 unresolved rank-changing issue均未通过。最终状态为：`STAGE25B.1 HUMAN REVIEW REQUIRED`。没有生成正式 Top20 figure，没有进入 target mapping 或 translational ranking。

Cutoff-critical recovery follow-up（2026-09-22）：仅复核 DOI `10.1089/jmf.2009.0024` 与 `10.1021/jf0208132`。Zotero 客户端未运行；前者的出版社 PDF 仍不可取，OpenAlex 所列 AECID/LA Referencia green-OA submitted-version handles 全部失效；后者为 closed 且无 repository full text。两篇均维持 `SOURCE_NOT_RECOVERED / X`，未使用摘要或二手数值。重算 primary rank 15–25 与 A+B1 Top20 membership 均不变；A+B1+B2 sensitivity 仍增加 Cyanidin 3-O-glucoside、Baicalein、Cyanidin并移出 Luteolin、Naringin、Ferulic acid。Tier A feasibility 继续 `HUMAN REVIEW REQUIRED`，frozen rubric 未修改，剩余 1,641 条未继续处理。完整记录见 `docs/qc/Stage25B1_Cutoff_Critical_Recovery_Report_CN.md`。

完成 commit + push 后，请通知 ChatGPT：`Antioxidants Project 已推送 GitHub，请读取最新版本并审核 Stage25B.1。`
