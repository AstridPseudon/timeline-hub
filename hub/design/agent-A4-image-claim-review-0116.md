## Verdict: PASS — source-causal audit

The captured request itself FAILS at the App emitter seam:

- Core fields (`schema_version`, `op`, `version`, `select`, `args`): **PASS**, exact match.
- `created`: **FAIL** — App submits `[]`; Agent records:
  - `parent/asset:variant-…`
  - `parent/clip:clip-0`
- Runtime result: **FAIL**, exact `validation_error / invalid_records / provider executed a different command`.
- Media custody: **PASS** — prepared media, verified selection, and registry entry match the same retained Runtime fixture.
- Preservation: **PASS** — raw visual-track `opaque: [null, false]` and all child placements/shots/revisions remain unchanged.
- Provider path: **PASS** — `clip.add-media` calls the authored-registry conditional allocator, then creates the clip.

Exact seam: App commit `22efcda3`, `timelineLocalSaveHandoff.ts:333-334`, where image `clip.add-media` omits `created`. The correction should derive allocation from `parent.registry.assets`: include `parent/asset:<media.asset>` only when absent, and always include `parent/clip:<row.id>`. No product edit was made.

Changed only the proof script: [a4_image_claim_proof.py](/home/user/work/wt/agt-A4-image-claim-review-0116/test-support/a4_image_claim_proof.py).

Checks passed:

- Offline proof using Runtime pin `8ea0766f`
- `py_compile`
- Ruff
- `git diff --check`

No live Runtime acceptance, Realm/public-body retry, browser, full suite, or fixture was used. The proof explicitly makes no Runtime acceptance claim.