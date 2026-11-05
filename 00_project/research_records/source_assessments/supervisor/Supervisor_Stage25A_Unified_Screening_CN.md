# Stage 25A 统一文献证据筛选：导师汇报版

本阶段在 Stage 23 冻结的 157 个 aqueous candidates 内建立统一的 literature/evidence screening layer，回答“哪些候选具有较成熟、较广泛的 antioxidant/redox 研究基础”，不回答抗氧化能力、人体疗效或最终实验价值。由于不同类别的 primary construct 不可直接合并，Stage 25A 不跨类别平均 ORAC、LOX-FL、KEAP1/NRF2、金属调控或其他 assay；统一指标仅为 antioxidant/redox original-publication density。候选宇宙未新增、未删除，也未按文献数量反向调整。

检索使用 Europe PMC 的统一可复现式：候选规范名称或经人工限制的唯一同义词必须出现在标题，antioxidant、oxidative stress、redox、ROS、radical、lipid peroxidation 或 oxidative damage 等主题词出现在题名/摘要。排除 review、meta-analysis、editorial、commentary、conference abstract、book chapter、case report、retracted、docking-only、不可归因的 extract/food study 和重复索引记录。全文中同一 cohort、同一实验拆分发表无法由元数据完全裁定，因此当前 `antioxidant_independent_publication_N` 是“DOI/PMID/规范化标题去重后的独立论文代理值”；涉及 cohort/experiment reuse 的最终确认仍需人工全文复核。高论文数只表示 research maturity，不表示 potency、quality 或 human efficacy。

OpenAlex coverage audit 先选取 18 个跨类别、跨年代、跨文献密度和 identity complexity 的代表候选，37/37 篇原始证据均匹配 OpenAlex work，37/37 均有 citation metadata。全量运行中，41,967 条纳入记录有 40,233 条具 DOI/PMID，其中 40,193 条匹配 OpenAlex，标识符匹配率 99.90%；已匹配 work 的 citation metadata availability 为 100%。所有类别、年代层和 simple/complex identity 层均分别超过 95%。因此冻结 `OpenAlex = sole primary citation source`，检索日期为 2026-09-20；未混入 Google Scholar、Semantic Scholar 或 Crossref citation counts。1,734 条缺 DOI/PMID、38 条 OpenAlex work not found、2 条 identifier mismatch 已单独保留。

主排名前十为 Curcumin、L-ascorbic acid、Quercetin、Epigallocatechin、Gallic acid、Epigallocatechin gallate、Salicylic acid、Rutin、Caffeic acid 和 Ferulic acid。该顺序反映历史研究密度，并不表示它们是“最强抗氧化剂”。publication count 与 total citation 的 Top20 重叠 19/20、Top40 为 40/40、Top50 为 49/50；recent-five-year 的对应重叠为 18/20、39/40 和 46/50。citation-per-year 与主榜一致性明显较低，Top20 仅重叠 2 个、Top50 为 23 个，说明年轻论文和不同 exposure-year denominator 会显著改变该指标，因此它只能作为 sensitivity dimension。

完全不设 class quota 时，Top20 保留 flavonoids 8、phenolic acids/conjugates 7、other aqueous phytochemicals 3、organosulfur 1、vitamin-like 1，而 betalains 和 stilbenes/lignans 均为 0。到 Top40 时七个 aqueous panels 均出现，累计覆盖 87.2% 的 metadata-deduplicated publication units；Top50 覆盖 91.4%，citation overlap 为 98%，recent overlap 为 92%，并继续保留七个 panels。基于累计覆盖、稳定性、类别可见性和下一阶段 H-ORAC 工作量，建议把 **Top50** 作为 Stage 25B 的 provisional retrieval frame，而不是直接称为最终 shortlist。不得因类别代表不足自动设配额；若研究者希望强制保留低 publication-density class，需另行 `HUMAN REVIEW REQUIRED — CLASS REPRESENTATION`。

Stage 25B readiness 与 Stage 25A 排名分开。157 个候选中，86 为 Ready、45 为 Conditional、24 为 Not suitable for H-ORAC ranking、2 为 Insufficient identity。另有 11 个冻结候选保留 candidate-universe human-review 标记，其中两项缺完整 PubChem CID/InChIKey，其余为正常膳食/范围 gate 未决；本阶段没有静默修改。Top50 文件保留每个候选的 readiness 和不适用原因，后续只能对 Ready/经人工裁决的 Conditional 项开展 H-ORAC-FL quantitative screening。

本阶段最主要的限制不是 OpenAlex 覆盖，而是元数据筛选与真正全文独立实验判定之间的差距。高密度候选的计数需要抽样复核 candidate 是否为实际 exposure、redox endpoint 是否为研究结果而非背景，以及相同 cohort/experiment 是否拆分发表。建议在冻结 Stage 25B 输入前，对 Top50 进行双人分层抽样：高密度候选、human-study 候选、复杂 glycoside/conjugate identity 和跨榜不稳定候选分别核对；若误纳入率或依赖性合并明显改变名次，应重算而不是沿用当前代理值。
