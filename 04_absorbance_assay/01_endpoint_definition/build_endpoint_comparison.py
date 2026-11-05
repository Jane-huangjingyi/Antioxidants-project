"""Build the endpoint comparison from explicit source-linked method interpretations."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
HERE=Path(__file__).resolve().parent
rows=read_json(HERE/'method_candidates.json')
assert len(rows)==4 and all(r['approval']=='NOT_APPROVED' for r in rows)
write_csv(HERE/'results/Endpoint_Method_Comparison.csv',rows)
print('04.1: four endpoint definitions compared; no assay or parameters approved.')
