# R1 independent review: PASS (conditional)

Candidate reviewed: `b7a32c523` (`tl/agt-R1-membership-current`), with parents
`7bf5f7bca` (current-forward) and `e6f7167d6` (reviewed membership precedence).
The merge base with integration `cf31566e8` is `e6f7167d6`; the current-forward
parent is an ancestor of the candidate. `git diff 7bf5f7bca..b7a32c523` has
only the approved two files: a three-line guard-order change in
`astrid/sdk/timeline/_commit_patch.py` and 40 conformance-test lines.

The collection guard is now checked before removed-member field guards, so stale
membership/order changes report `selection_changed`; same-field edits retain
`value_conflict`, and atomic mode retains `atomic_scope_changed`. The existing
physical successor proof, mirror normalization, alias continuation, declared
collection reads, and no-write behavior are unchanged. Blob audit also found
the current U2/U4a client/schema, P1 vectors, V4, and quality baselines identical
to `7bf5f7bca` (apart from `_commit_patch.py` and its new tests).

## Tests

All commands used the locked Runtime `27f0306b94d136d25f237edf4b8225b5d8487be0`
via `PYTHONPATH` and disabled pytest's shared cache:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-27f0306b" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_doc_patch_v2.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/editing_conformance/test_recipe_m1_commands.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-membership-precedence/original-p1/test_p1_doc_patch_provider.py::test_provider_refuses_stale_same_field_membership_and_order
result: 353 passed in 80.63s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-27f0306b" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p1_case_corpus.py tests/sdk/test_p1_doc_patch_requests.py
result: 25 passed in 6.78s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-27f0306b" /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_doc_patch_v2.py
result: All checks passed

MYPY_CACHE_DIR=/tmp/agt-r1-current-review-mypy PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-27f0306b" /tmp/astrid-u2-typecheck/bin/python -m mypy --follow-imports=skip astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_doc_patch_v2.py
result: Success: no issues found in 2 source files

RUFF_NO_CACHE=true PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-27f0306b" make ruff PY=/home/user/work/venv-agent/bin/python
result: current=2151 baseline=2151

MYPY_CACHE_DIR=/tmp/agt-r1-current-review-private-mypy PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-27f0306b" make mypy PY=/tmp/astrid-u2-typecheck/bin/python
result: current=1915 baseline=1915
```

The unchanged original membership/same-field/order controls passed inside the
353-test run. I also attempted the complete preserved
`test_p1_doc_patch_provider.py` corpus from a private temporary fixture overlay:
it produced 3 passed / 10 failed. The failures are historical-corpus issues,
not the R1 membership regression: one current canonical mirror output differs
from the old expected fixture, and the service cases hit the old test-provider
`runtime_protocol` stub/schema boundary. I report this as non-green original
wire evidence rather than hiding it; the focused original membership control is
green.

## Contract/wire qualification

The provider's production caller reaches `rebase_patch` from `commit.py:1058`
and preserves the full `{data, receipt}` result. Full mounted Runtime DTO/wire
acceptance is not verified here and remains conditional on Runtime R2r. The
current-forward generated client still has pre-R2r wire gaps:

* `astrid_runtime_client/timeline_commit_types.py:70` does not type v2
  `steps`, `merge`, or `reads` (and makes `label` optional).
* `timeline_commit_types.py:88` and generated client validation accept only
  `accepted`/`rebased`; `generated.py:948` rejects new `merged` replies.
* `astrid/sdk/timeline/sync.py:114` likewise rejects `merged`, and
  `sync.py:432-435` emits the legacy request body without v2 `label`, `steps`,
  `merge`, or `reads`.

These are preserved baseline/Runtime-R2r integration findings, not introduced
by `b7a32c523`. Therefore this is a source PASS conditional on the coordinated
Runtime R2r and regenerated DTO/client adoption, not an unconditional wire-green
claim. No product files were edited by this review.
