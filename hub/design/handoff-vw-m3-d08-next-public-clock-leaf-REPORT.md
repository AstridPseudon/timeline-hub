# D08 next public clock leaf handoff

App now delegates `getTimelineDurationInFrames` to the published public13 Composition export. The former App reduction body was exact; the compatibility export is the public function identity, covered by a direct assertion. Eight live preview/player/render/composition callers use public13 directly. `getClipTimelineDuration`, `getClipDurationInFrames`, producer/editor semantics, PCM, pixel lane, and the prior rate-wrapper hunks were left untouched.

Focused tests: 4 files/76 passed; affected-neighbor run: 11 files/258 passed. ESLint, TypeScript no-emit, and diff check passed. No full/browser/render/live parity suite run.
