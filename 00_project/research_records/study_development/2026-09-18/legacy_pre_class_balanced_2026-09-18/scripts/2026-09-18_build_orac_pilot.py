import csv, json, math, os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "figures"
DATA.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

pubchem = {x["query"]: x for x in json.loads((DATA / "pubchem_pilot_compounds.json").read_text(encoding="utf-8"))}

compounds = [
    ("EGCG", "epigallocatechin gallate", "Epigallocatechin-3-gallate", "Polyphenolic / phenolic compounds", "flavan-3-ols / catechins", "tea", "H-ORAC", "hydrophilic", "normal"),
    ("Catechin", "catechin", "(+)-Catechin", "Polyphenolic / phenolic compounds", "flavan-3-ols / catechins", "tea; cocoa; apples", "H-ORAC", "hydrophilic", "normal"),
    ("Epicatechin", "epicatechin", "(-)-Epicatechin", "Polyphenolic / phenolic compounds", "flavan-3-ols / catechins", "cocoa; tea; apples", "H-ORAC", "hydrophilic", "normal"),
    ("Quercetin", "quercetin", "Quercetin aglycone", "Polyphenolic / phenolic compounds", "flavonols", "onions; apples; capers", "H-ORAC", "hydrophilic", "normal"),
    ("Kaempferol", "kaempferol", "Kaempferol aglycone", "Polyphenolic / phenolic compounds", "flavonols", "kale; tea; broccoli", "H-ORAC", "hydrophilic", "normal"),
    ("Gallic acid", "gallic acid", "3,4,5-Trihydroxybenzoic acid", "Polyphenolic / phenolic compounds", "phenolic acids / hydroxybenzoic acids", "berries; tea; grapes", "H-ORAC", "hydrophilic", "normal"),
    ("Caffeic acid", "caffeic acid", "trans-Caffeic acid", "Polyphenolic / phenolic compounds", "phenolic acids / hydroxycinnamic acids", "coffee; fruits; vegetables", "H-ORAC", "hydrophilic", "normal"),
    ("Ferulic acid", "ferulic acid", "trans-Ferulic acid", "Polyphenolic / phenolic compounds", "phenolic acids / hydroxycinnamic acids", "whole grains; rice bran", "H-ORAC", "hydrophilic", "normal"),
    ("Chlorogenic acid", "chlorogenic acid", "5-O-Caffeoylquinic acid", "Polyphenolic / phenolic compounds", "phenolic acids / hydroxycinnamic-acid conjugates", "coffee; potatoes; apples", "H-ORAC", "hydrophilic", "normal"),
    ("Resveratrol", "resveratrol", "trans-Resveratrol", "Polyphenolic / phenolic compounds", "stilbenes", "grapes; peanuts; berries", "H-ORAC", "borderline", "special-case: low aqueous solubility/cyclodextrin sensitivity"),
    ("L-Ascorbic acid", "ascorbic acid", "Vitamin C", "Vitamins / vitamin-like dietary antioxidants", "vitamin C / ascorbic acid", "citrus; peppers; berries", "H-ORAC", "hydrophilic", "special-case: oxidation instability"),
    ("alpha-Tocopherol", "alpha-tocopherol", "alpha-Tocopherol", "Vitamins / vitamin-like dietary antioxidants", "tocopherols", "vegetable oils; nuts; seeds", "L-ORAC", "lipophilic", "special-case: stereoisomer/form and RMCD dependence"),
    ("gamma-Tocopherol", "gamma-tocopherol", "(+)-gamma-Tocopherol", "Vitamins / vitamin-like dietary antioxidants", "tocopherols", "soy/corn oils; nuts", "L-ORAC", "lipophilic", "special-case: stereoisomer/form and RMCD dependence"),
    ("Lycopene", "lycopene", "all-trans-Lycopene", "Carotenoids", "carotenes", "tomatoes; watermelon", "L-ORAC", "lipophilic", "special-case: aggregation, photolability, inner-filter effect"),
    ("beta-Carotene", "beta-carotene", "all-trans-beta-Carotene", "Carotenoids", "carotenes", "carrots; leafy greens", "L-ORAC", "lipophilic", "special-case: aggregation, oxygen/light and optical interference"),
    ("Lutein", "lutein", "Lutein A", "Carotenoids", "xanthophylls", "leafy greens; egg yolk", "L-ORAC", "lipophilic", "special-case: aggregation, isomerism and optical interference"),
    ("Sulforaphane", "sulforaphane", "Sulforaphane", "Organosulfur compounds", "isothiocyanates", "broccoli sprouts; crucifers", "Special-case", "noncanonical", "special-case: electrophilic/Nrf2 mechanism; ORAC may underestimate redox relevance"),
]

