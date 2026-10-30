from pathlib import Path
import argparse
from datetime import date
import csv, hashlib, json, math, os, re, statistics, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; CACHE=ROOT/'.tmp_stage25a'; CACHE.mkdir(exist_ok=True)
TODAY=date.today(); CURRENT_YEAR=TODAY.year; RECENT_START=CURRENT_YEAR-4
REDOX_TERMS=['antioxidant','oxidative stress','redox','reactive oxygen species','ros','free radical','radical scavenging','lipid peroxidation','oxidative damage','prooxidant','pro-oxidant']
REVIEW_TYPES={'review','meta-analysis','systematic review'}
EXCLUDED_TYPES={'editorial','comment','letter','conference abstract','news','book chapter','case reports'}
MANUAL_ALIASES={
 'Epigallocatechin gallate':['EGCG'], 'Epicatechin gallate':['ECG'], 'Epigallocatechin':['EGC'],
 'L-Ascorbic acid':['ascorbic acid','vitamin C'], 'Cyanidin 3-O-glucoside':['cyanidin-3-O-glucoside','cyanidin 3-glucoside'],
 'Delphinidin 3-O-glucoside':['delphinidin-3-O-glucoside','delphinidin 3-glucoside'],
 'Kaempferol 3-O-glucoside':['kaempferol-3-O-glucoside'], 'Luteolin 7-O-glucoside':['luteolin-7-O-glucoside'],
 'Apigenin 7-O-glucoside':['apigenin-7-O-glucoside'], 'S-Allyl-L-cysteine':['S-allylcysteine'],
 'trans-Resveratrol':['trans resveratrol'], 'Coenzyme Q10':['ubiquinone-10','ubiquinone 10'],
}

def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()
def year_int(x):
    try:return int(float(x))
    except:return None
def openalex_api_key():
    key=os.getenv('OPENALEX_API_KEY','').strip()
    if key or os.name!='nt': return key
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as h:
            return str(winreg.QueryValueEx(h,'OPENALEX_API_KEY')[0]).strip()
    except Exception:
        return ''
def request_json(url,retries=8):
    headers={'User-Agent':'AntioxidantsProject/Stage25A'}
    if 'api.openalex.org' in url:
        key=openalex_api_key()
        if key: headers['Authorization']='Bearer '+key
    req=urllib.request.Request(url,headers=headers)
    for n in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as resp:return json.load(resp)
        except Exception as exc:
            if n==retries-1: raise
            retry_after=getattr(exc,'headers',{}).get('Retry-After') if getattr(exc,'headers',None) else None
            time.sleep(float(retry_after) if retry_after else 3.0*(n+1))

aq=pd.read_csv(DATA/'Aqueous_Antioxidant_Candidate_Master.csv')
full=pd.read_csv(DATA/'Antioxidant_Class_Candidate_Master.csv')
base=aq.merge(full[['candidate_id','compound','synonym','candidate_eligible','major_known_assay_risk','isomer_status','glycoside_or_aglycone']],on='compound',how='left')
assert len(base)==157 and base.compound.nunique()==157

def search_terms(row):
    terms=[row['compound']]+MANUAL_ALIASES.get(row['compound'],[])
    # Generic abbreviations and class terms are deliberately excluded.
    terms=list(dict.fromkeys(t for t in terms if t and str(t).lower()!='nan'))
    return terms

def epmc_query(terms):
    names=' OR '.join(f'TITLE:"{t}"' for t in terms)
    redox=' OR '.join(f'TITLE_ABS:"{t}"' for t in REDOX_TERMS)
    return f'({names}) AND ({redox})'

