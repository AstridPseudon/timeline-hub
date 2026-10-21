# Agent private017 minimal materialization proof readiness

Date: 2026-10-21  
Scope: source-only Gate1/3 readiness from Agent `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`.

## Decision

No Agent product change or helper is necessary. The smallest existing bounded
proposal is one named suite combining the three existing private v1 refusal
selectors, their current-v2 replacements, and two Runtime-backed occurrence
lifecycle nodes:

```text
agent private017-materialization-minimal-normal42a
```

The proposal is not yet qualification evidence. It was not submitted to the
central service because the brief forbids private native/body execution.

## Exact identities and cheap guards

The reviewed source/pin tuple is:

| Input | Identity |
| --- | --- |
| Agent commit/tree | `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79` / `cc0a8dd1360324a1b440ba7d318a083e7f8814cc` |
| Runtime commit/tree | `42a7203f49bb89f299ec854cfbf2b1444e815a7c` / `1f220b3d3a27e8eb061b15c944bad784c8fdb82e` |
| Runtime package/artifact | `0.2.17`, producer `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0` |
| EditCommand schema | `sha256:6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16` (Agent and Runtime bytes equal) |
| Placement fixture | `sha256:87c59f76c683eac530e06511cb0dc6396f9c3dec3931a8bd0702606e2313e1f0` |
| Occurrence-media fixture | `sha256:59ef0259d6c5630ff01dbc1f77f4d4bafeeb36d72b68506aa12714be7cf9e0b1` |

The suite guard must set
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42a7203f` and
`PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f"`, and must assert the
Agent/Runtimes commit and tree identities above, `runtime.lock.json`'s source
commit, all 15 locked artifact hashes, the normal-client import path, and
`astrid_runtime_client.contract_metadata.CONTRACT_VERSION == "0.2.17"`.
Use `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, and
`-p no:cacheprovider`; do not create caches in shared installs.

## Proposed selectors

These are the exact collected node IDs on this tree:

```text
tests/editing_conformance/test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo[fixture_path1]
tests/editing_conformance/test_recipe_m2_placement.py::test_private_carrier_placement_v1_refuses_without_refreshing_original_claims
tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2]
tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_v1_refuses_original_claims_with_draft_kept
tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_equivalent_reauthored_v2_succeeds
tests/editing_conformance/test_recipe_occurrence_media.py::test_private_carrier_swap_v1_refuses_without_refreshing_original_claims
tests/editing_conformance/test_materialization_version_boundary.py::test_obsolete_capture_refusal_keeps_exact_durable_outbox_across_restart
tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[video-add]
tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[video-swap]
```

The first six selectors are the one-to-one AG-MAT rows:

- V01: private placement v1 refuses with the draft unchanged; the same
  materialization fixture's current builder is v2 and the golden test proves
  replay, JSON reload, strict inverse, and redo.
- V02: private swap v1 refuses without refreshing claims; the materialization
  fixture's `swap` golden is exercised with the current v2 builder.
- V03: the historical add remains 25 reads/3 selections and refuses; the
  reauthored current v2 success is 27 reads/4 selections and proves replay and
  inverse.

The outbox selector proves the old add draft, request bytes, flight identity,
and `capture_mismatch` survive a client restart and repeated flush. The two
Runtime selectors are the smallest normal Runtime pair for current v2 media:
one add and one swap, using the video case to retain source-window and exact
media-selection guards while exercising Runtime restart, ledger-first retry,
reload, inverse, redo, changed-payload refusal, and fresh identity-collision
refusal. They are not redundant: they cover V03 and V02 respectively.

Do not add Runtime's ordered-record or RT03 selector; those are Runtime-owned.
Do not add the public `old_sealed_placement` positive: it is the separate
103-read/3-selection S2 preservation case and is outside AG-MAT-V01..V03.

## Live callers retained

The relevant live call chain is unchanged:

- v2 selection: `capture_version` is called by `capture_move`, scalar/clip/
  shot/track capture, `native_placement_commands`,
  `native_occurrence_media_commands`, parent-reference, shot-pool, checkout,
  and the other existing source-bound native builders.
- accepted commit: `commands.execute` calls `_materialization.capture` and
  `verify_sources`; `commit.py` obtains accepted-history context through
  `accepted_context` before inverse/retry/reload execution.
- replay/inverse: `rebase.replay` calls `consume`; `inverse.py` calls
  `verify_sources` before consuming a recorded allocation; `sync.py` reloads
  accepted context and stages retries.
- Runtime-backed caller: `test_commit_runtime_occurrence_media.py` uses the
  normal authenticated Runtime commit service and provider, with the exact
  Runtime checkout selected by `ASTRID_RUNTIME_CHECKOUT`.

## Evidence run here

All commands used the shared Agent venv read-only, `PYTHONDONTWRITEBYTECODE=1`,
the exact Runtime checkout above, and disabled pytest cache writes.

```text
pytest --collect-only -q -o addopts= -p no:cacheprovider <nine source/runtime selector groups>
15 tests collected in 0.89s

pytest -q -o addopts= -p no:cacheprovider <12 local materialization/version selectors>
12 passed in 2.50s

pytest -q -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_materialization_version_boundary.py \
  tests/editing_conformance/test_materialization_map.py
66 passed in 6.83s

identity/artifact/schema/import preflight
PASS: Agent and Runtime commit/tree guards; runtime.lock source; all 15 locked
artifact hashes; normal-client/runtime imports; contract version 0.2.17

git diff --check
PASS
```

The Runtime-backed selectors were collected only; they were not executed.
No private native/body, HTTP/live socket, scene/render, browser, pin, install,
full suite, or central test-service request was made.

## Gaps and next step

There is no existing Runtime-backed `placement.move` selector for AG-MAT-V01.
The local V01 golden proves the current v2 lifecycle semantics, but not normal
Runtime admission. Also, the existing Runtime occurrence test does not assert
the materialization `id_map`/own-slot mapping directly; its current assertions
prove the accepted document, created asset, source selection, retry identity,
reload, inverse, and redo. Therefore the proposed suite is the smallest
readiness suite, not a complete current-pin qualification claim for all three
rows.

If the orchestrator requires “each row through Runtime admission” literally,
the next step is one narrowly scoped Runtime `placement.move` lifecycle
assertion using the existing materialization fixture and provider path, plus a
direct own-slot/id-map assertion in the existing occurrence lifecycle test or
its shared helper. That would be new proof surface; no such change was made
here. Runtime ordered/RT03 remains separate.
