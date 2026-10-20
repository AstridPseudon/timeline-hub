# Current capture coverage

Status: assigned alternative delivered: executable missing Runtime checks.
Agent verifier deletion remains HELD. Executable missing Runtime checks
are in rt-m3-current-capture-pair/tests/test_capture_candidate_actual.py.
No Runtime or Agent product edit has been made.

## Manager action requested

Please provide a central paired-source suite with the reviewed current Agent
source carrying BOTH the verified-source host and the complete saved filmstrip
expansion. Current Agent integration c456b3281497653cecf44f61acd6fa30565d83c8
has the optional projector and canonical-image conversion, but:

- astrid/core/rendering/verified_source.py is absent; GenericPackHost returns a
  plain dict without timeline_source.
- timeline_filmstrip.py::_open_current_input_closure reconstructs a reduced
  expansion and omits graph and outputs. It therefore does not equal the full
  startup-provider projection, even though managed_timeline.py already converts
  the GET envelopes onto canonical images.

Reviewed historical source tl/agt-m3-capture-projection-exact =
d977b59a6a2fc403c57ee76764dd3bd81523045c contains both missing pieces and the
approved canonical-image conversion. Its project_capture AST is IDENTICAL to
current integration (SHA256 ee459dc165f24980786240d35073a130673654f1f078e9cdd4a40908a0b48182).
The manager must choose the reviewed current composition; this worker has not
modified Agent or substituted the historical source for current qualification.

The proposed deletion is tl/agt-m2-capture-single-verifier =
c65619ed47517d3db9f47398bbf04c47f6dcf4ec.
Its project_capture AST differs (b7ce3e5aeb295a00da0425f2c79d5a2b8cbdb9ae7ce03484df1b66e4f443e61a).
Candidate-forward handoff: tl/agt-m3-capture-candidate-forward =
0add597d9ce8e4b5f6061b5b86ee92d761d4c7d7. Our Runtime tests forward the full
preview directly as ordinary task input; they do not qualify SDK invocation.

## Runtime verifier findings

Runtime _candidate_document checks preview kind, both digests, scope, base
identity, capture binding, retained document inputs and publication closure.
It does not compare the candidate's saved basis to the real saved closure or
prove publication derivation. Current Agent project_capture still does both.
There is no claimed present safety gap: the missing checks prevent deleting
the Agent checks, exactly as the orchestrator instructed at 09:26.

The new parameterized test calls the EXISTING Runtime verifier with a real
Runtime revision closure, bypassing only semantic projection so Agent's surviving
checks cannot conceal a missing Runtime check. It creates no alternative
verifier, projector, DTO, receipt or authority marker. All mutations preserve the
test's original expected refusal. Publication-derivation damage recomputes the
candidate digest and capture binding while retaining a different valid
publication, so it does not merely exercise a stale self-hash.

## Exact source tuple

- Runtime product/base: 6023cfb10307b4c0004642b5fa1995d72ba4f6d1.
  Final tests-only tree: 1c25e96821ec1bf00685f1c0932264ee4ab9a3d2.
- The two-file current-pair run used test tree
  8fe038d4ce146643ec43189e207b94dbbc790a38 and service external Agent
  c456b3281497653cecf44f61acd6fa30565d83c8.
- Final 31-case verifier run used final tree 1c25e968 and service external Agent
  ed60bf152b1b468d8d794f2c90ac8a3e1f233691.
- Final alias run used final tree 1c25e968 and service external Agent
  5c3f0c9905d79247f0fa4528c0777908e9ccaa18.
- The service reads Agent integration directly, rather than snapshotting that
  second repository. Agent advanced during this work. The capture provider,
  authoring bundle, filmstrip, managed opener and GenericPackHost sources are
  byte-identical across these three Agent commits (verified with git diff).
  This is bounded capture-source evidence, not a frozen whole-product pair.
- Service external metadata also names App
  18becfbede00038830b97e63345445eeef54fa42 and Composition
  e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab; these tests do not invoke either
  product or a renderer.
- Historical producer tuple remains Runtime
  4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136 / Agent
  321cef4b8c89a4a938cb9ede41ba6a5444cf1b62. Only the admission subprocess uses
  that archived Agent. Reopen now uses current Agent and its actual provider.

SHA256 of relevant source:

