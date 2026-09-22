# Stage25B H-ORAC 选择与排名最终方法

## 工作流

157 个 aqueous candidate universe → unified research-evidence-density screening → Stage25A provisional Top50 → H-ORAC applicability QC → 47 个 retrieval candidates → H-ORAC literature retrieval → canonical evidence adjudication → H-ORAC Evidence Rubric v2.0 → Tier A/B1 eligible quantitative evidence → 28 个 rankable candidates → Stage25B Frozen Top20 v1.0。

Stage25A primary metric 为 **metadata-deduplicated antioxidant/redox original-publication count**。legacy 字段 `antioxidant_independent_publication_N` 仅为 backward compatibility，**DO NOT INTERPRET AS INDEPENDENT-STUDY COUNT**；该指标也不是 antioxidant potency。

Primary ranking 仅使用 rubric v2.0 Tier A+B1 的独立实验，以 mol Trolox equivalents/mol compound 的 median H-ORAC 降序排列；不建立 publication、exposure、citation、human evidence 或其他维度的复合总分。B2 仅作预先规定的 sensitivity analysis。74 条已裁决实验迁移后为 A=7、B1=61、B2=4、X=2（C=0），形成 28 个 primary-rankable candidates。

## 可追溯性与解释

正式图由 `R/stage25b5/` 脚本读取 frozen CSV 生成；frozen candidate provenance 可回溯至 experiment ID、publication/source ID 与 DOI。排名解释限于当前 candidate universe、当前已裁决证据、rubric v2.0 和 A+B1 eligibility rule。

## 限制

1. H-ORAC 是化学抗氧化容量构念，不是人体疗效。
2. 只有 H-ORAC-compatible 候选可进入该定量汇聚。
3. B2 因未解决的 material comparability risks 不进入 primary ranking。
4. 纳入 B2 会导致 Top20 三进三出。
5. 部分候选仅有一个 eligible experiment。
6. 多个候选存在显著异质性。
7. rank20 与 rank21 仅差 0.1575 mol TE/mol。
8. Ferulic acid 标记为 HIGH_HETEROGENEITY。
9. 1,641 条 publication records 尚未完成全文裁决。
10. Stage25A 指标是 metadata-deduplicated antioxidant/redox original-publication count，不是独立研究数或抗氧化效力。
11. Top20 不是临床、营养或转化优先级排名。
