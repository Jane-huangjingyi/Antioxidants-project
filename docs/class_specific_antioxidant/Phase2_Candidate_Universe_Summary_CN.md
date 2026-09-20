# Phase 2 Candidate Universe Summary（CN）

## 1. Scope and method

本轮只依据 chemical identity、normal dietary occurrence、structural definition、class membership 和 normal dietary relevance 生成 universe。ORAC、DPPH、ABTS、FRAP、CUPRAC、NRF2 potency、target count、论文数和期刊影响因子均未参与纳入。所有历史 rank 均从 candidate master 中移除，仅用 `legacy_note` 指向归档。

## 2. Coverage results

共生成 **191** 个候选：**178 eligible**、**13 unresolved**；另保留 **12** 个明确排除项。PubChem 批量身份解析后仍有 2 个条目没有唯一 CID/InChIKey，均保持 unresolved，不允许进入 Phase 3 排名。

### Parent class counts

| Parent class | N |
|---|---:|
| Polyphenols | 103 |
| Other food-derived redox-active phytochemicals | 26 |
| Carotenoids | 19 |
| Organosulfur compounds | 15 |
| Betalains / nitrogen-containing phytochemicals | 11 |
| Vitamins / vitamin-like antioxidants | 10 |
| Antioxidant-related micronutrients / mineral cofactors | 7 |

### Analysis panel counts

| Analysis panel | N |
|---|---:|
| Polyphenols - Flavonoids | 59 |
| Polyphenols - Phenolic acids / conjugates | 29 |
| Other food-derived redox-active phytochemicals | 26 |
| Carotenoids | 19 |
| Polyphenols - Stilbenes / lignans | 15 |
| Organosulfur compounds | 15 |
| Betalains / nitrogen-containing | 11 |
| Vitamins / vitamin-like | 10 |
| Antioxidant-related micronutrients / mineral cofactors | 7 |

### Subclass counts

| Analysis panel / subclass | N |
|---|---:|
| Polyphenols - Stilbenes / lignans / Dietary parent lignans | 10 |
| Carotenoids / Xanthophylls | 10 |
| Other food-derived redox-active phytochemicals / Culinary spice phenolics | 10 |
| Polyphenols - Phenolic acids / conjugates / Hydroxybenzoic acids | 9 |
| Polyphenols - Flavonoids / Flavan-3-ols | 8 |
| Polyphenols - Phenolic acids / conjugates / Caffeoylquinic and related acids | 8 |
| Polyphenols - Flavonoids / Anthocyanins | 7 |
| Polyphenols - Phenolic acids / conjugates / Hydroxycinnamic acids | 7 |
| Antioxidant-related micronutrients / mineral cofactors / Mineral cofactors | 7 |
| Polyphenols - Flavonoids / Flavonols | 6 |
| Polyphenols - Flavonoids / Flavonol glycosides | 6 |
| Polyphenols - Flavonoids / Anthocyanidins | 6 |
| Organosulfur compounds / Isothiocyanates | 6 |
| Polyphenols - Flavonoids / Flavones | 5 |
| Polyphenols - Flavonoids / Flavanone glycosides | 5 |
| Polyphenols - Flavonoids / Isoflavones | 5 |
| Polyphenols - Phenolic acids / conjugates / Other defined phenolic conjugates | 5 |
| Polyphenols - Stilbenes / lignans / Stilbenes | 5 |
| Carotenoids / Carotenes | 5 |
| Organosulfur compounds / Allium sulfides | 5 |
| Betalains / nitrogen-containing / Betaxanthins | 5 |
| Other food-derived redox-active phytochemicals / Capsaicinoids | 5 |
| Polyphenols - Flavonoids / Flavone glycosides | 4 |
| Polyphenols - Flavonoids / Flavanones | 4 |
| Vitamins / vitamin-like / Tocopherols | 4 |
| Vitamins / vitamin-like / Tocotrienols | 4 |
| Carotenoids / Defined cis isomers | 4 |
| Betalains / nitrogen-containing / Betacyanins | 4 |
| Other food-derived redox-active phytochemicals / Dietary quinones | 4 |
| Other food-derived redox-active phytochemicals / Olive phenolics | 4 |
| Polyphenols - Flavonoids / Isoflavone glycosides | 3 |
| Other food-derived redox-active phytochemicals / Curcuminoids | 3 |
| Vitamins / vitamin-like / Water-soluble antioxidant vitamins | 2 |
| Organosulfur compounds / Thiosulfinates and derivatives | 2 |
| Organosulfur compounds / Water-soluble allium sulfur | 2 |
| Betalains / nitrogen-containing / Other dietary nitrogen-containing phytochemicals | 2 |

## 3. Coverage audit

