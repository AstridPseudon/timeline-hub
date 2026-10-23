# G4 held-image independent review

## Verdict

**PASS for the bounded G4 acceptance, with the inverse journey explicitly OPEN.**

The source port admits literal `clipType: hold` only when the authenticated
verified media kind is `image`; video hold remains refused. The current-Runtime
fixture independently proves authentic image ADD and SWAP acceptance on Runtime
`9345cb58fe8c54f114d666929e167bbeb5899c6c`, plus the current video-hold
negative. This is not a blanket G4/P2/P3/whole-suite verdict.

## Independent evidence

- Compared `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c` to
  `8eb98564075b7c084f00c29d5746f15ab36365a6`: only
  `native_occurrence_media_commands.py`, the new
  `test_occurrence_hold_current_runtime.py`, and the scoped recipe test
  changed.
- The source delta is four lines in `_clip`: `hold` is admitted only for
  `kind == 'image'`; all existing timing, source-window, ownership, selection,
  and registry guards remain.
- The recipe suite retains the original image/video ADD/SWAP capture/replay,
  inverse, refusal, foreign-binding, membership/order, media identity, and
  history/undo assertions. New image-hold tests preserve the literal row,
  `hold`, raw opaque/null/absent distinctions, and inverse.
- The new fixture uses one real `RuntimeService`, public project/timeline
  genesis, real `import_media`, exact public selection and verified-media reads,
  the registered current Agent provider, and production commit calls. No
  retired publish route, fake provider, private closure, read cache, guessed
  media identity, or admission bypass is used.
- ADD and SWAP each pass dry-run no-write, accepted canonical equality,
  selection/verified-media equality, physical ownership/dependency retention,
  full canonical document/records/history capture, and local authenticated
  inverse restoration. The video-hold control returns Runtime 422 and leaves
  history and the database unchanged.
- Durable evidence: `workers/agt-G4-held-image-current-1240/evidence/`
  (`current-held-image-add.json` and `current-held-image-swap.json`). The
  evidence records Runtime/Agent module origins, request base pair, commands,
  v2 step/records, bindings, effects, histories, and before/after canonical
  digests.

## Checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-9345cb58 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9345cb58 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_occurrence_hold_current_runtime.py tests/editing_conformance/test_recipe_occurrence_media.py` — **70 passed in 16.01s** (4 current-Runtime, 66 recipe).
- `RUFF_CACHE_DIR=/tmp/w-08f2d645e5/ruff-cache make PY=/home/user/work/venv-agent/bin/python ruff` — **2149/2149**.
- `TMPDIR=/tmp/w-08f2d645e5 MYPY_CACHE_DIR=/tmp/w-08f2d645e5/mypy-cache make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — **1912/1912**.
- `scripts/artifact_manifest.py --check` — passed.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — passed.
- `git diff --check` — passed.

## Open boundary

The test’s Agent-owned local authenticated inverse restoration passes. The
exploratory Runtime inverse remains the previously classified 422
`invalid_records` native/effect-coverage refusal; this review neither waives
it nor claims Runtime inverse completion. Runtime owner 1233/R2 remains the
owner of that journey. No full, browser, P2/P3, or unrelated suite was run.
