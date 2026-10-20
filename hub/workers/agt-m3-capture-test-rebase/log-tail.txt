All 21 `tests/sdk/test_capture_source_runtime.py` tests now pass against Runtime `tl/integration`. The 2 failures in `test_commit_runtime_m1.py` are pin drift, which I left unfixed as instructed. I wrote the commit message and created `DONE`.

## What was wrong
- **Real Agent bug:** the 4 happy-path tests failed with `capture differs from authoritative registry`. Runtime now requires a capture's registry to equal its own projection exactly. `prepare_filmstrip` (`astrid/sdk/timeline_filmstrip.py`) was enriching the registry with `content_sha256` first, so every real composed capture would have been refused at admission.
- **Fix:** `_runtime_snapshot_registry` still runs, so media admission is still checked, but its output is discarded and the projection is sent as is. The host already derives the digest from content-addressed `sha256:` media ids (`_managed_asset_identity`). Non-content-addressed media ids that relied on the injected `content_sha256` would now be refused by the host, since opaque ids need an explicit digest.
- **`ref()` fake:** it already used the real `service.ingest` path, so I didn't change it.

## Test changes
- **Strict xfails:** I removed the markers on the 14 cases (2 missing-candidate, 12 forgery). They all showed `XPASS(strict)` before removal. After removal they pass, and no assertions changed. The forgery test accepts any Runtime or Host refusal, and I didn't check each refusal's reason. I also updated the stale docstring and comments.
- **Duplicate-ref test:** `test_replaced_duplicate_capture_ref_is_refused_at_host` is now `…_at_admission`. Runtime refuses the replaced ref earlier, with `ValidationError: filmstrip authority reference differs from admitted authority context`. The old expectation was a `HostError` at materialize. It is still a refusal, but please check you're happy with that rewrite.
- **Overview fixture:** `tests/packs/rendering/test_timeline_visualize_overview.py::test_runtime_expansion_names_shots_from_payload_name_before_shot_id` was failing with `KeyError: content_digest`, in code I didn't touch. The fixture rows lacked the closure image fields (`content_digest`, `revision_id`, `timeline_id`, `payload`), so I added them.

## Runs (all via `request-test`, no full suite)
| Run | Command | Result |
|---|---|---|
| `commit-integration`, before | `tests/sdk/test_capture_source_runtime.py` + `tests/editing_conformance/test_commit_runtime_m1.py` | 21 failed, 2 passed |
| `commit-integration`, after | same files | 21 passed, 2 failed |
| `targeted`, neighbours | filmstrip, capture-projection, capture-closure-source, filmstrip-invocation, visualize-authority-objects, filmstrip-execution, visualize-overview, native-timeline-facades and revision-diff-admission tests | 186 passed, 1 failed, 2 xfailed (the failure was the overview fixture above) |
| `targeted` | `tests/packs/rendering/test_timeline_visualize_overview.py` | 14 passed, after the fixture fix |

The overview fixture fix was verified only by that last single-file run, not by re-running the other neighbour files.

## `test_commit_runtime_m1.py`: 2 failures, pin drift
- **Failing tests:** `test_cli_python_outbox_restart_and_guarded_inverse[disjoint-rebase-undo]` and `[touched-basis-conflict]`.
- **Error:** both fail with `runtime health schema digest sha256:7486348f… does not match this Astrid client's expected sha256:4e52f7df…`.
- **Cause:** Agent's vendored client in `astrid_runtime_client/` (via `runtime.lock.json`) carries `4e52f7df…`. Runtime `tl/integration` HEAD `b2a1d9fd` carries `7486348f…`, and the component manifest `1ad76db2…` is the same on both sides. The last Runtime commit to touch `packages/python/astrid_runtime_client/` is `8308cb9` ("expose exact retained project-pack object read"), so the Agent lock predates it.
- **Recommendation:** move Agent's vendor lock to Runtime `tl/integration` at `b2a1d9fd`, or at least `8308cb9c153d`. That means re-vendoring the files in `runtime.lock.json`. The schema digest changes with them, and `timeline-config.schema.json` is also listed there.

I changed no pins and requested no `full*` suite.
