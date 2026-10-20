# Runtime M2 write/safety review

Reviewed `4bb1d0f7..6023cfb10307b4c0004642b5fa1995d72ba4f6d1` (`tl/integration` when reviewed), tree `bb2d3b6235cc7bf819373d2078d7437360c322d4`. Read PLAN.md first. Scope: the requested publication, acceptance/projection, producer, verified-input, render-admission, and capture-safety paths. No repository changes.

## Ranked findings

### F1 — P1: restored legacy publication can overwrite another timeline's shot projection

**Location:** `runtime_protocol/service.py:3043`, calling `_apply_published_shot_projection` at `service.py:1518–1533`; the same-project-only identity check is at `service.py:2832–2834`.

**Scenario, reproduced:** Project P has a tracked timeline `owner`, whose accepted closure contains `shot-1` / `owned-shot`. Its live shot has name `KEEP OWNER NAME`, item `keep-owner-item`, and shot head `owned-shot`. Create a separate, empty, untracked timeline `main` in P. Call the restored `publish_parent_composition(P, "main", ...)` with `expected_head=None`, a fresh shot revision `shot-rev-1` for **the same `shot-1`**, empty items, and its own parent occurrence. The call succeeds. The existing owner's name changes to `shot-1`, `keep-owner-item` is deleted, and the global shot head becomes `shot-rev-1`. The `owner` timeline head remains unchanged. Thus an initial publication for an unrelated timeline clobbers mutable rows belonging to an accepted film. The old immutable shot revision remains available; this finding does not claim immutable-history deletion.

**Cause:** The restored route checks project membership, immutable revision identities, and its own parent head, but never proves authority over an existing mutable shot destination. A new revision enters `_apply_published_shot_projection`, which updates the existing shot and deletes all its items. The normal commit path has `_check_shot_destinations`; this route does not invoke an equivalent guard. All this happens atomically, so this is an authorization/occupancy omission, not a TOCTOU race.

**Existing tests:** `git grep` found `tests/test_timeline_projection_occupancy.py:114` (`test_occupied_destination_refuses_before_any_write`), `:146` (competing acceptors), and `:275` (external source read). They test `TimelineCommitStore.accept` / the command path, not legacy publication. `tests/test_timeline_legacy_authority.py:171` covers refusal on a tracked **target** timeline; the target in this reproduction is a fresh untracked timeline. No regression found covering this restored-route collision. Relevant existing suites passed despite the reproduction.

**Recommended action:** Keep the route available as PLAN.md requires, but add a preflight proving ownership of every mutable shot destination before any projection writes. Refuse unrelated same-project occupants as well as foreign ones. Cover the tracked-owner/untracked-target combination, archived occupants, and preservation of items, heads, receipts, and events on refusal.

### F2 — P1: empty-shell adoption ignores authored content in the legacy timeline document

**Location:** `runtime_protocol/timeline_commit_store.py:896–900`, using `timeline_scope_is_empty` at `:47–62`.

**Scenario, reproduced:** Start with the exact empty unpublished shell used by `tests/test_timeline_empty_shell_repair.py::_shell`: an empty parent revision, authentic publication event/receipt, and a parent head whose `publication_id` is NULL. Also retain `project_documents[id="timeline:main", project_id=P]` containing an authored clip `unsaved` at 7 seconds. Register the provider before installing this historical shell image, as in the existing repair fixture. A same-ID `create_timeline(P, "main", idempotency_key="adopt")` succeeds and installs a publication/head/history edge for the **empty** canonical document. Reading the editable revision closure returns no clips. The non-empty legacy document row still exists, but its authored clip has not entered accepted history and is excluded from subsequent command editing.

**Cause:** The shared emptiness predicate checks relational timeline rows, snapshot rows, and occurrence/dependency rows, but never checks `project_documents`. `bootstrap_install_plan` verifies the empty parent publication, not the separate retained legacy document. By contrast, `publish_parent_composition` explicitly checks that document at `service.py:2772–2775`. Adoption therefore bypasses the hidden-content safeguard and blesses an empty canonical baseline over authored legacy state. No physical deletion of the legacy document is claimed.

