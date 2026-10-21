# Phase 1C 机制证据数据库治理规则 v0.1

日期：2026-10-21（Asia/Shanghai）。状态：FINALIZED_FOR_HUMAN_REVIEW；所有规则 HUMAN_DECISION_REQUIRED，change_applied=NO。这里的“定稿”指提交审议的规则文本完成，不是规则生效、证据批准或数据库正式发布。基线 main/d29a6936603886e654b3cdfb24ccd3a1e76cee23；任务分支 codex/phase1c-governance-v0.1。

## 推荐决定与适用范围

推荐方案 B：主观察表加少量关联表。保留一行“候选物 × 具体关系 × 单项观察”的科学粒度，增加独立 target_confirmation_class、antioxidant_relevance_primary 及受控 secondary 关联。这些都是名义类别，不转成单轴分数。当前规模191个候选物并不要求立即建设完整关系数据库；Excel/CSV仍可维护，关联键与版本约束为将来迁移保留接口。本轮仅在 governance_v0.1 新增文件，不执行映射写回、正式迁移、检索扩展或算法分析。

决策矩阵含24项人工决策：15项建议优先批准原则，9项需继续讨论实施阈值与责任。两组当前都未批准。优先原则为 GOV-01、04–07、09–10、12、14–18、20、24；讨论项为 GOV-02、03、08、11、13、19、21–23。讨论项并不暂停“禁止过度推断”的现有边界；其待决内容是项目正式政策，不是对文献结果重新投票。

## 观察关系：五类保持，按本行支持判定

DIRECT_BINDING 记录本行小分子与蛋白的实验结合关系或明确标注的作者结合报告，不因类别名成为已确认靶点。FUNCTIONAL_CAUSAL 限于明确对象干预与结局比较支持的情境性依赖；不能由某组显著而另一组不显著直接推出交互显著。PATHWAY_MODULATION 包括表达、磷酸化、定位、活动或通路响应，亦是本版无特定蛋白红氧响应的兼容容器，必须用 target_role/endpoint 澄清其不是命名通路已验证。OMICS_ASSOCIATION 表示高通量统计关联及富集；COMPUTATIONAL_PREDICTION 表示计算预测。

同一行只放一个主要关系；不同检测、材料、剂量、时间点或主要比较产生不同观察，用关联键联结，不择优保留。若原文仅声称因果而关键设计未见，保留 author_claim 原文释义和来源层级，行状态 HOLD；不以分类重命名抹掉来源限制。历史原值保留，建议值须经逐行审核后另行实施。

## 独立靶点确认：七类的操作规则

共同前提：类别按单项观察判断，不能借用同论文其他行或同名蛋白的外部实验升级。target_species 是所研究蛋白来源物种，不是表达宿主；计算结构物种、细胞物种、重组材料身份分开。家族名不能强制映射一个基因/UniProt。一个实验支持结合，不自动支持细胞内靶点占有、选择性、功能介导或人体疗效。升级不是修改数字等级，而是新增足够来源与审核事件后更改名义类别。

DIRECT_BINDING_SUPPORTED：具体蛋白的来源物种、亚型/构建物及实际化合物形式可定位，原始方法、相关结果和图表可追溯，有适合该方法的背景/阴性控制、浓度及拟合或结构判读。ITC需区分稀释热、缓冲不匹配及模型；荧光需审查内滤、淬灭和自发荧光；其他方法同样审查非特异/聚集。不是要求每种方法都有 Kd；结构结合也不臆造亲和常数。候选项目政策建议至少有可靠结合测量与方法适配控制；有明显干扰风险时，正交结合或竞争/位点验证为升级前必要补证。是否对所有结合记录统一强制第二种方法为 GOV-02 待决。Co-IP 的蛋白–蛋白关系、热稳定性变化、对接或单纯活性变化均不单独满足。只有摘要、制备物冲突或身份未明时用 UNRESOLVED_PROTEIN_OR_EVIDENCE 并 HOLD。amylase Figure2B/Table3冲突正属此边界；恢复实验对象与控制后才可重审，不因PDB模板人源而升级。

