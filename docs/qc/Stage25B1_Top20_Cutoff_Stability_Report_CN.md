# Stage 25B.1 — Top20 cutoff stability report

Stage25B.1 以冻结的 Stage25B checkpoint 为起点，不重新运行 47-candidate retrieval，也没有覆盖原始 checkpoint。九个原始数据产物已复制到 `data/h_orac_stage25b/checkpoints/stage25b_initial_2026-09-21/`，并以 SHA-256 manifest 固定：3,115 publication-screening rows、71 experiment rows、26 rankable candidates，以及原始 `STAGE25B BLOCKED — METHOD / IDENTITY / PROVENANCE ISSUE` 状态均可重建。

## Priority construction

全部 1,657 条 remaining records 已进入 `Stage25B1_FullText_Adjudication_Priority.csv`。互斥优先级分布为 Priority 1 = 380、Priority 2 = 437、Priority 3 = 755、Priority 4 = 0、Priority 5 = 85。Priority 4 为 0 是因为所有 Conditional 且 fragile/rank-relevant records 已按“取最高优先级”原则进入 Priority 1–3，不表示 Conditional records 被遗漏。

本轮实际改变 adjudication status 的原 pending queue rows 为 16/1,657：Priority 1 = 12、Priority 3 = 4。另对已不在 pending queue、但由 Stage25B.1 明确指定的 Baicalein B2，以及新发现的 Conditional pure-compound paper 等执行 focused adjudication。`Stage25B1_Rank_Relevant_Adjudication_Log.csv` 共记录 15 个 source-level decisions；一个 source decision 可对应多个 candidate×publication rows。

## Batch 1 — cutoff-critical sources

Batch 1 优先核查 rank 15–25 的共享原始来源。DOI `10.1089/jmf.2009.0024` 的摘要确认比较 fluorescein ORAC，但出版社 PDF 返回 403，浏览器进入 Cloudflare security challenge；未绕过安全验证，Sinapic acid、Luteolin、Ferulic acid、p-Coumaric acid 相关值标为 `SOURCE_NOT_RECOVERED / X`。DOI `10.1021/jf0208132` 的 probe、原始数值、单位和 compound-level source location 无法从 primary full text 核实，同样保持 X。Myricetin 的 HPβCD paper `10.1016/j.foodchem.2009.05.061` 所登记机构仓储 handle 已失效，保持 X。`10.1016/j.jfca.2013.09.007` 明确为 pyrogallol-red ORAC，判 C；`10.3164/jcbn.11-21` 为 ORAC-EPR/cyclodextrin system，判 C。Batch 1 没有新增 A/B1，也没有改变 primary Top20。

## Batch 2 — B2/X, fragile and Conditional evidence

开放全文 DOI `10.3390/foods10081807` 提供三个新 B1 independent experiments：Eugenol 2.12 ± 0.08、Capsaicin 1.60 ± 0.25、Vanillin 1.81 ± 0.19 mol TE/mol。三者均为 pure compounds，报告 purity、AAPH 150 mM、fluorescein 80 nM、Trolox 1–8 µM、PBS 75 mM pH 7、37 °C、0.09–6.0 µM dose range、55 min kinetic AUC 及 N=3。精确 final ethanol percentage、compound-specific blank 和 aggregation test 未完整报告，因此为 B1 而不是 A。它们令 rankable candidate N 从 26 增至 29，但数值均低于 primary cutoff；Top20 membership 不变。Eugenol 进入 rank 25，Ellagic acid 从 rank 25 移至 26，因此 rank 15–25 membership 尚未连续两批稳定。

Baicalein focused second review 维持 B2。其 5.41 ± 0.33 mol TE/mol 若单独允许进入 A/B1 ranking，会进入约 rank 16 并把 Ferulic acid 从 primary Top20 挤至 rank 21；由于缺少 chromophore-specific optical blank/correction 及关键 solvent/aggregation QC，不允许升级。完整 A+B1+B2 sensitivity 同时加入 Cyanidin 3-O-glucoside、Baicalein 和 Cyanidin，替换 primary Top20 中的 Luteolin、Naringin 和 Ferulic acid。因此仍为 `TOP20 CUTOFF UNSTABLE TO B2 EVIDENCE`。

Tyrosol abstract报告 0.83 ± 0.03（无 HPβCD）和 1.20 ± 0.11（0.8 mM HPβCD），但未恢复完整 primary full text，保持 X。Pterostilbene、Sesamol 和旧 Vanillin paper 的 exact value/method location 同样未完全恢复；Curcumin 开放全文未提供本文 original curcumin quantitative value，继续不抽取。

## Stopping-rule evaluation

连续两个 batch 后：第一项“没有新的 A/B1 改变 Top20 membership”通过；第二项“rank 15–25 membership 稳定”未通过，因为 Eugenol 新进入 rank 25；第三项“B2 sensitivity 不再改变 primary Top20 interpretation”未通过；第四项“没有 unresolved rank-changing method/provenance issue”未通过。因此不能宣称 cutoff stable，也不生成正式 Top20 figure。

## Tier A feasibility

当前 A=0、B1=69。69 条 B1 中，66 条 consolidated records 未在当前 master 报告 purity；69/69 未记录 compound-specific blank、明确 optical-interference control、aggregation assessment 和完整 final cosolvent percentage。部分缺口是真正的 assay-comparability 风险，部分可能只是历史论文报告不足或旧 evidence consolidation 未展开到该字段。改变 Tier A 定义将可能把大量既有 B1 批量升级并改变 confidence interpretation，因此不得由本轮自行执行。正式标记：`HUMAN REVIEW REQUIRED — TIER A FEASIBILITY`。

## Conclusion

当前完成状态：`STAGE25B.1 HUMAN REVIEW REQUIRED`。Primary A+B1 Top20 membership 在本轮没有变化，但 rank 15–25 尚未稳定，B2 inclusion 仍改变三项 membership，且存在共享 cutoff source 未恢复、Tier A feasibility 与 second-review coverage 问题。剩余 1,641 条 priority queue records 继续保留为未裁决证据；不声称 systematic full-text review complete，也不进入 target mapping、mechanism prioritization 或 final translational Top20。
