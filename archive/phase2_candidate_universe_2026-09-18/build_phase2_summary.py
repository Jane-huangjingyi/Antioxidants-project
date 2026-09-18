import csv, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent; DATA=ROOT/'data'; DOC=ROOT/'docs'
with open(DATA/'Antioxidant_Class_Candidate_Master.csv',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
with open(DATA/'Antioxidant_Candidate_Exclusions.csv',encoding='utf-8-sig') as f: exclusions=list(csv.DictReader(f))

defs={
('Polyphenols','Polyphenols–Flavonoids'):'C6–C3–C6 flavonoids including flavan-3-ols, flavonols, flavones, flavanones, anthocyanins and isoflavones.',
('Polyphenols','Polyphenols–Phenolic acids / conjugates'):'Hydroxybenzoic/hydroxycinnamic acids and structurally defined dietary conjugates.',
('Polyphenols','Polyphenols–Stilbenes / lignans'):'Structurally defined dietary stilbenes and parent plant lignans; mammalian enterolignans excluded.',
('Vitamins / vitamin-like antioxidants','Vitamins / vitamin-like'):'Defined dietary vitamin C and vitamin E family compounds; water- and lipid-phase subclasses retained.',
('Carotenoids','Carotenoids'):'Defined carotenes and xanthophylls; cis/trans forms treated separately when specified.',
('Organosulfur compounds','Organosulfur compounds'):'Defined crucifer/allium sulfur compounds with parent or processing-generated status recorded.',
('Betalains / nitrogen-containing phytochemicals','Betalains / nitrogen-containing'):'Defined dietary betalain pigments and selected food-derived nitrogen-containing compounds.',
('Other food-derived redox-active phytochemicals','Other food-derived redox-active phytochemicals'):'Strictly gated culinary curcuminoids, capsaicinoids, spice phenolics, olive phenolics and dietary quinones.',
('Antioxidant-related micronutrients / mineral cofactors','Antioxidant-related micronutrients / mineral cofactors'):'Nutrient cofactors linked to redox enzymes or oxidative/prooxidant context; no small-molecule capacity ranking.'}
rel=[]
for (parent,panel),group in __import__('itertools').groupby(sorted(rows,key=lambda r:(r['parent_class'],r['analysis_panel'],r['subclass'])),key=lambda r:(r['parent_class'],r['analysis_panel'])):
 g=list(group); by=collections.defaultdict(list)
 for r in g: by[r['subclass']].append(r['compound'])
 for sub,names in by.items(): rel.append(dict(parent_class=parent,analysis_panel=panel,subclass=sub,definition=defs[(parent,panel)],example_compounds='; '.join(names[:5]),relationship_note='Subclass is nested under analysis panel; compounds are universe candidates, not ranked.'))
with open(DATA/'Antioxidant_Taxonomy_Relationships.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['parent_class','analysis_panel','subclass','definition','example_compounds','relationship_note']);w.writeheader();w.writerows(rel)

parent=collections.Counter(r['parent_class'] for r in rows); panel=collections.Counter(r['analysis_panel'] for r in rows); subclass=collections.Counter((r['analysis_panel'],r['subclass']) for r in rows)
elig=collections.Counter(r['candidate_eligible'] for r in rows)
def md_table(counter,h1,h2):
 return '\n'.join([f'| {k if not isinstance(k,tuple) else " / ".join(k)} | {v} |' for k,v in counter.most_common()])
pan_ge=[k for k,v in panel.items() if v>=20]; pan_lt=[k for k,v in panel.items() if v<20]
excluded_reason=collections.Counter(r['exclusion_reason'] for r in exclusions)
text=f'''# Phase 2 Candidate Universe Summary（CN）

## 1. Scope and method

本轮只依据 chemical identity、normal dietary occurrence、structural definition、class membership 和 normal dietary relevance 生成 universe。ORAC、DPPH、ABTS、FRAP、CUPRAC、NRF2 potency、target count、论文数和期刊影响因子均未参与纳入。所有历史 rank 均从 candidate master 中移除，仅用 `legacy_note` 指向归档。

## 2. Coverage results

共生成 **{len(rows)}** 个候选：**{elig['yes']} eligible**、**{elig['unresolved']} unresolved**；另保留 **{len(exclusions)}** 个明确排除项。PubChem 批量身份解析后仍有 {sum(not r['PubChem_CID'] for r in rows)} 个条目没有唯一 CID/InChIKey，均保持 unresolved，不允许进入 Phase 3 排名。

### Parent class counts

| Parent class | N |
|---|---:|
{md_table(parent,'Parent','N')}

### Analysis panel counts

| Analysis panel | N |
|---|---:|
{md_table(panel,'Panel','N')}

### Subclass counts

| Analysis panel / subclass | N |
|---|---:|
{md_table(subclass,'Subclass','N')}

## 3. Coverage audit

候选丰富的 panels 是 {', '.join(pan_ge)}，均达到或超过 20 个候选，可以在 Phase 3 完成 food-occurrence second review 后尝试 Top20。候选不足 20 的 panels 是 {', '.join(pan_lt)}；这些类别应采用 Top10 或 all eligible，不能为凑 Top20 加入边缘天然产物。Flavonoids、phenolic acids 和 other phytochemicals 的 universe 最完整；vitamins、betalains、minerals 和 stilbenes/lignans 的化学空间本来较小。Carotenoids 当前 19 个，接近但未达到 20，应优先完善真实膳食 cis/trans isomer occurrence，而不是机械补数。

身份风险最高的是 anthocyanin/betalain 的离子/盐/立体形式、caffeoylquinic positional isomers、carotenoid cis/trans forms、tocopherol/tocotrienol stereochemistry，以及 allium compounds 的 parent-versus-processing-generated 状态。Food occurrence 较薄弱的是 betalains、dietary quinones、部分海藻 carotenoids、ajoene、S-allylmercaptocysteine、podophyllotoxin 和少见 flavones；这些已标为 unresolved。食物来源证据最稳定的是常见 flavonoids、phenolic acids、vitamins、主流 carotenoids 和必需矿物质。

明确排除最多的类型是 mixture/aggregate variables、human/microbial metabolites、endogenous-only antioxidants 以及 supplement/medicinal dominant materials。主要排除原因包括 `total polyphenols/total carotenoids` 无唯一结构、extract composition 不固定、enterodiol/enterolactone 并非 dietary parent、glutathione/uric acid 主要为内源性，以及 NAC/baicalin/silymarin 等不满足正常膳食 gate。

## 4. Bias assessment

本轮没有使用 performance 或 publication count，因此没有把“研究多”直接写入 eligibility；但候选清单仍可能受已有 food databases 和英文文献的 popularity bias 影响。明显 geographic bias 包括：Phenol-Explorer 偏欧洲饮食，USDA/FoodData Central 偏北美食物，茶/大豆/香辛料数据库覆盖受亚洲地区研究影响，betalain、热带水果、海藻和地方香辛料可能被低覆盖。Phase 3 前的第二研究者审阅应纳入亚洲、拉丁美洲、非洲和地中海权威食物组成来源。

## 5. Phase 3 readiness

最容易开始 ranking 的顺序是：Flavonoids → Phenolic acids/conjugates，因为已有 H-ORAC SOP、record-level 数据和 tiering；随后是 vitamins（按水/脂相拆 construct）和 carotenoids（先冻结 singlet-oxygen/lipid assay QC）。Stilbenes/lignans 候选少，适合 Top10/all eligible。Organosulfur 应先冻结 causal KEAP1/NRF2/thiol-redox evidence rubric。Betalains需先处理光学干扰和 food occurrence。Other phytochemicals必须再次执行严格 dietary gate。Minerals不做 capacity ranking，仅构建 cofactor/deficiency/excess profile。

## 6. What is not completed

本轮未抽取 primary metric、未计算 rank/score/percentile、未生成 Top-N、未形成 Global Top Overview、未完成 cross-class comparability result、未冻结实验 panel，也未做 target mapping。Candidate master 中 `eligible=yes` 仅表示通过首轮身份与膳食存在 gate，仍需 candidate-level food reference 二次核验。

## Sync to ChatGPT

**A. Total：**{len(rows)} candidates。**B. Parent counts：**{'; '.join(f'{k}={v}' for k,v in parent.items())}。**C. Panel counts：**{'; '.join(f'{k}={v}' for k,v in panel.items())}。**D. Subclasses：**共 {len(subclass)} 个 subclass cells。**E. Excluded：**{len(exclusions)}。**F. Unresolved：**{elig['unresolved']}。**G. Panels ≥20：**{'; '.join(pan_ge)}。**H. Panels <20：**{'; '.join(pan_lt)}。**I. Bias risks：**food-database geography、known-compound familiarity、rare-food undercoverage。**J. Identity risks：**pigment ionic forms、glycosides、positional isomers、carotenoid stereoisomers、vitamin E stereochemistry。**K. Food gaps：**betalains、rare quinones、seaweed carotenoids、processing-generated allium compounds。**L. Recommended Phase 3 order：**Flavonoids → Phenolic acids/conjugates → Vitamins → Carotenoids → Stilbenes/lignans → Organosulfur → Betalains → Other phytochemicals；minerals 使用独立 cofactor framework。
'''
(DOC/'Phase2_Candidate_Universe_Summary_CN.md').write_text(text,encoding='utf-8')
print({'relationships':len(rel),'summary':str(DOC/'Phase2_Candidate_Universe_Summary_CN.md')})
