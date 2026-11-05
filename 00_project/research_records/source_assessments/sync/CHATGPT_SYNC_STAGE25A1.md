# 可直接复制给 ChatGPT 的 Stage 25A.1 摘要

Stage25A.1已完成pre-Stage25B QC和全项目科学功能重构。Stage25A primary metric正式名称为`metadata_deduplicated_original_publication_N` / Metadata-deduplicated antioxidant/redox original-publication count，中文为“元数据去重后的抗氧化/redox原始研究论文数”，解释为research-evidence density proxy。legacy字段`antioxidant_independent_publication_N`仅为backward compatibility，不得解释为true independent-study count。

OpenAlex仍为sole primary citation source；前置audit与全量class/年代/identity strata均通过95%。Top50 targeted metadata QC未发现已确认的rank-changing contamination，因此provisional Top50 membership保持不变。研究者已将Thymoquinone、Baicalein、Chrysin、Plumbagin的candidate-universe status全部裁决为INCLUDE；严格依据既有records和rubric，四者H-ORAC eligibility均为Conditional并进入retrieval。当前分流为Ready 31、Conditional 16、Not suitable 3、human-review hold 0；actual retrieval-eligible N由43更新为47，不用第51名补位。same-study/full-text endpoint仍是未完全解决的限制。

两张异常图已修复。底层数据正确；错误是log axis后的numeric nudge导致指数级轴扩张。旧图已归档，新canonical图由modular R生成。全项目362个初始文件完成inventory和ACTIVE_CANONICAL/ACTIVE_SUPPORTING/SUPERSEDED/HISTORICAL_ONLY分类，迁移记录在`PROJECT_FILE_MIGRATION_MAP.csv`。active项目按candidate_universe、class_specific_antioxidant、literature_screening、metal_and_micronutrients、methods/qc、supervisor和sync组织；Stage timeline仍完整保留。

当前active aqueous canonical figures=29，R-reproducible=29，failed=0，manual-edit dependency=0。长脚本已移入archive，`R/render_all_active_figures.R`是薄总入口。Stage25B方法学输入已READY，但本轮未执行Stage25B检索、未生成ORAC Top20；启动必须等待研究者下一条明确指令。
