# Independent Runtime capture authority review

Reviewer: `rt-m3-review-capture-authority`, 2026-10-20.
Assigned result is complete; neither held unit is qualified for the complete requested authority contract.

| Unit, relative to `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` | Verdict | Reason |
| --- | --- | --- |
| Alias fix `eff006404fc098e815e9ffe67c3998afb9408ffb`, tree `d9df917cc3c2a4c716eb64d82099c7dffb46dc04` | **REJECT** | Correct for nested authority contexts, including three aliases, independent digests and JSON/list duplicates. Misses the supported outer legacy authority context, so forged existing admissions retain revision claims at public claim. |
| Candidate binding `c10bad52ca524e779c54876489d2c12f857f2e13`, tree `ec1bb16c1bb3c512f2aafcbe4ddfd64bfc0bd312` | **REJECT** | Derivation comparison is sound in shape, but comparisons do not cover all embedded base/source entries. Extra, removed and renamed identities pass. Public admission writes task state and, for inline inputs, CAS/staging. Production provider/host/full-saved qualification also remains open. |

These are completion verdicts against the assigned requirements. The missed legacy layout and candidate comparison holes also exist in the baseline; this report does **not** attribute their introduction to these commits. No settled projector/provider decision needs changing. No merge is requested and Agent's surviving verifier must remain.

## Scope and provenance

Read PLAN, COMMON, Runtime manager STATUS (09:42), `design/runtime-capture-current-coverage.md`, coordination seam proposal, both complete diffs and adjacent admission/claim/materialization code. Both commits have exactly `6023cfb` as parent. Review worktree HEAD was `642eef7467a6b766480df3f34e7377e8d755fe92`; no repository file was edited.

Held capture-validation SHA256:

- Alias: `7f6589d70c53d22be041bbac561c594b527c0f1b2a7879558713d871b24ba38e`.
- Binding: `cff74ed6d28f04eb9fcbe955a1c27d32573b980e49e43704633fee350e974fa5`.

Private probes used a read-only git archive of binding Runtime and a **fixed archive** of Agent `efb96034fc7c80a6e73900bfc57dac53260beb3c`. Alias claim function was loaded from its exact git-show source into a private module. For candidate probes only, a private fixture attached the approved method shape to the copied Agent class:

```python
capture_candidate_inputs(document, *, candidate) -> {
    "base": bundle_from_document(deepcopy(document)),
    "preview": preview_authoring_candidate(deepcopy(candidate)),
}
```

It invokes the existing real pure constructors; it supplies no verifier or projector implementation. This is explicitly a **contract prototype**, not an installed Agent method, reviewed production pair, SDK forwarding qualification, or host qualification. All surrounding SDK compilation/projection and Runtime admission/state comparison were real. No sockets, browsers, renderer, broad/full suite, service request, dependency install or shared cache writes were used.

## Alias unit: precise blocker and retained behavior

**A1: supported outer legacy context is never visited.** At `eff0064:runtime_protocol/capture_validation.py:124-126`, claim relabeling reads only `spec["spec"]["authority_context"]`. With a stored shape such as:

```json
{"authority_context":{"input_snapshot_ref":{"source_kind":"revision","digest":"sha256:..."}},
 "spec":{"inputs":{"filmstrip_authority":"{...same reference...}"}}}
```

the label map is empty and line 147 returns the original spec. This is a supported location, not a newly invented wire format:

- `runtime_protocol/snapshot_refs.py:194-196` falls back to outer context when rewriting inline carriers.
- `runtime_protocol/store.py:520-525` falls back to outer context when validating capture refs.
- `astrid/core/execution/generic_host.py:6669-6685` explicitly supports the outer Runtime context and hydrates each alias.
- `runtime_protocol/store.py:268-280` preserves that outer context in the public task spec.
- `runtime_protocol/service.py:6506-6508` passes that public spec directly through `claim_capture_view`.

