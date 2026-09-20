# Broken Path Audit（Stage 25A.1）

审计日期：2026-09-20。检查范围为 archive 之外的 active Markdown、CSV、R、Python 和 text 文件；以 `PROJECT_FILE_MIGRATION_MAP.csv` 中所有发生路径变化的 `old_path` 为字典，并额外检查旧 monolithic R script、旧 Stage 25A master/provenance 路径和旧 `10_unified_literature_screening` figure path。

迁移表共 362 行：ACTIVE_CANONICAL 110、ACTIVE_SUPPORTING 85、SUPERSEDED 49、HISTORICAL_ONLY 118；执行字段中 moved=yes 为 218。迁移表自身因承担 old→new provenance 不纳入“旧路径残留”错误。扫描发现 migration-dictionary stale references 0 条，显式关键旧路径 references 0 条。无法判定是否完全替代而触发 `HUMAN REVIEW REQUIRED — FILE CONSOLIDATION` 的迁移项为 0 条。

审计结论：**PASS**。当前 active 文件未发现已知旧路径断链；archive 内历史脚本和历史说明允许保留当时路径，因为其用途是 provenance，而不是当前执行入口。若后续移动 active 文件，必须先更新 migration map 和 dependency，然后重跑本审计。
