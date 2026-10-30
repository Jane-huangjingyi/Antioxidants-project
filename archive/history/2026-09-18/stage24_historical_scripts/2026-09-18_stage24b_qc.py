from pathlib import Path
import csv, hashlib

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'/'aqueous_antioxidant_atlas'
ARCH=ROOT/'archive'/'figure_redundancy_stage24'
errors=[]
def check(ok,msg):
    if not ok: errors.append(msg)

active=sorted(FIG.rglob('*.png'))
archived=sorted(ARCH.rglob('*.png'))
check(len(active)==23,f'active PNG count={len(active)}, expected 23')
check(len(archived)==10,f'archived PNG count={len(archived)}, expected 10')
hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in active]
check(len(hashes)==len(set(hashes)),'active folder contains exact duplicate PNGs')
check(not any(x in p.name.lower() for p in active for x in ['carotenoid','tocopher','vitamine','lipid']), 'lipid-phase figure in active aqueous folder')

with (FIG/'FIGURE_INVENTORY_AUDIT.csv').open(encoding='utf-8-sig',newline='') as f: inventory=list(csv.DictReader(f))
required_inventory=['figure_file','folder','class','figure_type','primary_message','source_data','x_variable','y_variable','encoded_variables','audience','duplicated_with','redundancy_level','retain_or_archive','canonical_replacement','reason','notes']
check(list(inventory[0])==required_inventory,'inventory columns differ from specification')
check(len(inventory)==33,f'inventory rows={len(inventory)}, expected 33')
check({r['redundancy_level'] for r in inventory} <= {'unique','partially_redundant','highly_redundant','exact_duplicate'},'invalid redundancy level')
check(sum(r['retain_or_archive']=='archive' for r in inventory)==10,'inventory archive decisions must equal 10')
check(sum(r['redundancy_level']=='exact_duplicate' for r in inventory)==1,'exact duplicate count must equal 1')
check(sum(r['redundancy_level']=='highly_redundant' for r in inventory)==7,'high redundancy count must equal 7')
check(sum(r['redundancy_level']=='partially_redundant' for r in inventory)==2,'partial redundancy count must equal 2')

with (ARCH/'ARCHIVED_FIGURES_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as f: manifest=list(csv.DictReader(f))
check(len(manifest)==12,'archive manifest must contain 10 PNGs plus 2 derived status summaries')
for r in manifest:
    check((ROOT/r['archived_file']).exists(),f"missing archived file: {r['archived_file']}")
    check(bool(r['redundancy_reason']) and bool(r['canonical_replacement']),'archive row lacks reason or replacement')

index=(FIG/'FIGURE_INDEX_CN.md').read_text(encoding='utf-8')
check(index.count('\n## `')==23,'Figure Index does not describe all 23 canonical figures')
for p in active:
    check(p.relative_to(FIG).as_posix() in index,f'active figure absent from index: {p.name}')

with (ROOT/'data'/'CHATGPT_SYNC_FILES_STAGE24.csv').open(encoding='utf-8-sig',newline='') as f: sync=list(csv.DictReader(f))
check({r['upload_to_chatgpt'] for r in sync} <= {'yes','optional','no'},'invalid upload_to_chatgpt value')
for r in sync:
    if r['upload_to_chatgpt'] in {'yes','optional'}:
        check((ROOT/r['file_path']).exists(),f"sync manifest path missing: {r['file_path']}")

rscript=(ROOT/'R'/'plot_antioxidant_atlas.R').read_text(encoding='utf-8')
check('GENERATE_LEGACY_FIGURES <- FALSE' in rscript,'legacy figure generation is not disabled')
for forbidden in ['"Aqueous_Antioxidant_Class_Overview"','"Aqueous_Class_Ranking_Leaders"','"Stilbenes_Lignans_Evidence_Confidence"','"Other_Aqueous_Evidence_Confidence"','"Metal_Chelation_Evidence_Overview"']:
    check(forbidden not in rscript,f'R script still writes archived figure {forbidden}')
check('"Metal_Chelation_or_Fenton_Evidence_Profile"' in rscript,'R script does not generate canonical metal profile')

required_docs=['docs/CHATGPT_SYNC_MANIFEST_STAGE24.md','docs/Stage24B_Figure_Deduplication_Report_CN.md']
for rel in required_docs: check((ROOT/rel).exists(),f'missing required document: {rel}')
for folder in sorted(p for p in FIG.iterdir() if p.is_dir()):
    check(any(folder.iterdir()),f'empty active folder: {folder.name}')

if errors: raise SystemExit('STAGE 24B QC FAILED\n- '+'\n- '.join(errors))
print('STAGE 24B QC PASSED')
print({'inventory':len(inventory),'canonical_png':len(active),'archived_png':len(archived),'manifest_rows':len(manifest),'sync_rows':len(sync)})