Three pure negative probes and three additional real RealmStore-to-`RuntimeService.claim_next` negative probes failed, one per alias. The real probes simulated a pre-validator admission through the existing store API with a forged config, valid CAS/ref digest and valid saved revision. They did **not** bypass a new public admission guard. The public claim retained `source_kind: revision`; the persisted stored spec remained byte-equivalent to its pre-claim value. This establishes the missing claim downgrade for existing admissions without asserting that current public `create_task` admits those saved forgeries.

Required correction: apply the same supported context selection at claim that admission/materialization already use, and add a permanent outer-context legacy regression for every alias. If both supported locations are present, define and test which one is consumed; neither active claim may silently escape validation. Keep stored specs/history and every original snapshot byte unchanged.

**What is correct in the held patch:** lines 128-144 independently verify all `SNAPSHOT_KEYS`: filmstrip, input and capture. `source_kind_of` covers legacy refs with inferred revision kind. Replacements key on `(carrier name, that carrier's digest)`, removing revision and working-copy bindings only from failed claims. Lines 149-170 rebuild dictionaries/lists and JSON-encoded dictionary/list arguments, including nested argv-like JSON. Successful carriers survive independently of failed siblings; each failed carrier keeps its own digest. Four reviewer pure mixed/implicit-kind probes pass, with differing digests and copies in both filmstrip JSON and a JSON list argument. The input spec stays unchanged.

The added 12-case committed test covers inline/ref and single/multiple nested carriers and checks stored spec plus exact retry. Existing admission rewrites inline snapshots to refs, so the claim function need not rewrite their CAS payloads. No new task/history/CAS publication occurs in the alias diff. The independent label map does not substitute the first snapshot for another carrier.

## Binding unit: incomplete retained-base validation

**B1: loops compare subsets, permitting unretained source/base claims.** At `c10bad5:runtime_protocol/capture_validation.py`:

- Lines 50-54 check every supplied base-placement row's identity and require baseline rows to survive, but accept additional unretained base rows.
- Lines 55-59 check placement source only for **currently authored** placements whose identities are in the saved baseline. Deleted occurrences and sources for new identities are unchecked.
- Lines 62-68 check shot base payloads/internal payloads/source only for candidate keys that also occur in `baseline["shots"]`. A renamed authoring identity with an existing source mapping bypasses all three checks. Removed/unused source-shot entries are also unchecked.
- Lines 69-70 prove that publication derives from the supplied candidate. That does not prove that candidate's unchecked source/base fields came from retained history.

The copied current Agent `RuntimeCommitService.project_capture` has the same membership gates (`astrid/sdk/timeline/commit.py:667-691`). Its surviving verifier does **not** rescue these cases. The pure compiler validates complete authored shapes but deliberately trusts its supplied base/source mappings (`astrid/core/timeline/authoring_bundle.py:805-819,845-886,913-953,1002-1020`); compilation is not a retained-history check.

Reviewer counterexamples, all with fresh candidate/publication/snapshot digests:

| Case | Mutation | Observed result |
| --- | --- | --- |
| `extra_base_placement` | Add `{occurrence_id: "unretained", forged: true}` under a new base-placement key. | Accepted through public `create_task`, inline and ref. |
| `unused_placement_source` | Add an unretained entry to `source_mapping.placements`. | Accepted, inline and ref. |
| `unused_shot_source` | Add an unretained entry to `source_mapping.shots`. | Accepted, inline and ref. |
| `removed_placement_source` | Delete the authored placement but forge its retained source-placement row. | Accepted, inline and ref, with a real newly produced matching capture. |
| `removed_shot_source` | Delete authored placements/shots, retaining a source-shot row with false content digest. | Accepted, inline and ref, matching real capture. |
| `renamed_shot_base` | Rename the candidate authoring shot and corresponding placement/source-map key, leaving the existing source identity; forge its base shot and base internal payloads. | Accepted, inline and ref, matching real capture. |
| `renamed_shot_source` | Same rename, but falsify the source shot content digest. | Accepted, inline and ref, matching real capture. |
| `new_placement_source` | Add a new occurrence plus an invented source-placement row for it. | Accepted, inline and ref, matching real capture. |

