# 迁移影响评估 v0.1

2026-10-21。ASSESSMENT_ONLY。未迁移原21条、66字段字典、Master或191覆盖索引。影响是未来实施所需工作，不是自动修订指令。旧Gate2提案的17 MUST_CHANGE、21 RECOMMENDED、28 OPTIONAL_FUTURE是修改优先级，不是新增列数或可删除字段数；本评估保留该17项重点语义调整，并补充所有字段的目标归属。

## 原21条：覆盖不等于批准

逐行Gate2矩阵保持原状：12 KEEP_PROVISIONAL、2 RECLASSIFICATION_PROPOSED、7 HOLD_SOURCE_VERIFICATION。人工批准为0。七条来源HOLD为amylase一条、TRAF2两条、SIRT1一条、TYR一条、旧GSH两条。靶点类别提案为2功能参与、6读数、1组学、3计算、6未决、3无蛋白；直接结合支持0。红氧primary提案为1直接终点、3间接关联、14其他功能、3促氧化/不利。以上是Gate2历史提案口径，不是本轮新批准分布。

| evidence_id后缀（均前缀ME-AFF0061-） | 潜在实施影响 | 仍须人审/补证 |
|---|---|---|
| 32520409-001 | 情境性Sirt3功能参与，脂肪变仍为其他功能 | 给药途径、全身KO基线与交互；无本行动物补回 |
| 32520409-002 | 计算类别保持；可提案补人源Q9NTG7模型信息 | 原值保留，映射与计算支持分开 |
| 37482908-001 | Kmo组学关联，TRANSCRIPT/组学层级 | 差异结果/校正与样本单位 |
| 37482908-002 | Kmo qPCR READOUT_ONLY而非蛋白测量 | RNA-seq/qPCR实际材料是否共享未定 |
| 39589556-001 | 6L直接红氧primary加功能机制secondary，功能参与不等于结合 | 动物交互与图像量化；S2细胞补回不移植 |
| 39589556-002 | 无具体蛋白，富集仅间接红氧 | 基因集ID/背景/校正；不从富集推激活 |
| 41594941-001 | HDAC1表达/定位读数，其他功能 | 与002/003共享设计/材料待核 |
| 41594941-002 | GATA4读数，其他功能 | 蛋白表达不构成直接靶点 |
| 41594941-003 | RELA定位读数，其他功能 | 不因炎症背景标为已验证抗氧化机制 |
| 41594941-004 | HDAC1计算保持，CoIP不借作小分子结合 | 模型构建物来源及参数 |
| 41594941-005 | 原NO_ADDITIONAL_CHANGE需拆为方向与显著性；拟记录未检出显著增量 | 具体比较/效应量/区间；不是零效应或必要性 |
| 42170612-001 | dose_unit与dose_basis拆分，12mmol/L为注射器；靶点未决并HOLD | 方法/Table3/Figure2B对象冲突、物种亚型与货号 |
| 42170612-002 | TAS2R16计算保持；100ns只为模拟时长 | 不作抗氧化机制或受体功能验证 |
| 37025617-001 | p-eNOS读数及间接红氧，100nM最终暴露需按方法定位 | overnight不补小时，不借其他DHE行 |
| 37025617-002 | 拟FUNCTIONAL_CAUSAL→PATHWAY_MODULATION，保留单药理子标签 | Akt亚型不定，正交干预/特异性待核 |
| 42413844-001 | 结合作者报告保留，未决并HOLD | 原始全文、构建物、量热类型、剂量和控制 |
| 42413844-002 | 依赖为摘要报告，HOLD | 不将未见干预写为已做KO/救援 |
| 32007785-001 | SIRT1关联与炎症结局仍HOLD | BV2/PC12模型不可合并，剂量时长对照缺失 |
| 11023549-001 | 拟FUNCTIONAL_CAUSAL→PATHWAY_MODULATION；促氧化primary/红氧secondary | 来源先HOLD，arbutin选择性剂量对照待查 |
| 11714376-001 | 无蛋白对象，500mg/kg腹腔与真实GSH结局分层 | 全文、检测、对照和时间未核 |
| 11714376-002 | 无蛋白对象，0.1%饮水60日不换假定mg/kg/day | 百分比基准、摄入量与全文对照 |

