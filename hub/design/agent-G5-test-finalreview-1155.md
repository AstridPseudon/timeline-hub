# G5 final review: test-import migration

## Verdict

**SOURCE PASS; behavioral Runtime witness PENDING. Do not call whole G5 PASS.**

Reviewed `tl/agt-G5-test-imports-return-1147/b4a5b3b7e` cumulatively against
`086db31e4`, following PLAN §3 G5/G3 and C0 §§1–5. The cumulative diff changes
only the two assigned test files:

- `tests/timeline/test_authoring_feedback.py`
- `tests/editing_conformance/test_native_sheet_current_runtime.py`

No product, generated, contract, pin, service, or shared-dependency files were
changed. No Git mutation was performed.

## Source review

The previous 1143 failure was corrected at the right boundary. The three new
negative cases in `test_authoring_feedback.py:194-252` first emit ordinary
`doc.patch` commands and then call `DetachedRealm.call()`, which invokes the
production Agent `create_runtime_commit_service().commit()` at
`tests/sdk/test_timeline_commit_provider.py:103-105`; they do not ask the
serializer to refuse. Coverage is:

- malformed known `am-type` parameter (`text: None`);
- unknown sealed `am-flap` parameter (`null`);
- unverified media replacement outside the admitted manifest.

Each checks the wire code, provider code/reason, empty path, hint, suggested
command, unchanged head, unchanged history entries, and unchanged canonical
document map. The expected failures are `validation_error/invalid_document`
for the first two and `conflict/dependency_changed` for media.

The Runtime-facing replacement at
`test_native_sheet_current_runtime.py:279-307` emits the malformed-param patch
and submits it through `TimelineSession.commit_many`. It asserts the exact
patch, `validation_error`, `invalid_document`, reason, path, hint and command,
unchanged head/history, and no new history entry. The accepted half retains the
original authenticated `commit_many` proof for canonical output, history
records, reload, guarded undo/redo, opaque fields, and shared-source sibling
isolation (`:335-405`).

The original protected assertions remain present or are adapted to the settled
G3/C0 generic-patch boundary: guarded paths and `before` values, presence and
mirror-loss refusals, null/absence semantics, canonical/reload/undo behavior,
opaque preservation, source-bound media behavior, and shared-source behavior.
The old narration refusal was correctly replaced by an exact generic patch
assertion; it is no longer a serializer limitation. No success was changed to
refusal and no refusal was reduced to a serializer-only check.

## Verification

All commands ran in `/home/user/work/wt/agt-G5-test-finalreview-1155`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/agt-G5-final-author tests/timeline/test_authoring_feedback.py
33 passed in 2.23s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/agt-G5-final-emitter \
  tests/editing_conformance/test_document_patch_emitter_engine.py \
  tests/editing_conformance/test_document_patch_emitter_v2.py \
  tests/editing_conformance/test_native_sheet_ordinary.py \
  tests/sdk/test_timeline_sheet_native.py
135 passed in 16.90s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider \
  tests/timeline/test_authoring_feedback.py \
  tests/editing_conformance/test_native_sheet_current_runtime.py
52 tests collected; Runtime file contributes 19

/home/user/work/venv-agent/bin/ruff check \
  tests/timeline/test_authoring_feedback.py \
  tests/editing_conformance/test_native_sheet_current_runtime.py
All checks passed!

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m mypy \
  tests/timeline/test_authoring_feedback.py \
  tests/editing_conformance/test_native_sheet_current_runtime.py
Success: no issues found in 2 source files

git diff --check 086db31e4..HEAD
passed
```

The target diff names only the two assigned tests. The retired
`document_diff` imports/symbols are gone from both targets.

## Behavioral pending / harness evidence

The real Runtime HTTP lane remains unverified. The prior approved central
request was exactly:

```text
target=agt-G5-test-imports-return-1147
repo=agent
suite=targeted
files=tests/editing_conformance/test_native_sheet_current_runtime.py
```

Its environment was:

```text
HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages"
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-composition14-255b6856
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-composition14-255b6856/node_modules
/home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_native_sheet_current_runtime.py
```

The central lane reported `[integration] NO CI job runs this lane (manual: run
it by hand with -m integration)` and deselected all 19 Runtime cases, including
the edited case. It therefore provides no execution credit and is an ordinary
harness limitation, not a test result. No direct localhost/live-socket run was
performed under the central-service rule.

## Next step

Run the single edited Runtime integration case in an approved manual
integration environment using a genuine current fixture. Until that succeeds,
carry this as source-qualified but behaviorally pending; do not merge/integrate
or declare whole G5 complete.