def epmc_search(candidate,query):
    cache=CACHE/(re.sub(r'[^A-Za-z0-9]+','_',candidate).strip('_')+'.json')
    if cache.exists(): return json.loads(cache.read_text(encoding='utf-8'))
    results=[];cursor='*'
    while True:
        # Smaller pages avoid intermittent Europe PMC connection resets on broad
        # compound-name queries while preserving the same deterministic query.
        params={'query':query,'format':'json','resultType':'core','pageSize':200,'cursorMark':cursor}
        url='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode(params)
        obj=request_json(url); batch=obj.get('resultList',{}).get('result',[]);results.extend(batch)
        nxt=obj.get('nextCursorMark')
        if not batch or not nxt or nxt==cursor:break
        cursor=nxt;time.sleep(.12)
    cache.write_text(json.dumps(results,ensure_ascii=False),encoding='utf-8')
    return results

def pubtypes(rec):
    x=rec.get('pubTypeList',{})
    vals=x.get('pubType',[]) if isinstance(x,dict) else []
    return [str(v) for v in (vals if isinstance(vals,list) else [vals])]

def has_term(text,terms):
    n=norm(text)
    return any(norm(t) in n for t in terms)

def classify(rec,terms):
    title=rec.get('title') or ''; abstract=rec.get('abstractText') or ''; text=title+' '+abstract
    pts=[x.lower() for x in pubtypes(rec)]
    redox=has_term(text,REDOX_TERMS); identity=has_term(text,terms)
    is_review=any(any(k in p for k in REVIEW_TYPES) for p in pts)
    if is_review:return 'no','review','review'
    if any(any(k in p for k in EXCLUDED_TYPES) for p in pts):return 'no','excluded publication type','excluded'
    if str(rec.get('isRetracted','')).lower()=='true':return 'no','retracted article','excluded'
    if not identity:return 'no','candidate identity absent from title/abstract','excluded'
    if not redox:return 'no','no explicit antioxidant/redox endpoint in title/abstract','excluded'
    low=text.lower()
    if any(k in low for k in ['molecular docking','network pharmacology','in silico']) and not any(k in low for k in ['cell','animal','mouse','rat','assay','experiment','patient','clinical']):
        return 'no','prediction/docking only','excluded'
    if 'extract' in low and not has_term(title,terms):return 'no','food/extract study without candidate-specific title attribution','excluded'
    # Conservative metadata criterion: named candidate and redox endpoint in the same title/abstract record.
    return 'yes','','original'

def domains(rec):
    t=((rec.get('title') or '')+' '+(rec.get('abstractText') or '')).lower(); pts=' '.join(pubtypes(rec)).lower()
    chemical=any(k in t for k in ['dpph','abts','orac','frap','cuprac','radical scaveng','chemical antioxidant','lipid peroxidation','oxidation assay'])
    human=any(k in t+' '+pts for k in ['human','patient','participants','subjects','clinical trial','randomized','cohort','case-control','cross-sectional'])
    animal=any(k in t for k in ['mouse','mice','rat ','rats','murine','rabbit','zebrafish','in vivo']) and not human
    cellular=any(k in t for k in [' cell','cells','cellular','in vitro','culture'])
    mechanism=any(k in t for k in ['nrf2','keap1','nf-kappa','glutathione','redox signaling','nadph oxidase','mitochondrial ros','mechanism'])
    metal=any(k in t for k in ['fenton','chelat','iron','copper','metal-catalyzed'])
    lipid=any(k in t for k in ['lipid peroxidation','ldl oxidation','low-density lipoprotein oxidation'])
    labels=[]
    if chemical:labels.append('chemical antioxidant assay')
    if cellular:labels.append('cellular oxidative stress')
    if animal:labels.append('animal oxidative stress')
    if human:labels.append('human intervention' if any(k in t+' '+pts for k in ['trial','randomized','intervention']) else 'human observational')
    if mechanism:labels.append('redox mechanism')
    if lipid:labels.append('lipid peroxidation')
    if metal:labels.append('metal/redox mechanism')
    if not labels:labels=['other']
    return labels,chemical,cellular,animal,human,mechanism

