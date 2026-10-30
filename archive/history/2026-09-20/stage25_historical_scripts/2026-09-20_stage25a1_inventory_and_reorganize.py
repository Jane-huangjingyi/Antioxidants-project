from pathlib import Path
import csv, hashlib, re, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]

def stage_of(path):
    s=path.as_posix().lower()
    m=re.search(r'stage[_ -]?(\d+[a-z]?)',s)
    if m:return 'Stage '+m.group(1).upper()
    for pat,stage in [('phase3d','Stage 22'),('phase3c','Stage 21'),('phase3b','Stage 19'),('phase3a','Stage 18'),('phase2','Stage 17'),('global_top','Stage 20')]:
        if pat in s:return stage
    return 'Cross-stage / not encoded'

def classify(rel):
    s=rel.as_posix(); low=s.lower(); name=rel.name
    if name=='.gitignore': return 'ACTIVE_SUPPORTING',s,'Repository hygiene configuration retained at root.','', 'low'
    # Early-stage assets still used by the current project are recovered from the
    # legacy bundle into functional modules rather than archived merely by age.
    if 'archive/legacy_pre_class_balanced_2026-09-18/' in low:
        if low.endswith('/readme_h_orac_pipeline.md'):
            return 'ACTIVE_SUPPORTING','docs/methods/h_orac_framework/README_H_ORAC_PIPELINE.md','Current H-ORAC SOP entry retained as supporting methodology.','', 'medium'
        if '/docs/' in low and any(x in name for x in ['Antioxidant_Assay_Method_Audit','Antioxidant_Screening_Protocol_v2','Candidate_Scope_Definition','Database_and_Literature_Source_Audit','MASTER_H_ORAC_SCREENING_PIPELINE','Common_Failure_Modes_H_ORAC','Data_Provenance_Chain','H_ORAC_Pipeline_Tutorial','NO_AI_MANUAL_EXECUTION_GUIDE','Pipeline_Gaps_and_Inconsistencies','Pipeline_Script_Map','Primary_Antioxidant_Metric_Recommendation','SOP_','Stage1_vs_Stage2_Framework','Target_Evidence_Classification','Two_Reviewer_QC_Rules','Versioning_and_Audit_Rules']):
            return 'ACTIVE_SUPPORTING','docs/methods/h_orac_framework/'+name,'Early-stage method remains relevant to current H-ORAC governance.','', 'medium'
        if '/config/' in low:
            return 'ACTIVE_SUPPORTING','methods_qc/config/'+name,'Current evidence rubric or data dictionary retained for reuse.','', 'medium'
        if '/templates/' in low or '/checklists/' in low:
            folder='checklists' if '/checklists/' in low else 'templates'
            return 'ACTIVE_SUPPORTING',f'methods_qc/{folder}/'+name,'Current manual-execution template/checklist.','', 'medium'
    if low.startswith('archive/'):
        status='HISTORICAL_ONLY' if any(x in low for x in ['legacy','historical','atlas_transition','phase2_candidate']) else 'SUPERSEDED'
        return status,s,'Existing archive; retained in place.','', 'low'
    if name=='Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md': return 'ACTIVE_CANONICAL',s,'Fixed root history path.','', 'low'
    if name=='README.md': return 'ACTIVE_CANONICAL','README_CN.md','Current project entry renamed for language clarity.','', 'medium'
    if low.startswith('handoff/'):
        return 'ACTIVE_SUPPORTING','references/pending_zotero_import/'+name,'Pending reference-import asset.','', 'low'
    if low.startswith('docs/stages/'):
        return 'HISTORICAL_ONLY','archive/historical_stage_summaries/'+name,'Stage narrative retained as historical provenance.','docs/PROJECT_STAGE_INDEX_CN.md','medium'
    if low.startswith('data/'):
        if 'stage25a_' in low:
            base='data/literature_screening/'
            if 'provenance' in low: dest=base+'provenance/'+name.replace('Stage25A_','Literature_Screening_')
            elif any(x in low for x in ['shortlist','recommended']): dest=base+'shortlist/'+('Literature_Screening_Provisional_Top50.csv' if 'recommended' in low else name)
            elif any(x in low for x in ['audit','unmatched','coverage_by_stratum','search_log']): dest=base+'qc/'+name.replace('Stage25A_','Literature_Screening_')
            elif 'master' in low: dest=base+'master/Literature_Screening_Candidate_Master.csv'
            else: dest=base+'qc/'+name.replace('Stage25A_','Literature_Screening_')
            return 'ACTIVE_CANONICAL',dest,'Current unified literature-screening asset.','', 'high'
        if any(x in name for x in ['Candidate_Master','Candidate_Exclusions','Taxonomy_Relationships','Eligibility_Lock','Future_Candidate_Additions']):
            return 'ACTIVE_CANONICAL','data/candidate_universe/'+name,'Current candidate identity, taxonomy or eligibility asset.','', 'medium'
        if any(x in name for x in ['Metal_Redox','Micronutrient']): return 'ACTIVE_CANONICAL','data/metal_and_micronutrients/'+name,'Current metal/micronutrient asset.','', 'medium'
        if any(x in name for x in ['CHATGPT_SYNC','Supervisor_']): return 'ACTIVE_SUPPORTING','data/supervisor/'+name,'Supervisor/sync table.','', 'medium'
        if any(x in name for x in ['Global_Top_Overview_Master_v0.1','Global_Top_Overview_Master_v0.2','Cross_Class_Comparability_Matrix_v0.1']):
            return 'SUPERSEDED','archive/superseded_outputs/'+name,'Superseded by latest schema version.','data/class_specific_antioxidant/cross_class/'+('Global_Top_Overview_Master_v0.3.csv' if 'Global' in name else 'Cross_Class_Comparability_Matrix_v0.2.csv'),'medium'
        return 'ACTIVE_CANONICAL','data/class_specific_antioxidant/'+name,'Current class-specific evidence/ranking/profile asset.','', 'medium'
    if low.startswith('docs/'):
        if name=='PROJECT_STAGE_INDEX_CN.md': return 'ACTIVE_CANONICAL',s,'Fixed stage-history index.','', 'low'
        if 'CHATGPT_SYNC' in name or 'SYNC_MANIFEST' in name: return 'ACTIVE_SUPPORTING','docs/sync/'+name,'Current synchronization asset.','', 'medium'
        if name.startswith('Supervisor_') or 'Progress' in name: return 'ACTIVE_SUPPORTING','docs/supervisor/'+name,'Supervisor-facing report.','', 'medium'
        if any(x in name for x in ['Audit','Deduplication','Citation_Source']): return 'ACTIVE_SUPPORTING','docs/qc/'+name,'Quality-control report.','', 'medium'
        if any(x in name for x in ['Framework','Rules','Taxonomy','Why_Different','Roadmap']): return 'ACTIVE_CANONICAL','docs/methods/'+name,'Current method/taxonomy framework.','', 'medium'
        return 'ACTIVE_CANONICAL','docs/class_specific_antioxidant/'+name,'Current scientific report.','', 'medium'
    if low.startswith('figures/aqueous_antioxidant_atlas/'):
        parts=rel.parts; sub=parts[2] if len(parts)>2 else ''
        if name in ['FIGURE_INDEX_CN.md','FIGURE_INVENTORY_AUDIT.csv']: return 'ACTIVE_CANONICAL','figures/'+name,'Project-wide figure inventory/index.','', 'high'
        classmap={'00_overview':'00_overview','01_flavonoids':'01_class_specific_antioxidant_ranking/flavonoids','02_phenolic_acids':'01_class_specific_antioxidant_ranking/phenolic_acids','03_stilbenes_lignans':'01_class_specific_antioxidant_ranking/stilbenes_lignans','04_water_soluble_vitamins':'01_class_specific_antioxidant_ranking/water_soluble_vitamins','05_betalains':'01_class_specific_antioxidant_ranking/betalains','06_organosulfur':'01_class_specific_antioxidant_ranking/organosulfur','07_other_aqueous_phytochemicals':'01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals','08_metal_chelation':'02_metal_and_micronutrients/metal_redox','09_micronutrients':'02_metal_and_micronutrients/micronutrients','99_methods_qc':'99_methods_qc'}
        if sub=='10_unified_literature_screening':
            fmap={'Research_Evidence_Density':'03_unified_literature_screening/01_primary_ranking/Literature_Screening_Research_Evidence_Density_Top50.png','Publications_vs_Citations':'03_unified_literature_screening/02_metric_validation/Literature_Screening_Publication_Count_vs_Citations.png','Recent_vs_Historical':'03_unified_literature_screening/02_metric_validation/Literature_Screening_Recent_vs_Historical_Evidence.png','Shortlist_Stability':'03_unified_literature_screening/03_shortlist_stability/Literature_Screening_Shortlist_Stability_Top20_to_Top60.png','Class_Representation':'03_unified_literature_screening/04_class_representation/Literature_Screening_Class_Representation_Top20_to_Top60.png','Evidence_Domain_Breadth':'03_unified_literature_screening/05_evidence_breadth/Literature_Screening_Evidence_Domain_Breadth_Top30.png'}
            dest=next(v for k,v in fmap.items() if k in name)
            return 'ACTIVE_CANONICAL','figures/aqueous_antioxidant_atlas/'+dest,'Current literature-screening figure; scientific-content filename.','', 'high'
        return 'ACTIVE_CANONICAL','figures/aqueous_antioxidant_atlas/'+classmap.get(sub,sub)+'/'+name,'Current aqueous Atlas figure/status.','', 'high'
    if low.startswith('figures/'):
        # Earlier non-aqueous/current-framework graphics remain supporting assets.
        if any(x in name for x in ['Global_Overview','Cross_Class','Carotenoid','VitaminE','Vitamins_Parent']): mod='cross_class_and_lipid_supporting'
        elif any(x in name for x in ['Candidate_Universe','Taxonomy']): mod='candidate_universe'
        elif any(x in name for x in ['Flavonoid','PhenolicAcid']):
            return 'SUPERSEDED','archive/superseded_outputs/figures/'+name,'Superseded by current aqueous Atlas canonical figure.','figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/','medium'
        else: mod='supervisor'
        return 'ACTIVE_SUPPORTING','figures/'+mod+'/'+name,'Supporting current framework or paused lipid branch.','', 'medium'
    if low=='r/plot_antioxidant_atlas.r': return 'SUPERSEDED','archive/R_legacy/plot_antioxidant_atlas_pre_modularization.R','Superseded after modular scripts reproduce active figures.','R/render_all_active_figures.R','high'
    return 'ACTIVE_SUPPORTING',s,'Retained supporting asset; no safer automated consolidation rule.','HUMAN REVIEW REQUIRED — FILE CONSOLIDATION','high'

