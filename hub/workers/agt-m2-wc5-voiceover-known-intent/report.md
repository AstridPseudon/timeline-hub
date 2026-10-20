Implemented WC5 known-intent voiceover migration.

- Native proposal path: `track.create` → `occurrence.add-media` → guarded `text-binding.set`.
- Exact media 5-tuple, WAV metadata, producer provenance, frozen UTF-8 text guards.
- Existing-clip branches retain `TargetBound.publish`; ripple timing returns a concrete gap.
- Added private proposal helper module; ledger remains held.

Tests:

- Targeted suite: **188 passed**
- Voiceover tests: **27 passed**
- New helper Ruff check: passed
- `git diff --check`: passed

Runtime/App integration and live speech execution remain unverified.