parser=argparse.ArgumentParser()
parser.add_argument('--fetch-only',action='store_true')
parser.add_argument('--start',type=int,default=0)
parser.add_argument('--end',type=int,default=157)
args=parser.parse_args()
if args.fetch_only:
    for idx,row in base.iloc[args.start:args.end].iterrows():
        terms=search_terms(row);query=epmc_query(terms);found=epmc_search(row.compound,query)
        print(f'[{idx+1:03d}/157] cached {row.compound}: {len(found)} records',flush=True)
    raise SystemExit(0)

provenance=[]; search_log=[]
for idx,row in base.iterrows():
    terms=search_terms(row);query=epmc_query(terms);found=epmc_search(row.compound,query)
    included=reviews=0
    seen=set()
    for rec in found:
        doi=str(rec.get('doi') or '').strip();pmid=str(rec.get('pmid') or '').strip();pmcid=str(rec.get('pmcid') or '').strip()
        key=('doi:'+doi.lower()) if doi else (('pmid:'+pmid) if pmid else 'title:'+norm(rec.get('title','')))
        duplicate=key in seen;seen.add(key)
        include,reason,kind=classify(rec,terms)
        if duplicate:include='no';reason='duplicate indexed record'
        if kind=='review':reviews+=1
        if include=='yes':included+=1
        labels,chemical,cellular,animal,human,mechanism=domains(rec)
        year=year_int(rec.get('pubYear') or rec.get('firstPublicationDate','')[:4])
        group='S25A-'+hashlib.sha1((row.candidate_id+'|'+key).encode()).hexdigest()[:12]
        provenance.append(dict(candidate_id=row.candidate_id,canonical_name=row.compound,**{'class':row.analysis_panel},paper_title=rec.get('title',''),first_author=(rec.get('authorString','').split(',')[0] if rec.get('authorString') else ''),year=year,journal=rec.get('journalTitle',''),DOI=doi,PMID=pmid,PMCID=pmcid,publication_type='; '.join(pubtypes(rec)),antioxidant_redox_relevant='yes' if include=='yes' or kind=='review' else 'no',relevance_domain='; '.join(labels),chemical_assay='yes' if chemical else 'no',cellular='yes' if cellular else 'no',animal='yes' if animal else 'no',human='yes' if human else 'no',redox_mechanism='yes' if mechanism else 'no',independent_study_group_id=group,independence_uncertain='yes' if human else 'no',citation_source='OpenAlex',citation_count='',citation_retrieval_date=TODAY.isoformat(),include_primary_metric=include,exclusion_reason=reason,notes='Europe PMC title/abstract metadata screen; full-text cohort reuse cannot be completely excluded.'))
    search_log.append(dict(candidate_id=row.candidate_id,canonical_name=row.compound,database='Europe PMC',search_date=TODAY.isoformat(),exact_query=query,results_found=len(found),records_screened=len(found),included_original=included,reviews_found=reviews,search_terms='; '.join(terms),excluded_ambiguous_terms='generic class names; aglycone/glycoside substitutions; abbreviations not uniquely identifying the candidate',notes='Uniform title/abstract metadata screen.'))
    print(f'[{idx+1:03d}/157] {row.compound}: {len(found)} screened, {included} included',flush=True)

prov=pd.DataFrame(provenance)
log=pd.DataFrame(search_log)
log.to_csv(DATA/'Stage25A_Literature_Search_Log.csv',index=False,encoding='utf-8-sig')

# OpenAlex is the frozen sole citation source. Batch DOI then PMID identifiers.
included=prov[prov.include_primary_metric=='yes'].copy()
oa={}
def batches(items,n=100):
    for i in range(0,len(items),n):yield items[i:i+n]
dois=sorted(set(x for x in included.DOI.astype(str) if x and x.lower()!='nan'))
def fetch_doi_batch(batch):
    vals='|'.join('https://doi.org/'+x for x in batch)
    params={'filter':'doi:'+vals,'per-page':100,'select':'id,doi,ids,display_name,publication_year,cited_by_count'}
    return request_json('https://api.openalex.org/works?'+urllib.parse.urlencode(params))
