# Runtime capture qualification against actual Agent integration

Date: 2026-10-20

## Exact source tuple

- Runtime commit: `0a04782e9a5c5420b2d506d393cd79d8d5b47418`
- Runtime tree: `530e1c121cf3015a2702491cbdfd90d439c736e6`
- Agent ref: `tl/integration`
- Agent commit: `cf7448ed6c1298b172d004914cfe2bb8c99048e7`
- Agent tree: `c8a5e0cb320095129e9a1be125295dfa7adc2793`
- Frozen Agent archive: `/home/user/work/wt/rt-m3-capture-actual-agent-current-pair/agent-source`
- Archive inventory: 3,057 tracked files; every extracted file's Git blob ID was
  recomputed and matched `git ls-tree -r --full-tree tl/integration`.

The archive was created with:

```bash
git -C /home/user/work/agent archive --format=tar --prefix= tl/integration \
  | tar -x -C /home/user/work/wt/rt-m3-capture-actual-agent-current-pair/agent-source
```

Relevant current Agent source was loaded from that archive, including the whole
`capture_candidate_inputs` implementation, `project_capture`, the authoring
bundle/projector dependencies, filmstrip preparation, and rendering source
materialization. No Agent checkout, provider plugin, pin override, or frozen
method substitution was used.

## Named suite and exact environment

Named suite: `capture-agentcf7448-integration`.

The suite is registered in the central test-service configuration with this
exact command prefix:

```bash
env ASTRID_CHECKOUT=/home/user/work/wt/rt-m3-capture-actual-agent-current-pair/agent-source \
PYTHONPATH=$PWD:/home/user/work/wt/rt-m3-capture-actual-agent-current-pair/agent-source \
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q \
-p no:cacheprovider -m integration
```

The required `--files` selections were run separately, with no broad or full
suite:

1. Candidate selection copied from manager request 30103:
   `tests/test_capture_candidate_binding.py`, plus
   `test_original_working_copy_forgeries_refuse_before_writes`,
   `test_working_copy_without_candidate_is_admitted_uncertified`,
   `test_forged_working_copy_certificate_refuses_before_writes`, and
   `test_explicit_cas_candidate_is_native_without_binding` from
   `tests/test_capture_candidate_actual.py`.
2. Identity and aliases copied from manager requests 29820 and 23120:
   `tests/test_capture_claim_identity.py`, plus
   `test_all_capture_aliases_label_each_uncertified_carrier_without_rewriting`,
   `test_outer_legacy_aliases_are_labelled_without_rewriting_admission`, and
   `test_claim_checks_nested_and_outer_aliases_with_mixed_results` from
   `tests/test_capture_candidate_actual.py`.

Central result IDs, all against the same worker snapshot (Runtime snapshot
tree `fca8f4e30528afed83383e097c1e67b403717a87`, whose product parent is the
Runtime commit/tree above):

- `rt-m3-capture-actual-agent-current-pair-capture-agentcf7448-integration-1020114715-17067` — **141 passed**, exit 0.
- `rt-m3-capture-actual-agent-current-pair-capture-agentcf7448-integration-1020114715-9119` — **25 passed**, exit 0 (6 identity + 19 alias cases).

Direct repeats with the exact archive environment also passed:

- candidate selection: **141 passed in 87.25s**;
- identity selection: **6 passed in 4.25s**;
- alias selection: **19 passed in 11.55s**.

These are the scoped current-source Runtime admission results. They exercise
real startup provider loading and the actual current Agent projector/core
dependencies, not only method-byte equality with frozen `92427b3a`.

## Open external caller boundary

The four existing direct candidate-to-host positives were probed once with the
same real archived Agent source and Runtime provider:

```bash
PYTHONPATH="$PWD:$PWD/agent-source" \
ASTRID_CHECKOUT="$PWD/agent-source" PYTHONDONTWRITEBYTECODE=1 \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration \
'tests/test_capture_candidate_actual.py::test_actual_candidate_reaches_claim_and_host'
```

Result: **4 failed**, all at `RenderRequest.verified_source`; the current
`RenderRequest` class has no `verified_source` attribute. The assertions before
that access prove the real Runtime claim/materialization, snapshot, authority,
candidate digest, dependency expansion, and media bytes. This is the existing
RenderRequest propagation-4 gap, left open as directed. The SDK guard-3 gap is
also left open; neither requirement was weakened or relabelled.

No full suite, localhost/browser suite, or duplicate frozen `92427b3a` pair was
run.

## Archive housekeeping
The read-only qualification worker accidentally stored its source archive inside its own worktree; its completed branch includes that archive and is **ARCHIVAL ONLY, NEVER MERGE**. It was recycled. The manager reconstructed the exact same Agent cf7448 source with git archive at persistent /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m3-capture-actual-agent-current-pair/agent-source, outside all product repos, and updated only Runtime-owned capture-agentcf7448-integration suite paths. Original successful requests retain their original source paths and snapshots; no result is relabeled or rerun. Agent source identity is unchanged; any future service run uses this persistent complete archive. Runtime merge candidate remains0a04782e (four approved paths), never the qualification worker branch.
