# Element declaration retention — source review

2026-10-20. **APPROVE the bounded Agent source behavior; HOLD schema publication, pin changes and WC4 closure pending the additive canonical union and normal generated pair.** No source defect reproduced in the reviewed scope. This is not qualification of a new Agent/Runtime pair.

Reviewed Agent `98c38a7c85a3f1d2a8c5a1019a5815898ec922f5`, predecessor `167d050506b9ae81fe8839f122de34d2082558cf`, their final reports/development reports in `workers/agt-m2-element-{update-native,declaration-retain}/{report.md,log.txt}`, PLAN and repository AGENTS. Source worktree: `/home/user/work/wt/agt-review-element-retain`. Current comparison: Agent `/home/user/work/agent` at `df2739f903edac02bd36b4446deeea847524c040`; Runtime `/home/user/work/runtime` at `c0dcd3871d78c405184506eb6735565592498c77` (observed refs, not a tested pair).

## Source findings

- `astrid/sdk/timeline_elements.py:53–92` retains the same parent clip and submits one native command batch: `clip.set-element`, optional `clip.set` hold, optional `clip.set-params` only for a nonempty explicit patch. Both helper and `astrid/sdk/timeline/_clip_scalar_commands.py:109–132` preserve existing id/kind and an already selected `packId`. The owner check is not just admission existence: a review probe admitted a second same-id/same-kind pack in the SAME project, then confirmed raw provider refusal and helper refusal before submission. Legacy owner-less drafts can still acquire an admitted owner; the owner guard cannot establish an owner absent from the original ref. That is the existing draft-adoption behavior exercised by the conformance fixtures.
- `astrid/sdk/timeline/commit.py:350–460` hydrates the explicit pin and resolves the **target** element revision at the set-element stage. `_selected_schema` in `astrid/sdk/timeline/_scalar_commands.py:98–128` records `params.schema`, `params.snapshot` and the selected-element binding, and retains the exact document. `astrid/core/element/project_packs.py:536–700` checks scoped document id/version/digest, actual pack owner, unique id/kind/revision admission, snapshot descriptor/bytes, pack manifest and build receipt. Inline caller schemas, a catalog, source files and build caches do not establish save authority. The helper reads only Runtime declaration metadata; the provider reads the immutable selected object through `config_source`/`document_object`.
- Element-only absent/empty params remain literally absent/empty; the recorded authored write is only `['elementRef']` (plus alias removal when needed). No copied params writes or phantom clears remain. Nonempty params merge through native changed-property validation; opaque existing values are preserved, not retroactively validated against a new full schema.
- Hold uses the existing scalar recipe and literal source seconds. `_hold_extent` in `_clip_scalar_commands.py:14–76` retains rational-fps/frame, playback rate and occurrence-boundary rules. The 287-case rerun includes the speed-two/rational-fps/source-hold and move-then-hold neighbors. This is not renderer/pixel evidence.
- `astrid/sdk/timeline/_recording.py:205–215` derives an existing `config.clips` mirror through `derived_writes`; the helper does not author that mirror or prune `config.app.elements`. Tests preserve sibling rows, registry/transcript data, opaque params/clip fields, shots and internals. The old whole-candidate publisher and its Writer shim remain deleted from this helper.
- `timeline_elements.py:95–107` retains public result fields, receipt and explicit key, with native failed DomainResults passed through. Unit tests assert the complete success result, receipt/key and conflict/validation paths. Actual refusal tests use a direct RuntimeService adapter which raises Runtime errors; they do not independently prove HTTP-to-public-ErrorObject mapping.

## Replay, inverse and public retry limits

`tests/core/test_timeline_element_publication_runtime.py:61` proves changed/same revision + hold/params, reload, RuntimeService restart, exact captured-request retry without command execution, inverse/redo, preservation of a newer disjoint label and ABA inverse refusal. `:159` covers the four absent/empty existing/requested params combinations, reads exactly the target snapshot, asserts the source pin and absence of params writes, admits a later revision, removes the current admission selection, deletes source/cache, restarts, and proves replay/inverse/redo still use the original retained pin/object. The replay is based on the post-inverse closure that already authorizes this retained pin; it does not authorize arbitrary historical pins for fresh callers. Undo restores the exact authored parent payload while retaining provenance for redo, so pre-pin revision-id equality is not claimed.

**Public helper retry is narrower than request retry.** `update_parent_element(... expected_head=old, idempotency_key=same)` reopens the head and returns `conflict` at `timeline_elements.py:35–39` after the first call was accepted; it never reaches the idempotency store. The supplementary diagnostic reproduced this, then replayed the stored original commit request successfully. This preflight predates these two commits. Do not describe the nine cases as a restart-safe helper/outbox workflow: they prove Runtime replay of the captured request. Any public helper retry guarantee needs its own requester/outbox requirement and test; this review does not invent one.

## Mandatory canonical union — outgoing file is not the next source

Canonical path in Agent: `astrid/core/timeline/schema/edit-command.schema.json`; Runtime counterpart: `contract/schemas/edit-command.json`.

| Input | Raw SHA256 | Definitions / ops |
| --- | --- | --- |
| Candidate `98c38a7c` | `c520c7fa5269f837965b308607dcc7c73a9e4fd5f1da6bb09022996ba86620e6` | 43 / 21 |
| FROZEN `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00` | `30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd` | 48 / 22 |
| Current `df2739f9` | `83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224` | 43 / 21 |

