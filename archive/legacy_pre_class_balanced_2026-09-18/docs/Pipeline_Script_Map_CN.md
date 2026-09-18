# Pipeline Script Map

| pipeline step | manual task | script file | input file | output file | editable parameters | expected runtime | QC output | manual review required |
|---|---|---|---|---|---|---|---|---|
| Step 0 scope | 冻结问题 | manual only | protocol | scope statement | none | 30–60 min | scope签字 | yes |
| Step 1 candidate | 食物与结构核对 | scripts/fetch_h_orac_pubchem.py | 脚本内候选名 | data/pubchem_h_orac_phenolics.json | query names | 数分钟，受网络影响 | error字段 | yes |
| Step 2 search | 检索及追原文 | manual only | candidate universe | search log | search dates/queries | 每候选30–90 min | 检索日志 | yes |
| Steps 3–8 | assay、身份、抽取、换算、tier、独立性 | manual only | 原文全文 | extraction/exclusion records | rubric | 每篇20–60 min | 双人checklist | yes |
| Pilot | 早期pilot重建 | scripts/build_orac_pilot.py | 脚本内数据和PubChem JSON | pilot CSV/figures/docs | embedded records | <1 min | count/figure | yes |
| Exploratory | B1/B2探索输出 | scripts/build_orac_exploratory.py | pilot CSV | exploratory CSV/figures | embedded adjudication | <1 min | count/figure | yes |
| Steps 9–11 | 候选聚合和provisional榜 | scripts/build_h_orac_top20.py | PubChem JSON、pilot reclassification | candidate/ranking CSV及图 | embedded candidate/source records | <1 min | candidate/eligible counts | yes；脚本非通用 |
| Steps 12–14 | consolidation、稳定性、shortlist | scripts/build_top20_consolidation.py | provisional data、candidate universe | consolidation records、before/after、shortlist及图 | embedded added records/rules | <1 min | records/top20/readiness counts | yes；脚本非通用 |
| SOP文档 | 生成本套文档和模板 | scripts/build_master_pipeline_docs.py | 冻结规则 | docs/templates/checklists/flowchart | SOP文本 | <1 min | 文件清单 | yes |

现有构建脚本含硬编码研究记录和候选定义，适合复现对应版本，不应被当作自动文献抽取或通用排名引擎。运行前必须备份输出，禁止覆盖冻结版本。