两条关系收窄提案与“两条RECLASSIFICATION_PROPOSED总体状态”不是同一口径：TYR总体状态先HOLD，HDAC1-005是方向修订而非关系改类。SIRT3模型身份提案也不能计作新的实验靶点。治理优先级与行审核状态分别报告。

## 66字段逐项归属与调整

M=沿用Gate2的17个扩展前必须修订定义/类型/枚举重点；R=其余字段保留并规范映射或来源，仍受相应Gate约束，不表示可删除或不重要。原字段全部保留于legacy原始层，未来导出兼容视图不要求继续将每个字段都物理复制到Observation。

| 序号 | 原字段 | 优先 | 未来规则/归属 |
|---|---|---|---|
| 1 | candidate_id | R | Compound只读FK，稳定不重排 |
| 2 | compound_name | R | 展示名，不作实体合并键 |
| 3 | compound_form | M | 参考母体与实验形式分开，扩展合法形式须审议 |
| 4 | PubChem_CID | M | 参考锚，不当实验试剂鉴定；实验形式映射单独审 |
| 5 | InChIKey | M | 完整参考结构键，不按前14位合并 |
| 6 | study_id | R | 旧按出版物分配，映射Publication，不称独立研究 |
| 7 | article_title | R | Publication事实，保留原文 |
| 8 | DOI | R | Publication标识，文章自身提取，文本规范化可追溯 |
| 9 | PMID | R | Publication文本标识，不转数值科学记数 |
| 10 | journal | R | Publication来源事实 |
| 11 | publication_date | R | 原始精度保留，电子/卷期各事件 |
| 12 | publication_date_type | R | 分日期事件，不以最新日期覆盖历史 |
| 13 | article_url | R | 来源入口，不等于全文开放 |
| 14 | target_gene | R | Target/桥，物种特异，不由家族推单基因 |
| 15 | target_protein | R | 原作者名与标准对象分开 |
| 16 | UniProt_ID | R | 映射事实与实验确认分开 |
| 17 | target_species | R | 蛋白来源物种，不由表达宿主猜 |
| 18 | target_role | M | 角色与支持/来源拆开，兼容旧值不自动升级 |
| 19 | target_effect_direction | R | 方向、依赖、结合和显著性拆开，原词永久保留 |
| 20 | pathway_name | R | 作者轴保留，标准映射另列 |
| 21 | pathway_ID | R | 标准ID经核查，不造KEGG/Reactome编号 |
| 22 | pathway_database | R | 与ID和版本匹配，作者轴不冒充本体 |
| 23 | pathway_effect_direction | R | 富集方向不自动激活；统计另列 |
| 24 | experimental_model | R | 扩展离体/人观察等合法模型，受控审核 |
| 25 | species | R | 模型物种，材料多物种分列 |
| 26 | cell_line_or_tissue | R | Material含组织细胞基因型，不混计算模板 |
| 27 | dose | M | 原文本保留，规范数值空值配原因，不猜换算 |
| 28 | dose_unit | M | 单位与新dose_basis分开，频率维度明确 |
| 29 | treatment_duration | R | 原文及时间锚分开，计算时长不作给药 |
| 30 | assay_method | R | 方法事实与支持强度分开 |
| 31 | control_group | R | 比较臂/参考臂桥，保留完整析因设计 |
| 32 | evidence_id | R | 永久观察ID，拆分派生但不重用 |
| 33 | evidence_relation_type | M | 五类保持名义，收窄因果定义须逐行人审 |
| 34 | target_validation_status | M | 支持设计标签，避免混来源和结论；新增确认维度 |
| 35 | functional_outcome | M | 真实结局，红氧相关性与方向独立，不隐藏阴性 |
| 36 | effect_context | M | 模型剂量时间及解释边界，不能承载隐藏评分 |
| 37 | source_figure_or_table | R | Source_Check对应面板，不猜摘要图号 |
| 38 | source_verification_status | M | legacy保留，scope与issue分开，全文文本不等于原图审核 |
| 39 | evidence_status | R | 旧纳入状态映射review_state提案需人工决定 |
| 40 | notes | R | 仅补充，不用自然语言暗示审批 |
| 41 | PMCID | R | 可空公共标识，不等于全文已读 |
| 42 | publication_date_precision | M | 至少YEAR/MONTH/DAY，不补造日月 |
| 43 | compound_form_as_reported | R | 原作者形式不覆盖 |
| 44 | identity_mapping_status | R | 参考匹配与实验鉴定/人工审核分列 |
| 45 | identity_reference_url | R | 参考结构来源与查询日期 |
| 46 | experiment_id | M | 重建设计关联前保留legacy映射，不按观察数计独立 |
| 47 | observation_endpoint | R | 复用此字段，加测量层级/统计旁表，不加同义列 |
| 48 | administration_route | R | 途径受控，oral未知方式不猜 |
| 49 | pretreatment_duration | R | 与正式处理和挑战分时序 |
| 50 | challenge_agent | R | 应激因素，KO/药理另列perturbation角色 |
| 51 | challenge_dose | R | 不代替PCA剂量，多因素独立Intervention |
| 52 | challenge_duration | R | 挑战时序和时间锚 |
| 53 | target_experimental_support | M | 拆来源scope与支持design，不作为统一分数 |
| 54 | direct_target_status | M | 保留旧状态，未来派生视图不与确认维度双写冲突 |
| 55 | target_identifier_status | R | 映射状态非实验验证 |
| 56 | target_identifier_source | R | 来源版本时间与唯一性 |
| 57 | source_local_path | R | Source_Check相对路径及许可/hash，不默认上传全文 |
| 58 | source_locator | R | 逐结论方法结果图表精确定位 |
| 59 | source_result_paraphrase_CN | R | 原读释义保留，不冒充原文逐字引语 |
| 60 | source_review_mode | R | 归Source_Check范围，不暗示全图审计 |
| 61 | search_source_ids | R | 对应搜索日志，非独立研究计数 |
| 62 | extraction_date | R | 提取事件日期，不覆盖复核/批准日期 |
| 63 | extracted_by | R | 执行者角色，不写成人工审稿者 |
| 64 | human_review_status | M | 六状态及具名事件，不自动从NOT_REVIEWED升级 |
| 65 | publication_status | M | 撤稿/更正/关注声明及检查日期，历史不删除 |
| 66 | experiment_independence_status | R | 关联真实设计/材料与跨文复用，不从DOI推独立 |

