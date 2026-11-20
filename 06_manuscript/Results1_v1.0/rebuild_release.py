"""One-command figure and table regeneration without touching the frozen inputs."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
from build_results1 import HERE, ROOT

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()
output = str(a.out.resolve())
for cmd in ([sys.executable, str(HERE/"build_results1.py"), "--out", output],
            [os.environ.get("RESULTS1_RSCRIPT","Rscript"), str(HERE/"render_figure1.R"),output],
            [os.environ.get("RESULTS1_NODE","node"),str(HERE/"build_table1.mjs"),output]):
    subprocess.run(cmd, cwd=ROOT, check=True)
