**Option C only partly works.** The capture chain's code lands on tl/integration without 435357ae. Of its tests, the source-materialization ones can't run without 435357ae. The `commit-integration` evidence you asked for can't be produced against Runtime tl/integration at all.

## What landed
The unit is 3c382f4d + b30b164c + 95e770b5 minus 435357ae.
- **`astrid/sdk/timeline/commit.py` and `managed_timeline.py`:** applied cleanly (capture projector and image-field constants).
- **`astrid/sdk/invocation.py`:**
  - One conflict, in the `canonical_capture` hunk. Resolved by taking the 3c382f4d side, because it needs only the `capture_snapshot` mapping and not 435357ae's `mode` check.
  - It also has the `runtime_capture` candidate forwarding and the b30b164c uncertified-CAS ref.
- **`astrid/sdk/timeline_filmstrip.py`:**
  - 95e770b5 (no `content_sha256` enrichment) applied cleanly.
  - I also took three small producer-side hunks from 435357ae, because the closure tests need them: `content_digest` on shot rows, `parent_content_digest` in the candidate authority, and the project/timeline scope check in `_open_candidate_input_closure`.
- **Tests:** `test_timeline_capture_projection.py` and the b30b164c additions to `test_visualize_authority_objects.py` came in as-is, plus the overview test fixture. I dropped the `test_zz_probe_forgery_unmarked.py` hunk because that file doesn't exist on integration.

## What needs 435357ae
- **`astrid/core/rendering/verified_source.py` (new):** `reject_source_keys`, `RESERVED_SOURCE_KEYS` and `SOURCE_ENV`.
- **`GenericPackHost._materialize_inputs` in `astrid/core/execution/generic_host.py`:** the `timeline_source` materialization.
- **`reject_source_keys` calls at the top of `prepare_filmstrip` and `invoke`.**

These are the machinery behind the host-owned source. The source-key refusal and the host source materialization have no thin replacement.

## Tests (venv-agent, run from the worktree)
- **Targeted batch:** `pytest -q` over the filmstrip, invocation, managed-render, commit-provider, public-surface, cache, capture-projection, authority-objects, closure-source and overview tests gave **248 passed, 9 deselected, 9 xfailed**.
- **Capture source tests:** `test_capture_source_runtime.py` plus the projection test gave 32 passed, 30 deselected.
- **Ruff:** the F821/F401 check on the touched files is clean.
- **Strict xfails, with the original expectations kept:**
  - In `test_capture_closure_source.py` (7 cases): the CAS-metadata-can't-mint-source test and the reserved-source-key refusals.
  - In `test_capture_source_runtime.py`: the four tests that read `timeline_source`.
  - Each carries a reason naming 435357ae.
- **Admission-only tests:** the two in `test_capture_source_runtime.py` that don't read the host source (`test_missing_candidate_certificate_refuses_before_admission_writes` and `test_replaced_duplicate_capture_ref_is_refused_at_admission`) are left as-is.

## `commit-integration` against Runtime tl/integration
`commit-integration --files` over the four capture files plus the m1 conformance test: **fail**, 32 setup errors (`1020052211-10633`).
- Every error is `RetiredRouteError: legacy timeline writes are retired` from `publish_parent_composition`.
- The `source_runtime` fixture publishes an untracked parent chain through that retired route.
- The unmodified `tests/editing_conformance/test_commit_runtime_m1.py` hits the same error, so it fails the same way without my change.
- The 9 integration-marked projection and source-runtime tests therefore have no Runtime evidence. Those fixtures need a Runtime that still accepts untracked publishing, or a rewrite onto `commitTimeline`.

## Decisions and caveats
- I left `**expansion` out of the authority and the `reject_source_keys` call out of `prepare_filmstrip`, since both exist only for the verified-source path.
- The skip-objectify path (`canonical_capture`) isn't exercised end to end. The escalation says `rendering.timeline_visualize` never emits `capture_snapshot_ref` on integration, so Sol's finding may still hold. I checked only that the unit tests pass.
- Because of that, this unit probably doesn't restore the live preview on its own. Option B on the Runtime side is still the fast fix.
- The full Agent suite was not run, per the brief.
- The index conflict in `invocation.py` is resolved and staged. I wrote the commit message and created `DONE`. I did not create `BLOCKED`.

**Recommended next steps:**
1. Decide between taking this unit as-is, with the 435357ae-gated xfails, and landing 435357ae as the gated unit.
2. Rewrite the `source_runtime` fixture onto `commitTimeline`, or qualify it against a Runtime that still has the legacy route.
