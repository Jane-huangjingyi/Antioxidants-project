# Reproduced archive cleanup

Date: 2026-11-05. The researcher authorized removal of reproduced archived outputs after reviewing the current organization.

Removed 109 generated graphic files (6,630,126 bytes). Every removed file has the same SHA256 as its retained PNG or SVG registered under `06_manuscript/figures`. This includes 102 old editable exports and seven matching older PNG copies. No scientific input, source cache, script, approval, proposal, review document or unique historical result was removed.

The [removal map](Archive_Removal_Map.csv) gives every old path, retained unique path, hash and current R generator. Use it when a preserved historical document or the older evidence workbook names a removed graphic. Historical process documents retain their original text; their old figure paths are resolved through this map. The [conflict register](Archive_Cleanup_Conflicts.csv) lists four retained frozen graphics and 42 graphics without a byte-identical current export. Matching filenames or having a later plot are insufficient to establish equivalence.

## Dependencies and conflicts

The archive cannot be deleted as a whole. Current Python stages read the original candidate enumeration, PubChem identity cache, 157-candidate framework, chemical observations, later source closure and frozen ranking from it. Current supplementary R scripts also read archived source tables. These are active scientific inputs, rather than redundant products. Removing them would break offline reproduction.

The four frozen graphics remain at their manifest paths. One is identical to a current PNG but its frozen path and hash are part of the approved freeze. Important historical process files and source provenance also remain, including the larger evidence catalogue. Code adaptation alone does not supersede these records.

## Verification and recovery

`python 00_project/maintenance/prune_reproduced_archive.py` inspects exact figure duplicates. Its `--apply` mode records the action before deleting exact files, checks resolved paths stay in the archived figure subtree, and excludes frozen assets. `python run_pipeline.py --tables-only` checks the retained counterparts, all other migration entries and the frozen assets. Current graphs and input tables are not rewritten by the cleanup.

The before-cleanup Git snapshot is `fda5882459404b458dcf3c4a4771c161bc0cd48e`. Deleted historical exports remain recoverable from that commit. No dependency libraries or original scientific records were classified as deletable simply because they are old.
