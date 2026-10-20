# Runtime review: Agent full ordinary/carrier source union 357

Date: 2026-10-20 UTC

## Decision

**Agent source union: APPROVE for technical source review, with no native or
generation approval. Runtime counterpart/native pair: REJECT/HOLD as presented.**

The Agent source is the required new union. The available Runtime carrier is
still the older 3730/f802 pair and is not a counterpart for 357. It must not be
used for the one native pair, and no normal private generation, version freeze,
pin, release, or adoption is approved by this review.

## Exact sources and hashes

- Agent source: commit `357230816c86da65d5f8cc92b10a3a90d29874e0`, base
  `3c4f6de4fa777323b3386c01c7266b619b86af6d`, expected harness tree
  `94692ec85167d5c606626c4ec678fe2a63ee0aa5`.
- Agent canonical private schema:
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`;
  55 definitions, 29 operation clauses, 13 v2-capable source-bound ops.
- Agent carrier source
  `astrid/sdk/timeline/_materialization.py` SHA-256:
  `d83c8b5a10878c61b4bcba81cd5ae29666a62a5d57cf7e65ddd33f716043aaec`.
  It is byte-identical to the reviewed carrier in 3730.
- Assigned Runtime base: commit `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`,
  tree `94c5ffbc0b636e25475c0f351bfb384dd06ee8ab`.
- Available Runtime carrier candidate: commit
  `7b8d6d9afe963e2b7a6c6b32fd4e3797451090da`, tree
  `d20b745c26a33c2ea4e20863f846335c8cf33e1e`, based on 83fe rather than the
  assigned current e2 source.
- Candidate Runtime schema is the old private
  `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`
  (48 definitions/22 clauses), and its packaged bundle is
  `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425`.
  Candidate materialization helper is
  `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb`.
- Current e2 Runtime public schema remains
  `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`;
  current bundle is
  `e0cc63576c17f73d6d5855d0ef6ab2e441f3db67b5e07596e8ed7c0ff4f0e4c9`.

## Agent source findings

The source union passes the required containment checks:

1. Removing only the reviewed carrier widening reconstructs ordinary schema
   SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
   exactly, still with 55 definitions and 29 clauses. Each source-bound
   operation has the old v1 branch plus the equivalent v2 branch; `track.create`
   remains the deliberately open v2-capable case. The v2 set is exactly:
   `clip.move`, `placement.move`, `track.create`, `clip.set`,
   `clip.set-element`, `track.set`, `shot.set`, `clip.set-params`,
   `occurrence.add-media`, `occurrence.swap-media`, `placement.create`,
   `placement.unplace`, `shot.pool`.
2. The committed Agent tests reconstruct the reviewed private f802 schema by
   exact replacement and check compatibility against every prior published
   floor. The seven added ordinary operations/definitions absent from f802
   are retained by 357; no old private 10c source was adopted, and no group
   operation or invented 31-operation claim appears. The closed inventory is
   exactly 29 operations.
3. Ordinary semantics are widened, not rewritten: `equal()` keeps numeric
   equivalence while explicitly refusing boolean/number coercion; tagged
   absent/present state keeps null and presence distinct; item identity is
   added as a separate address. The source-bound materialization tests cover
   numeric-vs-boolean changes, null/presence, opaque secondary `id`, canonical
   `item_id`, source/owner/item bindings, and typed semantic births. The
   materialization path never treats a derived physical allocation as
   `create_entity`.
4. Public v1 positive capture remains exact (the 103-read/3-selection cases),
   including accepted retry/history/inverse/redo/restore controls. An obsolete
   new submission with an old sealed v1 capture still refuses with the draft
   and durable outbox unchanged; it is not silently upgraded. Current v2
   replay checks exact source maps/bindings and rejects missing, forged,
   incomplete, or caller-supplied proof. The detached accepted-history tests
   are not native Runtime qualification.
5. The Agent handoff reports overlapping focused lanes of 148, 349, 57, 66,
   22, and 249 passes; these counts must not be summed. It reports no full,
   native, generation, release, pin, or integration run. This review agrees
   that the Agent manager must provide the exact committed successor/tree and
   freeze ACK before normal private generation.

## Runtime counterpart findings

The candidate Runtime join design is technically compatible with the unchanged
214-line Agent carrier: its `materialization_join` validates source/parent
pins, owner/item bindings, source item maps, immutable closure reads, typed
birth separation, result maps, own-slot reuse, global item reservations, and
ledger-first accepted replay. The catalog-head fence in 7b8 is also the right
additional guard for current, inverse-source, and accepted-historical slots.

It is nevertheless not acceptable as the current counterpart:

- Its schema is f802/48/22, while Agent 357 is 613/55/29. Relative to 357 it
  lacks `AssembledTargetArgs`, `ClipAddMediaArgs`, `ClipAnchorArgs`,
  `OccurrenceCreateArgs`, `TextBindingSetArgs`, `TimelineInitArgs`, and
  `WordAnchor`, plus their seven operation clauses. A Runtime generated from
  that artifact cannot admit the complete ordinary 357 union.
- The candidate was composed before current e2. Comparing candidate 7b8 with
  e2 shows it removes the current selected-media CAS-byte verification from
  `RequestCommitPort`/`MediaReads`; this is the `3021a5b` protection and its
  neighboring replacement tests and must survive. It also predates the
  current catalog-text replay fixes and later parent-marker/current-main
  changes. No wholesale candidate port/store/service replacement is safe.
- The current e2 tree does not contain the source-bound helper at all, so the
  counterpart must port the narrow join/port/store changes onto e2 while
  preserving e2's current service and test bodies. Future composition must
  also retain the separately reviewed raw-media exact-base feature
  `dcac221296ef2c73e02d30534effb2a09d9a91bd`/`7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`
  and the strict D05 parent-swap route checks (`d05e638`/`a18022d`), rather
  than regressing them while carrying the materialization store changes.
- The candidate's bounded native controls were against Agent 3730/f802 only.
  They do not establish the requested 357 native lifetime: accepted-v1
  ledger-first retry after lost ACK/restart, inverse/redo/history/restore,
  obsolete-v1 refusal with draft preservation, current-v2 acceptance, own
  slot/sibling/global-item/catalog-head occupancy, dependent-B ACK identity,
  and retained ordinary operations.

## Minimal Runtime counterpart delta

1. Start from assigned current Runtime e2, not from 7b8's older parent. Port
   only the reviewed source-bound join, authenticated result-map/closure
   validation, own-slot/item/global occupancy checks, and catalog-head fence;
   preserve current CAS, catalog-text, parent-marker, raw-base, service, and
   strict D05 paths/tests.
2. Replace the private Runtime command-schema resource and its bundled closure
   with the exact Agent 357 schema `613123…aaad`, retaining all 55/29 ordinary
   definitions/clauses and the same 13 v2 operations. Run normal private
   generation only after Agent supplies the exact manager freeze ACK. Do not
   bump or publish a public version, pin, release, or artifact adoption from
   this review.
3. Retain the old schema syntactically for the obsolete-v1 refusal path and
   ledger-first accepted retries; refusal must preserve the exact draft. The
   one actual native pair must be generated from 357, never 3730 alone, and
   must use the Runtime counterpart after a fresh committed peer review.

## Evidence and limits

Direct review probe:

```text
Agent schema reconstruction from git show 357...:
ordinary SHA-256 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d;
55 definitions / 29 clauses; 12 closed source-bound clauses plus track.create.
```

Runtime targeted evidence run from assigned worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/rt-review-schema-compat tests/test_command_schema_compatibility.py
130 passed in 39.23s
```

No full suite, socket/browser suite, duplicate native execution, normal
generation, version freeze, pin, release, or integration adoption was run.
The Agent focused results above are handoff evidence, not rerun here. The
Runtime candidate source and Agent source are therefore technically reviewed,
but the required exact 357 native pair remains unverified and held.
