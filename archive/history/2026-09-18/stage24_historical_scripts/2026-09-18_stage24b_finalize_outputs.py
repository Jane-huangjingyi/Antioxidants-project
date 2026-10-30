from pathlib import Path
from datetime import date
import csv

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'/'aqueous_antioxidant_atlas'
ARCH=ROOT/'archive'/'figure_redundancy_stage24'
inv_path=FIG/'FIGURE_INVENTORY_AUDIT.csv'
with inv_path.open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
for row in rows:
    if 'class_name' in row:
        row['class']=row.pop('class_name')
fields=['figure_file','folder','class','figure_type','primary_message','source_data','x_variable','y_variable','encoded_variables','audience','duplicated_with','redundancy_level','retain_or_archive','canonical_replacement','reason','notes']
with inv_path.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

manifest_path=ARCH/'ARCHIVED_FIGURES_MANIFEST.csv'
with manifest_path.open(encoding='utf-8-sig',newline='') as f:
    manifest=list(csv.DictReader(f))
existing={r['original_location'] for r in manifest}
for panel in ['03_stilbenes_lignans','07_other_aqueous_phytochemicals']:
    original=f'figures/aqueous_antioxidant_atlas/{panel}/Class_Status_Summary.md'
    if original not in existing:
        manifest.append(dict(archived_file=f'archive/figure_redundancy_stage24/{panel}/Class_Status_Summary.md',original_location=original,redundancy_reason='derived summary redundant with active quantitative class figures and canonical Figure Index',canonical_replacement='figures/aqueous_antioxidant_atlas/FIGURE_INDEX_CN.md',date_archived=date.today().isoformat(),reproducible_from_R='no',notes='No scientific data removed.'))
with manifest_path.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(manifest[0]));w.writeheader();w.writerows(manifest)

by_rel={r['figure_file']:r for r in rows}
by_rel['08_metal_chelation/Metal_Chelation_or_Fenton_Evidence_Profile.png']=by_rel['08_metal_chelation/Fe_Cu_Fenton_Suppression_Profile.png'].copy()
by_rel['08_metal_chelation/Metal_Chelation_or_Fenton_Evidence_Profile.png']['figure_file']='08_metal_chelation/Metal_Chelation_or_Fenton_Evidence_Profile.png'
constructs={
 'Flavonoids':'H-ORAC-FL (mol TE/mol compound)','Phenolic acids / conjugates':'H-ORAC-FL (mol TE/mol compound)',
 'Stilbenes / lignans':'H-ORAC-FL (mol TE/mol compound)','Vitamin C aqueous':'H-ORAC-FL; singleton evidence summary',
 'Betalains / nitrogen-containing':'LOX-FL and MPO/HOCl assay-specific profile','Organosulfur':'KEAP1/NRF2, thiol chemistry, Fenton and radical-kinetic profile',
 'Other aqueous phytochemicals':'H-ORAC-FL coherent subpanel or assay-specific profile','Metal-ion mechanisms':'Chelation/reduction/Fenton-context profile',
 'Micronutrients':'Cofactor and dose-dependent redox-context profile','Metal/context':'Conceptual metal-redox mechanism framework',
 'Overview':'Within-panel position or counts; no shared raw construct'}
active=sorted(p.relative_to(FIG).as_posix() for p in FIG.rglob('*.png'))
lines=['# Aqueous Antioxidant Atlas — Canonical Figure Index（Stage 24B）','',
       '本索引仅列 active canonical figures。原则为 `one scientific message → one canonical figure`；被替代图见 `archive/figure_redundancy_stage24/ARCHIVED_FIGURES_MANIFEST.csv`。所有数值仍为 class/subpanel-specific，不形成 global antioxidant score。','']
for rel in active:
    r=by_rel[rel]; cls=r['class']; construct=constructs.get(cls,'Class-specific construct')
    superseded=[x['figure_file'] for x in rows if rel in x.get('canonical_replacement','')]
    caveat='Class-specific construct; raw values must not be compared across incompatible panels.'
    lines += [f'## `{rel}`','',f'- **Class：**{cls}',f'- **Scientific question：**{r["primary_message"]}',f'- **Source data：**{r["source_data"]}',f'- **Primary construct：**{construct}',f'- **Main message：**{r["primary_message"]}','- **Why retained：**该图提供独立信息，不能由另一张 active 图完整替代。',f'- **Supersedes：**{"; ".join(superseded) if superseded else "None"}',f'- **Major caveat：**{caveat}',f'- **Recommended use：**{r["audience"]}','']
(FIG/'FIGURE_INDEX_CN.md').write_text('\n'.join(lines),encoding='utf-8')

report=ROOT/'docs'/'Stage24B_Figure_Deduplication_Report_CN.md'
text=report.read_text(encoding='utf-8')
text=text.replace('归档重复图 **10**，其中', '归档重复图 **10**，另归档重复derived status summaries **2**；其中')
report.write_text(text,encoding='utf-8')
print({'inventory_rows':len(rows),'canonical_png':len(active),'archive_manifest_rows':len(manifest)})
