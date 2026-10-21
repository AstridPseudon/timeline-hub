# M2 current-ops producer proof execution preparation

## Result

Prepared the exact one-test Playwright execution command, but did not submit a
browser, localhost, Runtime-door, or gate run.

The custody approval is for the exact committed App source:

- App commit `36dd91257fd13dcad0d58b48c790caa5063b4c8c`
- App tree `d908845dbc8e5ebf96698d08621557e904f20c52`
- Approved source files: `tests/e2e/local/producer-ownership-current-pin.spec.ts`
  and `tests/e2e/local/support/producer-ownership-current-pin.ts`
- Approved source file hashes:
  - spec `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`
  - helper `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`

The durable selector config added in this worktree is
`playwright.producer-ownership-current-pin.config.ts` (SHA-256
`5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`). It
extends the existing `playwright.direct.config.ts` Runtime-door harness and
selects only `producer-ownership-current-pin.spec.ts` under
`testDir: ./tests/e2e/local`.

## Exact eventual command and suite

Registered exactly one named suite in the shared test-service allow-list:

`app ap2-m2-producer-current-ops-e2e-integration`

The registered command is:

```text
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2c4ac180 TIMELINE_BUNDLE_AGENT_HEAD=8130a401bf44a518d5a40ae274d398b8c560be55 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 TMPDIR=/tmp/tl-ap2-producer-current-ops node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts
```

The exact selector preflight with this same config, spec path, and `--list`
collected one test:

```text
Listing tests:
  producer-ownership-current-pin.spec.ts:87:3 › producer ownership on the current mounted route › removes only stale owned transcript output and moves only owned scene output
Total: 1 test in 1 file
```

The repository default config was tested first with the same explicit spec
path and failed with `No tests found` because its `testMatch` is fixed to
`direct-journey.spec.ts`. The dedicated config is the minimal existing config
seam used by neighboring direct journeys; no generic wrapper, fake provider,
or source-guard bypass was added.

## Exact cohort identity

- Agent: commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime: commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Runtime producer artifact: producer commit `2c4ac180`, artifact version
  `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
  schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
  75 manifest artifacts.
- App Composition public13 archive: SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77
  regular archive files (`all77`); Runtime producer manifest has 75 artifacts
  (`all75`).

The App source already contains the approved production ownership safety repair
from commit `9a5e9ed6c7a9cb43ee15a721029ecd0be5612d59`. This preparation does
not activate a host-field writer or change a pin.

## Source-only checks

Passed:

- `node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts tests/e2e/local/support/producer-ownership-current-pin.ts`
- `npx tsc --noEmit --pretty false`
- `git diff --check`
- Exact Playwright collection command above with `--list`: 1 test collected.
- Public13 archive SHA-256 and tar member count: hash matched and 77 regular
  files.
- Approved source commit scope: exactly the two spec/helper files; no
  production, shared writer, DTO, authority, carrier, three-products, or
  future-fresh source file changed.

Not run: browser execution, localhost, Runtime socket/door, actual gate,
full suite, or test-service submission.

## Live callers

The journey uses the existing `appTest` direct harness, its isolated Runtime
composition-revision genesis endpoint, `compositionPublication`, and the
mounted `/tools/video-editor` route. The UI callers exercised are the existing
Transcript actions-menu regenerate path in
`src/tools/video-editor/dev/transcript-lane/extension.ts` and the Scene Phase
Markers “Move existing shots to markers” path in
`src/tools/video-editor/dev/scene-phase-markers/extension.ts`, registered by
`src/tools/video-editor/dev/localExtensions.ts`.

The intended case retains the full accepted/refused boundary and all reload,
real-commit/lost-ack, exact raw-body/idempotency-key retry, protected raw-row
and order preservation, and guarded undo checks. It does not claim fresh
producer creation or writer closure.

## First blocker and next step

The first execution blocker is environmental: the exact Runtime checkout named
by the registered command, `/home/user/work/wt/rt-pin-2c4ac180`, is absent on
this machine. The exact Runtime commit/tree is present in the reference
repository object store, but no matching checkout was created here. The
manager must provision or point the guarded driver at that exact committed
checkout before authorizing the actual command. The Agent 8130 source is also
recorded by commit/tree rather than activated or repinned here.

After that external prerequisite is supplied, the manager may authorize the
registered one-test suite. If the mounted route visibly refuses, retain the
spec annotation and report refusal; do not relabel it as accepted ownership.
