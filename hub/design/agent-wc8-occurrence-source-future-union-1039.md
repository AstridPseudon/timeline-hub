# Agent WC8 occurrence source future union

Status: source-only composition complete; activation remains held.

## Exact base and source identity

- Base commit: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`
- Base tree: `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`
- Expected resulting worktree tree (before harness commit): `dfbf42afc597ef1d2b98d368d7f051b3a9213791`
- Reviewed trim repair: commit `9c35f4a18c65ec09d567f58839590f44b6d3997d`, tree `64a25c3a5f374a1598d97a555266ad4351e41b63`
- Reviewed child-delete repair: commit `d2be6511d411b1c0eb1f3b2a9c74ad3e369fb3ed`, tree `c87a1a8a07ab486e6d52a24ff01e65b909420931`

The composed source keeps the reviewed source blobs exactly:

- `astrid/sdk/timeline/_trim_commands.py`: SHA-256 `e950aa9ff793d9b5855410dbcf75912bf039248a504e0c8a7d93a48cf05d206d`
- `astrid/sdk/timeline/_delete_commands.py`: SHA-256 `7c0bf462960889c5bafdac40c01ce2ce368f787dc33192837e057195094fb4b6`

The resulting complete authoring schema is 65 definitions / 37 EditCommand
clauses:

- raw worktree schema SHA-256: `a21553a6fe9817b7e66ee7766ddebc1acdd941168df3070de49678d8abe7e66e`
- pretty canonical schema SHA-256: `7cfbf76c35dfd346e16e963ab32ba1a4e12e4c033a80133de836cd9bc4e7e66e`
- sorted compact schema SHA-256: `62e262f0abd9c9545c8436e0aa591e26c5884fa1765704e4fc8d5f5f7a5a45b7`
- reviewed trim clause source schema: raw `ca55d74acbeef104be3a4a1ef57e2b4b2d7d1859d5194873a0fdf76a879ad6e3`, canonical `b19161c0881d7496e65e3cb52dcf57b35e661b780a608bd8fabba062d7bc495f`
- reviewed child-delete source schema: raw `fc786bb530d197ae65a0b4f9e6e09e7d5a79ae2d28094ba0dc125d17cd71e8a8`

## Composed behavior

Trim adds only the dormant, unregistered `clip.trim@2` raw occurrence-child
source-window recipe. It retains the reviewed exclusive-owner refusal before
the child/source reads, exact raw child identity, translation-only/rate/
rounding/media/verified-input guards, and source-second `from`/`to`/`hold`
writes. Parent `clip.trim@1` remains the live registered operation.

Delete adds dormant `clip.delete@2` through the existing operation family and
capture hook. It preserves v1, refuses shared ownership before writes, records
child membership/order, source and sibling dependency reads, and retains
inverse/redo, ABA, and sibling isolation. `clip.delete` is in the separate
`SOURCE_BOUND_V2_ADDITIONS` set; the frozen 13-operation
`SOURCE_BOUND_OPERATIONS` set is unchanged.

Schema floor tests strip both occurrence clauses and reconstruct the current
ed5 canonical hash `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`;
the base ed5 raw source is `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`.
The ordinary floor remains exact `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## Evidence

All commands used `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime"`
with `/home/user/work/venv-agent/bin/python`:

- `pytest -q -p no:cacheprovider tests/sdk/test_timeline_occurrence_trim_source_spike.py` — **8 passed**
- `pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_clip_delete.py` — **67 passed**
- `pytest -q -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py` — **28 passed**
- `pytest -q -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py` — **34 passed**
- `ruff check` on all changed Agent source/tests — **passed**
- `python -m json.tool astrid/core/timeline/schema/edit-command.schema.json` — **passed**
- `git diff --check` — **passed**

No full suite, HTTP, native, renderer, generation, client, lock, pin,
registry-consumer, or live-caller test was run. The only live caller count is
**none**; `timeline_sheet.py` is unchanged and remains Runtime-owned for its
delegated bridge. The remaining gap is coordinated Runtime schema/client
generation and native/HTTP consumer qualification, which is intentionally held
until a separate activation decision.
