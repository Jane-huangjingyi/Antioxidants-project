# Phase 3D — Vitamins / Vitamin-like Antioxidants Class-Specific Ranking

## 1. Question

本阶段回答两个相互独立的问题：正常膳食来源的 vitamin C defined forms 在可比水相化学体系中的 capacity 如何；tocopherols/tocotrienols 在可比 lipid-chain-breaking kinetic construct 中的相对表现如何。营养学上的 “vitamins” 不是统一的 redox mechanism，因此不建立 Vitamins 总数值榜。

## 2. Candidate universe and eligibility lock

Phase 2 master 中共有 10 个 vitamin candidates：aqueous subpanel 2 个，即 L-ascorbic acid 与 dehydroascorbic acid；lipid-phase subpanel 8 个，即 α/β/γ/δ tocopherols 与对应四个 tocotrienols。L-ascorbic acid 和八个天然 dietary vitamin E vitamers 可进入相应证据审计。Dehydroascorbic acid 是氧化型 vitamer，没有与 L-ascorbic acid 可比的 primary capacity record，也不能用 ascorbate 数值替代，因此保留为 hold/context node。natural RRR/R-configured forms、all-rac synthetic forms 与 generic “vitamin E” records 不静默合并。

## 3. Vitamin C construct audit and decision

H-ORAC-FL 有两条可追溯 L-ascorbic acid B1 records：0.95 与 0.53 mol TE/mol，median=0.74 mol TE/mol。两篇研究均使用 AAPH、fluorescein、Trolox、pH 7.4 和 37 °C，但 duration、probe concentration 与处理细节不同，因此只达到 exploratory B1。Reducing capacity 与 direct radical kinetics 对 ascorbate chemistry 有意义，但当前没有第二个 aqueous dietary form 可形成同一 metric 下的候选比较，而且不同 reducing/radical endpoints 缺少统一尺度。故本阶段选择 H-ORAC-FL 为 provisional primary construct；antioxidant regeneration 单独成 profile，不参与 capacity rank。

Vitamin C 输出为 **all eligible / Top available 1**。由于只有 L-ascorbic acid 一个 eligible candidate，within-subpanel percentile 为 `NA`，状态为 `single eligible candidate / percentile not informative`，不得机械显示 100%。该值表示 aqueous AAPH–fluorescein chemical capacity，不表示人体疗效。

## 4. Vitamin E construct audit and decision

审计比较了 L-ORAC-FL、lipid-peroxidation inhibition、direct chain-breaking kinetics、liposome/membrane 与 LDL systems。研究者确认以 **vitamer-specific peroxyl-radical chain-breaking rate constant `k_inh`** 为 primary construct，采用 homogeneous organic autoxidation environment；L-ORAC 作为 secondary standardized profile。理由是 `k_inh` 直接对应 H-atom transfer chain termination、单位明确，经典研究覆盖 α/β/γ/δ tocopherols；Yoshida 等在同一实验框架中进一步显示对应 tocopherol/tocotrienol homologues 具有相同 radical reactivity。膜、micelle、LDL 和 L-ORAC 仍有更高 biological/matrix relevance，但 partition、initiator、regeneration 与 metal context 使数值不能跨环境 pooled。

## 5. Vitamin E Top available 8

Primary values 为 α 3.2×10^6、γ 1.4×10^6、β 1.3×10^6、δ 0.44×10^6 M^-1 s^-1；对应 tocopherol 与 tocotrienol homologues 在当前 exploratory framework 中并列。排序采用并列名次：α forms rank 1，γ forms rank 3，β forms rank 5，δ forms rank 7。八个候选目前均为 Low confidence / Fragile，因为每个 vitamer 的 eligible kinetic evidence chain 仍集中在少量经典研究，且 tocotrienol 数值依赖 corresponding-homologue equivalence。此榜是 chemical chain-breaking kinetics，不是体内 vitamin E activity、吸收或临床价值。

L-ORAC secondary profile 可追溯到 Huang 等 2002：α-tocopherol 0.50、γ-tocopherol 0.74、δ-tocopherol 1.36 mol TE/mol；generic tocotrienols 0.91 不能映射到四个独立 tocotrienol candidates。这一顺序与 `k_inh` 不同，正说明 assay construct 会改变观察顺序，不能合并为 composite score。

## 6. Parent-class overview, confidence and stability