FUNCTIONAL_PARTICIPATION_SUPPORTED：已定位的基因/蛋白在明确模型内具有可溯源的丧失功能、互补/补回或充分正交干预支持，至少能核对处理、对照、结局、对象与时序。遗传缺失须审查基线、发育代偿、细胞活性及干预效率；补回须核对同一背景、空载体/表达恢复、剂量、时间及对应结局。不同动物与细胞、不同终点之间不得搬运救援。项目拟允许有边界的遗传依赖进入本类，同时在 validation_design 标注 LOSS_OF_FUNCTION_CONTEXTUAL；精确的交互统计/正交补回要求由 GOV-03 审议。缺相应比较或仅有平行表型、非加和时不满足本类。Sirt3脂肪变与Nrf2动物6L仅支持各自情境参与，不是直接结合；NRF2补充S2细胞补回如未来提取应新建观察。本类升级到结合类别必须另有合格结合观察，不能靠更多敲除实验。

READOUT_ONLY：有可定位对象和实测表达、磷酸化、定位或活动读数；最低要求为方法、比较和读数层级可核查。qPCR 属 TRANSCRIPT 而非 PROTEIN_ABUNDANCE；蛋白变化不是其直接调控或必要性。HDAC1/GATA4表达与平行 siRNA 表型不能成为 PCA–HDAC1结合。来源不足以确认该读数时改未解决并 HOLD；升级功能参与须有对象干预–结局比较，升级结合须独立结合证据。

OMICS_ASSOCIATED：对象来自组学差异或关联，最低要求可追溯检测平台、对比、样本单位与统计方法；校正阈值未报则记录缺失并限制解释，不能声称已通过多重校正。富集不等于激活。仅通路集合没有蛋白对象时用 NOT_APPLICABLE_NO_PROTEIN_TARGET；单独qPCR复核另行记 READOUT_ONLY，不把组学行升级。关键统计/对象无法核实则 UNRESOLVED 并 HOLD。升级功能或结合均需新增相应实验支持。

COMPUTATIONAL_ONLY：本行只有对接、MD或其他计算预测，最低要求能定位方法、模型和输出，尽可能保留结构版本/物种；模型参数缺失记录为缺失，不补造。PDB/UniProt仅对象映射；100 ns轨迹稳定不是实验结合。SIRT3、HDAC1及TAS2R16预测均保持此类。取得湿实验后新增观察而非将旧预测伪装成实验；模型身份严重冲突时先 HOLD/UNRESOLVED。

UNRESOLVED_PROTEIN_OR_EVIDENCE：存在拟研究蛋白，但身份、制备物或核心支持无法确定。最低要求记录具体未决点、可见来源及需要的补证，不强行挑另一个类别。TRAF2摘要报告与amylase对象矛盾保持此类。只有恢复相关原始方法/材料、冲突解释和逐行人工决定后才能改类；“全文已下载”本身不构成升级。

NOT_APPLICABLE_NO_PROTEIN_TARGET：本行无蛋白对象，如GSH代谢物或单纯基因集富集。最低要求明确被测对象；不把GSH写成蛋白、不把通路名称当单基因。不是未知蛋白的占位符，也不因未来发现相关蛋白而改写原测量对象；未来蛋白实验另建观察。来源连对象都不明确时用 UNRESOLVED 而不是不适用。

单一药理抑制剂记录 validation_design=SINGLE_PHARMACOLOGICAL_SUPPORT。即便响应受阻，也默认不足以断言特定蛋白必要性；审查选择性、实际靶点作用、毒性与正交干预。原Akt、TYR关系收窄仍为逐行提案，不在本轮应用。多种抑制剂也不是自动充分条件，需排除共享脱靶并明确对象。基因补回支持特定背景的功能解释，不证明小分子物理结合。

## 抗氧化相关性：独立判定与冲突处理

一个 primary，零至多个不重复 secondary，secondary 使用同一六类词表且不得包含 UNRESOLVED 或 primary 自身；无secondary在关联表为零行，宽表导出为[]。标签必须有本行来源支持，不为增加“抗氧化”标签借用同论文其他实验。判定顺序为：终点/语境不足则 UNRESOLVED；有明确促氧化/不利响应则 PROOXIDANT_OR_ADVERSE_RESPONSE；本行实测红氧终点则 DIRECT_REDOX_OUTCOME；没有直接红氧测量但有可核查的干预–红氧机制链则 ANTIOXIDANT_FUNCTIONAL_MECHANISM；只有相关背景/富集则 INDIRECT_OXIDATIVE_STRESS_ASSOCIATION；其余真实功能为 OTHER_BIOLOGICAL_FUNCTION。机制类不由蛋白名称触发，相关性也不代表靶点强度。

