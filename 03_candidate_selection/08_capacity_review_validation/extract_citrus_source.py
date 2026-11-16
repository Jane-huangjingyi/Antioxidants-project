"""Extract original single-flavonoid ORAC from the 2020 citrus study Table4."""
from pathlib import Path
import csv
import hashlib
import re
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'02_identity_and_evidence/01_systematic_supplement'
VALUES=[('Hesperidin',247.3,13.2),('Hesperetin-7-O-glucoside',323.9,13.7),
        ('Hesperetin',710.9,12.0),('Narirutin',283.4,15.7),('Prunin',363.9,18.1),
        ('Naringenin',475.1,13.3),('Sinensetin',7.6,.4),('Nobiletin',6.0,.4),('Tangeretin',5.8,.4)]


def main():
    path=SOURCE/'fulltext_xml/PMC7278842.xml'
    root=ET.fromstring(path.read_bytes())
    table=next(t for t in root.findall('.//table-wrap') if 't004' in t.get('id',''))
    rows=[[' '.join(' '.join(c.itertext()).split()) for c in list(r)] for r in table.findall('.//tr')]
    with (ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as handle:
        profiles={r['compound_name'].lower():r for r in csv.DictReader(handle)}
    output=[]
    for name,mean,error in VALUES:
        found=[r for r in rows if r and re.sub(r'\s+','',r[0]).lower()==name.lower()]
        assert len(found)==1,(name,found)
        parsed=re.search(r'(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)',found[0][3])
        assert parsed and tuple(map(float,parsed.groups()))==(mean,error),(name,found)
        p=profiles.get(name.lower(),{})
        mw=float(p['molecular_weight_g_mol']) if p else None
        row=dict(extraction_id='CITRUS2020-'+name,candidate_id=p.get('candidate_id',''),
                 compound_name=name,candidate_name=p.get('compound_name',''),candidate_mapping='PARENT_NAME_EXACT_FORM_PENDING' if p else 'OUTSIDE_CURRENT193',
                 doi='10.3390/antiox9050360',PMCID='PMC7278842',source_row=name,
                 source_locator='Table4 ORAC column; sections2.2 and2.6; Table4 footnote',
                 raw_mean=mean,raw_error=error,raw_units='mg TE/100mg compound',error_type='SD_TRIPLICATE_EXPERIMENTS',
                 reported_replication='Table4 mean+/-SD of triplicate experiments; independent units unspecified',
                 independent_n='',assay='ORAC_FL',pH='',temperature_C=37,
                 integration_rule='120min; every3min; sample25uL+FL150uL+AAPH25uL;485/535nm; AUC vs Trolox',
                 reference_MW_g_mol=mw if mw else '',conditional_molar_capacity=mean/100*mw/250.29 if mw else '',
                 conditional_molar_error=error/100*mw/250.29 if mw else '',
                 conversion_rule='TABLE4_MG_TE_PER100MG_COMPOUND_DIVIDE100_TIMES_PARENT_MW_OVER_TROLOX250.29',
                 source_experiment_cluster='10.3390/antiox9050360',source_independence='SAME_DOI_SHARED_EXPERIMENTAL_SOURCE',
                 unresolved_fields='Exact chemical form/purity and catalogue; final solvent; pH; replicate independence. Table4 compound100mg basis retained separately from extract mgTE/g methods.',
                 source_url='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7278842/fullTextXML',
                 source_file=path.relative_to(SOURCE).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 extraction_date='2026-11-16',model_label_release='NO',human_review_status='NOT_REVIEWED',change_applied='NO',
                 protocol_stratum='CITRUS2020_TABLE4_120MIN_PH_UNREPORTED')
        output.append(row)
    with (HERE/'Reviewed_Citrus_Capacity_Rows.csv').open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(output[0]),lineterminator='\n');writer.writeheader();writer.writerows(output)
    print('Nine original rows; four parent-mapped conditional molar conversions.')


if __name__=='__main__':main()
