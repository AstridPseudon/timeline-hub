# Agent ordinary014 current initializer/source candidate

Status: **APP source candidate only; not an integration pin, release, activation,
or App/browser qualification.** This is a routine merge-forward composition of
the approved initializer source with the current Agent integration delta.

## Exact source identity

| Item | Value |
| --- | --- |
| Approved initializer parent | `2585e01cd2a198d3a091066848bd72152955bb0a` (`tl/agt-review-init-opaque-inverse-real`) |
| Approved initializer parent tree | `5b314600becfbfc13c36b0183e4b07d7ad064ecb` |
| Current integration merge parent | `f133a87986d839d7716d3efac2c2ba25fe036098` (`tl/integration`) |
| Current integration tree | `3f38f816181d7564e5cd7db4d9672a0d6dea9ac3` |
| Common base for the forward delta | `30fc8dd154015a7c58cf4ce7b065ccc46f470ee8` |
| Expected candidate tree before harness commit | `5f17c47a36b75a69e1fa50fd1cc3a1e54e1a80c0` |
| Candidate HEAD | Harness-assigned two-parent commit after worker exit; first parent is the approved initializer parent and merge parent is `f133a879` |

The expected tree was calculated from the clean approved parent plus the exact
`git diff 30fc8dd1 f133a879` patch. The harness owns the commit, so this worker
does not invent a commit SHA or run `git merge`.

## Composed delta and boundaries

Only the six paths in `30fc8dd1..f133a879` were applied:

```text
astrid/sdk/timeline_sheet.py
tests/editing_conformance/test_native_sheet_current_runtime.py
tests/packs/timeline/test_cli_assets.py
tests/packs/timeline/test_cli_native_sheet.py
tests/packs/timeline/test_cli_voice_bindings.py
tests/sdk/test_timeline_sheet_native.py
```

NativeSheet now maps omission of an addressed `parent/clip:<id>` row to the
existing captured `clip.delete` command, while track/occurrence omissions and
row additions remain refused. The tests cover sibling/opaque/order retention,
lost-ACK restart retry, guarded undo/redo, disjoint rebase, and membership or
already-deleted selection conflicts. The two CLI fake-checkout fixtures retain
their `_check_core` seam; the CLI native-sheet test covers the omission path.

No WC3, WC6, D13, audio, private carrier, project-data, Mouth, schema, Runtime
source, generated client, lock, Composition, App, or public013 changes were
included. Existing normal014 bytes from `e86f44d0` and ordinary current-source
bytes from `ee896821` remain untouched.

## Immutable normal014 tuple

- Runtime producer checkout: `/home/user/work/wt/rt-pin-a0dca169`
- Producer commit/tree: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` /
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- Package: `0.2.14` (unpublished)
- Frozen Agent schema source: SHA-256
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
  (`$defs`: 55; command operations: 29)
- Runtime wire schema digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`
- Runtime artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`
- Runtime `contract/artifacts.json` SHA-256:
  `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`
- Agent `artifacts.json` SHA-256 (unchanged):
  `6963e3393d22b8e46d1df5f2cb81f401bee7080407bd3f61f108560a2ef9a176`

`scripts/vendor_lock.py check runtime.lock.json --producer
/home/user/work/wt/rt-pin-a0dca169` passed. The lock, generated client files,
schema, and artifact manifest compare byte-for-byte with the approved `e86f44d0`
parent. No source refresh or artifact regeneration was performed.

## Tests

Local targeted lane (no bytecode or pytest-cache writes):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/sdk/test_timeline_sheet_native.py \
  tests/packs/timeline/test_cli_assets.py::test_edit_replace_asset_and_swap_asset_forward_to_the_sdk \
  tests/packs/timeline/test_cli_native_sheet.py::test_clip_row_omission_is_native_delete_and_keeps_other_rows \
  tests/packs/timeline/test_cli_voice_bindings.py::test_replace_insert_and_from_script_forward_existing_sdk_arguments
```

Result: **74 passed in 6.52s**.

Central exact generated014 HTTP lane, requested once on this combined source:

```text
agent ordinary014-consumer-integration
  tests/sdk/test_timeline_pristine_initialize_runtime.py
  tests/editing_conformance/test_native_sheet_current_runtime.py
```

Result: **pending central test-service completion at report time**.

No full suite, App/browser journey, release, integration pin, or renderer/audio
qualification was run or claimed. The earlier 143-test `e86f44d0` actual-provider
proof remains historical evidence and is not relabeled as this candidate's
qualification.

## Next step

After the central lane completes, the orchestrator may review this source
candidate as the normal App2/Runtime cohort input. App2 and Runtime must retain
the exact producer/schema/artifact tuple above; `e86f44d0` and `310e5484` remain
immutable.
