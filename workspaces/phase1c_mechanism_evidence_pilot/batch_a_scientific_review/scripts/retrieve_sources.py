"""Retrieve five in-scope public article pages and their selected figure assets only.
Raw files remain ignored/local; access logs contain hashes, not article content.
"""
import concurrent.futures, hashlib, json, pathlib, re
import urllib.request, urllib.error
def get(url):
    try:
        with urllib.request.urlopen(url,timeout=25) as response:
            return response.status,response.headers.get('Content-Type',''),response.read()
    except urllib.error.HTTPError as e:return e.code,e.headers.get('Content-Type',''),e.read()
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'local_sources'
OUT.mkdir(exist_ok=True)
PAPERS={'PMC10424289':['JCMM-27-2290-g002.jpg','JCMM-27-2290-g001.jpg'], 'PMC11599353':['10565_2024_9953_Fig2_HTML.jpg'], 'PMC12837532':['biology-15-00206-g004.jpg','biology-15-00206-g006.jpg'], 'PMC13187579':['gr6.jpg'], 'PMC10070727':['fnut-10-1060226-g004.jpg','Image_2.jpg']}
def retrieve(pmc):
    entries=[]
    url=f'https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/'
    try:
        status,ctype,content=get(url)
        html=content.decode('utf-8',errors='replace')
        good=status==200 and '<article' in html and 'captcha' not in html[:5000].lower()
        if good: (OUT/(pmc+'.html')).write_bytes(content)
        entries.append({'paper':pmc,'url':url,'status':status,'usable_article_html':good,'sha256':hashlib.sha256(content).hexdigest(),'local_file':f'local_sources/{pmc}.html' if good else None})
        urls=re.findall(r'(?:src|href)="([^"]+)"',html)
        for asset in PAPERS[pmc]:
            candidates=[u for u in urls if asset in u and 'cdn.ncbi' in u]
            if not candidates:
                entries.append({'paper':pmc,'asset':asset,'result':'URL_NOT_DISCOVERED_NO_CONTENT_CLAIM'})
                continue
            u=candidates[0].replace('&amp;','&')
            status,ctype,content=get(u)
            image=status==200 and ctype.startswith('image/')
            filename=pmc+'_'+asset
            if image:(OUT/filename).write_bytes(content)
            entries.append({'paper':pmc,'url':u,'status':status,'usable_image':image,'sha256':hashlib.sha256(content).hexdigest(),'local_file':f'local_sources/{filename}' if image else None})
    except Exception as e:entries.append({'paper':pmc,'url':url,'error':str(e),'result':'NOT_RECOVERED'})
    return entries
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        log=[item for group in pool.map(retrieve,PAPERS) for item in group]
    (ROOT/'qc'/'Source_Access_Log.json').write_text(json.dumps({'date':'2026-10-23','raw_distribution':'LOCAL_ONLY_EXCLUDED','entries':log},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(log,ensure_ascii=False))
