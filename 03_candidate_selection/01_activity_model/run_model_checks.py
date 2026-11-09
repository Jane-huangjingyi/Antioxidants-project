"""Reproduce model preparation and exploratory comparisons offline; no network or ranking."""
import subprocess,sys,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
steps=[('audit_protocol_lineage.py',[]),('check_model_protocol.py',[]),('build_extended_model_inputs.py',[]),('map_flavonoid_labels.py',[]),('audit_flavonoid_structures.py',[]),('audit_stereochemistry.py',[]),('build_scaffold_groups.py',[]),('validate_scaffold_baseline.py',[]),('validate_scaffold_baseline.py',['--augmented']),('validate_scaffold_baseline.py',['--fingerprint']),('diagnose_scaffold_errors.py',[]),('audit_catechin_and_external_sources.py',[]),('assess_external_comparability.py',[]),('run_retrospective_pressure_test.py',[]),('build_external_validation_readiness.py',[]),('build_analysis_set.py',[]),('complete_exploratory_model.py',[])]
for script,args in steps:subprocess.run([sys.executable,str(P/script),*args],check=True)
subprocess.run([sys.executable,str(P.parents[1]/'06_manuscript/code/build_manuscript_outputs.py')],check=True)
if '--figures' in sys.argv:
    rscript=shutil.which('Rscript')
    if not rscript:
        candidates=sorted(Path('C:/Program Files/R').glob('R-*/bin/Rscript.exe'))
        if candidates:rscript=str(candidates[-1])
    if not rscript:raise RuntimeError('Rscript required for --figures; install R or add Rscript to PATH')
    subprocess.run([rscript,str(P.parents[1]/'05_analysis/R/render_model_diagnostics.R')],check=True)
print('Offline exploratory modelling reproduction PASS; formal primary/global ranking remains unsupported.')
