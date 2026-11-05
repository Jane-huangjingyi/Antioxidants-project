# AFF-0061逐行科学审核准备 v0.1

本文件只编排下一轮审核，不作科学裁决。审核对象为原21条AFF-0061机制观察；21条记录不等于21项独立研究或21个独立实验。历史Gate2提案保持12条KEEP_PROVISIONAL、2条RECLASSIFICATION_PROPOSED、7条HOLD_SOURCE_VERIFICATION，所有记录的人工审核状态仍为 `NOT_REVIEWED`。治理批准不批准这些证据，也不应用257项待审科学提案。

建议依次处理A组9条来源可核查且分类争议较少的观察、B组5条需收窄因果或模型边界的观察、C组7条来源不足或冲突的观察。此处分组只反映审核顺序，不代表A组已达科学验收标准。

| 顺序组 | evidence_id | 历史提案状态 | 下一轮重点；人工状态均为NOT_REVIEWED |
| --- | --- | --- | --- |
| A | ME-AFF0061-37482908-001 | KEEP_PROVISIONAL | Kmo RNA-seq表达观察；区分表达与靶点结合 |
| A | ME-AFF0061-37482908-002 | KEEP_PROVISIONAL | Kmo qPCR验证；与同文组学共享研究来源 |
| A | ME-AFF0061-39589556-002 | KEEP_PROVISIONAL | NRF2相关GO富集；不虚构单一蛋白直接作用 |
| A | ME-AFF0061-41594941-001 | KEEP_PROVISIONAL | HDAC1丰度变化；不等于直接结合 |
| A | ME-AFF0061-41594941-002 | KEEP_PROVISIONAL | GATA4丰度变化；限定模型、比较与终点 |
| A | ME-AFF0061-41594941-003 | KEEP_PROVISIONAL | RELA定位观察；区分核转位与结合 |
| A | ME-AFF0061-41594941-004 | KEEP_PROVISIONAL | HDAC1 docking仅计算支持 |
| A | ME-AFF0061-42170612-002 | KEEP_PROVISIONAL | TAS2R16 MD仅计算稳定性支持 |
| A | ME-AFF0061-37025617-001 | KEEP_PROVISIONAL | p-eNOS比值；核查归一化及比较 |
| B | ME-AFF0061-32520409-001 | KEEP_PROVISIONAL | 全身Sirt3敲除下脂肪变性功能参与；不推导结合或抗氧化因果 |
| B | ME-AFF0061-32520409-002 | KEEP_PROVISIONAL | SIRT3 docking与人源3GLS/Q9NTG7元数据提案分开裁决 |
| B | ME-AFF0061-39589556-001 | KEEP_PROVISIONAL | 动物NRF2与Fig6L BODIPY；不移植细胞补回为动物rescue |
| B | ME-AFF0061-41594941-005 | RECLASSIFICATION_PROPOSED | HDAC1干预非加和；NS不代表零效应或等效 |
| B | ME-AFF0061-37025617-002 | RECLASSIFICATION_PROPOSED | Akt inhibitor IV通路支持；不指定AKT1或充分因果 |
| C | ME-AFF0061-42170612-001 | HOLD_SOURCE_VERIFICATION | α-amylase商业制剂与saliva图注冲突；物种/同工酶未定 |
| C | ME-AFF0061-42413844-001 | HOLD_SOURCE_VERIFICATION | TRAF2结合仅摘要；需全文方法、材料与读出 |
| C | ME-AFF0061-42413844-002 | HOLD_SOURCE_VERIFICATION | TRAF2/HAP1依赖仅摘要；需干预及对照 |
| C | ME-AFF0061-32007785-001 | HOLD_SOURCE_VERIFICATION | SIRT1/BV2摘要；不混同PC12模型 |
| C | ME-AFF0061-11023549-001 | HOLD_SOURCE_VERIFICATION | TYR/GSH摘要；拟收窄关系不解除总体来源HOLD |
| C | ME-AFF0061-11714376-001 | HOLD_SOURCE_VERIFICATION | 肝GSH，500 mg/kg腹腔注射；需全文条件 |
| C | ME-AFF0061-11714376-002 | HOLD_SOURCE_VERIFICATION | 肾GSH，0.1%饮水60天；百分比基准及摄入量未明 |

