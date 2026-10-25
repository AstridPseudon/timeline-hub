# F-D86 D107 legacy READ handoff — SOURCE_EXACT

## Result

`SOURCE_EXACT`: the requested current read proof already exists; no new
`tests/editing_conformance/test_m1_legacy_archive_read.py` was added. The
original M1 ten-test source remains unchanged. No product, Runtime, fixture,
schema, pin, generated file, or archive was changed.

## Exact selector and evidence

Primary exact selector:

`tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_retains_authenticated_pair_and_canonical_source`

The reader fixture at `test_current_pair_reader.py:51-73` consumes the genuine
`ASTRID_AUTHENTIC_LEGACY_ARCHIVE`, requires SHA-256
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, runs the
existing backup extraction/verification and restore APIs, then runs
`verify_baseline`. It asserts the authenticated source identity:

```text
project     7b6f2bae8ffe42bf925216c38249ed79
timeline    film
revision    a3e671256f1c42b8837d3e118c97b21b
publication txn-11c90075be6c4c8bb9e2627366f0fe4f
```

The primary test uses the actual current read APIs:

```text
RemoteTimelines.open_bundle(project, "film")
astrid.sdk.timeline.store.fetch_bundle(project, "film", client=client)
```

It asserts the exact revision/publication pair and equality between
`bundle["source_mapping"]["_runtime_document"]` and Runtime's authenticated
`revision_closure(project, "film", revision)`. This is full closure identity,
including opaque values, graph, CAS/media pins, transcript/text-binding pins,
and source dependencies; it is not an archive substitution or payload-only
check.

Supporting exact existing selectors:

- `test_explicit_historical_read_does_not_acquire_current_publication`
- `test_explicit_wrong_publication_refuses`
- `test_current_fetch_requires_exact_publication_history_entry`
- `test_current_fetch_fails_closed_without_head_proof`
- `test_current_fetch_preserves_exact_scope_digest_and_owner_guards`

All are in `tests/editing_conformance/test_current_pair_reader.py`. The latter
three retain strict refusal for damaged history/head/scope/digest/owner input
using existing read guards; no new security attack construction is needed.

## Provenance and proof recipe

The exact reader source was introduced by Agent commit
`75fde1b96259ab3bc29923229e3b01e668a61bc6`,
`fix(timeline): hydrate current checkouts from the exact history head`. The
source file is unchanged in this worker worktree. The original M1 source is
`tests/editing_conformance/test_commit_runtime_m1.py`; its ten selectors remain
unchanged and are still the legacy-only baseline scope.

Protected proof recipe: run the six named test functions above from
`test_current_pair_reader.py` through the central integration test service,
with the authenticated archive environment available. The first selector is
the D107 read proof; the other selectors supply historical-read and strict
refusal evidence.

Source-only checks completed here:

- AST parse and in-memory compile: PASS.
- Ruff on the exact current source: PASS.
- Ruff on the parent source via stdin: PASS.
- mypy on the exact current source: PASS.
- `git diff --check`: PASS.

No pytest, collection, helper/fixture/function execution, Runtime service,
probe, build, browser, render, install, or full suite was run.

Evidence files:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D107-legacy-read-0633/evidence/`