def inventory():
    paths=[]
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True,encoding='utf-8').splitlines()
    other=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True,encoding='utf-8').splitlines()
    for item in sorted(set(tracked+other)):
        rel=Path(item)
        if rel.as_posix()=='PROJECT_FILE_MIGRATION_MAP.csv' or '__pycache__' in rel.parts: continue
        p=ROOT/rel
        if not p.is_file(): continue
        status,new,reason,repl,risk=classify(rel)
        paths.append(dict(old_path=rel.as_posix(),original_stage=stage_of(rel),scientific_role=reason,status_class=status,proposed_new_path=new,canonical_replacement=repl,reason=reason,dependency_risk=risk))
    return paths

def write_map(rows):
    out=ROOT/'PROJECT_FILE_MIGRATION_MAP.csv'
    with out.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print({'inventory_files':len(rows),'migration_map':str(out),'human_review':sum('HUMAN REVIEW' in r['canonical_replacement'] for r in rows)})

def execute(rows):
    # Moves are literal and auditable; existing archive files remain in place.
    for r in rows:
        old=ROOT/r['old_path']; new=ROOT/r['proposed_new_path']
        if old==new or not old.exists(): continue
        new.parent.mkdir(parents=True,exist_ok=True)
        if new.exists(): raise RuntimeError(f'Collision: {new}')
        shutil.move(str(old),str(new))

if __name__=='__main__':
    rows=inventory();write_map(rows)
    if '--execute' in sys.argv: execute(rows);print('migration executed')
