# 实体与关联设计 v0.1

2026-10-21。DESIGN_ONLY / HUMAN_DECISION_REQUIRED / change_applied=NO。未创建生产表、未赋予实际新实体ID、未合并原experiment_id。

## 方案比较与推荐

| 方案 | 优点 | 主要代价 | 当前结论 |
|---|---|---|---|
| A 单一宽表 | 单文件易看、沿用66字段 | 文献/材料/剂量/审核重复，无法可靠表示多对多，易把检测数算成独立实验数 | 保留作只读导出，不作长期唯一事实源 |
| B 主观察表加少量关联表 | 稳定观察ID、来源与实验共享、CSV可校验、便于未来数据库导入 | 编辑需外键检查与受控生成宽表，须指定维护人 | 推荐，先小表集后按真实重复结构扩展 |
| C 完整关系型数据库 | 外键事务、并发权限和复杂检索较强 | 运维、界面、迁移与培训成本，191候选规模本身不要求立即建设 | 当多人并发/关系复杂度实际需要时再立项 |

推荐B先实现Observation、Publication、Experiment、Review_Event四类事实表，Compound与既有候选索引只读链接，Target/Pathway复用现有经核查映射或小型lookup。Material、Arm/Intervention、Source_Check、Endpoint_Result和多对多桥在出现相应重复数据时必须结构化，不应为“少表”把异质内容塞成分号字符串。阶段表集及可维护性由GOV-11批准；本轮只是逻辑设计，不承诺只有四张物理表就满足所有未来场景。

## 主键、外键与基数

| 实体/桥 | 主键 | 外键及约束 | 含义 |
|---|---|---|---|
| Compound | candidate_id（沿用AFF） | 只读指向T002；形式特异身份另存并审查 | 参考候选身份，不替每篇试剂鉴定 |
| Publication | publication_id | DOI/PMID为可空唯一外部标识；同文章多标识归一，冲突先HOLD | 出版物，不等于独立生物学研究 |
| Study_Unit（可延后物理化） | study_unit_id | 一个Publication可描述多个单元；一个跨文研究单元可有多篇出版物 | 原科学研究/队列单元；现study_id不能自动迁入 |
| Experiment | experiment_id（新逻辑定义） | 可空study_unit_id，明确model/design；独立设计单元 | 一项设计/分配框架，不按终点数生成 |
| Experiment_Publication | experiment_id + publication_id + source_locator | 两端FK有效；多对多 | 同实验跨文报告或一文多实验 |
| Material_Set | material_set_id | experiment_id；parent_material_set_id可空且不得循环 | 样本/动物/培养批次与子集；同设计不保证同一实际样本 |
| Arm | arm_id | experiment_id；material_set_id按材料关联可多对多 | 分组、基因型、vehicle及剂量/时序 |
| Intervention | intervention_id | arm_id；compound或challenge/perturbation角色明确 | 每个成分、剂量与事件时序一行 |
| Observation | evidence_id（原ID不变） | candidate_id、experiment_id、publication_id为必需FK；可选material_set_id/endpoint_result_id | 单一关系与单项检测/比较，指向主出处 |
| Observation_Arm | evidence_id + arm_id + comparison_role | 角色TEST/COMPARATOR/REFERENCE；同实验或明确跨实验比较说明 | 一个比较可用多个臂，不把析因设计塞进一句control |
| Target | target_id | taxon/基因/蛋白accession/构建物的身份层级明确 | 可有未决target实体但不伪造具体基因 |
| Observation_Target | evidence_id + target_id + target_role | 同一观察不得复制计数；必要时target确认在此按对象记录 | 主表单靶点为常见投影，多对象用桥 |
| Pathway | pathway_entity_id | 作者命名轴与标准数据库ID/版本分列 | 作者轴可存在而无标准ID |
| Observation_Pathway | evidence_id + pathway_entity_id + relationship | 多对多；富集与功能响应分开 | 通路关联不自动衍生蛋白边 |
| Source_Check | source_check_id | publication_id + 可空evidence_id；文件hash/locator/日期/scope | 出版物有多个版本/补充附件及逐观察核查 |
| Endpoint_Result | endpoint_result_id | evidence_id或measurement_id；统计比较和n单位可追溯 | 原始读数/效应量与分析结果，缺值不猜 |
| Review_Event | review_event_id | evidence_id或entity_type/entity_id必有其一；版本/字段/来源有效 | 追加、不可覆盖的审核与实施事件 |
| Legacy_ID_Map | legacy_entity + legacy_id + rule_version | proposed_entity_id；status与依据 | 保留原study_id/experiment_id，不重排evidence_id |
| Independence_Link | independence_link_id | 两个experiment/material/publication实体+relation+依据 | 同源、部分重叠、独立或未决，不是简单去重开关 |

