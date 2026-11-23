"""Extract the original 2022 two-concentration phenolic-acid bridge table.

Capacity conversions are conditional on the reported sample concentration scale.
Both concentrations belong to one DOI and retain separate source/protocol blocks.
"""
from pathlib import Path
import csv
import hashlib
import re
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'02_identity_and_evidence/01_systematic_supplement'
VALUES=[('Protocatechuic acid',30,.9,57,2),('Gentisic acid',29,1,53,0),
        ('Gallic acid',23,1,28,1),('Vanillic acid',26,1,56,1),
        ('Syringic acid',29,2,40,1),('p-Coumaric acid',20,2,33,1),
        ('Caffeic acid',31,2,60,1),('Ferulic acid',26,2,45,0),
        ('Sinapic acid',25,1,44,1),('Rosmarinic acid',50,2,92,2)]


def main():
    path=SOURCE/'fulltext_xml/PMC9495677.xml'
    root=ET.fromstring(path.read_bytes())
    table=next(n for n in root.findall('.//table-wrap') if 'Table 2' in ' '.join(n.itertext()))
    source_rows=[[' '.join(' '.join(cell.itertext()).split()) for cell in list(n)] for n in table.findall('.//tr')]
    with (ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as handle:
        profiles={r['compound_name'].lower():r for r in csv.DictReader(handle)}
    output=[]
    for name,low,low_error,high,high_error in VALUES:
        # Require original table-row numbers in their original two ORAC columns.
        matched=[r for r in source_rows if r and (name.lower() in r[0].lower() or name=='p-Coumaric acid' and 'coumaric acid' in r[0].lower())]
        assert len(matched)==1,(name,matched)
        for cell,expected in zip(matched[0][-2:],[(low,low_error),(high,high_error)]):
            parsed=re.fullmatch(r'(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)',cell)
            assert parsed and tuple(map(float,parsed.groups()))==expected,(name,cell,expected)
        profile=profiles[name.lower()]
        for concentration,mean,error in [(2.5,low,low_error),(5,high,high_error)]:
            output.append(dict(extraction_id='BRIDGE2022-'+profile['candidate_id']+'-'+str(concentration),
                               candidate_id=profile['candidate_id'],compound_name=name,
                               candidate_name=profile['compound_name'],candidate_mapping='PARENT_NAME_EXACT_FORM_PENDING',
                               doi='10.3390/antiox11091784',PMCID='PMC9495677',
                               source_row=name+' '+str(concentration)+' uM',
                               source_locator='Table2 ORAC '+str(concentration)+' uM column; sections2.1,2.2.2,2.3',
                               raw_mean=mean,raw_error=error,raw_units='micromolar TE',
                               error_type='PLUS_MINUS_STATISTIC_UNRESOLVED',reported_replication='Three replicates; independent unit unspecified',
                               independent_n='',assay='ORAC_FL_CITED_METHOD',pH='',temperature_C='',
                               integration_rule='80-minute reading; probe and 37 C from cited method DOI10.3390/md20010064',
                               reference_MW_g_mol='',
                               conditional_molar_capacity=mean/concentration,conditional_molar_error=error/concentration,
                               conversion_rule='MICROMOLAR_TE_DIVIDED_BY_REPORTED_TEST_MICROMOLAR_CONCENTRATION_CONDITIONAL',
                               source_experiment_cluster='10.3390/antiox11091784',
                               source_independence='TWO_CONCENTRATIONS_SHARE_ONE_DOI',
                               unresolved_fields='Sample versus Trolox concentration scale/final-well dilution; final ethanol; pH; source-specific temperature confirmation; error definition; exact material/purity; independent n',
                               source_url='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9495677/fullTextXML',
                               source_file=path.relative_to(SOURCE).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                               extraction_date='2026-11-16',model_label_release='NO',human_review_status='NOT_REVIEWED',change_applied='NO',
                               protocol_stratum='2022_REPORTED_DOSE_'+str(concentration)+'_UM'))
    with (HERE/'Reviewed_Bridge_Capacity_Rows.csv').open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(output[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(output)
    print('Extracted 20 original two-concentration rows from one DOI; conditional scale retained.')


if __name__=='__main__':
    main()
