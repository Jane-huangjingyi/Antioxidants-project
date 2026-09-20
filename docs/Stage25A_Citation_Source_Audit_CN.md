# Stage 25A Citation Source Audit（CN）

## 冻结结论

**OpenAlex = sole primary citation source**

Audit panel包含18个代表性候选与37篇已在当前项目中判定为original antioxidant/redox evidence的独立publication units。候选跨越不同aqueous classes、publication density、发表年代与identity complexity；没有只选择高知名度化合物。`DOI/PMID → OpenAlex work matching rate`为 **100.0%**（37/37）；`citation metadata availability rate`为 **100.0%**（37/37）。两项阈值分别要求≥95%，不取平均；class-specific audit也应用同一95%门槛。

157候选全量运行提供了第二次验证。41,967条纳入记录中40,233条具有DOI或PMID，其中40,193条匹配OpenAlex work，故identifier-conditioned matching rate为 **99.90%**；40,193个matched works全部具有integer `cited_by_count`，citation metadata availability rate为 **100.0%**。按class、发表年代（≤1999、2000–2009、2010–2019、2020+）以及simple parent/aglycone与complex/form-specific identity分层后，两项指标仍分别≥95%。分层结果保存在`data/Stage25A_OpenAlex_Bulk_Coverage_By_Stratum.csv`。

## 方法

以Stage 24统一original-literature master中已经判定为candidate-specific antioxidant/redox original research的记录作为audit sampling frame。优先按DOI查询OpenAlex work endpoint，DOI未命中时再按PMID namespaced identifier查询；标题搜索只用于诊断失败原因，不将模糊标题匹配计为identifier match。Citation availability要求work成功匹配且`cited_by_count`为integer。Retrieval date为2026-09-20。

OpenAlex适合本项目的理由是identifier lookup可复现、work metadata包含publication year与`cited_by_count`、支持批量API和透明的开放数据模型。主要限制是citation coverage与去重规则仍会随OpenAlex更新，citation count是research attention而非evidence quality。Crossref可补DOI metadata但不是完整citation source；Google Scholar不可稳定批量复现；Semantic Scholar不与OpenAlex citation count混用。

## 失败分类与停止规则

未匹配清单保存在`data/Stage25A_OpenAlex_Unmatched_Publications.csv`，failure category严格使用：`missing DOI/PMID`、`identifier mismatch`、`OpenAlex work not found`、`work found but citation metadata unavailable`、`ambiguous match`。若总指标或任何明显class/年代/identity stratum低于95%，不得开始157候选的正式citation counting，也不得自行切换或混合citation sources。

全量失败记录另存于`data/Stage25A_OpenAlex_Bulk_Unmatched_Publications.csv`：`missing DOI/PMID` 1,734条、`OpenAlex work not found` 38条、`identifier mismatch` 2条、`work found but citation metadata unavailable` 0条、`ambiguous match` 0条。缺失identifier不进入“DOI/PMID→work matching rate”的分母，但作为上游provenance缺口单独报告；任何缺失项均未由其他citation source补值。
