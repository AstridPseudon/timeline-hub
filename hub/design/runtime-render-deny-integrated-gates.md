# Runtime render-deny integrated gates — APPROVE

Verification completed 2026-10-20 for the independently approved legacy render
publication refusal. This report covers integration of the refusal only; it
does not qualify the native registered-render completion path.

## Frozen sources and preservation

The integration source was frozen at the start of verification:

- Runtime integration commit: `c1fb9ef2f7736459ceaaaaf85b5f9650e32c942d`
- Runtime integration tree: `e0aa6fbeb28a771a121248c0879aa6831d16f5fd`
- Integration parent before this merge: `a51267ec3dd94ea465a3161e3b4d8fbcd061009e`
- Reviewed refusal commit: `693462918509964803ae6c127b9b8038a4ac7bf4`
- Reviewed refusal tree: `a53f2af3f58f763bc7c93419d94864c9a9f0029a`

`/home/user/work/runtime` was clean at the frozen integration commit. Its
delta from `a51267e` is exactly:

```text
runtime_protocol/service.py                        M
tests/test_timeline_render_publication.py          M
tests/test_timeline_render_publication_authority.py A
```

The service file has a legitimate later text-clear custody patch relative to
the reviewed refusal source. I inspected that diff; it is outside the render
publication functions. AST fingerprints for the reviewed and actual current
sources match exactly for both `_assert_legacy_render_publication_target` and
`publish_timeline_render`, including the tracking guard and exact-replay
ordering:

```text
_assert_legacy_render_publication_target
23df4547d1a0e9dfb2786626e9a8f108b1b6f907ce3dc5fe03530135c1497e25
publish_timeline_render
018465f8187f815aed847e30d9edb65ecbd6c759150b9b13b40b8d5a916fc55b
```

The guard merge changed no previously integrated S2 view, connector, artifact,
capture, or text files. Direct preservation checks were clean for the S2
authority files, `capture_validation.py`, the media-completion fence tests,
the text custody/selection files, contract/artifact metadata, the operation
handle, and artifact-manifest tests. The complete merge file list above is the
stronger whole-tree check.

## Verification

Direct focused publication and authority tests, run against the frozen
integration source with shared dependencies and pytest caches read-only:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_render_publication.py \
  tests/test_timeline_render_publication_authority.py
```

Result: **20 passed in 13.87s**, exit 0.

The exact neighbor selection from the approved source report also passed:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_render_publication.py \
  tests/test_timeline_render_publication_authority.py \
  tests/test_timeline_headless_overwrite_refused.py \
  tests/test_timeline_commit_baseline.py \
  tests/test_timeline_producer_guards.py \
  tests/test_timeline_producer_checkpoint.py \
  tests/test_timeline_commit_acceptance.py \
  tests/test_task_continuations.py
```

Result on current integration: **205 passed, 1 deselected in 84.11s**, exit 0.
The earlier source report recorded 204 because this selection ran before the
final legacy-head-positive test was added; the requested selection itself is
unchanged.

The required central named integration lane was requested with an explicit
file selection:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  integration:runtime commit-integration \
  --files "tests/test_timeline_commit_integration.py"
```

Request: `runtime-commit-integration-1020120653-21385`.
The central snapshot recorded tree `e0aa6fbeb28a771a121248c0879aa6831d16f5fd`.
Result: **9 passed in 10.08s**, exit 0. The named suite already includes the
file, so the service log shows it twice after appending `--files`; collection
still produced the expected nine passing tests.

## Safety semantics checked

The authority tests preserve the reviewed boundaries:

- Refusal diagnostics compare the complete SQLite `iterdump()`, all CAS and
  staging bytes, and `conn.total_changes`; tracked-target, target mismatch,
  malformed/missing admission, corrupt immutable spec, and inconsistent native
  target refusals are whole-state no-write negatives.
- The TOCTOU test introduces authentic canonical tracking after the separately
  committed prepare checkpoint. The second guard refuses before publication
  writes, leaves the prepared checkpoint prepared, and preserves the canonical
  head. It does **not** claim that the entire invocation is state-free across
  the injected race.
- Exact published-checkpoint replay happens before live target checks and still
  returns the original result after tracking, author cancellation, task-spec
  loss, and target archival. The changed payload under the same authoring
  identity is refused, and replay makes no SQL/CAS change.
- The approved native-only/registered-assembler completion behavior remains an
  explicit open gap. No native completion claim is made here.

No product edits, merge, pin, publish, shared-dependency/cache writes, full
suite, or broad suite were performed. No blocker found.
