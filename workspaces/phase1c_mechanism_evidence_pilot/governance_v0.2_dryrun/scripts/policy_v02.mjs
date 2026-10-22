export const accepted=new Set([1,4,5,6,7,9,10,12,14,15,16,17,18,20,24].map(n=>'GOV-'+String(n).padStart(2,'0')));
export const policies={
 'GOV-02':{rule:'采用方法适配控制及风险触发正交验证，不机械要求所有研究两种方法；核蛋白身份、实际形式、背景干扰、浓度、结果和对照；聚集/荧光/非特异或制备物冲突不得直接升级。',review:'接受风险触发策略；不设统一双方法门槛。',pre:'原方法与对应结果可核；风险项补证和具名签署。'},
 'GOV-03':{rule:'允许情境性遗传依赖支持功能参与；不强制每行救援；须核基线、对象干预、比较、终点、时序；不得以一组显著另一组不显著替代正式交互检验。',review:'保留情境性支持与交互边界；不机械否定无救援观察。',pre:'逐模型审查及具名签署；不能借他模型补回。'},
 'GOV-08':{rule:'六类primary及受控secondary保持；先按模型剂量时间终点拆观察；促氧化或不利优先仅展示政策，不代表强度或自动临床危害。',review:'保护和不利结果均保留，标签不作单轴评分。',pre:'逐观察终点与范围可追溯；展示政策正式签署。'},
 'GOV-11':{rule:'采用方案B主观察表加少量关联表，核心Publication/Experiment/Observation/Review_Event，按实际重复结构增设实体或桥，不用不可核自由文本塞多对多。',review:'采用方案B并授权隔离副本演练，不是生产迁移。',pre:'无孤立FK、原值可恢复、未决映射显式及维护责任签署。'},
 'GOV-13':{rule:'不同DOI不代表独立实验，同文不同检测不代表独立样本；材料共享需来源，不确定用UNRESOLVED_REUSE，不擅自合并或重复计数。',review:'保留所有旧experiment_id，但不宣称其相互独立。',pre:'正式分析前核样本复用、独立性与分析单位并签署。'},
 'GOV-19':{rule:'正式科学批准必须由项目指定具名审核者签署；ChatGPT和Codex建议或技术检查不能代签；未指定时保持待签署。',review:'本轮无指定具名审核人，不生成正式批准。',pre:'项目指定实名审核者、权限、版本和签署范围。'},
 'GOV-21':{rule:'技术QC为Gate1必要非充分条件，仍需规则版本、迁移核对、保护资产及具名验收；隔离演练通过不使正式Gate1通过。',review:'分开记录演练技术结果和正式Gate1。',pre:'规则获批、受控迁移及具名验收。'},
 'GOV-22':{rule:'允许指定已审版本子集通过Gate2；HOLD从已验证靶点、已验证抗氧化机制及正式支持计数隔离；12暂保留不得自动人工批准。',review:'保留HOLD登记，不将KEEP_PROVISIONAL升级。',pre:'逐行具名签署、子集范围、版本及HOLD过滤验收。'},
 'GOV-23':{rule:'暂定收集、已审主表纳入、正式分析排名、正式发布四权限独立；未来可申请有限批次，当前全部未授权。',review:'不因本轮演练自动扩展或启动分析。',pre:'每项用途批次范围和版本分别授权。'}
};
export const prereq='规则及作用范围由具名项目审核者正式签署；本轮仅记录建议与隔离演练，不改变生产状态。';
// Endpoint mappings are explicitly proposals, based on legacy extraction + Gate2, not a new scientific approval.
export const endpointMapping={
 '32520409-001':['NOT_REDOX_MEASUREMENT','PHENOTYPE'],
 '32520409-002':['NOT_REDOX_MEASUREMENT','COMPUTATIONAL_OUTPUT'],
 '37482908-001':['NOT_REDOX_MEASUREMENT','TRANSCRIPT'],
 '37482908-002':['NOT_REDOX_MEASUREMENT','TRANSCRIPT'],
 '39589556-001':['REDOX_PROBE_SIGNAL','PHENOTYPE'],
 '39589556-002':['NOT_REDOX_MEASUREMENT','GENE_SET_ENRICHMENT'],
 '41594941-001':['NOT_REDOX_MEASUREMENT','PROTEIN_ABUNDANCE'],
 '41594941-002':['NOT_REDOX_MEASUREMENT','PROTEIN_ABUNDANCE'],
 '41594941-003':['NOT_REDOX_MEASUREMENT','LOCALIZATION'],
 '41594941-004':['NOT_REDOX_MEASUREMENT','COMPUTATIONAL_OUTPUT'],
 '41594941-005':['NOT_REDOX_MEASUREMENT','PROTEIN_ABUNDANCE'],
 '42170612-001':['NOT_REDOX_MEASUREMENT','BINDING'],
 '42170612-002':['NOT_REDOX_MEASUREMENT','COMPUTATIONAL_OUTPUT'],
 '37025617-001':['NOT_REDOX_MEASUREMENT','PROTEIN_MODIFICATION'],
 '37025617-002':['NOT_REDOX_MEASUREMENT','PROTEIN_MODIFICATION'],
 '42413844-001':['NOT_REDOX_MEASUREMENT','BINDING'],
 '42413844-002':['NOT_REDOX_MEASUREMENT','PHENOTYPE'],
 '32007785-001':['NOT_REDOX_MEASUREMENT','PHENOTYPE'],
 '11023549-001':['REDOX_ANALYTE','METABOLITE'],
 '11714376-001':['REDOX_ANALYTE','METABOLITE'],
 '11714376-002':['REDOX_ANALYTE','METABOLITE']
};
