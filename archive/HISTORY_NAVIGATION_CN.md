# 历史版本查找说明

按阶段、用途、文件名和当前正式替代路径检索 `current_review/HISTORICAL_VERSION_INDEX.csv`。完整目录保留现有日期与阶段标识，避免打散同一构建包的内部依赖。`current_review/File_Reorganization_Migration_2026-10-16.csv` 对照本轮迁移前后的路径与内容校验结果；更早迁移见根目录 `PROJECT_FILE_MIGRATION_MAP.csv`。Git 提交历史保留可追溯的原始位置。

| 位置 | 内容和使用状态 |
|---|---|
| `phase2_local_cache/` | Phase 2 历史 PubChem 身份查询快照；已有 Git 记录，继续保留 |
| `phase3_historical_scripts/` | Phase 3A–3D 历史构建与 QC 脚本 |
| `stage24_historical_scripts/` | Stage24/24B 历史构建、图去重与 QC 脚本 |
| `stage25_historical_scripts/` | Stage25A/25A.1 历史检索、构建与目录治理脚本 |
| `stage25a_local_cache/` | Stage25A 候选检索 JSON 与本地审计中间件；仅 README 进入 Git |
| `historical_stage_summaries/`、`historical_sync/` | 当时的阶段说明与交接材料 |
| `superseded_outputs/`、带日期的 transition/legacy 目录 | 被替代产物及原上下文 |
| `R_legacy/` | 模块化前的历史 R 脚本 |
| `figure_qc_stage25A1/`、`figure_redundancy_stage24/` | 已替代或归档的图与清单 |
| `../data/h_orac_stage25b/checkpoints/` | H-ORAC 各次迁移前的不可变检查点 |
| `../data/h_orac_stage25b/frozen/` | 正式冻结交付，继续留在数据目录，不并入一般历史包 |

历史 Python 脚本保持归档时内容，部分仍假设旧目录深度、旧字段及当时的数据结构。它们用于审计方法演变；需要复现历史分析时，应从对应 Git 版本恢复独立环境，避免直接执行并覆盖当前结果。当前可用代码位于根目录 `scripts/` 和 `R/`，脚本名称中的阶段号表示生成阶段，不能据此推断其输出是当前正式版本。

冻结排名的正式性以 `CANONICAL_ASSET_REGISTRY.csv` 和 `current_review/LATEST_PROJECT_STATUS_CN.md` 为准，不能按文件日期或文件名中的最大版本号自动决定。原样保留阶段文件名；阶段数字 25B.1 在目录中统一写作 `stage25b1`，与既有 25B.6A–6D 命名一致。
