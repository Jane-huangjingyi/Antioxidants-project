# Antioxidants Project

最新阅读入口：[current_review](current_review/README_CURRENT_REVIEW.md)；查找历史版本：[历史索引](current_review/HISTORICAL_VERSION_INDEX.csv)与[归档说明](archive/HISTORY_NAVIGATION_CN.md)。2026-10-16 文件整理已将 H-ORAC 主表分入 `data/h_orac_stage25b/stage25b/`，正式排名仍为 `data/h_orac_stage25b/frozen/` 中的 Frozen Top20 v1.0。

当前科学主线为：冻结候选宇宙 → 类别内抗氧化表征 → 跨类别统一文献证据密度筛选 → Stage 25B H-ORAC-FL 定量检索 → 后续 Top20。先读根目录的 `PROJECT_FILE_INDEX_CN.md` 查找当前 canonical 文件；需要了解项目演变时读 `docs/PROJECT_STAGE_INDEX_CN.md` 和 `Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md`。当前不得把 research-evidence density 解释为抗氧化强度，也不得跨不相容 assay 构建总分。

数据位于 `data/`，方法和报告位于 `docs/`，当前水相图集位于 `figures/aqueous_antioxidant_atlas/`，可复现 R 代码位于 `R/`，早期版本和被替代文件位于 `archive/`。从项目根目录执行 `Rscript R/render_all_active_figures.R` 可重新生成全部 29 张 active canonical figures。
