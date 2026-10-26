# 同步给ChatGPT：Batch A定点补核与人工裁决准备

2026-10-26，在Batch A提交48b34a7314b1d5914c4bb70f770e7e6d2fe939fe基础上，仅新增batch_a_targeted_followup目录，未覆盖原审核材料。新分支codex/phase1c-aff0061-batch-a-targeted-followup。新增科学来源调查仅为HDAC1计算、p-eNOS归一化与两条Kmo观察；其他A组建议明确沿用，不重新检索21条或展开B/C组。

HDAC1：正文MM-PBSA -12.21 kJ/mol与Fig6G kcal/mol冲突仍未解决。公开Europe PMC补充包已取得，唯一附件为7页未裁切blot PDF，没有MD结构、金属/配体参数或能量更正。PDB编号、物种/构建体、金属参数、配体质子化/拓扑、独立重复和对照仍待补。100ns图示时长、末20ns能量窗口及作者所报软件可定位，只能作定性计算描述；MM-PBSA定量、亲和/跨研究比较和实验结合主张必须暂缓，不择单位、不换算。附件第2页只更新HDAC1/GATA4丰度行的原图可用性，不认证原始实验或计算结合。

p-eNOS：Fig4B为p-eNOS/eNOS，Fig4D有总eNOS/GAPDH；重新核Methods2.7及出版社正文，未恢复densitometry完整公式。总图注relative to GAPDH与比值读数如何结合仍需作者澄清。保留作者报告的方向及读数，不再除一次GAPDH、不补算柱高、不宣称算法已核实。n=6–7的单位和overnight精确小时仍未解决。

Kmo：DataS1现已合法取得并用禁宏只读方式读出，内容为S1–S5图注，没有Kmo基因级差异结果表或本行重复/复用说明。RNA-seq特异fold change、raw p、校正p仍未恢复；qPCR Fig5D保留###p<0.001阈值和无ISO时NS，不填精确数值。DRA014580经ENA镜像映射到PRJDB14081/DRP011843，DRA与项目两个run清单一致：sham SAMD00517030/DRX381960/DRR396181；ISO SAMD00517031/DRX381959/DRR396180；ISO+PCA SAMD00517032/DRX381958/DRR396179。三组各一个存档样本/实验/run，不等于每组一只动物、不排除混样，也不证明RNA-seq与qPCR是独立队列。未下载FASTQ或重跑RNA-seq；如需重分析，须另行授权且先确认生物重复设计。

9条候选建议如下。ACCEPT仅接受有明确限制的提案送人审，不批准证据或解除任何来源条件；REVISION_REQUIRED先收窄表述/用途；SOURCE_PENDING需先补关键来源。三维科学分类与Batch A一致，均不是正式人工决定。

| evidence_id | Codex候选 | 人工裁决重点 |
| --- | --- | --- |
| ME-AFF0061-37482908-001 | SOURCE_PENDING_CANDIDATE | Kmo特异统计与生物重复/混样 |
| ME-AFF0061-37482908-002 | ACCEPT_PROPOSAL_CANDIDATE | 仅转录响应、阈值与NS，复用/n仍开放 |
| ME-AFF0061-39589556-002 | ACCEPT_PROPOSAL_CANDIDATE | 仅集合关联；不指认NRF2蛋白/激活 |
| ME-AFF0061-41594941-001 | ACCEPT_PROPOSAL_CANDIDATE | 仅HDAC1丰度；新附件不证明结合 |
| ME-AFF0061-41594941-002 | ACCEPT_PROPOSAL_CANDIDATE | 仅原行剂量GATA4丰度，不泛化显著性 |
| ME-AFF0061-41594941-003 | REVISION_REQUIRED_CANDIDATE | p65定位陈述收窄，缺专门核/胞质定量 |
| ME-AFF0061-41594941-004 | SOURCE_PENDING_CANDIDATE | 单位、结构、参数及定量用途限制 |
| ME-AFF0061-42170612-002 | REVISION_REQUIRED_CANDIDATE | 模拟接触不等于受体激活或充分收敛 |
| ME-AFF0061-37025617-001 | REVISION_REQUIRED_CANDIDATE | 保留报告比值，完整公式未明 |

需要研究者决定：是否接受上述限定用途、哪些条目需补证后再裁决，以及是否请求作者的原始参数/统计/样本映射。15项剩余不确定性有对应来源与使用边界，包含部分恢复及未重新核查的继承项。人工审核者姓名、人工决定和批准日期均为空，human_review_status=NOT_REVIEWED、change_applied=NO。

QC结果130 PASS / 0 FAIL，原763个跟踪文件和53个既有来源缓存SHA256不变；原21条、其余12条、66字段字典、257项历史科学提案及待审事件、7条来源HOLD、Governance规则、Master和H-ORAC Top20均未更改。两张CSV通过Artifact Tool作者值读回、全列快照核对、错误扫描及预览；技术QC不代表实验复现或科学批准。原文/图像/PDF/DOC/ZIP均本地忽略，不提交Git。

转交5份文件，以下为完整项目相对路径。项目根目录D:\JANE\GitHub\antioxidants project。

```text
P0 workspaces/phase1c_mechanism_evidence_pilot/batch_a_targeted_followup/BatchA_Targeted_Source_Resolution.md
P0 workspaces/phase1c_mechanism_evidence_pilot/batch_a_targeted_followup/BatchA_Human_Adjudication_Preparation.csv
P0 workspaces/phase1c_mechanism_evidence_pilot/batch_a_targeted_followup/Sync_to_ChatGPT_BatchA_Targeted_Followup.md
P1 workspaces/phase1c_mechanism_evidence_pilot/batch_a_targeted_followup/BatchA_Residual_Uncertainty_Register.csv
P2 workspaces/phase1c_mechanism_evidence_pilot/batch_a_targeted_followup/BatchA_Targeted_Followup_QC.md
```

可选复核附件为本目录qc/Followup_Source_Manifest.json、qc/Followup_Validation.json和访问日志；其余脚本与基线用于本地追溯，不是正式生产数据。最终归档commit SHA、push和工作树状态见最终交付消息及Git历史，文件不自引用未来提交。本文件是可转交说明，不表示已向外部ChatGPT会话发送消息。

完成后停止。Gate1=HOLD、Gate2=HUMAN_SCIENTIFIC_REVIEW_REQUIRED，Scale-up S1–S4及生产迁移NOT_AUTHORIZED，Release=HOLD。不自动批准、启动B/C组、迁移、扩展候选物、分析或改排名。
