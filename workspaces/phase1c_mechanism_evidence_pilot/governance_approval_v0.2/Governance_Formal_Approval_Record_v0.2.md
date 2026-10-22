# Governance v0.2 正式批准记录

Antioxidants-project 将24项 Governance v0.2 决策作为未来机制证据数据库的治理基准。批准日期为2026-10-22；记录类型为 `GOVERNANCE_APPROVAL`，不是 `EVIDENCE_SCIENTIFIC_APPROVAL`。批准包括15项基础原则和9项实施政策，全部采用来源版本中的规则，不新增科学定义。

用户当前任务附件明确提供其在ChatGPT对话中的确认：

> 我确认正式批准24项Governance v0.2治理规则作为Antioxidants-project的项目基准。

此处归档用户声明的项目负责人授权。归档依据是当前用户附件对既往确认的明确转述；未独立读取既往ChatGPT原始对话，也未进行外部身份认证。附件位置与SHA256见 `qc/Start_Baseline.json` 及基准清单，附件本身不复制入库。

```text
record_type=GOVERNANCE_APPROVAL
governance_version=Governance_v0.2
approval_date=2026-10-22
approver_role=PROJECT_OWNER
approver_name=NOT_PROVIDED_IN_APPROVAL_MESSAGE
approval_source=USER_EXPLICIT_CHAT_CONFIRMATION_2026-10-22
approval_scope=GOVERNANCE_RULES_ONLY
signature_method=EXPLICIT_CHAT_CONFIRMATION
identity_verification=NOT_INDEPENDENTLY_VERIFIED
signature_time=NOT_PROVIDED_IN_APPROVAL_MESSAGE
approval_time_precision=DATE_ONLY
governance_approval_status=APPROVED
implemented_in_production=NO
evidence_scientific_approval=NOT_GRANTED
```

姓名未从Git作者、账户名或其他文件推断。只记录批准日期，不生成签署时刻、手写签名、电子签名证书或独立认证。

批准内容绑定来源分支 `codex/phase1c-governance-v0.2-dryrun`、提交 `9c6be49bac03a16bab1aa49790124dbdaf7a6af0`。规则全文依据 `../governance_v0.2_dryrun/Governance_Decision_Record_v0.2.md`，逐项文本依据同目录 `Governance_Decision_Diff_v0.1_to_v0.2.csv` 的 `v02_recommendation`。新矩阵逐字保存该列，同时保存完整规则文件引用及文本哈希；GOV-02风险触发正交验证、GOV-03情境性功能参与、GOV-08抗氧化标签优先级、GOV-22已审子集Gate2政策均以完整v0.2记录为准，不以摘要替代完整条件。

15项基础原则为GOV-01、04、05、06、07、09、10、12、14、15、16、17、18、20、24；9项实施政策为GOV-02、03、08、11、13、19、21、22、23。新的 `Governance_Approved_Decision_Matrix_v0.2.csv` 登记当前批准状态，原v0.1/v0.2历史文件中的待签署状态保留为历史，不回写覆盖。v0.2明确实施政策优先；未被替代的v0.1定义、受控词表和Gate标准继续适用。基准清单同时绑定这些继承规则及Schema设计的来源提交和SHA256。

生效范围限于未来机制证据数据库治理政策。逐条科学证据、正式数据迁移、候选物扩展、网络医学分析、正式分析或排名、数据库发布均不在批准范围。不得据此改变 `human_review_status`、`evidence_status`、`target_confirmation_class`、`antioxidant_relevance_primary`。原演练数据继续为 `NON_PRODUCTION_DRYRUN`；引用Schema或表契约不构成生产实现验收，清单也不将整个演练目录冻结为生产数据库。

后续规则变更须新建版本、追加变更记录、明确项目负责人授权、评估影响并生成新哈希；不得静默覆盖本v0.2基准。证据科学裁决、生产迁移和发布分别需要独立授权与验收。归档提交SHA由Git历史和最终交付报告提供，不在自引用清单中编造未来提交值。
