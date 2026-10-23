# G2/R2 independent review — PASS

Reviewed `tl/agt-G2-undo-v2-1113` at `78f4ef0d14da0003e271e5c43887bf0a080a5f24` against parent `abfa78a65`. The change is limited to the requested three files:

- `astrid/sdk/timeline/sync.py`
- `tests/sdk/test_timeline_sync_native.py`
- `tests/sdk/test_timeline_commit_provider_runtime.py`

## Verdict

PASS for the bounded requirement: ordinary public `undo()` now emits the complete v2 request metadata through the existing persisted `_flush()` path, while the provider supplies the real inverse patch, reads, dependencies, effects, and before/after bindings.

The implementation stages inverse intent and metadata under the existing outbox lock. A different pending command is refused before persistence; a matching pending inverse keeps the existing metadata. A new inverse with no existing flight/options freezes label `Undo timeline edit`, merge `fields`, and one stable `inverse` step with ordinal `[0]` and empty submitted patch. Existing flights—including legacy flights without v2 options—are replayed from their exact persisted body/key and do not gain metadata. `dry_run`, `via`/source, preview-key freshness, exact base pair, and the public facade signature remain on the existing paths. No caller `reads`, rationale, or group_id are invented, and no captures, provider, Runtime, contract, pin, executor, adapter, auth, request, history, or claim code was changed.

## Test evidence

The author selector from the supplied detailed report was run with a private temporary directory. It passed:

```text
185 passed, 4 deselected in 23.09s
```

The four expected integration deselections were the two new `test_public_undo_redo_persists_v2_effect_bindings` parameterizations and the two pre-existing Runtime restart tests. The first invocation had only pytest setup errors because the prescribed worker `tmpdir` path was an existing file; it did not execute tests. Rerunning with an equivalent private directory produced the result above.

The explicitly requested new real-provider selector passed against clean Runtime `49ce53289bc37d9387a7d9e6b9c9b16072162181`:

```text
2 passed in 2.96s
```

This covered whole and selected undo, preview with `would_status=accepted` and no receipt, exact idempotent replay, redo, canonical restoration/partial restoration, history `undo_steps`, provider-generated reads/dependencies/effects, and every effect's before/after binding. The test also checks the wire label, stable inverse step, empty submitted patch, omitted request/step reads, source, and absence of rationale/group_id; the provider response receipt result is checked against returned data.

Other exact checks:

```text
scoped Ruff: all checks passed
repository Ruff: current=2149 baseline=2149
private mypy: current=1912 baseline=1912
vendor-lock + artifact-manifest: 24 passed
git diff --check: passed
```

The vendor-lock and artifact-manifest tests were also included in the 185-pass selector. No shared dependency or cache was modified.

## Provenance and limits

Runtime was clean at `49ce532…` before the explicit real-provider run. After that run, an external orchestrator fast-forward merged `tl/rt-R2r-D17-current-stage-sol-1105`, moving `/home/user/work/runtime` to `3b926efab2eed122d374540baee297d4cdcec62a`; it remained clean. I did not run Git writes and did not rerun the real test against the new Runtime, as the brief requires the exact Runtime49ce selector and forbids a new D17-copy qualification.

The review does not claim new real Runtime coverage for merged or historical-rebased replies, conflict/refusal/invalid envelopes, or the D17 copy/auth path. Existing SDK tests preserve the unchanged error code/path/hint/suggested-command handling. The two pre-existing integration nodes were not duplicated. No full suite, browser/native14, HTTP, P1/P4, or unrelated copy suite was run.

No product files were edited by this review. Recommended next step: merge only `78f4ef0d1` after the repo queue records this PASS, then obtain integrated targeted proof at the merged target; do not reinterpret this review as D17 qualification.
