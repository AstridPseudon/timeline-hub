# OPS staging first-return final review: FAIL_SOURCE

Reviewed source: `9524356e2ca603f444eda451a502438ef9110d3b` (`93ba9e7a6f96ea4d2b9bb31460d01832fcb5945a`), the exact first return from `tl/rt-OPS-staging-return-2223`. No product or test source was edited, and no real worker was touched.

The four original review findings were rechecked. The return fixes are present for initial/action-open identity, no-follow evidence and lease-root inspection, ancestor/descendant marker discovery, and hardlink listing identity. The source is still FAIL_SOURCE because the following residual findings remain:

1. **HIGH — OPS-STAGING-FR-001, archive replacement after verification.** `drop_staging.py:1093-1105` publishes the archive by hard-linking the verified temporary file, but `execute` does not retain/recheck the final archive identity or digest before `drop_staging.py:1288-1289` deletes the quarantined source. Private `archive_symlink_race` replaces `staging.tgz` after `_write_log`; the command returns `packed`, deletes staging, and leaves the replacement symlink.

2. **HIGH — OPS-STAGING-FR-002, worker pathname replacement after open.** `drop_staging.py:1135-1167` checks worker identity only when the worker descriptor is opened. There is no parent-directory name/identity recheck before `drop_staging.py:1288-1289` or `1319-1320`. Private `worker_rename_race` renames the opened worker away and installs a replacement at the original name; the source removes the detached worker's staging.

3. **HIGH — OPS-STAGING-FR-003, stale lease guard.** Lease checks at `drop_staging.py:1200-1208` happen before quarantine. There is no lease recheck after quarantine/evidence validation and immediately before deletion. Private `late_lease_race` adds a matching manager lease after `_write_log`; the source still returns `packed` and removes staging.

4. **HIGH — OPS-STAGING-FR-004, partial deletion on late descendant mutation.** `drop_staging.py:956-980` deletes entries as it scans and only discovers a late marker/symlink/unsupported entry when encountered. In private `late_marker_fallback_race`, a `KEEP` marker is added after final validation; fallback raises but has already deleted `nested/payload`, restores an incomplete target, and has no archive.

5. **MEDIUM — OPS-STAGING-FR-005, evidence state not held through deletion.** The final evidence verification at `drop_staging.py:1266-1274` / `1296-1305` is closed before `_write_log` and deletion. Private `evidence_symlink_race` replaces a manifest-listed evidence file after that check; the source returns `packed`, deletes staging, and logs `evidence_verified=true` although the evidence path is now a symlink.

All private probes used temporary fixtures only. They did not read or delete outside fixture bytes. No cleanup authorization is inferred.
