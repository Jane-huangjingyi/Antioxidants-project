# R Figure System

2026-10-30：完整入口为`Rscript R/reproduce_all_figures.R`（从项目根目录运行）。全部51张当前科研图片同时导出PNG与SVG到`figures/editable/`，不覆盖旧图或冻结图；支持图使用完整的`supporting/render_supporting_figures.R`配方。逐图数据/代码/图片入口见[当前图片核查页](../current_review/VISUALIZATION_REPRODUCIBILITY_CN.md)。SVG使用svglite保留文字；修改通用色板/字体用common/plot_config.R，修改支持图的颜色、点线及布局用对应R配方顶部参数和图层。首次安装依赖到R/library后，运行入口会保存会话和警告记录。历史R脚本仅作当时过程记录，不作为当前可执行入口。

从项目根目录运行 `Rscript R/render_all_active_figures.R`。`common/` 只共享配色、字体、路径和保存函数；filtering、ranking 和 transformation 均写在对应科学模块脚本中。图目录与 R 目录基本镜像。修改全局颜色或默认字号请编辑 `R/common/plot_config.R`；修改某张图的筛选、尺寸或标签请编辑对应脚本顶部的 user-editable settings。
