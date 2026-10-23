# R2 combined fork + emitter inverse: causal diagnosis 1246

**Classification: Runtime inverse-stage physical materialization boundary needs work. No bounded Agent-only correction is justified by this capture.** The genuine whole undo remains RED; no guard was waived and no product or suite file was edited. This is a diagnosis, not G5/P1 qualification or a passing undo result.

`ORCH` below is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`. Worker evidence is `ORCH/workers/agt-R2-fork-emitter-undo-diagnosis-1246/evidence/`.

## Exact bases and execution

- Agent: `bfcf78db998868e4a7d92779a83cd3aaba82a98a`, tree `31af8a966328d313506919df9c073d4681854f0c`, assigned worktree. This is the independently reviewed A3 candidate, not integration ancestry imported into this task.
- Runtime: existing read-only `/home/user/work/wt/rt-pin-3b926efa`, commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`, clean when inspected. Current Runtime integration also reported 3b.
- Agent integration inspected at `5b1b4db82` (R1 merge of `dcb4cee32`). Relative to this candidate it has the atomic `_commit_patch.py` change and its test, and lacks the three A3 candidate paths/changes. Nothing was imported. R1 moves complete scope-union construction under `merge_mode == 'atomic'`; this captured request is `fields`. It does not change the captured leaf inverse or Runtime's physical-map comparison.
- `origins.json` captures actual imported paths and SHA-256 values, including the startup-loaded production provider, inverse, compiler, native copy, Runtime service/store/auth and fixture helpers. Offline `git show` comparisons verified **144 loaded module files** against these exact two commits (`origin-source-comparison.json`). No alternate executor/provider, generated client, dependency install, pin, daemon or socket was used.

The retained 1232 log contains the entire setup/acceptance body and the precise failing undo call, but abbreviates prepared/request values in the traceback. Those facts were sufficient to reconstruct the fixture and call, not the original random IDs or intermediate images. `agent-R2-fork-emitter-undo-regression-1246.py` retains that positive regression under ORCH/design. Setup/acceptance comes from the exact current source test; the undo call comes from the retained log. Its post-call accepted/exact-restoration assertions express the restoration requirement, not an invented captured outcome. The executed artifact is retained separately as `evidence/regression-executed.py`; the final design artifact differs only by an import-separating blank line.

One instrumented normal in-process service journey was executed. Observers call the original service method with the unchanged body and arguments, return its original result, and re-raise its exception. Python tracing captures the real auth inputs and local comparison images; it never replaces a prepared result or validation return. The first launch failed before any service request because the harness's `tmpdir` is a file naming the private scratch directory; correcting that path enabled the single actual journey. No failing undo body was retried after the actual refusal.

## Actual request → history → inverse → refusal

`service-01-*` is the full v2 fork+emitter preview; `service-02-*` is its accepted commit; `service-03-*` is whole undo. Both base IDs, command list, label, step labels/intents/tags/patches/reads/ordinals, merge/reads/dry-run, source/rationale/group and idempotency key are retained. Replies retain the actual data/receipt/canonical shapes. Preview returned `would_status: accepted` and no receipt; acceptance and unchanged sibling assertions completed before undo.

The publication in this capture is `txn-1c5db05293e34736a5207e6f07c3818f`. `auth-input-35.json` contains the actual inverse request, prepared result, authenticated source/base, continuations and store-loaded source history. That history has:

| Source step | Authored command and native capture | Canonical effect |
| --- | --- | --- |
| `fork-edit-0`, ordinal 0 | `occurrence.fork`: create `shot:selected-shot`; change selected occurrence's `shot_id` | Add copied internal/shot roots; update selected occurrence's shot ID and revision pin |
| `fork-edit-1`, ordinal 1 | Emitter `doc.patch`: remove `params.text` on `occurrence:f2-occurrence/clip:f2-agent-clip` | Replace selected internal/shot revisions and parent pin; remove preceding physical roots |

