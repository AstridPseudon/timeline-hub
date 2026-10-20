# Agent admission flight discriminator fix

## Result

Fixed only P2 strict local outbox flight discrimination on the reviewed
`tl/agt-m2-assembly-admission-durable-flight` candidate.

`TimelineSession._state()` now validates the persisted flight discriminator
before any state mutation or transport dispatch. A missing `kind` remains the
legacy commit-flight format. The only recognized present tag is
`assembly-admission`; present `null`, booleans, numbers, `commit`, and unknown
strings fail closed with `TimelineEditError`. The existing admission, flush,
undo, staging, and reload paths all use this validation gate. Invalid flights
retain their exact outbox bytes and retry identity; no alternate transport is
attempted.

No public DTO, schema, journal, authority rule, credential behavior, or
`outbox.py` behavior changed. The explicit `commit` value is rejected because
this candidate documents no explicit commit tag: legacy commits are identified
by an absent tag, as required by the review finding and retained probes.

## Files

- `astrid/sdk/timeline/sync.py`: strict discriminator helper and guarded path
  checks.
- `tests/sdk/test_timeline_sync.py`: regression for `null`, `false`, numeric,
  `assembly-admission-v2`, and `commit` tags on a valid lost-ACK commit flight;
  asserts refusal, exact-byte retention, and no second POST.

## Tests and checks

All commands ran from `/home/user/work/wt/agt-m2-admission-flight-strict-tag`
with the shared Agent virtualenv read-only and pytest cache disabled.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/packs/rendering/test_runtime_stitch.py tests/packs/rendering/test_assemble_timeline.py
138 passed in 21.49s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sheet_native.py
70 passed in 4.96s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/assembly.py astrid/sdk/timeline/sync.py tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py tests/packs/rendering/test_registered_assembler_admission.py tests/packs/rendering/test_registered_native_pair.py
All checks passed!

git diff --check
passed
```

The requested old producer paths
`tests/sdk/test_timeline_producer_guard.py` and
`tests/editing_conformance/test_producer_insertion.py` do not exist in this
checkout (the attempted command exited 4 before collecting tests). The current
registered producer coverage is included in the private central wrapper.

Because this changes real admission-flight dispatch, the named central wrapper
was run once:

```text
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
$ORCH/bin/request-test agt-m2-admission-flight-strict-tag identity-pin94114269-integration --files tests/packs/rendering/test_registered_native_pair.py
$ORCH/bin/wait-test agt-m2-admission-flight-strict-tag-identity-pin94114269-integration-1020133741-30684
test ...: pass exit=0 in 227s
15 passed, 2 xfailed in 187.42s; outer 4 passed in 215.30s
```

No full/full* suite, browser, live-socket local run, or shared dependency
mutation was performed.

## Handoff

The harness should commit the worktree using the conventional message in the
worker commit-msg path. No git commit, merge, rebase, checkout, push, or
integration-worktree edit was performed. Next step is normal merge-queue
composition of this two-file narrow delta.
