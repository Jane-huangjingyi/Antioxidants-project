# Stage25B.2 — Tier A feasibility audit

本轮仅审计现有 B1 evidence 的 Tier A 可行性，不处理剩余 1,641 条 publication records，不修改 rubric、B2 status 或 Top20。开始时 canonical state 与冻结状态一致：aqueous universe 157、Stage25A Top50 50、Stage25B retrieval set 47、experiment evidence A/B1/B2/X = 0/69/4/1、rankable candidates 29；primary rank 20 为 Ferulic acid 4.032，rank 21 为 Morin 3.8745 mol TE/mol。状态继续冻结为 `STAGE25B.1 HUMAN REVIEW REQUIRED` 与 `TOP20 CUTOFF UNSTABLE TO B2 EVIDENCE`。

## Sample and method

代表性样本为 15 个 independent B1 experiments，覆盖 current ranks 1–5、6–10、11–15、16–20 和 21–29，覆盖 singleton、2 和 ≥3 experiments，High/Moderate/Low confidence，HIGH_HETEROGENEITY 与非高异质性，以及 flavonoids、phenolic acids/conjugates 和较低水相兼容化合物。样本来自 7 个 sources、2001–2023；14/15 取得并重新核查 primary full text，2001 年 ACS source 未恢复全文，故其无法核实项标记 `UNCLEAR`，没有解释为 `NOT PERFORMED`。详细逐实验矩阵见 `Stage25B2_TierA_Feasibility_Audit.csv`。

## Criterion-level findings

22 项 criteria 的结果显示，A=0 由三类原因共同造成。第一，previous extraction incomplete：purity 在 8/15 被全文重新发现为 grade/supplier 信息，AAPH、fluorescein、Trolox range、buffer concentration、solvent、kinetic AUC 和 replicate detail 各有 9–14 条属于 `PREVIOUSLY_NOT_EXTRACTED`。第二，historical reporting incomplete：14 个可复核 experiments 中，compound-specific blank、explicit optical-interference control 与 aggregation assessment 均为 0/14 explicitly reported；这不能证明它们未执行。第三，current Tier A universally requires several controls whose scientific necessity is compound-risk dependent，因而对历史文献具有结构性低可达到性。

Purity missing 主要是 extraction completeness 与 reporting granularity 的组合，而不是 66 条研究都使用了未知质量化合物。本样本中 10/15 可从全文恢复数值 purity、analytical grade 或 supplier/grade 信息，其中只有 Eugenol/Capsaicin 两条给出 compound-specific numerical purity；四条全文只提供 supplier 或未给 compound-specific grade，一条早期全文不可得。未来应区分 certified/numerical purity、analytical/HPLC grade、supplier-only 与 truly unreported。

Compound-specific blank 在可复核样本中为 0/14 explicitly reported；一般 reagent/control blank 较常见，但不能等同 compound-only optical blank。将 compound-specific optical blank 作为所有历史 H-ORAC-FL experiments 的 universal Tier A gate，会使 Tier A 结构性接近空集。更合理的科学解释是：general assay blank 为 universal core；enhanced compound-specific optical correction 应由 absorption/fluorescence/chromophore risk 触发。Aggregation assessment 同样为 0/14 explicitly reported；其直接实验要求更适合 poorly soluble、hydrophobic 或 known colloidal-risk compounds，而 universal core 应是 concentration、solvent、solubility plausibility 与 dose-response review。本轮只提出此诊断，不修改规则。

Final cosolvent 的现实状态分为四类：明确报告 final percentage、可由 stock concentration/assay dilution 无歧义或近似推导、只报告 stock solvent、以及完全不可核实。Caffeic Acid source 明确 final ethanol 5% 并设置 matched controls；2014 phenolic-acid source明确全水相 buffer；2022 phenolic-acid source可由 80% ethanol/1000 µM stock 与 2.5–5 µM assay concentration推得约 0.2–0.4% ethanol，但文章未显式写 final %；Eugenol/Capsaicin 的上限可由 stock 与 assay concentration推得 trace ethanol；部分 flavonoid source 只说明 acetone/water stock 与 buffer dilution，无法可靠得到 final percentage。因此 future rubric 应接受 `EXPLICITLY_REPORTED` 或 `DERIVABLE_FROM_METHOD`，但必须分别记录。

