# R1 inherited declarations correction — 0137

Implemented against Agent `fa2cf5b6642384ec1ce77dee64b733d585c6308a` in
`/home/user/work/wt/agt-R1-inherited-reads-sol-0137`. Scope is PLAN §3 R1 and
commit-v2 §§1/3, including the inherited dependency and sequential boundary rules.
Read the independent 0129 triage finding 2 and its peer report from the
orchestrator's design directory before changing code.

`commands.execute` now holds the request/step reads captured by
`CommitPatch.before` separately while executing and verifying the command's
exact authored capture. After all supplied capture claims pass the unchanged
checks, it restores the inherited and native observations as a deduplicated
`record.reads` union. This is five added product lines in `commands.py`;
`_commit_patch.py`, `_recording.py`, `commit.py`, schemas and Runtime are unchanged.
Declarations are validated and bound at their original batch/step inputs;
they are neither discarded nor recaptured after execution. Step dependencies,
physical read bindings, history and undo continue to receive the complete union.

Sixteen focused regression cases use the existing authentic `realm.move()`
capture and production `RuntimeCommitService` through the existing detached
port. They cover mixed move + absent-root parent/meta patch in both merge modes,
preview without persistence, accepted publication, native capture preservation,
authoritative step patches/dependencies, inherited request reads on every step,
and sequential reads of a move's output. Boundary assertions distinguish
batch-entry reads from later step reads, even when the batch changes their value.
Other cases reject omitted/extra forged command reads, preserve disjoint-field
replay, reject atomic scope changes, and reject request/step dependency writes
including A→B→A. No original test was changed, skipped, removed or weakened.

Final verification (all exit 0):

```sh
# Run from the assigned Agent worktree. tmpdir is a harness pointer file whose
# contents name this private scratch directory, rather than a directory itself.
export PYTHONPATH="$PWD:/home/user/work/runtime"
export TMPDIR=/tmp/w-ef0625509b
export PYTHONPYCACHEPREFIX=/tmp/w-ef0625509b/pycache

/home/user/work/venv-agent/bin/python -m pytest -q \
  -o cache_dir=/tmp/w-ef0625509b/pytest-cache \
  --basetemp=/tmp/w-ef0625509b/pytest-final \
  tests/editing_conformance/test_doc_patch_v2.py tests/sdk/test_p1_doc_patch_provider.py
# 119 passed in 10.45s

/home/user/work/venv-agent/bin/python -m pytest -q \
  -o cache_dir=/tmp/w-ef0625509b/pytest-cache \
  --basetemp=/tmp/w-ef0625509b/pytest-regression-complete \
  tests/editing_conformance/test_doc_patch_v2.py \
  -k 'mixed_native_capture or inherited_reads_do_not_authorize or mixed_native_inherited_reads or inherited_native_read_conflicts'
# 16 passed, 86 deselected

/home/user/work/venv-agent/bin/python -m pytest -q \
  -o cache_dir=/tmp/w-ef0625509b/pytest-cache \
  --basetemp=/tmp/w-ef0625509b/pytest-native \
  tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py \
  -k 'paths_json_equality_claims_and_frozen_schema or original_capture_claims_are_verified_before_refresh or dependent_unsent_original_guards_allow_equal_state_aba_at_fresh_base'
# 3 passed, 234 deselected in 1.81s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache \
  astrid/sdk/timeline/commands.py tests/editing_conformance/test_doc_patch_v2.py
# All checks passed

env PYTHONPATH="$PWD" RUFF_CACHE_DIR=/tmp/w-ef0625509b/ruff-cache \
  /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# current=2151 baseline=2151

env PYTHONPATH="$PWD" MYPY_CACHE_DIR=/tmp/w-ef0625509b/mypy-cache \
  PYTHONPYCACHEPREFIX=/tmp/w-ef0625509b/typecheck-pycache \
  /tmp/astrid-u2-typecheck/bin/python -m mypy astrid/sdk/timeline/commands.py \
  --hide-error-context --no-color-output --no-pretty --show-error-codes
# Success: no issues found in 1 source file

env PYTHONPATH="$PWD" MYPY_CACHE_DIR=/tmp/w-ef0625509b/mypy-ratchet-cache \
  PYTHONPYCACHEPREFIX=/tmp/w-ef0625509b/typecheck-pycache \
  /tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
# current=1915 baseline=1915

git diff --check
```

Before the product fix, the initial 14 added cases produced 10 failures and
4 passes: legitimate mixed execution and later dependency checks stopped at
`capture_mismatch`; forged claims already refused. After the fix those 14
passed; the final two landing-head cases bring the focused total to 16. An
initial invocation without the Runtime source on `PYTHONPATH` could not load
conftest (`runtime_protocol` missing); the commands above correct that import
environment without installing or modifying dependencies. An intermediate new
assertion incorrectly treated native aliases as normalized dependency refs;
the final assertions check exact native observations and normalized dependency
entries separately. Field dependency conflicts retain the existing provider
classification `value_conflict`; atomic conflicts retain `atomic_scope_changed`.

The loaded command module was this worker's `astrid/sdk/timeline/commands.py`.
The read-only Runtime platform import came from `/home/user/work/runtime`, at
observed commit `44d6be180e65174a8c25047a599342752e7afeff`. The detached tests
use their existing fake ABI exceptions/schema digest; they do not run Runtime's
store or service. Logs are in `/tmp/w-ef0625509b/targeted-final.log` and
`mypy-ratchet.log`.

Wire limitations remain explicit: the existing detached port returns historical
`rebased` for a disjoint-head success and does not expose authoritative steps
in result data; the regressions verify prepared/stored `records.steps`, exact
commands, receipt and `rebased_onto`. No claim is made about real HTTP `merged`,
response steps, immutable Runtime history metadata, persisted idempotency,
authorization or generated schema/client validation. No reply adapters were
added. The separate 0129 wrong-before invalid-envelope finding belongs to R3,
and Runtime binding provenance belongs to its existing owner. No full, browser,
heavy or live Runtime suite was run; no schema, pin, shared dependency or git
mutation was made.

No plan decision changed and nothing blocks this scoped correction. Next:
independent review, harness commit/integration, then the existing Runtime owner
should qualify the joined native service cases after the parallel provenance,
wire expectation and R3 repairs land. This report does not mark those gates green.
