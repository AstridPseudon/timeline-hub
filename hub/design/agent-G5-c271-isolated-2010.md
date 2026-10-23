# G5 c271 isolated-process qualification

Status: **FAIL; G5 remains DRAFT / gated:P1.**

The D21 fresh-process correction fixed the prior setup identity problem. Source
audit showed that `tests/helpers/runtime.py` caches pinned temporary archives in
`_ARCHIVES` and the first selected tree in `_exposed`; ordinary `use_runtime()`
then reuses `_exposed`. The independent c271-only process started with empty
caches, selected `/home/user/work/wt/rt-pin-2a9e347f`, and loaded
`runtime_protocol` from that same path. No SDK archive bootstrap was imported.

Report-all preflight passed against Agent f27d/tree
`cf7395cc986fab4d9c6feb48b5a0be69ef7eac30` and Runtime 2a9e/tree
`f79a2355cfb39d9ada7721978bd20d5702105778`; authentic archive SHA-256 was
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`.
Canonical readiness was schema 31, head pair
`a3e671256f1c42b8837d3e118c97b21b` /
`txn-11c90075be6c4c8bb9e2627366f0fe4f`, 3 shots, 3 internals, 5 CAS media,
registry present, 9 null values, no opaque keys, retained `word:word-1`, and
credential scan 0. The exact c271 body lock matched
`c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.

Exact collection selected 1 / deselected 0. The single execution reached the
unchanged test body and then failed at its first inverse undo (body lines
627–649). Runtime execution 2a9e returned a real structured 422
`validation_error`, reason `invalid_records`, with message:

> inverse stage native writes do not cover its authenticated effect image

The refusal was no-write with unchanged head and history. The test’s original
`WorkspaceClientError` diagnostic path re-raised the error, so later full
redo/overlap assertions were unreached. Observer teardown completed; there were
no observer failures or origin mismatches. This is an execution qualification
FAIL, not an import/setup mismatch. No source ownership is assigned here.

The lossless packet archive and manifest are in the worker evidence directory:

- archive SHA-256 `a8dcf1d1fe6c2ce6905749ea11fe96057b421f7497c0e233c13ca1e0182bc3d4`
- 14,794,303 compressed bytes, 85 members, 142,243,149 raw bytes
- observer counts: 73 seam entries, 69 exits, 4 real seam exceptions, 0 observer failures, 0 origin mismatches

`git diff --check`, vendor freshness against producer
`/home/user/work/wt/rt-pin-34eac004`, and `scripts/artifact_manifest.py --check`
all passed. No tracked edits, retry, prohibited suite, marker/body/helper
change, bypass, merge request, or activation was performed. See the worker
report and adjacent packet manifest for the exact commands and limits.
