# Agent review: ordinary014 corrected public exports

## Verdict: APPROVE

This approves the corrected unpublished Runtime ordinary014 successor for
staging review only. It does not approve a consumer pin, merge, publication,
activation, or release.

### Candidate identity and scope

- Runtime commit: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
- Runtime tree: `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- Parent: rejected `806636baf42e9ed1e4c7f9fe76c3e14d7330fcc1`
- Frozen Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`
- Frozen Agent raw schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- Runtime schema digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`
- Corrected artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`
- Corrected `contract/artifacts.json` hash: `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`

The committed diff is limited to the four intended paths: the authoritative
Python initializer template, generated Python initializer, artifact manifest,
and the existing current-union contract test. No HTTP route, DTO wire shape,
provenance/source factory, private carrier, audio/producer path, or server
ancestry/interface changed. The old public 0.2.13 fixture and floor are
untouched.

### Schema, operations, and exports

The corrected Runtime package contains the frozen Agent schema byte-for-byte:
55 definitions and exactly 29 operations. The operation set is the frozen 22
plus exactly these seven additions:

`timeline.assembled-target`, `clip.add-media`, `timeline.init`, `clip.anchor`,
`occurrence.create`, `clip.swap-media`, `text-binding.set`.

The restored test asserts set equality (`==`), not a subset or count-only
condition. The unconditional public DTO identity assertion is restored. All
seven new definitions are publicly exported and identity-match the DTO module:

`AssembledTargetArgs`, `ClipAddMediaArgs`, `TimelineInitArgs`, `WordAnchor`,
`ClipAnchorArgs`, `OccurrenceCreateArgs`, `TextBindingSetArgs`.

The artifact manifest has 75 entries; comparison with the rejected parent
shows only the intended generated initializer hash changed among protected
artifact entries. Normal generation and artifact checks are coherent.

### Evidence

Ran independently against an extracted immutable copy of commit `a0dca169…`:

- Public Python import/identity, raw-schema hash, exact 55/29 inventory, and
  75-artifact/version/file-hash probe: **PASS**.
- `python generators/generate.py --check`: **PASS**.
- `python scripts/artifact_manifest.py --check`: **PASS**.
- `pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_current_union_contract.py`:
  **64 passed**.
- `npm test --prefix <extracted>/packages/typescript` with the shared
  node_modules used read-only: TypeScript build, strict public API compile,
  and both Node tests **PASS (2/2)**.
- `git diff --check` for rejected parent → corrected commit: **PASS**.

I inspected, rather than duplicated, the existing candidate evidence: central
commit integration **9 passed**, central TypeScript check **61 passed**, and
the frozen Agent ordinary native cohort **11 passed**. The peer Runtime review
also records the central generated-client coverage for the five worker-local
socket failures; those local failures are sandbox-only and do not invalidate
the socket-capable central result.

### Separate current-Agent qualification boundary

The frozen consumer constraint is Agent `310e…` / raw `6ba7…`. Current Agent
`8130a401` has a different raw schema (`sha256:a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`) and current P1 authority work. This review does not compose or qualify
that newer Agent authority. The Agent manager must perform the normal
current-Agent compose and actual consumer qualification separately.

### Newer Runtime work not included

This successor is not the current Runtime integration head and does not include
later catalog work. In particular, these remain separate and must be handled by
the Runtime owner before any final current-tree pin decision:

- `4c1a1a30a6dfed4b1d0c7674fe6f8bfc23aab15f` — project catalog candidate
  promotion restoration;
- `d037368d22373be92c1e4c1a821315a1130fdcff` — unplaced shot text-binding
  restoration;
- `cd6e9c7d2862ae7ece5f64dc931eebff9dd93160e` — native clip media-replacement
  positive coverage.

The current `c45cbc6` integration also contains test-only work, including
`37c4304`'s 125-line historical render-admission retry test; that test-only
delta should be forward-ported/reconciled before merging this candidate. No
product-file divergence was found in the corrected export repair itself.

### Peer Runtime ACK and limits

Peer Runtime final review `runtime-ordinary014-corrected-final-review.md`
independently **APPROVEs** the same committed SHA/tree and records the 9/61/11
central/native evidence. I ACK that peer result for this bounded export review.

No full suite, live current-Agent composition, newer catalog qualification,
consumer pin, merge, publication, or release claim was performed. Recommended
next step: reconcile the current Runtime test-only/catalog work, then let the
managers run the normal current `8130a401` Agent composition and pin gates.
