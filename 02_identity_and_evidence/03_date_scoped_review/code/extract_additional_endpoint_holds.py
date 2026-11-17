"""Preserve reported IC50-type outcomes independently of molar capacity labels."""
import hashlib
import re
import xml.etree.ElementTree as ET
from reconcile_existing_work import SOURCE, ROOT, write


def main():
    rows = []
    specs = [
        ('PMC13567345', '10.3390/molecules31172981', 'Table 1', [
            ('(+)-Catechin', 19.02, .15), ('Pterostilbene', 16.46, .42)], 3,
         'ORAC IC50 (mM); footnote describes mM Trolox equivalents',
         'Table1 IC50 definition conflicts with capacity-style discussion; Methods3.4.3 uses net AUC and printed AUC/CT expression. Sample concentration,pH,temperature and TE derivation unresolved.',
         'Table1 meanSD from3different experiments each in triplicate',
         '50uL each sample,buffer,FL192nM,AAPH16mM;75mM phosphate;330min every5min;485/528nm'),
        ('PMC13700797', '10.3390/antiox15101279', 'Table 3', [
            ('Kaempferol', .7, .1), ('Trolox', 3.0, .6)], 3,
         'ORAC IC50 microgram/mL',
         'IC50 protection against AAPH normalized to nonoxidized blank is a distinct response endpoint; no inverse IC50 or molar capacity conversion applied.',
         'Table3 meanSD; independent-n hierarchy pending',
         'pH7.4;37C;1mLcuvette;40uL1MAAPH;31min every30s;485/528nm;DMSO samples'),
    ]
    for pmc, doi, label, values, column, units, issue, error, conditions in specs:
        path = SOURCE / 'fulltext_xml' / (pmc+'.xml')
        root = ET.fromstring(path.read_bytes())
        table = next(t for t in root.findall('.//table-wrap') if ''.join(t.find('label').itertext()).strip().endswith(label))
        for name, mean, sd in values:
            source_row = next(r for r in table.findall('.//tr') if list(r) and name in ' '.join(list(r)[0].itertext()))
            numbers = re.findall(r'\d+(?:\.\d+)?', ' '.join(list(source_row)[column].itertext()))
            assert list(map(float, numbers[:2])) == [mean, sd], (name, numbers)
            rows.append(dict(doi=doi, PMCID=pmc, compound=name, raw_mean=mean, raw_error=sd,
                             raw_units=units, error_definition=error, conditions=conditions,
                             locator=label+'; original ORAC methods', unresolved=issue,
                             disposition='ENDPOINT_DEFINITION_HOLD', converted_molar_capacity='',
                             model_label_release='NO', human_review_status='NOT_REVIEWED', change_applied='NO',
                             source_file=path.relative_to(ROOT).as_posix(),
                             source_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    write('Additional_Endpoint_Original_Extraction.csv', rows)
    print('Four original endpoint outcomes preserved without capacity conversion.')


if __name__ == '__main__':
    main()
