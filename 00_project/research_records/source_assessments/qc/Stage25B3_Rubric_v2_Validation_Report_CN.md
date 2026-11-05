# Stage25B.3 — H-ORAC Evidence Rubric v2 validation

## Scope and frozen state

研究者已冻结选择 Option B：Universal Core + Risk-Triggered QC。本轮仅进行 DESIGN → VALIDATE → HUMAN REVIEW，不是full migration。开始与结束时canonical state均保持：aqueous universe 157、Stage25A Top50 50、Stage25B retrieval 47、A/B1/B2/X = 0/69/4/1、rankable candidates 29、primary rank20 Ferulic Acid 4.032、rank21 Morin 3.8745；旧rubric、canonical tiers、Top20与1,641条pending records未修改。

## Draft and blind validation

v2 DRAFT正式定义universal core、五类reporting provenance state、四个objective risk domains、enhanced-QC pass/fail规则、A/B1/B2/C/X及独立flags。Validation set固定为Stage25B.2的15条B1、当前4条B2和1条X negative control，共20条。Tier decisions先依据method/evidence fields和risk profile完成，之后才计算ranking impact；结果不作为规则修改输入。

模拟transitions为：B1→A 5、B1→B1 9、B1→B2 1、B2→B2 3、B2→X 1、X→X 1。五条B1→A来自方法核心完整且未触发未解决enhanced QC的phenolic-acid experiments；5/15并非“大量自动升级”，同时flavonoid、hydrophobic或protocol-detail不足的9条仍为B1，说明v2恢复了有限但有意义的A/B1 discrimination，而非简单放宽。没有B2→A/B1。

Baicalein继续B2：moderate optical risk、high solubility/aggregation risk、final solvent与matched control未解决。Cyanidin及Cyanidin 3-O-glucoside继续B2：anthocyanin optical/inner-filter、pH stability与可能的probe interaction属于HIGH/MODERATE triggered risks，原证据无enhanced QC。第四条Sinapic Acid B2为figure-only且没有exact numerical value/unit extraction，v2 simulation将其标为X；这是quantitative provenance收紧，不是rank outcome驱动。现有X Chlorogenic Acid historical record继续X，因为positional identity与conversion未解决。

Stage25B.2 Chlorogenic Acid `HORAC_EXP_0067`由B1模拟为B2。方法可推得约10% final methanol，但matched ORAC solvent control未明确，属于R3 HIGH且未通过；正式downgrade仍需人工裁决。该experiment是validation中唯一新的B1→B2风险。

## Ranking impact simulation

Simulation只从primary A+B1排除`HORAC_EXP_0067`，不覆盖canonical ranking。Chlorogenic Acid失去唯一eligible B1并退出simulated rankable set；它原rank24，因此Top20 membership不变，仍无enter/leave，rank20为Ferulic Acid 4.032，rank21为Morin 3.8745。现有B2 sensitivity仍会将Cyanidin 3-O-glucoside、Baicalein、Cyanidin加入Top20并移出Luteolin、Naringin、Ferulic Acid，所以cutoff仍对B2不稳定。

## Required conclusions

Q1：v2恢复了有意义但克制的A/B1 discrimination，5/15 sampled B1达到simulated A，9/15仍为B1。Q2：未观察明显over-upgrade；有风险或protocol/detail不足者没有自动升级。Q3：出现1条新的B1→B2 risk，即`HORAC_EXP_0067`。Q4：三条有exact value的现有B2继续B2合理；figure-only Sinapic更符合X，需人工确认。Q5：Chlorogenic Acid应先核实working dilution和matched solvent control；在约10% unmatched methanol成立时建议B2。Q6：simulated primary Top20 membership不变，rank20/21不变。Q7：B2 sensitivity仍改变三项Top20 membership。Q8：建议在研究者批准v2且先裁决Chlorogenic及figure-only Sinapic后进入full 69 migration。Q9：full migration需要补抽identity/form、purity层级、AAPH/FL/Trolox concentrations、buffer/pH/temperature、candidate range、stock/final solvent及derivation、matched controls、kinetics/AUC、replication、optical/solubility/aggregation/redox risk和source/protocol traceability。Q10：不必机械重新打开69次全文；同一source的方法字段和protocol traceability可source-level复用，但compound-specific identity、concentration、purity、risk profile、triggered QC与value location必须逐experiment确认。

## Completion state

`STAGE25B.3 COMPLETE — RUBRIC V2 VALIDATED; HUMAN APPROVAL REQUIRED`。建议进入full migration，但必须先取得研究者对v2.0 draft、Chlorogenic Acid solvent comparability与figure-only Sinapic B2→X simulation的明确决定。