**Existing tests:** `git grep` found the hidden-document safeguard test at `tests/test_timeline_headless_overwrite_refused.py:114`, which exercises publication, not adoption. `tests/test_timeline_empty_shell_repair.py:153` changes the **parent payload**, and `:171` exercises scoped rows; neither installs non-empty `project_documents` content. Both files passed in the central run. No adoption regression found for this case.

**Recommended action:** Make adoption's emptiness check include the same authored legacy-document test before installing any head/history/create receipt. Preserve a whole-state refusal regression for the empty-parent-plus-nonempty-document image.

### F3 — P2: uncertified working-copy aliases retain revision authority in a worker claim

**Location:** `runtime_protocol/capture_validation.py:126–128` and `:140`; admission's uncertified result is at `:75–82`.

**Scenario, reproduced through admission and claim:** Submit `rendering.timeline_visualize` with `authority_context.input_snapshot` rather than `capture_snapshot`. The snapshot references a real saved base but has a self-consistent working-copy marker with fabricated candidate/publication digests and candidate revision `draft-forged`; change a projected clip's hold to 99. Forward **no** `authoring_preview.candidate`. Admission is allowed, as intended for uncertified previews: `validate_capture(...)` returns False. Claim the task through `claim_next`. The returned `authority_context.input_snapshot_ref`, and its `filmstrip_authority` copy, still carry `source_kind="working_copy"`, `revision_id="draft-forged"`, and the fabricated revision digest. They are not reduced to CAS-only provenance.

**Cause:** Admission validates all three recognized aliases (`store.py:523–525`), but ignores the validator's boolean result (`store.py:2471–2473`). The dispatch-time fallback only inspects and relabels the literal `capture_snapshot_ref` key, so a supported `input_snapshot_ref` or `filmstrip_snapshot_ref` bypasses it. This violates the settled requirement that candidate-less previews be CAS-only and labelled uncertified. The reproduced impact is incorrect authority in the worker claim; final rendered output/certification was not tested.

**Existing tests:** `git grep` found `tests/test_capture_candidate_actual.py:246`, which checks candidate-less uncertified dispatch using only `capture_snapshot`; it does not parameterize aliases and is integration-marked (deselected in the central targeted run). `tests/test_snapshot_preflight.py:75` covers native aliases, and `:120` covers forged alias content with revision certification, but neither covers the candidate-less working-copy alias fallback. No regression found for the reproduced claim.

**Recommended action:** Apply dispatch certification/relabeling independently to all recognized capture carriers and their duplicate references, retaining each alias's exact digest. Parameterize the candidate-less working-copy test across all three carriers, inline/ref forms, and combinations of carriers.

## Checked and clean

These are bounded review conclusions, not a claim of exhaustive qualification; the exceptions above remain open.

