# Runtime shell integrated final gates

## Result

The independently approved shell repair `ff9d5c17bc75fb12b3293690a8d9acd8eded0db2` was merged by the manager as `b748ae723b51c6d578ba7a393209ce37d6e2b0c3` (`129493b` + `ff9d5c1`). The merged tree at qualification start was `1711b198be7f693f11ee4640eb0922ec0d0da952`.

No product, schema, pin, publication, or merge operation was performed by this worker. The worker worktree is clean.

## Focused integration evidence

Central targeted lane, against `integration:runtime` at `b748ae7` / tree `1711b198`:

```text
request-test integration:runtime targeted --files \
  "tests/test_bootstrap.py tests/test_timeline_empty_shell_repair.py \
   tests/test_timeline_headless_overwrite_refused.py \
   tests/test_timeline_commit_baseline.py"
runtime-targeted-1020130054-29879: 146 passed in 55.37s
```

This covers the unchanged corrupt duplicate-key refusal, absent/null/unpublished shell branches, strict baseline verification, headless refusal, and bootstrap neighbors. The public integration used the existing public schema; no init/schema override was installed.

The first diagnostic request accidentally targeted this worker’s pre-merge snapshot (`330ea396`); it passed 110 tests and is not used as integration evidence.

## Native/private qualification

The already-running native qualification was reused rather than duplicated. Its exact private evidence is:

- normal-generated private `0.2.14` full-S2-plus-init overlay only, with approved Agent `487ca1e0d74edf4aecdd2b4e045294ab089fc273`;
- central private cohort request `rt-m2-shell-native-final-qualification-targeted-1020125840-9634`: wrapper passed, child **23 passed**;
- separate named `commit-integration` request `rt-m2-shell-native-final-qualification-commit-integration-1020125919-4513`: **9 passed**;
- the cohort includes the unchanged real missing-head positive, absent/null repair durability, restart/edit/inverse/exact retry, actual-provider F1 historical-slot restore, and the nine existing commit cases.

This is private 014 qualification evidence, not a public 013 schema or release claim. No public generated artifact was changed.

## Source and preservation checks

`timeline_scope_is_empty` now reuses baseline `_json`, which rejects duplicate keys at every nesting level, escaped equivalents, non-finite values, overflow, and malformed JSON before bootstrap or persistence. Invalid legacy bytes return the existing refusal path and remain byte-for-byte unchanged.

The existing F1 projection guards and F2 shell-scope checks remain in place. `adopt_empty_shell` separately handles absent/null heads, refuses publication-bearing/unpublished-content and retained scoped data, and invokes the existing bootstrap only for the verified empty case. The native private cohort supplies the real provider/F1 proof; the public targeted lane supplies the public shell/parser neighbors.

The merge diff is limited to four expected paths:

```text
runtime_protocol/timeline_commit_store.py
tests/qualify_absent_head_repair.py
tests/test_timeline_absent_head_repair_integration.py
tests/test_timeline_empty_shell_repair.py
```

`git diff --check 129493b b748ae7` passed. All 38 current paths matching capture/text/render/triage/client were checked together and have identical Git blobs between `129493b` and `b748ae7`; no preservation hash mismatches were found.

## One permitted full suite

Request: `runtime-full-restore-integration-1020130236-16608`.

The request was queued at `13:02:36Z` with start snapshot `1711b198be7f693f11ee4640eb0922ec0d0da952`. Because another full suite occupied the central serialized slot, integration advanced before execution. The actual runner/final snapshot was `4cccb2d643194df7df95d624e89a6cd9f6f268fc`, commit `7f6dd8920e1ceec41b137358df5e7fecc304888d`. Drift from the queued start was three unrelated paths: `runtime_protocol/service.py` and two new journey/bootstrap test files.

Actual command and result:

```text
env ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-runtime/bin/python -m pytest -q -n 3

8 failed, 5533 passed, 18 skipped, 24 xfailed, 12 warnings
```

Classification against the exact prior full (`runtime-full-restore-integration-1020112501-27435`, tree `330ea396`, 7 failures):

- **Unchanged baseline (7):** the six named `tests/test_runtime_boundary.py` failures (`test_token_signal_exit_race_uses_only_retained_child_exit`, `test_unverifiable_live_owner_retains_cleanup_uncertainty`, `test_primary_start_error_retains_cleanup_uncertainty_as_cause`, `test_unowned_handle_does_not_infer_termination_from_poll`, `test_runtime_spawn_retains_owner_and_wires_escrow_before_seal`, `test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait`) and `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child`.
- **New, unrelated to this shell merge:** `tests/test_door_transport.py::test_audit_lines_without_credentials`. The failure is an audit-line count/unpack (`2` lines instead of `3`) on the drifted final tree. Neither the test nor door transport source is in the shell merge diff; the final-tree drift was a separate timeline service/test change. This is not evidence of a shell, parser, F1, or F2 regression and remains unverified independently.

No other new failure appeared. The prior baseline was `5491 passed, 18 skipped, 24 xfailed`; the changed final tree added unrelated tests, so counts are not directly comparable beyond node classification.

## Limits / next steps

The full suite is not green because of the seven known baseline failures and one unrelated transport failure on the drifted final tree. No browser/App workflow, public 014 release, pin, publication, ZIP, or macOS qualification is claimed here.
