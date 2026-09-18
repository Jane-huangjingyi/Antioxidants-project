# 抗氧化测定方法审计同步说明

## A. 最终是否推荐 ORAC

有条件推荐 ORAC-FL 作为 primary chemical antioxidant capacity metric。条件是主排序数据必须来自本项目锁定的 harmonized SOP，H-ORAC 与 L-ORAC 分臂测量并明确标记；不得把 ORAC 解释为人体抗氧化效果。

## B. 最重要的理由

ORAC-FL 采用持续生成的 AAPH-derived peroxyl radicals，评价竞争性 chain-breaking；其 kinetic fluorescence curve 和 net AUC 同时反映抑制程度与持续时间；Trolox 校准允许纯单体用 `mol TE/mol compound` 表示；H/L 两种实现覆盖不同极性，并存在经典标准化建议和 L-ORAC 实验室间验证。选择理由是构念和可执行性，不是文献量。

## C. 最重要的反对理由

ORAC 仍是体外模型且高度依赖 probe、radical flux、pH、温度、溶剂、时间窗和算法；AUC 不是基本速率常数，H-ORAC/L-ORAC 也不天然同标度。Carotenoids 等可能出现溶解、聚集和光学问题。ORAC 不能预测吸收、代谢或人体效果。因此推荐是“统一项目内化学排序”，不是“普遍抗氧化强度真值”。

## D. DPPH/ABTS/FRAP 为什么不是 primary

DPPH• 是非生理持久自由基，结果受立体可接近性、溶剂、反应时间和颜色影响；ABTS•+ 是人工自由基阳离子，生成方法、残余氧化剂、pH 和 endpoint 会改变排序；FRAP 只测 pH 3.6 下 ferric reducing power，不测 radical chain-breaking。三者均可有用，但不适合承担唯一主构念。

## E. 应保留的 secondary assays

CUPRAC 作为优先 ET/reducing-power complement；ABTS、DPPH 和 FRAP 作为固定 protocol 的机制对照；TRAP 作为 total peroxyl trapping 验证；一个预先规定的 lipid-peroxidation model 用于脂相/食品情境。HORAC、TOSC、superoxide、hydroxyl-radical 和 metal-chelation assays 属 supportive。

## F. ORAC 数据能否跨论文合并

默认不能。只有化合物形式与纯度、H/L 类型、AAPH/fluorescein/Trolox 浓度、buffer/pH、温度、溶剂/RMCD、加样顺序、读取间隔/总时长、AUC 公式、浓度线性和 QC 等价，并用共同 bridging standards 证明实验室间偏差可接受时才可合并。最佳方案是单中心统一复测。

## G. 推荐单位

纯化单体使用 `mol Trolox equivalents/mol compound (mol TE/mol)`；同时保存原始 concentration–net AUC slope、置信区间、板内/板间 CV、化合物纯度和具体 ORAC arm。µmol TE/mg 仅在身份、纯度和分子量明确时用于换算。

## H. 当前最大的可比性风险

最大的风险不是单位，而是同名 ORAC 下 protocol heterogeneity 被误当成同一测量。其次是用不同增溶体系强行比较亲水多酚、tocopherols 和 carotenoids，以及将 fluorescence interference 或不完全溶解误作低/高活性。

## I. 是否需要调整现有 Antioxidant Screening Protocol

需要在审核后增加一个 assay-specific annex：明确 ORAC-FL 是 chemical-capacity 域的主指标，限定其操作性定义、单位、H/L 分臂、最低元数据、QC、文献值准入和缺失处理。现有 protocol 中“cell-free assay 不能支撑人体结论”的原则保持不变。本轮遵守停止条件，未直接改动原 protocol。

## J. 是否建议下一步开始 ORAC 数据汇总

不建议立即批量汇总文献数值。建议先冻结 ORAC-FL SOP、QC compounds、可接受 CV、H/L bridging 规则和外部数据 eligibility checklist；随后做 6–10 个跨类别 pilot compounds 的统一测定或小规模方法复现。通过后再汇总符合完全等价条件的文献值，并为其余候选安排补测。

## K. Zotero 新增的关键方法学文献

均加入 `antioxidants project` collection：

| 文献 | DOI/PMID | Zotero item key | BibTeX key |
|---|---|---|---|
| Ou et al., ORAC-FL development/validation (2001) | 10.1021/jf010586o | 4FIGEV33 | ou_oracfl_2001 |
| Prior et al., H/L-ORAC-FL (2003) | 10.1021/jf0262256 | DZ8U424U | prior_orac_hl_2003 |
| Prior et al., standardized methods (2005) | 10.1021/jf0502698 | CD7CUABU | prior_standardized_2005 |
| Huang et al., chemistry behind assays (2005) | 10.1021/jf030723c | XM6ESFJM | huang_chemistry_2005 |
| Watanabe et al., interlaboratory L-ORAC validation (2016) | 10.2116/analsci.32.171 | B2R5YQVS | watanabe_lorac_validation_2016 |
| Schaich et al., ABTS/DPPH/ORAC pitfalls (2015) | 10.1016/j.jff.2015.01.043 | JGW8467V | schaich_pitfalls_2015 |
| Re et al., ABTS decolorization (1999) | 10.1016/S0891-5849(98)00315-3 | 6TM6YR4H | re_abts_1999 |
| Benzie & Strain, FRAP (1996) | 10.1006/abio.1996.0292 | PP8QVTAD | benzie_frap_1996 |
| Apak et al., CUPRAC (2004) | 10.1021/jf048741x | AYBQQLDP | apak_cuprac_2004 |
| Wayner et al., TRAP (1985) | 10.1016/0014-5793(85)81208-4 | LM2757JG | wayner_trap_1985 |
| Blois, DPPH (1958) | 10.1038/1811199a0 | U9QII5MG | blois_dpph_1958 |
| Winston et al., TOSC (1998) | 10.1016/S0891-5849(97)00277-3 | DFE36FWJ | winston_tosc_1998 |

## L. 需要研究者/ChatGPT 最终拍板的问题

1. 是否接受“ORAC-FL 为唯一 primary chemical metric，但不是总证据排名的硬门槛”。
2. 是否同意 H-ORAC 与 L-ORAC 分臂呈现，而不是未经验证直接混排。
3. 是否批准先制定 SOP 并做跨类别 pilot，再开始大规模数据汇总。
4. Secondary panel 是完整保留 DPPH/ABTS/FRAP/CUPRAC/TRAP，还是资源受限时采用 CUPRAC + lipid-peroxidation + TRAP 的精简组合。
5. 外部文献值是否只作支持性证据，除非通过严格的 protocol-equivalence checklist。

本轮没有生成 Top20、没有进行任何候选排名，也没有修改 compound–target pipeline。
