# Runtime source review: Agent raw OLD swap on floor5672

Date: 2026-10-21 UTC

## Verdict

**SOURCE ACK**, bounded to the committed Agent source `9b9baa01ab43bce144f3f1e6d6d73722df99a8e7`, tree `f924720e382d442f391d45cdc6e24064be9a6a5e`, parent `5672d2b7deee2bfe2ab375fd6db5fc35a192591d` (`floor5672`). No concrete source counterexample was found.

This is a closed-contract/custody ACK only. It is not Runtime generation, artifact/client, version or pin movement, freeze, adoption, activation, native, socket, browser, render, or full-suite approval. The uncommitted future composition mentioned by the packet was not reviewed. Published014 compatibility is not claimed; ordinary/published014 remains the separate ordinary6ba lane.

## Exact source and schema evidence

- The committed patch changes exactly the eight packet paths and no caller path:
  `astrid/core/timeline/schema/edit-command.schema.json`,
  `astrid/sdk/timeline/commands.py`,
  `astrid/sdk/timeline/commit.py`,
  `astrid/sdk/timeline/native_occurrence_media_commands.py`,
  `tests/editing_conformance/test_raw_old_swap_successor.py`,
  `tests/sdk/test_timeline_composed_schema.py`,
  `tests/sdk/test_timeline_current_union_schema.py`, and
  `tests/sdk/test_timeline_materialization_schema_union.py`.
- Raw schema SHA-256: `9e4b4421ebbba94f13f8f286c7ea1df5eb9ca128142ed904c92a993985954cfd`.
- Canonical `json.dumps(indent=2) + newline` SHA-256: `d3274d7ed2d4bd80691472dd94daf8f4b8041fc184f39f1dd562d5de5d6a15c2`.
- Full union inventory is 64 definitions and 36 closed operation clauses.
- Structural ordinary6ba reconstruction is 55 definitions / 29 clauses, SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Structural private84fc reconstruction is 59 definitions / 33 clauses, SHA-256 `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.

The existing lanes remain distinct: `clip.swap-media@1` and `occurrence.swap-media@2` retain their selected-media OLD behavior. The additive raw-OLD alternatives are `clip.swap-media@2` and `occurrence.swap-media@3`, with `old_media` exactly `{"media_id", "content_digest"}` and NEW exactly the existing five-field `selected_media` envelope.

## Contract/custody findings

- `validate_command` recognizes only the two raw-OLD operation/version pairs and validates them against the closed `RawOldSwapMediaArgs`; it does not broaden other versions.
- `RuntimeCommitService` calls the existing request-scoped `raw_media_info` only for raw OLD, and calls `selected_media` only for NEW. It does not use caller duration/metadata, adoption state, latest catalog state, or a new authority.
- The approved existing Runtime raw port is `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`, tree `d82f37052847949e77c12e1704c3f27c6dd56a46`. Its exact declared `MediaManifestEntry` membership, same-project `managed` custody, one-CAS-descriptor verification, candidate-manifest retention, and acceptance-time recheck are the required OLD boundary. The current Runtime integration head `b92d3e7a05eec65c142294ef4873edd059e9b31d` is not an ancestor of f53 and has no raw port; no current Runtime acceptance is inferred.
- Agent-side `_validate_pin`/`_raw_verified` require the exact raw pin and verified object identity/type/size before semantic execution. Owner patterns, the original clip row, and the original alias are read before the only authored write. Raw OLD alias binding is exact; NEW alias creation or reuse remains exact selected-media binding. Wrong original object, alias, owner, or undeclared pin therefore refuses before mutation.
- The swap changes only the target `asset`; the original clip row read preserves source window and opaque/sibling state, while the existing source-window, track, media-kind, and occurrence-boundary checks remain active. Existing recording, replay/rebase, guarded inverse, ABA, retry, and dependency behavior is retained. No caller was changed (`live callers changed: NONE`); the existing `native_voiceover` caller remains unchanged.

## Evidence

Read-only preflight passed for the exact commit/tree/parent, eight-path allowlist, import paths, schema hashes/inventory, and ordinary6ba/84fc floor reconstructions.

Exact mandated command, run once after that preflight:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_raw_old_swap_successor.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py
```

Result: **69 passed in 160.23s (0:02:40)**.

Not run by scope: Runtime installed/generation/client work, native qualification, socket/browser/render tests, and full suites. No source, product, schema, generated, version/pin, or repository documentation file was changed by this review; no scratch counterexample was needed.
