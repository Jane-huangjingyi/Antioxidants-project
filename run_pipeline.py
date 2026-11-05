"""One root command runs the research steps. Network discovery and human decisions remain explicit."""
from pathlib import Path
import argparse,subprocess,sys,shutil,os
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--tables-only',action='store_true');p.add_argument('--legacy-figures',action='store_true');p.add_argument('--workbook',action='store_true');a=p.parse_args()
steps=['01_candidate_discovery/code/build_universe.py','02_identity_and_evidence/code/build_evidence_profiles.py','03_candidate_selection/01_activity_model/audit_data.py','03_candidate_selection/01_activity_model/build_source_followup.py','03_candidate_selection/01_activity_model/audit_model_design.py','03_candidate_selection/code/select_candidates.py','04_absorbance_assay/01_endpoint_definition/build_endpoint_comparison.py','04_absorbance_assay/01_endpoint_definition/capacity_formula.py','06_manuscript/code/build_manuscript_outputs.py']
for script in steps:subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
if not a.tables_only:
 r=shutil.which('Rscript')
 if not r and os.name=='nt':
  found=sorted(Path('C:/Program Files/R').glob('R-*/bin/Rscript.exe'));r=str(found[-1]) if found else None
 if not r:raise SystemExit('Tables completed. Install R with ggplot2/svglite, or use --tables-only.')
 subprocess.run([r,'05_analysis/R/render_manuscript_figures.R'],cwd=ROOT,check=True)
 if a.legacy_figures:subprocess.run([r,'05_analysis/render_historical_figures.R'],cwd=ROOT,check=True)
if a.workbook:
 node=shutil.which('node')
 if not node:raise SystemExit('Core workflow complete. Optional workbook needs Node and @oai/artifact-tool; see 00_project/Environment.md.')
 subprocess.run([node,'00_project/exporters/build_review_workbook.mjs'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'07_quality_control/code/build_indexes.py'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'07_quality_control/code/validate_workflow.py'],cwd=ROOT,check=True)
