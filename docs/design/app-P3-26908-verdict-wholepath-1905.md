# P3/D75b independent terminal verdict

## Verdict

**FAIL. This is not gateGO.** The same-ID normal run is a real production
journey failure, not a source/custody failure at the limits below. The gate
stopped at the first recovery-count assertion, so no downstream history,
merged B, canonical-document, Agent, or guarded-undo credit is available.

## Same-ID custody and executed assertions

Normal run:

- ID: `app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908`
- preflight: `app-pin-3c29d553-d75b-p3-current-1855-preflight-1024185442-20128`, PASS, exit 0
- heads: App `3c29d553a7af0b0e0876760052855818ea834658`, Agent
  `831df37ffdfbb7cf802c95f91eac30681efdbb45`, Runtime
  `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f`, Composition
  `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`
- trees: App `2f0aa476b5cd40e2b80b5f4dec37571b7152a55f`, Agent
  `52213c5a56f332532759826f04be6659d8ddd34a`, Runtime
  `4feab0185b3750a55b8f0c21c92c6015aaf8e2f7`, Composition
  `5ab5191a296980a0a6bcd1178ab6902d6478a148`
- service snapshot: head `88ab2b2ab44ce7f8844cd5d746dd4d44df289c6f`, same App
  tree, clean, sole parent `3c29d553a7af0b0e0876760052855818ea834658`
- Node `v20.19.4`, npm `10.8.2`, Runtime `AstridRuntime/0.1 Python/3.13.16`,
  protocol `workspace.v1`, provider `astrid-v1`, compiler `authoring-bundle-1`
- schema digest: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`
- protected test hashes before and after are identical: `three-products.spec.ts`
  `8661fc919714d292c567844dc4f423855923077ca6a679a1398ec2a46154315b` and
  mounted-readiness `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`

JUnit was parsed from the retained files, without rerunning the suite:

- readiness: 1 test, 0 failures, testcase `26.288s`; suite `26.288s`, root
  `60.044522s`; PASS, exit 0
- original: 1 test, 1 failure, testcase `201.824s`; suite `201.824s`, root
  `248.905236s`; FAIL, exit 1
- submit wall duration was `471s`; it is not the JUnit testcase duration

The original reached `three-products.spec.ts:1773` after all preceding setup,
the Agent C edit, lost-ACK staging, the first reload mount, daemon restart,
new-page reconnect, durable owner inspection, and `posts === 1` assertion.
The unchanged `90_000ms` poll then saw `wire.observed.length === 3` while the
corrected assertion expected `4`. No later assertion ran.

The retained error context is the bounded evidence: it contains the same
failure and source excerpt. The retained trace was not extracted or used as a
second wire collector. Therefore the actual run proves the total observed
count of three and the first forwarded A (`posts === 1`), but does not prove
the individual later request body/key/origin/order assertions. Those
assertions remain unexecuted, not passed by inference.

## Whole-path comparison

The production path is:

1. The browser route intercepts the real POST at `tests/e2e/local/three-products.spec.ts:786–920`.
   `faultFirstCommit` records request identities and URLs, loses the first
   acknowledgement after the Runtime has accepted A, and stages the automatic
   retry. It does not inject a save or click a fixture recovery button.
2. The App POST uses the fixed stable door (`harness.doorBase`); the Runtime
   daemon is started behind it and writes discovery on each start
   (`tests/e2e/local/support/harness.ts:687–733`). `restartRuntime()` stops the
   daemon and starts it on a different port (`:745–752`), while the door
   remains the browser endpoint.
3. The test performs the first page reload, closes the page, restarts the
   daemon, creates a fresh page, reconnects, opens the real timeline, and
   verifies the same scoped outbox owner and pending request before arming the
   observer for the next recovery (`three-products.spec.ts:1742–1773`).
4. The mounted production hook reads the verified basis and recoverable
   identity, creates the real local save session, and calls `session.recover`
   for the sole owner (`src/tools/video-editor/hooks/useTimelineSave.ts:307–376`).
   The session lists durable owners, claims the exact owner, and `recover()`
   calls `pump()` (`src/tools/video-editor/commands/localSaveSession.ts:217–267,
   :322–326`). The outbox reserves and dispatches the persisted request only
   after its IndexedDB transaction (`src/tools/video-editor/commands/commitOutbox.ts:468–523`).

The passing comparison is P131083:

- App `830252327fc37b9c68fb7fa9e3d09ad560624fb8`
- Agent `263696c832220eebd79804a74f78c57734ad7bd7`
- Runtime `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`
- P1 JUnit: 2/2 passed; testcase durations `23.3s` and `17.807s`

Its retained source path performs the same real reload → durable owner →
Runtime restart → exact retry flow and reaches exact request/key assertions
(`three-products.p1-chain.spec.ts:1510–1565`). The production-path files are
byte-identical between passing App `83025232` and failing App `3c29d553`:

- `useTimelineSave.ts` SHA-256
  `33e0ff6b26689e8af62b099557e8455f6ba87ad2b9bbbcbc69e42ac84918638a`
- `localSaveSession.ts` SHA-256
  `def2c8c040daea9cff212c40f4f01062d2a6e7bfe6f76a4928cd53eabbf59230`
- `commitOutbox.ts` SHA-256
  `dc497f0676b72abee0736abe19f0c33848a059776440db507375847a12160b21`
- `useTimelinePersistence.ts` SHA-256
  `348e0481e13150ff63dea94884800e8d030fe09734e66a8da3573910bed3e63a`
- `timelineDraftIndexedDb.ts` SHA-256
  `ee337cbfbeaf52afe50b6692e40a06eb16abcf029d34a8345c690bdd4f2f84cb`

This rules out a production source change between the comparison runs, but it
does not establish why this D75b browser run produced only three observed
requests. The bounded alternatives remain a real recovery/lifecycle failure,
observer/page-route lifecycle loss across the two mounts, or unavailable
evidence after the first failed assertion. The result does not justify an
alternative count and does not justify calling the gate passed.

## Source/custody checks and next owner

The reused D75b source controls and same-blob receipt remain PASS only as
source/custody evidence: both automatic mounts, exact `A,A,A,A,B` observed and
`A,A,B` forwarded expectations, stable-door origin, full v2 request fields
(`api_version`, scope, base pair, commands, label, steps with intent/tags/
ordinals/patch, merge, reads, source, dry_run, and `Idempotency-Key`), and
accepted/merged `{data, receipt}` plus structured refusal assertions are still
present. They are not browser-run PASS evidence for this failed ID.

Checks run for this review:

- Node20 `--check scripts/testing/d66-plain-stack.mjs`: PASS
- `git diff --check`: PASS
- targeted Vitest, TypeScript, and lint evidence: reused from the exact
  immutable D75b source-equivalence receipt; no duplicate suite was run

Next owner: the future App product author, with the App manager/orchestrator
deciding whether to dispatch a new review-only investigation. If a protected
scope is needed, it should be limited to the D75b recovery body
`tests/e2e/local/three-products.spec.ts:1649–1863`, the mounted lifecycle
control `src/tools/video-editor/hooks/useTimelineSave.mountedRecovery.test.tsx`,
and the unchanged production recovery callers named above. Do not change the
counts, waits, route origin/key/body guards, downstream assertions, or
originals as part of that investigation.
