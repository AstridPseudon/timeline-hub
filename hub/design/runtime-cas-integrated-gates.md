# Runtime CAS integrated gates

**Result: PASS for the selected-media CAS integrity fix on current integration.**

Verification date: 2026-10-20.

## Exact source and preserved ancestry

- Runtime commit: `a51af885ea631c695a857985239c7fe7bf2e871f`.
- Runtime tree: `7c6ab6700307309a7942e64eb4d0c6c7cc42b681`.
- Current `/home/user/work/runtime` is clean at the same commit/tree.
- `81f8c7e` (catalog-head fence), `c45cbc6` (native historical admission), and
  `16acbb6` (door-audit race) are ancestors. The shell repair ancestry is also
  retained (`b748ae7`, `70102ac`). `runtime_protocol/timeline_commit_store.py`
  is byte-identical from `81f8c7e` through `a51af885`.
- Agent checkout used by the central marked lanes: commit
  `30fc8dd154015a7c58cf4ce7b065ccc46f470ee8`, tree
  `50925d6df67ce717653e3ce7ac12803f8865da93`.
- Tracked `tests/astrid-agent.pin` remains `1a407fefad05c498836a25594ed603e9a543705d`;
  this verification did not repin it.

## CAS and commit evidence

Local, socket-free, exact current worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --runxfail -m integration \
  tests/test_timeline_clip_replacement.py::test_native_clip_swap_is_atomic_cas_and_exactly_replayable \
  tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_tampered_cas_without_mutation \
  tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_selected_source_corruption_between_capture_and_accept
3 passed in 20.21s
```

These are the bounded controls for exact accepted retry, same-size pre-capture
corruption, capture-to-accept corruption, and zero durable mutation. The race
case asserts unchanged SQL dump, timeline head, command-idempotency rows, and
unchanged corrupted CAS bytes.

Central socket-capable service, exact current integration tree:

```text
request-test integration:runtime marked-integration --files \
  tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route
runtime-marked-integration-1020154417-1102
1 passed in 2.32s; runtime snapshot tree 7c6ab6700307309a7942e64eb4d0c6c7cc42b681

request-test integration:runtime marked-integration --files \
  tests/test_timeline_commit_integration.py
runtime-marked-integration-1020154505-16706
9 passed in 4.28s; runtime snapshot tree 7c6ab6700307309a7942e64eb4d0c6c7cc42b681
```

The first lane is the one marked actual native HTTP replacement case. The
second is the nearest nine-test commit lane; prior 9-test evidence was on an
older tree and was not reused.

## Public artifact boundary

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
contract/artifacts.json is current
```

`contract/artifacts.json` has 75 paths and is unchanged from `81f8c7e`, as are
the generated Python/TypeScript client files and conformance generated client.
The public contract remains `0.2.13`, schema digest
`sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
and the public EditCommand union has 22 operations. The normal `0.2.14`
candidate's 29-operation surface is not present here and is not claimed by
this report. Frozen `310`/normal `014` sources were not needed because the
merged fixture already exercised the selected-media controls.

The only paths changed from the promotion parent are the reviewed CAS port and
native replacement test file:

```text
M runtime_protocol/timeline_commit_port.py
M tests/test_timeline_clip_replacement.py
```

No product or test files were modified during this verification. No new
xfail/skip was added. The completed Runtime full `16434` belongs to the
separate promotion-only START state: merge `81f8c7e0b22c34804015c054762af3d737e4698a`,
tree `0e3a5b938d9ca489fc760b09d34b02d4ac9aad51`; it reported 5523 passed / 14
failed / 18 skipped / 22 xfailed. It does not cover this later `a51` CAS tree
and is not used as CAS evidence.

## Limits

This qualifies the selected-media native CAS capture/accept boundary and one
public native HTTP positive. It does not qualify all public operations, the
unpublished 29-operation candidate, renderer/audio behavior, or the unrelated
full-suite failures.
