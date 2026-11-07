"""Check new workbook tabs against their CSV sources and scan saved error cells."""
import csv,json,zipfile,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[2];ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
z=zipfile.ZipFile(R/'06_manuscript/tables/Candidate_Review_Workbook.xlsx')
names=[x.attrib['name'] for x in E.fromstring(z.read('xl/workbook.xml')).find('s:sheets',ns)]
assert len(names)==16
expected=[99,24,30,5]
for i,n in enumerate(expected,1):
    t=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
    assert len(t.findall('s:sheetData/s:row',ns))-1==n
errors=[]
for name in z.namelist():
    if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
        errors += [(name,c.attrib['r']) for c in E.fromstring(z.read(name)).iter() if c.tag.endswith('}c') and c.attrib.get('t')=='e']
assert not errors,errors
out=dict(status='PASS',worksheet_count=len(names),new_sheet_rows=dict(zip(names[:4],expected)),error_cells=errors)
(R/'07_quality_control/workbook_package_qc.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
