from pathlib import Path
from datetime import date
import json, os, time, urllib.parse, urllib.request
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DOCS=ROOT/'docs'
RETRIEVAL_DATE=date.today().isoformat()
PANEL=[
 ('Quercetin','high density; early and recent; simple aglycone'),
 ('Epicatechin','high density; stereospecific flavan-3-ol'),
 ('Cyanidin 3-O-glucoside','pigment; glycoside; optical-complexity'),
 ('Isoquercitrin','glycoside/aglycone collision risk'),
 ('Caffeic acid','high-density phenolic acid'),
 ('Neochlorogenic acid','positional-isomer complexity'),
 ('trans-Resveratrol','historically famous; stereochemistry'),
 ('Sesamol','lower-density lignan-related phenolic'),
 ('L-Ascorbic acid','vitamin; long publication history'),
 ('Betanin','betalain pigment; optical/pH complexity'),
 ('Indicaxanthin','lower-density betalain'),
 ('Sulforaphane','organosulfur; indirect redox mechanism'),
 ('Allicin','reactive organosulfur; identity/stability complexity'),
 ('S-Allyl-L-cysteine','lower-density organosulfur'),
 ('Hydroxytyrosol','other aqueous phenolic; moderate history'),
 ('Curcumin','famous compound; solubility/tautomer complexity'),
 ('Zingerone','lower-density spice phenolic'),
 ('Juglone','quinone; redox cycling rather than simple capacity'),
]

e=pd.read_csv(DATA/'Aqueous_Antioxidant_Primary_Literature_Evidence.csv')
rows=[]
for compound,design_reason in PANEL:
    g=e[(e.compound==compound)&(e.original_research_yes_no.astype(str).str.lower()=='yes')].copy()
    for _,r in g.iterrows():
        doi=str(r.get('DOI','')).strip()
        pmid=str(r.get('PMID','')).strip()
        if doi.lower() in {'','nan','na','unresolved'}: doi=''
        if pmid.lower() in {'','nan','na','unresolved'}: pmid=''
        if pmid.endswith('.0'): pmid=pmid[:-2]
        key=('doi:'+doi.lower()) if doi else (('pmid:'+pmid) if pmid else 'title:'+str(r.get('paper_title','')).lower())
        rows.append(dict(candidate=compound,analysis_panel=r.get('analysis_panel',''),design_reason=design_reason,paper_key=key,paper_title=r.get('paper_title',''),year=r.get('year',''),DOI=doi,PMID=pmid,evidence_tier=r.get('evidence_tier',''),eligible_stage25a='yes',eligibility_basis='Current curated original antioxidant/redox evidence master; candidate is experimental subject.',retrieval_date=RETRIEVAL_DATE))
audit=pd.DataFrame(rows).drop_duplicates(['candidate','paper_key'])

def openalex_api_key():
    key=os.getenv('OPENALEX_API_KEY','').strip()
    if key or os.name!='nt': return key
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as h:
            return str(winreg.QueryValueEx(h,'OPENALEX_API_KEY')[0]).strip()
    except Exception:
        return ''

def get_json(url):
    headers={'User-Agent':'AntioxidantsProject/Stage25A'}
    key=openalex_api_key()
    if key: headers['Authorization']='Bearer '+key
    req=urllib.request.Request(url,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=30) as resp: return json.load(resp),''
    except Exception as ex: return None,str(ex)

out=[]
for i,r in audit.iterrows():
    doi=r.DOI;pmid=r.PMID
    result=None;err='';match_method='';failure=''
    if doi:
        url='https://api.openalex.org/works/'+urllib.parse.quote('https://doi.org/'+doi,safe='')
        result,err=get_json(url);match_method='DOI'
    if result is None and pmid:
        url='https://api.openalex.org/works/'+urllib.parse.quote('pmid:'+pmid,safe='')
        result,err2=get_json(url);match_method='PMID';err=(err+'; '+err2).strip('; ')
    if not doi and not pmid: failure='missing DOI/PMID'
    elif result is None:
        # Identifier-based title search is diagnostic only; it never upgrades the denominator match.
        q=urllib.parse.quote(str(r.paper_title))
        diagnostic,_=get_json('https://api.openalex.org/works?search='+q+'&per-page=3')
        if diagnostic and diagnostic.get('results'):
            titles=[x.get('display_name','') for x in diagnostic['results']]
            failure='ambiguous match' if len(titles)>1 else 'identifier mismatch'
        else: failure='OpenAlex work not found'
    citation_available=result is not None and isinstance(result.get('cited_by_count'),int)
    if result is not None and not citation_available: failure='work found but citation metadata unavailable'
    out.append({**r.to_dict(),
        'openalex_matched':'yes' if result is not None else 'no',
        'match_method':match_method if result is not None else '',
        'OpenAlex_ID':result.get('id','') if result else '',
        'OpenAlex_title':result.get('display_name','') if result else '',
        'OpenAlex_publication_year':result.get('publication_year','') if result else '',
        'citation_metadata_available':'yes' if citation_available else 'no',
        'OpenAlex_cited_by_count':result.get('cited_by_count','') if citation_available else '',
        'failure_category':failure,
        'api_error':err})
    time.sleep(.08)

