# Stage25B.4 — Rubric v2 canonicalization and migration report

Rubric v2.0已canonicalized，69条原B1及current 4 B2、1 X全部完成一致性migration，共74 independent experiments。Pre-migration checkpoint与SHA-256 manifest保存在`data/h_orac_stage25b/checkpoints/stage25b3_pre_v2_migration_2026-09-22/`。

Tier分布由A/B1/B2/X=`0/69/4/1`变为`7/61/4/2`；transition为B1→A 7、B1→B1 61、B1→B2 1、B2→B2 3、B2→X 1、X→X 1，无B1→C/X。Chlorogenic Acid `HORAC_EXP_0067`已按批准正式B1→B2；figure-only Sinapic Acid `HORAC_EXP_0070`已正式B2→X。Baicalein、Cyanidin、Cyanidin 3-O-glucoside保持B2，未发现可自动执行的B2 upgrade。

Rankable candidates由29降至28，仅因Chlorogenic Acid失去唯一A/B1 evidence。Primary Top20 membership不变；rank20 Ferulic Acid=4.032 mol TE/mol，N=4、Moderate、HIGH_HETEROGENEITY；rank21 Morin=3.8745，N=2、Moderate、no high heterogeneity；gap=0.1575 mol TE/mol。A-only diagnostic包含6 candidates、7 experiments，与primary Top20重叠5 candidates。

B2 sensitivity仍加入Cyanidin 3-O-glucoside、Baicalein、Cyanidin，移出Luteolin、Naringin、Ferulic Acid。三条B2均因预定义optical/solubility/solvent comparability风险而不进入primary，并非因排名结果排除。没有新的rank-changing downgrade；但B2 sensitivity触及cutoff，且1,641条pending仍冻结未裁。因此本轮不自行freeze，状态为`STAGE25B.4 COMPLETE — RUBRIC V2 CANONICALIZED; FULL EVIDENCE MIGRATION COMPLETE; TOP20 HUMAN FREEZE DECISION REQUIRED`。
