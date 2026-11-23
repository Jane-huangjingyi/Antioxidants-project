"""One root command runs the research steps. Network discovery and human decisions remain explicit."""
from pathlib import Path
import argparse,subprocess,sys,shutil,os
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--tables-only',action='store_true')
p.add_argument('--legacy-figures',action='store_true')
p.add_argument('--workbook',action='store_true')
p.add_argument('--literature',action='store_true',help='Replay the current search-to-ranking workflow using local source exports')
a=p.parse_args()
if a.literature:
 if a.tables_only or a.legacy_figures or a.workbook:
  p.error('--literature runs the literature workflow by itself')
 literature_steps = [
  '01_candidate_discovery/code/01_build_universe.py',
  '02_identity_and_evidence/code/01_build_evidence_profiles.py',
  '03_candidate_selection/code/01_fit_orac_fl.py',
  '02_identity_and_evidence/code/02_screen_public_snapshot.py',
  '02_identity_and_evidence/code/03_summarize_screening.py',
  '03_candidate_selection/code/02_validate_and_rank.py',
  '03_candidate_selection/code/04_build_figure1_ranks.py',
  '02_identity_and_evidence/code/04_build_fulltext_batches.py',
  '06_manuscript/code/03_build_working_results.py',
  '07_quality_control/code/02_validate_workflow.py',
 ]
 for script in literature_steps:
  subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
 raise SystemExit(0)
steps=['01_candidate_discovery/code/01_build_universe.py','02_identity_and_evidence/code/01_build_evidence_profiles.py','03_candidate_selection/01_activity_model/audit_data.py','03_candidate_selection/01_activity_model/build_source_followup.py','03_candidate_selection/01_activity_model/audit_model_design.py','03_candidate_selection/01_activity_model/build_traceable_evidence.py','03_candidate_selection/01_activity_model/audit_legacy_coverage.py','03_candidate_selection/01_activity_model/reconcile_legacy30.py','03_candidate_selection/01_activity_model/build_bridge_protocol_matrix.py','03_candidate_selection/01_activity_model/build_bridge_error_audit.py','03_candidate_selection/01_activity_model/build_food_form_followup.py','03_candidate_selection/01_activity_model/build_analysis_entry.py','03_candidate_selection/01_activity_model/audit_comparison_identity.py','03_candidate_selection/code/select_candidates.py','04_05_experimental_validation/code/01_build_endpoint_comparison.py','04_05_experimental_validation/code/02_capacity_formula.py','06_manuscript/code/01_build_manuscript_outputs.py']
for script in steps:subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
if not a.tables_only:
 r=shutil.which('Rscript')
 if not r and os.name=='nt':
  found=sorted(Path('C:/Program Files/R').glob('R-*/bin/Rscript.exe'));r=str(found[-1]) if found else None
 if not r:raise SystemExit('Tables completed. Install R with ggplot2/svglite, or use --tables-only.')
 subprocess.run([r,'04_05_experimental_validation/code/figure_support/render_manuscript_figures.R'],cwd=ROOT,check=True)
 if a.legacy_figures:subprocess.run([r,'04_05_experimental_validation/code/figure_support/render_historical_figures.R'],cwd=ROOT,check=True)
if a.workbook:
 node=shutil.which('node')
 if not node:raise SystemExit('Core workflow complete. Optional workbook needs Node and @oai/artifact-tool; see 00_project/Environment.md.')
 subprocess.run([node,'00_project/exporters/build_review_workbook.mjs'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'07_quality_control/code/01_build_indexes.py'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'07_quality_control/code/02_validate_workflow.py'],cwd=ROOT,check=True)
