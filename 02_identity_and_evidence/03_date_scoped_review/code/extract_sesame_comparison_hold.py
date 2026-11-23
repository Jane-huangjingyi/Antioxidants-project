"""Extract the 2025 sesame comparison, preserving its unresolved denominator."""
import csv
import hashlib
import re
import xml.etree.ElementTree as ET
from reconcile_existing_work import SOURCE, ROOT, write


def main():
    source = SOURCE / 'fulltext_xml/PMC12719202.xml'
    root = ET.fromstring(source.read_bytes())
    table = next(t for t in root.findall('.//table-wrap') if t.findtext('label') == 'Table 4')
    profiles = list(csv.DictReader((ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv').open(encoding='utf-8-sig')))
    rows = []
    for name, mean, error in [('Sesamol',560.59,5.84), ('Pinoresinol Diglycoside',158.43,18.65),
                              ('Ferulic acid',2367.15,90.15), ('Pinoresinol',278.26,6.92),
                              ('Sesamin',29.59,12.97), ('Sesamolin',107.12,10.17)]:
        raw = next(t for t in table.findall('.//tr') if list(t) and ' '.join(list(t)[0].itertext()).strip() == name)
        values = re.findall(r'\d+(?:\.\d+)?',' '.join(list(raw)[1].itertext()))
        assert list(map(float,values[:2])) == [mean,error]
        matches = [p for p in profiles if p['compound_name'].lower() == name.lower()]
        rows.append(dict(doi='10.1016/j.fochx.2025.103317', PMCID='PMC12719202', compound=name,
                         candidate_id=matches[0]['candidate_id'] if len(matches)==1 else '',
                         candidate_mapping='PARENT_NAME_ONLY_EXACT_FORM_PENDING' if len(matches)==1 else 'EXACT_IDENTITY_MAPPING_PENDING',
                         raw_mean=mean, raw_error=error, raw_units='micromol TE/mM as printed',
                         error_definition='PLUS_MINUS_TABLE4_NO_STANDALONE_N_OR_ERROR_DEFINITION_CONFIRMED',
                         conditions='37C;20min preincubation;20uL ABAP119.4mM;150min every5min;485/535nm',
                         locator='Table4;Methods2.7_2.8;Results3.6',
                         unresolved='Amount versus concentration TE numerator; sample volume/dilution,pH,FL concentration,exact material forms,purity and independent n unresolved. Check independence against cited2017 method paper10.1039/C6RA26596K.',
                         disposition='DENOMINATOR_AND_STUDY_INDEPENDENCE_HOLD',
                         converted_molar_capacity='', model_label_release='NO',
                         source_file=source.relative_to(ROOT).as_posix(), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                         human_review_status='NOT_REVIEWED', change_applied='NO'))
    write('Sesame_Comparison_Original_Extraction.csv',rows)
    print('Six original sesame comparison rows extracted; units and independence remain pending.')


if __name__=='__main__':
    main()
