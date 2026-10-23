# V4 early five-case proof report

## Result

FAIL (branch-only proof; not integrated DONE). The one permitted original-five
pytest invocation was run exactly once against the reviewed FPS+anchor
dependency branch and exited 1: `2 passed, 2 errors, 1 failed, 49 deselected`
in 5.67s.

The complete first output is preserved in
`native-word-anchor-original5.log` in this worker directory, including
`EXIT_CODE=1`.

## Exact test command

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k 'native_move_refuses_anchor_basis_until_explicit_clear or native_acceptance_refuses_review_source_counterexamples_before_writes or half_open_window_and_exact_rational_fps_are_validated_at_acceptance or stale_anchor_refuses_when_intervening_window_excludes_selected_word'
```

## Failure evidence

- Passed: `test_native_move_refuses_anchor_basis_until_explicit_clear` and
  `test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance`.
- Errors during fixture setup for
  `test_native_acceptance_refuses_review_source_counterexamples_before_writes`
  (`short-occurrence` and `raw-source-window`): Runtime validation raised
  `candidate.shots['shot'].internal_timeline.clips['voice']: timeline interval
  must fit the occurrence's half-open bounds`.
- Failed during setup of
  `test_stale_anchor_refuses_when_intervening_window_excludes_selected_word`:
  Runtime rejected `trim-before-anchor` with
  `candidate.timing: legacy word anchor is missing`.

The dispatch required stopping on this failure. No source/test repair and no
pytest rerun was performed. Scoped Ruff and `git diff --check` were not run
after the failure because the dispatch says to stop/report the exact trace.

## Changes and verification

Only the two permitted reviewed blobs were imported:

- `tests/editing_conformance/native_word_anchor_fixture.py`
- `tests/editing_conformance/test_native_word_anchor.py`

Original worktree blob IDs:

- fixture: `ce3f06bbaeedeea805a82bde35035621cf4a0d42`
- test: `d90b21c3378c55e32bc7a43fa6436ed5ec655afa`

After import, blob IDs exactly match commit `5292b388a271b9ba07c4344a1072963109b2c9f9`:

- fixture: `af7407a5a2d42bb63b5cc11ba4a4924d3186c607`
- test: `5db819f485da679f613ef04455ec19708d316d6a`

`git diff 5292b388a271b9ba07c4344a1072963109b2c9f9 --` for those two files
is empty. The final worktree diff names only those two files.

Preflight confirmed HEAD `ad4e459a32d9abbbe28794fb13ef45b1b9cd6893`, the exact
Runtime checkout `ad823e0a0f5be4a7acf1d3006df6f794709da63d`, and recipe ref
`f894c3c9dda25ab03527eeb7f52da5da31d627c1`. The requested prior research
directory was absent in this environment, so that evidence was unavailable.

## Limits and next steps

This is branch evidence only. It does not qualify integration, native/browser
or full suites, and it does not request merge. The observed setup failures need
orchestrator review against the supplied Runtime pin and the settled plan;
this worker made no attempt to diagnose by changing behavior.
