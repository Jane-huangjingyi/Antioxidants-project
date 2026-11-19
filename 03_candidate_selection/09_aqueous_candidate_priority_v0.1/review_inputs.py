# Candidate decisions remain editable before rebuilding the workbooks.
PANEL = [
("AFF-0001","A","Flavanol","Stable multi-source FL signal and matched stereochemical contrast","Confirm (+) isomer and hydrate basis; stock oxidation and background","10.1016/j.heliyon.2024.e35819","Green tea infusion HPLC-DAD"),
("AFF-0002","A","Flavanol","Multi-paper flavanol comparator with method-dependent response","Confirm (-) isomer, stock and final-well stability","10.1016/j.heliyon.2024.e35819","Green tea infusion HPLC-DAD"),
("AFF-0060","A","Hydroxybenzoic acid","High within-source FRAP and DPPH response; small phenolic comparator","Check oxidation, pH drift and probe-only response","10.1016/j.heliyon.2024.e35819","Green tea infusion HPLC-DAD"),
("AFF-0076","A","Caffeoylquinic ester","Multiple FL papers and a distinct ester comparator","Confirm 5-CQA nomenclature and isomer/pH stability","10.1016/j.foodchem.2007.05.091","Commercial brewed coffee HPLC, 5-CQA"),
("AFF-0104","A","Ascorbate","Nonphenolic comparator with measured FL response; priority reflects chemistry coverage","Use L form; test oxidation over the full run and direct probe response","10.3390/s8117097","Orange HPLC-electrochemical analysis"),
("NEW-GSH","A","Reduced thiol peptide","Mechanistically distinct comparator with food-occurrence and FL records","Reduced GSH only; verify oxidation, pH and probe interaction","10.1080/01635589209514173","Primary abstract, HPLC analysis of foods"),
("AFF-0009","B","Flavonol","Strong, stable conditional FL signal; a useful high-response challenge","Verify final-well solubility and dihydrate vs anhydrous dosage; probe/color blank","", ""),
("AFF-0031","B","Flavanone","High conditional FL position and weak PGR response illustrate probe dependence","Native free-form food evidence and vehicle/solubility","", ""),
("AFF-0061","B","Hydroxybenzoic acid","Strong primary FRAP/DPPH and conditional FL response","Verify exact food occurrence; check pH and redox interference","", ""),
("AFF-0069","B","Hydroxycinnamic acid","Multiple original FL sources and distinct catechol acid","Confirm native free form in an edible matrix, stock oxidation and solvent","", ""),
("AFF-0084","B","Hydroxycinnamic ester","High conditional FL location driven by one DOI","Independent molar measurement; confirm food material and concentration scale","", ""),
("AFF-0003","B","Gallated flavanol","Dietary and multi-source activity evidence; gallate contrast","Confirm exact form and oxidation/alkaline instability","10.1016/j.heliyon.2024.e35819","Green tea infusion HPLC-DAD"),
("AFF-0006","B","Flavanol","High conditional FL position with single-source leverage","Check optical isomer; require compatible independent source","10.1021/jf000026+","(+)-Gallocatechin in HPLC food survey"),
("AFF-0005","B","Flavanol","Galloylation contrast with EGCG","Verify (-) stereoisomer and independent aqueous evidence","10.1021/jf000026+","(-)-Epigallocatechin in HPLC food survey"),
("AFF-0010","B","Flavonol","Cross-method structural contrast with quercetin","Confirm material and buffer solubility; qualify native form","10.35219/foodtechnology.2024.1.01","Green tea infusion HPLC"),
("AFF-0011","B","Flavonol","Marked response change across protocols is useful for verification","Check oxidation, solvent and exact food form","", ""),
("AFF-0017","B","Flavonol glycoside","Aglycone/glycoside comparison with quercetin","Hydrate basis, dissolved stock and optical background","10.35219/foodtechnology.2024.1.01","Tea infusion quercetin-3-rhamnosylglucoside lead"),
("AFF-0036","B","Flavanone glycoside","Glycoside contrast with hesperetin","Confirm exact glycoside and aqueous dissolution","", ""),
("AFF-0070","B","Hydroxycinnamic acid","Useful methoxy contrast in shared-dose and reducing assays","Confirm trans form; separate free and bound food occurrence","", ""),
("AFF-0071","B","Hydroxycinnamic acid","Lower-response phenolic contrast in FRAP/DPPH","Confirm trans form, native occurrence and solvent","", ""),
("AFF-0072","B","Hydroxycinnamic acid","Methoxy series contrast in shared ORAC-FL panels","Check native free form, material and vehicle","", ""),
("AFF-0030","B","Flavanone","Distinct FL/PGR and ABTS responses in published panels","Aglycone occurrence, final solubility and optical response pending","", ""),
("AFF-0045","C","Anthocyanin","Useful later optical-interference challenge","High priority color/pH and chloride basis check before kinetic ranking","", ""),
("AFF-0100","C","Lignan","Separate single-source conditional FL component; sesame evidence lead","Aqueous solubility and independent overlapping assay bridge unresolved","10.1007/s13197-014-1334-6","Sesame-oil isolated sesamin; prior partial source audit"),
]
# Selected, explicitly scoped original-table transcriptions.
# 2026 Table 1: name, FRAP µmol Trolox eq/mg, SD, DPPH SC50 µg/mL, SD.
PANEL_2026 = [
("AFF-0061",6.69,.04,1.18,.03),("AFF-0060",11.29,.05,.67,.06),
("AFF-0076",2.85,.01,2.38,.04),("AFF-0070",3.22,.01,4.87,.11),
("AFF-0071",.20,0,1569.81,12.63),("AFF-0069",4.76,.02,2.27,.08),
("AFF-0009",5.98,.03,1.40,.03),("AFF-0017",1.23,.01,3.90,.09),
("AFF-0011",.17,0,27.54,.87),("AFF-0002",2.69,.02,1.48,.07),
("AFF-0021",1.27,.01,5.45,.10),("AFF-0031",.30,0,192.56,17.55),
]
# 2016 Table 3: ABTS, FRAP, DPPH columns, each expressed relative to Myr-3-glc.
PANEL_2016 = [
("AFF-0001",1.888,1.255,1.146),("AFF-0002",2.081,1.082,.178),
("AFF-0031",.659,.057,.079),("AFF-0036",.769,.031,.016),
("AFF-0030",.326,0,0),("AFF-0022",.576,0,0),("AFF-0010",.778,.852,.427),
("AFF-0011",2.170,2.105,1.349),("AFF-0009",1.743,2.945,1.470),
("AFF-0017",.688,1.188,1.050),("AFF-0060",1.903,1.503,1.098),
("AFF-0069",.628,1.813,.763),("AFF-0071",.335,0,.011),
("AFF-0070",.759,.419,.370),("AFF-0104",.629,.666,.457),
]
# 2008 Table 3: normal, non-incubated CUPRAC and ABTS/persulfate slope ratios.
PANEL_2008 = [
    ("AFF-0011",4.27,3.43),("AFF-0009",5.49,3.21),("AFF-0010",1.47,.86),
    ("AFF-0017",2.56,1.15),("AFF-0022",.27,.65),("AFF-0021",2.90,1.01),
    ("AFF-0001",3.09,3.14),("AFF-0036",.97,1.40),("AFF-0031",.99,1.11),
    ("AFF-0060",2.62,3.48),("AFF-0084",5.65,2.30),("AFF-0070",1.20,2.16),
    ("AFF-0071",.55,1.63),("AFF-0069",2.89,1.39),("AFF-0076",2.47,1.21),
    ("AFF-0104",1.00,1.15),
]
