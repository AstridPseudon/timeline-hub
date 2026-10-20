# Runtime a6a private contract review

## BLOCK

Reviewed private Runtime commit `a6a11a806a51262192447fdeccc726b01ffd78fb`,
tree `8c027992e34ddf9a940d3e90cd38f7b9e11e4c25`, against current Runtime
`cc3796a0c333b956b171c68dc876d41f40f6219f` and Agent commit
`357230816c86da65d5f8cc92b10a3a90d29874e0`, tree
`94692ec85167d5c606626c4ec678fe2a63ee0aa6`.

### Blocking finding

The generated Python/TypeScript command shapes contain an `Any`/`unknown`
escape for closed operation-level `intent` objects. The frozen Agent
`clip.delete` clause requires `intent` to be an object with
`additionalProperties: false` and no properties. Runtime generation emits:

- `runtime_protocol/timeline_commit_types.py:117` — `EditCommandVariant1`
  has `intent: dict[str, Any]`.
- `packages/typescript/src/timeline-commit-types.ts:115` — the same branch has
  `intent?: { [key: string]: unknown }`.

Thus generated static clients admit arbitrary intent keys although the source
schema and Runtime validator refuse them. This fails the required exact
Python/TS shape and “no Any escape” review criterion. The generator needs a
closed empty-object representation (and a focused negative generated-type
test) before this artifact can be approved. This is the only blocking finding
from this review; no product code was changed.

### Verified evidence

- Normal provenance is hash-bound: `generators/agent-command-source.json`
  names Agent `357230816c86da65d5f8cc92b10a3a90d29874e0`, tree
  `94692ec85167d5c606626c4ec678fe2a63ee0aa6`, path
  `astrid/core/timeline/schema/edit-command.schema.json`, and SHA-256
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`.
  The Runtime schema is byte-identical: 82,018 bytes and the same SHA-256.
  `generators/generate.py --check` passed.
- The frozen source has exactly 55 definitions and 29 operation clauses. The
  actual v2-capable operations are exactly 12 (not the claimed 13):
  `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `clip.move`,
  `occurrence.add-media`, `occurrence.swap-media`, `placement.move`,
  `placement.create`, `placement.unplace`, `shot.pool`, `clip.set`.
  `track.create` retains its open string version as frozen. Generated Python
  and TypeScript each contain all 55 source names and 41 command branches.
  The 12-versus-13 discrepancy is reported here for Agent correction; the
  frozen schema was not changed.
- `MutationReceipt` remains the exact existing v1 alias: timeline schema
  `$defs.MutationReceipt` still references
  `CommittedMutation/properties/receipt`; generated Python preserves the nine
  fields and `project_seq: list[int]`, while TypeScript preserves the bounded
  `[number, number]` tuple. `CommitRequest.api_version` remains literal `1`.
  The existing worker evidence reports 218 generator/compatibility tests
  passed, including all five historical floors; those broad tests were not
  rerun per brief.
- Current CAS/catalog/door/service guards and the C4, headless, task-replay,
  verified-media, and null-speed regression files are byte-unchanged from
  Runtime `cc3796a0`. The new raw-media path retains exact base-pin,
  project-managed-object, descriptor recheck, and finite-positive WAV header
  duration guards; the worker evidence reports the focused 645-test selection
  and central 131-test selection passed. No full suite was run.

### Commands run by this review

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check  # 0
git diff --check                                                                            # 0
```

Independent read-only probes also confirmed schema byte identity, the 55/29/12
inventory, all source names in both generated languages, and the Python
`EditCommandVariant1.intent` broad-map type shown above.

