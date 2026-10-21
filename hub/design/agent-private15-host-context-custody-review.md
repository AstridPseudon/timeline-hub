# Agent private15 host-context custody review

Decision: **REQUEST CHANGES**

Reviewed identity:

- commit `64f8a02f7b692b039c457d2a585e55f613e6fa6a`
- tree `c4ca0e7eaca00cf554f5b0edab7318257552cc54`
- parent `4d4535882f1e028805c3da178bf9a7fa53696da8`

## Blocking finding

The converted action regresses existing successful advisory outcomes. The
shared `sync_draft_voiceover()` still returns a successful `{status:
"planned", ...}` for `plan_only` and `{status: "unchanged", ...}` when there
are no jobs (`astrid/packs/video_editing/shared/draft_voiceover.py:465-466`).
The new action unconditionally requires `result["authoring_proposal"]` and
raises `ValueError("synchronization produced no authoring proposal to settle")`
when it is absent (`astrid/packs/video_editing/actions/sync_draft_voiceover/run.py:78-80`).
The pack also makes the proposal output required and describes plan-only as
requiring a nonempty proposal (`pack.yaml:97-108`), so these Main-positive
advisory/report results cannot complete.

The added `test_advisory_shared_result_cannot_fabricate_proposal_output`
(`tests/packs/video_editing/test_sync_draft_voiceover_action.py:135-143`)
asserts this refusal for both statuses. That is the regression, not acceptable
action coverage. The unchanged shared tests passing proves only the direct
helper behavior; it does not qualify the action path.

Fix the output carrier one-to-one: preserve successful advisory/report output
for `plan_only` and `unchanged` (an existing optional-output/report carrier is
preferred), while requiring and settling the single
`timeline/authoring-proposal` file only for the changed, nonempty proposal
case. Do not synthesize a no-op command, receipt, or fake edit. Retain the
original advisory expectations as positive tests and add action-level
assertions for both statuses.

## Custody review

The private claim-to-admission-to-live-context path is otherwise consistent
with the design. `_producer_action_admission()` copies only the outer
task/attempt/executor/fence/runtime-epoch and exact four-key admitted target,
requiring task/capability/project matches and rejecting missing, conflicting,
or boolean-as-integer values. `_ActionContext` is read-only, scoped to the
managed runtime request and exact `attempt/outputs` directory, and fences
copied contexts, PID/thread changes, replacement directories, nesting, and
post-invocation use. The private preparation view ignores the caller's client
attribute and blocks legacy `publish`.

The existing host admission fields retain `network_nonce` and
`allowed_routes`, but this change does not add or widen them; the action
remains `network: false`, and the host does not install network policy/evidence
for it. Public inputs, DTOs, Runtime schema/routes/scopes, and serialized
request fields are unchanged. Existing capability/source digests are checked
before the action and the host stamps the admitted source identity on
settlement; the bounded forged-source/definition controls pass.

The changed-output path correctly writes one atomic
`authoring-proposal.json`, standard manifest, and primary
`timeline/authoring-proposal` result. `write_manifest`/harvesting recompute
the file hash, and `build_producer_batch` validates the existing six-key
proposal carrier without adding a guard to the serialized proposal. No
receipt or direct publication is fabricated. The real combined speech/shared
worker and Runtime acceptance are not proven by this tree; the action tests
stub preparation as documented.

No giant-file threshold or structure baseline was loosened (`new=0`), Ruff
findings improved by 34, no existing tests were edited/skipped/xfail-marked,
and no full/live suite was run. The added negative controls are bounded, but
they must not continue to encode the advisory regression.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover.py tests/editing_conformance/test_recipe_native_voiceover.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py` — **180 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py tests/packs/video_editing/test_sync_draft_voiceover_action.py -k 'noop or plan or advisory or existing_action_settles'` — **5 passed, 37 deselected**; the two action advisory cases pass only because they expect refusal.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_structure_baseline` — **passed** (`current=14, new=0, fixed=0`).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline` — **improved** (`current=2186` vs recorded `2220`; command exits 1 because the repository asks to lock improvements, and no baseline was changed).
- `git diff --check 4d453588..64f8a02f7` — **passed**.

No Runtime, normal-pin, live, browser, or full-suite qualification is claimed.
