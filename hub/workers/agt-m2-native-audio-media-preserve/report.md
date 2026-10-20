Implemented native audio media support and guarded verified-duration audio trims.

Changes:
- Accept verified `audio/*` media on existing `clip.add-media` / `occurrence.add-media`.
- Require explicit active audio tracks and exact source windows.
- Allow legacy audio trim using exact `VerifiedMedia.duration_seconds` when registry duration is absent.
- Preserve existing schema, registry shape, image/video behavior, inverse, replay, and guards.
- Added focused audio authoring/trim coverage.

Tests:

```text
275 passed, 84 deselected
```

Ruff: `All checks passed!`

Historical provider-bound audio trim remains OPEN because Runtime currently cannot provide an undeclared exact media-selection carrier. Full details: [agent-native-audio-media-preserve.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-native-audio-media-preserve.md)

Commit message and `DONE` marker written.