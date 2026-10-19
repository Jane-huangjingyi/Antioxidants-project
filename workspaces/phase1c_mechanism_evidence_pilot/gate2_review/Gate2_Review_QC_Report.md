# Gate2定向审核质控

共复核21/21条、10篇原始出版物。审核状态为{"HOLD_SOURCE_VERIFICATION": 7, "KEEP_PROVISIONAL": 12, "RECLASSIFICATION_PROPOSED": 2}；EXCLUDE_PROPOSED=0、UNRESOLVED=0（无整体无法判断行，但多个具体属性仍UNRESOLVED）。蛋白确认提案为{"COMPUTATIONAL_ONLY": 3, "FUNCTIONAL_PARTICIPATION_SUPPORTED": 2, "NOT_APPLICABLE_NO_PROTEIN_TARGET": 3, "OMICS_ASSOCIATED": 1, "READOUT_ONLY": 6, "UNRESOLVED_PROTEIN_OR_EVIDENCE": 6}。抗氧化相关性primary为{"DIRECT_REDOX_OUTCOME": 1, "INDIRECT_OXIDATIVE_STRESS_ASSOCIATION": 3, "OTHER_BIOLOGICAL_FUNCTION": 14, "PROOXIDANT_OR_ADVERSE_RESPONSE": 3}；NRF2行另有ANTIOXIDANT_FUNCTIONAL_MECHANISM secondary，促氧化GSH行另有DIRECT_REDOX_OUTCOME secondary。没有强制让每类都非零。

未发现把现有对接/MD行写为实验直接结合的错误。提出2个主关系收窄建议（Akt药理行、摘要TYR行）；TYR因来源不足总体先HOLD，不能将关系变更提案数与RECLASSIFICATION_PROPOSED状态数混为同一统计。另1个HDAC1联合组方向措辞需收窄，避免把NS当零效应。SIRT3对接物种可建议补为人源，但仍是计算预测。原行、原关系和字典均未修改。

TRAF2合法全文未恢复，两条保持ABSTRACT_ONLY/HOLD；α-amylase的Table3及原图核查未解决制备物矛盾，仍HOLD。NRF2实际读到补充S2细胞补回；不得移用于动物6L。Figure6M/N原图标签可读，但图文冲突仍待作者/底层数据裁决，保留6L不猜测改值。未发现10篇当前元数据中的DOI/PMID实质冲突或撤稿链接；这不是永久有效性保证。参考母体身份未发现新冲突，商业amylase及重组TRAF2具体身份仍待解决。

66字段逐项评估完成，建议先批准独立靶点确认、抗氧化相关性、剂量基准及审核事件/实验粒度规则；不要求无差别加列。抗氧化相关性独立于靶点强度，非抗氧化机制仍保留。暂不建议批量扩展其他候选物。

Gate1：HOLD（正式标准仍待批准）。Gate2：HUMAN_SCIENTIFIC_REVIEW_REQUIRED，未宣布通过。Release：HOLD。Phase1B风险、155临时映射/2待审、缺失身份及冻结资产均未被本轮关闭。

程序检查12项通过、0项失败，明细见Review_Counts_and_Integrity.json。逐行矩阵同时保留完整original_record_json及14类审查维度。KEEP_PROVISIONAL仅为待人工批准；HOLD不是判作者报告虚假；RECLASSIFICATION_PROPOSED仅提出规则/措辞修订，不自动写回。

起始分支main，实际HEAD与GitHub main只读核对均为f86aca02209d799367287082dea3d4438a224cd3。本轮审核产物生成时HEAD仍相同，工作树仅新增gate2_review目录。668个原有跟踪文件及31个既有本地来源缓存哈希均不变；保护对象含原21条/机制Master、T002/T004/T110、两套字典、Phase1B、矩阵与冻结结果。本轮新来源在sources/，通过本目录.gitignore排除上传，清单与URL日志可追溯。没有越权科学写回。

用户已持续授权合适任务的提交前整理与选择性commit/push，因此本轮仅将新增审核Proposal和QC提交，不提交sources、不改科学源表；这不表示Gate2或Release批准。上述HEAD是审核前/提交前快照，提交后的哈希由最终回复及Git记录报告，不改写历史基线。

本轮人工科学批准数0。完整图像检查仅针对NRF2 Figure6、其补充PDF第3页S2以及amylase Figure2；其余按正文/方法/图注复读，不冒称全部原图和原始数据已审。来源可访问性与图文矛盾分别报告，不用格式检查替代科学验证。未产生PPI、网络接近度、排名或其他候选物数据。

## 转交清单

- P0：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/AFF-0061_Gate2_Evidence_Review_Matrix.csv`
- P0：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/AFF-0061_Critical_Source_Verification_Report.md`
- P0：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/Sync_to_ChatGPT_Phase1C_Gate2.md`
- P1：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/Mechanism_Evidence_Classification_Proposal_v0.1.md`
- P1：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/Mechanism_Evidence_Schema_Change_Proposal_v0.1.md`
- P1：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/Gate2_Open_Issues_and_Decisions.csv`
- P2：`workspaces/phase1c_mechanism_evidence_pilot/gate2_review/Gate2_Review_QC_Report.md`
