"""Trace secondary ORAC columns to the cited original without releasing duplicate labels."""
import hashlib
import re
import xml.etree.ElementTree as ET
from reconcile_existing_work import ROOT, SOURCE, write


def main():
    path=SOURCE/'fulltext_xml/PMC8426225.xml'
    root=ET.fromstring(path.read_bytes())
    table=next(t for t in root.findall('.//table-wrap') if 'Reported in Gómez-Maqueo' in ' '.join(t.itertext()))
    values=[('Indicaxanthin',17.32,.68),('Betanin',10.92,.44),('Piscidic acid',3.56,.16),
            ('IG1',34.96,1.4),('IG2',30.24,1.2),('IG4',27.76,1.12),('IG5',18,.72),('Ascorbic acid',3.04,.12)]
    source_rows=[[' '.join(' '.join(c.itertext()).split()) for c in list(r)] for r in table.findall('.//tr')]
    output=[]
    for name,mean,error in values:
        row=next(r for r in source_rows if r and r[0].startswith(name))
        parsed=re.search(r'(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)',row[3])
        assert parsed and tuple(map(float,parsed.groups()))==(mean,error),(name,row)
        output.append(dict(citing_doi='10.1007/s11130-021-00914-7',PMCID='PMC8426225',compound=name,
                           secondary_ORAC_mean=mean,secondary_ORAC_error=error,secondary_units='micromol Trolox eq/mg',
                           cited_original_doi='10.1002/jsfa.9917',original_year=2019,
                           locator='Table1 ORAC superscript2 and footnote; reference4',
                           source_role='SECONDARY_ORAC_ORIGINAL_LOX_FL',original_verified='NO',
                           study_deduplication_key='10.1002/jsfa.9917',
                           disposition='RECOVER_CITED_ORIGINAL_NO_DUPLICATE_LABEL',model_label_release='NO',
                           source_file=path.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           human_review_status='NOT_REVIEWED',change_applied='NO'))
    write('Secondary_ORAC_Original_Source_Trace.csv',output)
    print('Eight secondary ORAC rows traced to one 2019 original DOI; no labels released.')


if __name__=='__main__':main()
