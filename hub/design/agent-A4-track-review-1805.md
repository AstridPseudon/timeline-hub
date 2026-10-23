# A4 track doc.patch witness review — PASS

## Scope and verdict

Reviewed Agent commit `4010f98760b43e2320f6207bc1f59789bf636b21` (`test_a4_track_doc_patch_witness.py`) against PLAN §3 A4, R1/C0, and the reviewed App donor `68594c668`.

Verdict: **PASS for the bounded nine-case A4 witness**. The file is test-only, adds exactly nine collected cases (seven test functions, one parametrized three ways), and preserves the existing fixture and provider helpers. No product, App, Runtime, Git, environment, daemon, or deletion changes were made.

## Source fidelity

- The Agent fixture `tests/editing_conformance/fixtures/recipe_m2_app_track_label.json` is byte-identical to the current App fixture (`sha256 5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00`). The witness builds the donor's three-row case: existing `picture` plus `audio` and `overlay`.
- Current App A2 sources are byte-identical to donor `68594c668`:
  - `documentPatchIntent.ts`: `5e1b1d1e2cd95ac7e402daf0ac9f4f4cf1ec606f`
  - `localSaveSession.ts`: `83d2166d57c05980d3bd8ebc9bbd79a37c3c5e44`
  - `trackReorderCapture.ts`: `81ec771ab972da61654b96e45caa9506e8a797e7`
  - `recipe_m2_app_track_label.json`: `b79b69f9a95b8df417c7b157f0db92eb803535e3` (Git blob; content hash above)
- The reviewed App hook-test donor adds the 97-line mounted block in `68594c668`; the current integration hook-test blob is its parent (`7c34989fc99cc75d3a7bf40517688546f2d052e4`). I therefore classify this as **exact coverage of the reviewed donor behavior**, not as evidence that the donor block is currently mounted. The witness does not claim to execute the App hook, HTTP, or a live Runtime.
- The expected emitted move matches the donor/current A2 encoder: `op=list.move`, `ref=parent`, `path=["config","tracks"]`, `id=overlay`, complete `before` row, `order_before=["picture","audio","overlay"]`, and `after_id=null`. The witness's step patch is the same ordered change list.

## Coverage

- Detached execution is immutable, JSON round-trippable, replayable, and does not write the source bundle.
- The three-row recipe preserves selected row data and JSON values including explicit `null`, `false`, `0`, nested opaque values, and app/parent opaque fields.
- The provider-call boundary covers preview (`status=preview`, `receipt=None`, unchanged head), accepted canonical output, base revision/publication pair, label and merge mode, authoritative step patch, read dependency persistence, command shape, and empty `created` claims.
- Bad previous value, stale collection order, and missing anchor are invalid and leave head, entries, and documents unchanged.
- Duplicate collection identity is refused before mutation; a forged occupied `created` claim is refused.
- A membership change and an order A→B→A both refuse with `selection_changed` and no stale-write mutation. A disjoint neighbor-field edit merges while preserving that field.
- Public-provider naming refers to the detached provider-call interface only; no HTTP or mounted-App claim is made. The dormant `track.reorder` envelope/revive operation is not required or exercised.

## Limits / uncovered by this witness

- This is not a mounted App, HTTP, or live Runtime proof, and it does not qualify `localSaveSession` restart/lost-ack/dependent-outbox behavior; those remain A2/P1 scope.
- It does not assert every complete C0 wire/reply field. In particular, full receipt authentication fields, command bindings/effects, complete dependency records, history/undo-step exposure, preview `would_status`, and structured errors are not re-proven here. The test only asserts the C0 fields directly relevant to this A4 patch witness; existing C0/provider suites remain the authority for the rest.
- The moved row and neighbor opaque values are asserted, but the `picture.extension.clear` value from the recipe is not independently asserted by a field-specific expectation.
- The provider reports the legacy success spelling `rebased` for the disjoint merge case. This matches the current Agent detached harness and is not a claim that a new v2 Runtime response should use the plan's `merged` spelling.

## Commands and results

Initial direct run lacked the Runtime source on `PYTHONPATH` and stopped during conftest import with `ModuleNotFoundError: runtime_protocol`; no test cases ran. Re-run with the repository's read-only Runtime source exposed:

```text
PYTHONPATH="$PWD:/home/user/work/venv-agent-child-f1012-installed/source/runtime" /home/user/work/venv-agent/bin/pytest -q tests/editing_conformance/test_a4_track_doc_patch_witness.py --timeout=25
.........                                                                [100%]
9 passed in 2.04s
```

```text
/home/user/work/venv-agent/bin/ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/editing_conformance/test_a4_track_doc_patch_witness.py
All checks passed!

/home/user/work/venv-agent/bin/mypy --no-incremental --follow-imports=skip --ignore-missing-imports tests/editing_conformance/test_a4_track_doc_patch_witness.py
Success: no issues found in 1 source file

git diff --check 4010f9876^ 4010f9876
passed
```

No broad/full/browser/HTTP/seed/native/P1/P4/SDK or unrelated suite was run. The worktree remained clean after review.
