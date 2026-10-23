# Runtime R2r leaf inverse review 1334 — FAIL

Reviewed exact candidate `6e256ea3d2786581525bafbc2e4f343c60ef6a03`
(tree `09789d08d2b70bf4134ab5ccba836a1d286ab062`) against base
`8592822fd11275540f596562f43c715676f2bc0f` (tree
`ed9856f43a4e44a058bf2230badea2c4c7080050`). Verdict: **FAIL; no merge and
no whole undo/redo credit**.

## Blocking evidence

The added `test_captured_leaf_inverse_materialization_turnover_is_authenticated`
does not load the actual package. Its helper at test lines 275–366 reuses
captured IDs but invents internal/shot/parent/unrelated payloads, closure roots,
digests, and source history. Actual package:

- `agent-R2-leaf-1246-e97f81ce7c350f08.json`, SHA-256
  `1123978b7b18c59d280f73c9ad9155b5ba18d0c64b24e45b8bdd02af30a887b0`;
- manifest SHA-256
  `803c11e3e9bd1c4a8794365f7ce11574a7224bd2f735aaafc7ec2ce942cdfc74`;
- actual stage image hashes: `request`
  `9513a98ac9413e4395632693701c664db3557c61e5ed150ca1875a4885e50b5b`,
  `prepared`
  `bd78bb8ffa030ccadddeebe62bec56ab9fa7623232c6e0c4d759523048d92afa`,
  `history`
  `0122a97346985a270f38b2e9f49819a28399f4f7faa3e9821622d85b2447897e`.

Actual `stage_before`/`stage_after` have five roots and 9,059/9,052 compact
JSON bytes. The helper has four roots and 1,651/1,664 bytes. Actual history is
`fork-edit-0` / `occurrence.fork` / ordinal `[0]`, then `fork-edit-1` /
`doc.patch` / ordinal `[1]`; the helper invents only a `doc.patch` at ordinal
`[0]`. Its binding digests therefore do not prove the actual physical images,
parent pin, sibling/unrelated closures, or actual source-step lookup.

An independent in-memory probe proved only the synthetic boundary:
old `8592822fd` rejected with `inverse stage native writes do not cover its
authenticated effect image`; candidate accepted. Direct comparisons of helper
before/after images to the actual package were false. The eight negative cases
also run only against this synthetic closure and omit the required combined
effect-image+binding forgery and equal-payload foreign-owner swap controls.

## Remaining retained failure

The exact retained whole-undo request targets publication
`txn-1c5db05293e34736a5207e6f07c3818f`. `service-03-error.json` durably says:

```text
status=refused reason=invalid_records
message=inverse stage native writes do not cover its authenticated effect image
conflicts=[] base=null current=null
```

`service-03-after.json` preserves the unchanged head and canonical document.
The prior actual diagnosis locates the remaining stage at Agent source step
`fork-edit-0`, native range `[1,3]`, effect range `[5,9]`: the Runtime owner
`runtime_protocol/timeline_commit_auth.py:_inverse_stage_boundaries` still
fails on the later aggregate/root sequential input after the leaf turnover.
Agent's captured final canonical document exactly matched the original, so the
smallest correction is a bounded Runtime aggregate/root materialization proof
using the exact authenticated stage images and owner/pin/digest/closure guards.
Do not add fabricated root writes, normalize pins, or weaken guards.

## Checks

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_source_duplicate_authority.py
170 passed in 56.38s; 0 skips reported

/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
All checks passed

PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python /root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py
0 errors, 0 warnings, 0 informations

git diff --check
passed
```

Base and candidate production Pyright both had zero diagnostics. Original test
function ASTs are unchanged (17 common bodies); only three new functions were
added. Current `9c694858e` source/allocation guard paths have no diff. The
candidate changes only the two authorized paths; no separate 77-path manifest
was included in this leaf packet, so no standalone 77-item count is claimed.

No full, browser, native14, original20, P1–P4, or live known-failing retry was
run.