DIRECT_REDOX_OUTCOME涵盖具体ROS/氧化损伤探针、GSH/GSSG等红氧测量和化学抗氧化实验，但探针信号只是其检测层级，不自动等于特定ROS绝对浓度。记录 redox_measurement_level、assay_method、方向及干扰限制。NRF2动物6L可提案 primary=直接红氧、secondary=功能机制；GSH下降可提案 primary=促氧化/不利、secondary=直接红氧。GSH下降的真实测量与其生物学不利解释分开，任何下降不自动等同临床危害。eNOS磷酸化不是ROS实测，SIRT3脂肪变不因蛋白名成为抗氧化机制。化学ORAC不自动外推为细胞/人体功效，更不变更Frozen Top20。

保护与不利结果发生于不同剂量、模型、时间或终点时拆成观察，沿用共享设计/材料关联。若同一不可拆复合终点确有双向结果，primary=PROOXIDANT_OR_ADVERSE_RESPONSE、secondary=相应已支持类别，标记 MIXED 并人工审核，禁止净分抵消。该优先级为项目展示政策 GOV-08，非自然界证据排序。未显著结果按终点类别保留，例如测脂质氧化但无显著差异仍可为 DIRECT_REDOX_OUTCOME；另记 result_significance=NOT_STATISTICALLY_SIGNIFICANT，不设为零或“无作用”。等效需要预设界值、适配设计与相应区间/检验；未检出差异不能升级 EQUIVALENCE_SUPPORTED。

## 条件、剂量与原始值

dose 原始文本、dose_unit原始单位和原source定位均不覆盖。未来规范层用 dose_value（数值或空值）、dose_unit、dose_basis，空值必须配 missing_reason，不能把缺失字符串塞入数值列。每个剂量一条干预臂，不将多个剂量拼为可计算单值。mg/kg是一次体重归一量还是累计量须以来源确认；mg/kg/day是时间归一暴露，不能仅凭时长除算互换。培养液最终浓度、stock和ITC注射器浓度分列；ITC12mmol/L只属SYRINGE_CONCENTRATION。0.1%饮水须先查w/v等基准、摄入与体重，未齐全不得换mg/kg/day；局部nmol不等于mg/kg或浓度。μM/µM等显示可统一为umol/L，必须保存原值、转换因子、形式特异分子量、公式与转换事件；禁止自动推定盐/母体可互换。

treatment_duration保留原文，规范层分数值/单位/事件起止；pretreatment_duration、challenge_duration与检测时间各自关联时间锚，overnight不补小时。100ns MD是模拟时长，不是生物处理时长。administration_route区分口服具体方式、腹腔、局部及体外孵育；oral未说明时不猜灌胃或饲料。experimental_model区分体内、体外、无细胞、计算、离体与人观察，species记录模型物种；多物种共培养按材料实体分列，不填一个混合物种。cell_line_or_tissue保存细胞名、组织与基因型；实验材料和计算模板各自追溯。

challenge_agent是疾病/应激因素；KO、siRNA、药理阻断另列 perturbation，不把基因缺失伪装为化学挑战。control_group需标识真实比较臂及相同背景、vehicle、基线和正对照是否存在；未报不推断。observation_endpoint是实际检测/比较，不以“激活抗氧化通路”替代BODIPY、GSH或p-eNOS。结构化效应量旁表应记录value/unit、n及其单位、生物/技术重复、区间、检验、校正和比较组，不从柱图视觉估值。

通用缺失语义为NOT_REPORTED（已核相关来源而未报）、UNRESOLVED（未获得/未提取/冲突）、NOT_APPLICABLE（不适用）、NOT_AVAILABLE（公共标识不可用），并用 source_issue 区分未获得、未读、未提取和冲突。0仅真实零。主外键不得用缺失哨兵；可空FK必须有原因或用未决Target实体，不能伪造一个具体蛋白。暴露相关性 exposure_relevance 独立记录；缺人PK/摄入形式及游离浓度证据时UNRESOLVED，标题physiological或低nM不足以认定膳食可达。

## 审核权限、版本与来源

独立Review_Event至少含 review_event_id、evidence_id、reviewer_type、reviewer、review_date、review_action、old_value、proposed_value、decision、decision_reason、source_reference、approval_status、change_applied，并增加 field_name、record_version_before/after、source_hash、rule_version、supersedes_event_id。非观察对象事件使用entity_type/entity_id，evidence_id可空且不伪造。每字段更正一事件，批次用change_set_id串联；old/proposed按规范JSON或原始文本记录并声明类型。

