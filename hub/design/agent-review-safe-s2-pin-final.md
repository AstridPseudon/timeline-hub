# Final Agent S2 consumer pin review

**APPROVE the bounded pin/source unit** `905a4f0f1dcadf92a226b1da0baba50b8a37178d` (tree `41c7fe73dbd50bb31cdadf41e82a52a2520d78f6`), including prepared source `fc69684789f52ef1d65467dc9b590893ed8d7b3b`. No blocking product or authority defect found. This is approval for the reviewed consumer unit, not a claim that a composed integration tree or the project gates have passed. The orchestrator must resolve the one conflict described below while preserving both guards.

## Exact pin and generated outputs

Independently verified the clean immutable producer checkout `/home/user/work/wt/rt-m2-pin-2c4ac180`: HEAD `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.

- Normal `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180` passed on an unmodified archive of the final consumer. All 15 locked files equal the official producer bytes, their lock hashes, and their artifact-manifest hashes.
- Independently recalculated **75/75 official artifact hashes**, also comparing every producer file with its committed HEAD blob. Manifest version is `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`; manifest file SHA256 is `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`.
- Generated client metadata is `0.2.13`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, **133 distinct HTTP operations**. The final pin changes only the lock, four generated client files, and two test files relative to `fc696847`. No handwritten generated output or schema override was found.
- Agent canonical command-schema bytes equal frozen S2 `26ef2bbb` and official producer `contract/schemas/edit-command.json`: raw SHA256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`, **48 definitions / 22 operations**. Existing published schema floors remain tested. There is no parent/init/word/text contract expansion.
- Composition `0.0.12` package JSON, lock, tarball, presenter test, and public element helper are byte-identical across prepared source, final pin, and reviewed integration `cf7448ed`. Full-theme equality remains an actual `assert.deepEqual(DEFAULT_THEME, BUILTIN_DEFAULT_THEME)` via the presenter's serialized builtin-theme input.

## Behavior and fixture audit

AST comparison preserved the complete original M1 test body (both `disjoint-rebase-undo` and `touched-basis-conflict` parameters) and the complete numeric producer positive. The temporary disjoint-view xfail and producer xfail are removed. Neither those files nor the identity lane retain skips/xfails. The central run below passes normally without `--runxfail`.

The source prep retains request-scoped Runtime `producer_attempt` capture, exact producer dependency recording, original admission/attempt/digest identity through rebase, first-only/nonempty producer guarding, and pending-proposal isolation in the outbox. Selected element changes require the exact retained document/object and selected pack owner; raw schema bytes or caller pins do not supply Runtime authority. Existing native schema, history, reservations, and inverse checks remain intact. WC4/public-helper publication remains explicit separate debt.

Inspected the changed tests and fixtures, including the element golden's structural JSON changes. Its new pin, admitted owner/revision, object inputs and capture binding support the retained-schema requirement; original before/after and inverse assertions remain. New refusal cases supplement existing positives. Design-only producer goldens and detached preview tests are clearly separate from actual Runtime acceptance tests.

The new automatic-placement fixture restores the existing authenticated pre-cut film, adjusts the neutral parent's duration/FPS through the existing publication API, then enables the scene tripwire. The tripwire's entire original body is AST-identical after extraction into `_disable_scene`; preview/acceptance/retry/inverse/redo run with it enabled. Media identity and video duration arrive through normal task admission and fenced settlement (`generation.publish_v1` metadata), followed by generated-client selection and verified-media reads. No SQL writes, manufactured authoritative database metadata, fake acceptance port, schema override, or renderer bypass appears in the new positive path. Private closure calls read the baseline; publication happens only during seed preparation. The unchanged identity tests contain SQL **reads** for preservation assertions, not new setup shortcuts.

New keyed-view cases use the normal generated transport and actual HTTP handler, lose an accepted ACK, advance head, restart, recover the original keyed result, reject changed options under the original key, and allocate fresh logical keys. Real read-only credentials are denied before ingestion; inspection still works; projects:write creates the view. No passing success test was rewritten to expect denial. The reviewed seed and media payloads qualify contract behavior, not decoded media quality or pixel/audio rendering.

## Integration overlays and exact conflict

**Correction to the earlier source-review description:** `fc696847` is not a descendant of `78d548cf`. Its parent, and its merge base with the current integration line, is `01926d032de76ccf2514adde0a1854c98341aba9`. Consequently a direct tree replacement would lose newer integration work; an ordinary merge preserves the files added on that line.

Read-only path intersection plus three-way `diff3 -m -E` inspection against the actual merge base found:

| Integration point | Paths changed on both sides | Actual conflicting path |
| --- | --- | --- |
| `78d548cf` native frontends | `_timing_evaluators.py`, `sync.py` | `astrid/sdk/timeline/sync.py` |
| `60ddf8f0` video unplace | same | `astrid/sdk/timeline/sync.py` |
| `cf7448ed` CLI trim | same | `astrid/sdk/timeline/sync.py` |
| `a2ba1bca` PCM overlay | `_timing_evaluators.py` | none |

