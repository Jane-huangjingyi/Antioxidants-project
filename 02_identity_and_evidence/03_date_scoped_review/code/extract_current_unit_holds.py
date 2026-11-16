"""Retain original standard capacities with unresolved unit scale, without conversion."""
import hashlib
import re
import xml.etree.ElementTree as ET
from reconcile_existing_work import ROOT, SOURCE, write


def main():
    path=SOURCE/'fulltext_xml/PMC11200581.xml'
    root=ET.fromstring(path.read_bytes())
    table=next(t for t in root.findall('.//table-wrap') if 'Standard/Method' in ' '.join(t.itertext()))
    output=[]
    for name,mean,error in [('Apigenin',438.90,46.52),('p-hydroxybenzoic acid',32519.03,3568.44),
                            ('Caffeic acid',33057.22,3312.59),('Vanillic acid',28072.31,1815.50)]:
        row=next(r for r in table.findall('.//tr') if list(r) and name.replace(' ','').lower() in ''.join(list(r)[0].itertext()).replace(' ','').lower())
        cell=' '.join(list(row)[1].itertext()).replace(',','')
        parsed=re.search(r'(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)',cell)
        assert parsed and tuple(map(float,parsed.groups()))==(mean,error)
        output.append(dict(doi='10.3390/antiox13060738',PMCID='PMC11200581',compound=name,
                           raw_mean=mean,raw_error=error,raw_units='mmol TE/g standard as printed in Table7',
                           error_type='SD_TRIPLICATE_ANALYSIS',pH=7.0,temperature_C='',
                           buffer='Printed0.075mM phosphate',material='Named analytical standard; exact form/purity unresolved',
                           locator='Table7; sections2.4.1 and2.4.3',
                           issue='Table7 mmolTE/g versus extract-method micromolTE/g; confirm standard scale. Printed buffer concentration also requires verification.',
                           disposition='UNIT_SCALE_HOLD',converted_molar_value='',model_label_release='NO',
                           source_file=path.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           human_review_status='NOT_REVIEWED',change_applied='NO'))
    write('Current_Standard_Unit_Holds.csv',output)
    print('Four original standard rows retained on unit hold.')


if __name__=='__main__':main()
