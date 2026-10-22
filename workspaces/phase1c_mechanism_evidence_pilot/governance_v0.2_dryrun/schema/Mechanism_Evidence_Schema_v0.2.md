# 方案B隔离演练schema v0.2

NON_PRODUCTION_DRYRUN / schema_version=0.2_DRYRUN。所有CSV含dataset_role、schema_version列；空验证视图保留相同表头，其非生产用途同时由Table_Contract、Build_Manifest及本说明界定。没有额外生产CSV，也不导出未经批准xlsx版本。

## 表集与关联

| 数据/审计表 | 行数 | 主键 | 外键与语义 |
|---|---:|---|---|
| Publication | 15 | publication_id | 保存Study_Register所有字段的raw_投影；10篇有观察，排除/背景/暂缓5篇不删除 |
| Experiment | 21 | experiment_id | publication_id；原ID一对一保留，entity_scope=LEGACY_COMPARISON_NOT_INDEPENDENT_EXPERIMENT，不是21个已确认独立实验 |
| Observation | 21 | evidence_id | candidate_id沿用源候选；publication_id/experiment_id/source_check_id/intervention_id指向本表集；原关系和状态等以raw_保存 |
| Review_Event | 257 | review_event_id | evidence_id、proposal_id；每字段提案一个待审事件，无签署或应用 |
| Legacy_ID_Map | 57 | map_id | 15出版物＋21旧比较＋21观察映射；new_table/new_id动态外键需校验 |
| Source_Check | 21 | source_check_id | evidence_id/publication_id；历史来源范围映射，不声称新核查 |
| Legacy_Field_Value | 1386 | evidence_id＋field_name | 每原观察×66字段，raw_value精确恢复，field_order保留列序 |
| Scientific_Proposal | 257 | proposal_id | evidence_id/review_event_id；分类、映射建议与原事实隔离 |
| Observation_Tag | 4 | tag_id | evidence_id/proposal_id；仅secondary提案，禁止以标签行计证据数 |
| Observation_Target | 18 | observation_target_id | evidence_id；原对象投影不自动去重/合并为确定Target；3条无蛋白观察不造对象 |
| Intervention | 21 | intervention_id | evidence_id/experiment_id；只存原剂量、单位、时间和原比较上下文，不臆造Arm |
| Independence_Assessment | 21 | assessment_id | evidence_id/experiment_id；UNRESOLVED_REUSE，不推论文独立或共享材料 |
| Unresolved_Mapping | 23 | issue_id | publication_id必需；evidence_id/experiment_id可空，21设计材料事项＋NRF2 S2和M/N |

另有Verified_Direct_Targets、Verified_Antioxidant_Mechanisms、Verified_Evidence_Support三个派生验证视图，当前均0行。共13表＋3视图，不把字段映射、词表快照或决策差异算作科学数据表。机器合同Table_Contract_v0.2.json记录实际列、主键、静态外键和行数；Schema_Field_Mapping_v0.2.csv逐项说明原66字段的实体投影与恢复键。

Observation多对一Publication/Experiment在逻辑上允许；本次不自动合并旧experiment_id。各Material/Arm/Target的实际统一实体均未获足够来源，故本演练不新造这些实体表或共享ID。Experiment/Observation.material_id为空且material_missing_reason=UNRESOLVED；Intervention.parsed_control_arm_id为空且control_mapping_status=PENDING_ARM_EXTRACTION。原control_group等复合文本只是原始上下文保留，不冒称已经完成多臂/多对多标准化；本次真正出现的多值secondary用Observation_Tag桥。未来资料足够时需Material、Arm、Observation_Arm、Intervention分成分记录等扩展，不用自由文本替代正式多对多关系。

候选身份在Observation.raw_candidate_id、raw_compound_form、raw_PubChem_CID、raw_InChIKey及完整legacy层保留；candidate_id为外部只读候选键，当前只出现AFF-0061。未复制整个191候选生产主表。若未来引入Compound内部实体，须对照T002做FK核验，不从名称补身份。Study_Register是出版物登记，不迁成生物学独立Study。

## 原始层、规范映射和科学提案

raw_列和Legacy_Field_Value.raw_value是“原提取记录的事实”，不宣称底层科学结论已验证。Publication.raw_来自Study_Register；若它与某观察出版元数据不同，不覆盖，原观察可从legacy层恢复。所有1386值按文本保留，包括原哨兵、大小写、单位、日期精度与source_locator。字段恢复不依赖推断或重分类。

Scientific_Proposal逐观察演示12个字段：target_confirmation_class、antioxidant_relevance_primary、antioxidant_relevance_secondary、dose_basis、redox_measurement_level、readout_level、result_direction、result_significance、source_scope、source_issue、missing_reason、independence_relation。12×21=252项，加Akt/TYR关系2项、HDAC1措辞1项及SIRT3模型物种/UniProt两项，共257。全部proposal_status=PROPOSED_NOT_APPROVED、applied_to_production=NO。

