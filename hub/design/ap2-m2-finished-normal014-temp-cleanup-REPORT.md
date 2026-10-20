# Finished normal014 App temporary-root cleanup

Date: 2026-10-20 UTC

## Result

Five finished App2 normal014 roots were removed. Only the exact generated
root was deleted; `/tmp`, inherited TMPDIR parents, shared dependencies,
locked graphs, source repositories, runtimes, and symlink targets were not
modified.

| Root | Created | Allocated bytes | Provenance | Decision |
|---|---:|---:|---|---|
| `/tmp/timeline-normal014-app.6qCmgd` | 20:11:58Z | 811,704,320 | `ap2-m2-bootstrap-committed-service-qualification-1020201152-30268`, central status `fail` | removed |
| `/tmp/timeline-normal014-app.8C8NAp` | 19:55:02Z | 811,982,848 | `ap2-m2-private014-enabled-runtime-final-candidate-normal014-integration-e2e-gate5-1020195447-8973`, central status `pass` | removed |
| `/tmp/timeline-normal014-app.NLv0LV` | 20:31:09Z | 811,704,320 | `ap2-m2-bootstrap-real-create-first-failure-fix-ap2-m2-bootstrap-committed-service-qualification-1020203056-22178`, central status `fail` (`No tests found`) | removed |
| `/tmp/timeline-normal014-app.e5J43i` | 20:34:11Z | 813,477,888 | `ap2-m2-bootstrap-real-create-first-failure-fix-normal014-integration-e2e-gate5-1020203406-14558`, central status `fail` | removed |
| `/tmp/timeline-normal014-app.rNrqy6` | 20:19:23Z | 813,731,840 | `ap2-m2-bootstrap-central-selector-source-fix-ap2-m2-bootstrap-central-selector-source-fix-1020201909-29453`, central status `fail` | removed |

Removed allocated bytes: **4,062,601,216** (apparent bytes: 3,855,647,903).

## Preserved roots and skip reasons

| Root | Observed bytes | Provenance / state | Skip reason |
|---|---:|---|---|
| `/tmp/timeline-normal014-app.91b9YO` | 814,088,192 | Finished central parent qualification, status `fail`; created 20:47:25Z | younger than 20 minutes at final check (592 seconds) |
| `/tmp/timeline-normal014-app.cPq73K` | 813,592,576 | Finished central bootstrap observer qualification, status `fail`; created 20:46:06Z | younger than 20 minutes at final check (671 seconds) |
| `/tmp/timeline-normal014-app.cpsIv3` | 181,370,880 | Partial root containing only `sources`, `python-runtime`, and `pip-cache`; no finished-test record identified | younger than 20 minutes (177 seconds) and provenance uncertain |

`/tmp/timeline-normal014-app.r5nXh6` was present in the initial inventory
(about 842 MiB) and belonged to the running
`ap2-m2-parent-valid-selection-refusal-fixture` worker. It was not targeted;
it was absent from the final inventory, consistent with the fixed harness
cleaning its owned root after the run. No byte count was captured before that
independent cleanup.

Initial matching-root count: 9. Removed by this worker: 5. Preserved at final
check: 3. Independently absent at final check: 1. No other `/tmp` roots were
inspected or removed.

## Safety checks

Immediately before each removal, the root was revalidated as a direct,
canonical, real directory under `/tmp`, older than 20 minutes, with terminal
central status. A `/proc` scan found no other process cwd, open descriptor, or
command reference; the validator's own ancestor processes were excluded from
the command-argument scan. No root contained a KEEP, lease, or evidence
sentinel, and no top-level symlink pointed at a candidate. Generated private
node-module symlinks pointed outward to the locked graph; descendant deletion
removed only the symlink entries and did not follow them.

The final process scan found no cwd/open-descriptor references to any of the
three preserved roots. The active parent qualification worker remained in the
queue, so its young/owned output was preserved.

## Disk and verification

`df -P -B1 /tmp` before cleanup: available `12,621,684,736` bytes.

`df -P -B1 /tmp` after cleanup: available `17,357,418,496` bytes (final check).

Observed available-space increase: `4,735,733,760` bytes. This exceeds the
five-root allocated total because the independently owned active root also
disappeared during the cleanup window and other lifecycle activity may have
run concurrently.

The App worktree remained clean. No product code, tests, dependencies,
browser/socket/full suite, or new private copy was created or changed.