逻辑基数：Compound 1→多Observation；Publication 1→多Observation（主出处）；Publication 多↔多Experiment（桥）；Experiment 1→多Material_Set/Arm/Observation；Observation 多↔多Arm/Target/Pathway；Observation 1→多Review_Event。综述或二次来源不能被当作独立原始实验证据重复建行，补充材料作为主论文来源资产而不是新研究。

现Study_Register有15个登记出版物，其中10篇有纳入观察。原study_id实际按出版物分配，未来应映射到Publication，不能把这15项宣称为15个独立实验。EXCLUDE/背景/暂缓条目继续保留及各自状态；没有PMID的未来论文可用内部稳定ID，不能伪造PMID。

## 粒度与独立性规则

同一动物实验的组织学、蛋白和代谢物测量可以共享experiment_id；只有来源证明同批材料，才共享material_set_id。不同检测用不同evidence_id和assay/run信息；技术重复不新造独立动物n。不同基因型、药物剂量与时间属于同一析因设计时归于同experiment的不同Arm或测量时刻，但结局/比较逐观察记录。另一次独立随机化、另一批培养、另一队列或另一个计算方案应单独设计/材料单元；仅图号不同不构成独立实验。

跨论文潜在复用先建立UNRESOLVED_REUSE链接，记录队列名、伦理批件、样本日期、作者声明、重叠图表等线索；相同作者/剂量不是复用的充分证据，不同DOI也不是独立性的证明。SAME_MATERIAL_SET不重复计为独立n，PARTIAL_OVERLAP需分辨重叠部分，UNRESOLVED_REUSE在独立性敏感分析前不得按完全独立输入。跨文ID合并须人工确认映射，不自动删行。正式meta/算法还需预先确定分析单位与聚类规则，不把21观察当21独立研究。

示例均为关系说明而非已证实样本映射：HDAC1/GATA4/RELA三条100umol/L、24h观察（41594941-001/002/003）可能共享设计，但原图/方法须确认是否同一裂解物/批次，未确认不能合并材料；Kmo RNA-seq与qPCR（37482908-001/002）同动物设计不证明相同个体子集。NRF2动物6L与补充S2细胞实验必须不同Experiment/Material，且S2不在原21条中。500mg/kg腹腔与0.1%饮水60日必须不同处理设计/臂，不合成一个剂量反应点。

一项底层测量支持多个不同对象关系时，用measurement_id关联，不能复制测量来扩大样本量；同一行有多个受控secondary标签用Observation_Tag桥，宽表导出用排序去重JSON数组，不以CSV分隔符充当多对多关系。若确实有多个不同终点，则新Observation各自关联同材料；拆分历史行要标记derived_from、原行版本及SUPERSEDED，不复用旧ID赋新语义。

## CSV实施与一致性

未来经批准后用UTF-8、单行表头、RFC4180引号规则；稳定ID/DOI/PMID强制文本导入，避免Excel日期/科学记数自动转换。不得手改只读宽表后反向覆盖事实表。每次导出注明schema/rule/vocabulary/data版本和有效审核范围，宽表行数因多对多展开时标明唯一evidence_id数，统计时先恢复观察单位。

QC应拒绝重复PK、孤立FK、错误版本、循环派生、未审数据进入验证视图及未知枚举；可空FK必须缺失原因明确。日期精度独立，不给仅有年份的出版物补1月1日。合并、拆分与删除策略分别审议，历史不硬删除；重跑导出应确定性一致，发布包文件清单和SHA256可复核。实施脚本需先在隔离副本演练，再经人工授权迁移，不能直接复用旧构建器覆盖母表。

依据：本工作区治理决定GOV-11/12/13/20，既有66字段与21条观察、Study_Register，以及[ARRIVE 2.0](https://arriveguidelines.org/arrive-guidelines)的实验单位报告原则和[FAIR](https://www.nature.com/articles/sdata201618)的标识/追溯原则。实体名称与分阶段方案是本项目建议，不是这些指南要求的固定表结构。
