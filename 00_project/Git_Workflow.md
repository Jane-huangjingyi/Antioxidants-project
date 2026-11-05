# Git workflow and branch interpretation

The current working branch is `codex/food-candidate-manuscript-workflow-20261105`. The reorganization starts from `c6bca4d13e33cf2ce7d1bae7e3d45e69cf4b23b4`; the earlier review, governance and Track B branches are contained in that baseline. Their approvals and HOLD states remain as recorded. A branch name is not a scientific approval.

## Current handling

Use the current workflow branch as the single active checkout for this task. Do not merge each old branch again: the branch inventory reports whether its tip is already an ancestor. Preserve old branch names as traceable milestones; none is deleted automatically. The new organization is committed once after QC.

At audit, local main pointed to `d29a6936603886e654b3cdfb24ccd3a1e76cee23`. Main was older than the reviewed working chain. This task does not silently merge or reset main, change remote defaults, or authorize database migration. After explicit integration approval, a fast-forward is sufficient if main has not diverged:

```sh
git fetch origin
git switch main
git merge --ff-only codex/food-candidate-manuscript-workflow-20261105
git push origin main
```

Those integration commands are instructions, not operations performed by this task. If `--ff-only` fails, inspect divergence and resolve deliberately; do not force-push. For a fresh clone before main integration:

```sh
git switch --track origin/codex/food-candidate-manuscript-workflow-20261105
python run_pipeline.py --tables-only
```

Future changes should use one purpose-specific branch from the agreed current authority, retain source baselines, and commit only reviewed scope. See `07_quality_control/branch_inventory.json` for actual tips and containment.
