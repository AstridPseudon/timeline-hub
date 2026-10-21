# Agent transition complete-source review

Verdict: conditional approval of the transition feature after the schema-hash probe repair; the complete current-source join is not approved until the nine b3c current blobs below are restored. That nine-file repair is explicitly assigned to `agt-m2-next-transition-nine-current-blobs-repair-1043` and is outside this review's transition delta.

## Source/tree inventory

- Reviewed HEAD: `eebfe1035839b628e472b204c0c204a1d4127e2f`, tree `141e34d3e2bf95589841aabe0a7aba0f152e6480`, parent/approved private source `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`.
- Corrected transition reference: `1acc64610019cd13e344a4a4d75e84280b8b7f16`.
- Current integration reference: `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`.
- Old peer-repair reference checked: `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`.
- The feature delta from `6c1989adf` is limited to the transition schema/implementation/recording/authority/commit seams and focused tests; no old ca9 wholesale file copy was found.

The committed transition schema hashes are:

- raw file: `95193e5a1f90a8072f55deb19f8b7ac63dc5054130c14eab097f0dd73f149729`
- canonical JSON: `8500046e82587856c16cd6e241f27c886f9089538884a0b806fa75138a57cb49`
- transition-only strip canonical floor: `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`, matching the `ed5fd33c4` floor.

## Contract review

The focused source and tests cover:

- no-reference updates requiring both raw reference keys absent and exact transition type/revision presence;
- selected project-pack P1 authority and refusal on a changed revision/source;
- same-track predecessor adjacency and shortest-adjacent-clip fit;
- literal `params` absent, `null`, and object values with opaque literals retained;
- destructive non-empty-params-to-null refusal without mutation;
- exact inverse for paired transition/reference set and clear, including legacy `element_ref` cleanup/preservation;
- explicit rejection of transition aliases/compiled fields and no new rounding/frame policy.

Live Agent callers remain the existing `clip.set` path: `astrid/sdk/timeline/commands.py` operation registration, `native_checkout.py`, `timeline_elements.py`, and the sheet command map in `timeline_sheet.py`; selected-param hydration/authority is in `commit.py` and `_selected_param_authority.py`.

## Current-preservation finding

The candidate is based on approved `6c`, not byte-identical to current `b3c` for the nine files changed by `c4b964f6a..b3c96a758`. They must be restored exactly from `b3c`; no transition implementation file or schema pin should be changed while doing so:

```text
astrid/sdk/media_transcript.py                          d2d3b98960d7c118816663437362d2a7ebb5efe25b29424558fdbbcd350f9467
astrid/sdk/timeline_sheet.py                            0c448a48778f90bc4f6cf0302b84ee7aa1e17221363dfbb84342fd298036c3f8
astrid/sdk/timeline_transcripts.py                      36868a1e0937c067d1f06cdf589841ef59647a5e81bfe076e89a6fcae36a6281
tests/editing_conformance/test_commit_runtime_occurrence_media.py 0e3ca47ed177690035670bece0a0b68c92c55e98c91ee5d1ec3f6658a7e49bbd
tests/editing_conformance/test_commit_runtime_parent_media_swap.py 2bde457aa4f5313e98119aadfa2fd3fe6f4feb648f8f6274096b8d6dc4897222
tests/editing_conformance/test_native_sheet_ordinary_runtime.py e001ccb91bc88807e77a86e753ff90713698b5ad85e2c4811398f61df112cad4
tests/integrations/test_generic_host_remotion_render.py 39c4260d2868df9781b1a543fb5d8c1a1721264e37e1ee8fab820ee5a6c6772f
tests/sdk/test_media_transcript.py                    c825b05dde7979e18ff3dd02f59f0faa354fb2b7ed7ee55646990ce32457686d
tests/sdk/test_timeline_sheet_native.py                85f813720a0bcf8c9888acf3cb3be1fa93369c1b0772c94f67517d6bd7adc597
```

The approved private017 normal lock/client bytes are preserved exactly from `6c`: `runtime.lock.json`, `astrid_runtime_client/__init__.py`, `contract_metadata.py`, `generated.py`, and `timeline_commit_types.py` all have identical SHA-256 values against `6c`.

## Evidence

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_materialization_schema_union.py tests/editing_conformance/test_recipe_clip_scalar_fields.py` — **154 passed**.
- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q --maxfail=1 tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_scalar.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_selected_schema_runtime.py` — **174 passed, 33 deselected**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" timeout 45s /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions tests/sdk/test_timeline_current_union_schema.py::test_each_added_definition_and_operation_matches_its_approved_source tests/sdk/test_timeline_composed_schema.py` — **7 passed**.
- `git diff --check` — passed.

An initial provider-lane attempt without `ASTRID_RUNTIME_CHECKOUT` failed only because the runtime locator could not find a checkout; the rerun above supplied the shared read-only Runtime checkout and passed. No full, native, generation, browser, or broad suite was run.

Recommended next step: let worker 1043 restore and hash-check exactly the nine `b3c` blobs, then re-run its compact transcript/WC8/checker matrix. Preserve this transition finding and the schema-hash test when issuing the reciprocal Runtime/App ACK.
