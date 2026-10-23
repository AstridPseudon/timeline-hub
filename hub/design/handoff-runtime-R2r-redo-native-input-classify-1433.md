# R2r/R2 redo native-input classification — Agent-owned capture defect

## Result

**FAIL for the current redo positive; Agent owns the next repair. Runtime’s refusal is correct.**

The exact retained public redo reaches Runtime cfa0 and is refused at
`runtime_protocol/timeline_commit_auth.py:971` with:

```text
invalid_records: inverse stage write differs from its sequential input
```

This is not evidence of a Runtime guard bug, and no alias normalization by name
or equal payload is justified. The native capture is not an authenticated
representation of the exact canonical input image required by the redo stage.

## Exact source/history/input comparison

Evidence packet:

- `design/agent-R2-redo-media-1404-a29df82beb548306.json`
- size `1,481,631` bytes
- SHA-256 `a29df82beb548306683ab64d738eb776a519587fdb30cad3e997e91468621ef8`
- Runtime pin `cfa0af0d476e6954df041c08d7ef378fd6782932`
- source packet SHA `9603ca432b1c9d1c1b16908f00547d26da6d04df3ad681308cbae5f3e57635d1`

The accepted forward publication is `txn-7d039d147e1b4c5ba6cc7ca912b95cba`.
Its `fork-edit-0` `fork.source` binding authenticates:

- physical root `internal-revision:document-diff-e0c6162a4844471b99fd8d1076df92e9-internal-revision`;
- revision `document-diff-e0c6162a4844471b99fd8d1076df92e9-internal-revision`;
- content digest `sha256:0fd72e6d7c0c4ba0b477d39e9d1624e5ae3712ad596f0a6dd136bb30032f367d`;
- complete owners `{occurrence:f2-occurrence/shot, occurrence:shared-sibling/shot}`.

The same forward command’s authoritative `commit.effect` before binding for
`parent / occurrences / occurrence_id:f2-occurrence / shot_id` is:

- physical root `parent`;
- revision `document-diff-e0c6162a4844471b99fd8d1076df92e9-parent-revision`;
- content digest `sha256:d27b4d12889d6e8d76d6ac7f47668cff6c0e25b901a14ece5f4da6061853b74e`.

The accepted whole undo is publication
`txn-75285c95600949c8b1267a71f8e71a9d`, step `undo-0`. Its authoritative
`commit.effect` after binding for the same occurrence path is still the exact
canonical `document-diff-e0c6162a4844471b99fd8d1076df92e9-parent-revision`
and digest `sha256:d27b4d12889d6e8d76d6ac7f47668cff6c0e25b901a14ece5f4da6061853b74e`.
The stored source stage partition is complete and ordered:

| source step | source command ordinals | native writes | canonical effects |
|---|---:|---:|---:|
| `fork-edit-1` | `[1]` | `[0,1]` | `[0,5]` |
| `fork-edit-0` | `[0]` | `[1,3]` | `[5,9]` |

The redo request targets only that accepted undo. It has base publication
`txn-75285c95600949c8b1267a71f8e71a9d` and base revision
`document-diff-e0c6162a4844471b99fd8d1076df92e9-parent-revision`. Its single
redo stage is authenticated as source publication `txn-75285c95600949c8b1267a71f8e71a9d`,
source step `undo-0`, command ordinals `[0]`, native range `[0,3]`, effect
range `[0,4]`.

At the actual first mismatch:

- Runtime sequential input parent edge:
  `f2-occurrence -> document-diff-e0c6162a4844471b99fd8d1076df92e9-shot`,
  shot revision `document-diff-e0c6162a4844471b99fd8d1076df92e9-shot-revision`;
- its physical input images are shot digest
  `sha256:b977bb48d8bed9aca33bfbbce47c5dd0c68174fc1bb4403d3e4ecf140b5a074a`
  and internal digest
  `sha256:0fd72e6d7c0c4ba0b477d39e9d1624e5ae3712ad596f0a6dd136bb30032f367d`;