NOT_REVIEWED为尚无人审；PROVISIONAL为暂存/可供讨论；HOLD为关键来源/身份或设计阻塞；REVISION_REQUESTED为请求修订；HUMAN_APPROVED为具名有权人对精确版本/范围签署；REJECTED为否决但保留历史。程序仅能报告技术QC，Codex仅能提出科学建议、保留来源与修订请求，二者均不能写HUMAN_APPROVED。项目须由研究负责人指定实名科学审核者和数据维护者（GOV-19）；ChatGPT/Codex角色与Git授权均不能代替人工科学签署。

新条目 NOT_REVIEWED 后可暂存 PROVISIONAL 或进入 HOLD；任一待审状态可由有权人工决定批准/否决/请求修订。HOLD解除须补证并有新事件，不靠日期自动转移；HUMAN_APPROVED版本出现新冲突进入新版本HOLD/REVISION_REQUESTED，旧批准只适用旧快照。REJECTED重开需新的理由/事件，不删除否决记录。技术维护者仅在批准事件存在、旧值/版本吻合、前后QC通过时应用变更；事件通过追加 APPLY_CORRECTION 记录生效，而不是覆盖原提案事件。approval_status区分提案待审、人工批准/否决与不适用，review_action、decision和数据状态分别管理。

原evidence_id永久保留，split产生新ID并用derived_from关联，原行标记SUPERSEDED而非删除或重排。publication_id与experiment_id改进用映射表保留legacy_id；数据库/schema/rule/词表版本分别标记，任何新版本有迁移说明、差异和回滚快照。Git commit只是文件归档。

来源核查拆为scope（摘要、正文文本/图注、原图、补充材料、原始数据）与issue（无已识别问题、未获得、未读、未提取、冲突）。FULL_TEXT_VERIFIED作为历史字段只指正文相关文本/图注已读，不兼容地宣称原图完整性审核。每个核查结论有locator、URL/本地相对路径、检索时间、文件SHA256与许可；全文取得合法不等于允许再分发。来源冲突记录作者主张、各处定位与未决原因，不以多数文本取代作者澄清。publication_status按检查时点追踪更正/关注声明/撤稿及通知关联，未查到标记不是永久无问题；撤稿观察从有效集合隔离，历史不删除。

## Gate与当前建议

正式标准见Gate_Criteria文件。本轮建议Gate1=HOLD、Gate2=HUMAN_SCIENTIFIC_REVIEW_REQUIRED、Scale-up四种权限全部HOLD/NOT_AUTHORIZED、Release=HOLD。允许有HOLD隔离区不等于允许HOLD进入已验证靶点、已验证抗氧化机制、证据支持计数或正式算法/排名。

收集下一批暂定证据、纳入已审主表、分析/排名、正式发布分别授权。可讨论让有限下一批暂定收集不等待全部历史HOLD关闭，但须先批准治理政策与技术schema、明确隔离和批次范围、指定审核人、完成试点可执行演练并获得书面批次授权；此建议不是当前扩展许可。正式分析另需适用问题、独立性、纳排、版本冻结与分析方案审批。发布另需许可、审核覆盖、可复现包和负责人签署；不因治理文档提交自动触发。

## 依据与待审事项

直接依据为试点同步/使用说明、21条原记录、Study_Register（15个登记出版物，其中10篇纳入、5篇排除/暂缓/背景）、66字段字典、Gate2逐行矩阵/来源报告/两份Proposal/12项开放问题及QC、Phase1B 14项风险与冻结说明。Gate2的12/2/7提案状态和所有原值不在本轮重判。AFF-0082/AFF-0150身份缺失、155临时映射/2待审、21项旧字典缺口以及冻结管理边界保持开放。

外部方法依据于2026-10-21只读检索，未检索新候选物。FAIR用于稳定标识、机器可读元数据与来源追溯：[Wilkinson等，Scientific Data 2016](https://www.nature.com/articles/sdata201618)。实验单位和设计报告参考[ARRIVE 2.0现行官方指南](https://arriveguidelines.org/arrive-guidelines)。结合检测的背景、聚集和正交排干扰参考[NIH Assay Guidance Manual](https://www.ncbi.nlm.nih.gov/books/NBK53196/)及其[Aggregation章节](https://www.ncbi.nlm.nih.gov/books/NBK442297/)。这些规范支持记录和核查原则，不替本项目制定数值评分、强制实验套数或科学批准阈值；项目具体政策全部由决策矩阵审议。本轮不重新确认2026-10-19后各论文的动态有效性，后续审核/发布须刷新。
