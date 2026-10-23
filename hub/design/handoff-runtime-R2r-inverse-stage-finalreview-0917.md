# Runtime R2r inverse-stage final review handoff

Result: **FAIL** on `430e2061c7958e2eccaa724c18638e8816f1596b` (`a01e9d806`
parent). Review-only; no product/test repair.

The prior `a744` provenance gap is addressed in the synthetic real-store
coverage: `history_entry(project, timeline, publication)` supplies authenticated
undo history; stage identity binds to exact `undo_of`, selected source step,
source command ordinal partition, fixed `parent` ref/policy/empty dependencies,
and contiguous reverse ranges. Stage images are derived from authenticated
effects and checked for exact native writes, exact effect before/after images,
physical refs, revision/content digests, and final output. The named Runtime
test accepts/replays one real-store seeded inverse and refuses 14 forged or
missing-history variants.

Blocking faithful-Agent result:

```text
CORRECTASTRID_CHECKOUT=/home/user/work/agent ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_acceptance.py tests/test_timeline_commit_integration.py -k 'inverse or history'
7 passed, 3 failed, 68 deselected in 9.85s
```

Failures:

- `test_real_inverse_preserves_newer_disjoint_work_and_original_recorders`:
  `inverse stage writes differ from its authenticated effect image` at
  `timeline_commit_auth.py:865`.
- `test_real_inverse_dry_run_and_exact_retry_write_only_the_undo_once`: same
  refusal at line 865.
- `test_real_track_create_and_inverse_keep_complete_film_closure`:
  `provider observation has an ambiguous item path` at line 867 through
  `_inverse_stage_state`.

Each test accepted its preceding actual Agent forward commit; inverse was
refused before durable inverse receipt/replay. The identical bounded selection
on an extracted `a01e9d806` tree was **10 passed, 68 deselected**, so this is a
regression introduced by `430e2061c`, not only the former missing-checkout
setup error. The likely repair seam is per-stage native/effect image
correspondence in `_inverse_stage_boundaries`; no repair was attempted.

Required named Runtime acceptance: **100 passed in 15.89s**.

Static review: auth and new-test Ruff clean; store Ruff has the exact parent
11 diagnostics. Current/parent Pyright auth/store diagnostic identities match
(zero auth, 76 pre-existing store diagnostics). `py_compile`, AST parse of all
three touched files, and `git diff --check` passed. Delta is exactly auth,
store, and the permitted new test; frozen contract/schema/client/pin/config
surfaces are unchanged. No full/HTTP/browser/live/native/crash/broad-Agent58
run was performed. Whole-inverse qualification is withheld.