每条记录必须分别完成以下14个审核维度，并保存来源定位、当前值、建议值、裁决值和理由，不能以整篇论文一次批准替代逐行审核：

| 编码 | 必核维度 | 审核要求 |
| --- | --- | --- |
| D01 | 化合物及实验形式 | PCA身份、纯度/制剂、原型与代谢物分别记录 |
| D02 | 论文来源 | DOI/PMID、版本、原始论文与来源文件哈希 |
| D03 | 实验模型与材料 | 物种、组织/细胞、蛋白构建体、商业制剂身份 |
| D04 | 剂量和暴露基准 | 浓度/剂量、给药途径、时间、母液与终浓度分开 |
| D05 | 实验比较和对照 | 各组比较、载体、干预及交互作用所需对照 |
| D06 | 具体蛋白或通路对象 | 蛋白、家族、通路、GO集合不得相互替代 |
| D07 | 机制关系类型 | 表达/定位/功能参与/计算支持/直接结合分别判断 |
| D08 | 靶点确认类别 | 按批准v0.2完整规则裁决，不由关系标签自动升级 |
| D09 | 抗氧化相关性 | 直接redox终点与一般表型、富集关联分开 |
| D10 | 阴性或不利结果 | 阴性、NS、不利方向原样记录；不得只保留正结果 |
| D11 | 来源核查范围 | 全文/补充/摘要、页图表、未读部分及冲突明确记录 |
| D12 | 证据独立性 | 论文、样本、实验及重复观察层级分别判定 |
| D13 | 需要的修订 | 字段级旧值、建议值、理由及未决条件 |
| D14 | 人工裁决结果 | 保持待审直到具名审核；不能预填批准 |

未来人工审核矩阵建议以 `evidence_id + record_version + review_event_id` 为键，包含上述D01–D14及 `source_reference`、`source_file_sha256`、`rule_version`、`reviewer_name`、`reviewer_role`、`reviewer_project_authority`、`review_date`、`review_action`、`old_value`、`proposed_value`、`adjudicated_value`、`decision_reason`、`approval_scope`、`human_review_status`、`change_applied`。本轮不生成已签署的科学审核事件；未来审核矩阵初始 `human_review_status=NOT_REVIEWED`、`change_applied=NO`。审核完成也不直接写入生产库，字段实施仍须单独授权与验证。

需补充的来源按C组优先定位：TRAF2（PMID42413844，DOI10.1016/j.abb.2026.110937）原始全文未合法恢复，既往publisher403、机构库无附件不能替代全文；需要蛋白构建体/物种、剂量、真实结合方法及基因干预对照，不预设ITC或Kd。α-amylase（PMID42170612，DOI10.1016/j.crfs.2026.101435）需核对Methods2.7.2、结果/Table3与Fig2B的制剂矛盾，索取作者澄清、批次/目录或原始ITC；商业制剂9.4 U/mg不能由PDB1JXJ的人源P0DUB6推定身份，12 mmol/L注射器浓度不能充当终浓度。

SIRT1（PMID32007785，DOI10.1016/j.jneuroim.2020.577164）需全文剂量、时间、模型及对照；TYR/GSH（PMID11023549，DOI10.1093/carcin/21.10.1899）需20000 nmol局部处理3小时的完整条件、arbutin对照与选择性信息，不将不利GSH结果外推临床。肝/肾GSH（PMID11714376，DOI10.1021/jf0106594）需全文测定方法、对照及饮水百分比基准；500 mg/kg腹腔注射与0.1%饮水60天分别处理，无摄入量和体重不得换算mg/kg。

B组补核包括NRF2 Fig6L与M/N图注/标签冲突、S2 PDF第3页细胞补回与动物观察的边界；HDAC1 Fig5C–D非加和所需对照与置信区间（CoIP蛋白互作不等于PCA结合）；Akt inhibitor IV选择性及Sirt3全身敲除的基线、交互作用和途径。以上均为已有未决项的审核准备，不是本轮新读取全文后的裁决；不能凭二手数值、标题或审核进度解除HOLD。