For the final five cases the reviewer generated the capture via real `prepare_filmstrip(...authoring_preview=preview)` **after** mutation, rather than letting a stale rendered snapshot cause an unrelated projection refusal. All ten public negatives report `admission refusal=NONE`. Inline cases changed `objects`, `project_objects`, task/run/idempotency/event/sequence rows, a new CAS file and a publication staging journal. Ref cases, whose ingest is in the baseline, changed task/run/idempotency/event/sequence rows. Each ref probe also directly invoked the held `_candidate_document` against the actual retained closure; all returned successfully. No Agent check or fake projector masked these misses.

The first diagnostic run used the existing test helper's `_rebind` approach for all eight cases. Its first three cases already demonstrated six public acceptance failures. Its other ten cases refused due to a stale snapshot after genuine draft structural changes; those are **not** counted as retained-base safety passes. The corrected, narrowly selected ten-case run regenerated the whole capture and exposed all ten missing refusals.

This proves false embedded base/source provenance is accepted and admission writes happen. It does not prove overwriting saved revisions, arbitrary cross-project media access, or a rendered difference for an unused source entry. Those stronger claims are not made.

Required correction: compare every embedded saved-source/base claim with the retained base, including removed entries and alias/renamed authoring identities. Resolve source claims by the actual retained source identity, not solely by candidate dictionary membership. Reject invented base/source rows; preserve legitimate new draft shots/occurrences and supported clone/edit behavior. Add these negatives together with matching genuine new/renamed/deleted draft positives, so the fix cannot succeed by refusing all such drafts. Keep one projector and the existing pure compiler.

**What is correct in the held patch:**

- Optional method lookup at lines 40-42 fails certification closed; the agreed pure seam shape is already approved and is not challenged here.
- Line 44 detaches both inputs and the returned result. There is no direct Agent import, new compiler/projector, endpoint, DTO, persistence table, I/O or save call in the diff.
- Lines 46-47 compare scope, base revision and parent base payload with JSON identity, distinguishing false/0/0.0. Existing base child/source and runtime-document checks are exact for the identities they visit.
- Lines 69-70 compare the entire derived publication and its hashes/head/kind. Refreshing self-hashes alone cannot conceal an unrelated publication when this method exists.
- Lines 71-86 retain document-pin equality and immutable closure checks; `_validate_closure` does not publish the candidate. `revision_closure` opens the retained revision and verifies its dependencies rather than choosing latest head.
- `store.py:2454-2473` collects inline publications and all carrier validation before the admission transaction and actual `_publish_spec_snapshot` calls at lines 2541/2731. The ordering is right; missed comparisons let the counterexamples pass that boundary.

The committed new negative tests correctly replace `project_capture` with an assertion trap after genuine setup, recompute caller hashes, and compare all SQL/CAS/staging state. They test only existing retained identities, so they do not expose B1. Their detached-input control also checks the saved closure is unchanged. These tests should remain, supplemented by the missing cases; no passing behavior expectation should be rewritten to refusal.

## Existing results reused, with their limits

No central job was submitted by this reviewer. The following completed results were inspected and matched to exact held trees, replacing the worker reports' earlier "queued" wording.

1. Alias exact-tree central request `rt-m3-capture-alias-uncertified-targeted-1020093810-15310`, command:

   ```bash
   /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_snapshot_authority_refusal.py tests/test_snapshot_preflight.py tests/test_capture_candidate_actual.py
   ```

   **41 passed, 29 deselected, 26.82s, exit 0.** The cached repeat `1020094148-25645` is the same result, not another qualification. The 29 marked candidate cases, including the 12 new alias nodes, were deselected. The included frozen-provider saved/native controls, original saved forgery refusals, scope/duplicate mismatch checks and later-carrier preflight refusals are useful Runtime seam evidence, not actual current Agent host evidence.

