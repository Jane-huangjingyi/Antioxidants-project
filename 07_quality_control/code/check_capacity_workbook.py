"""Check new workbook tabs against their CSV sources and scan saved error cells."""
import csv,json,zipfile,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[2];ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
z=zipfile.ZipFile(R/'06_manuscript/tables/Candidate_Review_Workbook.xlsx')
names=[x.attrib['name'] for x in E.fromstring(z.read('xl/workbook.xml')).find('s:sheets',ns)]
assert len(names)==17
files=['Capacity_Analysis_Entry.csv','Food_and_Material_Followup.csv','Within_Source_Descriptive_Order.csv','Legacy30_Verification.csv','Bridge_Protocol_Matrix.csv']
sources=[]
for file in files:
    with (R/'03_candidate_selection/01_activity_model/results'/file).open(encoding='utf-8-sig',newline='') as f:sources.append(list(csv.reader(f)))
expected=[len(r)-1 for r in sources]
strings=[]
if 'xl/sharedStrings.xml' in z.namelist():
    strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
for i,n in enumerate(expected,1):
    t=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
    assert len(t.findall('s:sheetData/s:row',ns))-1==n
    source=sources[i-1]
    for ri,row in enumerate(t.findall('s:sheetData/s:row',ns)):
        for cell in row.findall('s:c',ns):
            letters=''.join(c for c in cell.attrib['r'] if c.isalpha());ci=0
            for c in letters:ci=ci*26+ord(c)-64
            ci-=1
            value=cell.find('s:v',ns)
            actual=value.text if value is not None else ''
            if cell.attrib.get('t')=='s':actual=strings[int(actual)]
            elif cell.attrib.get('t')=='inlineStr':actual=''.join(cell.find('s:is',ns).itertext())
            target=source[ri][ci] if ci<len(source[ri]) else ''
            if str(actual or '')!=target:
                assert cell.attrib.get('t') not in ['s','inlineStr'] and float(actual)==float(target),(i,ri,ci,actual,target)
errors=[]
for name in z.namelist():
    if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
        errors += [(name,c.attrib['r']) for c in E.fromstring(z.read(name)).iter() if c.tag.endswith('}c') and c.attrib.get('t')=='e']
assert not errors,errors
out=dict(status='PASS',worksheet_count=len(names),new_sheet_rows=dict(zip(names[:5],expected)),error_cells=errors)
(R/'07_quality_control/workbook_package_qc.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
