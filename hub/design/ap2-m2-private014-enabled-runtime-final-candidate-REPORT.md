# Private014 enabled-runtime final candidate

## Result

The standalone private014 fixture candidate is qualified. The one authorized
fresh central normal014 Gate 5 run passed after the fixture reset was made
conditional on the accepted Runtime state. The first-admission fix remains
unchanged: standalone command journeys enable the existing Astrid authoring
profile before opening the App.

The later reset had been using `5 -> 0` even though a fresh
`seedThreeProducts` head places `f2-app-clip` at `0`. The candidate now reads
the accepted head after the real command session is ready, skips the reset when
the actual position is already zero, and otherwise drags from that actual
position to zero. A non-zero reset still requires the real commit response,
drains the real outbox, and reads the accepted head back at zero. The helper is
used by both Gate 5 and the dependency-conflict setup. No product
initialization, command-session readiness, authority, actor, metadata, draft,
header, session-identity, or captured-guard behavior was changed.

## Source and exact tuple

- App base commit: `0da8afd8f` (`fix(timeline): enable authoring before standalone command journeys`).
- Working-tree change: only `tests/e2e/local/three-products.spec.ts`.
- Central snapshot App tree: `171d388a9a093f139e1a2519663133ec9ced2f67`.
- Agent: `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`.
- Runtime: `202074110717146fc7f08af2306a8dd7f695b0b1`, tree `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Immutable producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Artifact: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`.
- Schema: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Locked private App dependency graph: source archive
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
  (the 300,830,720-byte `app-ap2-m2-locked-graph-source.tar`). This is the
  entire test dependency-graph archive, not the Composition package. It
  contains the official Composition tarball at
  `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`.

The exact official Composition package used inside that graph is
`@banodoco/timeline-composition@0.0.13`,
`design/handoff-vw-m3-release13-banodoco-timeline-composition-0.0.13.tgz`,
SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
58,477 bytes. Its immutable Composition source package/lock blobs at release
commit `73bd62b1e1b710a730545c862bd2da76e324ca46` are respectively
`package.json` SHA-256
`7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61` and
`package-lock.json` SHA-256
`f0665832797f59b20afc1e868a11499035046930e1b406d3823cfb704b3018e6`.
The App lock entry resolves to the file tarball and records integrity
`sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`.

The passed central run checked the graph archive SHA, graph package version,
and the extracted official tarball SHA; it did not count Composition tar
members. The separate immutable release13 evidence records the official
tarball as 77 regular members and exactly matching the supplied sorted
77-member manifest. Therefore this Gate 5 report makes no claim that the
0148973 run itself performed the 77-member count.

## Evidence

Targeted local checks:

```text
git diff --check
PASS

node node_modules/eslint/bin/eslint.js src/test/threeProductsAuthoring.test.ts tests/e2e/local/three-products.spec.ts --no-cache --max-warnings 0
PASS

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-private014-first-admission-guard-fix/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/test/threeProductsAuthoring.test.ts
1 file, 3 tests passed

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-private014-first-admission-guard-fix/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/test/native014Admission.test.tsx src/test/threeProductsAuthoring.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/timelineCommit.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
8 files, 135 tests passed
```

The first direct Vitest invocation without the repository's `__dirname`
preload failed at config startup; the corrected command above passed. No local
browser, localhost, live socket, or full suite was run.

Exactly one central request was made:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-private014-enabled-runtime-final-candidate normal014-integration-e2e-gate5) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result:

```text
test ap2-m2-private014-enabled-runtime-final-candidate-normal014-integration-e2e-gate5-1020195447-8973: pass exit=0 in 129s
1 passed (32.4s)
```

The central hosted build completed in 1m18s. Its source tuple, artifact
checks, private graph/bin setup, Chromium journey, lost-ACK/retry/restart/
undo assertions, and zero-legacy traffic all passed for the selected Gate 5.

The predecessor admission-fix evidence remains: focused regression 3 RED ->
3 GREEN, private014 targeted 137 PASS, and 2 native admission traces PASS.
This candidate's fresh focused rerun is the 3-test and 8-file result above.

## Scope and next steps

No public pin, activation, generation, DTO, store, API, dependency, Runtime,
Agent, Composition, or product-initialization change was made. No test was
weakened or removed. The worktree has only the intended E2E fixture source
change; the harness should commit it with the supplied commit message.
