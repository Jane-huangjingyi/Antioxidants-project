# AFF-0061 A组QC

2026-10-23。自动检查138 PASS / 0 FAIL；逐项结果见qc/BatchA_Validation.json。此结果是准备材料的完整性与边界检查，不是9条证据的科学批准。

9个ID完整唯一，59列覆盖14项逐行要求；每行保存原66字段JSON、来源哈希、历史建议及独立本轮建议，三维枚举均通过已批准词表核对。target_confirmation_class与antioxidant_relevance_primary原本不在旧表，未把旧target_validation_status冒充新类别。建议关系2组学、5响应、2计算；靶点建议1组学关联、5读数、2计算、1无蛋白对象；红氧建议7其他功能、2间接关联。全部NOT_REVIEWED / change_applied=NO，具名裁决和批准日期为空。

747个既有跟踪文件与41个旧本地缓存SHA256均比对；原21条观察、其余12条、66字段字典、257项科学提案、257项待审事件、7条来源HOLD、三张空Verified视图及治理/冻结文件保持不变。未迁移、扩展候选物或改Top20。

18项来源对象有SHA256及用途记录：5个旧XML、5个当前HTML、7张主图、1份既有49页补充PDF。主图均实际视觉阅读；补充PDF仅页级文本筛查及p14/p17视觉核对，不称全部页读毕。3个附件响应为HTML而非目标二进制，已判未取得。QC不认证原始实验、图像完整性、统计有效性或永久无撤稿。

8种内存负例覆盖缺失/重复/越界ID、自动批准、实施变更、推断签署人、伪造日期和无效类别；均不得写入原数据。Artifact Tool完成矩阵作者值写入/读回、recalculate、inspection、错误扫描及A1:C10预览；CSV无公式，重新计算不是实验复现。预览仅便于检查状态/ID，不替代全59列读回。

独立分支codex/phase1c-aff0061-batch-a-review。Git提交与推送结果以最终交付消息和Git历史为准；不自引用未来提交SHA。可使用配置的捆绑Node运行scripts/validate_batch_a.mjs复核；该脚本不运行检索/作者脚本、不改旧资产，仅更新本目录QC。
