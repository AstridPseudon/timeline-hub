The Runtime pin is done and the targeted tests pass. But the real-Runtime integration test for `test_commit_runtime_m1.py` could not be verified against the pinned tuple: the `commit-integration` lane runs a newer Runtime head, so its 2 `test_cli_python_outbox_restart_and_guarded_inverse` cases fail.

## What changed
- `runtime.lock.json` `source_commit` is now `94114269d1ce23ab3224d7eca5a85138ce2b5fed`. I confirmed the producer checkout `rt-pin-94114269` was at exactly that SHA first.
- I ran `scripts/vendor_lock.py update` against that checkout. It re-vendored `astrid_runtime_client/__init__.py`, `contract_metadata.py` and `generated.py`, with CONTRACT_VERSION 0.2.9 and SCHEMA_DIGEST `sha256:8d7f2987…`.
- `vendor_lock.py check` reports "ok (matches producer manifest)".
- Commit message and `DONE` are written.

## Tests
- **Targeted unit run:** 426 passed and 2 xfailed. The xfails were already in the suite; I added none. It covered:
  - `tests/test_vendor_lock.py`
  - `tests/stage1/test_vendored_workspace_client_parity_luna.py`
  - `tests/sdk/test_runtime_response_conformance.py`
  - `tests/sdk/test_workspace_client_timeline_commit.py`
  - `tests/sdk/test_capture_source_runtime.py`
  - `tests/sdk/test_timeline_sync.py`
  - `tests/editing_conformance/test_recipe_m1_commands.py`
  - `tests/editing_conformance/test_conformance.py`
  - `tests/editing_conformance/test_compile_contracts.py`
  - `tests/integrations/test_e2_publication_contract_roundtrip.py`
  - `tests/journeys/test_cross_client.py`
  - `tests/test_lanes.py`
- **`commit-integration` lane:** 17 passed, 6 xfailed, 2 failed.
  - `suites.conf` hard-codes `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, whose head is now `6023cfb` (the D13 regen merge, digest `sha256:3e5e78d0…`).
  - The vendored client expects `8d7f2987…`, so `connect()` rejects that Runtime's health response.
  - It is not a test bug.
  - To verify the pin, add a named suite like the existing `bundle1-runtime6be9706-integration` line. It should run `test_commit_runtime_m1.py` with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-94114269`. I can't edit `suites.conf`; I haven't run this and it needs your go-ahead.

## Decisions
- **Digest skew (item 2):** `89a396aa` and `a4e1eebd` don't appear anywhere in this base, so there was nothing to fix there. Nothing is hard-coded: `SCHEMA_DIGEST` comes from the vendored `contract_metadata`.
- **Superset (item 3):** I made no change. Agent's edit-command schema stays the superset of Runtime's 14 ops. The superset and vendored-client guard tests I could find pass, so I added no xfails. I didn't separately check that typed args classes exist for the extra ops. Runtime's section 5 says those ops only arrive with its next regeneration.
- **Composition (item 4):** I did not look at `tl/vw-m3-agent12-presenter-cohort`, so I have no conflict list yet.

## Next steps
- Add the pinned-checkout suite and re-run `test_commit_runtime_m1.py`.
- Note that Runtime integration has already moved past this tuple to the 0.2.10 / D13 regen. The next pin move will change the digest again.
