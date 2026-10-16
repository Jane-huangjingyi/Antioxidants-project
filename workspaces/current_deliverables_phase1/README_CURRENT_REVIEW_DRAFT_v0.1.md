# Antioxidants Project Current Deliverables

DRAFT v0.1 | 2026-10-16 | Baseline `24653d04f4b96849bdcc57039aecfb3cda99da4f` | Formal release date not assigned

## Project Overview

本草稿包整合现有数据库、方法和证据边界，供研究者与ChatGPT进行科学审查。权威源文件继续保留在原模块；本目录是受控工作区，不是已发布数据库，也不覆盖原current_review入口。

## Database Scope

全类别背景库为191条记录、9个analysis panels；不能直接称为191种身份去重化合物。当前水相主线为157种候选物、7个panels。既有H-ORAC排序覆盖28种候选，不表示28种均符合VSIR。

## Current Deliverables

- [中文Word说明书](guides/Antioxidant_Database_User_Guide_v0.1_CN.docx) 与 [English User Guide](guides/Antioxidant_Database_User_Guide_v0.1_EN.docx)
- [实际字段字典](dictionaries/Database_Field_Dictionary_v0.1.csv) 与 [缩写及编码](dictionaries/Abbreviations_and_Codes_v0.1.csv)
- [Methods CN](manuscripts/Methods_Draft_v0.1_CN.md)、[Methods EN](manuscripts/Methods_Draft_v0.1_EN.md)、[Results CN](manuscripts/Results_Draft_v0.1_CN.md)、[Results EN](manuscripts/Results_Draft_v0.1_EN.md)
- [Manifest草稿](governance/Release_Manifest_DRAFT_v0.1.csv)、[QC](qc/Phase1_Deliverables_QC_Report_v0.1.md) 与 [来源导航](provenance/Source_and_Evidence_Navigation_v0.1.md)

## Module Maturity

Frozen Top20 v1.0为既有正式冻结成果。其他模块分别属于候选范围、类别内阶段证据、元数据文献筛选、局部来源审计及五维框架原型；详见[科学状态矩阵](provenance/Scientific_Scope_and_Status_Map_v0.1.csv)。新制作文件全部为DRAFT，不改变被引用源成果的科学状态。

## Quick Start

先确定问题是候选身份、文献覆盖、特定化学测定还是生物与应用证据。按[表清单](provenance/Table_Inventory_v0.1.csv)选择模块，再按实际表头及字段字典读取。使用candidate_id关联有该字段的表；水相主表需通过compound与筛选主表canonical_name的受控映射及结构核对，不能按两个canonical_name字段直接假定一致。

## Data and Evidence Navigation

表清单覆盖138份仓库源表及10份草稿元数据结构。历史诊断表和旧设计schema明确标注。原始数据不复制为第二套可编辑库。本包没有新源数据快照；数据使用者须能访问Manifest定位的基线仓库文件。由结果依次追至实验键、原论文、原始表页、原值与单位及换算。外部文献访问状态以来源表为准，本轮不重新裁决全部原文。

## Screening and Evaluation Rules

既有H-ORAC记录使用Rubric v2.0，A+B1构成既有主集合，B2仅敏感性。VSIR v1.0科学设计条件性冻结但状态为APPROVED_NOT_IMPLEMENTED：至少两项符合要求且真正独立的原始实验研究；自动GO/NO-GO另需SEARCH_COMPLETE和EVIDENCE_CLOSED。关键缺口或重大争议进入HOLD及人工复核。12项边界测试未执行，本轮不赋予候选新资格。

## Methods Summary

候选物按身份和类别组织，Stage25A保留Europe PMC检索与OpenAlex引用元数据；既有H-ORAC表保留原值、单位、形式、换算和复核状态。主排名按A+B1记录中位数，描述性范围和误差与研究独立性分别报告。当前制作实施了表头、来源提交、文件哈希、计数和中位数复核，未实施新的科学筛选或全文抽取。

## Results Summary

来源表有45,643条候选物论文记录，其中41,967条计入元数据主指标。H-ORAC为74条实验，A/B1/B2/X=7/61/4/2，A+B1为68条，既有可排名候选28种。6D表内来源核实8/16，候选历史资格9/10/9。数值误差27/68、明确SD为4/68；70/74条实验待第二复核，1,641条筛选记录待全文裁决。Frozen Top20 v1.0及三进三出的B2敏感性保持不变。五维框架有26个指标、三个应用场景及785条覆盖行，未形成综合评分。

## Limitations

6D的PASS_VERIFIED不是VSIR GO；元数据论文数不是独立研究数；技术重复不是独立研究。来源未检索、未报告、不可访问、未解决和不适用分别保留。候选CI与排名概率未估计，体外H-ORAC不直接证明人体临床获益。字段和编码中的NEEDS_REVIEW为显式待审语义，不计为已验证定义。Word视觉渲染状态见QC，不能用结构解析代替视觉验收。

## Version and Provenance

baseline_commit记录本轮参考基线；source_commit经逐源核对可定位现路径及内容，行尾差异由local与Git blob两个哈希说明。新文件无正式release_date，不替代任何旧版本。完整证据截止在不能确立时保留未知，不使用文件修改日期代替。

## Links to User Guides and Manuscript Drafts

使用上方Current Deliverables链接。历史解释和维护记录见[CHANGELOG](governance/CHANGELOG_DRAFT_v0.1.md)、[可核实Git事件](governance/Version_and_Maintenance_History_v0.1.csv)及[命名规范](governance/Naming_and_Versioning_Convention_DRAFT_v0.1.md)。