The accepted source record for ordinal 1 already carries two `commit.materialization` bindings naming those internal/shot successors. Thus ordinary forward acceptance actually exercised native leaf capture plus canonical physical turnover, rather than requiring invented root-native writes.

`apply_inverse` (`astrid/sdk/timeline/inverse.py:703`) reverses the authenticated steps. First is `fork-edit-1`, native range `[0,1]`, effect range `[0,5]`. Its only native write is exactly the authenticated source write reversed:

```json
{"ref":"occurrence:f2-occurrence/clip:f2-agent-clip","path":["params","text"],"before":{"state":"absent"},"after":{"state":"present","value":"hello"}}
```

The second stage is `fork-edit-0`, native range `[1,3]`, effect range `[5,9]`. Runtime fails before authenticating that stage; it is not credited as passing. Agent's complete prepared final canonical document is nevertheless **exactly equal to the full original document**, including its original revision identities, as verified offline against the captured pre-preview document.

The first failing comparison is `runtime_protocol/timeline_commit_auth.py:961` in `_inverse_stage_boundaries`, after source-history stage/site membership and each sequential native before-value check have succeeded. `stage-comparison-01.json` retains its actual `stage_before`, `stage_after`, `native_image`, native writes, stage effects and binding. Repeated snapshots 02–08 are trace events at the same multiline expression, not additional service executions.

The complete payload mismatch is bounded to physical identity turnover:

| Image | Native projection retains | Authenticated stage effect restores |
| --- | --- | --- |
| Internal root | `authoring-timeline-revision-97f6376e…` | `authoring-timeline-revision-156c0be1…` |
| Shot root | `authoring-shot-revision-9a042d5c…` | `authoring-shot-revision-13a1eb4e…` |
| Parent selected occurrence | pin to `9a042d5c…` | pin to `13a1eb4e…` |

Full IDs are in `causal-summary.json`. Offline checks establish that the restored native internal payload equals the effect's replacement internal payload in full; the shot payload differs only by its internal revision pin; and the parent payload differs only by the selected shot revision pin. All other closure payloads agree. Both restored intermediate roots equal the accepted source fork step's root effects, and the source emitter's materialization bindings describe the reverse turnover. This is not an unrecorded authored content difference or a missing undo of the text field.

The service raises `RuntimeErrorBase` with `reason: invalid_records`, `status: refused`, empty conflicts and null base/current (`service-03-error.json`). The observed underlying rejection is the same 422 `inverse stage native writes do not cover its authenticated effect image` as 1232. The stored head and entire canonical document before/after rejection are equal. The guard prevented persistence.

## Ownership and smallest next change

This conclusion follows the production capture compared with the positive requirement, not the repository containing the exception.

Agent's existing `_restore_write` and `apply_inverse` preserve authenticated native membership and sequential values. `CommitPatch.after`/`inverse_closure` compile each intermediate bundle through the existing immutable-source reuse; `finish` records the actual physical effects and bindings. This capture proves their reversed native leaf, intermediate historical payloads and final canonical closure agree. Adding fabricated root-native writes would contradict the immutable source capture; retaining the old revision ID with different bytes would contradict immutable image binding. Neither is an acceptable Agent repair.

Runtime3b's ordinary `step_output` authenticates the canonical root/edge effects and materialization bindings; the accepted forward command is direct evidence. Its inverse aggregate-root path (`_inverse_stage_root`, `_inverse_stage_root_equal`, and `_inverse_stage_boundaries:916–940`) already verifies native `shot:*`/`occurrence:*` aggregate observations against physical closure images, accounting for compiler-managed pins. But the leaf path at 942–960 changes a payload **under the old physical key**, then compares the entire physical-keyed payload map at 961. It has no equivalent proved materialization-turnover handling for this leaf stage. The first emitter reversal therefore cannot reach its correctly compiled physical stage image, even though its authored bytes match.

