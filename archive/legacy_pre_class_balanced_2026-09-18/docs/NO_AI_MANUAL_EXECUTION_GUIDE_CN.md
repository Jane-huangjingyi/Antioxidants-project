# 无 AI 人工执行指南

假设只有浏览器、PubMed/Google Scholar、Excel，R/Python可选。Day 1上午阅读README、MASTER、SOP01–04，复制五个空白模板并冻结scope；下午建立候选表，逐项核对CID/InChIKey、form、food occurrence。Day 2开始按候选运行四个检索式，每次把数据库、日期、原式、命中和筛选数写入search log；用review发现原文，但不抄review数值。后续每天以“一个候选完成一个闭环”为单位：全文→assay checklist→身份QC→一实验一行→换算→tier→独立性。

Excel建议工作簿含五张表：Candidates、Search_Log、Records、Exclusions、Compound_Summary；Change_Log单独保存并版本化。每录入一个数值立即记录exact page/table，不要留到最后。可以程序化的内容：单位算术、字段完整性、分组n/median/range/IQR、排序、制图和重复ID报警。必须人工判断：probe、HORAC/ORAC差异、H/L arm、化学form、光学干扰、原始/二手来源、独立实验和tier。

停止点：身份无法唯一确定时停止换算；probe或arm不明时判X并停止排名使用；只有图无数字时进入B2/exclusion；完成一个候选检索且所有线索有去向后才可写“未找到”。必须请第二人复核的时点是身份锁定、tier终判、原始数值、每个换算、experiment ID及任何会改变名次的修正。完成所有候选、生成summary和before/after、填完exclusion/change log并得到双签后，才可冻结shortlist。

若不使用R/Python，Excel公式示例：标准化值=`original_umol_per_g*MW/1000000`；中位数=`MEDIAN(FILTER(values,compound=current))`；计数=`COUNTIFS(compound,current,tier,"B1")+COUNTIFS(compound,current,tier,"A")`。公式列锁定后由第二人抽查至少10%和全部rank-changing行。
