# PASS — R1/A3 integrated fork proof (`900ba8f09`)

This is a read-only integrated-tree review. No source changes were made.

## Tree and merge provenance

`900ba8f09cff705b5d2db8d31021e4c2ad3f7786` has tree
`4bd98aad458f267521946ce183aa0700091ed5ed` and parents
`bf40d6bb5923210a3f5d210414c9ad737b40403d` plus reviewed
`1f418aea45c70bff3d8517b506c72cf8b230060e`. `1f418aea4` is exactly one own
commit over `bf40d6bb5`; `git diff 1f418aea4 900ba8f09` is empty and both trees
are identical. The merge contains exactly 13 reviewed fork paths and no
schema/generated/pin/lock/artifact/Runtime/App/Composition production paths.
No test weakening was detected.

The source manifest from `agent-A3-occurrence-fork-call-0504.json` recomputes
to exact source-set SHA256
`e7c96edb911f6a1d89fb218cc951fea6094ee350f2ab62cbf039f951239e6830`, with all
10 per-file hashes matching. The current production registry maps
`occurrence.fork` to `native_occurrence_fork.occurrence_fork`; Agent imports
are from the integrated worktree.

## Evidence

- Fork/recipe command using explicit frozen Runtime pin
  `/home/user/work/wt/rt-pin-34eac004`: **25 passed** in 3.83s.
- Scoped Ruff: **PASS**.
- Normal Ruff via persistent `venv-agent`: **2150/2150**.
- Scoped mypy via persistent `venv-agent-typecheck-v2`: **10 files, no issues**.
- Normal mypy baseline: **1915/1915**.
- Vendor lock, artifact manifest, and diff checks: **PASS**.
- Prior independent exact-tree evidence is reused for actual RuntimeService:
  **1 passed**, with Runtime archive `be5848e17fbf...` byte-verified against
  Runtime commit `be5848e17fbf68100286114883f5820fe4755911`. That private
  archive is absent now; because the current tree is identical to `1f418aea4`,
  no second service run was warranted.

## App handback

```json
{
  "schema_version": 1,
  "op": "occurrence.fork",
  "version": "1",
  "select": "occurrence:occ-0",
  "args": {"shot_id": "shot-fork"},
  "intent": {"ownership": "occurrence"},
  "created": ["shot:shot-fork"]
}
```

The destination shot must be reserved once; the exact request body and
Idempotency-Key must be retained across retries. App sends the complete v2
scope/base, label, steps (including patch/reads), merge, request reads,
dry-run, source/rationale/group_id controls. Only the reserved shot created
claim is allowed; no created occurrence, edge patch, duplicate/delete
sequence, or new Runtime tuple.

Retained checks: `5292b388a...` is an ancestor; `runtime.lock.json` retains
normal Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`; frozen schema hashes
are `d106dfe8...` for `edit-command.json` and `07613763...` for `run.json`;
both protected test files from `f2521256c...` are byte-identical. G234
`31a5e8d3c` is not an ancestor and remains a separate review, not integrated.

This report makes no mounted App/shared-HTTP/H3/full-suite claim and does not
waive the separately owned Runtime inverse issue.
