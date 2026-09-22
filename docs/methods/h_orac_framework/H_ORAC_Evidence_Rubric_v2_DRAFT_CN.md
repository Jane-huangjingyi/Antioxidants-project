# H-ORAC Evidence Rubric v2.0 DRAFT

> **DRAFT — NOT YET CANONICAL**  
> 研究者已选择 Option B（Universal Core + Risk-Triggered QC），但本文件仅用于 Stage25B.3 validation。旧 rubric、canonical evidence tiers 与排名继续有效，直至另行人工批准 full migration。

## Architecture

v2.0 draft 采用五层结构：第一层确认 pure-compound identity 与 H-ORAC-FL universal core；第二层建立 R1 optical、R2 solubility/aggregation、R3 cosolvent/matrix、R4 redox/probe-interaction 风险；第三层只对触发的 MODERATE/HIGH risk 要求 enhanced QC；第四层分配 simulated A/B1/B2/C/X；第五层独立保存 identity、purity、optical、solubility、aggregation、cosolvent、matched-control、redox、reporting、source-access 与 protocol-traceability flags。QC flag 不直接等于 tier，purity numerical value missing 也不自动等于 B2。

## Universal core

ESSENTIAL：unique identity 与 consequential form；AAPH–fluorescein–Trolox aqueous/buffer construct；buffer identity、pH、temperature 与 reagent concentrations，或真正完全可追溯的 referenced protocol；candidate concentration/range 与可解释 dose-response；stock solvent 和 final reaction solvent 可解释；kinetic fluorescence decay与 net AUC或科学等价的 kinetic ORAC calculation；原始 quantitative value、unit和 mol TE/mol conversion可重复；value对应 defined pure compound而不是 food/extract。

IMPORTANT：replicate/precision 足以解释；purity、grade和supplier分层记录。缺少 numerical purity 会降低 reporting completeness，但在没有 material impurity concern 时不自动降到 B2。DOCUMENTATION：instrument、plate、reading细节等用于reproducibility，但只有在影响核心动力学解释时才升级为 comparability gate。RISK-DEPENDENT：compound-specific optical correction、direct aggregation test、enhanced cosolvent bridge和redox-mechanism control，仅在客观 trigger 达到 MODERATE/HIGH 时成为 Tier A mandatory。

## Reporting provenance states

`EXPLICITLY_REPORTED` 表示原文直接给出；`DERIVABLE_FROM_METHOD` 仅在 stock concentration、stock solvent composition、assay concentration、transfer/reaction volume均明确且无额外 dilution ambiguity 时使用；`TRACEABLE_TO_REFERENCED_PROTOCOL` 要求被引 protocol 唯一、可取得，且本文未声明修改相关条件，不能因“按某法”而自动补齐全部字段；`NOT_REPORTED` 表示全文未找到；`UNCLEAR` 表示现有证据不能区分。五种状态不得合并。

## Risk-triggered enhanced QC

R1 optical：已知吸收与 fluorescein excitation 465–505 nm 或 emission 500–550 nm 重叠、相关波段 intrinsic fluorescence、anthocyanin/betalain/strong visible chromophore 或浓度依赖 quenching 触发 HIGH；普通 UV chromophore在较高 assay concentration且无 spectrum 时触发 MODERATE。MODERATE/HIGH 需要 compound-only fluorescence/absorbance control、inner-filter correction、matched blank或等效 validation。

R2 solubility/aggregation：可见沉淀、浑浊、nonmonotonic response或浓度超过有证据的 aqueous solubility为 HIGH；需要有机 stock、客观低溶解度/较高 lipophilicity或 exposure接近可溶界限为 MODERATE。需要 concentration below plausible limit、monotonic dose response、controlled cosolvent、no precipitation evidence，必要时 direct aggregation assessment；不要求所有小分子做 DLS。

R3 cosolvent：final organic cosolvent ≤1%为 LOW，>1–5%为 MODERATE，>5%为 HIGH；RMCD/detergent造成arm改变也为 HIGH。MODERATE/HIGH 需要 samples、Trolox和blank之间 matched solvent control；HIGH 还需要 kinetic equivalence或validated bridge。若 final percentage仅可推导，必须保留 derivation与假设。

R4 redox：quinone/quinone-like electrophore、已有 redox cycling/prooxidant response、probe reaction或radical generation证据触发 HIGH；需要orthogonal或kinetic control排除非scavenging机制。若 validation set 无相应实验，只定义规则，不新增检索。

## Tier definitions

Tier A：universal core fully satisfied，所有 triggered enhanced QC均得到充分处理，quantitative traceability high。Tier B1：universal core足以支持定量比较，没有可能使排名失效的 unresolved material compound-specific risk，但仍有报告或非关键QC限制。Tier B2：存在定量 H-ORAC-like value，但至少一个 material comparability risk未解决，只进入sensitivity。Tier C：已知 assay construct、arm、probe、radical或normalization与 frozen H-ORAC-FL ranking不兼容。Tier X：source、method identity、chemical identity或quantitative provenance不足，无法裁决。

## Validation guardrail

Stage25B.3 的 tier simulation先使用 method/evidence fields和上述 risk rules，再读取排名影响。规则不会因为候选是否进入Top20而改变。任何 simulated transition均不是 canonical tier change。
