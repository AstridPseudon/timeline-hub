# D139 return review — FAIL / sourceNOT_READY

## Decision

FAIL. The maker/source security correction is materially present and the exact
candidate and f07 preimage match the requested bytes. The review cannot pass
because the canonical Agent 2149 census is not accepted by the checker, so the
claimed exhaustive import coverage is not actually wired. Separately, the
owner-approved D73 carrier remains absent; production admission must remain
`sourceNOT_READY`.

## Open finding

### CENSUS-005 — blocker — canonical census schema mismatch

The exact canonical input
`agt-F-D139-import-input-census-2149-input-census.json` contains 1,146 rows
with `module`, `category`, `distribution`, and related evidence fields. The
production checker `ops-child-custody/check-child-imports` accepts
`--census-file` rows only when each row has a string `name` (and defaults its
classification from that field). Running the exact canonical input produced:

```text
check-child-imports: error: census rows require a string name
STATUS=2
```

Thus the author’s `imports-summary.json` assertion that the merged census was
consumed is not independently reproducible from the canonical input. The
focused tests cover a hand-normalized synthetic census, not the actual 2149
packet. This is a source/evidence integration defect, not a reason to treat
the synthetic result as canonical coverage. The checker needs an explicit,
tested adapter for the 2149 schema or a canonical normalized artifact whose
provenance and complete 1,146-row equality are checked.

## Security disposition

The following 2212 findings were independently rechecked as addressed in the
production maker:

- fixed `TRUSTED_SCHEMA` equality rejects a self-asserted manifest, and the
  source bytes/modes are independently compared with the fixed Git tree;
- physical source and manifest ancestry, ownership, modes, symlinks, and
  hardlinks are refused;
- the source is copied to an owner-only immutable snapshot, re-read before
  publication, then the snapshot is CAS-checked immediately before archive;
- schema identity is bound into the Store identity tuple and checked through
  the source marker, installed inventory, provision report, metadata, and
  receipt projection;
- the f07 preimage is exact, and private CAS controls retain no-clobber,
  descriptor identity, symlink, hardlink, and helper-preservation guards;
- relative imports, stdlib, `typing_extensions` as external, platform
  conditional, optional, dynamic-unresolved, and all-missing behavior were
  exercised with focused or private controls;
- shell stage stderr retention and the original 44 tests remain present.

These are source-level results only. No install, Store publication, child
registration, or genuine child acceptance was performed.

## Remaining input gates

The exact missing carrier is a physical, owner-supplied authenticated source
directory for:

- origin: `https://github.com/banodoco/ArtAgents.git`
- commit: `242f9c4306bf3b501222cb041a9eb246ef47bc85`
- subdirectory: `packages/timeline-schema/python`
- Git source tree: `75a5a697f630affee40632e500b3f5b704a9b834`

It must preserve original bytes, Git modes, ownership, regular-file shape,
manifest identity, and source provenance. The qualified installed package,
old shared venv, nearby vendor copy, or an alternate mirror is not this
carrier. No known approved repository contains the pinned revision object.
Genuine child receipt/interpreter/origin/inventory proof remains NOTRUN.
