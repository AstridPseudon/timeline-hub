# Runtime native text source review

## Verdict

**REJECT for landing as currently evidenced.** The test-only commit is structurally
bounded, but its claimed 11-case qualification does not reproduce against the
exact approved corrected ordinary014 candidate. The first explicit marked native
case fails during Runtime request-schema validation, before the real provider or
any native text behavior runs.

## Exact inputs

- Reviewed Runtime commit: `efbbec205c2bff2ed60cc02ef0b24d9e0b43ac04`
- Reviewed Runtime tree: `c19093d3d261c53b1699af87e2d18c33dd2ec529`
- Reviewed file: `tests/test_timeline_text_native_positive.py` (278 lines)
- Exact corrected ordinary014 Runtime candidate used for execution:
  `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- Candidate package: `0.2.14` (unpublished); schema digest
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`;
  Agent schema digest `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  corrected artifact digest
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`
- Frozen Agent source pin supplied by the brief: commit
  `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, content tree
  `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`
- Current public Runtime collection source: `81f8c7e0b22c34804015c054762af3d737e4698a`,
  contract version `0.2.13`

## Blocking finding

Command run against the exact corrected private candidate and frozen Agent source:

```text
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source \
PYTHONPATH=/home/user/work/wt/rt-pin-a0dca169/tests:/home/user/work/wt/rt-pin-a0dca169:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source \
/home/user/work/venv-runtime/bin/python -m pytest -q --import-mode=importlib -o addopts= -p no:cacheprovider -m integration \
/home/user/work/wt/rt-m2-native-text-source-review/tests/test_timeline_text_native_positive.py::test_native_first_use_is_project_scoped_deterministic_and_replays --maxfail=1
```

Result: **failed** on the UTF-8 first-use parameter before provider execution.
Runtime schema validation rejects the Agent-captured authorship key:

```text
occurrence:occurrence-1/text-binding:voiceover_script::
```

The corrected candidate’s `TargetKey` schema does not admit the
`/text-binding:...` target form. The Agent `commands._normalize` path produces
that key while canonicalizing the captured command. The same failure reproduced
against the older private `candidate-0.2.14`/artifact `8023...` tree; it is not
caused by the corrected public DTO export change. Therefore the report’s
`11 passed, 0 failed` claim is not valid for the exact approved pair, and the
new 11 cases do not currently prove provider/CAS/lifecycle semantics.

No assertion was weakened, no skip/xfail was added, and no source was edited.
The fix owner should reconcile the frozen Agent capture/schema contract (or use
an already schema-valid captured command) before re-running the native cohort.

## Independent positive evidence

One explicit marked central core case was run against the exact corrected private
Runtime candidate and the frozen Agent source:

```text
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169 \
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source \
/home/user/work/venv-agent/bin/python -m pytest -q --import-mode=importlib -o addopts= -p no:cacheprovider -m integration \
'tests/editing_conformance/test_next_ordinary_union_runtime.py::test_born_occurrence_text_order_clear_grouped_inverse_and_redo[]'
```

Result: **1 passed in 4.90s**. This uses the real registered Agent provider and
normal Runtime fixture path, and proves one schema-valid occurrence text batch
through clear/reload/inverse/retry behavior. It does not qualify the reviewed
test file’s captured-command path, nor does it establish the unrun 11 cases.

Public 0.2.13 collection-only check, with `ASTRID_CHECKOUT` set to a deliberately
missing Agent path, collected **11 tests in 0.20s**. This confirms the current
public default collection does not eagerly import missing Agent modules. It is
collection-only, not behavior evidence.

The previously reported central default targeted result (`69 passed, 11
deselected, 4 xfailed`) is correctly classified as **not running the new 11
integration-marked cases**. No broad/default lane was rerun here.

## Source review against the requested boundaries

- Real provider: present (`load_timeline_commit_provider("astrid")`), not a fake
  provider.
- Normal bootstrap and source pins: present (`create_project`, `create_timeline`,
  `ingest`, exact descriptors, private Agent checkout fixture).
- CAS bytes/project scope/UTF-8/size/empty-PRESENT/rebind/events/restart/exact
  inverse/redo: assertions and setup are present in the file, but the reviewed
  native cases did not reach them because of the schema failure above. Do not
  claim them as run evidence.
- SQL: no SQL writes or accepted-history fabrication. The event assertion uses
  one direct SQL `SELECT`, which is observational only.
- Guard refresh/caller authority: `_commit` supplies `authorize=lambda: None`.
  This is the existing direct-service test convention, but it is still an
  inline caller authorization hook and conflicts with this review brief’s
  explicit “no caller-inline-authority” constraint. Resolve that policy point
  before landing.
- Legacy literal `text/plain`: the positive path uses Runtime’s
  `TEXT_MEDIA_TYPE` (`text/plain; charset=utf-8`); the literal `text/plain`
  cases are negative MIME guards or belong to the retired legacy tests. They
  were not run by the failed native case and must not be claimed as positive
  legacy coverage.
- Unplaced target: the test keeps `shot:unplaced` refusal separate from the
  occurrence-owned capability and asserts no writes. The owner decision is no
  longer pending: the recorded 14:32/14:34 ruling approves existing
  project-catalog promotion outside accepted film history, with no new timeline
  carrier. The test/docstring/design wording that says “pending its owner” is
  stale, although the refusal remains a distinct capability and is not itself a
  replacement claim.
- Size: 278 lines, below the requested 500-line limit.

## Checks and limits

- `git diff --check efbbec2^ efbbec2`: passed.
- Reviewed worktree remained clean; no product source, shared dependency, or
  build output was changed.
- No full, broad, matrix, or shared-dependency test run was performed.
- The exact 11-case native qualification remains **unverified/blocked** by the
  captured-authorship schema mismatch.

## Recommended next step

Reconcile the Agent `text-binding.set` capture output with the approved ordinary
schema, then rerun the exact 11 marked cases against Runtime
`a0dca16975dfe8f5e762703b99d9791a16cf7fd7` / tree
`4b7dd0fe44be973c344bab3de568eaf0bdd28476`. Keep the unplaced refusal separate,
update the stale “pending owner” wording to the settled catalog decision, and
resolve whether direct-service authorization callbacks are allowed under the
no-inline-authority rule. Do not land on the prior `8023...` candidate merely
because its historical report said 11 passed.
