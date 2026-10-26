import concurrent.futures,json,pathlib
from retrieve_targeted import get
ROOT=pathlib.Path(__file__).resolve().parents[1]
targets={
'Kmo_EPMC_supplement.zip':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10424289/supplementaryFiles',
'PRJDB14081_runs.tsv':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJDB14081&result=read_run&fields=run_accession,study_accession,sample_accession,experiment_accession,scientific_name,sample_title,library_strategy&format=tsv',
'DRP011843.xml':'https://www.ebi.ac.uk/ena/browser/api/xml/DRP011843'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: entries=list(pool.map(get,targets.items()))
(ROOT/'qc/Kmo_Final_Access_Log.json').write_text(json.dumps({'date':'2026-10-26','entries':entries,'raw_sequence_downloaded':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(entries,ensure_ascii=False))