doi_batches=list(batches(dois))
with ThreadPoolExecutor(max_workers=8) as pool:
  futures={pool.submit(fetch_doi_batch,b):i for i,b in enumerate(doi_batches,1)}
  for completed,fut in enumerate(as_completed(futures),1):
    obj=fut.result()
    for w in obj.get('results',[]):
        doi=(w.get('doi') or '').replace('https://doi.org/','').lower();
        if doi:oa['doi:'+doi]=w
    if completed % 25 == 0: print(f'OpenAlex DOI batches completed: {completed}/{len(doi_batches)}',flush=True)
pmids=sorted(set(x for x in included.loc[included.DOI.fillna('').eq(''),'PMID'].astype(str) if x and x.lower()!='nan'))
def fetch_pmid_batch(batch):
    params={'filter':'pmid:'+'|'.join(batch),'per-page':100,'select':'id,doi,ids,display_name,publication_year,cited_by_count'}
    return request_json('https://api.openalex.org/works?'+urllib.parse.urlencode(params))
pmid_batches=list(batches(pmids))
with ThreadPoolExecutor(max_workers=8) as pool:
  futures={pool.submit(fetch_pmid_batch,b):i for i,b in enumerate(pmid_batches,1)}
  for completed,fut in enumerate(as_completed(futures),1):
    obj=fut.result()
    for w in obj.get('results',[]):
        pid=str((w.get('ids') or {}).get('pmid','')).split('/')[-1]
        if pid:oa['pmid:'+pid]=w
    if completed % 25 == 0: print(f'OpenAlex PMID batches completed: {completed}/{len(pmid_batches)}',flush=True)

def citation_for(r):
    doi=str(r.DOI or '').lower();pmid=str(r.PMID or '')
    w=oa.get('doi:'+doi) if doi and doi!='nan' else oa.get('pmid:'+pmid)
    return w.get('cited_by_count') if w and isinstance(w.get('cited_by_count'),int) else None
prov['citation_count']=prov.apply(lambda r:citation_for(r) if r.include_primary_metric=='yes' else '',axis=1)
prov.to_csv(DATA/'Stage25A_Publication_Provenance.csv',index=False,encoding='utf-8-sig')

# Preserve every failed bulk citation linkage with a mutually exclusive reason.
unmatched=[]
for _,r in included.iterrows():
    doi=str(r.DOI or '').strip(); pmid=str(r.PMID or '').strip()
    if doi.lower()=='nan': doi=''
    if pmid.lower()=='nan': pmid=''
    if not doi and not pmid:
        category='missing DOI/PMID'
    elif doi and not re.match(r'^10\.\d{4,9}/\S+$',doi,re.I):
        category='identifier mismatch'
    else:
        w=oa.get('doi:'+doi.lower()) if doi else oa.get('pmid:'+pmid)
        if not w: category='OpenAlex work not found'
        elif not isinstance(w.get('cited_by_count'),int): category='work found but citation metadata unavailable'
        else: continue
    unmatched.append(dict(candidate_id=r.candidate_id,canonical_name=r.canonical_name,paper_title=r.paper_title,DOI=doi,PMID=pmid,failure_category=category,citation_source='OpenAlex',retrieval_date=TODAY.isoformat(),notes='No alternative citation source substituted.'))
pd.DataFrame(unmatched,columns=['candidate_id','canonical_name','paper_title','DOI','PMID','failure_category','citation_source','retrieval_date','notes']).to_csv(DATA/'Stage25A_OpenAlex_Bulk_Unmatched_Publications.csv',index=False,encoding='utf-8-sig')

