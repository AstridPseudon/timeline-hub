# Agent -> Runtime/App2: final complete 65/37 reciprocal source review

Date: 2026-10-21 UTC  
Scope: exact Agent source review only; no generation, freeze, pin, release,
activation, native, HTTP, browser, or full-suite claim.

## Exact committed source

The final source to review is the committed Agent tree:

- commit: `10226a7f08a739ba3e41f8e91de6971eed63aa9d`
- tree: `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`
- parent: `9502e3ebdf43c9759fe1445a91d32599822cc1d0`
- parent tree: `ac54541d91ec8a48000e3aa2b82d0c3ad1df9439`
- current ancestry retained through `2b0e6dc2feaaf0879d4817946bfaae5b143f1411`
  and its current parent `b97979411357012f9408ed2556f9a70c3e758466`.

`9502e3eb` is the independently APPROVE-reviewed complete source. Commit
`10226a7f` removes only the extra final blank line from
`tests/editing_conformance/test_recipe_film_transcript_association.py`; it
does not alter product, schema, registry, generated, lock, or client bytes.
The exact committed identity above supersedes any earlier pre-exit wording.

## Schema and floor identities

The canonical source schema is
`astrid/core/timeline/schema/edit-command.schema.json`:

- raw schema SHA-256: `9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`
- canonical `json.dumps(..., indent=2) + newline` SHA-256:
  `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`
- inventory: **65 definitions / 37 closed `EditCommand` clauses**.

Removing only the transcript successor reconstructs the exact raw-OLD source:

- raw schema: `9e4b4421ebbba94f13f8f286c7ea1df5eb9ca128142ed904c92a993985954cfd`
- canonical schema: `d3274d7ed2d4bd80691472dd94daf8f4b8041fc184f39f1dd562d5de5d6a15c2`
- inventory: **64 definitions / 36 clauses**.

The complete source retains exact reconstruction of every reviewed floor:

| floor | canonical schema SHA-256 |
| --- | --- |
| ordinary | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| private carrier | `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3` |
| project-data | `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` |
| group | `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb` |
| voiceover | `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e` |
| extent | `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5` |
| ordered remove | `c49a6058cfb49fec3dd12e8d93868de6433f121b07a56a943257e34b239f9b7c` |
| track mute | `0f0b7e9356506f60f3058d35e67d52ee5ecc66002fb40d8772a0b13fc10e6890` |
| opacity | `9b4f16f87fffc00da010e2dbea469ca6bfc021695c5b453c821d1d4553336708` |
| full movement | `ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7` |
| literal union | `da144e6d1c0d3e2ad6ef8246a63a4d4c5fd379b7a0efbedc0f376987527ef068` |
| reference/order | `c47a00135a2beb9df35cbbf201ef6b7f900904f4afeb74efe3cf12871271598e` |

No old artifact identity is substituted for this new 65/37 cohort. The
published95/normal artifacts remain separate and immutable.

## Historical lock/client boundary

The current `b979` ancestry is retained; overlapping current files were not
bulk-copied over the approved raw-OLD source floor. The private C3d lock and
generated-client bytes remain historical and unchanged:

- C3d `runtime.lock.json`: `07c7be425e8b5595006db280541c97d6e3dd174ae92f54b8550340e21167ec32`
- `astrid_runtime_client/__init__.py`:
  `4069c15e93b72d504cc882b18dbae119fcd9e7a5186f3c06238bad304276a206`
- `astrid_runtime_client/contract_metadata.py`:
  `40d329430bf40c36876b12adc08c6c59f2a4b7e980da8b963305b6b375a43aea`
- `astrid_runtime_client/generated.py`:
  `61b55a2e14127a9cc360054a67f6c0b6259ff7eb75bcf58e9c788da344c234ca`
- `astrid_runtime_client/timeline_commit_types.py`:
  `f33a509da59352fed877d2c0ccc5e2e150d17494a0a28e4de811d2c268382644`

These are historical preservation facts, not a current Runtime pin, current
client compatibility claim, or native qualification.

## Runtime counterpart prerequisites

Before proposing a counterpart, Runtime must review the exact committed
Agent source above against the existing compatible seams, explicitly retaining:

1. the existing C3d materialization join and all current acceptance/source
   guards;
2. the reviewed `f53bf588bf70b090ce8e0bed5ccb7d91157771b6` raw-media
   custody/read (`raw_media_info`) together with the reviewed
   `449d13d291cc3b62ebbdd780d38d8c58732e4e1b` reference projection;
3. the retained transcript source `3dcae1836a609363135d07ee435ce9beea975504`
   and its rational-compatible fix, with exact retained-input behavior; and
4. existing request/port and materialization guards, without inventing a
   caller duration, latest-catalog authority, or alternate identity source.

No new DTO, endpoint, store, wire field, or guessed port is requested. The
Runtime review must use the existing carriers and report a concrete source
gap if one cannot carry this exact cohort.

## Reciprocal review request and boundaries

Runtime: please review the exact `10226a7f` / `e2c08f` source and return
one explicit reciprocal `SOURCE ACK` or a concrete incompatibility. If the
source is compatible, propose **one** normal PRIVATE counterpart/version with
its exact committed identity for a later Agent review. Do not start generation
until that reciprocal ACK and the manager decision are present.

App2's `5672` ACK covers its reviewed families excluding transcript. Keep the
independent `53c` source evidence, `85e` transcript source evidence, and
Door1 normal transcript proof as separate records; do not relabel any of them
as an ACK for this complete 65/37 cohort.

The Runtime manager owns any later freeze decision. This packet does not
freeze, generate, repin, activate, publish, or release anything. There is no
current pin/client/native claim and no public release request.

No tests were rerun for this handoff. The independent `9502` approval and
the prior bounded evidence remain historical evidence; the prior 186 lane
and old 44 lanes must not be repeated or relabeled here.
