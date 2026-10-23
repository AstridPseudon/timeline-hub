# G2/G5 retained historical-basis source repair — 1917

**Product defect confirmed and repaired; source remains DRAFT. P1 NO-GO.**
No integration merge/request or original FOUR/firstnode qualification was run.

## Cause and interface

The corrected1907 packet proves both ordinary `TimelineSession.move` commits
were accepted. The earlier1902 `internal_error` was the observer's missing
`_event(name)` argument; it is not a Runtime product finding.

`find_version` iterated retained history but discarded each row's publication
ID when calling `Checkout.open(revision_id=...)`. The existing
`store.fetch_bundle` deliberately leaves revision-only reads unbound to a
publication. Current-head checkout, however, hydrates the authenticated exact
revision/publication pair. Publication identity participates in `sheet_version`
because it is present in `Checkout.document()`.

Before patching, I reconstructed those two **real construction paths** using
corrected1907's complete original canonical closure from
`cases/005-port-prepared.json` (not a fabricated DB/history or a new fixture).
`open_authoring_bundle` equals `bundle_from_document` after removing the latter's
private `_runtime_document`. The full public document difference is exactly:

```text
/base_parent/publication_id
original head: txn-11c90075be6c4c8bb9e2627366f0fe4f
revision-only historical read: absent
reconstructed original sheet hash: 9ebd6df1c29b
reconstructed historical sheet hash: 3c9e1de54da4
```

The revision is `a3e671256f1c42b8837d3e118c97b21b`, parent digest
`sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`.
These hashes are reconstruction results from the captured closure, not a claim
that the old observer directly captured the test's original Python local.
Complete canonical input, both full documents and the path diff are in
`evidence/cause.json`. Thus the old assertion is valid; no test adaptation is
needed. The existing packet was sufficient, so no new diagnostic service run
was needed. The early finding/interface was published here before source edits.

The patch adds optional `publication_id` to existing `Checkout.open`, forwards
it to existing `store.fetch_bundle`, and passes both retained row IDs from
`find_version`. The real public remote reader continues to verify the pair,
receipt ID, scope, immutable digest, manifest and child owners. No current-head
substitution, payload-equality identity inference, metadata removal or new
hydrator was introduced. `store.py` is unchanged. Only two production files
changed (six inserted lines, three removed lines).

## Regression and bounded evidence

The new file `tests/sdk/test_g5_retained_sheet_basis.py` reuses the existing
complete `document_fixture` and real provider `DetachedRealm.call` commit path;
only immutable transport reads are fake. It exercises the real public closure
reader, one-item history pagination, original head open, two ordinary moves,
reopen and `find_version`, asserting exact complete document and source-mapping
equality plus no document/history mutation. Opaque fields, explicit nulls,
registry, source pins and shared child closure remain in that existing fixture.
Six cases cover bootstrap/accepted/repeated-revision publications × shared or
unshared children. Repeated publication is produced by a real no-op provider
commit; its revision stays equal and publication changes.

Before the source patch, all four initial bootstrap/accepted cases failed at
`assert restored is not None`, matching the original failure. After the patch
those four passed in a 124-test selection. Final coverage adds the repeated
publication cases and the existing checkout initial-base test: **127 passed in
15.10s**. The separate existing authentic current-pair/store selection passed
**16 tests in 4.34s**. Total final bounded evidence: **143 passed**.

Exact final node IDs (including all parametrizations) are in
`evidence/exact-nodes.txt` (143 collected). Critical nodes include:

- `tests/sdk/test_g5_retained_sheet_basis.py::test_find_version_preserves_exact_retained_publication[bootstrap-False]`
- `tests/sdk/test_g5_retained_sheet_basis.py::test_find_version_preserves_exact_retained_publication[bootstrap-True]`
- `tests/sdk/test_g5_retained_sheet_basis.py::test_find_version_preserves_exact_retained_publication[accepted-False]`
- `tests/sdk/test_g5_retained_sheet_basis.py::test_find_version_preserves_exact_retained_publication[accepted-True]`
- `tests/sdk/test_g5_retained_sheet_basis.py::test_find_version_preserves_exact_retained_publication[repeated-False]`
- `tests/sdk/test_g5_retained_sheet_basis.py::test_find_version_preserves_exact_retained_publication[repeated-True]`
- `tests/sdk/test_timeline_checkout_history.py::test_sheet_local_basis_does_not_cross_accepted_base`
- `tests/sdk/test_timeline_checkout.py::test_first_draft_pins_the_fetched_bundle_for_edit_diffs`
- `tests/editing_conformance/test_current_pair_reader.py::test_explicit_historical_read_does_not_acquire_current_publication`
- `tests/editing_conformance/test_current_pair_reader.py::test_explicit_wrong_publication_refuses`
- `tests/editing_conformance/test_current_pair_reader.py::test_reset_reads_reused_revision_under_new_publication`

