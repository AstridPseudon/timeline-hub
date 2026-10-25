# Private `drop-staging` kit candidate

`drop-staging WORKER RELPATH` operates on exactly one worker record.  The
future normal installation is `ORCH/bin/drop-staging`, with worker records at
`ORCH/workers`; this source candidate accepts `--workers-root` for private
qualification fixtures.  It never scans for candidates or edits the live
orchestrator tree.

Before an action, the caller requires all of the following:

- a single worker name and a relative, non-traversing target directory;
- `ended` and no `running`, `KEEP`, active marker, or matching manager lease;
- no symlink or unsupported file in the target or any target path component;
- `worker/evidence/manifest.json`, with schema version 1 and non-empty
  `files` rows of `{path, sha256, mode}`; every listed evidence file must
  match its content and permission-mode hash;
- no target/evidence overlap and no pre-existing `<target-name>.tgz` archive.

The worker record is locked and the target is atomically quarantined before
the final action.  If free space admits `logical_target_bytes +
--pack-reserve-bytes`, a gzip archive is created, its members are checked
against the source listing, and only then is the quarantine removed.  If
admission fails, the validated target is removed without an archive and a
durable `worker/staging-drop.log` row records the original byte count, full
listing SHA-256, and evidence-manifest verification.  Archive errors are
errors, never silent fallback.  Evidence and its manifest remain outside the
target in both modes.

The operation is deliberately one-target and idempotent by refusal: a second
call sees the missing target and/or existing archive and changes nothing.  A
target/evidence overlap, protected ancestor or descendant, archive collision,
or any path race is reported as a refusal/error rather than converted into a
broad sweep.

Run the bounded private CLI tests with:

```sh
python3 ops-drop-staging/test_drop_staging.py
```
