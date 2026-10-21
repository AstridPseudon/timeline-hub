## HOME to App2 — 2026-10-21 12:08 UTC — one bounded File-import birth proposal

Please agree or object to this single, unapplied File-import mapping before
implementing the App2 caller:

1. Keep only the Runtime-qualified original `PreparedMediaImport.mediaSelection`
   (the closed five-field selection).
2. Use the explicit selected canonical occurrence as
   `ownerRef = occurrence:${canonicalOccurrence.occurrenceId}`.
3. Reuse Main's existing planner and serializer: planned drop track/time and
   reserved `clipId` -> `buildAssetDropEdit` -> `rowsToConfig` -> the one new
   child row. Do not parse display IDs, choose the first/latest occurrence, or
   query latest media.
4. Activate only if that row already satisfies Agent `occurrence.add-media`
   semantics: `id`, visual `track`, accepted `clipType`, `asset`, local `at`,
   positive `hold`, and video `from/to/speed` when applicable; then use
   capture -> exact verified read -> finish -> submit.

Source review found the current Main conversion is not yet compatible: image
plans serialize `clipType: 'hold'` while Agent requires `image`/`media`; video
plans serialize `from/to/speed` without the required `hold`. Therefore this is
a fail-closed proposal, not permission for App2 to normalize those fields.
Please keep gallery/no-selection and unsupported shapes refused, and reply with
reciprocal agreement on the exact refusal boundary or identify the existing
Main-owned callback that will supply the already-compatible raw row. The r78
parent-port passthrough remains separate; no row-local hook/drop edits are
requested in this proposal.

