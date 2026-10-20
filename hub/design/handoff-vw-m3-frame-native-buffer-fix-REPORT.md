# Handoff: frame native-buffer fix

## Result

Fixed the App viewing-parity test decoder on the requested `1ba0800af` base.
`decodeRgb()` now validates probed dimensions, derives FFmpeg stdout `maxBuffer`
from `width * height * 3` plus 1024 bytes, and refuses decoded frames above a
256 MiB byte bound. The existing 640x360 comparator contract and threshold
(`channel > 2`, fraction `.001`) are unchanged.

Added a direct decoder regression that generates a 1920x1080 PNG and an
FFV1/RGB24 lossless video in a temporary directory. Both decode through the
production test helpers, have equal native RGB bytes, and are then rejected by
the existing comparator as oversized Player/export frames. This proves the
failure occurs at the comparator's existing dimension contract rather than at
the child-process stdout buffer.

## Evidence

From `/home/user/work/wt/vw-m3-frame-native-buffer-fix`:

```text
XDG_CACHE_HOME=/tmp/vw-m3-frame-native-buffer-cache node --import tsx --test \
  tests/e2e/timeline/viewing-parity/directframes.test.ts \
  tests/e2e/timeline/viewing-parity/compare.test.ts \
  tests/e2e/timeline/viewing-parity/media.test.ts
```

Result: exit 0; 3 file-level subtests passed, 0 failed. The native generated
PNG/lossless-video regression passed.

```text
XDG_CACHE_HOME=/tmp/vw-m3-frame-native-buffer-cache ./node_modules/.bin/eslint \
  tests/e2e/timeline/viewing-parity/frames.ts \
  tests/e2e/timeline/viewing-parity/directframes.test.ts \
  --report-unused-disable-directives --max-warnings 0
```

Result: exit 0.

`git diff --check` passed. The private cache and generated test media were
removed. No browser, render, socket, network, install, full suite, product
code, fixture, comparator, threshold, profile, or parity claim was made.

## Decision / follow-up

The 256 MiB decoded-frame cap is a defensive test-pipeline bound; it is well
above the retained 1920x1080 native frame (about 5.94 MiB RGB) while preventing
unbounded child output. No blocker remains. The orchestrator should run its
normal integration qualification after applying this worker patch.
