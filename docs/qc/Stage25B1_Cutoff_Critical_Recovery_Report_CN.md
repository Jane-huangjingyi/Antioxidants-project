# Stage 25B.1 — cutoff-critical 原始全文恢复与重算

本次仅处理 DOI `10.1089/jmf.2009.0024` 与 `10.1021/jf0208132`，没有继续处理其余 1,641 条记录，也没有修改 frozen Tier A rubric。Zotero 本地 API 已启用但客户端未运行，因此未能读取本地附件。对 `10.1089/jmf.2009.0024`，出版社 PDF 仍返回 403；OpenAlex 将其标为 green OA，并列出 AECID/LA Referencia 的 submitted-version records，但三个 Handle 均返回 404，AECID endpoint 未提供可核查文件。对 `10.1021/jf0208132`，OpenAlex 标为 closed，`any_repository_has_fulltext=false`，出版社、PubMed 与书目来源均未给出原始全文。两篇均未合法恢复到可核查的 primary full text，故严格保留 `SOURCE_NOT_RECOVERED / X`，没有用摘要、数据库摘要或二手文献中的数值替代。

由于两篇均维持 X，A+B1 evidence set 与本次恢复前完全相同；重算后的 primary rank 15–25 为：15 Sinapic acid 5.99，16 p-Coumaric acid 5.01，17 Hesperidin 4.50，18 Luteolin 4.136，19 Naringin 4.11，20 Ferulic acid 4.032，21 Morin 3.8745，22 Myricetin 3.416，23 Epigallocatechin 3.252，24 Chlorogenic acid 2.21，25 Eugenol 2.12 mol TE/mol。Primary A+B1 Top20 membership 没有变化；rank 20 cutoff 仍为 Ferulic acid 4.032，rank 21 仍为 Morin 3.8745。

A+B1+B2 sensitivity 也按现有 frozen classification 重算。其 rank 15–25 为：15 Rutin 6.705，16 Sinapic acid 5.99，17 Baicalein 5.41，18 p-Coumaric acid 5.01，19 Hesperidin 4.50，20 Cyanidin 4.40，21 Luteolin 4.136，22 Naringin 4.11，23 Ferulic acid 4.032，24 Morin 3.8745，25 Myricetin 3.416 mol TE/mol。与 primary Top20 相比，sensitivity 增加 Cyanidin 3-O-glucoside、Baicalein、Cyanidin，移出 Luteolin、Naringin、Ferulic acid；因此 B2 sensitivity 仍改变三项 membership，但这不是本次全文恢复造成的新变化。

Tier A feasibility 继续保持 `HUMAN REVIEW REQUIRED — TIER A FEASIBILITY`；A=0、B1=69、B2=4、X=1 的 experiment-level distribution 未改变。结论仍为 `STAGE25B.1 HUMAN REVIEW REQUIRED`：两项 cutoff-critical provenance 问题尚未解决，primary Top20 membership 相对恢复前没有变化，且不得冻结 Stage25B Top20。本次到此停止。
