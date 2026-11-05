# AFF-0061 A组科学评估建议

2026-10-23。9条观察对应5篇论文；不是9项独立研究。依据已批准Governance v0.2及其继承定义，三个维度分别判定，不形成统一强度分数。本轮的矩阵及以下文字均为Codex准备的科学建议，人工状态全部NOT_REVIEWED、change_applied=NO；没有人审姓名、裁决或批准日期。旧66字段记录完整保存在每行original_record_66_fields_json，原target_validation_status不冒充新target_confirmation_class；后两维在旧表不存在，明确记NOT_PRESENT_IN_LEGACY_SCHEMA。历史Gate2建议另列，257项旧提案不应用。

| evidence_id | evidence_relation_type建议 | target_confirmation_class建议 | antioxidant_relevance_primary建议 |
| --- | --- | --- | --- |
| ME-AFF0061-37482908-001 | OMICS_ASSOCIATION | OMICS_ASSOCIATED | OTHER_BIOLOGICAL_FUNCTION |
| ME-AFF0061-37482908-002 | PATHWAY_MODULATION | READOUT_ONLY | OTHER_BIOLOGICAL_FUNCTION |
| ME-AFF0061-39589556-002 | OMICS_ASSOCIATION | NOT_APPLICABLE_NO_PROTEIN_TARGET | INDIRECT_OXIDATIVE_STRESS_ASSOCIATION |
| ME-AFF0061-41594941-001 | PATHWAY_MODULATION | READOUT_ONLY | OTHER_BIOLOGICAL_FUNCTION |
| ME-AFF0061-41594941-002 | PATHWAY_MODULATION | READOUT_ONLY | OTHER_BIOLOGICAL_FUNCTION |
| ME-AFF0061-41594941-003 | PATHWAY_MODULATION | READOUT_ONLY | OTHER_BIOLOGICAL_FUNCTION |
| ME-AFF0061-41594941-004 | COMPUTATIONAL_PREDICTION | COMPUTATIONAL_ONLY | OTHER_BIOLOGICAL_FUNCTION |
| ME-AFF0061-42170612-002 | COMPUTATIONAL_PREDICTION | COMPUTATIONAL_ONLY | OTHER_BIOLOGICAL_FUNCTION |
| ME-AFF0061-37025617-001 | PATHWAY_MODULATION | READOUT_ONLY | INDIRECT_OXIDATIVE_STRESS_ASSOCIATION |

分类组合与历史Gate2建议相同，不意味着重复认可；本轮新增实际原图阅读、补表5信息、字段级原/建议值和更具体的未决项。没有一行满足本行直接结合证据，也没有将本行磷酸化/富集变成直接redox结果；原始关系类型均建议保留。是否采纳建议须由研究者针对精确版本逐条裁决。

## 两条Kmo转录观察

ME-AFF0061-37482908-001的实际支持为ISO小鼠心室RNA-seq候选Kmo下调；Fig4A/C只展示全局谱，Kmo特异FC和校正p尚未恢复。平台、比较及DRA014580指针可追溯，可暂提OMICS_ASSOCIATED并明确统计缺口；若将来用于正式分析，应先核实样本单位、基因级结果和多重校正。不能将DRA014580存在写成已重分析，不能借同文siRNA或Fig8 DHE把本行升级功能依赖或直接抗氧化。

ME-AFF0061-37482908-002的实际支持是Fig5D Kmo mRNA/Gapdh下降，2^(-ΔΔCt)与小鼠引物可核，未测本行Kmo蛋白或酶活。PATHWAY_MODULATION在批准词表中可承载转录响应，必须保留TRANSCRIPT读数标签，READOUT_ONLY不等于蛋白结合。无ISO时的NS须保留，不能推断等效或挑战×PCA交互显著。两条观察是同文发现—验证链，不把qPCR叫第二项独立研究；RNA-seq与qPCR是否同一动物样本仍需确认。

两行OTHER_BIOLOGICAL_FUNCTION遵循单行终点不借用其他观察的规则。研究者若认为Kmo与同文已定位红氧链足以支持间接关联，应说明精确关联观察和条件后另行裁决，不能因Kmo名称或全文主题自动改标签。本轮不新增Fig8正式观察。

## 基因集富集

ME-AFF0061-39589556-002是未加脂毒挑战的MHCC97-H细胞5µM PCA/16h与未处理比较。Fig2D和补充Table5已恢复部分术语ID、背景计数和作者Log(q-value)，纠正旧“这些信息全部缺失”的笼统表述。补表GO:0070482、GO:0006979、GO:2000377与R-HSA-211859指向多个集合；GO/Reactome/WikiPathways不能统称同一数据库。1644命中基因相对1800个差异基因的映射过程、测序重复、版本及背景选择理由仍需确认。

