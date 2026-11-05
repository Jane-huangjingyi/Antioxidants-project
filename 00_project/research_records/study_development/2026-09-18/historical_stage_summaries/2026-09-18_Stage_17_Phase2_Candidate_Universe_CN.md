# Stage 17 — Phase 2 Candidate Universe Construction

## 1. Stage purpose

为 9 个 analysis panels 建立不依赖 antioxidant performance 的统一 candidate universe。

## 2. Why this stage was necessary

Cross-Class Pilot Panel v1.0 只有 20 个有机代表，不能支持各类别 Top-N，也容易把 pilot inclusion 误解为最终选择。

## 3. Input

Taxonomy v1.0、历史 50-candidate H-ORAC universe、Cross-Class Pilot Panel、PubChem PUG REST identity records，以及 Phenol-Explorer、FooDB、USDA/EFSA/NIH ODS 等食物与营养来源优先级。

## 4. Method

按类别和食物相关性生成候选；批量核对 CID、InChIKey、分子式和分子量；分开 glycoside/aglycone、isomer、parent/conjugate 和 dietary parent/metabolite；保留 unresolved 与 exclusion records。没有使用任何 assay value、potency、target count、publication count 或 journal metric。

## 5. Decision rules

候选必须是正常膳食可摄入、结构明确的单一实体，有基本 food occurrence；未表征混合物、aggregate variables、内源性/代谢物冒充 dietary parent、supplement/medicinal dominant 项不进入 eligible universe。

## 6. Output files

| file | role | current status |
|---|---|---|
| `data/Antioxidant_Class_Candidate_Master.csv` | 统一 candidate universe | active |
| `data/Antioxidant_Taxonomy_Relationships.csv` | parent–panel–subclass 关系 | active |
| `data/Antioxidant_Candidate_Exclusions.csv` | 排除审计 | active |
| `docs/Phase2_Candidate_Universe_Summary_CN.md` | coverage/bias audit | active |
| `R/plot_antioxidant_atlas.R` | Phase 2 universe figures | active |

## 7. Main results

总计 191 candidates：178 eligible、13 unresolved，另有 12 exclusions。各 panels 为 Flavonoids 59、Phenolic acids/conjugates 29、Stilbenes/lignans 15、Vitamins 10、Carotenoids 19、Organosulfur 15、Betalains/nitrogen-containing 11、Other phytochemicals 26、Minerals 7。

## 8. Scientific interpretation

所有 Atlas 类别已有统一结构的候选基础，可以在审核后分别设计 class-specific ranking。

## 9. What this result does NOT mean

候选进入 universe 不表示其 antioxidant activity 高、人体有效或应进入 Top-N；candidate count 也不是类别科学重要性的量尺。

## 10. Limitations

食物来源仍需 candidate-level 第二研究者核验；数据库覆盖偏欧洲/北美及已知化合物；rare foods、betalains、海藻 carotenoids 和加工生成含硫物可能低覆盖。

## 11. Decision made

Phase 2 candidate universe 冻结为 v1.0；unresolved 不得进入 Phase 3 numerical ranking，除非身份和 food occurrence 问题解决。

## 12. Next stage

等待研究者和 ChatGPT 审核；通过后进入 Phase 3 class-specific Top-N，不自动产生 global score。
