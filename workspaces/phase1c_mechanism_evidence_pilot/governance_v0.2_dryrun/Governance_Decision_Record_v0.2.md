# Phase 1C Governance v0.2 待签署决策记录

日期2026-10-22（Asia/Shanghai）。前序分支codex/phase1c-governance-v0.1，前序SHA 7e62d3b6fcebda2d4941d8e93631d96959fc9581；本轮分支codex/phase1c-governance-v0.2-dryrun。v0.1未合并main，历史决策文件保持原样。此版记录用户附件所提供的ChatGPT科学审查建议和隔离结构演练授权；不冒称已经收到具名科学签署。

## 24项记录的状态

GOV-01、04、05、06、07、09、10、12、14、15、16、17、18、20、24共15项基础原则记录为SCIENTIFIC_RECOMMENDATION_ACCEPTED_PENDING_FORMAL_SIGNOFF。这是审查建议接受状态；formal_approval_status仍PENDING_FORMAL_SIGNOFF，signed_by和signoff_date为空，implemented_in_production=NO。其内容分别覆盖三维分类、药理边界、读数和互作对象、组学、计算、secondary/拆行、阴性结果、观察粒度、剂量、时序、缺失、来源、身份与文献、修订历史及冻结/发布边界。接受科学建议不改原数据库human_review_status。

另外9项为IMPLEMENTATION_POLICY_PROPOSED_PENDING_FORMAL_SIGNOFF，拟定政策如下。全部24项在Governance_Decision_Diff_v0.1_to_v0.2.csv逐项保留v0.1原规则、v0.2建议、审查意见、依据、适用范围、前置条件、正式批准及实施状态。未指定具名审核者，不填写HUMAN_APPROVED。

| 决策 | v0.2拟定政策 | 正式实施前置条件 |
|---|---|---|
| GOV-02 | 方法适配控制与风险触发正交验证；不一律要求两种方法；核蛋白身份、实际化合物形式、背景干扰、浓度、结果及对照。有聚集/荧光/非特异风险或制备物身份冲突不得直接升级确认结合 | 对应原始方法/结果、风险排查及有权审核者签署 |
| GOV-03 | 情境性遗传依赖可支持功能参与，不强制每条有救援；核基线、对象干预、比较、终点及时序。一组显著另一组不显著不等于交互显著 | 模型内比较审查，明确相互作用证据及适用边界，不搬运他模型救援 |
| GOV-08 | 六类primary和受控secondary保持；先按模型/剂量/时间/终点拆观察。促氧化/不利优先只作展示政策，不代表强度或临床危害 | 逐观察终点和标签依据核查，展示政策签署 |
| GOV-11 | 方案B主观察表＋少量关联表。优先Publication/Experiment/Observation/Review_Event；重复结构需要时增设实体与桥 | 结构/外键、原值恢复、维护责任与迁移批准；本轮只隔离演练 |
| GOV-13 | DOI数不等于独立实验数，检测数不等于独立样本数；共享材料要有来源，未知用UNRESOLVED_REUSE，不自动合并或重复计数 | 正式分析前核材料复用、独立性和分析单位 |
| GOV-19 | 正式科学批准须项目指定具名审核者；ChatGPT和Codex不能代签 | 指定姓名、权限、审核范围、数据/规则版本及签署日期 |
| GOV-21 | 技术QC为Gate1必要非充分条件，规则/版本/迁移核对/资产保护/具名验收缺一不可 | 本演练通过后仍单独验收正式Gate1 |
| GOV-22 | 指定已审版本子集可通过Gate2；HOLD保留但不进入验证靶点、验证抗氧化机制或正式支持计数。12暂保留不自动批准 | 精确子集/版本和逐行具名科学签署，隔离过滤验收 |
| GOV-23 | 暂定收集、已审主表纳入、正式分析排名、正式发布四权限独立；允许日后申请有限批次，当前均未授权 | 每项权限单独批准用途、候选范围、批次及版本 |

## 演练实施与生产实施分开

本轮允许将上述结构与QC约束在NON_PRODUCTION_DRYRUN副本中实现，因此“实际实施”必须区分dryrun_implementation和implemented_in_production。13张数据/审计表和3个视图仅是迁移演练，不是新正式数据库。257项字段分类/映射建议与257个待审Review_Event均为PROPOSED_NOT_APPROVED或PENDING_HUMAN_REVIEW，没有科学批准或生产应用。

Observation保留原21个ID和原始关系；其余原66字段通过实体投影及1386个Legacy_Field_Value单元格恢复。重分类建议单列Scientific_Proposal，新字段不作为有效事实写入Observation。sandbox_review_state仅技术隔离，7个来源HOLD仍不进入任何验证视图；原evidence_status与human_review_status逐字保留。

直接结合与功能参与、红氧相关性与临床意义、来源可核查度与人审状态继续正交。三条计算观察不升级实验，表达不升级必要性，NS不等同零/等效。原候选参考身份、实验形式、剂量和单位保持。未确认的设计/材料关联不强行补全；没有为S2创建第22条正式观察或虚构细胞实验ID。

## 科学依据与审查范围

本版按既有试点/Gate2/v0.1记录及用户2026-10-22任务附件落实政策，不开展新的论文有效性复核或新候选物检索。依据包括Gate2对TRAF2、amylase、Sirt3、NRF2、HDAC1、Akt/TYR的逐行核查和v0.1的FAIR/ARRIVE/NIH AGM方法依据；引用指针保留在旧文件，本轮没有把未重新访问的文献称为今日已验证。ChatGPT审查意见由用户提供，review_provenance如实记录USER_SUPPLIED_CHATGPT_REVIEW_IN_TASK_ATTACHMENT，不伪造独立人工审核。

Phase1B 14项风险、AFF-0082/AFF-0150缺失身份、临时crosswalk及冻结资产边界保持；未关闭TRAF2全文、amylase制备物、NRF2 M/N标签冲突、跨论文材料复用或原儿茶酸未完筛选。普通培养浓度单位本身不足以确认final或stock，隔离提案允许dose_basis为JSON null＋UNRESOLVED，而非为凑齐字段猜值。

## 待签署和下一步

由项目负责人指定具名科学审核者，再对24项政策、schema及所需逐行证据决定分别签署。正式Gate1=HOLD；Gate2=HUMAN_SCIENTIFIC_REVIEW_REQUIRED；Scale-up四权限=NOT_AUTHORIZED；Release=HOLD。技术演练、Git提交和推送都不改变这些状态。完成本轮后停止，不自动正式迁移、扩展检索或启动网络/排名/训练。
