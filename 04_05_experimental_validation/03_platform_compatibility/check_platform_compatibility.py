"""Match checked source wavelengths to documented channels, not laboratory validation."""
from pathlib import Path
import csv
import hashlib
import json

HERE=Path(__file__).resolve().parent
ASSAY=HERE.parent
ROOT=ASSAY.parent

def channel_status(wavelength,available):
    return 'EXACT_CHANNEL_AVAILABLE' if wavelength in available else 'NO_EXACT_DEFAULT_CHANNEL'

def run():
    config_path=ASSAY/'config/platform_decisions.json'
    audit_path=ASSAY/'02_pilot_design/formula_source_audit.json'
    registry_path=ASSAY/'inputs/primary_method_registry.json'
    platform=json.loads(config_path.read_text())
    capabilities=platform['documented_capabilities']
    assert platform['instrument_model']=='Opentrons Flex Absorbance Plate Reader Module GEN1'
    assert capabilities['default_wavelengths_nm']==[450,562,600,650]
    assert capabilities['built_in_temperature_control'] is False
    assert capabilities['built_in_shaking'] is False
    assert capabilities['gripper_required'] is True
    assert capabilities['OT_2_compatible'] is False
    assert all(value is None for key,value in platform.items() if key.startswith('approved_'))
    sources={row['source_id']:row for row in json.loads(registry_path.read_text())}
    audited={row['id']:row for row in json.loads(audit_path.read_text())['records']}
    checked=[('Crocin bleaching',audited['CBA_2002_MANUAL'],
              'Separate 2002 plasma method supports 450 nm optical feasibility; the proposed pure-compound dose-time capacity endpoint remains unvalidated'),
             ('ORAC-PGR as audited',sources['PGR2011'],
              'Do not replace published 540 nm with 562 nm without independent analytical validation'),
             ('ABTS as audited',sources['ABTS1999'],
              'Do not replace published 734 nm with 650 nm or relabel the resulting response as the published method')]
    rows=[]
    for method,source,interpretation in checked:
        wavelength=source['detection_wavelength_nm']
        rows.append(dict(method=method,source_doi=source['doi'],checked_source_wavelength_nm=wavelength,
                         exact_channel_status=channel_status(wavelength,capabilities['default_wavelengths_nm']),
                         interpretation=interpretation,thermal_qualification='UNRESOLVED_NO_READER_TEMPERATURE_CONTROL',
                         local_accessories='PENDING_RESEARCHER_CONFIRMATION',assay_status='NOT_APPROVED',
                         human_review_status='NOT_REVIEWED',change_applied='NO'))
    assert sum(row['exact_channel_status']=='EXACT_CHANNEL_AVAILABLE' for row in rows)==1
    # API examples accepting integer lists do not imply arbitrary physical wavelengths.
    assert channel_status(734,capabilities['default_wavelengths_nm'])=='NO_EXACT_DEFAULT_CHANNEL'
    assert channel_status(540,capabilities['default_wavelengths_nm'])=='NO_EXACT_DEFAULT_CHANNEL'
    target=HERE/'Method_Platform_Compatibility.csv'
    with target.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    inputs=[config_path,audit_path,registry_path,Path(__file__)]
    summary={'documentation_checks':'PASS','execution_readiness':'NOT_READY','source_methods_compared':len(rows),
             'exact_channel_matches':1,'experimental_rows':0,'formal_model_fitted':False,
             'unresolved':['Actual gripper and accessory inventory','Installed software/API and labware','In-well temperature history during reaction/readout','Timing, dead time and optical/interference qualification','Capacity-estimator validation'],
             'sha256':{path.relative_to(ROOT).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs}}
    (HERE/'platform_readiness.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print('Platform documentation checks PASS; 1/3 exact wavelength matches; laboratory execution NOT_READY.')

if __name__=='__main__':
    run()
