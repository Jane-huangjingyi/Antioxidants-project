# 历史版本与重复清理

本轮按用户授权执行分类导航和有限清理。170个既有archive历史文件采用archive/history/YYYY-MM-DD/原主题/日期_原文件名，日期优先取git log --follow --diff-filter=AM追溯到的最后内容更新，避免用本次移动时间充当研究更新时间。日期是可验证的Git内容记录，不声称等于未记录的离线编辑日期。各主题分层存放；完整原名、新名、SHA256和日期依据在[操作台账](../workspaces/repository_review_20261030/File_Actions.json)。

旧current_review入口、清单、治理/QC报告在更新前保留带日期快照。固定引用的冻结资产、检查点、原始来源缓存、治理批准与审核过程表保留稳定源文件名，通过[分类导航](PROJECT_NAVIGATION.md)和[历史索引](HISTORICAL_VERSION_INDEX.csv)显示日期；不为了改名破坏来源哈希、证据引用和批准清单。文件移动不代表内容更新或科学状态变化。

只删除2个无独立过程信息的相同字节历史图副本：superseded_outputs中的Flavonoid_Top20_Evidence_Confidence.png与PhenolicAcid_Evidence_Confidence.png，保留figure_redundancy_stage24对应图（已日期化归档）。它们的SHA256分别以313eaeab2da4和4cff0c1cfb9b开头，删除前后保留内容一致。旧治理清单中原路径作为历史事实保留，由新台账解析当前位置，不改写旧检查结论。

其余相同字节项继续保留，包括机制compound/master视图、冻结/检查点、迁移演练与重建验证、空检索响应及重要过程记录。字节相同本身不足以证明这些文件可删。依赖包及版本库内部文件不参与科研重复清理。历史脚本按原字节归档，它们可能引用当时的数据布局，不作为当前可运行入口；当前R复现使用[本轮完整入口](../R/reproduce_all_figures.R)。