Exact test commands (cwd is the assigned worktree; `$TMPDIR` is the private
harness scratch root `/tmp/w-435215d331`):

```bash
# Before product patch; initial four new cases: 4 failed in 2.40s (red.log).
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$TMPDIR/red tests/sdk/test_g5_retained_sheet_basis.py

# After patch; initial four plus existing selection: 124 passed in 14.76s (green.log).
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$TMPDIR/green tests/sdk/test_g5_retained_sheet_basis.py tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sheet_native.py tests/sdk/test_remote_timeline_owner_scope.py

# Final selection: 127 passed in 15.10s (final-tests.log).
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$TMPDIR/final tests/sdk/test_g5_retained_sheet_basis.py tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sheet_native.py tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_timeline_checkout.py::test_first_draft_pins_the_fetched_bundle_for_edit_diffs

# Existing authentic store controls, without sockets: 16 passed in 4.34s (current-pair.log).
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=$TMPDIR/current-pair -m integration tests/editing_conformance/test_current_pair_reader.py
```

## Lint, type, artifact and source checks

```bash
# PASS: Ruff findings current=2148 baseline=2148.
env PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=$TMPDIR/ruff PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# PASS: Mypy findings current=1911 baseline=1911.
env PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=$TMPDIR/mypy-private PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# Scoped production files: 7 inherited Ruff / 1 inherited mypy findings,
# zero added or removed diagnostic identities versus HEAD snapshots in private scratch.
/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline_sheet.py astrid/sdk/timeline/checkout.py --output-format json
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline_sheet.py astrid/sdk/timeline/checkout.py --hide-error-context --no-color-output --no-pretty --show-error-codes
# New tests: Ruff clean / mypy Success: no issues found in 1 source file.
env PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=$TMPDIR/ruff /home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_g5_retained_sheet_basis.py
env PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=$TMPDIR/mypy-new-tests /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy tests/sdk/test_g5_retained_sheet_basis.py --hide-error-context --no-color-output --no-pretty --show-error-codes
# Both PASS, unchanged frozen producer and artifacts.
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

The first mypy ratchet attempt using `venv-agent` failed (exit 2) because that
dependency environment lacks YAML stubs and exposes a NumPy stub using a Python
3.12 type statement under the configured 3.11 target. No dependency was changed.
The existing `venv-agent-typecheck-v2` environment then passed the exact 1911
ratchet. Both logs are retained. Scoped baseline/current checks use private
caches and HEAD source copies under `$TMPDIR`; details and all command arrays
are in `scoped-quality.json` and corresponding raw logs. The initial packet
reconstruction first failed before running because Runtime was absent from
PYTHONPATH; adding the actual requested Runtime path resolved that import.

Actual Runtime preflight: HEAD
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree
`f79a2355cfb39d9ada7721978bd20d5702105778`. Corrected1907 child boot itself
records this actual commit while configured expected remains stale `d9e2…`.
Fresh imports of server, service, execution, port, provider, store,
`timeline_commit_auth` and `auth` all originate in that checkout and match its
actual committed bytes. Their SHA256 values are in
`preflight-source-identity.json`. This is static/import preflight, not a claim
of a new observed daemon run. Archive SHA256 remains `2915bd4a…`.

All original FOUR function bodies/decorators match their exact observer body
locks. The entire original test file and the provider/inverse/store sources,
vendor lock and artifact manifest match base `89c38c9355f5d4bcc68597ec74e4729435a7a07a`.
The request/reply writer path is untouched: C0 request fields, full receipt,
canonical document, records, bindings, effects, dependencies, history, undo
steps, preview/null receipt and structured refusal fields retain their existing
implementations. No schema, pins, auth, inverse, root, step, commit-patch,
executor or Runtime guards changed. No original test/assertion/recipe was
modified, skipped, xfailed or weakened. No Git writes or shared dependency
mutations occurred.

## Packet and next owner

Own evidence root: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-history-basis-sol-1917/evidence`.
Complete corrected1907 cases/logs/bodylocks/observer sources are retained in
`corrected1907-complete.tar.gz` (1,062,200 bytes), SHA256
`98b0ecccd27a940c8b3c7a4ee7a3267f1706edbba947af0366a659f34b161223`.
`cause.json` SHA256
`04007ce6026824baa656882c0f8e08dcbcfc323467023c80b37fc9774ff8cf35`.
`SHA256.json` covers all own evidence files. Total evidence is under 2 MB.
Credential-shaped value scan: **0 findings**, including decompressed packet
members; the original observer's packet credential scans are also retained.

No work is blocked locally. Independent Luna1917 review is manager-owned and
not claimed complete here. Recommended next step: review this minimal exact-pair
source change and six new regressions; only after independent review PASS should
the manager own one original firstnode/FOUR qualification as separately
permitted. No original node, FOUR, c271, redo journey, live sockets/browser,
full suite or integration qualification was run here. Keep `89c…` G5 draft and
P1 NO-GO; these bounded results do not authorize activation.
