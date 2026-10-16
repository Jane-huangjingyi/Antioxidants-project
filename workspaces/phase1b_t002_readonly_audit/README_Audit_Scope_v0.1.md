# Phase1B T002审计范围与转交清单

只读主表与关联参照；唯一新增目录为`workspaces/phase1b_t002_readonly_audit/`。原始结构、191条记录、26/7/2分层及所有现有文件不变。报告CSV为机器可读审计中间结果，不创建或修改工作簿；按用户边界使用Python标准库、-B禁缓存、不安装依赖。audit_t002.py仅支持本轮核查，所有输出exclusive create，若同名文件存在立即停止，禁止直接覆盖重跑。

本审计仅依据当前仓库数据及字典判断记录一致性和证据边界，未进行外部PubChem结构查证、文献恢复或化学形式裁决。未确认实体的名称相同不能视为结构匹配；空CID不与另一个空CID构成正匹配。诊断CID使用Decimal检验正整数等值，仅存于审计输出；所有源值逐字保留。完整InChIKey精确匹配，不以第一段代替完整键。名称大小写折叠仅为诊断，未做同义词规范化。CSV逻辑记录号从1计、表头不计；physical_lines从文件第1行计并包含多行单元格的整个区间。观察值列表是描述统计，不是获批受控词汇。

P0指阻止身份自动确认/映射批准的问题，P1指应优先人工定义/证据审核的问题，P2指维护与探索性提示；不等同科学错误严重度。DATA_CONFIRMED_ISSUE只陈述表内可直接证明的缺失/来源粒度问题；DEFINITION_REVIEW_REQUIRED不宣称已有错误；POTENTIAL_SCIENTIFIC_RISK不宣称具体化学或临床结论已经证实。

## 转交ChatGPT的完整相对路径

- P0：`workspaces/phase1b_t002_readonly_audit/T002_ReadOnly_Audit_Report_v0.1.md`
- P0：`workspaces/phase1b_t002_readonly_audit/Sync_to_ChatGPT_Phase1B_T002_v0.1_CN.md`
- P0：`workspaces/phase1b_t002_readonly_audit/T002_Identity_and_CrossTable_Match_Audit_v0.1.csv`
- P0：`workspaces/phase1b_t002_readonly_audit/T002_Scientific_Risk_Register_v0.1.csv`
- P1：`workspaces/phase1b_t002_readonly_audit/T002_Field_Dictionary_Review_v0.1.csv`
- P1：`workspaces/phase1b_t002_readonly_audit/T002_Observed_Value_Domain_Audit_v0.1.csv`
- P1：`workspaces/phase1b_t002_readonly_audit/T002_Structure_and_Missingness_Audit_v0.1.csv`
- P2：`workspaces/phase1b_t002_readonly_audit/README_Audit_Scope_v0.1.md`

supporting包含逐单元格问题定位、全行语法验证、输入/匹配质控、前后完整性证据和最终Git状态。它们用于追溯，非正式crosswalk。CSV用UTF-8 BOM；JSON单元格为完整列表，无Excel显示截断带来的信息删除。

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
