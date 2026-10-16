# 文件移动影响核查（2026-10-16）

本轮以 Git `efb7600542e363c2099dd93fba10548747711339` 为移动前基线。42 个原位置消失的受跟踪文件均在现目录找到一份内容相同的对应文件；比较同时考虑 Git 的 LF/CRLF 行尾转换。本轮迁移清单记录现文件 SHA256，行尾一致时标记 `BYTE_IDENTICAL_TO_BASELINE`，仅行尾差异标记 `IDENTICAL_AFTER_GIT_EOL_NORMALIZATION`。未发现移动造成的科学数据缺失或数值改动。

已修复当前脚本、R QC、canonical registry 和 current_review 导航中的失效路径。H-ORAC 主表现位于 `data/h_orac_stage25b/stage25b/`，25B.1–25B.4 产物各归相应目录；主表保留持续更新后的 canonical 状态，不因移入 `stage25b/` 而退回初始阶段版本。Frozen Top20 v1.0、Rubric v2 和既有科学结果保持原内容，冻结清单的 10 个文件逐项匹配。

命名已调整：`phase3_local_cache`、`stage24_local_cache`、`stage25_local_cache` 主要保存历史 Python 构建脚本，改名为对应的 `*_historical_scripts`；其中 `.tmp_stage25a` 单列为 `archive/stage25a_local_cache/`。Phase2 的两个历史身份查询 JSON 保持 `phase2_local_cache`，名称符合内容。Stage25A 本地缓存仍受 Git 忽略，README 是该目录唯一拟纳入版本控制的文件。原有科学文件名保留，用迁移索引解决路径变化。

历史版本按原阶段/日期目录保留，新增 `HISTORICAL_VERSION_INDEX.csv`、`archive/HISTORY_NAVIGATION_CN.md` 及各整理目录 README；索引覆盖 archive、H-ORAC checkpoints 和既往阶段诊断。正式冻结产物继续位于 `frozen/`。历史报告与冻结 provenance 中的原路径保留当时语境，通过迁移清单查到现位置；历史脚本仍保持原内容，其根目录深度和输入版本假设须在历史 Git 环境中恢复，不能据本次路径核查声称历史脚本可直接重跑。

`Repository_File_Inventory.csv`、原重复审计与前轮治理 QC 保留为 2026-10-15 基线记录。本轮现状见 `Repository_File_Inventory_Current.csv`、`File_Reorganization_Validation_2026-10-16.json`；当前清单不对自身、动态总索引和最终验证 JSON 存储自引用哈希。规范文件登记、导航源文件存在性、哈希和 Python/PowerShell 语法通过静态核查。未执行会重建或覆盖科学结果的阶段构建脚本；未删除历史版本或启动科学排名重算。

本次按用户授权整理本地文件和依赖，尚未执行 Git commit/push。Git 在提交前仍会把原路径显示为删除、现路径显示为新增；这是未暂存迁移的表现，提交时可识别对应重命名。源数据的内容校验与正式状态不依赖 Git 状态界面的这一显示。