| File | SHA256 |
| --- | --- |
| Runtime runtime_protocol/capture_validation.py | d49c52fd534f4a2888d84faf8a07cd3bd32d5a03e76664792ac44b7e3d003f87 |
| Runtime tests/test_capture_candidate_actual.py | 8f1409a171fcb23e7880d7b036246462ce93fe0327f2719971240ae949bff575 |
| Runtime tests/snapshot_legacy_fixture.py | d59bbcc4570f6ecdaa8656afec95e15ca97fe836a655588112418d1b98c6f6f3 |
| Runtime tests/test_snapshot_legacy_certification.py | 50ebf06eb776ab5afa375a90376208fbd924755aa69babb26acfcc5ac8b41de7 |
| Agent astrid/sdk/timeline/commit.py | a52d6c32b005744994721dd3b723e2a9d1c11350528fdf5458912990a2313a67 |
| Agent astrid/sdk/timeline_filmstrip.py | c6e19d6674b68b327f39caac1fb774bc452e283b11e36f01db673f4461e70b57 |
| Agent astrid/packs/rendering/actions/render/managed_timeline.py | fde15d771bf2ad51a74416fbeedc05a7679fdc82659a83232f92d337d5225494 |

## Mapping of deleted Agent checks

All cases below are live Runtime tests in test_capture_candidate_actual.py.
The parameter names refer to
test_runtime_candidate_verifier_covers_removed_agent_checks[PARAM].
PASS means the existing Runtime verifier independently refused the damage;
MISSING means it returned successfully and the refusal assertion failed.
Every case compares all SQLite tables and all CAS/staging files/directories
before/after; no state changes were observed, including on failing cases.

| Deleted Agent check | Runtime case(s) | Result |
| --- | --- | --- |
| preview kind, head and both digests | kind, head, candidate_digest, publication_digest | PASS |
| exact publication supplied with the preview | publication | PASS for stale digest; see derivation below |
| candidate project/timeline and saved base identity | project_id, timeline_id, base_parent | PASS |
| exact base parent payload, with JSON encoded identity | base_parent_payload, json_bool, json_float | MISSING (3) |
| source mapping and source shots must be mappings | source_mapping_shape, source_shots_shape | MISSING (2) |
| base placements mapping, valid row identity and exact saved row | base_placements_shape, base_placements, base_placement_identity, base_placement_payload | MISSING (4) |
| placement source mapping and matching saved placement | placement_sources_shape, source | MISSING (2) |
| authored placements must be a list of mapping rows | placements_shape, placement_shape | MISSING (2) |
| embedded Runtime base must equal the verified closure | embedded_base | MISSING (1) |
| shots mapping and reused shot row shape | shots_shape, shot_shape | MISSING (2) |
| exact reused shot and internal bases | child_base, internal_base | MISSING (2) |
| reused source mapping equals verified saved image | child_source | MISSING (1) |
| reused source digest corruption affecting compiled retained pins | retained_pin, reused_pin | PASS through closure validation |
| frozen candidate may not change after its digest | candidate_after_freeze | PASS |
| publication must derive from the candidate even with recomputed hashes/binding | publication_derivation | MISSING (1) |
| real candidate absent | test_working_copy_without_candidate_is_admitted_uncertified | Intentional CAS-only preview, not certification; capture_snapshot inline/ref PASS, other aliases FAIL |

Result: **20 missing checks / 11 passing independent Runtime refusal cases**.
The new malformed-shape cases update the candidate digest, retaining an otherwise
valid publication, so they cannot pass by triggering only a stale digest.
The JSON cases change a saved opaque integer zero to false or 0.0.
These are tests requiring refusal, not probes asserting that a defect is success.

Current Agent safety control:
test_current_agent_still_refuses_unrelated_candidate_publication[ref/inline]
both PASS via public create_task with a self-consistent forged candidate hash,
binding and snapshot identity. The still-present Agent verifier refuses and all
SQL/CAS/staging state remains unchanged. Removing that verifier now is unsafe.

## Genuine captures, original forgery matrix and legacy preservation

- Existing four candidate-to-host positives remain RED at the import of the
  absent verified_source module. They are not counted as certified positives.
- Existing explicit native-CAS-to-host positive remains RED because current
  GenericPackHost returns dict without timeline_source.
- Added saved/native inline/ref positives compare the COMPLETE saved expansion
  before admission. All four currently fail because the SDK drops graph/outputs.
  There is no ignore list or replacement of the producer's saved snapshot.
- All six original working-copy config/registry/shot-digest forgeries PASS
  refusal before any SQL/CAS/staging write.
- Added the matching six original saved config/registry/shot-digest forgeries
  using current real SDK production. All six stop at the saved expansion parity
  prerequisite. Their refusal is UNQUALIFIED; the frozen-provider 25-pass lane
  below does not replace this missing real saved proof.
