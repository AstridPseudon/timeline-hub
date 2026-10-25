# Private install-prep recipe

1. Review the candidate source and its `source-manifest.json` independently.
2. Copy `ops-drop-staging/drop_staging.py` and the executable launcher
   `ops-drop-staging/drop-staging` into the future kit's `ORCH/bin/` directory,
   preserving the launcher mode `0755`; keep the module beside the launcher.
3. The normal caller is:

   ```text
   ORCH/bin/drop-staging WORKER RELPATH
   ```

   It derives `ORCH/workers` from its installed location. For private
   qualification only, use `--workers-root PRIVATE_WORKERS_ROOT`; do not point
   it at the live orchestration tree during review.
4. Install no dependencies. The implementation uses only Python's standard
   library and requires Linux directory-descriptor semantics (`O_NOFOLLOW`,
   `dir_fd`, and `flock`) for its guarded execution path.
5. Run the exact bounded validation command from `validation.md` in the
   installed source checkout, then perform an independent CAS/source-hash
   review before any live installation or cleanup authorization.

The candidate has no automatic sweep mode and does not modify
`ORCH/bin/compact-scratch` or any worker record.
