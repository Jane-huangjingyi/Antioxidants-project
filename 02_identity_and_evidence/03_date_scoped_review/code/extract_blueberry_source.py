"""Transcribe verified original blueberry ORAC columns with exact glycoside identities."""
import hashlib
import re
import xml.etree.ElementTree as ET
from reconcile_existing_work import HERE, ROOT, SOURCE, read, write


def main():
    path=SOURCE/'fulltext_xml/PMC10232738.xml'
    root=ET.fromstring(path.read_bytes())
    table=next(t for t in root.findall('.//table-wrap') if 'ORAC' in ' '.join(t.itertext()))
    profiles={r['compound_name'].lower():r for r in read(HERE.parent/'results/candidate_evidence_profiles.csv')}
    values=[('BB1','Delphinidin-3-O-galactoside',13.23,.03),
            ('BB2','Delphinidin 3-O-glucoside',9.44,.12),
            ('BB3','Petunidin-3-O-galactoside',11.31,.22),
            ('BB4','Petunidin-3-O-glucoside',11.02,.16),
            ('BB5','Malvidin-3-O-galactoside',11.89,.13)]
    output=[]
    for label,name,mean,error in values:
        row=next(r for r in table.findall('.//tr') if list(r) and ''.join(list(r)[0].itertext()).strip()==label)
        cell=' '.join(list(row)[-1].itertext())
        assert re.search(rf'{mean:.2f}\s*±\s*{error:.2f}',cell),(label,cell)
        profile=profiles.get(name.lower(),{})
        output.append(dict(evidence_id='BLUEBERRY2023-'+label,doi='10.3389/fnut.2023.1172982',PMCID='PMC10232738',
                           compound=name,candidate_id=profile.get('candidate_id',''),raw_mean=mean,raw_error=error,
                           raw_units='micromol Trolox/micromol sample',error_type='SD_TABLE_N3',
                           replication='Table n3; methods triplicate and at least three independent experiments; hierarchy unresolved',
                           independent_n='',material_identity='Blueberry isolated and preparative-HPLC purified; HR-ESI-MS and NMR characterized',
                           purity='',pH=7.4,temperature_C=37,solvent='Reported phosphate buffer75mM; extraction solvents kept separate',
                           probe='Sodium fluorescein63nM final',initiator='AAPH12.8mM final',integration='60-minute relative fluorescence; blank-subtracted netAUC; Trolox calibration',
                           locator='Table1 ORAC column; Measurement of antioxidant capacity; extraction/purification and statistical analysis',
                           concentration_or_protocol_issue='Text says20uL sample and20uL Trolox together; clarify co-spiking versus parallel standard wells. Sample concentrations and independent-unit hierarchy unresolved.',
                           disposition='MATERIAL_PROTOCOL_QUALIFICATION_PENDING' if profile else 'EXACT_GLYCOSIDE_OUTSIDE_CURRENT193_SCOPE',
                           source_file=path.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           reading_scope='ORIGINAL_XML_METHODS_TABLE1_IDENTITIES_AND_STATISTICS',
                           model_label_release='NO',human_review_status='NOT_REVIEWED',change_applied='NO'))
    write('Blueberry_Original_Capacity_Extraction.csv',output)
    print('Five original ORAC rows extracted; one current-index parent match; exact sugar identities retained.')


if __name__=='__main__':main()
