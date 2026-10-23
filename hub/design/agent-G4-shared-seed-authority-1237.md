# G4/A3/P2 shared popup source qualification

## Decision

**NO QUALIFYING EXISTING SOURCE. P2 remains blocked at the fixture seam.**

The exact popup source is not present in any retained authenticated backup or
realm that I could qualify for normal read-only admission. No source was
copied, reconstructed, imported, or mutated, and no product or fixture file was
changed.

The missing capability is specific: an authenticated v2 semantic placement
that adds a new occurrence membership/placement while retaining the exact
source occurrence's existing shot, shot revision, internal revision, media,
variant/raw-registry bindings, IDs, order, opaque fields, and project/timeline
scope. Current `occurrence.create`, `occurrence.duplicate`, and
`occurrence.fork` do not provide that operation; `doc.patch` refuses managed
occurrence membership. The current `timeline.duplicate` is a whole-timeline
copy into an empty destination with fresh injective maps and is not an exact-ID
importer.

## Required source and observed source

The App caller at
`/home/user/banodoco/reigh-app/tests/e2e/local/three-products.p2-popup.spec.ts:209-272`
still constructs the required state by posting the retired
`composition-revisions` route. It clones the selected source occurrence,
creates `f2-occurrence-copy` at `start_ms: 12000` with the same
`shot_id`/`shot_revision_id`, imports old media, updates the child raw registry,
and preserves the opaque `p2_popup_opaque` value. This is the exact state that
must be reproduced; an isolated duplicate is not equivalent.

Runtime 1109/1112 evidence was applied as settled: the supported public path
creates and edits an empty timeline; an authenticated pre-cut backup may be
used as disclosed private setup, but it is not a public complete-fixture
importer. The 1222 independent seam review confirms that all ordinary public
seams fail to create this shared membership edge.

## Retained-backup audit

I inspected the Runtime fixture archives in both `/home/user/work/runtime` and
`/home/user/work/wt/rt-pin-3b926efa` without changing either tree. Across the
12 unique archive names, every archive containing `backup/realm.sqlite3` was
read through a temporary read-only SQLite connection with `PRAGMA query_only=1`.
Search covered all textual SQLite columns for `f2-occurrence-copy`,
`occurrence-copy`, and `12000`, and inspected occurrence rows, parent payloads,
dependency manifests, history, objects, and generation tables. No archive
contained the target marker or placement.

The canonical `tests/fixtures/precut-v31.tar.gz` is authentic backup material,
but it is the unrelated synthetic film realm:

- manifest schema 31, realm `synthetic-film-realm`, database SHA-256
  `49fbca3d0fc2285c398eb9e8060d5706251399676446ec48015eda18d5bb433c`;
- five managed CAS objects (three distinct video objects, one audio object,
  and one transcript object);
- one parent revision with three distinct occurrences at 0, 1650, and 3300 ms
  on `shot-1`, `shot-2`, and `shot-3` respectively;
- no `f2-occurrence-copy`, no 12000-ms placement, and no shared physical shot
  pair for the popup.

One retained D17 test realm was a near-match:
`/tmp/agt-D17-integrated-1053-40/test_repeated_source_copy_real0/saved-source/realm.sqlite3`
(read-only SHA-256
`46c61b95ab811f41d972fd5800032dfd6209a0730fd0ae73d7717c4b3fb10bbd`). Its
`saved-parent` has `occ-film` at 0 and `again` at 12000, sharing `shot-film`
and its `internal-film`; the parent digest is
`sha256:5d0758fef092b6a898335fc3c336115e132271f2103408e62750fea8201379b2`.
It is not usable for P2: the IDs are not the original popup IDs, the parent
has empty `clips` and `registry`, its commit manifest has `media: []`,
`generation_variants` and `generations` both have zero rows, and the retained
admission marker says `active_verified: false`. Its history explicitly labels
the source publication `trusted-test-setup-1`, not a normal production
authenticated admission. It is evidence of a test semantic shape only, not
authority for the popup media/variant/raw-registry closure.

## Existing path disposition

The current Agent head is `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`; the
Runtime qualification pin is `3b926efab2eed122d374540baee297d4cdcec62a`.
Source inspection confirms:

- `doc.patch` rejects managed occurrence membership;
- `occurrence.create` creates a new shot and occurrence;
- `occurrence.duplicate` copies into a fresh shot identity;
- `occurrence.fork` copies/re-homes a shot for one existing occurrence;
- `timeline.duplicate` requires authenticated source closure, raw-media
  capture, an empty destination, and fresh injective maps.

The Runtime source-closure and raw-media checks are useful prerequisites, but
they do not authorize a same-physical-shot second occurrence in the current
provider command set. The retired route remains denied. No old-route call,
store injection, fabricated manifest, guard weakening, or unsafe authority
reconstruction is acceptable.

## Decision question and unapplied minimal extension

Before any implementation, the orchestrator must decide whether to authorize
one new semantic capability in the existing v2 `TimelineSession.submit` /
outbox path: **authenticated shared-occurrence placement**. The operation
would accept a source occurrence reference and destination placement/identity;
Runtime would resolve and recheck the source revision/publication/content
digest, complete closure, media/variant/raw-registry custody, and destination
scope, then let the provider add only the new occurrence membership while
retaining the source physical shot/internal identity. The returned canonical
document must retain original IDs/order/scope and all opaque data.

This is a proposal only and is **UNAPPLIED**. It must preserve the full v2
base revision/publication pair, commands, label, per-step patches and ordinals,
merge mode, declared reads, idempotency key, dry-run, source/rationale/group_id,
and accepted/merged/conflict/invalid/preview response fields. If the
orchestrator does not authorize this scope, P2 must remain held; App must keep
the faithful fixture expectations and the retired route must remain stopped.

