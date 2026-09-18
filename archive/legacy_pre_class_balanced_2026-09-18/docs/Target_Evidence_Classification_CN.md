# 化合物–靶点证据分类规则

版本 1.0；适用于单一、结构明确化合物与蛋白质之间的关系。分类单位是“化合物形式–蛋白–物种–实验体系–文献”，同一蛋白可在不同记录中具有不同层级。

## T1：直接生化/生物物理结合

要求纯化或定义明确的蛋白体系中获得可归因的直接结合或酶学抑制证据，例如共晶/cryo-EM 密度、SPR、ITC、MST、BLI、平衡透析，或在排除聚集、氧化还原循环、胶体和读数干扰后得到的 Ki/Kd。单独 IC50、结构对接、非特异沉淀或缺乏阴性/竞争对照的天然产物 assay 不自动属于 T1。结构证据须能区分配体身份和结合位点；酶学证据须报告底物条件、机制与可重复性。

## T2：细胞靶点占有/化学蛋白组学

包括经适当对照的 CETSA、TPP、DARTS、ABPP、可竞争亲和捕获和化学蛋白组学。T2 表示在细胞或复杂基质中靶点参与，但并非所有信号都证明直接结合：完整细胞 TPP 可反映代谢物、复合物、翻译后修饰或下游状态。若无裂解液/重组蛋白复核、剂量依赖或竞争证据，应标记 `directness_qualified=ambiguous`，必要时降为 T3。衍生探针还需证明其保留母体活性。

## T3：功能靶点验证

敲低、敲除、过表达、耐药突变或 rescue 显示该蛋白对化合物效应必要或关键，但没有直接结合证据。T3 是功能靶点，不得写成 validated direct target。需要方向一致、适当对照，并排除普遍毒性或完全失去细胞状态造成的伪 rescue。

## T4：受调控/通路相关蛋白

仅观察到表达、磷酸化、定位、核转位、活性或通路 readout 改变。Nrf2、KEAP1、NF-κB/p65、SOD、CAT、GPX 等如仅有此类变化均进入 T4；关系类型应写 `regulated_protein` 或 `pathway_associated`，不能写 binding/direct target。

## T5：预测靶点

来自 SwissTargetPrediction、network pharmacology、机器学习、反向对接、分子对接或其他计算推断。必须保存算法、版本、输入结构、分数、背景数据库和检索日期；多个共享训练数据的预测不构成独立验证。T5 只用于假设生成。

## 分层输出与判定规则

只有通过质量检查的 T1/T2 进入 high-confidence direct-target layer；T2 的间接性无法排除时不进入该层。T3 输出为 functional target，T4 为 regulated/pathway-associated protein，T5 为 predicted target。数据库标签不能覆盖原始 assay 判定：BindingDB/ChEMBL/PubChem BioAssay 的记录必须回看 assay description 与原文；CTD/STITCH 的 association 不能默认视作结合。

证据冲突时保留全部记录，以 assay 质量、物种、化合物形式、自由浓度和原始数据为依据，不使用简单多数票。多酚常见的 PAINS、胶体聚集、蛋白非特异结合、金属螯合、共价氧化、荧光/发光干扰和样品降解必须检查。所有 T1/T2 至少记录纯度、蛋白构建体、缓冲液、温度、化合物形式、剂量范围、定量值、阴性/竞争对照和正交验证状态。

## 例子

“EGCG 降低 p65 核转位”为 T4；“基因敲除使 EGCG 的 redox 表型消失”为 T3；“竞争性 pull-down 在细胞裂解物中富集某蛋白并由游离 EGCG 竞争”为候选 T2；“纯化蛋白 ITC 获得可重复 Kd，并用正交方法排除聚集”为 T1。
