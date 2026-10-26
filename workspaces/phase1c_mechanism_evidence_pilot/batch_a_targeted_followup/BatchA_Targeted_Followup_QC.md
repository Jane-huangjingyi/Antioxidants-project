# Batch A定点补核QC

日期2026-10-26。130 PASS / 0 FAIL；逐项结果见qc/Followup_Validation.json。这是材料完整性、追溯与权限检查，不是科学证据批准。

9个ID唯一且与Batch A一致。4条ACCEPT_PROPOSAL_CANDIDATE、3条REVISION_REQUIRED_CANDIDATE、2条SOURCE_PENDING_CANDIDATE仅为Codex准备意见。每条保留原66字段、原Batch A完整59字段、原建议字段变更、三维分类、来源、具体用途限制及剩余问题关联；三维分类未升级。15项不确定性有来源和所需补证。全部NOT_REVIEWED、change_applied=NO，人审姓名/决定/批准日期为空。

763个既有跟踪文件、53个既有来源缓存逐文件SHA256不变。21条原观察及其余12条、66字段字典、257项科学提案、257项待审事件、7条来源HOLD、治理规则、Master和H-ORAC Top20资产均保留。新来源与失败响应本地忽略，不提交全文、图像、PDF、DOC、ZIP或序列数据。

DRA与项目run清单均核对同3条映射，样本/run不等同生物重复；HDAC1有效补充包只有7页blot PDF，DataS1已只读取得并核对文本。失败附件按签名/内容类型排除，DDBJ应用壳不冒称元数据。没有RNA-seq重分析、剂量补算或能量单位择一换算。

两张CSV使用Artifact Tool作者值写入及读回、recalculate、inspection、错误扫描和有界PNG预览。CSV是无公式文本记录，重新计算不代表实验复现；全列内容由读回及JSON快照核对，预览只检查主要ID和状态。9种内存负例拒绝越界、重复、漏项、自动批准、伪造签署与错误候选；不写入原证据。

分支codex/phase1c-aff0061-batch-a-targeted-followup，来源提交48b34a7314b1d5914c4bb70f770e7e6d2fe939fe。正式Gate/Scale-up/Release权限不变。归档提交SHA和push状态见最终交付与Git历史，文件不自引用未来SHA。复核可用捆绑Node运行scripts/validate_followup.mjs，仅读旧资产并更新本目录QC；不调用检索或重分析。
