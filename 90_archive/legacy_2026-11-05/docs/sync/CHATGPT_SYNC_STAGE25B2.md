# CHATGPT SYNC — Stage25B.2

Stage25B.2 已完成 representative Tier A feasibility audit。Canonical state 无变化：A/B1/B2/X = 0/69/4/1，rankable candidates = 29，primary rank 20 Ferulic acid 4.032、rank 21 Morin 3.8745；`STAGE25B.1 HUMAN REVIEW REQUIRED` 与 `TOP20 CUTOFF UNSTABLE TO B2 EVIDENCE` 保持冻结。未处理剩余 1,641 条、未搜索新 evidence、未修改 rubric、未升级 Baicalein/Cyanidin/Cyanidin 3-O-glucoside、未重算 Top20。

审计样本为 15 个 independent B1 experiments、7 sources、2001–2023，覆盖全部指定 ranking/evidence-depth/confidence/heterogeneity/chemistry strata。14/15 primary full texts 可重新核查；1 条早期 ACS source不可得，其未知项按 `UNCLEAR`，不解释为未执行。结果：13 条维持 B1但不满足 frozen strict Tier A，1 条维持 current B1 pending full text，0 条可确认 strict Tier A；Chlorogenic Acid `HORAC_EXP_0067` 因可推得约 10% final methanol且未说明 matched ORAC solvent control，被标记 `HUMAN REVIEW REQUIRED — POTENTIAL B1 DOWNGRADE`，未执行降级。

A=0 是 historical reporting incomplete、previous extraction incomplete 和 universal strictness 的组合。旧 extraction 明显遗漏了 purity grade/supplier、reagent concentrations、solvent、kinetic AUC 和 replicate detail；同时 14 个可复核 experiments 中没有任何一条明确报告 compound-specific optical blank 或 aggregation assessment。Purity missing 主要是 extraction completeness + reporting granularity，而不是证实实验材料低质。当前 universal compound-specific blank/optical/aggregation gates 对 historical literature 呈结构性不可达到；科学上更合理的候选结构是 universal assay-comparability core + compound-risk-triggered enhanced QC，但任何修改必须由研究者批准。

核心文件：`data/h_orac_stage25b/Stage25B2_TierA_Feasibility_Audit.csv`、`data/h_orac_stage25b/Stage25B2_TierA_Criterion_Summary.csv`、`docs/qc/Stage25B2_TierA_Feasibility_Report_CN.md`。Human Review Log 已追加 rubric feasibility、potential B1 downgrade 与 universal-vs-risk-triggered decisions。

## HUMAN DECISION REQUIRED

Question: Tier A 后续如何处理？

Option A — 保持当前 strict Tier A。Scientific rationale：A 保留为 historical + prospective gold standard。Advantage：严格且无需迁移。Disadvantage：A 可能长期为空、实际 discrimination value 低。Impact on existing 69 B1：不变。Impact on Top20 interpretation：无即时变化。Re-adjudication workload：低。

Option B — 采用 universal core + risk-triggered QC。Scientific rationale：AAPH/FL/Trolox/buffer-pH/temperature/identity/concentration/solvent interpretability/kinetic AUC/value-unit traceability universal mandatory；enhanced optical、aggregation、solvent QC 由风险触发。Advantage：符合 chemistry-specific risk并恢复 A/B1区分。Disadvantage：需定义和验证 risk triggers。Impact on existing 69 B1：全部重裁。Impact on Top20 interpretation：A↔B1本身不变；风险触发 downgrade可能改变。Re-adjudication workload：高。

Option C — Tier A 保留为 prospective ideal；historical primary evidence 使用 B1 + QC flags。Scientific rationale：分离 prospective standard 与 historical comparability。Advantage：避免空 A并透明表达风险。Disadvantage：历史 A/B1 两级被弱化。Impact on existing 69 B1：保留 B1、补齐 flags。Impact on Top20 interpretation：无即时变化，主要改变置信解释。Re-adjudication workload：中等。

状态：`STAGE25B.2 COMPLETE — TIER A FEASIBILITY AUDITED; HUMAN DECISION REQUIRED`。
