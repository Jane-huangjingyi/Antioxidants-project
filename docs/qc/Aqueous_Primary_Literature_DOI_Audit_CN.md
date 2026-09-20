# Aqueous Antioxidant Primary Literature DOI Audit

## Scope and interpretation

本轮采用经研究者确认的分层策略：对 Flavonoids、Phenolic acids/conjugates 和 Vitamin C 完成当前排名证据的 record-level consolidation；对 Stilbenes/lignans、Betalains、Organosulfur、Other aqueous phytochemicals、metal mechanisms 与 micronutrients 仅建立框架、锚点文献和缺口。锚点不得解释为系统检索完成。

## DOI completeness

证据主表共有 **109** 行，覆盖 **25** 个 paper/source units；其中 DOI 可用 **24**，DOI 缺失或来源未解析 **1**，paper-level DOI coverage 为 **96.0%**。Current-ranking core papers 为 **16**，preliminary/supporting papers 为 **7**。

| Class | Original papers | DOI available | DOI missing | Core ranking papers | Supporting papers |
|---|---:|---:|---:|---:|---:|
| Polyphenols - Flavonoids | 15 | 15 | 0 | 10 | 3 |
| Polyphenols - Phenolic acids / conjugates | 11 | 10 | 1 | 10 | 1 |
| Vitamin C — aqueous | 2 | 2 | 0 | 2 | 0 |
| Polyphenols - Stilbenes / lignans | 1 | 1 | 0 | 0 | 1 |
| Betalains / nitrogen-containing | 1 | 1 | 0 | 0 | 1 |
| Organosulfur compounds | 1 | 1 | 0 | 0 | 1 |

## Papers with broadest compound coverage

- Tabart (2009), DOI `10.1016/j.foodchem.2008.08.013`：16 compounds；H-ORAC-FL。
- Žuvela (2019), DOI `10.3390/ijms20092328`：14 compounds；H-ORAC-FL。
- Zhang (2013), DOI `10.1021/jp307746c`：11 compounds；H-ORAC-FL。
- Skroza (2022), DOI `10.3390/antiox11091784`：10 compounds；H-ORAC-FL。
- Ou (2001), DOI `10.1021/jf010586o`：9 compounds；H-ORAC-FL。

## Ranking provenance and unresolved items

三个 active ranking 的每个 aggregate 均可逆向连接到 legacy evidence ID，再连接 paper ID、DOI/PMID、exact location、original value/unit、conversion 和 normalized value。Evidence master 保留 legacy source file，未覆盖旧表。

当前排名中 single-paper supported compounds 包括：3,4-Dicaffeoylquinic acid, 3,5-Dicaffeoylquinic acid, 4,5-Dicaffeoylquinic acid, Chlorogenic acid, Cryptochlorogenic acid, Daidzein, Ellagic acid, Epicatechin gallate, Eriodictyol, Fisetin, Gallocatechin, Hesperidin, Isoquercitrin, Isorhamnetin, Kaempferol 3-O-glucoside, Myricitrin, Neochlorogenic acid, Quercitrin, Rosmarinic acid。这些候选的数值可追溯，但 confidence 仍低。

- `Legacy figure-only sinapic-acid ORAC report` 缺 DOI、paper identity 与精确数字，维持 B2/supporting，不进入排名。
- HORAC 和 β-phycoerythrin ORAC records 虽有 DOI 和数值，但与 H-ORAC-FL primary construct 不兼容，保留为 `excluded_incompatible`。
- 未发现仅靠 review citation 进入当前 A/B1 ranking 的记录；所有 current-ranking records 均映射至 original-study DOI。
- 多篇 B1 的 buffer、cosolvent、purity 或 compound-specific optical QC 仍不完整，因此没有升级 Tier A。
- Preliminary anchors 的 exact table/value 尚未全量抽取，明确标为 `anchor_unadjudicated`。

## Highest-quality evidence and class gaps

方法学最完整且影响多个 current ranks 的核心来源包括 Ou 2001、Dávalos 2004、Tabart 2009、Zhang 2013、Žuvela 2019、Sakurai 2022、Skroza 2022 与 Carvalho 2023。这里的“高质量”依据 defined compounds、明确 assay identity、可提取数值、单位、protocol metadata 和来源可追溯性，而非期刊影响因子。

证据最明显不足的是 Stilbenes/lignans、Betalains、Organosulfur 和 other aqueous phytochemicals；本轮各自只有候选框架或少量锚点。Metal-chelation/Fenton 与 micronutrient panels 也只是机制框架，尚不能进行 coverage 或 ranking 推断。

## Metal-ion and micronutrient status

Metal layer 已区分两类关系：有机小分子的 Fe/Cu chelation 或 Fenton suppression 属于 chemical antioxidant mechanism；Se/Zn/Mn/Cu/Fe 的酶辅因子、缺乏和过量效应属于 micronutrient/cofactor profile。二者都不是 protein direct-target evidence，也不进入 ORAC 排名。Fe/Cu 氧化态、pH、chelation 与 reduction/Fenton endpoint 必须在未来逐条抽取。

## HUMAN REVIEW REQUIRED

- 复核全部 rank-changing B1 conversions 和 paper exact locations；本轮不重新裁决 rank。
- 裁决 figure-only sinapic-acid legacy source的 paper identity。
- 对所有 metal anchors复核 Fe2+/Fe3+、Cu+/Cu2+、chelation、reduction 与 Fenton suppression 的边界。
- 对 betalain pigment optical interference、stilbene cyclodextrin/cosolvent、organosulfur class boundary 和正常膳食 gate 做第二研究者复核。
- Micronutrient recommended-intake 数值应在后续阶段从选定权威机构按地区、性别与 life stage 单独冻结。

## Sync to ChatGPT

**A. total aqueous candidates：**157。**B. active classes：**Flavonoids、Phenolic acids/conjugates、Stilbenes/lignans、water-soluble vitamins、Betalains/nitrogen-containing、water-compatible Organosulfur、other aqueous phytochemicals；metal mechanisms 与 micronutrients 为独立 profile。**C. total paper/source units：**25。**D. DOI coverage：**24/25（96.0%）。**E. core ranking papers：**16。**F. supporting anchor papers：**7。**G. class-specific paper counts：**见 DOI completeness table。**H. top papers by compound coverage：**Tabart 16；Žuvela 14；Zhang 11；Skroza 10；Ou 9。**I. single-paper support：**19 个 current ranked compounds。**J. unresolved mapping：**1 个 figure-only legacy source；preliminary anchors尚未完整 table-level extraction。**K. metal-chelation：**已建立 Fe/Cu/Fenton anchor framework，未系统检索。**L. micronutrients：**7 个 nutrient/context rows，均不做 ORAC rank。**M. active rankings：**Flavonoids Top20、Phenolic acids Top available 18、Vitamin C Top available 1。**N. paused lipid analyses：**Carotenoid `kq`、Vitamin E `k_inh`、L-ORAC profiles。**O. major gaps：**unranked aqueous classes、Tier A=0、optical/solubility/metal-state QC。**P. recommended next class：**Stilbenes/lignans 或 Organosulfur，由研究者依据 direct-capacity 与 causal-redox priority 选择。**Q. human review：**conversion、source identity、metal oxidation state、class/dietary gates。