真正影响 quantitative comparability 的 universal core 包括：unique identity/form、ORAC-FL、AAPH及其浓度或完全可追溯 protocol、fluorescein及浓度、Trolox calibration、buffer/pH、temperature、candidate concentration/range、solvent interpretability、kinetic net-AUC、replication、quantitative value 与 unit traceability。更适合作为 risk flags 或 risk-triggered mandatory QC 的是 enhanced compound-specific optical correction、direct aggregation test，以及针对高 cosolvent/低溶解度条件的增强 solvent/solubility validation。

## Experiment-level decisions

13/15 sampled experiments 维持 B1，但均未满足当前 strict Tier A 的全部 universal requirements；1/15 early experiment 因全文不可得维持 current B1 pending source recovery，不重新分类；0/15 可在 frozen rubric 下确认升级为 strict Tier A。Chlorogenic Acid `HORAC_EXP_0067` 的方法写明 20 µL methanolic compound sample进入 200 µL reaction well，可推得约 10% final methanol，但未明确 matched ORAC solvent control，且 assay material purity/form reporting 不充分。本轮只登记 `HUMAN REVIEW REQUIRED — POTENTIAL B1 DOWNGRADE`；它当前 rank 24，不在 Top20，未执行降级或排名重算。

## Required answers and interpretation

目前 A=0 不是单一原因，而是 historical reporting incomplete、previous extraction incomplete 与 universally strict risk-control gates 的组合。Purity missing 主要是旧 master 未展开 grade/supplier，再叠加历史论文较少给 compound-specific numerical purity。Compound-specific blank、optical control 和 aggregation test 在样本历史文献中极少明确报告；enhanced optical QC 与 direct aggregation testing 不适合作为所有化合物同强度的 universal gate，更适合作为 universal risk assessment + risk-triggered requirement。Final cosolvent 并非通常都显式可得，但部分可推导；显式值与推导值必须分开。当前存在一条 potential B1 downgrade，没有任何一条在 frozen strict rubric 下可确认 Tier A。当前 Tier A 作为 prospective gold standard 有意义，但对 historical evidence 的实际 discrimination value 很低，因为它把 reporting completeness 与 chemistry-specific risk controls同时作为 universal gate。

若保持当前 strict Tier A，无需重裁 69 条，只需承认 historical primary evidence 主要停留在 B1。若采用 universal core + risk-triggered QC，原则上需重新 adjudicate 全部 69 条 B1，建立每条 compound-specific risk profile；若仅改 A/B1 label 而不降出 A+B1，primary Top20 membership 不应改变，但 confidence interpretation 会改变，任何新发现的 B1→B2/C/X 才可能改变排名。若保留 A 为 prospective standard、historical evidence 采用 B1 + QC flags，则需为 69 条补齐 flags，但无需把全部重新分成 A/B1；Top20 的 quantitative set原则上不变。

## Options for human decision

Option A — KEEP CURRENT STRICT TIER A。Scientific rationale：保留理想 gold standard。Advantage：最高方法学严格度且无需 rubric migration。Disadvantage：历史 evidence 中 A 可能长期为空，reporting completeness 与实验有效性难以区分。Impact on existing 69 B1：维持原级，仅可选择性补抽字段。Impact on Top20：无即时变化。Re-adjudication workload：低。

Option B — UNIVERSAL CORE + RISK-TRIGGERED QC。Scientific rationale：所有实验满足 assay-comparability core，optical/aggregation/enhanced solvent QC 随 chemical risk 触发。Advantage：更贴合化学风险并恢复 A/B1 discrimination。Disadvantage：需要定义透明、可重复的 risk triggers，边界判断可能引入 reviewer variability。Impact on existing 69 B1：全部 69 条需要重新 adjudicate。Impact on Top20：纯 A↔B1 移动不改变 A+B1；若风险审查触发 downgrade则可能改变。Re-adjudication workload：高。

Option C — A AS PROSPECTIVE IDEAL; HISTORICAL B1 + QC FLAGS。Scientific rationale：将 prospective gold standard 与 historical comparable evidence 分离。Advantage：避免空 A，同时明确 optical/solubility/aggregation/cosolvent/purity uncertainty。Disadvantage：弱化 A/B1 两级在历史数据中的作用，并需要维护 flags。Impact on existing 69 B1：保留 B1，补齐 QC flags。Impact on Top20：无即时变化；flags改变解释而非数值集合。Re-adjudication workload：中等。

最终状态：`STAGE25B.2 COMPLETE — TIER A FEASIBILITY AUDITED; HUMAN DECISION REQUIRED`。Rubric 未修改，B2 未升级，Top20 未重算，剩余 1,641 条未继续处理。
