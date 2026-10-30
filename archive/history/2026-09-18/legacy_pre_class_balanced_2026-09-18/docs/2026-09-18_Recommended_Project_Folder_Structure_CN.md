# 推荐项目目录结构

```text
project/
  README_H_ORAC_PIPELINE.md
  docs/          # protocol、MASTER、SOP、教程、审计说明
  config/        # rubric、字段字典、固定参数
  raw/           # 原始下载数据和只读原文索引
  extracted/     # 人工逐记录抽取；未聚合
  processed/     # 标准化、去重、聚合中间表
  data/          # 冻结发布的数据表
  figures/       # 可由processed/data重建的图
  scripts/       # 有版本的可执行脚本
  templates/     # 空白人工模板
  checklists/    # 可打印QC表
  logs/          # search、exclusion、run和review日志
  references/    # BibTeX/RIS、Zotero导出及文献清单
  handoff/       # 阶段同步和上传清单
  archive/       # 旧版只读快照；禁止删除
```

`raw/`永不被脚本改写；`extracted/`保留原值；`processed/`允许重建；`data/`只有通过复核的冻结版本；`figures/`不得成为数据源。每次发布同时归档输入、脚本版本、run log和change log。
