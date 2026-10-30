# Archive

2026-10-16 查找入口：[历史版本总索引](../current_review/HISTORICAL_VERSION_INDEX.csv)；[阶段与用途说明](HISTORY_NAVIGATION_CN.md)；[本轮旧路径→现路径对照](../current_review/File_Reorganization_Migration_2026-10-16.csv)。历史脚本按阶段置于 `phase3_historical_scripts/`、`stage24_historical_scripts/`、`stage25_historical_scripts/`；Stage25A 本地检索缓存置于 `stage25a_local_cache/`，缓存仍不进入 Git。原文件名保留，以便按文件名、阶段号或旧路径检索。

Archive 中的文件不是当前 canonical analysis。`historical_stage_summaries/` 保存项目演变，`historical_sync/` 保存已被当前交接包替代的阶段通信，`superseded_outputs/` 保存被后续结果替代的数据和图，`R_legacy/` 保存模块化前长脚本，`figure_redundancy_stage24/` 保存功能重复图，`figure_qc_stage25A1/` 保存轴变换错误图及替换清单。当前 canonical replacement 应从 `PROJECT_FILE_MIGRATION_MAP.csv`、`CANONICAL_ASSET_REGISTRY.csv` 或相应archive manifest查询；历史文件不得作为当前分析输入。

本目录保留真实版本演化，不追求文件最少。2026-09-20最终信息架构审计发现5组archive内部byte-identical文件；它们可能是build staging或两次归档产生的副本，已标记 `HUMAN REVIEW REQUIRED — ARCHIVE RETENTION`，在确认其独立provenance前不删除。忽略的`__pycache__`、partial R library和runtime temporary files不属于科学资产。
