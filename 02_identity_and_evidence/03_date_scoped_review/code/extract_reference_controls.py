"""Reproduce original control values with unresolved TE calculation retained."""
import csv
import hashlib
import re
import xml.etree.ElementTree as ET
from reconcile_existing_work import ROOT, SOURCE, write


def main():
    path=SOURCE/'fulltext_xml/PMC12937457.xml'
    root=ET.fromstring(path.read_bytes())
    table=next(t for t in root.findall('.//table-wrap') if t.findtext('label')=='Table 1')
    cells=table.findall('.//tr')[1]
    profiles=list(csv.DictReader((ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig')))
    output=[]
    for column,name,mean,error in [(5,'Beta-carotene',.56,.05),(6,'Quercetin',5.48,.13),(7,'Ascorbic acid',.65,.01)]:
        values=re.findall(r'\d+(?:\.\d+)?',' '.join(cells[column].itertext()))
        assert list(map(float,values))==[mean,error]
        matches=[r for r in profiles if r['compound_name'].lower().replace('尾','beta')==name.lower()]
        output.append(dict(doi='10.3390/antiox15020163',PMCID='PMC12937457',compound=name,
            candidate_id=matches[0]['candidate_id'] if len(matches)==1 else '',
            candidate_identity_followup={'Ascorbic acid':'AFF-0104 parent match pending L stereochemistry','Beta-carotene':'AFF-0114;AFF-0129;AFF-0130 geometric isomer unspecified','Quercetin':'AFF-0009 exact material form pending'}[name],raw_mean=mean,raw_error=error,
            raw_units='TE relative to Trolox=1 as printed',error_definition='TABLE_SD_N3_INDEPENDENCE_UNRESOLVED',
            endpoint='NET_AUC_CONCENTRATION_CALIBRATION_TE_FORMULA_PENDING',
            conditions='37C;PBS pH unspecified;final sample0.625-20uM;20uLsample+120uLFL58nM+60uLAAPH40mM;250cycles60s;485/520nm',
            material='MilliporeSigma standards; exact form,purity and final vehicle unresolved',
            locator='Table1;Methods2.1 and2.2.1;Results3.1.1;Figure6',
            unresolved='TE slope ratio and regression range not explicitly defined; concentration-dependent quercetin response; pH and independent replication unresolved; supplements not checked',
            disposition='CALCULATION_AND_PROTOCOL_HOLD',conditional_molar_capacity='',model_label_release='NO',
            source_file=path.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            human_review_status='NOT_REVIEWED',change_applied='NO'))
    path=SOURCE/'fulltext_xml/PMC10416741.xml'
    root=ET.fromstring(path.read_bytes())
    paragraph=next(' '.join(p.itertext()) for p in root.findall('.//body//p') if '2378' in ' '.join(p.itertext()))
    assert 'ascorbic acid' in paragraph.lower()
    output.append(dict(doi='10.1080/13880209.2023.2244000',PMCID='PMC10416741',compound='Ascorbic acid',
        candidate_id='',candidate_identity_followup='AFF-0104 parent match pending L stereochemistry',raw_mean=2378,raw_error='',
        raw_units='micromolar Trolox equivalence/g as printed',error_definition='ERROR_NOT_REPORTED_IN_CHECKED_RESULTS_PARAGRAPH',
        endpoint='NET_AUC_TROLOX_CALIBRATION_UNRESOLVED_AMOUNT_DENOMINATOR',
        conditions='75mM phosphate,pH7.4;37C60min;25uLsample+100uLFL+30uLAAPH;FL3nMfinal;AAPH19mMfinal;485/525nm',
        material='Ascorbic acid reference; exact form,purity and vehicle unresolved',locator='ORAC Methods;Results paragraph;Figure3B caption',
        unresolved='TE amount versus concentration per g; reference material form,replication and error unresolved; figure image and supplements not checked',
        disposition='REFERENCE_DENOMINATOR_HOLD',conditional_molar_capacity='',model_label_release='NO',
        source_file=path.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        human_review_status='NOT_REVIEWED',change_applied='NO'))
    write(ROOT/'02_identity_and_evidence/03_date_scoped_review/results/Reference_Control_Original_Extraction.csv',output)


if __name__=='__main__':main()
