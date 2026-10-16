# Results Draft v0.1 CN
DRAFT | 2026-10-16 | Baseline 24653d04f4b96849bdcc57039aecfb3cda99da4f
状态标签区分已完成方法、已观察结果、已批准未实施规则、计划分析和未核实细节。

## 1 数据库构成

全类别背景库包含九个面板的191条记录，当前水相总体包括七个面板的157种候选物，分别为59种黄酮、29种酚酸或结合物、15种芪类或木脂素、2种维生素或类似物、15种有机硫、11种甜菜色素或含氮物质，以及26种其他植物化学物。上述计数描述数据库范围，不表示效力。[OBSERVED_RESULT]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Antioxidant_Class_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv)

## 2 文献覆盖

来源表包含45,643条候选物与论文记录，其中41,967条计入元数据主指标。同一论文关联多个候选物时可贡献多行，因此总数不是唯一论文数或独立实验研究数。后续H-ORAC筛选表包含3,115行，其中1,641行待全文裁决。暂定Top50与47种候选检索框架仍为不同成果。[OBSERVED_RESULT]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Publication_Screening.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/shortlist/Literature_Screening_Provisional_Top50.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv)

## 3 实验性证据可用性

canonical H-ORAC表包含74条实验记录，分层为A七条、B1六十一条、B2四条和X两条。A加B1主集合共68条记录，构成28种候选物的既有定量排序。该排序反映此前裁决的rubric，不能描述为28种候选均满足VSIR v1.0。[OBSERVED_RESULT]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv)

## 4 来源核查

6D来源审计将16个既有DOI中的8个标为已核实原始实验，另8个保持未解决。Hayes 2011提供鞣花酸原始结果151.77±3.57 g Trolox/100 g干样品，原表注释说明为三次测定及SD。该结果补齐来源和精度描述，但不为该候选新增第二项独立研究。这些属于继承的来源审计结果，并非本轮制作重新裁决全部全文。[OBSERVED_RESULT]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv)

## 5 统计信息完整性

68条A加B1记录中，27条具有数值误差，其中4条可明确为SD，23条误差类型尚未解决，41条没有恢复数值误差。全部68条误差审计行仍为CI_NOT_ESTIMABLE；canonical表中70/74条仍标PENDING_SECOND_REVIEW。上述完整性结果不支持把记录中位数解释为按精度加权的合并效应或Top20入选概率。[OBSERVED_RESULT]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv)

## 6 独立研究覆盖

28种候选的6D审计中，PASS_VERIFIED、UNRESOLVED与FAIL_ON_AVAILABLE_EVIDENCE分别为9、10和9项。最后一类表示当前已审计资料不足，不证明不存在其他研究。九项PASS_VERIFIED属于先前局部审计，不是VSIR GO结果。已批准VSIR条件的完整实施及12项边界测试仍未完成。[OBSERVED_RESULT；VSIR为APPROVED_NOT_IMPLEMENTED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Candidate_Eligibility.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv)

## 7 冻结H ORAC排名

既有Frozen Top20 v1.0首位为迷迭香酸，末位为阿魏酸。本轮独立复算重现28个canonical A加B1中位数和冻结Top20顺序。将B2纳入敏感性分析后，相对主Top20仍为三进三出。冻结成果继续表示已裁决证据范围内、按既定资格定义的体外化学容量；本轮不更新为v1.1。[OBSERVED_RESULT]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv)

## 8 综合框架准备度

阶段性框架包括五个维度、26项二级指标、三个应用场景及785条候选物维度覆盖记录。D1在既有H-ORAC范围中包含8项AVAILABLE_VERIFIED和20项AVAILABLE_UNVERIFIED，另127项NOT_SEARCHED、2项IDENTITY_UNRESOLVED。D2有28项未核实条目，没有维度级完全核实条目；D3仍基于元数据，D4缺少结局裁决，D5尚未开展应用可行性评价。本轮未计算综合分数或综合Top20。[OBSERVED_RESULT；进一步综合为PLANNED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Candidate_157_Data_Availability_Matrix.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Application_Scenario_Applicability_Matrix.csv)

## 9 当前证据缺口

剩余工作包括原始来源闭环、误差定义与重复单位识别、独立第二复核、VSIR实施和边界测试、CR最终裁决衔接，以及生物学和应用场景证据评价。维生素C仍需恢复Ou 2001原表。Platzer 2022包含原始纯标准品AAPH-fluorescein AUC实验，但缺少可重建Trolox当量换算，不能直接进入主汇聚。证据缺失保留为缺失，不解释为没有活性。[OBSERVED_RESULT；缺少来源闭环处为UNVERIFIED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Proposed_Change_Requests.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/stage25b6d/Stage25B6D_VitaminC_Reconciliation_CN.md); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/stage25b6d/Stage25B6D_Ranking_Readiness_CN.md)
