"""Preserve original ORAC-related outcomes whose endpoint or denominator is unresolved."""
import hashlib
import re
import xml.etree.ElementTree as ET
from reconcile_existing_work import ROOT, SOURCE, write


def main():
    output=[]
    specs=[('PMC8229286','10.3390/molecules26123542','Table 5',3,
            [('Curcumin',.32,.10),('DMC',.49,.03),('4HC',.43,.04),('4HDC',.41,.03),
             ('6HC',.39,.06),('8HC',.43,.11),('8HDC',.49,.29),('Trolox',2.02,.13)],
            'AAPH_response_IC50','micromolar compound','SEM_TABLE_N6_TO10',
            '3h every1.5min; pH7.4; FL70nM; AAPH12mM; stock1%MeOH;485/520nm',
            '50% response defined as(AUCsample-AUCblank)/AUCblank*100. IC50 requires a validated endpoint relationship before capacity synthesis. Independent-n hierarchy unresolved.'),
           ('PMC12040637','10.61882/ibj.4567','Table 1',5,
            [('Ursolic acid',.31,None),('Oleanolic acid',.46,None),('Cynaroside',.95,None),
             ('Rutin',.83,None),('Rosmarinic acid',.60,None),('Quercetin',1.06,None)],
            'ORAC_TE_UNSPECIFIED_DENOMINATOR','TE as printed','ORAC_ROW_ERROR_NOT_REPORTED',
            '75mM phosphate;37C;FL0.96uM working;2.5h every4.5min;485/538nm',
            'TE concentration/molar/mass denominator, sample concentration, pH and AAPH concentration unresolved. Table-wide SD statement supplies no numeric ORAC error.')]
    for pmc,doi,label,column,values,endpoint,units,error_type,conditions,issues in specs:
        path=SOURCE/'fulltext_xml'/(pmc+'.xml');root=ET.fromstring(path.read_bytes())
        table=next(t for t in root.findall('.//table-wrap') if t.find('label') is not None and ''.join(t.find('label').itertext()).strip()==label)
        source_rows=[[' '.join(' '.join(c.itertext()).split()) for c in list(r)] for r in table.findall('.//tr')]
        for name,mean,error in values:
            found=next(r for r in source_rows if r and (r[0]==name or name=='Quercetin' and r[0].startswith(name)))
            cell=found[column]
            numbers=re.findall(r'\d+(?:\.\d+)?',cell)
            assert numbers and float(numbers[0])==mean,(name,cell)
            if error is not None:assert len(numbers)>1 and float(numbers[1])==error
            output.append(dict(doi=doi,PMCID=pmc,compound=name,raw_mean=mean,raw_error=error if error is not None else '',
                               raw_units=units,error_definition=error_type,endpoint=endpoint,conditions=conditions,
                               locator=label+'; original assay methods',unresolved=issues,
                               disposition='DISTINCT_ENDPOINT_HOLD' if error is not None else 'DENOMINATOR_HOLD',
                               converted_molar_capacity='',model_label_release='NO',
                               source_file=path.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                               human_review_status='NOT_REVIEWED',change_applied='NO'))
    write('Distinct_Endpoint_Original_Extraction.csv',output)
    print('Fourteen original endpoint rows extracted with explicit holds.')


if __name__=='__main__':main()
