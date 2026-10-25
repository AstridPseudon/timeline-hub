# D116/G3 whole-path source-only validation

Verdict: `SOURCE_DEPENDENCY/EXACTMISSING`.

## Static checks

- AST parse and Python compile (venv-agent Python 3.11) passed for the current fixture, companion test, current source fixture, occurrence-delete implementation, word-anchor implementation, and command executor.
- Protected JSON evidence (`body-admission`, `facts`, `predicate-map`, `source-custody`, `source-verdict`) parsed successfully.
- Scoped Ruff passed:

  `RUFF_CACHE_DIR=/tmp/app-D116-native-gate3-wholepath-1800-ruff-cache /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py`

- Existing author-commit `git diff --check HEAD^ HEAD` passed.
- Worktree was clean before and after review; no files were modified.
- No pytest, collection, service, socket, browser, native body, or Gate3 rerun was performed.

## Exact source trace

The retained Gate3 selector prepares `occurrences == []`, appends `gate3-title`, mirrors `config.clips`, and then tests public checkout move/reload/undo plus unavailable visualize (`test_commit_runtime_native_checkout.py:71-131,248-299`). The current companion preserves those predicates at `test_native_checkout_current_equivalent.py:196-233` and adds current source/media/opaque topology in `native_checkout_current_fixture.py:25-74`.

The current companion's binding is authored by `current_pick(case, 1, text=DECLARATION)` and committed at `native_checkout_current_fixture.py:27-31`. Its exact choice is `occurrence:occ/clip:voice`, pinned to `case.pin`; the protected predicate map explicitly retains the picker index, declaration, pin, media, tracks, and opaque values.

Gate3 then calls `capture_occurrence_delete` at `native_checkout_current_fixture.py:91`. The helper executes the delete immediately for capture. `occurrence_delete` clears the selected occurrence (`native_occurrence_delete.py:9-24`); `commands.execute` invokes `compile_recorded` after the command (`commands.py:224-275`). Since the card's word anchor remains, `compile_recorded` calls `compile_authored` (`native_word_anchor.py:366-381`), whose binding finds zero placements after the occurrence is cleared (`native_word_anchor.py:67-76`, exact failure at line 71). The subsequent `clip.add` cannot repair a source that is already missing.

The current source fixture does have a genuine unanchored state: `current_form` first creates the current-form card, authenticates the exact anchor, then clears it and removes `word_anchors` before returning (`native_word_anchor_fixture.py:164-170,228-264,269-303`). However, `native_checkout_current_fixture.prepare` intentionally reintroduces the protected current picker/declaration binding before all companion topology and Gate3 setup. Omitting or clearing it would change the protected authored input; rebinding or inventing a replacement source/pin would violate source custody; removing the card is explicitly out of scope.

Therefore no exact fixture-only route exists under the settled source/predicate contract. The existing owner for any future supported semantic behavior is Agent G3/R2 (occurrence deletion versus relational word-anchor dependency); this review makes no product, compiler, guard, emitter, or test change.
