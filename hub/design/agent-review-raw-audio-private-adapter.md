# Agent raw-audio private adapter review

## Decision

**HOLD** for Agent commit `8f15518ed346c9d6785a7664c327163057efafe2` (tree
`721d3f14a462841599743fef24fa17969b628823`). Scope reviewed: that commit's
changes to `_trim_commands.py`, `commit.py`, `sync.py`, its focused test
changes, and `docs/agent-raw-audio-trim-private-adapter.md`.

This is a source/pure-Agent review only. It is not an end-to-end qualification
and does not pair with rejected Runtime candidate `ab4cc...`. Pair only after
the corrected Runtime counterpart is committed and reviewed; the active
corrected branch currently resolves to `e220670e40e196fb8f37dd8ce5d558fe0f6adf1c`
(source fix `89fb7dcd113023d7e1e044d537202caca509830a`).

## Blocking finding

The Agent record does not capture the original request-scoped duration read.
`clip_trim()` reads the authored registry fields and records
`trim.source` as an entity dependency, but `_verified_source_duration()` only
consults transient `ctx.verified_media`; it never records a
`duration_seconds` read/state tied to the exact base `MediaPin`. The command
therefore has no recorded original duration claim for the proposal's
capture/replay contract.

Concrete pure probe on this tree:

```text
record_reads_duration_seconds = []
record_dependencies = trim.source -> {asset: voice, source: {media_id: pin, duration: null, ...}}
original_trim = {from: 0.0, to: 8.0, hold: 8.0}
changed_replay = {from: 0.0, to: 7.0, hold: 7.0}
```

The probe captured with a positive `duration_seconds: 8`, then replayed the
same command with positive `duration_seconds: 7`; replay succeeded and changed
the trim. This violates the agreed requirement that capture declare the
original duration read/dependency so replay/acceptance is based on the same
bytes and request-scoped result. The Runtime authority's later recomputation
does not repair the missing Agent record; it only protects the Runtime path.

Required correction: record the exact existing media-pin dependency plus the
`duration_seconds` read/state during capture, and make replay verify that
original claim while retaining the Runtime recomputation. Preserve absent
metadata as a visible refusal, not a guessed duration or a weakened guard.

## What passed / what was inspected

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest --collect-only -q tests/editing_conformance/test_recipe_m2_clip_trim.py` — 121 collected.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_clip_trim.py` — 121 passed in 8.88s.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest --collect-only -q tests/editing_conformance/test_recipe_m2_clip_trim.py tests/editing_conformance/test_recipe_parent_media.py` — 146 collected.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_parent_media.py` — 25 passed in 3.72s.
- `git diff --check 8f15518e^ 8f15518e` — passed.
- `py_compile` of the four changed Python/test modules — passed.

The reviewed diff adds no public command field, schema/DTO, selection,
registry-duration write, table, decoder, ffprobe save path, or generation
adoption. Exact base-pin discovery, Runtime `media_info` consumption, WAV-only
authoring preflight, source-time hold/speed, boundary handling, opaque data,
and inverse guards are otherwise scoped as intended. The local preflight is
nonauthoritative and failures remain visible through the missing verified
metadata refusal.

## Counterpart conditions

1. Do not pair this Agent source with Runtime `ab4cc...`; that counterpart was
   rejected for verify-then-path-reopen read TOCTOU.
2. Pair only with the corrected committed Runtime counterpart after its
   descriptor-stable single-FD fix is present and its focused tests pass.
3. Before any native/raw-music qualification, land an Agent successor that
   records and verifies the original `duration_seconds` read/dependency, then
   rerun the 121-test trim lane and the nearest pure/provider lanes. Only then
   run a bounded paired acceptance proof. No full suite was run here.