- Existing four forged working-copy certificate cases PASS, with and without
  candidate, inline/ref. The new unrelated-publication public cases also PASS.
- Candidate-less capture_snapshot inline/ref still dispatch as exact CAS-only
  references. The added input_snapshot and filmstrip_snapshot inline/ref cases
  all FAIL: they retain working_copy revision authority. This confirms F3 in
  design/runtime-review-writepaths.md using the live Agent-generated candidate.
  No Runtime product fix was attempted.
- Legacy admission remains archived and byte-exact; current Runtime/current
  Agent reopen now registers the actual startup provider. All 20 legacy
  certification/retry nodes ERROR at the missing timeline_source host boundary.
  The helper checks the original stored task spec and captured timeline bytes
  before that failure. Final CAS preservation, exact retry and certification
  assertions are therefore UNQUALIFIED. No original snapshot is rewritten or
  silently recertified. Existing two dynamic strict xfails remain unchanged and
  are not reached by this current-pair run; no new xfail/skip was added.

## Exact commands and results

ORCH below is
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch.
Every service result has log.txt, summary, snap and ext under ORCH/tests/ID.

```bash
"$ORCH/bin/request-test" rt-m3-current-capture-pair capture-legacy-integration --files "tests/test_capture_candidate_actual.py tests/test_snapshot_legacy_certification.py"
"$ORCH/bin/wait-test" rt-m3-current-capture-pair-capture-legacy-integration-1020093215-643
```

**24 failed, 25 passed, 20 errors in 42.47s; exit 1.**
Of the failures, 15 are the missing saved/host prerequisites above; nine are the
initial value/derivation Runtime gap corpus. No fixture error remains in that
20-case verifier corpus. The subsequent final corpus adds eleven shape/source
cases and is fully enumerated above.

```bash
"$ORCH/bin/request-test" rt-m3-current-capture-pair capture-legacy-integration --files "tests/test_capture_candidate_actual.py::test_runtime_candidate_verifier_covers_removed_agent_checks"
"$ORCH/bin/wait-test" rt-m3-current-capture-pair-capture-legacy-integration-1020093532-2012
```

**20 failed, 11 passed in 9.15s; exit 1**, final tree 1c25e968.
Every failure is DID NOT RAISE; no setup error, xfail or skip.

```bash
"$ORCH/bin/request-test" rt-m3-current-capture-pair capture-legacy-integration --files "tests/test_capture_candidate_actual.py::test_working_copy_without_candidate_is_admitted_uncertified"
"$ORCH/bin/wait-test" rt-m3-current-capture-pair-capture-legacy-integration-1020093623-3154
```

**4 failed, 2 passed in 2.11s; exit 1**, final tree 1c25e968.
Failures are the two non-capture aliases in inline/ref form retaining working_copy.

The underlying command for each capture-legacy-integration request is:

```bash
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration <exact files/node IDs above>
```

```bash
"$ORCH/bin/request-test" rt-m3-current-capture-pair targeted --files "tests/test_snapshot_authority_refusal.py"
"$ORCH/bin/wait-test" rt-m3-current-capture-pair-targeted-1020093216-24781
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_snapshot_authority_refusal.py
```

**25 passed in 5.57s; exit 0**, final tree 1c25e968. This is explicitly the
existing frozen-provider Runtime seam lane, not live saved/candidate certification.

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache tests/test_capture_candidate_actual.py tests/test_snapshot_legacy_certification.py tests/snapshot_legacy_fixture.py
git diff --check
```

Both PASS. No full suite, browser, socket server, install, shared-cache mutation,
git mutation or product edit.

Initial diagnostic 1020092916-7547: **24 failed / 43 passed / 25 deselected /
2 existing xfailed**, exit 1, 44.39s. Its --files also named
tests/test_snapshot_authority_refusal.py (all 25 deselected by -m integration).
Two new JSON fixture paths were corrected afterward. That run still reopened
legacy realms using archived Agent, so its 18 legacy passes and two xfails are
NOT current-pair evidence and are superseded by the genuine current reopen run.

## Handoff

The requested alternative is complete: permanent executable missing checks,
with actual current-pair failures and an explicit mapping. Keep the red refusal
tests unchanged and land them with the separately owned Runtime verifier fix;
this branch is not a green merge candidate. The manager's next Runtime unit
must preserve one verifier and reuse existing pure candidate construction,
per the 09:26 instruction. Agent must retain its verifier until this corpus
passes and the reviewed current source pair proves genuine saved/candidate/native
positives plus all twelve original forgery negatives. Also fix F3 across every
recognized capture carrier before claiming CAS-only fallback preserved.
