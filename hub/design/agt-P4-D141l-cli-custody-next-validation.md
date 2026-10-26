# P4 D141l CLI custody review

Verdict: `PASS_EVIDENCE`.

## Actual proof

The subject continuation's exact central-service commands were:

```text
bin/request-test integration:agent p4-current-becfe-http-3legs --no-cache
bin/wait-test agent-p4-current-becfe-http-3legs-1026103939-14092 1
```

This reviewer did not invoke either command and did not submit or rerun a test.
The returned native service directory was read directly at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-p4-current-becfe-http-3legs-1026103939-14092
```

Its `status` is `pass`, `exit` is `0`, and its summary reports `1 passed in
4.66s` with service elapsed `7s`. The owning launcher command retained:

```text
-m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration --junitxml=<durable-p4-d141l-cli.xml> tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back
```

The actual JUnit has exactly 1 test, 0 failures, 0 errors, and 0 skipped;
suite time is `4.643s`, testcase time is `3.436s`. The selected test and
predicates are unchanged. The JUnit SHA256 is
`7ff7ea370c09f99b9d65bf1acf8beba5eaaee2a97e0071ba00eafdcb03f56891`.

## Admission and disk custody

The named native P4 class is LIGHT with an admission floor of
`5,000,000,000` bytes. The recorded controller value `4,714,564,096` was not
used as an override. The run was not forced, renamed, or guard-bypassed, and
no other heavy body was present.

The genuine manager trace was inspected directly:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/agent/rounds/20261026T1038Z-cli-manager-disk-trace.jsonl
```

It starts at `2026-10-26T10:38:09.649314Z`, before the worker start at
`10:38:31Z`, and ends at `10:42:54.769919Z` after terminal completion. It has
58 samples, maximum sample gap `5.006671s`, minimum available space
`7,406,792,704` bytes, and no sample below either the 5 GB admission floor or
the 4 GB stop floor. The exact service appears as queued twice, running twice,
then pass for 39 samples; the terminal sample has no stop requests. The trace
SHA256 is `69a541620009011957cbbba85748645b90bbfdcc06d64fa6d6518ab12f059ac7`.
The bounded trace summary is retained in `disk-trace.txt`; the raw JSONL remains
at its original absolute path.

The service directory has no dispatcher `disk-trace.tsv`; this is recorded as a
limitation, not filled or backfilled. The manager trace is the actual retained
5-second custody trace used for this review.

## Source and artifact validation

Read-only checks completed successfully:

- JSON parse of the continuation result and source manifest.
- XML parse of the actual JUnit; XML counts match the result and the actual
  body exit/log.
- Exact JUnit path alignment across the launcher manifest, runmanifest,
  launcher argv, and JUnit artifact.
- Exact service ID alignment across the request, status, summary, snap, ext,
  terminal custody record, and manager trace.
- Source heads, trees, origins, and clean status read directly after terminal
  completion for Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, Runtime
  `95d98f038320d5d46bd679ac000ab3e15825c935`, App
  `82e9e13ddf1d7ec6c736521b2eb091dca9877598`, and Composition
  `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.
- Pinned Node `v20.19.4`, launcher, installer, profile, lock, runtime lock,
  composition, client, and schema digests match the source packet; see
  `source-map.json`.
- CAS registration preimage/after hashes, exact candidate row installation,
  and byte-identical outside rows match the subject registration record.
- Input and materialized manifests have equal SHA256 but are distinct,
  non-symlink, non-hardlink files; the durable JUnit did not exist before the
  body according to the subject custody record.
- All 14 entries in the publication receipt were compared byte-for-byte with
  their exact originals and published copies.

## Not run by this reviewer

No product pytest, typecheck, lint, request, test-run, wait-test, CAS, install,
provider, browser, build, dependency, profile, shared-environment, hub, Store,
child, Git, source, or historical-receipt write was performed. Product
typecheck/lint/test rerun is `N/A` because this review made no product or test
change. Stub positive/poison controls receive no behavioral credit.

This evidence covers one CLI selector only. It does not claim the P4 ten-note
per-step undo, conflict/re-run, Python, or sheet lanes.
