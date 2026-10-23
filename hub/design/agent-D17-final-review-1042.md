# D17 final Luna review — PASS (scoped)

Date: 2026-10-23

## Verdict and source boundary

**PASS for the cumulative D17/R1 normalizer and authenticated source-copy slice.**
This is not a P1, G5-retirement, full-project, original58, native14, HTTP,
browser, journey, or installed-environment qualification. G5 remains gated by
P1 as required by the plan; the legacy writer paths remain present.

The reviewed candidate is:

- Agent commit `d57207fb5e4a55be70ffe953c6b8b5604e893502`, tree
  `0cc5c761099494b0bf80699aeb25ab733e961dbd`.
- Current Agent integration base `tl/integration` at
  `7abfb8d69f625d0aada79346d5806f5f9525ed8c`, tree
  `9618a0928a361eca8f172e0bf56a1ae5d0e472fa`.
- Cumulative D17 commits audited: `80680fab5`, `f209b0455`, and
  `d57207fb5`; the cumulative commit-union is 24 paths. The net candidate
  delta against current integration is 12 paths, including all effective
  product and test changes.
- Runtime authority is the unchanged detached pin
  `1365e4b17b31c4a7093d5943674637067fd2bab4`, tree
  `6c69c3dc47822fffbaf27cd63815d2895155ffaa`, with clean status.

No cumulative diff changes contract, generated/client, Runtime lock, pin,
environment, Runtime service, or Composition files. The normal34e/generated
surface is outside this D17 delta and was not modified. No source, test, pin,
contract, environment, service, or shared dependency was changed by this
review.

## Evidence

The final-40 selection, using the exact report test selection and a private
basetemp (the report-only `evidence` pytest plugin is unavailable in this
worker venv), passed:

```text
40 passed in 14.67s
```

The inverse-281 selection passed:

```text
281 passed in 28.76s
```

The exact commands, with only `-p evidence` omitted because that plugin is not
installed here and with the unavailable old basetemp replaced, were:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1:/tmp/w-e409539a14 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1 /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/agt-D17-final-review-1042/pytest-author tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared tests/editing_conformance/test_commit_runtime_source_copy.py tests/editing_conformance/test_recipe_timeline_source_copy.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1:/tmp/w-e409539a14 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1 /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/agt-D17-final-review-1042/pytest-inverse tests/editing_conformance/test_doc_patch_mirrors.py tests/editing_conformance/test_inverse_clip_mirrors.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_grouped_clip_cache_inverse.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_recording_clear.py
```

The two original duplicate test functions are AST-exact against the pre-
normalizer `80680fab5` tree, including assertions. The final-40 inventory
therefore covers the required raw-parent four combinations, repeated sharing,
canonical/opaque/order/membership preservation, fresh IDs, idempotency,
lost-ACK/retry, restart, archive cleanup, media/document custody, and all
required negative cases: forged media, foreign/outside source, stale capture,
occupied IDs, order/sharing claims, inverse/ABA guards, and retained-input
fail-closed behavior.

Quality and hygiene gates:

```text
make PY=/home/user/work/venv-agent/bin/python ruff        PASS: current=2149, baseline=2149
make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy  PASS: current=1912, baseline=1912
ruff check --no-cache <eight scoped files>                PASS
scripts/vendor_lock.py check runtime.lock.json            PASS: ok
scripts/artifact_manifest.py --check                      PASS: current
git diff --check; git diff <current-integration> --check  PASS
```

The saved same-process origin evidence records the Agent/Runtime module
origins and hashes before/after the source-copy run. The Runtime pin remained
`1365e4b17b31c4a7093d5943674637067fd2bab4` with empty status. Current hashes
also match the recorded Agent `commit.py` (`741e8afc…`), Runtime port
(`30dc4087…`) and Runtime authority (`bb7307e6…`) artifacts.

## Authority and implementation audit

The production path is still `duplicate_timeline -> _duplicate ->
_commit_bundle -> session.submit`, using the existing durable carrier and one
`timeline.duplicate` semantic command. `_source_reference` selects the exact
accepted publication from source history. The provider-side resolver obtains
the closure only from Runtime's private `revision_closure(source_ref)` port,
hydrates its declared media/document inputs, and checks the returned project,
timeline, revision, and digest. Runtime's unchanged source port separately
validates the exact five-field reference, source access, publication pair,
digest, and captured inputs before acceptance. `physical_content` derives
physical roots only from the authenticated Runtime document; it is not a
second source authority or a guessed cache.

The normalizer preserves raw parent `clips`/`registry` presence by using a
complete parent effect when topology changes, while retaining alias effects
when topology is stable. Repeated shared roots are normalized only through
authenticated source links and exact payload/internal images; changed aliases
raise an inverse conflict. Retained media/document deltas are reversed only
for complete accepted root records with exact loaded boundaries. Existing
aggregate/leaf, order, membership, history, surviving-consumer, ABA, and
Runtime guards remain in force. No native writer, scope guard, aggregate-leaf
guard, physical-normalization guard, history guard, or ABA assertion was
relaxed.

## Known baseline failure and limits

The explicitly requested representative legacy shared-slot test was rerun
against the candidate:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1 /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/agt-D17-final-review-1042/pytest-legacy-current tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_slot_move_inverse_redo_and_rematerialization
```

Result: **2 failed**, parameterizations `original-third` and `authored-first`.
Both fail on the first move, before inverse, with
`timeline interval must fit the occurrence's half-open bounds`. The saved
corrected private baseline-overlay replay has the same two failures and the
same causal validation error. This is reported as a pre-existing baseline
timing issue only; the other eight exploratory failures are not relabeled as
baseline-proven, and no whole58/full/journey suite was run.

The scope also does not newly qualify historical `rebased` behavior, arbitrary
mixed inverse/schema batches, process-kill recovery, archive-operation failure,
or P1/G5 writer retirement.

## Recommendation

Accept this scoped D17 review and integrate through the Agent queue. Keep the
P1 gate and legacy writer deletion decision with the orchestrator. Investigate
the shared-slot timing baseline in its owning lane before claiming the broader
inverse or project qualification.
