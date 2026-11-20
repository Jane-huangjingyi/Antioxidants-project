# Repository cleanup audit

The pre-deletion walk inventoried 12,613 files, including 1,427 Git-tracked files. Git object storage and symlink/junction targets were outside the walk. The [public manifest](Repository_Cleanup_Manifest.csv) records every tracked file and every deleted file. The full local inventory is in download_raw/Repository_Cleanup_Local_Inventory.csv and stays local to protect licensed-source information.

Three staging assets from the September 18 atlas transition were byte-identical to tracked authoritative copies: the mechanism master, panel master and dated master report. The pre-release Git blobs and canonical SHA-256 values were verified. A tracked fixed-string scan checked full forward- and backslash paths. The live references were generated source or navigation indexes. These were repaired. The dated historical plotting script and other assets with distinct provenance remain. Historical audit mentions remain evidence of the old layout.

Nine local, reproducible exports were deleted: six v0.1 workbook previews, two workbook inspection exports and one intermediate JSON payload. The underlying source and generation code remain. The immutable release snapshot replaces the disposable JSON as the reproduction input for Results 1.

The cleanup removed 12 files totaling 4,621,712 bytes, of which 58,791 bytes were tracked staging content. Of the pre-cleanup inventory, 12,601 files were retained, including 1,424 tracked files. The counts precede replay outputs and new release files. Git history was not rewritten, so deleted blobs remain in the old commit. The new release adds versioned scientific artifacts and may increase the final checkout despite removal of redundancies.

Retained assets include the original experimental extractions and user-supplied records, the frozen Stage25B Top20 and figures, conditional FL models, the historical ruling and governance records, literature caches, and all needed runtime dependencies. Another 110 local files were conservatively marked REVIEW_REQUIRED, including unclassified local or build assets. They were left in place. Matching content in a freeze, distinct scientific role or governance record was insufficient grounds to delete it.

Post-cleanup verification is in [the reproducibility QC](Post_Cleanup_Reproducibility_QC.md).
