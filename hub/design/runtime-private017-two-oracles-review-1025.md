# Runtime PRIVATE017 two-oracles assertion review

Date: 2026-10-21 UTC

## Disposition

- Ordered source `8ad62e4dce83ab3df7f3778dec2a449100e585d1`: **APPROVE**.
- RT03 source `42a03d324af6e7916923fe7c152aa1fcccf996d4`: **APPROVE**, with exactly its one-line/comment manifest-order hunk applied to the `8ad62e4d` test file.
- No target body, full suite, HTTP/socket/browser/render/install/generation/pin/product-code/test-body run was performed.
- This is an oracle review only; it makes no qualification or adoption claim.

The projected Runtime test file is `8ad62e4d` plus only the RT03 hunk from `42a03d3`; no RT03 process document is included. Runtime source outside `tests/test_timeline_owned_reference_integration.py` remains exact `42a03d3` for the RT03 source context.

Projected test-file SHA256:

```text
28583b4adda23d464207a43c71b3f134ff960363050908b51187fab646705b13
```

## Ordered case audit

The changed helper is a valid independent authoritative capture:

```python
plan = execute(agent.bundle(document), [copy.deepcopy(command)])
return plan.records[0]["command"]
```

It uses the exact pre-remove `original` canonical document and an unchanged deep copy of the raw remove command. It does not inspect the remove result, derive a subset, sort either side, strip recorder metadata, or alter the submitted key/body/guards. The accepted record's complete enriched command is therefore compared one-to-one with the normal Agent recorder's complete command. The prior raw-command equality was necessarily wrong because normal recording adds capture metadata.

The remaining ordered assertions match the existing contracts:

- exact accepted envelope: receipt result equals accepted data;
- removed map and canonical key order: target is absent while `a-before` and `z-after` remain in order;
- exact recorded writes: leaf `null` to absence, then empty target namespace to absence, including the full `insertion_order`;
- opaque sibling values and explicit null/absence states remain exact;
- restart retry uses the same exact body/key, trips if the provider executes, returns the original accepted envelope, and leaves SQLite/history unchanged;
- inverse restores the complete original parent payload and ordered map;
- redo restores the complete removed parent payload and ordered map.

No assertion is result-derived or metadata-weakened. **APPROVE**.

## RT03 case audit

The `42a03d3` hunk changes only the canonical media-manifest order assertion and explains it. Both complete pins remain asserted, with neither side sorted in the test. The expected order is the existing Agent/Runtime canonical `media_id` order: `exact_pin` precedes `unrelated_pin`.

The whole unchanged RT03 body preserves:

- exact one-to-one accepted reference identity, object pin, and source role in both the live projection and snapshot;
- managed raw ownership through the real `MediaReads.raw_media_info` descriptor, exact manifest pin retention, and a foreign-project raw pin refusal;
- no placement: parent occurrences and clips remain empty;
- accepted receipt identity/result equality;
- restart exact retry with provider-execution tripwire and no duplicate projected row/SQLite writes;
- same-key changed payload refusal without writes;
- occupied reference-id refusal with unchanged SQLite state, head, and history;
- inverse removal back to the unrelated reference and exact restoration of the prior parent payload/closure.

The correction does not sort both sides, compare sets, drop pin fields, or replace an accepted positive with refusal. **APPROVE**.

## Evidence and limits

Read-only source checks performed:

- `git show 8ad62e4d...` and `git show 42a03d324...`: inspected the exact committed test diffs and complete test body.
- Read-only Runtime source trace: `TimelineCommitStore._validate/_publish`, `revision_closure`, the accepted envelope/ledger path, raw-media custody, and reference projection occupancy/removal rules.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B -c '...ast.parse(...)'`: **PASS**.
- `git diff --check 8ad62e4d^ 8ad62e4d -- tests/test_timeline_owned_reference_integration.py`: **PASS**.
- `git diff --check 42a03d3 -- tests/test_timeline_owned_reference_integration.py design/runtime-rt03-manifest-order-diagnosis-1019.md`: **PASS**.
- Projected-file streaming SHA256 computation: **PASS**, value recorded above.

The earlier ordered pure-recorder probe and RT03 pure manifest probe were read as prior evidence from their reports; they were not rerun here. The central corrected RT03 run stopped at the old manifest-order assertion, and the ordered corrected body has not run, so downstream behavior remains unverified live. No full or live-socket/browser/render suite was requested or run.

