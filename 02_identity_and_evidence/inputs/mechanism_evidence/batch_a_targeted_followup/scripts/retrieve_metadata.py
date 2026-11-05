import concurrent.futures,json,pathlib
from retrieve_targeted import get
ROOT=pathlib.Path(__file__).resolve().parents[1]
targets={acc+'.xml':'https://www.ebi.ac.uk/ena/browser/api/xml/'+acc for acc in ['SAMD00517030','SAMD00517031','SAMD00517032','DRX381958','DRX381959','DRX381960','PRJDB14081']}
targets.update({'HDAC1_EPMC_supplement.zip':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12837532/supplementaryFiles','Kmo_PMC_DataS1.doc':'https://pmc.ncbi.nlm.nih.gov/articles/instance/10424289/bin/JCMM-27-2290-s006.doc'})
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: entries=list(pool.map(get,targets.items()))
(ROOT/'qc/Metadata_and_Alternative_Access_Log.json').write_text(json.dumps({'date':'2026-10-26','entries':entries,'sequence_data_downloaded':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(entries,ensure_ascii=False))
