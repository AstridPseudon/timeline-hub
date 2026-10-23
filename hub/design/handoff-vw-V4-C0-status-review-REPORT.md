# V4 C0 expected-status review

## Result

**PASS** — narrow negative-status adaptation only.

Reviewed `5292b388a271b9ba07c4344a1072963109b2c9f9` against parent `38e8063162a36a87369561c581bc18fe8fbef37c` (the exact 38e base), PLAN §3 V4, approved C0 §4, and the two required handoff reports.

The commit changes only `tests/editing_conformance/test_native_word_anchor.py`, with exactly three assertion-line edits covering four cases:

- `short-occurrence` and `raw-source-window`: `refused` → `invalid`.
- Acceptance-time half-open/rational source window: `refused` → `invalid`.
- Stale anchor after an intervening window narrowing: `refused` → `conflict`.

The diff contains no source, fixture, recipe, generated, pin, package, manifest, or unrelated test/assertion edits. No broader accepted status was introduced.

## Evidence

Preserved in the diff and targeted execution: every reason and message assertion; no-write, unchanged-head, unchanged-history, and direct-recorder guards; other counterexample parameter cases; positive boundary/restart/undo behavior; equal-text undo positives; all rebase/body assertions; and the latent merged-status assertion remains unchanged.

Independent targeted run (the only requested semantic run):

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k 'native_acceptance_refuses_review_source_counterexamples_before_writes or half_open_window_and_exact_rational_fps_are_validated_at_acceptance or stale_anchor_refuses_when_intervening_window_excludes_selected_word'
....                                                                     [100%]
4 passed, 50 deselected in 3.90s
```

Additional checks:

```text
ruff check tests/editing_conformance/test_native_word_anchor.py
All checks passed!
git diff --check HEAD^ HEAD
PASS
```

Typecheck: N/A; only test expected-status strings changed.

## Decisions and limits

No new decision was made; the settled C0 mapping was applied exactly. The production caller remains the actual native provider through Runtime; no mock or alternate port was used. No full54/native14/full/browser/heavy suite was run. The three residual issues documented by the diagnosis report remain unresolved (two undo C0-scope tensions and one real-replay metadata defect); this review does not claim V4 completion or overall-54 PASS.

No blocker remains for the narrow independent review. The worktree was read-only and clean after verification.