meta = {}
for display, query, synonym, cls, sub, foods, arm, compat, special in compounds:
    p = pubchem[query]
    meta[display] = dict(compound_name=display, synonym=synonym, PubChem_CID=p["CID"], InChIKey=p["InChIKey"], chemical_class=cls, subclass=sub, food_source_examples=foods, preferred_ORAC_arm=arm, compatibility_group=compat, special_case=special)

common_ou = dict(
    ORAC_arm="H-ORAC", H_ORAC_or_L_ORAC="H-ORAC", compound_form="free compound as named", stereochemistry="as reported/structure-specific where applicable", purity="supplier stated; numerical purity not reported", original_unit="mol TE/mol compound", molar_conversion_possible="yes", AAPH_concentration="12.8 mM final", fluorescein_concentration="48 nM", Trolox_concentration="12.5, 25, 50, 100 uM", buffer="75 mM potassium phosphate", pH="7.4", temperature="37 C", solvent="50:50 acetone/water stock; diluted with buffer", solubilizer_RMCD="none", reading_interval="1 min", total_duration="30 min", AUC_method="normalized AUC; net AUC=sample-blank; Eq. 2 molarity ratio", concentration_range="compound-specific; full range not tabulated", linearity_reported="method-level yes; compound-specific incomplete", interference_noted="fluorescein control; no compound-specific optical QC", PMID="11599998", DOI="10.1021/jf010586o", publication_year="2001", study="Ou, Hampsch-Woodill & Prior, J Agric Food Chem 49:4619-4626", Zotero_key="4FIGEV33", exact_location="Table 4, p. 4622; methods pp. 4619-4620", comparability_tier="B", notes="Original ORAC-FL record. Tier B because numerical purity and full compound-specific linearity/interference data are not reported."
)
common_fig = dict(
    ORAC_arm="H-ORAC", H_ORAC_or_L_ORAC="H-ORAC", compound_form="reported analytical reagent; quercetin specifically dihydrate", stereochemistry="as purchased/reported", purity="analytical reagent grade; numerical purity not reported", original_unit="mol TE/mol compound", molar_conversion_possible="yes", AAPH_concentration="12 mM final well concentration", fluorescein_concentration="35 nM final well concentration", Trolox_concentration="2-10 uM", buffer="75 mM phosphate", pH="7.4", temperature="37 C", solvent="buffer; 5% final ethanol for quercetin/caffeic acid", solubilizer_RMCD="none", reading_interval="1 min", total_duration="up to 3 h", AUC_method="normalized decay; AUC to 5% initial fluorescence; slope ratio versus Trolox", concentration_range="ascorbic 3.5-9 uM; gallic 2-10 uM; quercetin 0.40-2.0 uM; caffeic 0.40-1.0 uM", linearity_reported="yes; five standards, triplicate on two days, R>0.9964", interference_noted="ethanol effect evaluated; fluorescence stability control; no complete compound spectral QC", PMID="36829987", DOI="10.3390/antiox12020505", publication_year="2023", study="Carvalho et al., Antioxidants 12:505", Zotero_key="EHLKNP4E", exact_location="Table 3; Methods 2.1-2.3; Table 1", comparability_tier="B", notes="Original ORAC-FL AUC value. Tier B because numerical purity is not reported; quercetin was tested as dihydrate and requires explicit form adjudication against anhydrous identifiers."
)
common_huang = dict(
    ORAC_arm="L-ORAC", H_ORAC_or_L_ORAC="L-ORAC", compound_form="natural tocopherol form as named", stereochemistry="reported (+) where stated; alpha form requires source-form review", purity="supplier/material stated in paper; numerical purity not verified in accessible text", original_unit="mol TE/mol compound", molar_conversion_possible="yes", AAPH_concentration="reported in full method; not verified in accessible abstract", fluorescein_concentration="reported in full method; not verified in accessible abstract", Trolox_concentration="Trolox standard=1.0; detailed range not verified", buffer="75 mM phosphate", pH="7.4", temperature="37 C", solvent="50% acetone-water stock into buffer", solubilizer_RMCD="7% w/v randomly methylated beta-cyclodextrin", reading_interval="not verified in accessible text", total_duration="not verified in accessible text", AUC_method="ORAC-FL net AUC relative to Trolox", concentration_range="linearity validated; exact range not verified", linearity_reported="yes at method level", interference_noted="solubility validation reported; compound-specific optical QC not verified", PMID="11902917", DOI="10.1021/jf0113732", publication_year="2002", study="Huang et al., J Agric Food Chem 50:1815-1821", Zotero_key="2TR33GW5", exact_location="Abstract reports values; full article validation tables require second-pass extraction", comparability_tier="B", notes="Original L-ORAC-FL value. Tier B pending full-text verification of purity, reading schedule, exact concentrations and compound-specific QC."
)