- **Normal commit transaction and exact retry:** `accept` resolves its persisted receipt before current-head, occupancy, input, and producer-consumption checks. Closure persistence, acceptance receipt/history/head, text-binding projection, document links, and producer checkpoint share the outer `BEGIN IMMEDIATE` transaction and store mutex. Refusal after publication/projection rolls back those database changes.
- **Normal commit destination guards:** unrelated same-project and foreign shot destinations are refused before persistence. Exact immutable reuse avoids mutable projection writes; inverse/history proofs use authenticated publication records. No additional bypass substantiated in the command path.
- **Headless legacy publication guards:** receipt replay precedes current-state checks; a NULL current head cannot publish over hidden authored legacy-document content or the scoped rows covered by `timeline_scope_is_empty`. The missing adoption check is F2.
- **Text selection and binding projection:** exact object/digest/size/MIME and managed-project membership, CAS hash verification, UTF-8 validation, declared selection, acceptance revalidation, shot ownership/before-state checks, and transactional event persistence were traced. The one strict xfail retains the required clear behavior and explicitly names the missing removal/tombstone support; it is not an inverted passing-behavior assertion. Text-binding clear/undo remains an acknowledged unimplemented requirement, not a green behavior claim.
- **Producer attempt and consumption:** exact proposal bytes/digest, commands/rationale, admitted target, current completed settled attempt, fence/epoch/executor, managed-output association/provenance, and continuation child identity are checked. Acceptance re-captures authority under the lock/transaction. Consumption is per task, including later attempts or different actors/keys. Exact accepted retries precede live guard checks. No additional guard bypass substantiated.
- **Producer render handoff:** the checkpoint binds the accepted receipt/revision/digest and normalized pending intent; altered reserved-key admission is rejected before freezing. Linking a render task/run/receipt and completing the checkpoint occur in the render admission transaction. No partial database handoff found.
- **Historical render and replay:** the five-field selector is scoped to project/timeline and publication, accepted immutable closures/media/retained inputs are checked, Runtime-owned snapshot overrides are refused, and initial historical publication waits until admission checks pass. Persisted frozen authority supports exact retries after head changes. No additional overwrite/replay defect substantiated.
- **Verified media and retained-document/object reads:** project authorization precedes read execution; source/retained pin and object custody checks remain project scoped and read-only. No foreign-project data disclosure substantiated in these changed helpers.
- **Capture admission:** scope, CAS bytes, saved projection, expansion, retained inputs, working-copy bindings, and duplicate snapshot references are checked before snapshot publication. Canonical `capture_snapshot_ref` falls back to CAS-only when it cannot certify at claim. The alias exception is F3. Real Agent candidate integration was not executed by the targeted service configuration.

## Verification

All three findings are confirmed by a disposable-realm probe retained outside the repositories:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime:/home/user/work/runtime/tests:/home/user/work/runtime/packages/python /home/user/work/venv-runtime/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-review-writepaths/probe_writepaths.py
```

Exit **0**; printed `CONFIRMED F1`, `CONFIRMED F2`, and `CONFIRMED F3`. Assertions deliberately confirm observed defects; this file is review evidence, not a replacement for behavior tests in the main suite. Temporary realms are removed automatically. No sockets/browser/renderer was used. F1 uses the main suite's host-acceptance helpers to establish ownership; F2 uses its historical-shell fixture and a retained legacy document row; F3 uses its frozen trusted-projection fixture, then real service admission and claim.

Central targeted request and wait:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
"$ORCH/bin/request-test" integration:runtime targeted --files "tests/test_timeline_projection_occupancy.py tests/test_timeline_headless_overwrite_refused.py tests/test_timeline_empty_shell_repair.py tests/test_timeline_text_selection.py tests/test_timeline_producer_guards.py tests/test_timeline_producer_checkpoint.py tests/test_render_historical_admission.py tests/test_render_admission_exact_retry.py tests/test_snapshot_authority_refusal.py tests/test_capture_candidate_actual.py"
"$ORCH/bin/wait-test" runtime-targeted-1020092539-6585
```

Underlying exact command:

```bash
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_projection_occupancy.py tests/test_timeline_headless_overwrite_refused.py tests/test_timeline_empty_shell_repair.py tests/test_timeline_text_selection.py tests/test_timeline_producer_guards.py tests/test_timeline_producer_checkpoint.py tests/test_render_historical_admission.py tests/test_render_admission_exact_retry.py tests/test_snapshot_authority_refusal.py tests/test_capture_candidate_actual.py
```

Result: **187 passed, 64 deselected, 1 xfailed in 34.16s**, service exit **0**, on the reviewed tree `bb2d3b6235cc7bf819373d2078d7437360c322d4`. The xfail is `test_clear_removes_the_live_binding`. Log: `orch/tests/runtime-targeted-1020092539-6585/log.txt`. The 64 deselections include integration-marked tests; no Agent-paired candidate qualification is claimed. No full suite requested or run. No macOS, browser journey, or final renderer qualification performed.

Decisions: preserve all settled design choices, including temporary route availability; report defects without fixes or route retirement. No blocked work. Recommended next step: assign fixes and permanent regressions for F1/F2 before accepting further safety qualification, and extend capture alias coverage for F3.
