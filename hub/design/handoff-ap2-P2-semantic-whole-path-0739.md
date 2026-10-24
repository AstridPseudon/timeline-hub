## Result: FAIL

No files were modified; worktree remains clean.

Finding: the current helper rejects a genuine parent `clip.add-media` request because the producer preserves `row.opacity: 1`. Its fixed row-key allowlist is not compatible with `timelineLocalSaveHandoff.ts:405–460`, which serializes the complete authored row. Authentic request evidence from 0730: body hash `sha256:bc3fe9f3dfda5db0904b39227bde6eb9300b53f9d60197f174132a928cce20ae`.

Source map:

- Parent path: `authoredJson(row)` + exact five-field media selection; created claims are ordered `parent/asset:*` when absent, then `parent/clip:*`.
- Automatic occurrence image path: row vocabulary is exactly `asset, at, clipType, hold, id, track`; ownership intent is `{ ownership: 'occurrence' }`.
- `localSaveSession` supplies the v2 envelope, `merge: 'fields'`, empty semantic patch, omitted reads, and preserves command contents.
- Provider capture internals may add claims/reads/resolved metadata; these are not wire DTO fields.

Helper boundaries:

- Negative controls correctly reject extra top-level, command, args, media, step, claim, read, merge, patch, and created fields.
- It correctly derives created claims from the immutable pregesture authored registry.
- It falsely rejects legitimate authored row fields (`opacity`, and any other preserved authored fields).

Checks run:

- Helper controls: PASS.
- Three serialized TypeScript checks: PASS.
- Scoped ESLint `--max-warnings 0`: PASS.
- Playwright list-only: PASS, 3 tests collected.
- `git diff --check`: PASS.
- No browser, backend, HTTP, socket, service, full-suite, or live transport run.

Recommendation: Sol0739 should derive the expected row from the immutable pregesture/source-produced row, preserving legitimate authored fields and absent/null distinctions, while retaining the current exact envelope, claims, metadata, reads, patch, and provider-field refusals.