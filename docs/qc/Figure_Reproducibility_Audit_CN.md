# Figure Reproducibility Audit（Stage 25A.1）

审计日期：2026-09-20。审计对象为 `figures/FIGURE_CODE_DATA_MAP.csv` 登记的 active canonical aqueous atlas figures。本次从薄入口 `R/render_all_active_figures.R` 依次调用模块化脚本，29/29 张登记图均成功重建。该结论只覆盖 active canonical 图，不把 supporting、superseded 或 historical figures 误计为当前可复现图包。

映射登记数为 29；当前 atlas PNG 数为 29；缺失图 0；缺失 R script 0；缺失输入文件 0；未登记 canonical PNG 0。每张图的路径、科学问题、生成脚本、输入数据、过滤与转换摘要、输出 metric、可调参数和 caveat 均记录于 figure-code-data map。两张 Stage 25A 旧图的轴异常已定位为在 log10 坐标转换后使用数值型 `nudge_y` 导致标签尺度再次失真；错误版本保留在 `archive/figure_qc_stage25A1/`，canonical replacement 改为单次 log10 transform 并使用显示空间的 `vjust`。

审计结论：**PASS（29/29 active canonical figures reproducible）**。执行环境仍可能报告 Windows locale 警告；这不改变数值或文件生成。任何未来 figure 增删必须同步更新 `figures/FIGURE_CODE_DATA_MAP.csv`、`figures/FIGURE_INDEX_CN.md` 和模块脚本，且不得直接手工覆盖 canonical PNG。