records = []
def add(compound, value, source):
    r = {**meta[compound], **source}
    r["original_ORAC_value"] = value
    r["standardized_ORAC_mol_TE_per_mol"] = value
    records.append(r)

for c, v in [("Caffeic acid",4.37),("Chlorogenic acid",3.14),("Quercetin",7.28),("Catechin",6.76),("L-Ascorbic acid",0.95)]: add(c,v,common_ou)
for c, v in [("L-Ascorbic acid",0.53),("Gallic acid",1.25),("Quercetin",16.62),("Caffeic acid",8.26)]: add(c,v,common_fig)
for c, v in [("alpha-Tocopherol",0.50),("gamma-Tocopherol",0.74)]: add(c,v,common_huang)

raw_fields = ["compound_name","synonym","PubChem_CID","InChIKey","chemical_class","subclass","food_source_examples","ORAC_arm","H_ORAC_or_L_ORAC","compound_form","stereochemistry","purity","original_ORAC_value","original_unit","molar_conversion_possible","standardized_ORAC_mol_TE_per_mol","AAPH_concentration","fluorescein_concentration","Trolox_concentration","buffer","pH","temperature","solvent","solubilizer_RMCD","reading_interval","total_duration","AUC_method","concentration_range","linearity_reported","interference_noted","PMID","DOI","publication_year","study","Zotero_key","exact_location","comparability_tier","notes"]
with (DATA / "ORAC_Pilot_Raw_Extraction.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=raw_fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in raw_fields} for r in records])

analysis=[]
for display,*_ in compounds:
    rs=[r for r in records if r["compound_name"]==display]
    a=[r for r in rs if r["comparability_tier"]=="A"]
    b=[r for r in rs if r["comparability_tier"]=="B"]
    c=[r for r in rs if r["comparability_tier"]=="C"]
    x=[r for r in rs if r["comparability_tier"]=="X"]
    vals=[r["standardized_ORAC_mol_TE_per_mol"] for r in a]
    status="eligible_multi_study" if len(a)>=2 else "single_study" if len(a)==1 else "supportive_only" if b else "not_measured"
    analysis.append({**meta[display],"Tier_A_count":len(a),"Tier_B_count":len(b),"Tier_C_count":len(c),"Tier_X_count":len(x),"missing":1 if not rs else 0,"analysis_status":status,"Tier_A_median":np.median(vals) if vals else "","Tier_A_min":min(vals) if vals else "","Tier_A_max":max(vals) if vals else "","Tier_A_IQR":(np.percentile(vals,75)-np.percentile(vals,25)) if len(vals)>=4 else "","Tier_B_values":";".join(str(r['standardized_ORAC_mol_TE_per_mol']) for r in b),"heterogeneity_notes":"No Tier A records; Tier B values retained without ranking" if not a else ""})
fields=list(analysis[0].keys())
with (DATA / "ORAC_Pilot_TierA_Analysis.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(analysis)

cuprac_yes={"EGCG":"yes","Catechin":"yes","Epicatechin":"yes","Quercetin":"yes","Gallic acid":"yes","Caffeic acid":"yes","Ferulic acid":"yes","L-Ascorbic acid":"yes","alpha-Tocopherol":"yes","Kaempferol":"unclear"}
with (DATA / "CUPRAC_Coverage_Summary.csv").open("w",newline="",encoding="utf-8-sig") as f:
    cols=["compound_name","chemical_class","CUPRAC_available","approximate_number_of_studies","unit_type","comparability","notes","key_source_DOI","Zotero_key"]
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for row in analysis:
        name=row["compound_name"]; avail=cuprac_yes.get(name,"no_identified_in_pilot")
        w.writerow(dict(compound_name=name,chemical_class=row["chemical_class"],CUPRAC_available=avail,approximate_number_of_studies="1+" if avail=="yes" else "0/unclear",unit_type="mol TE/mol or TEAC depending paper" if avail=="yes" else "not_applicable",comparability="moderate; protocol verification required" if avail=="yes" else "not_assessed",notes="Coverage only; no CUPRAC ranking performed",key_source_DOI="10.3390/12071496" if avail=="yes" else "",Zotero_key="BC43GAEF" if avail=="yes" else ""))

colors={"Polyphenolic / phenolic compounds":"#4472C4","Vitamins / vitamin-like dietary antioxidants":"#ED7D31","Carotenoids":"#FFC000","Organosulfur compounds":"#70AD47"}

def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
    ]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def insufficient_arm_plot(arm, filename, title):
    subset=[r for r in analysis if r["preferred_ORAC_arm"]==arm]
    labels=[r["compound_name"] for r in subset]
    bcounts=[r["Tier_B_count"] for r in subset]
    W,H=1800,1100; im=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(im)
    d.text((70,35),title,fill="#202020",font=font(34,True))
    d.text((70,88),"No Tier A records passed the frozen rubric; distribution/ranking not estimated",fill="#B3261E",font=font(25,True))
    d.text((70,130),"Bars show supportive Tier B coverage only, not antioxidant-capacity rank.",fill="#555555",font=font(22))
    left,top,right,bottom=110,210,W-60,H-330; d.line((left,top,left,bottom),fill="#333",width=3); d.line((left,bottom,right,bottom),fill="#333",width=3)
    maxv=max([1]+bcounts); gap=(right-left)/max(1,len(labels)); bw=gap*.58
    for i,(lab,val,row) in enumerate(zip(labels,bcounts,subset)):
        x=left+gap*(i+.5); bh=(bottom-top-40)*val/maxv
        d.rectangle((x-bw/2,bottom-bh,x+bw/2,bottom),fill=colors.get(row["chemical_class"],"#888"))
        d.text((x-8,bottom-bh-35),str(val),fill="#222",font=font(21,True))
        # vertical labels keep long names readable
        txt=Image.new("RGBA",(260,35),(255,255,255,0)); td=ImageDraw.Draw(txt); td.text((0,0),lab,fill="#222",font=font(19)); txt=txt.rotate(52,expand=True)
        im.paste(txt,(int(x-25),bottom+12),txt)
    d.text((10,(top+bottom)//2),"Tier B count",fill="#333",font=font(22))
    im.save(FIG/filename)

insufficient_arm_plot("H-ORAC","H_ORAC_Historical_Distribution.png","Historical H-ORAC values across representative food-derived antioxidant compounds")
insufficient_arm_plot("L-ORAC","L_ORAC_Historical_Distribution.png","Historical L-ORAC values across representative lipophilic antioxidant compounds")

labels=[r["compound_name"] for r in analysis]
A=np.array([r["Tier_A_count"] for r in analysis]); B=np.array([r["Tier_B_count"] for r in analysis]); CX=np.array([r["Tier_C_count"]+r["Tier_X_count"] for r in analysis]); M=np.array([r["missing"] for r in analysis])
W,H=1800,1250; im=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(im)
d.text((70,30),"ORAC literature coverage by compound (pilot)",fill="#202020",font=font(36,True))
legend=[("Tier A","#2E7D32"),("Tier B","#F9A825"),("Tier C/X","#C62828"),("No eligible record found","#BDBDBD")]
x=70
for lab,col in legend:
    d.rectangle((x,90,x+28,118),fill=col); d.text((x+38,88),lab,fill="#333",font=font(21)); x+=240 if lab!="No eligible record found" else 360
left,top,rowh=420,150,57; scale=170
for i,(lab,a,b,cx,m) in enumerate(zip(labels,A,B,CX,M)):
    y=top+i*rowh; d.text((55,y+10),lab,fill="#222",font=font(21))
    xpos=left
    for val,col in [(int(a),"#2E7D32"),(int(b),"#F9A825"),(int(cx),"#C62828"),(int(m),"#BDBDBD")]:
        if val:
            d.rectangle((xpos,y+8,xpos+val*scale,y+42),fill=col); d.text((xpos+8,y+10),str(val),fill="#111",font=font(19,True)); xpos+=val*scale
    d.line((left,y+47,W-60,y+47),fill="#EEEEEE",width=1)
d.text((left,H-70),"Counts reflect record eligibility under the frozen A/B/C/X rubric; gray indicates no eligible record found in this pilot.",fill="#555",font=font(20))
im.save(FIG/"ORAC_Literature_Coverage.png")

print(f"raw_records={len(records)} compounds={len(compounds)} tierA={sum(x['Tier_A_count'] for x in analysis)} tierB={sum(x['Tier_B_count'] for x in analysis)}")
