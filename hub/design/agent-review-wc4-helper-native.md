# WC4 helper final owner review

**HOLD whole-writer deletion / WC4 closure.** One original helper compatibility regression is reproduced. The portable-admission native helper and its retry machinery otherwise pass the inspected targeted scope. This is a completed read-only review, not a blocked review task. No fixes, integration changes, Git mutation, schema/pin edits or ledger deletion were made.

Reviewed `tl/agt-m2-wc4-helper-native-finish` at **a6098b5ddd1f3621e4467343875f705aab6c339e**, its authored delta from **905a4f0f**, original whole-parent helper, approved `98c38a7c` source, prior review and worker reports, PLAN and repository AGENTS. Review worktree HEAD is d8749a9c; tests deliberately use an exact private archive of a6098b5d, not that different worktree tree. Runtime tests select the immutable normal **2c4ac180c2220bdad966bc01e95ad230e99ce26a / contract 0.2.13** using `use_runtime(commit=vendored_runtime_commit())`; `/home/user/work/runtime` is only the Git locator. Agent command-schema SHA256 is `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

## Finding requiring the hold

**P1 — preserve the original digest-only admission success before deleting its writer.** Candidate `astrid/sdk/timeline_elements.py:171–174` requires `snapshot_object` for every update, including an element-only/hold update. Original `905a4f0f` calls `resolve_admitted_element`, whose verified local artifact/build-receipt path supports an admission containing only `id`, `kind`, `revision`, `snapshot_digest`. Its parser explicitly permits that shape (`core/element/project_packs.py:90–92`). Validity of those historic artifacts does not supply the new Runtime portable-object authority, so an ad hoc client authority bypass would be wrong; it also does not justify claiming compatible deletion.

The supplementary comparison creates an admission and build artifacts using the existing project-pack fixture, removes only the optional portable descriptor, independently verifies that the real `resolve_admitted_element` still resolves the exact revision, and invokes each helper with identical explicit head/clip/element/hold inputs. **Original succeeds; candidate returns `validation_error: pack snapshot unavailable; re-admit pack`.** The original comparison uses its real resolver, validator and publisher preparation with a mocked publication transport; it is not a live old-endpoint acceptance claim. The candidate refuses before POST. The original success expectation stays an ordinary assertion; no test was changed to expect refusal or marked skip/xfail.

The 89 helper/session and 266 neighbor evidence therefore does not establish *all original helper positives*: its unit setup always supplies `snapshot_object`, while actual-service legacy-shape negatives exercise native authority refusal, not old-helper compatibility. Keep WC4 held until a bounded compatible migration is qualified, or the orchestrator/owner explicitly settles the behavior change. Do not silently re-admit during save, weaken snapshot authority, or label this gap pre-existing in the public helper. The earlier decision allowing old-field PARAM refusal does not establish that this broader public-helper success may be removed under this brief.

## Source and behavior assessment

- The helper emits only `clip.set-element`, optional hold `clip.set`, optional nonempty-values/clear `clip.set-params`. It no longer calls the parent publisher or embeds a timing compiler. `RemoteTimelines.update_parent_element` forwards the additive `session`/`clear_params` arguments; existing positional/keyword parameters and public result/receipt/key fields remain.
- Scope is explicit: helper target is always `parent/clip:<actual-id>`; native `_target` accepts explicit parent or occurrence references, records `scalar.images`/`scalar.target`, and binds occurrence identity/shot ownership when relevant. It does not infer a raw ID from a displayed ID. Helper and native command both preserve id/kind and an already selected pack owner; owner-less drafts can still adopt a real admitted owner. Existing actual second-owner admission/refusal coverage passed.
- `element.targets` records actual scoped clip membership **and order**, with `query_version=1` and `guard-membership`. `check_mirrors=False` keeps scalar compatibility with divergent legacy mirrors. Permanent occurrence membership/order replay/inverse tests pass; actual helper requests also assert parent selection capture. Relevant generated-hold/raw-media preconditions are recorded as reads. This is not a claim that every unchanged sibling property conflicts: the selection concerns membership/order.
- `_selected_schema` records exact `params.schema`, `params.snapshot`, and `params.element` relationships and retains the chosen verified document. Actual service tests prove selected V1 after V2/removal, deleted source/cache, restart, replay, inverse and redo through exact object custody. Existing missing/corrupt/foreign/unadmitted-source negatives remain passing.
- Authored absence versus empty params remains distinct. `None`/empty requested patch does not manufacture params writes; explicit `clear_params` emits native clears; known changed properties validate without retroactively rejecting opaque stored values. Inverse/redo, ABA refusal, sibling/registry/transcript/shot/internal preservation pass. Existing equal raw mirrors are derived by recorder/compiler; opaque config/app fields remain intact. The legacy app element catalog is preserved rather than pruned, as in the previously approved native source.
- Pending requests use the **existing** `TimelineSession._stage`, outbox format, fsynced atomic write and `flush`. Exact original request body/key are durable before POST. Retry matches existing pending intent before capture, never refreshes original guards/schema pin, and retains flight on ambiguous failure. No extra request journal/cache or fabricated accepted history was introduced.
- Acknowledged identities are looked up in real paginated Runtime history, scoped to actor and key; receipt result supplies original request `base_revision_id`, not accepted `previous_revision_id`. Original before-state is reopened at that original base; result is built from the original accepted canonical image. No recapture/POST/admission read occurs. The added probe proves this even when **the initial acceptance was rebased** (`previous_revision_id != base_revision_id`), after lost ACK, Runtime/client restart and another disjoint head; forced real one-item history pages exercise pagination. Full public result and receipt equal the recovered result.
- `_matches` uses recursive JSON `equal`, which distinguishes bool from number while allowing numeric equivalence. The probe accepts duration `3.0` for original `3`, refuses nested `True/False` changed to `1/0`, and preserves current head. Existing tests cover changed duration/target/key/base while pending and changed acknowledged intent.
- Explicit source pins remain immutable through native session matching and Runtime idempotency: the supplementary probe changes a persisted command's pin and confirms refusal before another POST with the original flight intact; after helper recovery it changes the same-key body pin and confirms real Runtime refusal with head unchanged. The public helper itself has no caller `schema_source` argument; its matching deliberately removes the internally captured pin. Do not describe this as qualification of a public explicit-pin argument.

## Owner 12:16 original selected-PARAM source boundary

Read `design/app-selected-param-original-pin-authority.md` and the separately assigned rule/fixture brief. No authority policy is invented here. The bounded helper does **not** choose first/last/latest matching entries from `dependency_manifest.documents`; it reads the current default/named admission document and captures its exact pin, always emitting `clip.set-element` before PARAM. That gives explicit recorded provenance for this invocation, but does not recover a target's original historical PARAM source.

**Hold the same-element PARAM/reselection interpretation and general original-pin production binding for the separate freeze.** A params-oriented helper call still includes the required element argument and always emits set-element, even if canonical element JSON is unchanged. Whether that constitutes the owner's required *explicit reselection* cannot be inferred merely from the presence of the generated op. This review neither authorizes silently selecting current metadata for ordinary PARAM nor chooses a manifest-order winner. No new accessor/endpoint/DTO/history policy was added. Historical recovery of this helper's already captured flight does preserve its original pin, independently of that fresh-edit policy question.

## Independently executed evidence

Exact source preparation, from `/home/user/work/wt/agt-review-wc4-helper-native`:

```sh
mkdir -p /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-wc4-helper-native/notes/source
git archive tl/agt-m2-wc4-helper-native-finish | tar -x -C /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-wc4-helper-native/notes/source
git show 905a4f0f:astrid/sdk/timeline_elements.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-wc4-helper-native/notes/original_helper.py
```

All following pytest/Ruff commands ran from that private `notes/source` archive; shared dependencies were read-only. The temporary source archive is removed after reporting; the supplementary probe and original helper source remain alongside this report for reproduction.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/core/test_timeline_element_publication_runtime.py tests/sdk/test_timeline_selected_schema_runtime.py tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py
```