候选丰富的 panels 是 Polyphenols - Flavonoids, Polyphenols - Phenolic acids / conjugates, Other food-derived redox-active phytochemicals，均达到或超过 20 个候选，可以在 Phase 3 完成 food-occurrence second review 后尝试 Top20。候选不足 20 的 panels 是 Polyphenols - Stilbenes / lignans, Vitamins / vitamin-like, Carotenoids, Organosulfur compounds, Betalains / nitrogen-containing, Antioxidant-related micronutrients / mineral cofactors；这些类别应采用 Top10 或 all eligible，不能为凑 Top20 加入边缘天然产物。Flavonoids、phenolic acids 和 other phytochemicals 的 universe 最完整；vitamins、betalains、minerals 和 stilbenes/lignans 的化学空间本来较小。Carotenoids 当前 19 个，接近但未达到 20，应优先完善真实膳食 cis/trans isomer occurrence，而不是机械补数。

身份风险最高的是 anthocyanin/betalain 的离子/盐/立体形式、caffeoylquinic positional isomers、carotenoid cis/trans forms、tocopherol/tocotrienol stereochemistry，以及 allium compounds 的 parent-versus-processing-generated 状态。Food occurrence 较薄弱的是 betalains、dietary quinones、部分海藻 carotenoids、ajoene、S-allylmercaptocysteine、podophyllotoxin 和少见 flavones；这些已标为 unresolved。食物来源证据最稳定的是常见 flavonoids、phenolic acids、vitamins、主流 carotenoids 和必需矿物质。

明确排除最多的类型是 mixture/aggregate variables、human/microbial metabolites、endogenous-only antioxidants 以及 supplement/medicinal dominant materials。主要排除原因包括 `total polyphenols/total carotenoids` 无唯一结构、extract composition 不固定、enterodiol/enterolactone 并非 dietary parent、glutathione/uric acid 主要为内源性，以及 NAC/baicalin/silymarin 等不满足正常膳食 gate。

## 4. Bias assessment

本轮没有使用 performance 或 publication count，因此没有把“研究多”直接写入 eligibility；但候选清单仍可能受已有 food databases 和英文文献的 popularity bias 影响。明显 geographic bias 包括：Phenol-Explorer 偏欧洲饮食，USDA/FoodData Central 偏北美食物，茶/大豆/香辛料数据库覆盖受亚洲地区研究影响，betalain、热带水果、海藻和地方香辛料可能被低覆盖。Phase 3 前的第二研究者审阅应纳入亚洲、拉丁美洲、非洲和地中海权威食物组成来源。

## 5. Phase 3 readiness

最容易开始 ranking 的顺序是：Flavonoids → Phenolic acids/conjugates，因为已有 H-ORAC SOP、record-level 数据和 tiering；随后是 vitamins（按水/脂相拆 construct）和 carotenoids（先冻结 singlet-oxygen/lipid assay QC）。Stilbenes/lignans 候选少，适合 Top10/all eligible。Organosulfur 应先冻结 causal KEAP1/NRF2/thiol-redox evidence rubric。Betalains需先处理光学干扰和 food occurrence。Other phytochemicals必须再次执行严格 dietary gate。Minerals不做 capacity ranking，仅构建 cofactor/deficiency/excess profile。

## 6. What is not completed

本轮未抽取 primary metric、未计算 rank/score/percentile、未生成 Top-N、未形成 Global Top Overview、未完成 cross-class comparability result、未冻结实验 panel，也未做 target mapping。Candidate master 中 `eligible=yes` 仅表示通过首轮身份与膳食存在 gate，仍需 candidate-level food reference 二次核验。

## Sync to ChatGPT

**A. Total：**191 candidates。**B. Parent counts：**Polyphenols=103; Vitamins / vitamin-like antioxidants=10; Carotenoids=19; Organosulfur compounds=15; Betalains / nitrogen-containing phytochemicals=11; Other food-derived redox-active phytochemicals=26; Antioxidant-related micronutrients / mineral cofactors=7。**C. Panel counts：**Polyphenols - Flavonoids=59; Polyphenols - Phenolic acids / conjugates=29; Polyphenols - Stilbenes / lignans=15; Vitamins / vitamin-like=10; Carotenoids=19; Organosulfur compounds=15; Betalains / nitrogen-containing=11; Other food-derived redox-active phytochemicals=26; Antioxidant-related micronutrients / mineral cofactors=7。**D. Subclasses：**共 36 个 subclass cells。**E. Excluded：**12。**F. Unresolved：**13。**G. Panels ≥20：**Polyphenols - Flavonoids; Polyphenols - Phenolic acids / conjugates; Other food-derived redox-active phytochemicals。**H. Panels <20：**Polyphenols - Stilbenes / lignans; Vitamins / vitamin-like; Carotenoids; Organosulfur compounds; Betalains / nitrogen-containing; Antioxidant-related micronutrients / mineral cofactors。**I. Bias risks：**food-database geography、known-compound familiarity、rare-food undercoverage。**J. Identity risks：**pigment ionic forms、glycosides、positional isomers、carotenoid stereoisomers、vitamin E stereochemistry。**K. Food gaps：**betalains、rare quinones、seaweed carotenoids、processing-generated allium compounds。**L. Recommended Phase 3 order：**Flavonoids → Phenolic acids/conjugates → Vitamins → Carotenoids → Stilbenes/lignans → Organosulfur → Betalains → Other phytochemicals；minerals 使用独立 cofactor framework。