**Conflict with the predecessor's final recommendation:** copying its outgoing `workers/agt-m2-element-declaration-retain/edit-command.schema.json` byte-for-byte as the next Runtime source would drop frozen/current behavior. Its older base does not justify those deletions. The final report's “generate that pair” needs this correction before generation.

Exact required additive successor: **FROZEN 0a0ac7ba/30da unchanged, except replace `$defs.ClipSetElementArgs` with the reviewed candidate definition**: add optional `properties.schema_source = {"$ref":"#/$defs/DocumentPin"}` and its owner/retained-pin description; preserve `required: ["elementRef"]` and `additionalProperties: false`. Keep all five definitions `ProducerAdmittedTarget`, `ProducerIdentity`, `ProducerAttemptPin`, `ProducerGuardArgs`, `SettledProducerProposal`; the complete `EditCommand.allOf` condition for `producer.guard`; and the exact closed optional `consumed` array definitions in BOTH `OccurrenceAddMediaArgs.properties` and `PlacementCreateArgs.properties`. Preserve every other definition/condition and numeric constraint. Result: **48 definitions / 22 ops**. A new hash/freeze belongs to the manager, not this review.

Read-only comparison with Runtime's `generators/command_schema_compatibility.py` reports eight compatibility errors against the freeze (five missing definitions, missing operation, two removed consumed fields), and two against current (the consumed fields). An in-memory union constructed exactly as above passes whole-schema compatibility against candidate, frozen AND current, plus `Draft202012Validator.check_schema`. No schema file was written. Read-only `git apply --check` of the combined two-commit product delta onto observed current passed: no textual conflict requires replacing a whole source file. The conflict is semantic if an old full schema is used as the canonical source.

Before generation, carry forward and extend `tests/sdk/test_timeline_current_union_schema.py` from the frozen source: protect the ENTIRE frozen/current inputs and update `test_only_reviewed_producer_and_consumed_additions_change_current_schema` to allow exactly the new optional field/description. Its old exact-equality allowance does not yet include this change; do not remove producer definitions or weaken containment checks to make it pass.

Normal Runtime generation remains required: publish the byte-identical approved union, run `python generators/generate.py` and `python scripts/artifact_manifest.py` with their normal checks/release procedure, then refresh Agent through `scripts/vendor_lock.py` and rerun the named qualification on that immutable pair. `runtime.lock.json` in this candidate is still `94114269d1ce23ab3224d7eca5a85138ce2b5fed`; its generated client has no typed set-element variant. Acceptance via that Runtime's generic envelope does not qualify the new schema/type publication. No schema, generated file, release or pin was edited here.

## Evidence and remaining regression gaps

Commands below ran from `/home/user/work/wt/agt-review-element-retain`; shared dependencies remained read-only.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/test_timeline_element_publication.py tests/editing_conformance/test_recipe_clip_set_element.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_recipe_scalar_commands.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_commit_provider_scalar.py
```

**287 passed in 65.57s, exit 0.** The original empty-params success test is passing, not xfail.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/core/test_timeline_element_publication_runtime.py
```

**9 passed in 19.64s, exit 0.** Direct RuntimeService only; no daemon/sockets. The module's `use_runtime(commit=vendored_runtime_commit())` selects immutable `94114269`, regardless of the locator's current HEAD.

Prior central evidence independently inspected, not resubmitted: `tests/agt-m2-element-declaration-retain-commit-integration-1020094633-31228/{snap,summary,log.txt,status,exit}` under the orchestrator directory. **34 passed in 81.75s, exit 0.** Its snapshot tree `f836181e24aee0213db5248ac4dc74b96ab986f0` equals this review HEAD's tree exactly (`git diff <tree> HEAD` empty). Executed command:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/core/test_timeline_element_publication_runtime.py tests/sdk/test_timeline_selected_schema_runtime.py tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py
```

Supplementary review-only command:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -c /dev/null -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-element-retain/scratch/test_review.py
```

**15 passed in 21.41s, exit 0**; two unknown-integration-marker warnings because `-c /dev/null` bypasses repository marker configuration. Thirteen actual element-only refusals cover missing pin, inline schema, wrong version/digest, changed id/kind/owner, revoked/legacy admission, missing/corrupt object, foreign project and denied authorization. One authentic second-owner test and the public-retry diagnostic complete the count. These are supplementary probes, not new permanent conformance evidence.

Permanent gaps: `tests/sdk/test_timeline_selected_schema.py:290` has five detached-provider element-only negatives, while the new actual-service module has only the forged revision element-only refusal; the larger actual-service refusal matrix in `tests/sdk/test_timeline_selected_schema_runtime.py:463` exercises **set-params**, not set-element. Promote the relevant supplementary element-only refusals and genuinely admitted second-owner case into the existing main-suite files. Also qualify changed payload under the same key and public error/receipt mapping on the generated pair; the nine cases do not establish those specifically for this helper. No demonstrated authority bypass is being reported.

`git diff --check`: exit 0. Product worktree remains unchanged. No full suite, make check, browser/live-door journey, App, render or macOS qualification was run/requested; no new pair qualification or WC4 deletion-ledger closure is claimed. Review task is complete and unblocked. Recommended next step: manager composes/freezes the exact additive successor, preserves the source tests and strengthens the missing permanent negatives, then obtains normal generation/pin qualification before closure.