建议保留OMICS_ASSOCIATION、无蛋白对象及间接氧化应激关联，不赋予“NRF2直接靶点”“NRF2激活方向”或“已抑制ROS”。研究者需决定未来用关联集合表或拆行表达多个词表；本轮只给字段修改建议，不执行Schema迁移或新增第22条观察。

## 三条HUVEC响应

ME-AFF0061-41594941-001保留HDAC1丰度下降；ME-AFF0061-41594941-002保留GATA4丰度上升。两行均针对AngII后PCA100µM/24h，Fig4I/J分别以GAPDH作比值，n=3的实验单位未核。GATA4其他剂量未全部标显著，不能概括为各浓度均有效。抗炎表达变化不等于HDAC1抑制剂直接结合，也不能把CoIP的蛋白–蛋白互作当作小分子结合。

ME-AFF0061-41594941-003保留RELA/p65定位响应。Fig4E和正文支持作者报告PCA减弱核转位，DAPI作核参照；未恢复专门的核/胞质比例和相应显著性，建议明确为定性/半定量来源不足的定位观察，而不是“已定量证明转位”。三条均为PATHWAY_MODULATION/READOUT_ONLY/OTHER_BIOLOGICAL_FUNCTION，不移用同文其他ROS或siRNA终点。

需要研究者共同裁决的报告问题：Methods2.8的6组/5组差异、未明确匹配的vehicle、细胞批次与n=3含义，以及未取得的补充原始blot。Fig4B的500µM细胞毒性必须保留为剂量边界；它既不证明100µM有毒，也不构成广义安全保证。同一Fig4I/J共享的样本和GAPDH不支持两项独立研究计数；p65 IF是否另批样本未确认。

## 两条计算观察

ME-AFF0061-41594941-004支持HDAC1 docking/MD预测，不能支持直接结合。Fig6显示0–100ns，建议将模拟时长从旧NOT_APPLICABLE改为明确模拟语义，但不实施原表修改。正文MM-PBSA -12.21kJ/mol与图6G kcal/mol存在单位冲突，定量亲和/跨研究能量比较暂不可用；不能选择一个单位自动换算。PDB ID、物种/构建体、配体/金属参数及apo/重复轨迹尚未恢复。建议保留计算观察及未决标志，研究者决定是否在定量比较前要求作者澄清；不因缺参数把它伪装为实验或删除真实预测。

ME-AFF0061-42170612-002支持hTAS2R16单复合物100ns轨迹及残基接触，Desmond/OPLS4/SPCE可定位。Fig6A配体中途明显偏移、作者称70ns后相对稳定，尚不能证明充分收敛、亲和常数、受体激活或人涩感因果。具体结构模板、版本和膜模型仍需补。Table4模型筛选与amylase实验不是该受体的功能/结合验证；本轮不处理C组amylase制剂冲突。两条计算均COMPUTATIONAL_PREDICTION/COMPUTATIONAL_ONLY/OTHER_BIOLOGICAL_FUNCTION，不因抗氧化数据库主题强行贴抗氧化标签。

## p-eNOS响应

ME-AFF0061-37025617-001支持mBMEC在IL-1β0.5ng/mL背景、PCA100nM overnight后p-eNOS/eNOS相对IL-1β单独组恢复。精确小时未报，不填24h，也不把共孵育改成预处理。Fig4B比例轴与Fig4D总蛋白条带可核，图注n=6–7，1/10nM未标显著不是无效或等效。总图注“relative to GAPDH”未把精确计算算法说清，建议研究者先核densitometry，不能再除一次GAPDH或抹去原图注。

建议PATHWAY_MODULATION/READOUT_ONLY及INDIRECT_OXIDATIVE_STRESS_ASSOCIATION：本行是NO相关信号响应与氧化/炎症语境，而非ROS实测或PCA–eNOS物理结合。Fig3 DHE、Akt阻断实验不转移为本行结果；标题“directly”指直接孵育，不代表直接蛋白结合，“physiological”也不是本项目已确认的游离人体暴露。研究者需裁决间接关联标签是否充分及归一化算法；本轮不审核B组Akt阻断行。

## 下一轮裁决入口

优先明确三项：HDAC1能量单位及结构身份、p-eNOS归一化公式、两组RNA-seq的统计/样本单位。随后逐条确认定位定量、剂量边界和独立性。矩阵中human_reviewer_name、human_decision、human_approval_date留空供后续具名审核；不得把Codex或ChatGPT写成代签人。Gate1=HOLD、Gate2=HUMAN_SCIENTIFIC_REVIEW_REQUIRED、Scale-up/生产迁移未授权、Release=HOLD均不变。准备完成即停止，不自动开始B/C组或扩展检索。
