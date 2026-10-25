# OPS staging disposition — PASS_ASSESSMENT / UNAPPLIED_HOLD

This is an independent read-only assessment of `rt-OPS-staging-residual-sol-2239`.
The assessment passes because the residual report is executable, complete and
honest. The executable source itself remains `FAIL_SOURCE` against the residual
safety contract and is held unapplied.

## Custody and delta

- Candidate is `25f311f8567fdb65408f1ae8a8f662649c1e0f57`, whose parent is the
  exact reviewed source `9524356e2ca603f444eda451a502438ef9110d3b`.
- The only candidate delta is the 20-line qualification note in
  `ops-drop-staging/README.md`. `drop_staging.py`, `drop-staging`, and
  `test_drop_staging.py` are byte-identical to `9524356`.
- The launcher remains executable (`0755`); all source/test modes and hashes are
  recorded in `source-manifest.json`.
- The README does not change runtime behavior, test expectations, installation,
  or cleanup authorization. It records `UNAPPLIED` and the five residuals.

## Findings, all reported together

1. **OPS-STAGING-FR-001 — HIGH: archive identity is not held through delete.**
   At `drop_staging.py:1093-1105` the verified temporary archive is linked into
   the worker, then `execute` logs and deletes at `1260-1289`. The recovered
   `archive_symlink_race` replaces the published path after `_write_log`; the
   command returns `packed`, leaves the replacement symlink, and removes
   staging. The outside fixture remains unchanged, but the verified archive is
   no longer the retained artifact.

2. **OPS-STAGING-FR-002 — HIGH: worker pathname detaches from its identity.**
   `execute` opens/checks the worker at `1135-1167`, then acts through the old
   descriptor at `1288-1289`/`1319-1320` without binding the worker name at the
   destructive boundary. The recovered `worker_rename_race` renames the worker
   away and installs a replacement at the original name; the detached source is
   removed while the replacement remains.

3. **OPS-STAGING-FR-003 — HIGH: a late matching lease is ignored.**
   Lease protection is checked before quarantine at `1200-1208`; the archive
   and fallback paths then log and delete at `1245-1320` without a shared lease
   exclusion. The recovered `late_lease_race` adds the matching lease after the
   last check; the command still returns `packed` and removes staging.

4. **OPS-STAGING-FR-004 — HIGH: late KEEP can cause partial fallback deletion.**
   `_unlink_tree_at` deletes entries as it traverses at `956-980`. If KEEP
   appears after validation, the fallback has no archive and the exception path
   can rename back an incomplete tree. The recovered
   `late_marker_fallback_race` reports the protected-marker error but the nested
   payload is already absent.

5. **OPS-STAGING-FR-005 — MEDIUM: evidence can change after verification.**
   Final evidence verification occurs at `1266-1274` (pack) or `1296-1305`
   (fallback), before log/delete at `1288-1289` or `1319-1320`. The recovered
   `evidence_symlink_race` replaces a manifest-listed file after verification;
   the command logs `evidence_verified=true`, returns `packed`, and removes
   staging while the evidence path is now a symlink.

The five new private subprocess controls preserve their original expectations:
each requires source bytes to remain present, and all five fail against the
unchanged executable. They are not rewritten, skipped, or converted into a
green result. The recovered five probe script completed with the five defect
observations; it did not read or delete outside fixture bytes.

## Scope distinction

The owner request explicitly requires guarded one-worker containment, lifecycle
and marker/lease checks, no-follow/evidence verification, archive-first removal
when disk permits, a guarded low-disk fallback, durable fallback accounting,
evidence preservation, and refusal/error rather than a broad sweep. Those are
not waived.

The residual review also asks for a stronger invariant: arbitrary same-UID
mutations after the last finite recheck must not permit deletion or make a
refusal lossy, including worker-name replacement, lease publication, archive
replacement, evidence replacement, and fallback rollback after unlink. That
invariant is not created by adding another pathname recheck. The current
operational writers do not participate in the worker-directory `flock`; the
lock is advisory to cooperating holders, and quarantine does not revoke other
descriptors. The low-disk fallback retains no recovery copy.

No waiver or new policy is inferred here. Under the residual brief's requested
strong guarantee, the supported route is insufficient, so the correct finite
disposition is `UNAPPLIED_HOLD`.

## Minimum mechanism / next owner decision

Before implementation can be safely commissioned, the orchestrator must decide
whether same-UID concurrent mutation protection is part of the actual contract
or whether an explicit non-concurrent operational admission is in scope. If it
is part of the contract, the minimum mechanism is a shared exclusion/admission
protocol used by cleanup and every relevant operational writer, held from
admission through quarantine, archive/log publication and final unlink (or an
equivalent kernel-atomic state transition). Archive mode must retain and verify
the exact published archive under that exclusion. Fallback mode cannot roll back
unlinked bytes without a retained copy; it therefore needs either the shared
exclusion to make late mutation impossible or a separately retained recovery
copy/durable reservation.

That cross-writer mechanism is outside the current `ops-drop-staging/` source
scope. Do not dispatch a source-only repair or install-prep task until the
contract scope and its owner are settled. If affirmed, the finite next source
task is a narrowly scoped implementation across the operational writers and
the kit, followed by the unchanged 14-test baseline and the five retained
private subprocess controls under independent review.