- the redo native write for
  `occurrence:f2-occurrence / [shot_id]` claims before
  `shot-placement-90b9827beed9a42dfba309ec7e05837ada743a57e18dd5f26704de552870c382`
  and after `selected-shot`;
- the redo effect after is the selected physical closure: parent revision
  `authoring-parent-revision-654f86c641c168806331405e773fddb80279366027b202d2d77d9d07995e27dc`,
  selected shot revision
  `authoring-shot-revision-e568be5951da3ce7c18cc871dbd1ce428cf55513582c5eafbd94364cf017fef4`,
  internal revision
  `authoring-timeline-revision-7a359d276a5221748b217fbe94b7b28bad96bd8fe5a8d4db98c75466c7cd4b56`;
- the selected physical shot and internal effect bindings are owned completely
  by `occurrence:f2-occurrence/shot`; the sibling remains on the document-diff
  physical closure.

The source undo record itself contains the inverse native write
`selected-shot -> shot-placement-...`; it does not contain an authenticated
binding whose `ref`, `physical_ref`, `successor`, or managed edge names
`shot-placement-...`. A complete scan of the retained accepted history found
no physical binding for that alias. Thus the packet does not prove that the
native alias and the canonical document-diff edge are the same exact
source-bound image. The mismatch is not resolved by matching payload bytes or
similar IDs.

## Ownership and bounded repair

Runtime’s current `_inverse_stage_boundaries` correctly authenticates source
publication/step/ranges, applies native writes sequentially, checks physical
shot/internal roots, owner sets, effect bindings, managed edges, and final
closure equality. `_inverse_stage_root` resolves aggregate roots through the
authenticated physical closure; `_inverse_stage_root_equal` only permits its
existing narrowly scoped aggregate representation rule. Store history
`_inverse_stage_history` and `_validate` preserve and re-authenticate the
authoritative records. No Runtime relaxation is warranted.

The current Agent source at `8c355a48...` / redo candidate `80523b472...`
leaves `inverse.py` and `_root_inverse.py` byte-identical. The only relevant
candidate change in `_commit_patch.py` is the restored-shot baseline carrier;
it does not authenticate or repair the occurrence `shot_id` native capture.
The bounded next seam is Agent `inverse.py` stage capture (`apply_inverse`’s
`_restore_write`/`inverse_stages` path): emit the occurrence edge from the
authenticated canonical source-bound edge used by the accepted history, with
the exact physical revision/digest/owner provenance retained. If the Agent
must retain the working alias, it must export a complete authenticated mapping
from that alias to the exact parent/shot physical root, including source
publication, step/ordinal, input head, revision/digest, owner and managed edge;
an alias-name or equal-payload conversion is not acceptable.

Next-worker controls must include the positive preview/forward/whole-undo/
exact-retry path only after this source repair, plus refusals for forged alias
mapping, wrong revision/digest, wrong owner or sibling owner set, wrong
publication/step/ordinal/range/order, foreign/stale history, unrelated payload,
and ABA/later-history cases. Preserve existing unknown-root, created-item,
range, managed-edge, source, foreign, stale, and no-write guards.

## Verification and limits

Scratch assertions passed for packet custody/hash/size, exact before/after
database/document/head/history equality, request/base and undo target, stage
ranges, canonical input, native write, accepted physical pins/owners, absent
`shot-placement` mapping, and credential scan. Ruff passed for the scratch
verifier. `git diff --check` passed.

No product files, tests, schemas, clients, pins, contracts, config, env, or
Git refs were changed. No public redo rerun, new body, full suite, browser,
native14, matrix58/40/281, P1/P4, or typecheck was run. Typecheck is N/A for
this read-only classification. The public packet’s retained SQL/document/head/
history all remain unchanged after the refusal.

This is a report-only handoff; **NEVERMERGE**.
