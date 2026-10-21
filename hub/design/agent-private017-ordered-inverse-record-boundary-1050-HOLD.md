# Agent PRIVATE017 ordered inverse record-boundary review — HOLD

Date: 2026-10-21 UTC

## Reviewed source identity

- Agent commit: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`
- Agent tree: `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`
- Runtime reviewed candidate: `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`
- Ordered proof: `rt-m2-private017-reviewed-two-proof-1029-private017-agent6c-integration-1021103142-12634`
- Retained Runtime report/test SHA: `28583b4adda23d464207a43c71b3f134ff960363050908b51187fab646705b13`

## Exact Agent boundary comparison

The refusing guard is `astrid/sdk/timeline/commit.py:181-183`, in
`_inverse_media_removals`:

```python
if not equal(list(records), [record for entry in records.entries
                             for record in entry['records']['commands']]):
    raise CommandError('media inverse records differ from accepted history', ...)
```

The left operand is populated at `commit.py:1047-1048` by `_records()`.
`_records()` (`commit.py:613-628`) validates the accepted record shape and
then does only `copy.deepcopy(recorder["commands"])`; it does not rebuild,
sort, normalize, or filter command records. Therefore, for the ordered target
entry, the left operand is a deep copy of the exact right-operand list. The
optional `writes[*].insertion_order` member is not handled by `_records()` and
cannot be dropped there.

The Agent comparison also cannot be explained by JSON object-member order:
`astrid/sdk/timeline/_command_state.py:31-43` compares mapping keys as a set,
while preserving list order and distinguishing booleans from numbers. The
ordered carrier itself is emitted by
`_project_data_commands.py:116-124`, copied by `_recording.py:137-151`, and
forwarded by `inverse.py:100-102,488,530-540`.

Consequently, no first differing Agent path/presence/value exists in the
reviewed reconstruction. If the two operands reach `_inverse_media_removals`
with the same `records.entries` object contents, this guard is mathematically
true. The retained central log records only the exception and does not retain
the two operand snapshots, so it cannot identify a path/value difference.

## Evidence

Targeted command:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py
```

Result: **23 passed in 1.48s**. This includes the source-created ordered
namespace remove, JSON reload, inverse/redo exact restoration, ABA refusal,
absent-key compatibility, and malformed order/value coverage.

No files in the Agent worktree were changed. No Runtime proof node, old44/186,
full, HTTP, socket, browser, native, renderer, or outer suite was run.

## Disposition / next step

**HOLD — Runtime-owned operand capture is required.** Runtime should retain one
bounded rerun of the already-authorized ordered node, after the final Agent
review, with a read-only diagnostic immediately before the Agent guard that
compares the first differing path, key presence, value/type, and list order
between:

1. the `AcceptedRecords` list returned by `_records()`; and
2. `entry['records']['commands']` from the exact accepted history entry.

If `insertion_order` is absent only on the second operand after restart, that
is a Runtime persistence/carrier defect and belongs to Runtime. If the operand
diff is elsewhere, Runtime should return that exact path and bytes before any
Agent change is considered. No guard exemption, assertion weakening, schema
change, normalization, refreshed claim, or Agent workaround is reviewed.
