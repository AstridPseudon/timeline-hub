Implemented the occurrence audio carrier slice.

- Extended existing `occurrence.add-media` / `occurrence.swap-media` to accept verified audio and require explicit raw audio tracks.
- Added real WAV capture/record/replay/inverse coverage plus malformed-duration and wrong-track atomic negatives.
- Preserved all visual paths and existing registry/inverse semantics.
- No schema, DTO, operation, pin, or generated-client changes.

Tests:

- Occurrence conformance: 64 passed
- Parent/placement/shot-pool neighbors: 177 passed
- Schema floors: 54 passed
- Ruff and `git diff --check`: passed
- No full suite or Runtime HTTP qualification run.

Report: [agent-occurrence-audio-native-source.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-occurrence-audio-native-source.md)

Commit message and `DONE` marker written.