res=pd.DataFrame(out)
res.to_csv(DATA/'Stage25A_OpenAlex_Coverage_Audit_Publications.csv',index=False,encoding='utf-8-sig')
unmatched=res[(res.openalex_matched!='yes')|(res.citation_metadata_available!='yes')]
unmatched.to_csv(DATA/'Stage25A_OpenAlex_Unmatched_Publications.csv',index=False,encoding='utf-8-sig')
den=len(res);matched=(res.openalex_matched=='yes').sum();cit=(res.citation_metadata_available=='yes').sum()
mr=matched/den if den else 0;cr=cit/den if den else 0
by_class=res.groupby('analysis_panel').agg(publications=('paper_key','size'),matched=('openalex_matched',lambda x:(x=='yes').sum()),citation_available=('citation_metadata_available',lambda x:(x=='yes').sum())).reset_index()
by_class['matching_rate']=by_class.matched/by_class.publications
by_class['citation_metadata_rate']=by_class.citation_available/by_class.publications
by_class.to_csv(DATA/'Stage25A_OpenAlex_Coverage_Audit_By_Class.csv',index=False,encoding='utf-8-sig')
freeze=(mr>=.95 and cr>=.95 and (by_class.matching_rate>=.95).all() and (by_class.citation_metadata_rate>=.95).all())
status='OpenAlex = sole primary citation source' if freeze else 'HUMAN REVIEW REQUIRED — CITATION SOURCE'
doc=f'''# Stage 25A Citation Source Audit（CN）

## 冻结结论

**{status}**

Audit panel包含{len(PANEL)}个代表性候选与{den}篇已在当前项目中判定为original antioxidant/redox evidence的独立publication units。候选跨越不同aqueous classes、publication density、发表年代与identity complexity；没有只选择高知名度化合物。`DOI/PMID → OpenAlex work matching rate`为 **{mr:.1%}**（{matched}/{den}）；`citation metadata availability rate`为 **{cr:.1%}**（{cit}/{den}）。两项阈值分别要求≥95%，不取平均；class-specific audit也应用同一95%门槛。

## 方法

以Stage 24统一original-literature master中已经判定为candidate-specific antioxidant/redox original research的记录作为audit sampling frame。优先按DOI查询OpenAlex work endpoint，DOI未命中时再按PMID namespaced identifier查询；标题搜索只用于诊断失败原因，不将模糊标题匹配计为identifier match。Citation availability要求work成功匹配且`cited_by_count`为integer。Retrieval date为{RETRIEVAL_DATE}。

OpenAlex适合本项目的理由是identifier lookup可复现、work metadata包含publication year与`cited_by_count`、支持批量API和透明的开放数据模型。主要限制是citation coverage与去重规则仍会随OpenAlex更新，citation count是research attention而非evidence quality。Crossref可补DOI metadata但不是完整citation source；Google Scholar不可稳定批量复现；Semantic Scholar不与OpenAlex citation count混用。

## 失败分类与停止规则

未匹配清单保存在`data/Stage25A_OpenAlex_Unmatched_Publications.csv`，failure category严格使用：`missing DOI/PMID`、`identifier mismatch`、`OpenAlex work not found`、`work found but citation metadata unavailable`、`ambiguous match`。若总指标或任何明显class/年代/identity stratum低于95%，不得开始157候选的正式citation counting，也不得自行切换或混合citation sources。
'''
(DOCS/'Stage25A_Citation_Source_Audit_CN.md').write_text(doc,encoding='utf-8')
print({'panel_candidates':len(PANEL),'eligible_publications':den,'matched':matched,'match_rate':mr,'citation_available':cit,'citation_rate':cr,'freeze':freeze,'status':status})