`astrid/sdk/timeline/_timing_evaluators.py` is byte-identical on both sides (SHA256 `be152d3e6e8427aedbdcd74fa0d452ca4df56a4d01154bebc2b05a0357251908`); preserve its exact-fraction `_timing_number` rename. It is an overlap, not a conflict.

The single divergent hunk is immediately after `state = self._state()` in `TimelineSession._stage`. Preserve **both** checks before pending matching/capture:

```python
if base is not None and state["base"] != _pin(base):
    raise TimelineEditError("outbox no longer has the original sheet basis")
if any(call['op'] == 'producer.guard' for call in state['pending']):
    raise TimelineEditError('flush the producer proposal before another edit')
```

Keep integration's `base` parameter and forwarding in `commit_many`/`_stage`, its native trim method, native checkout/sheet files and tests, and its video-unplace/delete/pool changes. The four PCM files from `a2ba1bca` are untouched by the entire prepared source and final pin, so preserve them from integration. No other conflicting path was found in these comparisons. This was static composition analysis only: no merge or synthesized product tree was written or tested. Requalify targeted frontend/sheet/trim/producer guards on the orchestrator's actual composed tree.

## Exact independent checks

From a private unmodified `git archive 905a4f0f` under this reviewer's `notes/source`:

```sh
python3 scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180
```

**Exit 0**, matches producer manifest.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_vendor_lock.py tests/stage1/test_vendored_workspace_client_parity_luna.py tests/sdk/test_workspace_client_timeline_commit.py tests/sdk/test_native_timeline_facades.py tests/sdk/test_timeline_current_union_schema.py tests/editing_conformance/test_recipe_auto_placement_reads.py tests/editing_conformance/test_producer_guard.py tests/sdk/test_timeline_producer_guard.py tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_selected_schema.py
```

**484 passed in 130.35s; exit 0.** These are targeted file checks, not a full suite.

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m2-safe-s2-pin-current commit-integration --files "tests/editing_conformance/test_commit_runtime_identity.py tests/sdk/test_timeline_producer_guard_runtime.py"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-m2-safe-s2-pin-current-commit-integration-1020115555-25777 1
```

**18 passed in 51.06s; exit 0**, new central execution, final consumer tree `41c7fe73dbd50bb31cdadf41e82a52a2520d78f6`. Actual command:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/editing_conformance/test_commit_runtime_identity.py tests/sdk/test_timeline_producer_guard_runtime.py
```

M1's first fixture selects `use_runtime(commit=vendored_runtime_commit())`, archiving exact Runtime `2c4ac180` from the configured object store. The shared test locator subsequently reuses that exposed Runtime, so the identity and producer cases in this process use the same immutable pair. The service command's moving integration path is not the Runtime source being executed.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-safe-s2-pin-final/notes/audit.py
```

**Exit 0**: all artifact/lock/schema checks, metadata, preservation AST checks, package preservation and overlap/conflict analysis above. The exported source was removed after review.

## Inspected prior evidence and remaining limits

Read the actual pinner execution log, not just its summary: `workers/agt-m2-safe-s2-pin-current/log.txt` contains **385 passed / 1 integration deselected / 5 tar-extraction warnings in 229.24s**, **8 presenter cases passed in 60.08s**, and **5 original producer cases passed in 5.61s**. Their exact commands are in the pinner's detailed report `workers/agt-m2-safe-s2-pin-current/notes/report.md`. The presenter uses a private package extraction with read-only peer links and asserts package/peer preservation. Its unchanged query asserts full theme equality. These local results preceded the last M1 fixture corrections; they are evidence for their unchanged tested files, not a relabeled final-tree full pass.

Also inspected central `agt-m2-safe-s2-pin-current-commit-integration-1020114630-24838`: **13 passed in 61.14s**, snapshot tree exactly the final `41c7fe73...`. The independent **18-pass** rerun adds all five original producer cases to that lane.

The pinner reports **104 passed / 54 setup errors** in an earlier broader lane; six new auto cases were subsequently relocated, while **48 original occurrence-media cases** remain unchanged and unqualified. Five unchanged direct-shot-write tests also failed centrally. The missing `_binding_descriptor` already is absent in Runtime `94114269`, whose direct-shot/text-binding methods explicitly raise `RetiredRouteError`. These are retained visible migration debt; none was skipped, removed, or converted to refusal. This review does not turn them into green coverage.

Minor nonblocking source hygiene finding: `git diff --check 01926d03 905a4f0f` exits **2**, solely `tests/core/test_timeline_element_publication_runtime.py:357: new blank line at EOF`. The narrow `git diff --check fc696847 905a4f0f` passes. No product fix was made.

No full/full* suite was requested. No App/browser, composed integration runtime, WC4 durable helper recovery, capture certification, pixel/audio parity, owner-film, or macOS qualification is claimed. Shared dependencies and all product/integration worktrees were left unchanged. Recommended next step: orchestrator merges the reviewed unit while retaining both `_stage` guards and all integration overlays, then runs its bounded composed-tree guard/frontend checks and App's separate normal-pin qualification.
