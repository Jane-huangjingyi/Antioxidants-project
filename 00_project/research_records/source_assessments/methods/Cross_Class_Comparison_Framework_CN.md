# Cross-class Comparison Framework（v1.0）

跨类别比较不产生统一 antioxidant score。原因是各类别的 primary construct 不同：H-ORAC 衡量 AAPH/peroxyl-radical 条件下的 kinetic chain-breaking；tocopherol 主要在脂相链终止；carotenoid 需要 singlet-oxygen/lipid-phase 测量；organosulfur 主要通过 electrophile/thiol/NRF2 网络；矿物质是酶辅因子且具有状态依赖和促氧化风险。把这些数值 z-score、平均或相乘会消除原始含义。

正式 cross-class profile 采用矩阵、heatmap、radar 或 alluvial，分别展示：dietary exposure；direct chemical antioxidant activity；endogenous antioxidant-defense regulation；lipid-phase activity；singlet-oxygen activity；metal interaction；NRF2/GSH/GPX；SOD/CAT；NOX/mitochondrial ROS；ferroptosis/lipid oxidation；human intervention evidence；PK/bioavailability；direct-target evidence；experimental tractability；safety/prooxidant context。每个 cell 保存 `Strong/Moderate/Limited/Predictive/Not reviewed/No eligible evidence`，其中 `Not reviewed` 不能编码为 0。

比较顺序是：先在各类内部完成 Top-N，再把类内代表映射到同一 profile schema；随后以 µmol/day 和可达到的 systemic exposure 检查实验剂量现实性，优先选择暴露在约 100 倍窗口内的代表。超出窗口但具有不可替代机制的因子进入 exceptional representative layer。当前 `Antioxidant_Panel_Master.csv` 仅是 **Cross-Class Pilot Panel v1.0**，用于测试 taxonomy、exposure、mechanism matrix 和 visualization，不是最终 20 种，也不赋予跨类名次。

进入最终 experimental representative panel 的条件是：类别覆盖充分、身份明确、class-specific ranking 已执行、暴露值有可追溯人口/情境、核心机制至少有独立证据、关键 assay risk 可解释、安全/促氧化情境已记录。最终 panel 与 target mapping shortlist 是两种输出：前者强调跨类代表性和可实验剂量，后者还要求 target evidence 与实验 tractability。

