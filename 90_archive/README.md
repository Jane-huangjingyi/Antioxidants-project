# Preserved original source baseline

`legacy_2026-11-05` contains the prior project's original data, source caches, approvals, proposals, scripts, reports, figures and evidence catalogue. Its scientific/process file bytes were preserved during migration; the path map and hashes are in `../07_quality_control/migration_manifest.json`. Original-language text is retained as source evidence, not presented as the active English project narrative.

Old relative paths are interpreted relative to this baseline directory. The frozen asset manifest therefore still resolves without editing its contents. Current research stages read the required source snapshots from here and write new outputs only to their numbered active step. Historical scripts can depend on their original layout and should not be used to overwrite current outputs.

Useful R modules were relocated and adapted in `../05_analysis/legacy_modules`; the old files remain as provenance copies. The discovery generator's literal enumeration is directly consumed by Step 01. Historical drafts, QC and rejected/held proposals are process records and are retained even when byte-identical to another role. No important process file is deleted.

Generated diagnostic previews, dependency caches and exact temporary build mirrors are not canonical research outputs. Any future redundant-file deletion must identify the retained counterpart, verify byte identity, resolve consumers and record the action; path migration alone does not authorize scientific-data deletion.

After researcher authorization, 109 byte-identical reproduced graphics were removed. Their retained unique outputs and R generators are listed in the [removal map](../07_quality_control/Archive_Removal_Map.csv). Historical documents and the older workbook may still name those original paths; resolve them through that map. Four frozen graphics, nonidentical historical graphics, all scientific inputs and important process records remain. See the [cleanup report and conflicts](../07_quality_control/Archive_Cleanup_Report.md).
