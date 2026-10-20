# Agent review — sequential Viewing extraction gates

Review date: 2026-10-20. This is a read-only owner review. No Agent source,
integration worktree, borrowed worktree, branch, or ref was changed.

## Exact refs and merge order

- Actual current integration: `8e3107853d17453758a933d1f47215cc1c002660`
  (`tl/integration`).
- Shared candidate parent / merge base: `4ef1391c2c104d5d11b3a27265035c51be296045`.
- First candidate: `tl/vw-m4-service-window-source-extract`, commit
  `0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6`, tree
  `3db1e03e44304891884b9f4db61bcdb7de1e2503`.
- Second candidate: `tl/vw-m3-root-prep-lifetime-extract`, commit
  `634867fed71b4ae53acaa3c3162315527c2bdb23`, tree
  `e2ac895d16ab205221358aeee9b8540f57f71779`.

The candidates are independent siblings of `4ef1391c2`; merge them in the
briefed order: service extraction first, then Root-preparation extraction.
The current `8e310785` tree has byte-identical pre-extraction blobs for every
touched path, and the two candidate path sets have no overlap with the
`4ef1391c2..8e310785` delta. Sequential patch application onto a disposable
archive of `8e310785` passed `git apply --check` for both patches.

Manager conflict/ancestry commands:

```bash
AG=/home/user/work/agent
git -C "$AG" merge-base tl/integration tl/vw-m4-service-window-source-extract
git -C "$AG" merge-base tl/integration tl/vw-m3-root-prep-lifetime-extract
git -C "$AG" diff --name-status 4ef1391c2c104d5d11b3a27265035c51be296045 0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6
git -C "$AG" diff --name-status 4ef1391c2c104d5d11b3a27265035c51be296045 634867fed71b4ae53acaa3c3162315527c2bdb23
git -C "$AG" merge-tree 8e3107853d17453758a933d1f47215cc1c002660 0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6
```

For a non-mutating sequential conflict check, archive
`8e3107853d17453758a933d1f47215cc1c002660`, then apply/check these exact
patches in order:

```bash
git -C /home/user/work/agent diff --binary \
  4ef1391c2c104d5d11b3a27265035c51be296045 \
  0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6 | git -C <private-tree> apply --check
git -C /home/user/work/agent diff --binary \
  4ef1391c2c104d5d11b3a27265035c51be296045 \
  634867fed71b4ae53acaa3c3162315527c2bdb23 | git -C <private-tree> apply --check
```

Both checks are clean. Do not compare either sibling directly to `8e310785` as if it were a
linear diff; use the shared parent or the merge queue.

## Gate 1 — service window/source extraction

**APPROVE** `0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6`.

The candidate changes exactly these two files: `service.py` and the new
`window_inputs.py`. The extracted executable body is AST-identical to
`RenderService._segment_request` after normalizing only the injected
`slice_timeline=self._window_timeline` hook. Native pass-through, original
render-view extent measurement, layer/track/clip filtering, legacy slicing,
alpha metadata, atomic materialization, sidecar hashing, error paths, request
immutability, and source handling remain in the same order. No new API,
SourceFactory, authority, DTO, query activation, security/source/drop/env, or
PCM policy is introduced.

The current service file is 2,298 lines after extraction versus the recorded
2,314; the 1,200 threshold and 50-line tolerance are unchanged. No unrelated
old change is present: the parent-to-candidate diff is only the two expected
files.

Minimal checks:

```bash
git -C /home/user/work/agent diff --check 4ef1391c2c104d5d11b3a27265035c51be296045 0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-tree> \
  /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q -o addopts= \
  <private-tree>/tests/core/rendering/test_service.py \
  <private-tree>/tests/packs/rendering/test_native_layer_extent.py \
  <private-tree>/tests/packs/rendering/test_live_scene_composition.py \
  -k 'not real_ffmpeg and not real_render_scene'
```

