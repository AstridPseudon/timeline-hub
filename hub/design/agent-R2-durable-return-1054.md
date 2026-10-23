# R2 durable return 1054

## Disposition

PASS for the requested genesis correction. Only
`tests/editing_conformance/test_inverse_stage_runtime_regressions.py` was
changed.

The blocking 1049 finding was corrected by removing the synthetic
`original_document()` closure construction, hand-built `prepared(...)` value,
canonical publication, recorder clearing, and direct `TimelineCommitStore.accept`
call. The setup still uses the real Runtime `create_timeline` and authenticated
empty bootstrap. After registering the pinned Agent provider, it creates the
baseline through ordinary public `RuntimeService.commit_timeline` operations:

1. native `track.create` for the `picture` output track;
2. native `clip.add` for `clip-a`;
3. native `clip.add` for `clip-b`;
4. public `doc.patch` creating `config.output` and `unknown`.

Each operation is submitted through the existing `_submit` helper, hence the
Runtime service → registered Agent provider → real SQLite TimelineCommitStore
path. The resulting accepted canonical document is the baseline returned to
all seven regressions. No fabricated forward record, publication, claim,
cache, SQL journal, or direct acceptance remains. The baseline uses ordinary
text clip births because the retained cases exercise parent clip mirrors and
do not require a media claim; no unrelated media fixture was synthesized.

The five retained case identities and all existing assertions remain intact:
cases 4, 16, 28, 40, 49; authenticated forward history; full v2 request and
receipt fields; canonical records, steps, dependencies, effects, bindings,
ranges, and physical mirrors; whole undo/redo; forged-source/step refusal; and
native-write/ABA refusal.

## Evidence

Collection:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_inverse_stage_runtime_regressions.py
7 tests collected in 0.62s
```

Final seven-test run after the setup correction:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_stage_runtime_regressions.py
.......                                                                  [100%]
7 passed in 15.62s
```

An earlier post-correction diagnostic run exposed only that the new baseline
omitted the existing `parent.unknown` container used by the preserved note
patch; it reported 6 failures and 1 pass with `missing path ancestor`. The
final public baseline patch creates that empty container, and the final run
above passes all seven.

Static and artifact checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_inverse_stage_runtime_regressions.py
All checks passed!

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=<worker tmpdir>/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check
clean
```

The final worktree has one modified file, the permitted test file. No full,
HTTP/browser/live-socket, native14, Runtime237, or original 58-case suite was
run. Runtime source custody remains checked by the test's existing exact
module-origin and SHA-256 assertions for Runtime `49ce...2181` and the Agent
commit/inverse blobs.

## Blockers and next steps

Nothing is blocked. The harness should commit the worktree with the supplied
message, then run the orchestrator's review/merge qualification. A full suite
remains intentionally unverified here per the task brief.
