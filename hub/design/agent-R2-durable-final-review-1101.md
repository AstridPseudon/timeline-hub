# R2 durable final Luna review — PASS

## Scope and disposition

Reviewed `tl/agt-R2-durable-return-1054` at `db3c11ca6` against `7abfb8d69`,
the previous independent FAIL at `agent-R2-durable-review-1049.md`, and the
author return at `agent-R2-durable-return-1054.md`.

PASS for this requested seven-test R2 regression witness. The correction is
real: the synthetic `prepared(...)`/hand-built publication/direct
`accept(...)` genesis from 1049 is gone and the baseline is now created by
ordinary public Runtime service/provider commits.

The cumulative diff from `7abfb8d69` is exactly one new file:
`tests/editing_conformance/test_inverse_stage_runtime_regressions.py`, 413
lines. No original test was changed, deleted, or rewritten, and the review
worktree is clean. This is a new seven-test named regression witness; it does
not recover or qualify the original 58-case probe.

## Authentic genesis and public creation

The fixture creates a temporary RealmStore, then uses the real Runtime
`RuntimeService.create_project`, `create_timeline`, authenticated canonical
bootstrap, and the registered Agent provider. It obtains the empty closure,
then creates the baseline through four ordinary public
`RuntimeService.commit_timeline` submissions via `_submit`:

1. native `track.create` for the `picture` output track;
2. native `clip.add` for `clip-a`;
3. native `clip.add` for `clip-b`;
4. public `doc.patch` for `config.output` and `unknown`.

Each accepted response supplies the next canonical document used to build the
following request. There is no hand-built prepared record, fabricated
publication, recorder-claim clearing, direct `TimelineCommitStore.accept`,
synthetic closure, SQL journal, private row insertion, cache/provider
bypass, or executor path. The only direct store usage is canonical bootstrap
and read-side inspection (`revision_closure`, `history_entry`, and SQLite
`iterdump()` snapshots); all authored baseline and regression writes go
through the public service and registered provider.

## Behavioral coverage

The exact seven collected tests are:

- case 4: two-step clips-before;
- case 16: two-step clips-after;
- case 28: two-step config/clips-before;
- case 40: two-step config/clips-after;
- case 49: native whole;
- forged source publication and forged step refusal;
- native write followed by ABA refusal.

For every parametrized positive case, the test keeps the original forward,
whole inverse, and inverse-redo assertions. Forward and inverse requests are
submitted through `RuntimeService.commit_timeline` and the registered Agent
provider. The assertions cover the full request fields used by this witness:
base revision/publication pair, commands, label, full steps and step patches,
declared reads, command ordinals, `merge`, idempotency key, `dry_run`, source,
rationale, and group id. Accepted data/receipt identity, accepted status,
canonical document, durable history, command records, dependencies, effects,
derived writes, bindings, ranges/boundaries, physical `clips`/
`config.clips` mirroring, undo records, and exact redo are retained.

The two refusal tests retain the no-write assertions: the head publication
and complete SQLite `iterdump()` are unchanged for forged source/step and for
the native ABA intervening-write case, with the expected refusal reasons.
No original assertion was weakened or removed; the return diff changes only
fixture setup/imports and preserves the seven test bodies.

## Source custody

The test pins Runtime commit
`49ce53289bc37d9387a7d9e6b9c9b16072162181`. The real
`/home/user/work/runtime` checkout is clean at that commit, and the tested
Runtime module origins and SHA-256 hashes match the pinned files:

- `runtime_protocol/timeline_commit_auth.py`:
  `65fd735edfa0e9f4a77aaf4f473095f1539ea1ce453439177e9fe7f39b4466f1`;
- `runtime_protocol/timeline_commit_store.py`:
  `243d312fe404f5ed80f0ef1aa9d7405b93ff77949eef5157827a7779c6323b9f`.

The Agent source hashes asserted per fixture and per case are:

- `astrid/sdk/timeline/commit.py`:
  `7776e31c83a7f0fc58965141b5863548c7cd4bb60f58f5c827848254c810eb3b`;
- `astrid/sdk/timeline/inverse.py`:
  `267b1b1589c0254345a13bf802df8b40301f70020389c223c91f4b14808f336d`.

Both match the working tree and the corresponding `7abfb8d69` product blobs.
The current `/home/user/work/agent` integration checkout is the distinct D17
line (`abfa78a65`); this review does not claim a joined D17 proof. That later
integration proof remains a separate required step.

## Exact verification

Collection:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_inverse_stage_runtime_regressions.py
7 tests collected in 0.59s
```

Exact seven-test run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_stage_runtime_regressions.py
.......                                                                  [100%]
7 passed in 14.84s
```

Additional checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_inverse_stage_runtime_regressions.py
All checks passed!

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR="$review_mypy_cache" /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check 7abfb8d69..HEAD
clean
git diff --name-status 7abfb8d69..HEAD
A tests/editing_conformance/test_inverse_stage_runtime_regressions.py
git status --short --untracked-files=all
clean
```

No full suite, HTTP/browser/live-socket suite, native14, original58,
daemon, Git write, install, or shared-dependency mutation was run. Nothing is
blocked for this review. Recommended next step: merge this test-only return,
then obtain the later joined proof on the distinct current D17 integration
line before treating the integrated product as qualified.