old_orac=pd.read_csv(DATA/'Aqueous_Antioxidant_Primary_Literature_Evidence.csv')
rank=pd.read_csv(DATA/'Supervisor_Aqueous_Class_Ranking_Overview.csv')
summary=[]
for _,r in base.iterrows():
    g=prov[(prov.candidate_id==r.candidate_id)&(prov.include_primary_metric=='yes')].copy()
    reviews=((prov.candidate_id==r.candidate_id)&(prov.exclusion_reason=='review')).sum()
    # Metadata deduplication uses identifier/title keys; uncertain human reuse remains flagged, not silently merged.
    pubN=len(g); independentN=g.independent_study_group_id.nunique()
    citations=pd.to_numeric(g.citation_count,errors='coerce').dropna()
    years=pd.to_numeric(g.year,errors='coerce').dropna().astype(int)
    exposure=sum(max(1,CURRENT_YEAR-y+1) for y in years)
    domain_set=set(x for cell in g.relevance_domain.fillna('') for x in cell.split('; ') if x)
    o=old_orac[(old_orac.compound==r.compound)&(old_orac.rank_eligible=='yes')&old_orac.assay.astype(str).str.contains('ORAC',case=False,na=False)]
    rr=rank[rank.compound==r.compound]
    aqelig=str(r.aqueous_assay_eligible)
    if pd.isna(r.PubChem_CID) or pd.isna(r.InChIKey):
        s25='Insufficient identity'; elig='conditional'; inelig='Frozen candidate lacks a complete PubChem CID/InChIKey identity anchor; HUMAN REVIEW REQUIRED.'
    elif str(r.candidate_eligible).lower() not in {'yes','nan'}:
        s25='Conditional'; elig='conditional'; inelig='Frozen candidate has an unresolved dietary/scope gate; HUMAN REVIEW REQUIRED — CANDIDATE UNIVERSE.'
    elif aqelig=='yes': s25='Ready';elig='yes';inelig=''
    elif aqelig.startswith('conditional'): s25='Conditional';elig='conditional';inelig=aqelig
    else:s25='Not suitable for H-ORAC ranking';elig='no';inelig='Primary redox construct is not interpretable as comparable H-ORAC-FL.'
    summary.append(dict(candidate_id=r.candidate_id,canonical_name=r.compound,**{'class':r.analysis_panel},subclass=r.subclass,PubChem_CID=r.PubChem_CID,InChIKey=r.InChIKey,candidate_status=r.candidate_eligible,search_name=r.compound,synonyms_used='; '.join(search_terms(r)),search_database='Europe PMC',search_query=epmc_query(search_terms(r)),search_date=TODAY.isoformat(),antioxidant_publication_N=pubN,antioxidant_independent_publication_N=independentN,review_N=int(reviews),human_study_N=int((g.human=='yes').sum()),in_vivo_study_N=int((g.animal=='yes').sum()),in_vitro_study_N=int(((g.cellular=='yes')|(g.chemical_assay=='yes')).sum()),recent_5y_publication_N=int((pd.to_numeric(g.year,errors='coerce')>=RECENT_START).sum()),total_citation_N=int(citations.sum()) if len(citations) else 0,median_citation_per_paper=float(citations.median()) if len(citations) else 0,citation_per_year=(float(citations.sum())/exposure if exposure else 0),first_antioxidant_publication_year=int(years.min()) if len(years) else '',latest_antioxidant_publication_year=int(years.max()) if len(years) else '',evidence_domain_N=len(domain_set),existing_H_ORAC_evidence='yes' if len(o) else 'no',existing_H_ORAC_eligible_record_N=len(o),existing_class_specific_rank=(int(rr.within_class_rank.iloc[0]) if len(rr) else ''),existing_class_specific_percentile=(rr.within_class_percentile.iloc[0] if len(rr) else ''),stage25B_ORAC_eligibility=elig,ORAC_ineligibility_reason=inelig,Stage25B_status=s25,identity_QC='anchored to frozen PubChem CID/InChIKey; no silent changes',independence_QC='identifier/title deduplicated; same cohort/experiment reuse remains independence_uncertain pending full-text review' if pubN else 'no included publications',citation_QC=f'OpenAlex citation metadata available for {citations.notna().sum()}/{pubN} included publications',search_completeness='uniform Europe PMC title/abstract screen completed; full-text endpoint and cohort confirmation remain limitations',major_caveat='Publication density measures research maturity, not antioxidant potency, efficacy or quality.',human_review_required='yes' if s25=='Insufficient identity' or str(r.candidate_eligible).lower() not in {'yes','nan'} else 'no'))