**63 passed in 87.21s, exit 0.** This reruns the final adapter form, including all 16 public-helper cases; it does not merely cite the earlier 63-before-cleanup result. RuntimeService only, no daemon/socket/browser.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/test_timeline_element_publication.py tests/sdk/test_timeline_sync.py tests/editing_conformance/test_recipe_clip_set_element.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_recipe_scalar_commands.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_commit_provider_scalar.py
```

**355 passed in 80.00s, exit 0**, combining the prior 89 helper/session and 266 neighboring recipe/provider cases.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py
```

**24 passed in 98.50s, exit 0.** No schema or generated pin change by this candidate/review.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -c pyproject.toml -o addopts= -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-wc4-helper-native/notes/test_review_wc4.py
```

**3 passed / 1 failed / 2 unknown-integration-marker warnings in 4.59s, exit 1.** Passes: combined rebased/lost-ACK/restart/pagination/typed-intent probe, explicit-pin pending+acknowledged refusal, original helper digest-only success. Failure is the unchanged candidate success expectation described above. These are supplementary probes, not newly landed main-suite evidence. The external test's imported modules emit marker warnings because its collection does not load repository `tests/conftest.py` registration. An initial probe version had duplicate aliases of the same configured fixture (2 setup failures, 2 passes); this was corrected only in private probe code. An attempted `-c pytest.ini` invocation failed because this repository uses pyproject.toml. Neither was classified as a product failure. The penultimate corrected probe also gave 3 pass / 1 same product failure; the final run added the acknowledged explicit-pin check.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline_elements.py astrid/sdk/timeline/_clip_scalar_commands.py astrid/sdk/timeline/_recording.py
```

**All checks passed, exit 0.** From the review Git worktree, `git diff --check 905a4f0f a6098b5d` passed and `git status --porcelain` was empty.

No full/full* request, make check, HTTP/authentication/local-door journey, App/browser, renderer/pixel/audio, macOS or composed integration-tree qualification was performed. No passing behavior test was weakened, disabled, skipped or rewritten to assert refusal. No shared dependency/runtime/fixture was changed. The unresolved public-helper compatibility finding and separately frozen PARAM-source rule prevent an unconditional writer-deletion approval; they do not block completion of this review. Recommended next action: orchestrator sends the bounded compatibility counterexample to the implementation owner, retains WC4's existing held ledger state, then requests review of the corrected migration together with the settled original-pin boundary.