The bounded Runtime need is to authenticate that stage's owner-preserving internal → shot → parent revision turnover after applying its exact authenticated native captures, then require complete payload/ownership equality and unchanged unrelated images. Existing history/step/range/site guards, sequential before-values, per-effect bindings, digest/closure checks and forged-native controls must remain. Do not copy arbitrary `stage_after` roots into the native image or merely ignore revision fields; the full restored payload and owner correspondence must be proved. Also do not align only to the final accepted closure: this intermediate `selected-shot` root legitimately disappears during the later fork reversal. No new policy, schema, wire shape or contract decision is needed to classify this requirement.

The unique Runtime G5 inverse owner `rt-G5-inverse-boundary-diagnosis-1236` owns the separate restructure 503 diagnosis. Its peer note says its underlying cause was not yet established. This report supplies the exact shared source candidate (`timeline_commit_auth.py:898–993`), input and physical-turnover cause for coordination; it does **not** assert the two failures share a cause. No competing Runtime patch or second observer was started. Handoff is also recorded in `peer-agent-to-runtime-20261023T1254-fork-emitter-inverse-cause.md`.

The A3 `_CopiedShot` provenance is not a serialized baseline grant: native copying installs an internal subclass; `_copied_shot_baseline` verifies the immutable runtime document, project/timeline, exact parent pair, source occurrence/shot pin and destination before rebuilding the baseline/remap. This task loaded those candidate sources. The captured restored intermediate roots equal accepted source history, which argues against candidate copy provenance being the cause of this failure. Raw internal subclass attributes were not separately captured, so no claim is made that this observer replaces A3's provenance-forgery controls.

## Commands, results and limits

All commands ran from the assigned worktree; private scratch is `/tmp/w-bbcee88e99` (the value stored by the harness in the worker's `tmpdir` file). Exact diagnostic command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa timeout 30 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-fork-emitter-undo-diagnosis-1246/observe.py
# exit 1: genuine retained inverse-stage 422; durable observer-run.log and evidence above
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-fork-emitter-undo-diagnosis-1246/analyze.py
# exit 0: 10 offline causal checks passed; no service/classifier replay
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/inverse.py astrid/sdk/timeline/_commit_patch.py astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/native_occurrence_duplicate.py
# exit 0: All checks passed (ruff.log)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-bbcee88e99/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --follow-imports=silent astrid/sdk/timeline/inverse.py astrid/sdk/timeline/_commit_patch.py astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/native_occurrence_duplicate.py
# exit 0: Success: no issues found in 4 source files (mypy.log)
git diff --check
# exit 0; git status --porcelain is empty; product/tests unchanged
```

Scoped Ruff also passed for the three diagnostic Python artifacts (`observe.py`, `analyze.py`, design regression; `artifact-ruff.log`), after correcting one import-separating blank line in the design artifact. The 144-module source comparison used only `git show` and SHA-256, not a provider rerun. No pytest suite, full suite, HTTP/browser/native broad lane or repeated type-full was run. This standalone observer needs no localhost or pytest `--net`; its wall timeout was 30 seconds. No success claim is made for undo, merged/conflict journeys, guard-negative suites or later-stage Runtime validation.

Capture limitation: service requests/replies/prepared/auth inputs/history and native/effect images have separate durable files, as do pre/post head/canonical snapshots. The observer wrote module origins before and after each service boundary to the same filename; only its final `origins.json` survives. Therefore distinct pre/post origin snapshots were not retained. Actual loaded source locations are also present in the traceback, and the final origins all match exact source bases, but this is not presented as a separately retained temporal origin comparison. No second live observer was justified solely to repair that reporting limitation.

Recommended next step: the existing Runtime owner should assess this bounded materialization boundary from the capture, preserve the positive regression, and implement/review any fix in its authorized Runtime worktree with strict forged-write/pin/owner controls. Keep combined undo/G5 unresolved until the original positive behavior passes. No task blocker prevented this causal diagnosis; the product behavior remains blocked on that implementation and proof.