`Vitamins_ParentClass_Overview_v1.0.csv` 只并列展示两个 subpanels。Vitamin C raw H-ORAC 与 Vitamin E raw `k_inh` 位于独立 facets/columns，不共享 raw axis。Vitamin E percentile 仅在 N=8 lipid-phase subpanel 中计算；Vitamin C percentile 为 NA；不存在 parent-class percentile 或 overall vitamin rank。

## 7. Antioxidant regeneration and prooxidant context

Ascorbate–tocopheroxyl regeneration 作为独立 mechanism profile 保存，不改变任一 primary rank。Vitamin C 在 redox-active Fe/Cu 与高局部浓度环境中可能促进金属循环；Vitamin E 的净效应依赖 tocopheroxyl radical 是否被 ascorbate/ubiquinol 等还原。Yoshida 等还观察到 α-tocopherol 与 α-tocotrienol在 Cu(II)/methyl-linoleate SDS micelles 中的 prooxidant response。上述条件是 translation/safety context，不是早期自动排除条件。

## 8. Global schema stress test II — same parent class, different constructs

Global schema 可以容纳同一 parent class 内的不同 constructs，但必须增加 `analysis_subpanel`。三层结构推荐为 `parent_class → analysis_panel → analysis_subpanel`；所有 rank、rankable N 与 percentile 均以最小的 mechanistically coherent ranking subpanel 为分母。研究者已经确认不计算 Vitamins parent-class percentile。Vitamin C singleton 使用 NA，而不是 100%；Vitamin E 按八个 vitamers 计算。该规则也适用于未来任何同一营养类别中存在不同 phase/mechanism 的情况。

## 9. Major gaps and interpretation limits

当前 Vitamin E Tier A=0，tocotrienol exact kinetic constants 的原始全文数值需要第二研究者复核。天然 stereochemistry 与 synthetic all-rac 文献必须继续分开。H-ORAC 与 `k_inh` 均为 chemical constructs；它们不回答人体 exposure、bioavailability、selective α-tocopherol transport、disease prevention 或 clinical efficacy。Dehydroascorbic acid 缺少可比数值不等于没有营养或 redox relevance。

## 10. Next step

完成 second-review 后，可选择 Organosulfur compounds 作为下一类，以测试 causal KEAP1/NRF2 与 thiol-reactivity construct；本阶段不执行 Organosulfur ranking、target mapping、experimental panel 或 global composite score。

## HUMAN REVIEW REQUIRED — VITAMER IDENTITY

| compound | reported form | identity issue | possible mapping | ranking impact | recommendation |
|---|---|---|---|---|---|
| α/β/γ/δ-tocopherols | natural or unspecified vitamin E | RRR versus all-rac may be unclear | only explicitly natural form maps to candidate | can add/remove records | hold unspecified/synthetic records |
| α/β/γ/δ-tocotrienols | natural R form or generic tocotrienols | generic mixture cannot resolve vitamer | no automatic mapping | affects all four ranks | require vitamer-resolved source |
| Dehydroascorbic acid | oxidized vitamin C | not equivalent to L-ascorbic acid | separate context node | excluded from capacity ranking | retain hold; never impute ascorbate value |

## Sync to ChatGPT

A. Total vitamin universe N=10；B. Vitamin C subpanel N=2；C. Vitamin E subpanel N=8；D. ranking eligible=9，dehydroascorbic acid hold；E. Vitamin C primary construct=H-ORAC-FL；F. Vitamin E primary construct=peroxyl-radical chain-breaking `k_inh`；G. primary environments=aqueous AAPH–fluorescein and homogeneous organic autoxidation；H. Vitamin C 输出 all eligible 1，median 0.74 mol TE/mol，percentile NA；I. Vitamin E 输出 Top available 8 with tied homolog ranks；J. confidence=Vitamin C Moderate 1，Vitamin E Low 8；K. stability=Moderately stable 1，Fragile 8；L. natural/synthetic/generic vitamin E identity remains a second-review gate；M. regeneration profile is retained separately；N. Fe/Cu and tocopheroxyl contexts are recorded without automatic exclusion；O. Global schema v0.3 now includes analysis_subpanel and subpanel-level percentile；P. pending items are full-text kinetic verification, vitamer stereochemistry, and local Zotero import；Q. recommended next class=Organosulfur compounds.
