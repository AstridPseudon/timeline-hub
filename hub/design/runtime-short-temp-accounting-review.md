# Runtime review: accounted short browser temp

## Verdict

**APPROVE the accounting seam for the current bounded owner change; no Runtime
product change is required.** The rejected external-`TMPDIR` design remains
rejected. The current Agent owner change keeps the short Remotion/Chrome temp
directory inside the already admitted attempt root, so the existing Runtime
byte estimate and Agent attempt guards continue to cover it.

This is an accounting/ownership review only. The path checks are ordinary
pathname checks rather than an atomic directory-fd handoff; an independent
security/process-custody review is still required before merge, as requested by
the task. No browser, full suite, pin, release, DTO, public setting, store
field, codec/profile, symlink, or Chrome-flag change is approved here.

## Exact current proposal and owner seam

No separate `accounted-short-temp-owner-proposal` report was present. The
available current proposal is Agent commit `21e84b7d0d39f9d0b0cf97eaeac62aa7cebb37f8`,
merged into Agent integration as `d0a5072b`; the peer update at
`peer-agent-to-viewing-20261020T2001-short-path-merged.md` identifies the same
three-file delta. The independent Agent review
`agent-short-attempt-current-review.md` approves that exact delta.

The concrete owner seam is Agent
`astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:_accounted_attempt_root`:

1. It requires the existing internal invocation marker and exact
   `.astrid-progress.json` path (`root_preparation.py:30-37`).
2. It rejects symlinked marker/staging/output ancestry, requires the marker
   parent to be an existing owner-only directory, and requires the staging
   workspace to be that attempt's direct child with output under
   `attempt/outputs` (`root_preparation.py:39-60`).
3. On proof, Root preparation uses that attempt as the parent and allocates
   `.r-*` with `TemporaryDirectory` (`root_preparation.py:128-141`). Failed or
   foreign proof falls back to the existing staging parent.

The same proposal keeps the established ephemeral reclaim prefix
`astrid-attempt-` and creates host-owned ephemeral/explicit attempt roots with
mode `0700` (`generic_host.py:5284-5298`). It does not put task identity into
the ephemeral basename; the existing progress/lease identity remains the
identity source.

## Runtime boundary evidence

Runtime has no external-temp accounting or path-registration carrier:

- `runtime_protocol/local_worker_composition.py:493-498` propagates only the
  existing allowlisted process environment, including `TMPDIR`, `TMP`, and
  `TEMP`; it launches with the fixed profile support-root cwd.
- `runtime_protocol/local_execution_supervisor.py:149-151` validates that
  environment allowlist, and `:1005-1025` forwards the inherited environment
  while launching the host with `cwd=config["support_root"]`. This is process
  environment transport, not sandbox or quota authority.
- `contract/schemas/task.json:29-36` and
  `runtime_protocol/store.py:_validate_storage_estimate` accept only the
  existing `scratch_bytes` and `output_bytes` estimate. The task execution
  request has no attempt-temp path field.
- `runtime_protocol/store.py:1128-1137` exposes
  `attempt_staging_dir`, but that is Runtime settlement staging under
  `staging/settlements/<attempt_id>`, not the Agent GenericHost attempt root
  and not a browser-temp registration mechanism.
- Claim returns the immutable task/attempt identity and estimate at
  `runtime_protocol/service.py:7096-7134`; it does not create or return a
  browser-temp root.

Therefore Runtime must not make the external environment path appear
accounted merely because it crosses the relay. The current in-attempt design
is the only minimal fix compatible with the settled contract.

## Actual normal-render path

The normal CPU MP4 path is, from the current Agent integration source:

`RenderService` creates a workspace beside `attempt/outputs`
(`astrid/core/rendering/service.py:157-169,414-420`) -> Remotion passes that
workspace as `staging_parent`
(`.../remotion/run.py:1651-1664`) -> Root preparation allocates the short
`.r-*` child in the proved attempt root (`root_preparation.py:128-141`) -> the
Remotion child receives `TMPDIR`, `TMP`, and `TEMP` set to that nested root
(`.../remotion/run.py:1092-1117`) -> Chrome creates its profile and
`SingletonSocket` below it.

This is the normal render path. It does not use `HostRemotionSession`; that is
a separate managed visualization/session carrier and must not be substituted
for this path.

## Accounting and cleanup proof

The current placement preserves the existing positive accounting path:

- `_attempt_tree_bytes` walks regular files below the attempt root without
  following symlinks (`generic_host.py:2093-2112`).
- `_assert_live_storage_envelope` computes scratch as attempt bytes minus
  output bytes and rejects scratch/output overruns
  (`generic_host.py:3961-4000`); the live loop invokes it at `:8099-8103`.
- Final settlement recomputes the same attempt-root view
  (`generic_host.py:4003-4060`). The `.r-*` marker is also classified as a
  renderer workspace for existing diagnostics.
- `TemporaryDirectory`/`ExitStack` removes the nested browser directory.
  GenericHost cleanup deletes only the owned attempt root and releases its
  evidence charge after verified deletion, or retains/latches uncertainty
  (`generic_host.py:5465-5478,9984-10010`).

The required negative is equally clear: a file placed in an external
`TMPDIR` is not visited by `_attempt_tree_bytes`, so the old external design
can report zero attempt scratch for nonzero external bytes. That is the
reported 4096-byte budget escape and is why the external patch stays on HOLD.

## Required disposition

Keep the current three-file Agent delta and pair it only after the separate
security/process-custody review. That review should retain the existing
fallback, owner/mode/symlink ancestry checks, explicit-attempt collision
refusal, and fail-closed cleanup uncertainty behavior, and should examine the
non-atomic pathname-check limitation. No Runtime source or contract change is
needed for the accounting seam.

## Evidence run

Runtime worktree: `3b900c377e7126e14eeb92dc2ce73114cbda5a0e`, clean; no Runtime
source changed.

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python \
  -m pytest -q -p no:cacheprovider tests/test_task_storage_estimate.py
14 passed in 7.99s
```

The combined focused command passed 154 tests but had 6 failures in
`tests/test_local_execution_supervisor.py`; every failure was the sandbox's
`PermissionError: [Errno 1] Operation not permitted` on `socketpair()`/frame
`sendall`, including the private-wire journey. This is environment evidence,
not a short-temp failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python \
  -m pytest -q -p no:cacheprovider \
  tests/test_task_storage_estimate.py tests/test_local_execution_supervisor.py
154 passed, 6 failed in 12.94s
```

The Agent review records its exact current-delta evidence as 71+6 targeted
tests plus one independent collision guard; I did not rerun Agent tests from
this Runtime worktree. No browser/MP4, localhost, full suite, or renderer
rerun was performed.
