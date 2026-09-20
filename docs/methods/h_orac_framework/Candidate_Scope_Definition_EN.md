# Antioxidants Project Candidate Scope Definition (Frozen)

## 1. Main-candidate eligibility

A main candidate must satisfy all of the following: it occurs naturally in foods, beverages, or common culinary spices consumed in normal diets; it has one defined chemical structure; it is an individually quantifiable small molecule; it maps uniquely to a PubChem CID and InChIKey; and it has traceable food occurrence. Uncharacterized extracts, mixtures, compounds obtained mainly from medicinal plants or supplements, substances whose main source is endogenous human synthesis, and elements or materials without one molecular structure are excluded from the main list. Metabolites, conjugates, and gut-microbial products remain in a secondary layer and do not compete with dietary parent compounds.

“Antioxidant” is a functional property, not a chemical class. Classification follows chemical skeletons, while ORAC compatibility is a parallel measurement attribute. Phenolic acids are a subclass of phenolic compounds and are not an independent top-level class competing with polyphenols. The project uses `Polyphenolic / phenolic compounds` as the top level, followed by flavonoids, phenolic acids, stilbenes, lignans, and related subclasses.

## 2. Frozen chemical taxonomy

| chemical class | subclass | example compounds | reason for inclusion |
|---|---|---|---|
| Polyphenolic / phenolic compounds | flavan-3-ols / catechins | catechin, epicatechin, EGCG, EGC, ECG | Common tea, cocoa, and fruit compounds with traceable structures and occurrence |
| Polyphenolic / phenolic compounds | flavonols | quercetin, kaempferol, myricetin | Widely present in fruit, vegetables, tea, and spices |
| Polyphenolic / phenolic compounds | flavones | apigenin, luteolin | Present in celery, parsley, herbs, and other foods |
| Polyphenolic / phenolic compounds | flavanones | hesperetin, naringenin, and defined glycosides | Common in citrus; glycosides and aglycones are separate entities |
| Polyphenolic / phenolic compounds | anthocyanidins / anthocyanins | cyanidin and cyanidin-3-O-glucoside | Common in berries and colored produce; aglycones and glycosides are not pooled |
| Polyphenolic / phenolic compounds | isoflavones | genistein, daidzein | Clear exposure from soy foods |
| Polyphenolic / phenolic compounds | phenolic acids / hydroxybenzoic acids | gallic, protocatechuic, vanillic acids | Broad food occurrence and defined single structures |
| Polyphenolic / phenolic compounds | phenolic acids / hydroxycinnamic acids | caffeic, ferulic, p-coumaric acids | Common in coffee, grains, fruit, and vegetables |
| Polyphenolic / phenolic compounds | hydroxycinnamic-acid conjugates | chlorogenic acid (5-O-caffeoylquinic acid) | Important dietary phenolic ester; defined isomers are separate |
| Polyphenolic / phenolic compounds | stilbenes | trans-resveratrol | Occurs in grapes, peanuts, and berries; cis/trans forms remain separate |
| Polyphenolic / phenolic compounds | lignans | secoisolariciresinol, matairesinol | Clear whole-grain, seed, and plant-food sources |
| Polyphenolic / phenolic compounds | other defined food phenolics | curcumin, capsaicin, carvacrol | Included only with normal culinary exposure and a defined structure |
| Vitamins / vitamin-like dietary antioxidants | vitamin C / ascorbic acid | L-ascorbic acid | Clear normal dietary source; oxidized forms are separate entities |
| Vitamins / vitamin-like dietary antioxidants | tocopherols | alpha-, gamma-, delta-tocopherol | Common in edible oils, nuts, and seeds; isomers/stereochemistry are separate |
| Vitamins / vitamin-like dietary antioxidants | tocotrienols | alpha-, gamma-, delta-tocotrienol | Present in grains and selected edible oils; homologues are separate |
| Carotenoids | carotenes | beta-carotene, lycopene, alpha-carotene | Common in produce; lipophilicity and isomerism require structured fields |
| Carotenoids | xanthophylls | lutein, zeaxanthin, beta-cryptoxanthin | Common in leafy vegetables, egg yolk, and fruit |
| Organosulfur compounds | isothiocyanates | sulforaphane | Real crucifer exposure; principal mechanisms may not be captured by ORAC |
| Organosulfur compounds | thiosulfinates / related sulfur compounds | allicin and defined degradation products | Allium-derived, but stability and exact entity require verification |
| Other food-derived antioxidant small molecules | betalains | betanin, indicaxanthin | Food-derived from beet/cactus fruit; optical interference requires QC |
| Other food-derived antioxidant small molecules | quinones | ubiquinone forms only when dietary parent exposure is meaningful | Dietary exposure must be separated from endogenous synthesis; usually extended list |
| Other food-derived antioxidant small molecules | nitrogen-containing phytochemicals | betalain alkaloids, capsaicinoids, or other defined entities | Included only with a defined structure and normal food exposure |

## 3. ORAC compatibility strata

### H-ORAC-compatible / predominantly hydrophilic

Most flavan-3-ols, flavonols, flavones, flavanones, anthocyanins, isoflavones, phenolic acids, L-ascorbic acid, and other water-soluble compounds preferentially enter H-ORAC. Solubility, pH, salt form, glycosylation, and fluorescence interference remain compound-specific checks; polyphenol membership does not guarantee an artifact-free assay.

### L-ORAC-compatible / predominantly lipophilic

Tocopherols, tocotrienols, carotenes, xanthophylls, and other strongly lipophilic compounds preferentially enter L-ORAC. RMCD, cosolvent, solvent fraction, and inclusion conditions must be recorded. L-ORAC is ranked only within a comparable arm and is not pooled with H-ORAC without bridging validation.

### Technically problematic / special-case

Poorly water-soluble phenolics such as resveratrol may depend on cyclodextrin or cosolvent. Ascorbic acid is vulnerable to rapid oxidation during preparation. Tocopherols require locked natural/synthetic stereochemistry and RMCD complexation. Carotenoids are vulnerable to incomplete dissolution, aggregation, isomerization, photodegradation, oxygen tension, absorbance, and inner-filter effects. Betalains can cause strong absorbance/fluorescence interference. Organosulfur compounds often act through thiol exchange, electrophilic sensing, or Nrf2-related mechanisms. A special-case label is a QC requirement rather than an exclusion and acknowledges that ORAC may underestimate or distort activity.

## 4. Explicit main-list exclusions

The main list excludes crude food/plant extracts, multicomponent mixtures, operational totals such as “total polyphenols,” proteins, polysaccharides and structurally heterogeneous polymers, mineral elements without one structure, endogenous glutathione or uric acid as main candidates, human metabolites and conjugates, compounds requiring medicinal plants or supplements for meaningful exposure, and compounds supported only by docking/network predictions without genuine food occurrence. These may remain as context, metabolite, extended, or interaction nodes.

## 5. Pilot scope

The frozen pilot contains 17 entities: EGCG, catechin, epicatechin, quercetin, kaempferol, gallic acid, caffeic acid, ferulic acid, chlorogenic acid, trans-resveratrol, L-ascorbic acid, alpha-tocopherol, gamma-tocopherol, lycopene, beta-carotene, lutein, and sulforaphane. They comprise 10 phenolic/polyphenolic, 3 vitamin/vitamin-like, 3 carotenoid, and 1 organosulfur candidate. Expected assay assignment is 11 H-ORAC, 5 L-ORAC, and 1 noncanonical special case. Eight candidates also carry at least one technical special-case flag, so assay arm and special-case status are not mutually exclusive fields.
