"""Prioritize explicit method titles and recover available Europe PMC XML."""
from pathlib import Path
import csv,re,json,urllib.request,concurrent.futures,hashlib,xml.etree.ElementTree as ET,time
HERE=Path(__file__).resolve().parent

def run():
 with (HERE/'Master_Article_Register.csv').open(encoding='utf8',newline='') as f:articles=list(csv.DictReader(f))
 selected=[r for r in articles if re.search(r'\bORAC\b|oxygen radical absorbance|crocin bleaching|pyrogallol red',r['title'],re.I)]
 folder=HERE/'fulltext_xml';folder.mkdir(exist_ok=True)
 def fetch(row):
  pmc=row['PMCID'];path=folder/(pmc+'.xml');status='INSTITUTIONAL_OR_AUTHOR_SOURCE_REQUIRED';error=''
  if pmc:
   try:
    if not path.exists():
     url='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML'
     with urllib.request.urlopen(url,timeout=35) as response:data=response.read()
     ET.fromstring(data);path.write_bytes(data)
    ET.fromstring(path.read_bytes());status='PUBLIC_XML_RECOVERED_PENDING_READING'
   except Exception as exc:status='PUBLIC_XML_FETCH_FAILED';error=str(exc)
  return dict(article_key=row['article_key'],doi=row['doi'],PMID=row['PMID'],PMCID=pmc,title=row['title'],journal=row['journal'],title_priority='EXPLICIT_METHOD_TITLE',fulltext_recovery=status,source_url='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML' if pmc else 'https://doi.org/'+row['doi'] if row['doi'] else '',source_file=path.relative_to(HERE).as_posix() if path.exists() else '',sha256=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else '',error=error,scientific_screening='PENDING',human_review_status='NOT_REVIEWED',change_applied='NO')
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(fetch,selected))
 with (HERE/'Method_Fulltext_Queue.csv').open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 print(json.dumps(dict(explicit_method_titles=len(rows),public_XML_recovered=sum(r['fulltext_recovery']=='PUBLIC_XML_RECOVERED_PENDING_READING' for r in rows),failed=sum(r['fulltext_recovery']=='PUBLIC_XML_FETCH_FAILED' for r in rows))))
if __name__=='__main__':run()
