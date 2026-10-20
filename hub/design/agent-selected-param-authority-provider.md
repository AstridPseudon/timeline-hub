# Selected PARAM authority provider

Implemented on isolated Agent branch `tl/agt-m2-selected-param-authority-provider`, base `ce363f6d6d60e504dbd4d79803c2d6299f648ade` (base tree `78af007de1d7c5a59f86fffacd9823de355cd260`). Final qualified source tree: `d35d0a36e4bc1f0a33f278a1bd798e4e857ec557`, captured by central targeted request `agt-m2-selected-param-authority-provider-targeted-1020130147-14497`. Harness commit SHA is not yet assigned. No Git mutation or integration edits performed.

## Change and contract

One internal helper, `astrid/sdk/timeline/_selected_param_authority.py`, walks the existing scoped accepted history through the exact HeadPin. It uses existing `_history`, `_records`, `_load`, and `State.matches`; no separate journal, history framework, persistence, endpoint, DTO or port operation. It requires consistent direct command/source/snapshot/element bindings and scoped raw target identity. Native config/object validation checks the winning association's actual portable snapshot bytes and descriptor.

New selected PARAM always requires its recorded original source, including unchanged and clear-only writes. A supplied admitted pin cannot bootstrap selection. Accepted complete PARAM records remain valid historical selection proof, including records predating enforcement; newly executed PARAM cannot create such proof without prior authority. Explicit set-element can select another pin with identical authored element JSON. Incomplete/malformed/later unproven relevant effects leave authority unavailable. Earlier bootstrap/legacy edges do not prevent a later explicit selection.

Provider checks base-stage authority and resolves again at the real head on rebase. Earlier records in the same batch supply the stage's authority; commands' original capture claims remain unchanged. Disjoint edits pass; changed P/E conflicts. Equal-state ordinary ABA remains allowed; inverse retains its existing stricter write guards.

Inverse resolves authenticated original targets to their exact previous publication boundary, including inverse of inverse and inverse of restore. Consumed inverse snapshot pins are never treated as restored selection. Revision-only restore considers every earlier matching accepted source publication; disagreement or missing authority leaves subsequent PARAM unavailable without changing restore or renderer behavior.

Size: helper 163 lines; provider 27 added / 4 removed; command callback 1 added. Total product addition 191 lines / net +187. Under the preferred 200-line bound; no expansion into a generic framework.

## Exact source and immutable public surface

- Agent schema SHA256 remains `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` (public S2).
- Vendored client `CONTRACT_VERSION = 0.2.13`, normal artifact producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a` from unchanged runtime.lock.json. No generated/public bytes or pins changed.
- Final native run used a private **git archive**, not a moving worktree, of Runtime `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, tree `1711b198be7f693f11ee4640eb0922ec0d0da952`. This server patch retains the normal published 013 contract. The private source archive was removed after testing.
- Helper SHA256: `38d30e8fca3566fdf6526e84e538d2f5be5a5d159c8b3ad18c560eb58d85e19b`.
- commit.py SHA256: `25920c4c155d81cf66a807e0129b7289b76c02ab7988054231b459bab56d4c5f`.
- commands.py SHA256: `19b3dee77735fad5dfb1de0d8db026aa89e2aea6382376c8cffc3572e11ed686`.

## Tests and exact commands

Commands ran from `/home/user/work/wt/agt-m2-selected-param-authority-provider`. Shared dependencies were read-only; bytecode and pytest caches were disabled in direct runs. No full suite was requested.

Final central targeted request (exit 0, **446 passed / 1 strict xfailed**, 107.70s pytest):

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m2-selected-param-authority-provider targeted --files 'tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider_scalar.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_recipe_occurrence_duplicate.py tests/editing_conformance/test_recipe_clip_scalar_fields.py'
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-m2-selected-param-authority-provider-targeted-1020130147-14497 0
```

The service command was `/home/user/work/venv-agent/bin/python -m pytest -q` followed by the eight files above. The direct run of the same files with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD`, `-o addopts= -p no:cacheprovider` also passed **446 / 1 strict xfail** before the final additional scalar-binding shape checks; central evidence covers the final exact tree.