2. Alias worker's recorded narrow marked command (reviewed log, not independently re-run):

   ```bash
   ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/packages/python" /home/user/work/venv-runtime/bin/python -m pytest -q -m integration tests/test_capture_candidate_actual.py -k all_capture_aliases
   ```

   **12 passed, 17 deselected, 10.38s.** This qualifies nested inline/ref, single/multiple candidate-less claim labels only. The external Agent checkout was not frozen by that invocation.

3. Binding exact-tree central request `rt-m3-candidate-binding-authority-capture-legacy-integration-1020093841-11587`, command:

   ```bash
   env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_capture_candidate_binding.py tests/test_capture_candidate_actual.py tests/test_snapshot_authority_refusal.py tests/test_snapshot_legacy_certification.py
   ```

   **25 failed, 32 passed, 25 deselected, 2 existing xfailed, 74.16s, exit 1.** Twenty new binding nodes fail because the actual provider lacks the method (including two tests that try to remove an absent class method). Four candidate host positives fail importing `verified_source`; native host positive receives dict without `timeline_source`. The 25 frozen-provider saved/refusal nodes are deselected, not passed. The original working-copy negative passes can be caused by missing-provider refusal and therefore do not prove semantic comparison with a capable provider.

   `ext` records Agent moving from `5c3f0c9905d79247f0fa4528c0777908e9ccaa18` to `efb96034fc7c80a6e73900bfc57dac53260beb3c` during the run, App `18becfbede00038830b97e63345445eeef54fa42`, Composition `e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab`. This is **not** a frozen whole-product pair. The legacy helper in this held test tree reopens with archived Agent and no registered current projector, so its 18 legacy passes/two xfails do not establish current-pair legacy certification. The later tests-only coverage unit correctly identifies that limitation.

The binding worker's 22 prototype passes and original-verifier negative control support the new checks' purpose but do not qualify the actual Agent method or host. This reviewer did not repeat that suite or the prior coverage unit's 31-node corpus. The original 31-node corpus remains a precise required check list after its call is adapted to the new provider argument, preserving refusal expectations. It must not be merged as known-red tests without a fix.

## Reviewer commands and results

Artifacts are under `$W = $ORCH/workers/rt-m3-review-capture-authority`, where `$ORCH` is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.

Sources were prepared using read-only `git archive c10bad52...` in this Runtime repo and `git -C /home/user/work/agent archive efb96034... astrid astrid_runtime_client schemas config runtime.lock.json pyproject.toml`; alias function by `git show eff0064:runtime_protocol/capture_validation.py`. `prepare_review_sources.py` preserves the exact reconstruction commands. Heavy copied archives and private realm/temp directories were removed after the probes.

All successful collection runs used this environment, from `$W`:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=$PWD/runtime-copy:$PWD/runtime-copy/tests:$PWD/agent-copy \
  ASTRID_CHECKOUT=$PWD/agent-copy \
  /home/user/work/venv-agent/bin/python -m pytest ...
```

Exact argument tails and outcomes:

```bash
-q -s -p no:cacheprovider --confcutdir=. --basetemp=private-tmp test_review_binding.py test_review_alias.py
# review-probes.log: 9 failed, 14 passed, 4 warnings, 13.38s; exit 1.

-q -s -p no:cacheprovider --confcutdir=. --basetemp=private-tmp test_review_binding.py -k 'removed or renamed or new_placement'
# review-semantic-probes.log: 10 failed, 6 deselected, 4 warnings, 9.51s; exit 1.

