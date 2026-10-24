## Done

- Fixed popup media serialization to strip only the matching derived `assetEntry`, preserving strict authored-field validation and opaque fields.
- Added focused regression coverage, including forged derived-field rejection.
- Added mounted full-caller coverage for accepted and merged Runtime responses with authoritative forked closure.

Tests:

- `media.test.ts`: 29 passed.
- Full caller: 2 passed.
- A3 provider controls: 36 passed, including conflict/invalid rollback.
- ESLint: passed.
- All three TypeScript configs: passed.
- `git diff --check`: passed.

Known note: mounted tests emit existing Remotion/jsdom `useCurrentFrame` warnings but pass. The shared-media command path currently omits request-level `reads`; this was preserved due the task’s file-scope restriction, while response step dependencies remain asserted.