Final real Runtime013 in-process service lane (exit 0, **26 passed in 48.88s**):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-selected-param-authority-provider/runtime-source /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/sdk/test_timeline_selected_schema_runtime.py
```

The RuntimeService fixture uses actual normal project/timeline creation, pack admission, immutable managed objects, command execution, acceptance, history, restart and ledger retry. It does not open sockets or browsers. Final log: `notes/native-runtime-frozen.log`. Earlier moving-worktree results are retained as diagnostics only; the frozen run is the exact-source qualification.

Native positives/negatives include: P1/P2 with the same E/O and equal complete canonical JSON after opposite explicit-selection orders; retained original max10 refuses16/accepts8 after newer max20 admission; caller pin switching; unchanged/clear-only/empty unselected refusal; exact object-only reads with unselected objects missing/corrupt; same-value reselection; mixed pins/targets and stage selection; disjoint peer rebase; relevant P and E conflicts; original exact retry after head selection change/restart; inverse/redo round trips; inverse BEFORE-selection; equal-revision ambiguous restore; and inverse-of-restore recovering the exact before-publication selection. Existing first-ledger retry assertions remain intact.

Portable replay (exit 0, **2 cases / 6 effects**, all record envelopes and whole canonical outputs equal to the original fixture):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/selected-param-original-pin-probe.py
```

Static checks (both exit 0):

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/_selected_param_authority.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py tests/sdk/test_timeline_selected_param_authority.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_selected_schema_runtime.py
git diff --check
```

The two original new strict probes are now real passes, with actual explicit-selection records establishing the pin. Expanded direct cases cover stage claims, ordinary/inverse ABA, occurrence materialization and sibling isolation, copied-target refusal, broken ancestry, and malformed/missing/duplicate associations. No original assertion was changed to expect lost behavior.

## Fixture provenance and required positive gaps

Existing selected fixtures previously used PARAM as their first selection or changed an admitted source implicitly. They now execute normal explicit set-element before the scenario, or immediately after birth inside the same birth batch. No history or prepared acceptance was fabricated. Mixed-pin tests explicitly select the intended initial/current source and retain all original state, maximum, opaque-field, restart/retry, exact-object and inverse/redo assertions. Record assertions select their original PARAM ordinals around the added explicit-selection command. The stale-source negative now explicitly selects the newer version before submitting the original pin, because a previously accepted original pin is correctly retained rather than becoming invalid on readmission.

One unchanged old positive is marked strict xfail: `test_inverse_of_older_param_record_uses_only_selected_identity`. Its setup births a clip with both elementRef and an ignored element_ref alias and then immediately PARAMs it without selected history. A normal set-element would clear the ignored alias, destroying the legacy-alias scenario and its original inverse assertion. The original assertions are retained; the failure occurs at the unproven new PARAM setup, before the legacy inverse scenario. Restoring this positive requires a proven alias-preserving ownership/source association or an authentic legacy accepted-history setup. No arbitrary pin, fabricated accepted record, new field or alias-clearing weakened expectation was substituted. This is an OPEN positive gap, not claimed green.

Copies/duplicates and generic whole-row/source replacements do **not** inherit authority by equal JSON. They remain unavailable unless an existing explicit set-element establishes selection; direct tests prove both refusal and subsequent explicit repair. Carrying duplicate source authority automatically remains a positive gap deliberately outside this bounded helper. Unknown structural producer shapes fail closed.

Public S2 forbids an empty values/clear PARAM (`anyOf` requires a write), so empty PARAM is rejected before provider acceptance. The no-authority refusal is tested in native Runtime. Accepted empty PARAM recording is **not qualified** and cannot be added while keeping S2 bytes fixed. This is concrete evidence that the rule handoff's accepted-empty-record expectation needs a later coordinated schema decision; this unit did not deviate from S2.

Runtime port-review ACK is still pending in the shared coordination file. Existing operations have real native test evidence, but this report is not joint approval or integration/release authorization. No new Runtime port/shape was introduced. App authenticated read forwarding, browser draft/inflight preservation and browser restart/outbox behavior were not modified or verified. Ordinary permanent refusal preserves the submitted command and no accepted head change in the native tests; that is not a browser qualification claim.

## Handoff

Bounded provider unit complete with the precise fail-closed gaps above. Recommend independent Agent/Runtime review of this exact tree, then App's existing authenticated same-client capture bridge consuming the selected source. Resolve the legacy-alias positive setup before claiming a fully green compatibility lane; decide accepted-empty support only in a later explicitly authorized schema unit. No full suite, endpoint retirement, new public artifact, shared dependency mutation or push.
