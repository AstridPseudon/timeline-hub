# D115 Runtime security/core review: PASS

Reviewed exact author commit `274bbf7d73c543d72058ce3563eba2af5cdc4bd1` on
the clean review worktree. The diff is exactly the authorized two files:
`runtime_protocol/timeline_commit_auth.py` and
`tests/test_timeline_intermediate_image_auth.py`. No product, existing-test,
store, port, pin, generated, registry, or upstream files were changed.

## Verdict

PASS for the requested Runtime source/security review, with the two known
baseline exclusions below. The candidate uses the already authenticated
landing output for each step's `step_output` projection, while retaining the
prepared canonical document as the final transaction endpoint. It does not
invent an effect for empty `media.admit`, and the existing ordinal, source,
closure, owner, pin, ordering, and mutation guards remain in the unchanged
authenticator/verifier path.

## Evidence

- Exact immutable Agent provider: `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`,
  clean checkout `/home/user/work/wt/agt-pin-070dfc5e`; provider origin was
  inside that checkout and provider id was `astrid-v1`.
- Candidate exact regression: 5 passed, no skips.
- Exact parent auth source (`d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e`)
  with the same Agent and exact test file: 1 genuine RED at
  `provider intermediate parent lacks an effect image`, plus 4 strict
  forgery refusals passed.
- Real native-provider smoke: the two mandated selectors executed, 2 passed,
  no skips/deselections.
- Strict source/effect/step/native/inverse neighbors: 321 passed, 74 default
  integration/live tests deselected.
- Authentication integration lane: candidate 39 passed, 1 failed out of 40;
  exact parent reproduced the same failure and message
  `sequential original or landing input does not match its authenticated
  head`. This is not caused by the two-line projection change.
- Sequential verifier: candidate 66 passed, 1 known excluded case failed;
  exact parent reproduced the same failure. The excluded case constructs a
  `TimelineCommitStore` from a `SimpleNamespace` without the required
  `db_path`.
- Ruff `--no-cache`, Pyright, compileall, `git diff --check`, release-smoke
  control test, bash syntax, and smoke-test Ruff/compile all passed.

## Security trace

`validate_sequential_capture` authenticates the captured command boundaries
and the landing output before `validate` receives them. `validate` checks each
captured input against the Runtime-computed ordinal input, passes only that
step's captured last output as `authenticated`, and compares the resulting
projection back to the capture. `step_output` uses that authenticated closure
for image alignment/reconciliation; it does not use a later final candidate
as authority for an earlier step. Effect ordinals remain range-checked by the
unchanged `_capture_records` path, and the new forgery cases for image,
ordinal, changed pin, and wrong owner all refuse without writes.

## Scope and next steps

This is a source/security PASS, not a claim that the two known pre-existing
integration/verifier failures are fixed. The orchestrator may merge the exact
author commit after recording those baseline-identical exclusions and the
required smoke evidence. No implementation edits were made by this review.
