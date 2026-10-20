# Runtime storage headroom triage

Date: 2026-10-20 UTC

## Result

No safe deletion was available from this worker. The shared filesystem had
8,067,194,880 bytes free (7.51 GiB) at the final reading, below the requested
10 GiB recovery target. No product, test, or admission-guard change was made.

The exact seven visual-seam nodes are already classified by the Runtime triage
worker as environment-only storage-floor refusals. The authoritative full run
was on `81f8c7e` / tree `0e3a5b9` (`5523 passed, 14 failed, 18 skipped, 22
xfail, 12 warnings`); the seven nodes passed in `1.26s` with a private
`ASTRID_RUNTIME_FREE_DISK_FLOOR_BYTES=0` test-process override. The normal
Runtime storage guard must remain unchanged.

## Exact seven-node scope

```text
tests/test_visual_seam_admission.py::test_managed_render_freezes_child_effects_and_offset_from_pinned_closure
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[parent]
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[parent-media-id]
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[shot]
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[internal]
tests/test_visual_seam_admission.py::test_publication_and_render_preserve_uncovered_child_with_advisory_report[clips0]
tests/test_visual_seam_admission.py::test_publication_and_render_preserve_uncovered_child_with_advisory_report[clips1]
```

Their first exception was `runtime_protocol.errors.ConflictError: task
admission refused: storage estimate would cross the free-space floor`. The
failure occurs in `RuntimeService.create_task` storage preflight before the
visual assertions. This is an environment condition, not a visual regression.

## Inventory and classification

The triage worker's completed private paths were checked explicitly:

| Path | Observed size / state | Classification and disposition |
| --- | ---: | --- |
| `/tmp/rt-visual-seam-pytest.l5Zjza` | 5.0 MiB when triage evidence was captured; absent at 15:55:30 UTC | Completed private pytest scratch output; already cleaned up. No action taken. |
| `/tmp/rt-visual-seam-target.v2qpiN` | 8.7 MiB when triage evidence was captured; absent at 15:55:30 UTC | Private authoritative source tree used by the exact rerun; source input, protected. No action taken. |
| `/tmp/pytest-of-root/pytest-2898` | absent at 15:55:30 UTC | Central pytest output/accepted realms; not owned by this worker and protected. No action taken. |

The remaining large Runtime-named paths were not positively attributable to
this worker and include private source trees, realms, backups, joins, or
ownership/proof fixtures. They are therefore candidates for their respective
owners only, not deletion candidates here. Examples inventoried include:

```text
/tmp/rt-m2-carrier-private-pair-final-focused       145,469,440 bytes
/tmp/rt-m2-carrier-private-pair-focused2            145,465,344 bytes
/tmp/rt-m2-carrier-private-pair-focused             145,465,344 bytes
/tmp/rt-m2-carrier-current-tree-compose-focused-final2 133,988,352 bytes
/tmp/rt-m2-carrier-compose-finish-focused           133,988,352 bytes
/tmp/rt-m2-carrier-private-pair-agent3730.m99Etr     116,887,552 bytes
/tmp/rt-m2-secondary-id-fix-join                    103,116,800 bytes
/tmp/rt-m2-secondary-id-independent-review-join     103,116,800 bytes
/tmp/rt-m2-ordinary014-public-export-fix-pytest-neighbors 62,058,496 bytes
/tmp/rt-m2-carrier-final-source-review-compat        58,281,984 bytes
/tmp/rt-carrier-proof-pytest                         57,786,368 bytes
```

The inventory did not touch any other worker worktree, branch, report, archive,
log, accepted realm, source input, lease/dirty/KEEP directory, shared cache,
venv, node_modules tree, or central test snapshot.

## Disk evidence

Command used:

```text
df -B1 /tmp /home/user/work /home/user/peteromallet /home/user/banodoco
```

Before/initial reading at `2026-10-20T15:55:30Z`:

```text
/dev/vda  270553174016 33316593664 8507265024 80% /tmp
```

After inventory and with no deletion at `2026-10-20T15:56:43Z`:

```text
/dev/vda  270553174016 33756663808 8067194880 81% /tmp
```

All four paths are the same filesystem, so the same free-space value applies.
The shared filesystem lost 440,070,144 bytes during the inventory despite no
deletion by this worker; this is external concurrent activity, not recovered
headroom.

## Owner action

This worker is blocked on the requested `>=10 GiB` recovery: there is no safe,
positively identified disposable output of sufficient size in this worker's
scope. The Runtime manager/orchestrator must recycle additional clean,
unleased, non-KEEP finished worktrees or explicitly authorize the owners of
the listed Runtime temporary trees to remove their completed disposable
outputs. The seven nodes should then be rerun through the central test service
with the normal storage floor; do not lower or bypass the production guard.