master=pd.DataFrame(summary)

def rank_by(cols):
    ascending=([False]*(len(cols)-1)+[True]) if cols[-1]=='canonical_name' else [False]*len(cols)
    order=master.sort_values(cols,ascending=ascending,kind='mergesort').index
    return pd.Series(range(1,len(master)+1),index=order).reindex(master.index)
master['primary_rank']=rank_by(['antioxidant_independent_publication_N','antioxidant_publication_N','recent_5y_publication_N','total_citation_N','median_citation_per_paper','canonical_name'])
master['citation_rank']=rank_by(['total_citation_N','antioxidant_independent_publication_N','canonical_name'])
master['citation_per_year_rank']=rank_by(['citation_per_year','antioxidant_independent_publication_N','canonical_name'])
master['recent_5y_rank']=rank_by(['recent_5y_publication_N','antioxidant_independent_publication_N','canonical_name'])
master['human_evidence_rank']=rank_by(['human_study_N','antioxidant_independent_publication_N','canonical_name'])
for n in [20,30,40,50,60]:master[f'Top{n}_primary']=master.primary_rank.le(n).map({True:'yes',False:'no'})
master=master.sort_values('primary_rank')
master.to_csv(DATA/'Stage25A_Unified_Literature_Screening_Master.csv',index=False,encoding='utf-8-sig')

# Cutoff and class sensitivity.
cut=[]
total_pubs=master.antioxidant_independent_publication_N.sum()
for n in [20,30,40,50,60]:
    p=set(master.nsmallest(n,'primary_rank').candidate_id);c=set(master.nsmallest(n,'citation_rank').candidate_id);cy=set(master.nsmallest(n,'citation_per_year_rank').candidate_id);re=set(master.nsmallest(n,'recent_5y_rank').candidate_id);h=set(master.nsmallest(n,'human_evidence_rank').candidate_id)
    jac=lambda a,b:len(a&b)/len(a|b) if a|b else 0
    cut.append(dict(cutoff_N=n,primary_metric_candidates='; '.join(master.nsmallest(n,'primary_rank').canonical_name),citation_metric_overlap_N=len(p&c),citation_per_year_overlap_N=len(p&cy),recent_5y_overlap_N=len(p&re),human_evidence_overlap_N=len(p&h),Jaccard_primary_vs_citation=jac(p,c),Jaccard_primary_vs_recent=jac(p,re),cumulative_publication_coverage=(master[master.candidate_id.isin(p)].antioxidant_independent_publication_N.sum()/total_pubs if total_pubs else 0),class_count_retained=master[master.candidate_id.isin(p)]['class'].nunique(),notes='No class quota applied.'))
cutdf=pd.DataFrame(cut);cutdf.to_csv(DATA/'Stage25A_Shortlist_Cutoff_Sensitivity.csv',index=False,encoding='utf-8-sig')

cl=[]
for cls,g in master.groupby('class'):
    row={'class':cls,'candidate_N':len(g)}
    for n in [20,30,40,50,60]:row[f'Top{n}_N']=int(g.primary_rank.le(n).sum())
    row['retained_fraction']=row['Top60_N']/len(g);row['notes']='Observed literature-density representation; no quota applied.';cl.append(row)
pd.DataFrame(cl).to_csv(DATA/'Stage25A_Class_Representation_Sensitivity.csv',index=False,encoding='utf-8-sig')

print({'candidates':len(master),'screened_records':len(prov),'included_original':int((prov.include_primary_metric=='yes').sum()),'citation_available':int(pd.to_numeric(prov.citation_count,errors='coerce').notna().sum()),'top5':master.head().canonical_name.tolist()},flush=True)