必须新增的三个语义维度是target_confirmation_class、antioxidant_relevance_primary、dose_basis；secondary为可空受控桥。不是要求只加三列即可完成治理：Review_Event、Experiment/Material关联、来源scope/issue、endpoint测量层级与方向/统计拆分也是必须的逻辑结构，可按B方案旁表实现。旧direct_target_status等兼容导出应由统一批准事实派生，禁止与新类别手动双写成为两套真相。

## 191候选覆盖与风险

覆盖索引仍191行，AFF-0061仅SEARCHED/PARTIAL，其余190 NOT_SEARCHED且计数留空，不能改成0证据。新规则不会自动消除AFF-0082/AFF-0150结构缺失，不关闭Phase1B 14项风险或临时crosswalk问题；候选层身份许可不等于每篇实验试剂已核。未来扩展要指定批次清单，不能因有191行索引就生成191个已审状态。

最高迁移风险为：合并实验导致不实独立性、规范单位抹掉基准、将legacy审核状态映射为批准、将计算模板身份误用到实验材料、宽表多对多展开造成重复计数。回滚要求为原CSV/字典及既有冻结资产只读留存、每新行与legacy一对一或派生映射、逐字段差异和批准事件、版本manifest与确定性导出。未来应先对原21条做副本dry-run，核对ID集合不变、原始字段可恢复、状态无越权、HOLD过滤和旧宽表对账，再申请生产迁移；本轮不生成迁移后的21行或重新计算任何排名。
