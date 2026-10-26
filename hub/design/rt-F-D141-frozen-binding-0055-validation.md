# D141 frozen Farm source binding validation

Status: `SOURCE_BOUND_VENUE_NOT_READY`.

## Source and custody

- Read-only `git cat-file -e` and `rev-parse <commit>^{tree}` checks pass for
  all four approved commit/tree pairs in their owning repositories.
- The normal `queue/done` checkout receipts were read, not fabricated, for
  Agent and Composition. Exact Runtime and App checkout receipts are not yet
  present; their commit/tree objects are present, so those venue bindings
  remain unbound. No stale `/home/user/work/{agent,runtime,app,composition}`
  checkout was substituted.
- Agent `runtime.lock.json` was read from the approved commit: blob
  `2d4d12a1…`, SHA-256 `0cc3ba73…`, 3577 bytes. The 15 canonical mappings,
  hashes, bytes, and modes remain unchanged; only producer provenance moved to
  Runtime `6a011d58…`.
- Runtime `contract/schemas/timeline-commit.json` was read from the approved
  commit: blob `d94415a7…`, SHA-256 `3654ca3c…`. It is byte-identical to the
  historical f103 C0 schema; no request/reply field or shape was changed.
- The `4c/ab1e` canonical census remains historical supporting evidence only;
  it is not relabelled as a D141 census.

## Commands and results

| Command | Result |
|---|---|
| `pytest -q ops-d140-farm/test_recipe.py` | PASS — 97 passed in 186.44s |
| `bash -n ops-d140-farm/receive-farm.sh` | PASS |
| `git diff --check` | PASS |
| `jq empty evidence/source-manifest.json` | PASS |
| source-object/tree, blob, SHA-256, parent, origin and receipt readback | PASS for available objects/receipts; missing Runtime/App checkout receipts remain declared |
| old-head negative receiver control | PASS — stale Agent/Runtime/App pins are absent from the production receiver and the private custody suite leaves request routes uncalled |

No Farm census, child request, import check, controls body, service, Store,
core suite, package acquisition, network, or full suite was run.
