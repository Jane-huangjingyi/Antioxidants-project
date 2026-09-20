# Pre-Stage25B QC 与 shortlist freeze audit

Stage 25A 在冻结的157个aqueous candidates上建立了统一 literature screen。Stage25A.1 将正式主指标名称修正为 **Metadata-deduplicated antioxidant/redox original-publication count（元数据去重后的抗氧化/redox原始研究论文数）**，简写为 research-evidence density proxy。旧字段名为兼容历史脚本而保留，但不再出现在导师图标题、轴标签或主要结论中。该指标完成 DOI、PMID 和规范化标题去重，没有完成全部 same cohort/same experiment/full-text endpoint adjudication，因此不能称为 independent-study count。

OpenAlex 继续冻结为唯一 citation source：前置 audit 37/37 matched、37/37 citation available；全量 identifier-conditioned match 为99.90%，matched-work citation availability为100%，所有 class、年代和 identity-complexity strata均超过95%。本阶段没有混入其他 citation counts。

两张异常图的问题来自绘图代码，而不是底层数据：log10 axis 后使用数值型 `nudge_y`，导致标签位移把 y 轴扩展到1e+26。旧图已移入 `archive/figure_qc_stage25A1/`；新图只做一次log10 transformation，先过滤零值并用`vjust`放置标签，publication、citation和recent raw values未改变。

Top50 targeted QC逐候选检查 identity、synonym specificity、glycoside/aglycone、positional isomer、generic-name risk、duplicate indexing、redox relevance metadata、same-study risk和H-ORAC eligibility。没有发现可由当前metadata证据确认、且足以改变Top20/30/40/50/60 membership的 contamination；因此保留原research-density Top50，不重算、不补位。限制是未对41,967条records逐篇全文 adjudicate；高密度、人群研究和复杂form候选仍需后续抽样复核。

Top50的H-ORAC分流为：Ready 31；方法学Conditional且可按预定义QC进入检索12；`HUMAN REVIEW REQUIRED — CANDIDATE UNIVERSE` 4（Thymoquinone、Baicalein、Chrysin、Plumbagin）；Not suitable 3（Sulforaphane、Caffeine、Allicin）。因此当前实际 Stage25B retrieval-eligible set 为43，另有4个hold，不用第51名补位。Top50 research-density status与H-ORAC eligibility始终分开。

项目已按科学功能重构，Stage history保留在stage index和migration map。29张aqueous active canonical figures已由16个modular R scripts从项目根目录全部重建；长脚本移入`archive/R_legacy/`。建议在研究者裁决四个hold candidates并接受当前metadata-level独立性限制后启动Stage25B；本阶段不执行H-ORAC systematic retrieval。