-q -p no:cacheprovider --confcutdir=. --basetemp=private-tmp test_review_alias.py -k real_legacy
# review-legacy-claim-probes.log: 3 failed, 7 deselected, 2 warnings, 3.37s; exit 1.
```

Failures are preserved negative expectations exposing the defects above. Private pytest runs register no repo lane plugin; their harmless warnings are imported modules' unknown `integration` marks. No tests were disabled. Initial collection before adding `$PWD/agent-copy` to PYTHONPATH failed once with missing `astrid_runtime_client`; it executed no probes and is not product evidence. The first probe version used `_rebind`; the final saved probe regenerates full captures, as explained above.

Read-only verification: `git diff 6023cfb <each-held-SHA> -- <changed-files>` and `git show <SHA>:<file>` inspected both complete changes; `git rev-parse <SHA>^{tree}` matched cached tree IDs; `git diff --check` passed; `git status --porcelain` was empty. No git mutation or integration/other-worktree edits occurred.

## Required real-current-pair qualification

Keep existing Agent checks until all of these are on one pinned reviewed Agent source and the corrected Runtime source. Optional pure provider, verified-source host and full saved expansion are still **pending**, not green because of the private prototype or archived legacy positives.

1. Agent implements the approved pure `capture_candidate_inputs` with defensive copies, existing constructors only, and no reads/writes/save/render dependency. Freeze exact Runtime and Agent source SHAs for the entire run; the service's live `/home/user/work/agent` path must not drift underneath qualification.
2. Run the existing 31 independent verifier cases with the new provider argument, plus all eight cases above. For public negatives, replace `project_capture` with an assertion trap only **after** producing valid setup, so its surviving Agent checks cannot hide missed Runtime checks. Recompute candidate/publication/binding/snapshot hashes. Require unchanged complete SQLite tables, CAS bytes and staging paths before/after `create_task`, including valid first carrier + invalid later carrier and all three aliases, inline/ref. Add JSON false/zero/float base identity cases to the public lane, not just internal helper calls.
3. Prove original **12** semantic negatives (config, registry, shot digest; saved and working-copy; inline/ref) with the real capable provider, matching full SDK snapshots, and state equality. A missing optional method is not the passing reason. Preserve the four original certificate negatives and duplicate scope/digest/ref/ref-inline mismatch tests.
4. Prove real parent-edit and child-edit candidate positives inline/ref from SDK/CLI producer through public create_task, claim, host materialization and verified-source consumption. Assert unchanged forwarded whole `authoring_preview.candidate`, exact per-carrier CAS bytes, working-copy authority and base revision, no save/publication of canonical revisions. Add genuine new/renamed/removed occurrence/shot controls beside the new negative cases. Mutate provider input objects in a detachment test and show caller preview/retained document do not change.
5. Prove saved/native inline/ref positives using real saved `prepare_filmstrip`, with **complete** projection equality including graph and outputs, not a reconstructed reduced expansion or ignore list. Saved capture stays certified even after a newer head; explicit CAS never acquires a verified source, including leftover metadata. With the optional candidate method absent, saved certification still works and candidate-less/explicit-CAS previews remain exact UNCERTIFIED.
6. Prove candidate-less claims across all three aliases, inline/ref, single/multi/mixed certified/uncertified carriers with differing digests; nested JSON/list argument duplicates and both supported authority-context layouts. Exact retries and task reads retain original stored admission bytes; claiming changes only the worker view.
7. Reopen actual historical admissions with the **reviewed current provider and current host**, testing genuine saved certification, native CAS, forged config/registry/expansion downgrade and exact retry. Assert immutable original task spec, saved closure/history, snapshot/CAS bytes before and after upgrade/claim. Do not count archived-Agent reopen or strict xfail as a genuine certified positive.

Suggested central lanes, once the corrected code/tests and reviewed pair exist, are the existing targeted `test_snapshot_authority_refusal.py test_snapshot_preflight.py` lane and `capture-legacy-integration --files "tests/test_capture_candidate_binding.py tests/test_capture_candidate_actual.py tests/test_snapshot_legacy_certification.py"`. The tests-only missing-coverage cases should land with their fixes. No full suite is requested by this review.

The assigned review itself is complete and unblocked. External Agent dependencies and both concrete fixes block acceptance of the held capture units, not completion of this report.
