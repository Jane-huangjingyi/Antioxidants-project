# Track B：候选物优选依据 v0.1

日期：2026-10-26。性质：待科学审查的可行性草案；human_review_status=NOT_REVIEWED，change_applied=NO。不产生正式综合排名、权重或分数，不批准实验。Git基线为07e3adb02eac1aeb54dfbb4bf801fed09cae03ad，独立分支codex/track-b-robot-screening-feasibility。该提交包含已完成Track A历史；本任务未合并其他分支，也未修改Track A目录。当前状态入口LATEST_PROJECT_STATUS_CN.md日期为2026-10-15，早于后续治理与科学审核材料，不能代表全部最新进展。

## 覆盖范围与解释

191种全集来自data/candidate_universe/Antioxidant_Class_Candidate_Master.csv。157种文献主表、综合证据画像和五维可用性矩阵的candidate_id集合一致，均属于191全集；785行矩阵为157×5。Aqueous_Antioxidant_Candidate_Master.csv有157行但无candidate_id，其同名数量不作为身份等价证明；本次以三个带ID的157种输入界定覆盖范围，不进行模糊名称合并。未覆盖的34种为AFF-0106–0113的8种维生素E形式、AFF-0114–0132的19种类胡萝卜素、AFF-0185–0191的7种矿物/辅因子条目，完整逐项构念保存在qc/Build_Summary.json及交付CSV。缺少框架覆盖不代表无活性。

AFF-0082 Feruloylquinic acid和AFF-0150 Probetanin的既有CID/InChIKey不完整，保留身份待决。原始索引的标识是溯源线索，并非本轮采购物料已经核定。盐型、异构体、糖苷、水合物、实际纯度及配制分子量必须逐批确认。

五维定义和26项指标沿用docs/framework/Comprehensive_Antioxidant_Framework_v0.1_CN.md及data/framework/Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv。矩阵中的AVAILABLE_VERIFIED仅表示原快照定义下已有核查内容，不能解释为该维度所有指标均完整或当前实验就绪。

|维度与目标|既有指标及来源|157种快照覆盖|缺失规则和解释边界|
|---|---|---|---|
|D1 抗氧化活性：区分具体化学/功能终点|ORAC_FL、DPPH、ABTS、FRAP、CUPRAC、CAA、OX_STRESS；冻结表、原始实验主表、证据画像|已核查8，未核实20，未检索127，身份待决2|不跨方法直接合并TE数值；未检索不等于无效；化学值不证明人体获益|
|D2 证据可靠性：判断来源、独立性和测量质量|ORIGINALITY、INDEPENDENT_N、PRECISION、HETEROGENEITY、BIAS；6D来源闭环、误差审计|未核实28，未检索127，身份待决2|无SD/SE/CI不补算；实验记录数、去重论文数及独立研究数分别保留|
|D3 研究成熟度：描述研究积累|EARLIEST、LATEST、SPAN、ORIGINAL_N、RECENT_5_10、ASSAY_N；文献主表元数据|未核实155，身份待决2|文献量不等于效力；数据库检索覆盖不等于全部文献；未来年份需核实|
|D4 生物学相关性：区分细胞、动物和人体证据|CELL、ANIMAL、HUMAN_OBS、HUMAN_INT；证据画像与筛选元数据|未核实126，未检索29，身份待决2|计数不证明效应方向、因果或临床获益；AFF-0061机制观察尚未人工批准|
|D5 应用可行性：材料、稳定性、暴露和安全背景|STABILITY、BIOAVAIL、SAFETY、SOURCE；框架与后续采购/实验记录|未检索155，身份待决2|当前无充分采购与平台验证；不按类别推断溶解性、生物利用度或安全性|

以上状态逐字保留于CSV的D1–D5_snapshot_status；34种范围外条目留空并标NOT_COVERED_BY_157_SNAPSHOT，不能伪造为原矩阵NOT_SEARCHED。NOT_REPORTED、NOT_SEARCHED、INACCESSIBLE、IDENTITY_UNRESOLVED和不适用必须分别记录，不以0插补，不做均值插补，不据此计算综合分数。文献主表中AFF-0159、0104、0009、0069、0084、0010、0061存在2027年最新年份，与当前日期不符，已加标记，未修改原值或重算成熟度。

## 分层及小面板

本次以“拟议首批统一水相H-ORAC-FL方案”作为方法适配情景。优先进入实验可行性评估0种：没有物料可获得性、实际批次和平台相容性证据足以满足全部入层条件。需要补证后再评估133种。暂缓该情景首批58种，其中24种在既有文献主表明确标记不适合可比较H-ORAC排名，另34种的原索引构念需要脂相、单线态氧或辅因子等独立检测臂，当前没有统一水相方案适配依据。逐种原因和来源在CSV，暂缓不是永久排除，也不是断言物理不溶或没有抗氧化作用；更换检测情景后须重新审查分层。

冻结Top20仅为探索入口，保留原A+B1中位数排名及整行JSON，不是机器人Top20。其eligible_A_B1_N是原证据记录数，不能替代6D确认的独立研究数。6D在Top20中确认至少2篇独立纯物质原始研究的有8种；另有Gallic acid在Top20外。未形成新的正式v1.1，不据此剔除或重排冻结表。Rosmarinic acid虽冻结第1，但当前闭环仅1篇；Daidzein、Hesperidin、Naringin确认数为0表示当前闭环未确认，不能解释为无研究或无活性。所有候选物的6D确认DOI和未解决来源数分别保留；本轮未重新逐篇验证全文。

P4条件面板：AFF-0002 Epicatechin、AFF-0069 Caffeic acid、AFF-0061 Protocatechuic acid、AFF-0071 p-Coumaric acid。选择依据是每种至少两篇已有6D闭环来源、可用于小规模方法与剂量响应核查，并非活性前四或已证实可采购。P6条件面板在P4基础上增加AFF-0001 Catechin与AFF-0070 Ferulic acid，分别增加异构体身份控制及已有研究间差异的复现问题。六种的逐项DOI均在CSV；不依据类别赋予未知物性。原儿茶酸入选不使用尚待人工裁决的21条机制观察加分。

P4与P6全部仍属“需要补证后再评估”。采购COA、可用物料、溶解度和光学相容性通过后，研究者再决定是否进入首批。P6增加成本和干扰验证工作，不能因面板较大认定科学价值更高。未选入的候选物不构成负面结论，未来可按明确问题加入Top20外候选物。不存在强行凑齐20种的需要。

复现：使用随附scripts/build_track_b.mjs重建两张CSV；qc/Build_Summary.json保存输入哈希、集合差、覆盖计数及输出哈希。CSV的original_universe_row_json保留原始索引字段，existing_profile_json保留既有画像；所有新增建议保持NOT_REVIEWED与change_applied=NO。