Owner rerun: `139 passed, 4 deselected` in 46.85s on the composed current-base
tree. The prior exact identity harness also reports AST equality and 78
identical payload/error/immutability examples. The central named native-window
lane recorded in the handoff is `25 passed`, service
`vw-m4-service-window-source-extract-targeted-1020133240-23843`.

## Gate 2 — Root-preparation lifetime extraction

**APPROVE** `634867fed71b4ae53acaa3c3162315527c2bdb23`, after the service
candidate in the stated order.

The expected seven-file diff is: the private `root_preparation.py` helper,
`run.py`, the existing frame source fingerprint, the owned giant-file
rationale row, and three direct test files. The helper is a private context
manager with the exact handoff signature and plain tuple yield; it does not
add a public API, DTO, SourceFactory, authority field, or new query caller.
`run.py` has one helper call inside the existing renderer execution path. The
existing lock remains owned by the caller; staging/config/source/registry/theme/
props/occurrence identity, managed asset server, temp/effect roots, normal PCM,
callback timing, renderer process continuation, and reverse cleanup remain
inside the same lifetime.

Independent AST checks on the candidate proved all four regions equal after
only backend-name normalization: admission/preparation, Root-preparation
body, cleanup, and renderer continuation. No query is activated, no capture is
certified, and no frame/video process is launched by context entry. The source
fingerprint addition is the one necessary adjacent cache-identity change.

The candidate has one nonblocking `git diff-tree --check` warning: an extra
blank line at EOF in `root_preparation.py`. The prior independent gate records
this as a cleanup nit, not a correctness blocker; the manager may trim it and
rerun the small Root lane if repository whitespace policy requires it.

```bash
git -C /home/user/work/agent diff-tree --check \
  634867fed71b4ae53acaa3c3162315527c2bdb23^ \
  634867fed71b4ae53acaa3c3162315527c2bdb23
# warning only: root_preparation.py has one new blank line at EOF
```

Minimal direct checks used on the composed private tree:

```bash
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-tree> \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-current/node_modules \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/rendering/test_remotion_capture_scene_props.py \
  tests/packs/rendering/test_remotion_native_window.py \
  tests/packs/rendering/test_remotion_layer_tail_compat.py \
  tests/packs/rendering/test_remotion_scratch_guards.py \
  tests/packs/rendering/test_scene_source_carry.py \
  tests/packs/rendering/test_capture_scene_labels.py \
  tests/packs/rendering/test_composed_frame_capture.py \
  tests/packs/rendering/test_normal_audio_run.py \
  tests/packs/rendering/test_normal_audio_sources.py \
  tests/packs/rendering/test_normal_audio_source_phase.py
```

This passed `219 passed` in 164.12s. The six unchanged structure/import checks
passed separately (`6 passed`); the focused Root context/fingerprint subset
passed `11 passed` in 25.38s. The composed candidate inventory check passed
(`1 passed`), with the 1,200/50 limits unchanged.

The existing central named HTTP/PCM/phase/backend/lock command from the Root
handoff is the required small HTTP gate; it passed on the final candidate tree
`e2ac895d16ab205221358aeee9b8540f57f71779`:

```text
request-test vw-m3-root-prep-lifetime-extract integration-viewing-normal-pcm-http-final-current --files <handoff file list>
wait-test vw-m3-root-prep-lifetime-extract-integration-viewing-normal-pcm-http-final-current-1020133642-9871
=> 82 passed in 63.83s, exit 0
```

It was not duplicated from this read-only owner review. An initial local
focused attempt used the ordinary `agent-remotion` fixture, which lacks
`normal-audio-sources.mjs` and produced six fixture-environment errors; the
rerun with the existing `agent-remotion-current` PCM fixture passed all 11.

## Limits and next steps

No full suite, browser/real-render run, D09 private-crop deletion, physical
frame/audio parity, SDK explicit-Scene/save-core integration, or query
qualification is claimed. Inventory thresholds remain unchanged. Manager may
merge the approved service commit first, verify the service gate, then merge
the approved Root commit and verify the Root/HTTP lane plus combined inventory.
