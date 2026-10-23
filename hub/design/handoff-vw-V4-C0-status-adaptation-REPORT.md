# V4 C0 status expectation adaptation report

## What changed

Changed only `tests/editing_conformance/test_native_word_anchor.py`.

- The parameterized `short-occurrence` and `raw-source-window` cases now expect `details.status == "invalid"`.
- The acceptance-time half-open window case now expects `details.status == "invalid"`.
- The stale-anchor replay after an intervening window change now expects `details.status == "conflict"`.

This is the narrow C0 expectation migration approved for the four original negative cases. The shared parameterized assertion accounts for two cases; there are three changed assertion lines for four cases total.

Preserved unchanged: all `reason` and message matching assertions; no-write, unchanged-head, unchanged-history, and direct-recorder guards; both equal-text undo positives; all rebase/body assertions including the latent rebased expectation; all other counterexample parametrizations; and all positive cases. No fixture, recipe, provider, Runtime, source, schema, generated, pin, manifest, or product file was changed.

## Verification

Targeted command (run once after the edit):

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k 'native_acceptance_refuses_review_source_counterexamples_before_writes or half_open_window_and_exact_rational_fps_are_validated_at_acceptance or stale_anchor_refuses_when_intervening_window_excludes_selected_word'
```

Result: `4 passed, 50 deselected in 3.80s`.

Lint and whitespace checks:

```sh
ruff check tests/editing_conformance/test_native_word_anchor.py
git diff --check
```

Result: Ruff reported `All checks passed!`; `git diff --check` passed. Typecheck is not applicable: this change only adapts expected status strings in tests.

## Decisions and status

The diagnosis and approved C0 mapping establish base-invalid failures as `invalid` and later-head stale replay as `conflict`; no production behavior was changed. No decisions beyond that settled mapping were needed. No full, browser, native14, heavy, or overall-54 suite was run, per task scope. No blocker remains for independent review and home merge after the targeted PASS.

Evidence log: `targeted-pytest.log`; command copy: `targeted-pytest.command` in this worker directory.
