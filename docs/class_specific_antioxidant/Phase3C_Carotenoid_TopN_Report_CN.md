# Phase 3C — Carotenoids Top-N report

本阶段从 Phase 2 master 锁定 19 个 carotenoid candidates，17 个暂可进入证据审计，astaxanthin 与 fucoxanthin 因正常膳食 gate 未冻结而 hold。类胡萝卜素的 primary construct 冻结为 direct singlet-oxygen physical quenching rate constant `kq`。H-ORAC-FL 与其疏水性、长共轭多烯及经典 ^1O2 physical quenching chemistry 不匹配，因此不作为本类主指标。

环境覆盖审计显示，homogeneous organic-solvent direct `kq` 可支持 9 个 ranking-eligible compounds；DPPC liposome/micelle 数据仅覆盖少数候选并存在 xanthophyll aggregation、膜定位和 nonlinear response，尚不能产生同等覆盖的第二套排名。因此当前采用 organic-solvent `kq` 作为 provisional primary environment，明确解释为 class-specific chemical quenching construct，不代表 biological membrane efficacy。不同有机溶剂记录只有在 B1 条件下才在 compound 内聚合；跨 organic/micelle/liposome 的数值不合并。

当前输出为 **Top available 9**，未达到 10 个可比候选，故不称 Top10。按 median `kq` 排列为：1. all-trans-Lycopene, 2. Canthaxanthin, 3. alpha-Carotene, 4. all-trans-beta-Carotene, 5. Zeaxanthin, 6. 9-cis-beta-Carotene, 7. Lutein, 8. Phytofluene, 9. Phytoene。只有 lycopene、all-trans-beta-carotene、alpha-carotene、zeaxanthin 和 lutein 有两条 B1；其余为 single-study。Tier A=0，B1=15。该列表展示的是历史有机溶剂中报告的 quenching kinetics；它不说明膳食暴露、人体效果或跨类别“最强抗氧化剂”。

cis/trans QC 仍是关键限制。只有 9-cis-beta-carotene 获得 form-resolved record；generic beta-carotene 或 lycopene 记录未映射至 13-cis/9-cis candidates。Phytofluene 虽具有暗态 quenching `kq`，原研究同时报告 UVA 下显著 ^1O2 photosensitization，故不能把其数值解释为净 photoprotection。Carotenoid prooxidant behavior 还取决于氧分压、浓度、radical chemistry 和 matrix。

Secondary lipid profile 保留 Cantrell 等人的 DPPC liposome 研究。Lycopene 与 beta-carotene 在该模型的 `kq` 接近，且明显低于有机溶剂；xanthophylls 更受聚集和定位影响。这一结果说明 environment 是 construct 的组成部分，也支持禁止把 `kq` 与 L-ORAC、lipid-peroxidation endpoint 或摄入量做 composite score。

## HUMAN REVIEW REQUIRED — pause decision

Astaxanthin 与 fucoxanthin 的正常膳食 gate 尚未由第二研究者确认，因此相关 `kq` 不改变当前榜单；generic beta-carotene/lycopene 文献也不得映射到 9-cis/13-cis candidates。organic-solvent 层内部仍含 benzene 与 ethanol/chloroform/water 条件，本版只将其作为 B1 exploratory records；升级为 formal Tier A 或在 cutoff 附近作精细名次解释前，必须完成 full-text、温度、viscosity、isomer 与 aggregation 的双人复核。当前没有第二个达到相当候选覆盖的 primary environment，因此不构成 organic-solvent 与 membrane 两套排名之间的竞争；若膜层覆盖扩展到可排名规模，必须重新暂停并由研究者选择 primary environment。

## Sync to ChatGPT

A. Universe N=19；B. ranking eligible lock=17，实际有 primary A/B1 的候选=9；C. primary construct=direct singlet-oxygen quenching `kq`；D. primary environment=homogeneous organic solvent（provisional，因唯一达到足够覆盖）；E. evidence tiers=A 0、B1 15，其中1条 astaxanthin 因 dietary hold 不进榜；F. 输出 Top available 9；G. confidence 为 Moderate 5、Low 4；H. single-study=4；I. generic cis/trans 记录不映射；J. xanthophyll aggregation 是主要风险；K. direct decay method 的 optical risk 低于颜色终点法，但仍需核对吸收与 sensitizer；L. prooxidant context 已独立记录；M. lipid-phase evidence 只做 profile；N. Global schema 可容纳不同 primary unit 与 percentile，但不能生成 unified score；O. 人工待决包括 astaxanthin/fucoxanthin dietary gate、cis identity 与 full-text second review；P. 推荐下一类为 Vitamins，先拆分 vitamin C aqueous construct 与 vitamin E lipid-phase construct。
