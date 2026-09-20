# R Figure System

从项目根目录运行 `Rscript R/render_all_active_figures.R`。`common/` 只共享配色、字体、路径和保存函数；filtering、ranking 和 transformation 均写在对应科学模块脚本中。图目录与 R 目录基本镜像。修改全局颜色或默认字号请编辑 `R/common/plot_config.R`；修改某张图的筛选、尺寸或标签请编辑对应脚本顶部的 user-editable settings。
