# 同步ChatGPT：Phase1B T002只读核查 v0.1

Git基线与结束HEAD：`46a02f850ca29fefebe47081f0221475f8d2a9eb`；分支main。任务完成后停止，未自动同步至其他聊天，由用户转交本文件及P0/P1附件。

本轮完整读取T002的191条记录、35个字段，保持26个核心、7个扩展、2个技术/历史字段。candidate_id无空白、无重复、格式有效，可唯一定位记录；191条候选记录不等于191种身份去重的独立化合物。UTF-8严格解析、表头唯一性、各行宽度、CID/InChIKey/分子式语法、非空分子量正数及日期诊断通过；分子式仅做词法检查，不做元素/结构计量科学确认。存在身份缺失及定义问题，故总体不是无问题PASS。

AFF-0082（Feruloylquinic acid）和AFF-0150（Probetanin）的CID、InChIKey、分子式及分子量均为空，每字段缺失2/191（1.0471%）；保留未解决身份，不自动补齐。synonym与exclusion_reason各191条真空白，notes有185条真空白；这不自动构成错误。空白、独立unresolved、复合unresolved、not applicable等已分开统计；全部35字段的完整原值域和频数均输出，无截断。

T002与T110按ID匹配157条，T002独有34条，T110孤儿0条。名称原值差异58条，其中仅大小写差异30条；CID原值差异155条，诊断整数化后实质CID冲突0条；完整InChIKey差异0条。未观察到不同非空CID/完整键的实质冲突，但同义名、立体限定词、阳离子/盐型及形式解释仍待审核，不能从标识相同宣布结构已人工确认。T110缺席仅为表间覆盖差异，不自动判数据缺漏。

T004的157条记录只有候选建议：{"MATCH_PROVISIONAL": 155, "UNRESOLVED_IDENTITY_REVIEW": 2}；一对多0条，多对一候选0个，无任何候选0条。CID、完整键、规范名及来源compound各独立比较，非空两结构锚同时支持且唯一者才标MATCH_PROVISIONAL；2条缺少结构锚的名称候选保留UNRESOLVED_IDENTITY_REVIEW。没有生成获批crosswalk或回填T004。现有身份表状态：{"IDENTIFIER_PRESENT_NOT_STRUCTURALLY_RECHECKED": 155, "IDENTITY_UNRESOLVED": 2}；标识存在未结构复核与identity resolved不是同一层审核。完整键前14位相同的10组仅作防误合并提示，不合并记录。

字典35/35字段存在且英文名完全一致，逐项核查已完成；21项是通用占位或旧定义待确认。字典状态分布为{"CURATED_PROJECT_DEFINITION": 14, "NEEDS_REVIEW": 21}。CN文本均非空且未含替换字符，但非空不等于科学定义完整；所有35项操作性类型/取值/边界仍需复核。字典没有独立human approval或本次field stratum属性，本轮明确报告缺失，不把CURATED_PROJECT_DEFINITION当成人工批准。T002 compound定义含T004特定映射说明，其表内适用范围需复核。字典完整审阅不等于定义已获批准。

观察到candidate_eligible为yes182、unresolved9；normal_dietary_exposure为yes180、unresolved11，supplement/medicinal为no180、unresolved11。food_occurrence_confidence为moderate178、low / unresolved11、unresolved2；第三状态及复合状态均不是自动批准枚举。parent_class7类、analysis_panel9类、subclass36值；分类、面板及结构轴之间的边界属于DEFINITION_REVIEW_REQUIRED。current_review_status为identity resolved等复合文字178条、researcher inclusion4条、unresolved do not rank9条；4条纳入决定不代表全部结构已经人工审核。

191条food_occurrence_reference均为通用库名/资料类别，未提供候选物级定位引文，这是来源粒度的已确认问题，不是否定食物存在。分子式/分子量具体形式、食物存在与暴露/摄入、候选资格与实验/VSIR/临床、likely构念与实测证据之间均须保持边界。7条矿物辅因子源表已明确no capacity rank，不得并入小分子直接容量排名。分子量范围24.305–863.3，1.5 IQR诊断界限-189.34999999999997–831.05，标记1条分布离群，仅作为形式复核提示，不判错、不删除。

风险登记共14个去重issue_id：P0=2、P1=10、P2=2。这是独立治理问题数，不是错误候选物数；受影响记录和单元格可跨问题重叠。证据类型分别为{"DATA_CONFIRMED_ISSUE": 2, "DEFINITION_REVIEW_REQUIRED": 7, "POTENTIAL_SCIENTIFIC_RISK": 5}。原值、路径、逻辑记录号和CSV物理行区间详见主表关联结果及supporting/Cell_Level_Findings_v0.1.csv。

建议人工审查顺序：先处理AFF-0082/AFF-0150的具体身份及155条身份审核状态与下游文字的对应，再审阅名称含立体、盐、阳离子限定词的映射建议；随后决定候选物级食物来源和暴露证据标准，最后逐项审定字典定义、状态空间与审核角色。26/7/2分层本轮保持不变，建议在定义审核后再决定是否授权任何结构调整。允许进入人工审查，不允许直接发布、批准crosswalk、改字典、清洗身份或进入Phase 2；不重新计算任何排名，不判定VSIR，不commit/push。

开始HEAD与结束HEAD均为`46a02f850ca29fefebe47081f0221475f8d2a9eb`，任务初次读取时工作树干净。写入前、后对审计目录和.git以外的全部7109个现有文件逐一做SHA-256及大小比对，变化0。审计程序先在唯一授权输出目录创建，故执行时Git已显示该目录未跟踪；与初次干净快照区别已记录。结束工作树只允许新增本审计目录。完整哈希和输入解析记录位于supporting；最终Git状态另见supporting/Final_Git_Status_v0.1.json。未修改任何原始CSV、Phase1字典、Word、历史包、冻结资产或配置，未执行Git写操作。

```text
T002 Structural Audit: ISSUES_FOUND
T002 Identity Audit: ISSUES_FOUND
Cross-table Mapping Readiness: HOLD
Field Dictionary Review: COMPLETE
Original Data Modified: NO
Frozen Assets Modified: NO
Release Readiness: HOLD
Phase 2 Reorganization: HOLD
```
