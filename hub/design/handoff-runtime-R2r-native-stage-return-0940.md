# R2r native-stage return — PASS

Base: `1365e4b17b31c4a7093d5943674637067fd2bab4`, tree `6c69c3dc47822fffbaf27cd63815d2895155ffaa`.
Only the two permitted production files and the new inverse-stage test file changed. No git writes or borrowed ancestry; harness commit pending.

## Change and decision

Recovered the cumulative `b3367ab8f` authentication/store/test delta using `git show`, while retaining D17's `source_revision_closure` and all other D17 files/interfaces. Store AST changes are limited to `_verify_accepted`, `_validate`, and the new authenticated-history handoff.

Stage membership now requires the complete ordered native ref/path sequence to equal either the reversed authenticated source-native sequence or the exact ordered canonical effect sequence. The existing source-derived native cardinality remains mandatory. The canonical representation is required by the unchanged grouped intermediate-image positive; the finer native representation preserves genuine sequential parent/container observations. Neither route admits arbitrary path overlap, additional facts, omitted facts, or reordered/duplicated native facts. Every native observation still receives sequential before/after authentication, and its entire projected physical-root payload map must equal the authenticated stage output. Existing provenance/ranges/physical-binding/digest/history guards remain active.

Added the reviewer's exact first-write replacement as a normal main-suite test, plus a separate source-membership-without-effect-coverage forgery. Both preserve full SQL dump byte/value equality and public history on refusal. Added actual-Agent add/remove/change-path/duplicate/reorder/replacement variants and an exact retry of the original canonical grouped-image positive. The original 367-line, 20,020-byte test prefix is unchanged.

## Exact commands and results

The first requested lane was split because `test_timeline_commit_read_basis.py` contains a localhost HTTP fixture, which must use the central service. Its complete coverage is **33 + 73 + 12 = 118 passed**, with no excluded cases:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent:/tmp/w-bcafc22f99 ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p capture_wire_r2r tests/test_timeline_inverse_stage_authentication.py
# 33 passed in 23.50s (final-native.log)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py
# 73 passed in 10.86s (auth.log)

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-R2r-native-stage-return-sol-0940 targeted --files tests/test_timeline_commit_read_basis.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-R2r-native-stage-return-sol-0940-targeted-1023095026-20055
# 12 passed in 4.61s; service exit 0; snapshot 63da3d89c3dabc59d82cf50f0e25690aff042a59

CORRECTASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_acceptance.py tests/test_timeline_commit_integration.py -k 'inverse or history'
# 10 passed, 68 deselected in 10.18s (final-inverse-history.log)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py tests/test_timeline_commit_inputs.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_port.py
# 101 passed in 17.88s (final-d17.log)
```

The wire plugin records complete requests, replies, failures, prepared records and loaded module paths; it changes no product data or assertions. Earlier combined auth/inverse run: 105 passed before the final additional coverage case; final 33-file run includes that additional case.

Regression sensitivity checked in a private overlay using the recovered b336 authenticator and this worktree's store:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python /tmp/w-bcafc22f99/baseline_probe.py -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py::test_reviewer_replaced_native_write_is_refused_before_persistence
# Expected baseline RED: both variants failed with DID NOT RAISE (final-baseline-red.log).
```

Static/preservation commands:

```sh
ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
# clean
ruff check --no-cache --output-format=json runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py
# current/parent: 11 identical inherited store diagnostics, zero added/removed
pyright --outputjson runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py
# current/parent: 76 identical diagnostics, zero added/removed, including source-line mapping
python /tmp/w-bcafc22f99/compare_static.py
PYTHONDONTWRITEBYTECODE=1 python /tmp/w-bcafc22f99/verify_preservation.py
git diff --check
# PASS: compile/AST; 77 frozen files identical; 277 existing tracked test files identical byte-for-byte and Python AST.
```

The parent currently has 277 existing tracked test files, rather than the brief's older count of 276. All are preserved. All original 15 store controls and nine actual-Agent cases remain unchanged and pass.

## Evidence and limits

Evidence manifest: [evidence.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-native-stage-return-sol-0940/evidence.json).
Artifact directory: `/tmp/w-bcafc22f99`; final wire: `final-production-wire.jsonl`; module origins: `loaded-modules.json`; preservation/static summaries: `preservation.json`, `static-identity-comparison.json`.

Loaded Runtime auth/store originate in this worktree. All 59 loaded Agent module bytes match the normal `/home/user/work/agent` checkout at `c424ee9a54f0c0fc3471a9fd99c7763455bda36e`. Final inverse-wire capture contains 74 full requests, 46 replies (43 accepted, 3 preview), 28 refusals, 67 prepared accepts and 3 prepared previews. Legacy `rebased` receipt/history preservation is exercised by the named acceptance lane; complete canonical closure/readback and exact retry remain exercised by the real-Agent positives. Generated request/reply schemas and clients are among the untouched frozen files.

No full, broad native/crash, browser, P4 or additional HTTP lane was run; no daemons were started. This evidence exercises normal service/store/provider production modules; a fresh RuntimeDaemon/WorkspaceClient mutation journey was not run in this task. The central read-basis fixture exercised its existing generated-client HTTP read. No product schema, pins, fixtures, Agent files, or existing tests changed. H3 remains NO-GO; V4 remains cut.

No blocker. Next step: harness creates the single own commit, then immediate independent review, specifically checking exact canonical/native membership and full-image coverage before integration.
