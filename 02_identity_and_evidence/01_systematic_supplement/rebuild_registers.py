"""Offline regeneration of coverage, article registers and recall checks."""
from pathlib import Path
import csv,subprocess,sys
import retrieve
HERE=Path(__file__).resolve().parent

def run():
 with (retrieve.ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as handle:profiles=list(csv.DictReader(handle))
 retrieve.EXPANDED=False;retrieve.OUTPUT=HERE/'inputs';retrieve.audit(profiles)
 retrieve.EXPANDED=True;retrieve.OUTPUT=HERE/'inputs/expanded_capacity';retrieve.audit(profiles)
 for script in ['build_screening_register.py','merge_historical_register.py','audit_known_sources.py']:
  subprocess.run([sys.executable,str(HERE/script)],check=True)
if __name__=='__main__':run()
