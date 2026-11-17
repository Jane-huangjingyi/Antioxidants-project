"""Hash user-supplied originals and preserve the original 2021 ORAC table."""
import csv,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'02_identity_and_evidence/03_date_scoped_review/results'
CACHE=ROOT/'02_identity_and_evidence/01_systematic_supplement/inputs'
manifest=[]
for path in sorted((ROOT/'download_raw').glob('*.pdf')):
    if not (path.name.startswith('1-s2') or path.name.startswith('i-trans')):continue
    pages=[p.extract_text() for p in PdfReader(path).pages]
    dois=re.findall(r'10\.\d{4,9}/[^\s]+',' '.join(pages[:2]))
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    (CACHE/(path.stem+'_page_text.json')).write_text(json.dumps(pages,ensure_ascii=False),encoding='utf8')
    manifest.append(dict(file=path.relative_to(ROOT).as_posix(),sha256=digest,pages=len(pages),DOI_tokens=';'.join(dict.fromkeys(dois)),reading_scope='IDENTITY_AND_TARGETED_TEXT_INTAKE',human_review_status='NOT_REVIEWED',change_applied='NO'))
def write(name,rows):
    with (OUT/name).open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
write('User_Original_PDF_Intake.csv',manifest)
source=ROOT/'download_raw/1-s2.0-S2667160321000296-main.pdf'
pages=[p.extract_text() for p in PdfReader(source).pages]
assert any('ORAC value 1.00 1.11 0.400 0.203 5.65 10.9 5.08 0.00541 1.14 5.03' in t for t in pages)
rows=[]
for code,value in zip(['TRO','ASC','CYS','BHT','EDA','QUE','MYR','HYD','CUR','CAP'],[1,1.11,.4,.203,5.65,10.9,5.08,.00541,1.14,5.03]):
    rows.append(dict(doi='10.1016/j.bbadva.2021.100030',source_code=code,raw_ORAC=value,raw_units='micromolar Trolox equivalent per micromolar; Results3.3',raw_error='',locator='Table1 ORAC row;Results3.3',source_file=source.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),disposition='PROTOCOL_IDENTITY_AND_REPLICATION_REVIEW_PENDING',identity_note='QUE is quercetin dihydrate; CAP reagent is N-vanillylnonanamide; preserve exact source identity',human_review_status='NOT_REVIEWED',change_applied='NO',model_label_release='NO'))
write('Takatsuka_Original_ORAC_Table.csv',rows)
print('Four PDFs registered; ten original ORAC rows retained for qualification.')
