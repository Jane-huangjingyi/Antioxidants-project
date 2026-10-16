# H-ORAC 数据目录与版本查找

`stage25b/` 保存持续更新至 Rubric v2 迁移后的 canonical 主表，虽然目录以起始阶段命名，内容并非初始 Stage25B 快照。最初版本及迁移前版本见 `checkpoints/`，正式冻结排名见 `frozen/`。文件名保留，便于用阶段编号和原始名称查找。

| 目录 | 用途 |
|---|---|
| `stage25b/` | canonical 实验、候选汇总、量化排名、检索和来源记录 |
| `stage25b1/` | cutoff 优先级、定点裁决及敏感性记录 |
| `stage25b2/` | 当时 Tier A feasibility 审计 |
| `stage25b3/` | Rubric v2 验证与影响模拟 |
| `stage25b4/` | 已批准 v2 迁移、方法汇总和敏感性产物 |
| `stage25b6a/`–`stage25b6d/` | 后续证据诊断，不能替代正式冻结排名 |
| `checkpoints/` | 带阶段和日期的历史检查点，原样保留 |
| `frozen/` | 正式 Stage25B.5 Frozen Top20 v1.0 与 SHA256 清单 |
| `_working/` | 检索过程工作文件 |

本轮移动前后的路径见 `../../current_review/File_Reorganization_Migration_2026-10-16.csv`。后续引用应使用现路径；历史报告和冻结 provenance 中的旧路径保留当时语境，可通过迁移对照查询。阶段和日期排序不等同于科学状态排序。
