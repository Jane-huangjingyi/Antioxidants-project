"""Reproduce the browser-checked Table6 transcription; local original fetch is pending."""
import csv
from reconcile_existing_work import ROOT, write


VALUES = [
    ('p-Hydroxybenzoic acid',6.05,.78), ('Protocatechuic acid',7.61,.63),
    ('Vanillic acid',3.70,.67), ('Gallic acid',1.75,.17), ('Syringic acid',1.62,.22),
    ('Cinnamic acid',.13,.03), ('p-Coumaric acid',5.00,.46), ('Ferulic acid',3.43,.27),
    ('Sinapic acid',2.66,.28), ('Catechin',10.80,1.07), ('Epicatechin',9.37,.86), ('Rutin',7.40,.55),
]


def main():
    profiles = list(csv.DictReader((ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv').open(encoding='utf-8-sig')))
    rows = []
    for name, mean, error in VALUES:
        matches = [p for p in profiles if p['compound_name'].lower() == name.lower()]
        rows.append(dict(doi='10.1007/s00217-022-04135-3', compound=name,
                         candidate_id=matches[0]['candidate_id'] if len(matches)==1 else '',
                         raw_mean=mean, raw_error=error, raw_units='ORAC TE as printed',
                         locator='Original PDF p91 Table6 Experimental values ORAC column; Methods pp83-84',
                         provenance='MANUAL_TRANSCRIPTION_FROM_BROWSER_ORIGINAL_PDF_TEXT',
                         source_url='https://link.springer.com/content/pdf/10.1007/s00217-022-04135-3.pdf',
                         original_local_file='', original_local_sha256='',
                         local_recovery='PUBLISHER_CLIENT_CHALLENGE_RESPONSE;NO_LOCAL_PDF_RECOVERED',
                         conditions='10mM phosphate,pH7.4;37C30min preincubation;57cycles90s;485/520nm;FL10nM working;AAPH240mM working',
                         calculation='AUC=1+sum(f_i/f_0),i1..57;netAUC=AUCsample-AUCblank;Trolox calibration',
                         error_definition='Table6 plusminus,n4; independent standard preparations and exact error definition unresolved',
                         material='Reported suppliers/purities in Chemicals section; catechin hydrate98%; epicatechin source/form not explicitly resolved',
                         disposition='MOLECULAR_NORMALIZATION_AND_MATERIAL_QUALIFICATION_HOLD',
                         unresolved='Explicit sample concentration/molar denominator and final vehicle absent from checked text; exact isomers and independent n require followup; literature comparison columns excluded',
                         converted_molar_capacity='', model_label_release='NO',
                         human_review_status='NOT_REVIEWED', change_applied='NO'))
    write('Hop_Original_Table_Transcription.csv',rows)
    print('Twelve original ORAC cells transcribed with explicit browser-only provenance and holds.')


if __name__=='__main__':
    main()