新字段原schema不存在时old_value_presence=NOT_PRESENT_IN_LEGACY_SCHEMA、old_value_json=null；关联旧字段的语境单存legacy_related_value_json，避免冒称新字段原来已有值。已有字段如evidence_relation_type的old_value_json保存原值。Review_Event同步old/proposed JSON、来源、理由、字段、版本与角色；decision=PENDING、approval_status=PENDING_HUMAN_REVIEW、change_applied=NO、signed_by/signoff_reference为空。review_date是本轮导入/映射事件日期，不伪装成旧Gate2人工审核日期。

## 类型与枚举

CSV按UTF-8/RFC4180文本交换，ID/DOI/PMID原样文本。raw_value保持历史类型；结构化提案proposed_value_json用JSON string/array/null保留类型，proposed_value只作文本显示。JSON null不等于空字符串或0，必须有NOT_REPORTED、UNRESOLVED、NOT_APPLICABLE或NOT_AVAILABLE原因。missing_reason演练行示范原dose缺失，全部66字段原因另在legacy层。未提取显著性时null＋UNRESOLVED，不从效应方向猜p值。

受控枚举取v0.1词表快照：五关系、七靶点、六primary及对应终点/基准/来源/缺失/独立性值。FIELD_RULE_NOT_ENUM和MULTIVALUE_CONSTRAINT是规则文本，不是可填值；secondary从primary词表排除UNRESOLVED和重复primary/重复标签。legacy raw_字段是历史文本，不强制套用新枚举以免改写事实。target_effect_direction提案的NO_STATISTICALLY_SIGNIFICANT_INCREMENT_DETECTED为历史措辞修订，不加入result_direction方向枚举；规范显著性另列NOT_STATISTICALLY_SIGNIFICANT。

技术状态包括NON_PRODUCTION_DRYRUN、PROPOSED_NOT_APPROVED、PENDING_HUMAN_REVIEW、HOLD/PROVISIONAL、PENDING_DESIGN_AND_MATERIAL_REVIEW、PENDING_ARM_EXTRACTION、UNRESOLVED_REUSE；全部有明确范围。APPROVED_SCOPED只用于验证过滤器的内存假设测试，不存在于真实演练提案或来源映射。所有其他技术列可由生成器常量与校验脚本复核，不作为科学分类。

## 来源与三个重点案例

Source_Check.source_scope从legacy的FULL_TEXT_VERIFIED保守映射FULL_TEXT_TEXT_LEGEND、ABSTRACT_ONLY保持；source_issue对6条摘要行用NOT_RECOVERED、amylase对象冲突用CONFLICT，其余在所涉观察范围用NONE_IDENTIFIED_AT_REVIEW。mapping_status全部待审，check_mode=IMPORTED_PRIOR_REVIEW_NOT_NEW_VERIFICATION。历史具体核查日期未在逐行矩阵给出，保持空＋UNRESOLVED；import_date仅本轮日期。source_sha256可能是本地元数据/文本缓存，需结合raw_source_verification_status，不能把它称作已恢复全文的hash。NRF2 M/N冲突独立任务记录，不改6L也不提取M/N值。

Akt/TYR原FUNCTIONAL_CAUSAL留在Observation.raw_evidence_relation_type，PATHWAY_MODULATION在独立提案/事件。HDAC1原NO_ADDITIONAL_CHANGE留在Observation_Target和legacy，未显著增量措辞与显著性分开，不生成零效应量或等效结论。NRF2动物6L仍IN_VIVO；S2仅Unresolved_Mapping中的待提取事项，无观察/实验ID，不链接动物材料，不生成第22条。未来若提取S2，须不同Experiment/Material及新evidence_id。

## 验证视图、恢复与扩展

当前零具名科学签署，三个验证视图都为空。过滤器要求指定版本HUMAN_APPROVED、具名有权事件与签署来源、所涉来源范围适配且无HOLD、非撤稿状态和已批准的特定科学分类；任何PROPOSED_NOT_APPROVED不得生效。结合视图需直接结合支持；抗氧化机制视图需功能参与及已批准红氧机制链，允许直接红氧primary＋功能机制secondary的适配组合。纯计算、单读数或直接红氧测量本身不进入机制验证。正式支持视图也需具名版本审核，无HOLD；用途许可仍另行审批。过滤器是演练接口，不授予实际审批权或正式发布权限。

reconstruct_legacy.mjs从Legacy_Field_Value按原行列序恢复21×66值，输出qc/Rollback_Reconstruction.json；其中还附Input_Snapshot里的原CSV字节，可独立SHA256对照，原行末/引号布局与语义恢复分开验证。该脚本只写本工作区JSON，禁止写回生产路径。生产未动，故无需执行生产回滚；此处验证的是可逆结构和保留的回滚材料。

构建和校验均限制输出在本工作区；build_dryrun.mjs可重建同路径文件，validate_migration.mjs会另在忽略的qc/rebuild_check重建并逐文件hash比较。此演练不作191候选性能/并发/完整迁移验证；双候选内存测试只证明键设计不要求合并，不代替下一批授权和科学审核。
