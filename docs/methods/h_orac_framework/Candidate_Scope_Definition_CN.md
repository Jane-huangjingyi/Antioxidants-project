# Antioxidants Project 候选范围定义（冻结版）

## 1. 主候选资格

主候选必须同时满足：天然存在于正常膳食中的食品、饮料或常见香辛料；具有明确单一结构；属于可独立计量的小分子；可唯一映射 PubChem CID 与 InChIKey；具有可追溯的 food occurrence。未表征提取物、混合物、仅主要来自药用植物或补充剂的成分、以人体内源合成为主要来源的物质，以及无唯一分子结构的元素或材料不进入主候选榜。代谢物、结合物和肠道菌群产物保留在 secondary layer，不与膳食原型竞争。

“抗氧化”是功能属性，不是 chemical class。分类只依据化学骨架；ORAC compatibility 是与分类平行的测量属性。Phenolic acids 是 phenolic compounds 的一个 subclass，不与 polyphenols 并列成两个互斥大类。在本项目数据模型中，顶层采用 `Polyphenolic / phenolic compounds`，其下再区分 flavonoids、phenolic acids、stilbenes、lignans 等。

## 2. 冻结的 chemical taxonomy

| chemical class | subclass | example compounds | 纳入理由 |
|---|---|---|---|
| Polyphenolic / phenolic compounds | flavan-3-ols / catechins | catechin, epicatechin, EGCG, EGC, ECG | 常见茶、可可和水果成分，结构与食物暴露可追溯 |
| Polyphenolic / phenolic compounds | flavonols | quercetin, kaempferol, myricetin | 广泛存在于蔬果、茶和香辛料 |
| Polyphenolic / phenolic compounds | flavones | apigenin, luteolin | 常见于芹菜、欧芹、香草等食物 |
| Polyphenolic / phenolic compounds | flavanones | hesperetin, naringenin及明确糖苷 | 柑橘类常见；糖苷与苷元分别建实体 |
| Polyphenolic / phenolic compounds | anthocyanidins / anthocyanins | cyanidin及cyanidin-3-O-glucoside | 浆果和有色蔬果常见；苷元/糖苷不得合并 |
| Polyphenolic / phenolic compounds | isoflavones | genistein, daidzein | 大豆食物真实暴露明确 |
| Polyphenolic / phenolic compounds | phenolic acids / hydroxybenzoic acids | gallic, protocatechuic, vanillic acids | 食物来源广，结构单体明确 |
| Polyphenolic / phenolic compounds | phenolic acids / hydroxycinnamic acids | caffeic, ferulic, p-coumaric acids | 咖啡、谷物、果蔬中常见 |
| Polyphenolic / phenolic compounds | hydroxycinnamic-acid conjugates | chlorogenic acid (5-O-caffeoylquinic acid) | 重要膳食酚酸酯；明确异构体单列 |
| Polyphenolic / phenolic compounds | stilbenes | trans-resveratrol | 葡萄、花生和浆果中存在；顺反异构体分开 |
| Polyphenolic / phenolic compounds | lignans | secoisolariciresinol, matairesinol | 全谷物、种子和植物性食物来源明确 |
| Polyphenolic / phenolic compounds | other defined food phenolics | curcumin, capsaicin, carvacrol | 仅在正常香辛料暴露和结构均明确时纳入 |
| Vitamins / vitamin-like dietary antioxidants | vitamin C / ascorbic acid | L-ascorbic acid | 正常膳食来源明确，属于主候选；氧化形式另建实体 |
| Vitamins / vitamin-like dietary antioxidants | tocopherols | alpha-, gamma-, delta-tocopherol | 食用油、坚果和种子常见；异构体/立体化学分开 |
| Vitamins / vitamin-like dietary antioxidants | tocotrienols | alpha-, gamma-, delta-tocotrienol | 谷物和部分食用油中存在；同系物分别记录 |
| Carotenoids | carotenes | beta-carotene, lycopene, alpha-carotene | 蔬果中常见，脂溶性和异构体需结构化 |
| Carotenoids | xanthophylls | lutein, zeaxanthin, beta-cryptoxanthin | 叶菜、蛋黄和水果中常见 |
| Organosulfur compounds | isothiocyanates | sulforaphane | 十字花科真实膳食来源；主要机制可能不被 ORAC 捕捉 |
| Organosulfur compounds | thiosulfinates / related sulfur compounds | allicin及结构明确降解物 | 葱蒜来源，但稳定性和化学实体必须核实 |
| Other food-derived antioxidant small molecules | betalains | betanin, indicaxanthin | 甜菜、仙人掌果等食物来源明确；光学干扰需 QC |
| Other food-derived antioxidant small molecules | quinones | ubiquinone forms only when dietary parent exposure is meaningful | 必须区分膳食暴露与内源合成；通常进入 extended list |
| Other food-derived antioxidant small molecules | nitrogen-containing phytochemicals | betalain alkaloids, capsaicinoids or other defined entities | 仅在结构和正常食物暴露均明确时纳入 |

## 3. ORAC compatibility 分层

### H-ORAC-compatible / predominantly hydrophilic

多数 flavan-3-ols、flavonols、flavones、flavanones、anthocyanins、isoflavones、phenolic acids、L-ascorbic acid 和其他水溶性单体优先进入 H-ORAC。具体化合物仍需核实溶解度、pH、盐型、糖苷化和荧光干扰；“属于多酚”不自动等于方法无问题。

### L-ORAC-compatible / predominantly lipophilic

Tocopherols、tocotrienols、carotenes、xanthophylls 及其他高度脂溶性单体优先进入 L-ORAC，并完整记录 RMCD、共溶剂、溶剂比例和包合条件。L-ORAC 只在同一可比 arm 内排序；未经桥接验证不与 H-ORAC 合并。

### Technically problematic / special-case

Resveratrol等低水溶性 phenolics 可能依赖 cyclodextrin 或共溶剂；ascorbic acid 存在快速氧化和制样稳定性问题；tocopherols需锁定天然/合成立体异构体与 RMCD 包合；carotenoids存在溶解、聚集、异构化、光降解、氧分压、吸光和内滤效应；betalains存在强吸光/荧光干扰；organosulfur compounds 常通过硫醇交换、亲电感应或 Nrf2 等非典型机制作用。Special-case 不是排除标签，而是要求专门 QC，并承认 ORAC 可能低估或失真。

## 4. 明确不纳入主候选

不纳入：食品或植物粗提取物；多成分混合物；“总多酚”等操作性总量；蛋白、多糖及结构异质聚合物；无单一结构的矿物元素；人体内源性 glutathione、uric acid 等作为主候选；人体代谢物与结合物；主要依靠药用植物或补充剂达到暴露的化合物；只有 docking/network prediction 而缺乏真实食物发生证据的化合物。它们可作为 context、metabolite、extended 或 interaction nodes 保存。

## 5. Pilot 范围

本轮冻结 17 个代表性实体：EGCG、catechin、epicatechin、quercetin、kaempferol、gallic acid、caffeic acid、ferulic acid、chlorogenic acid、trans-resveratrol、L-ascorbic acid、alpha-tocopherol、gamma-tocopherol、lycopene、beta-carotene、lutein 和 sulforaphane。它们覆盖 10 个 phenolic/polyphenolic、3 个 vitamin/vitamin-like、3 个 carotenoid 和 1 个 organosulfur candidate。预期 assay arm 为 11 个 H-ORAC、5 个 L-ORAC、1 个非典型 special-case；其中 8 个候选另带至少一个技术 special-case flag，因此 arm 与 special-case flag 不是互斥字段。
