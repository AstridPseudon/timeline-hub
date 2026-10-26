# P5 D141 final-Agent source applicability

## Verdict

**PASS_SOURCE_APPLICABILITY** for the original P5 execution boundaries with Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` and final Agent `ec0a9f5baef2c31bc5179087b83f044524575182` / tree `83b84c79941917fde535ee3ddba5533a776cace3`.

The original actual `runtime-d141-p5-cut-1026013331-6934` receipt remains the proof: 38/38 passed in 31.02s on Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` / Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70`. This review does not create a body, receipt, semantic retarget, or new P5 run.

## Exact successor delta

The required exact command reports 11 changed paths from ecdc to ec0a:

- Production: new `astrid/core/timeline/inverses.py`; modified `astrid/packs/timeline/cli_native.py`.
- Tests only: nine test paths, including inverse tests and CLI/presentation coverage.

The inverse file is genuinely production source, but static source inspection found no import of `astrid.core.timeline.inverses` anywhere in the final production tree. Existing `timeline.inverse` handling remains in `astrid/sdk/timeline/inverse.py` and the unchanged provider/command modules; the additive planner is outside the P5 closure.

`cli_native.py` is also genuinely production-called: `astrid/packs/timeline/cli.py:2241` calls `commit_document`, `:3179` calls `dispatch_ordinary_edit`, and `:940` calls `show_native`. Its changed conflict presenter and detached-document summary are therefore not dead code. They are nevertheless outside original P5 execution: P5 directly builds `capture_move` and loads the Agent Runtime provider, then posts the Runtime commit/restore route through the door. No P5 test imports or calls the CLI parser or `cli_native.py`.

## Retained P5 closure

The final Agent bytes for `astrid/sdk/timeline/api.py`, `capture.py`, `commit.py`, `_common.py`, `astrid/core/timeline/authoring_bundle.py`, `astrid_runtime_client/generated.py`, and `astrid_runtime_client/contract_metadata.py` equal the original Agent 28e blobs and SHA-256 values. The provider boundary remains `astrid.sdk.timeline.capture`, `astrid.sdk.timeline.commit`, and Runtime `runtime_protocol.timeline_commit_provider`.

Runtime’s 6a→95d delta remains exactly two generated TypeScript metadata outputs plus `runtime_protocol/upgrade.py`. The only Python hunk adds `threading`, `db_path`, and an `RLock` in `_validate_candidate`. P5 setup calls `migrate_canonical_to_current` at `tests/test_timeline_commit_crash.py:81`; static caller inspection shows `_validate_candidate` is reached by `upgrade_realm`, not that migration route. The P5 provider, daemon, service, door, store, port, utility, visual seam, Runtime metadata, and package boundary are byte-identical across 6a/95d.

Runtime’s own `tests/conftest.py` and `tests/lanes.py` own P5 collection. `tests/astrid_checkout.py` only prepends the Agent package root for the `astrid_importable` fixture. Agent test conftest/lanes changes are not loaded by P5.

The Agent lock is byte-identical from ecdc to ec0a and still selects Runtime 95d. The 15 consumer mappings, manifest, producer, producer version, and source hashes remain unchanged and match the Runtime 95d artifact manifest/source custody recorded in the prior independent evidence. No contract C0 shape changed.

## Boundary safety

The retained Agent capture path still validates timing values as finite numbers, uses only authored start/`at_ms` data (with the existing finite zero fallback for an absent occurrence placement), and requires an explicit positive authored duration/window. The Runtime crash source installs an `_unavailable` tripwire for renderer, provider, source readers, and candidate compilation after the measured boundary; the host-first-capture provider is explicitly a host-boundary fixture, not a substitute Agent semantic collector. No new source acquisition or alternate collector was added by ec0a.

## Limits

No imports, collection, provider calls, preflight, tests, typecheck, lint, full suite, source refresh, package/environment/network acquisition, service/queue/registry/kit/CAS/Store/hub/Git write, cleanup/deletion, fixture/assertion/generated/pin/DTO/schema edit, build/ZIP, credentials, D130, or stopped-investigation retry was performed. Integrated53 and final Agent publications were retained as source facts only. The observer first-tool gap is disclosed in `disk-trace.txt`.
