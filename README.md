# Antioxidant Functional Factor Atlas

本项目当前已完成 **Phase 3A：Polyphenols–Flavonoids provisional Top20 v1.0**。该结果仅比较正常膳食来源、身份锁定且具有 A/B1 级历史 H-ORAC-FL 数据的黄酮单体；它不是全类别排名、人体功效排名或靶点优先级。科学口径与阶段边界以 `Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md` 为准；阶段入口见 `docs/PROJECT_STAGE_INDEX_CN.md`，本阶段完整报告见 `docs/Phase3A_Flavonoid_Top20_Report_CN.md`。

Phase 3A 锁定 59 个黄酮候选，57 个可进入文献排名检索、2 个暂缓；证据主表含 94 条记录，其中 Tier A=0、B1=53、B2=5、C=7、X=29。25 个候选至少有一条 A/B1，足以形成 provisional Top20；前五为 epicatechin、catechin、gallocatechin、apigenin 和 isorhamnetin。Top20 中 11 个仍是单研究估计，且一项 2019 年同实验室比较研究贡献了大量覆盖，因此进入 Phase 3B 前仍需第二研究者复核身份、换算、独立实验和食物来源。

Phase 3A 的四张核心数据表是：

- `data/Flavonoid_Phase3_Eligibility_Lock.csv`：59 个黄酮候选的 Phase 3A 身份与范围锁定。
- `data/Flavonoid_H_ORAC_Evidence_Master.csv`：一条独立实验一行的完整证据与换算来源链。
- `data/Polyphenols_Flavonoids_Top20_v1.0.csv`：按 compound-level median H-ORAC 排序的 provisional Top20。
- `data/Flavonoid_Ranking_Coverage.csv`：各 subclass 的候选数、可排名数、缺失数与 Top20 覆盖。

正式图由 `R/plot_antioxidant_atlas.R` 从活动 CSV 重新生成。脚本把项目内 `R/library` 加入 `.libPaths()`，并在开头集中提供尺寸、DPI、字体、配色、标签和 panel 顺序参数。在项目根目录用 PowerShell 运行：

```powershell
& 'C:\Program Files\R\R-4.5.3\bin\Rscript.exe' R\plot_antioxidant_atlas.R
```

运行后除 Atlas 总览图外，应得到 `Flavonoid_Top20_H_ORAC.png`、证据置信度图、subclass coverage 图和 evidence-depth-versus-ORAC 图。下一步为 Phase 3B phenolic acids / conjugates 的类别内流程；在多类结果完成并审核前不生成 Global Top Overview，也不进入 target mapping。任何修订均须保留旧版和变更记录；历史文件及构建期辅助脚本保存在 `archive/`。
