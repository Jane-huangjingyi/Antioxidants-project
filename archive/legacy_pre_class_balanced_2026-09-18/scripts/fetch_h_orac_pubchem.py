import json, time, urllib.parse, urllib.request
from pathlib import Path

names = [
"(+)-Catechin","(-)-Epicatechin","(-)-Epigallocatechin gallate","(-)-Epigallocatechin","(-)-Epicatechin gallate",
"Gallocatechin","Quercetin","Kaempferol","Myricetin","Isorhamnetin","Fisetin","Quercitrin","Rutin",
"Luteolin","Apigenin","Naringenin","Hesperetin","Eriodictyol","Hesperidin","Cyanidin","Cyanidin 3-O-glucoside",
"Delphinidin","Pelargonidin","Malvidin","Genistein","Daidzein","Glycitein","Gallic acid","Protocatechuic acid",
"Vanillic acid","Syringic acid","Caffeic acid","trans-Ferulic acid","p-Coumaric acid","Sinapic acid","Rosmarinic acid",
"Chlorogenic acid","Neochlorogenic acid","Cryptochlorogenic acid","trans-Resveratrol","Piceatannol","Secoisolariciresinol",
"Matairesinol","Sesamol","Curcumin","Capsaicin","Carvacrol","Thymol","Eugenol","Tyrosol"]

out={}
for i,name in enumerate(names):
    url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+urllib.parse.quote(name,safe='')+'/property/Title,IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChIKey/JSON'
    try:
        with urllib.request.urlopen(url,timeout=30) as r: data=json.load(r)
        p=data['PropertyTable']['Properties'][0]
        out[name]=p
        print(i+1,name,p.get('CID'),p.get('InChIKey'))
    except Exception as e:
        out[name]={'error':str(e)}; print('ERROR',name,e)
    time.sleep(.12)
Path('data/pubchem_h_orac_phenolics.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
