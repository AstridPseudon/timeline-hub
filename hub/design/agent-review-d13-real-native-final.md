# Agent D13 final native-consumer deletion gate

## Verdict

**REQUEST CHANGES**.

The native consumer replacement and deletion are substantively qualified, but the
final candidate adds an environment-dependent `pytest.skip` for `ffmpeg`,
`ffprobe`, and `node` in `tests/packs/video_editing/test_runtime_publication_chain.py`.
The gate requires new markers/skips to be absent. Remove that skip (tool
availability belongs to the named lane precondition) without weakening the
render assertions, then rerun the named central suite once on the final tree.

## Source identity

- Candidate HEAD: `081f0907c008baeb8e35b0a56cdd63b2b08bb8a6`
- Candidate tree: `740ac183a97650368234f0a5c1cc86f1bc8499a1`
- D13 source base: `310e5484` (tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`)
- Worktree status: clean; no source changes made by this review.

## Evidence reviewed

The central named run used the final candidate tree and the pinned private
Runtime/Remotion/Node environment:

```text
agent registered-native-render-integration
pytest -m integration
2 passed in 227.61s
```

The two exact test IDs are the real daemon-backed native assemble and final
render chain. The test reads the rendered bytes from Runtime CAS, requires a
non-trivial MP4, runs `ffprobe` over those bytes, asserts a positive duration,
checks the render task parent revision, and completes guarded undo. The runner
did not retain a standalone MP4 in its result directory, so independent
post-run replay of that file is not possible; the in-run CAS-byte and ffprobe
assertions are the available final-render proof.

The original legacy refusal and artifact-preservation test remains positive;
the old strict xfails are removed. The native path preserves settled proposal
validation, exact producer/task/attempt provenance, ordered CAS aggregation,
media lifecycle checks, normal `rendering.render` admission, revision-pinned
rendering, and guarded undo.

The lost-ACK/restart path was checked: admission is captured once, the exact
outbox body/key is retried after restart, and no recapture is performed. The
unknown flight-kind guard remains strict (`c610` cases included); there is no
reset, adopt, or recapture fallback.

The GenericHost change is minimal: epoch is propagated from authoritative
claimed task/attempt context and validated with the Runtime fence/epoch
validator. The preserved tuple is target, fence, epoch, executor, and proposal
digest; caller JSON is not authoritative. The old pre-settlement canonical
writer is removed only alongside the positive native replacement.

The WorkspaceClient additions are the existing Runtime media-selection and
verified-media read facades and their existing generated operations. No new
DTO, endpoint, or public alias was introduced. `STITCH`/assemble remains
distinct from `rendering.render`. The requester uses the owner commit
credential; the GenericHost uses the Runtime worker token, so no credential
lending was found. No `ScopeFactory`, fake GenericHost, render-worker project
write, or manifest-forge path was found.

One remaining source issue is the new conditional skip described in the
verdict. It is separate from the local fixture skip below and is present in
the candidate source.

## Targeted tests

Run directly in this worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py::test_present_unknown_flight_kind_refuses_reload_without_post_or_mutation tests/packs/video_editing/test_runtime_publication_chain.py::test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task
8 passed, 1 skipped in 2.41s
```

The one local skip was the pre-existing lane fixture requirement: no Runtime
checkout was available at `/home/user/work/wt/astrid-runtime` or
`/home/user/peteromallet/astrid-runtime`. It was not a test assertion failure.
The isolated refusal test reports the same reason (`1 skipped in 1.24s`).
`git diff --check HEAD` passed. No full suite was run.

## Composition audit

Current Agent integration is `tl/integration` commit
`30fc8dd154015a7c58cf4ce7b065ccc46f470ee8`, tree
`50925d6df67ce717653e3ce7ac12803f8865da93`, with merge-base
`4ef1391c2c104d5d11b3a27265035c51be296045`. It is not the D13 candidate base:
D13 is based on `310e5484`, and the candidate is not merged into integration.

After the exact source014/ordinary014 pin, the composition delta is:

- Keep current integration's document read facades in
  `astrid/sdk/workspace_client.py` and add/retain D13's existing media
  selection and verified-media facades; these are a union, not a replacement.
- Keep current integration's stage-guard additions to
  `tests/sdk/test_timeline_sync.py` and retain D13's strict unknown-flight-kind
  coverage.
- Apply D13's `generic_host.py` deletion of the old automatic pre-settlement
  assembler writer and add `astrid/sdk/timeline/assembly.py`; current
  integration still has `_publish_assembled_timeline` and has no assembly
  module.
- Carry the remaining D13 paths exactly: runtime orchestration contract,
  rendering assemble action/manifest, timeline sync, workspace client,
  publication-chain tests, and assembly/sync tests, resolving only the
  two documented overlaps above.

The current integration includes later P1/Scene/Root/AM work; the frozen
candidate base `310e` must not be treated as current integration or merged
prematurely.

## Remaining current-pair and ledger gates

1. Remove the new environment-dependent skip and rerun the named central
   `registered-native-render-integration` suite once on the final candidate.
2. Compose D13 after the exact source014/ordinary014 pin, preserving the
   current integration overlaps listed above; do not delete D13 during the
   composition.
3. Qualify the current Agent/Runtime pair. The central artifact used external
   Runtime commit `c45cbc6ba3772ac2cebb5a5c94f91be24231e2d8`; the current
   Runtime worktree is `81f8c7e0b22c34804015c054762af3d737e4698a`, so that
   current pair is not yet proven by this review.
4. Re-run the post-composition current-pair and deletion-ledger gates, including
   the real render/ffprobe and lost-ACK restart chain, before recording D13 as
   merged and closing the ledger row.

Runtime peer inspection found no shared protocol concern: the validator still
requires the authoritative task/attempt identity, positive fence and epoch,
exact admitted target, proposal digest, and one-shot producer guard before
settlement.

