# Versioning and Audit Rules

Protocol 使用 `vMAJOR.MINOR`：科学构念、tier门槛或范围变化升MAJOR；澄清和兼容补丁升MINOR。Ranking 使用 `ranking_vMAJOR.MINOR_YYYYMMDD`：eligibility/aggregation规则变化升MAJOR；新增合格记录升MINOR。Record 数据集和 shortlist 各自独立版本，不继承文件修改时间作为版本。

禁止 silent overwrite。发布新文件前把旧版复制到 `archive/<artifact>/<version>/`，并保持只读。Changelog 必须列出新增/删除记录、旧/新数值、旧/新名次、B1计数、原因、来源和复核者。Excluded records 保留在exclusion log，raw values永不删除或被标准化值覆盖。所有derived values必须能由冻结record文件和脚本重算。日期采用ISO 8601；人员使用固定 initials，同时在组内受控人员表映射全名。任何 rank-changing correction 要求两人签字；脚本运行记录命令、Python版本、输入文件名/哈希、输出和时间。
