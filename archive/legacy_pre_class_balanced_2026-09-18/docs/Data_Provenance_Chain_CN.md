# Data Provenance Chain

逆向链固定为：rank → compound summary → eligible records → independent_experiment_id → original paper → DOI/PMID → exact table/page/supplement → original numerical value/unit → molecular weight source与conversion formula → standardized mol TE/mol → compound median → confidence/rank。

真实示例 quercetin：排名文件中的 quercetin 中位数必须回到 `Top20_Evidence_Consolidation_Records.csv` 中的多个 B1 行；每行包含 experiment ID、study、DOI/PMID、exact location、原始单位、换算状态和理由。例如 Ou 2001（DOI 10.1021/jf010586o，Table 4）直接报告7.28 mol TE/mol，无MW换算；Carvalho 2023（DOI 10.3390/antiox12020505，Table 3）报告16.62并注明quercetin dihydrate form风险；新增独立研究分别保留自己的experiment ID。去重后的值排序并取median，记录数决定confidence。审计者不能从图反推数值，必须沿CSV回到原文。

最小provenance要求：DOI或PMID至少一个；精确位置；原值和单位；身份form；experiment ID；换算公式与复核；tier理由。缺一项即在gap字段说明，不得用“已核对”笼统替代。
