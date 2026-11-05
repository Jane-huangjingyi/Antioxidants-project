from pathlib import Path
import urllib.request,urllib.parse,json
ROOT=Path(__file__).resolve().parents[3];RAW=ROOT/'workspaces/phase1c_mechanism_evidence_pilot/search_logs/raw'
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Antioxidants-project/0.1'}),timeout=45) as r:return r.read()
def put(name,obj):
 with (RAW/name).open('x',encoding='utf-8') as f:f.write(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2))
url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=11023549,11714376,14705020,37025617'
try:put('Additional_PubMed_Metadata.xml',get(url).decode('utf-8'));print('PUBMED_ADDITIONAL_OK',flush=True)
except Exception as e:put('Additional_PubMed_Error.json',{'url':url,'error':str(e)})
q='(organism_id:9606 OR organism_id:10090) AND (gene_exact:SIRT3 OR gene_exact:KMO OR gene_exact:NFE2L2 OR gene_exact:HMOX1 OR gene_exact:GPX4 OR gene_exact:HDAC1 OR gene_exact:GATA4 OR gene_exact:RELA OR gene_exact:TRAF2 OR gene_exact:TAS2R16 OR gene_exact:NOS3 OR gene_exact:TYR) AND reviewed:true'
url='https://rest.uniprot.org/uniprotkb/search?'+urllib.parse.urlencode({'query':q,'format':'json','size':100})
try:put('UniProt_Target_Identifiers.json',{'query':q,'url':url,'response':json.loads(get(url))});print('UNIPROT_OK',flush=True)
except Exception as e:put('UniProt_error.json',{'url':url,'error':str(e)})
url='https://pmc.ncbi.nlm.nih.gov/articles/PMC7443473/?report=xml'
try:
 body=get(url).decode('utf-8');put('PMC7443473_browser_response.html',body);print('SIRT3_HTML',len(body),'body_contains_methods',('Cell culture and treatments' in body),flush=True)
except Exception as e:put('PMC7443473_browser_error.json',{'url':url,'error':str(e)})
