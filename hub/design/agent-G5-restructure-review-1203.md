# Independent G5/G4 review — `ee7f0b809`

## Verdict

**PASS — bounded correctness/security/fidelity review.** This is a draft-only
review: PLAN §3 P1 is still NO-GO, so no integration merge is requested or
authorized. Broad guarded undo/redo, browser/render, HTTP, full P1/P4 and
integration qualification remain unverified.

## Identity and scope

- Candidate: `tl/agt-G5-restructure-1137` / `ee7f0b809`
- Base: `d1fa6c133`
- Candidate tree is clean and changes exactly five paths:
  `_command_state.py`, `commands.py`, new `native_restructure.py`,
  `publish.py`, and `tests/sdk/test_timeline_restructure.py`.
- Runtime was not moved or modified. The real Runtime used by the witnesses
  was `/home/user/work/runtime`, commit
  `3b926efab2eed122d374540baee297d4cdcec62a`, tree
  `b794170504544b259781e50d7ca4d61b6729e67c`.
- Import origins in the same process: Agent command/native/CLI modules came
  from `/home/user/work/wt/agt-G5-restructure-review-1203`; `runtime_protocol`
  came from `/home/user/work/runtime`.

## Independent behavioral evidence

Command (real current Runtime service/provider, private basetemp):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= \
-p no:cacheprovider --basetemp=/tmp/w-5f85cff4a7/g5-review-focused/basetemp \
tests/sdk/test_timeline_restructure.py::test_the_renderer_gets_the_same_input_before_and_after \
tests/sdk/test_timeline_restructure.py::test_round_trip_flat_to_stored_to_flat_and_back_keeps_everything \
tests/sdk/test_timeline_restructure.py::test_split_stores_chapters_as_shots_and_music_and_crossers_on_the_film \
tests/sdk/test_timeline_restructure.py::test_cli_restructure_commits_the_complete_equivalent_bundle_and_followups \
tests/sdk/test_timeline_restructure.py::test_restructure_retries_the_original_commit_after_lost_ack \
tests/sdk/test_timeline_restructure.py::test_restructure_reconciles_narration_without_republishing_the_cut \
tests/sdk/test_timeline_restructure.py::test_restructure_provider_refuses_changed_inputs_without_writes \
tests/sdk/test_timeline_restructure.py::test_restructure_reuses_an_existing_chapter_root \
tests/sdk/test_timeline_restructure.py::test_restructure_retries_narration_before_a_flight_exists \
tests/sdk/test_timeline_restructure.py::test_restructure_order_carrier_only_permutes_unchanged_rows \
tests/sdk/test_timeline_restructure.py::test_restructure_provider_preview_has_no_writes
```

Result: **17 passed in 101.49s**. The parameterized refusal test supplied the
seven actual Runtime/store witnesses: foreign project, changed before-state,
created-order mutation, forged identity, caller media, occupied ID, and stale
closure. Each asserts unchanged document, history, and SQLite dump. The same
run passed the three restored original cases: complete equivalent bundle and
followups, narration reconciliation without republishing the cut, and exact
original request/key retry after lost ACK. It also covered accepted-cut
recovery, narration failure/recovery with one transcript, preview
`would_status` with no writes, root reuse, renderer-input equivalence, and
placement/order/identity/media/null/absence preservation.

An additional read-only carrier witness accepted a reversed permutation of the
complete current rows. The test suite's carrier negatives reject membership,
content/identity, and false-versus-zero changes. The provider tests exercise
foreign, occupied, and stale protections through the public Runtime service,
not fake admission alone.

## Path and contract review

The production path is intact:

```text
cli_working._cmd_restructure
  -> Checkout.publish(restructure=True)
  -> _commit_restructure
  -> TimelineSession.submit(..., merge="atomic")
  -> native timeline.restructure provider operation
```

`timeline.restructure` is registered in the existing native operation registry.
The command has an empty, closed argument schema; the handler derives the cut
from the authenticated current closure, checks project/timeline/base-parent
identity, runs the existing split/equivalence logic, and uses the existing
recorder for allocations and writes. The order carrier accepts only a
permutation of complete unchanged rows. No executable source-image claim,
managed-edge patch, second executor, synthetic journal/prepared acceptance,
fake authority, or generic `three_way` copy was found in the new,
registration, or carrier production paths.

The focused accepted/preview/recovery witnesses and the unchanged protected
transport/schema files cover the v2 request/reply shape: label, steps and
patches, reads and ordinals, atomic merge, base pair, idempotency key,
dry-run/source/rationale/group ID, accepted/merged data and receipt,
canonical document/records/dependencies/effects/history/undo steps, preview
`would_status`, conflict head/reason, and invalid code/path/hint/command.
The candidate diff changes no schema, generated client, Runtime pin, or
commit/result implementation outside the five listed paths.

The ordinary non-restructure `publish_bundle`/legacy three-way path remains in
the existing publisher by design for this draft; it was not counted as a
claim that all G5 deletion work is complete.

## Quality and integrity checks

Executed independently on this tree:

- normal Ruff: **2149/2149**, baseline clean;
- required scoped Ruff (`native_restructure.py`, `_command_state.py`,
  `commands.py`): **pass**;
- private mypy: **1912/1912**, baseline clean;
- vendor lock against `/home/user/work/wt/rt-pin-34eac004`: **pass**;
- artifact manifest: **pass**;
- `git diff --check d1fa6c133 ee7f0b809`: **pass**.

For transparency, an extra broader ad hoc Ruff invocation over all changed
source/test files reported four diagnostics: the pre-existing publisher import
ordering and `E741` at `publish.py:511`, plus two import-order findings in the
new fixture imports. That was not the requested scoped gate and no files were
edited during this review.

The author’s exact 109-case selector was **reused**, not rerun, because this
tree is byte-identical to the author evidence after the final carrier change:
the durable author report records **109 passed, 5 deselected in 100.53s**.
The five excluded nodes were collected by exact name and not executed:

```text
test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter
test_duplicate_guard_refuses_a_copy_that_collapses_shots_and_keeps_a_repeated_shot_repeated
test_duplicate_refuses_when_the_wrong_form_of_the_source_is_copied
test_duplicate_commit_keeps_a_repeated_shot_shared
test_duplicate_preflights_and_publication_are_core_only
```

No duplicate D17, full, browser, render, P1/P2/P3/P4 HTTP, native14/58,
daemon/shared-install, generated/pin/dependency, Git, or product/test edit was
performed by this review.

## Next step

Keep the candidate draft-only. Integration remains gated on the orchestrator's
P1 GO; after that, requalify the integrated heads and separately qualify the
broader guarded undo/redo and remaining G5 deletion scope.
