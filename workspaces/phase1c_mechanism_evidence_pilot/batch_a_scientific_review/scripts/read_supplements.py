import hashlib,json,pathlib,re,urllib.parse,zipfile,xml.etree.ElementTree as ET
from retrieve_sources import get
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'local_sources'
log=[]
for pmc,asset in [('PMC12837532','biology-15-00206-s001.zip'),('PMC13187579','mmc1.docx'),('PMC10070727','Image_2.jpg')]:
    html=(OUT/(pmc+'.html')).read_text(encoding='utf-8')
    links=re.findall(r'href="([^"]+)"',html)
    candidates=[u for u in links if asset in u]
    if not candidates:log.append({'paper':pmc,'asset':asset,'result':'URL_NOT_DISCOVERED'});continue
    url=urllib.parse.urljoin('https://pmc.ncbi.nlm.nih.gov',candidates[0].replace('&amp;','&'))
    try:
        status,ctype,content=get(url)
        usable=status==200 and (content[:2]==b'PK' or content[:2]==b'\xff\xd8')
        dest=OUT/(pmc+'_'+asset)
        if usable:dest.write_bytes(content)
        item={'paper':pmc,'url':url,'status':status,'content_type':ctype,'usable':usable,'sha256':hashlib.sha256(content).hexdigest(),'local_file':'local_sources/'+dest.name if usable else None}
        if usable and content[:2]==b'PK':
            with zipfile.ZipFile(dest) as z:
                item['members']=z.namelist()
                if asset.endswith('.docx'):
                    xml=ET.fromstring(z.read('word/document.xml'))
                    text=' '.join(n.text or '' for n in xml.iter() if n.tag.endswith('}t'))
                    item['document_text_local']='local_sources/'+dest.stem+'.txt'
                    (OUT/(dest.stem+'.txt')).write_text(text,encoding='utf-8')
        log.append(item)
    except Exception as e:log.append({'paper':pmc,'url':url,'error':str(e)})
(ROOT/'qc/Supplement_Access_Log.json').write_text(json.dumps({'date':'2026-10-23','entries':log},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(log,ensure_ascii=False))
