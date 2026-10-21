# D01 native-None transition clear source stage

This packet stages the existing real single/bulk parent-clear proof for a later
browser qualification. It changes only the current source guard's frozen
identity and the launcher/control wording; it does not add product controls,
source protocol, owner inference, graph copying, or a wrapper framework.

## Exact source and dependency roles

The App source snapshot at staging time is:

- App checkout: `/home/user/work/wt/app-m2-transition-clear-current-route-source-stage-r6`
- App `HEAD`: `bc6f9dd39c7e5154ddf075cb87b7202cf5702e65`
- App `HEAD^{tree}`: `4cd13d09b7cffd60612d8521f1a2921ca4e762d2`
- App origin: `https://github.com/banodoco/reigh-app`
- App branch role: `tl/integration` base, with this source-stage diff to be committed by the harness

The later exact dedicated checkouts are deliberately pinned, detached, and
not the mutable integration keepers:

- Agent6ef: `/home/user/work/wt/agt-pin-6efc8150`, `HEAD`
  `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, origin
  `https://github.com/peteromallet/astrid-agent`. Retained hub refs include
  `hub/tl/agt-m2-main95bd-added-gates-result`,
  `hub/tl/agt-m2-main95bd-forward-latest-gates`, and
  `hub/tl/agt-m2-wc10-bootstrap-native-consumer`.
- Runtime95: `/home/user/work/wt/rt-pin-95bd3c5f`, `HEAD`
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, origin
  `https://github.com/banodoco/banodoco-workspace-runtime`. Retained hub refs
  include `hub/tl/rt-m2-d04-wc10-main95-own-consumer-slice`,
  `hub/tl/rt-m2-d13-hold-clear-current-ledger-mapping`, and
  `hub/tl/rt-m2-main014-final95bd-release-packet`.
- Runtime artifact role: Runtime95 `contract/artifacts.json`, SHA256
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
  producer `astrid-runtime`, artifact version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`,
  exactly 76 artifacts.
- Vendor role: current App `vendor/astrid-browser/provenance.json`, SHA256
  `44b80edea6747bf388cb5083120cf12b9fe9d600667432d324917fabd471ad47`,
  Astrid/vendor commit `091aa23ec83ea05ffd3b0115a640230d51c8c429`.
- Composition role: `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`,
  SHA256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  exactly 77 regular members.
- App runtime lock role: `runtime.lock.json`, SHA256
  `770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e`,
  producer source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` and producer
  version `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
- Agent runtime lock role: SHA256
  `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`.

The synthetic App snapshot role is the exact App tree supplied later as
`TIMELINE_CURRENT013_APP_TREE`; the source guard compares it to the App
checkout before and after the named lane. The source-stage base commit/tree
are recorded above. The harness must record the resulting post-stage
commit/tree after it commits this diff before any browser review.

## Existing real packet retained

The two existing cases in `tests/e2e/local/three-products.spec.ts` remain
unchanged and are the only cases selected by this literal command:

```text
npm run test:e2e:three-products -- --grep M2 native None
```

The single case preserves field removal for `None`, raw-mirror absence,
accepted reload, exact restart retry bytes/receipt, guarded inverse, and
`zeroLegacy`/empty legacy-wire assertions. The bulk case preserves one
original-basis atomic clear, unknown revision and opaque data, field removal
and order, exact retry, accepted reload, guarded inverse, and real-conflict
retention of the whole draft. The pure contract controls still require the
literal `{ clear: ['transition'], values: {} }` command, only the
`scalar.target` binding, and refusal of invented owners or mismatched targets.

The launcher remains `scripts/testing/current013-native-none.mjs`; its control
test remains a six-case launcher-only test and asserts the exact named command,
validated Agent/Runtime identities, both source-guard boundaries, child status,
and launch failure behavior.

## Retirement and remaining cut

The exact old clear writer/consumer retirement is commit
`0bc2d8ebbc724c54745276dffa3bd25e869e7d00` (tree
`81cee4ec952fede797417cbd52be1b006f7a7d99`),
`fix(timeline): remove legacy transition none writers`. That product retirement
predates this packet. This source stage does not perform or claim a new
physical product deletion; it only rebinds the existing test guard from the
old 0.2.13/Agent-old roles to Agent6ef/Runtime95/public13/vendor091aa.

The remaining applicable cut is the separate transition SET/type-change,
duration/reset/params and broader D01/whole-document writer retirement work.
Those callers remain outside this packet and must not be inferred from the
native-None proof.

## Allowed source-stage evidence

Cheap checks for this stage are syntax, the guard/launcher/contract control
tests, `git diff --check`, and Playwright test discovery only. No request-test,
browser execution, localhost/live-socket suite, build, install, or project
typecheck belongs to this stage. The later reviewer must use the pinned
dedicated Agent6ef and Runtime95 checkouts and a committed exact App
snapshot/tree.

Executed source-stage checks:

- `node --check scripts/testing/current013-integration.mjs && node --check scripts/testing/current013-native-none.mjs` — PASS.
- `node --experimental-vm-modules --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs tests/e2e/local/support/current013-native-none.test.mjs tests/e2e/local/support/native-transition-clear.contract.test.mjs` — PASS, 23/23.
- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts --list --grep 'M2 native None'` — PASS, exactly 2 tests in 1 file.
- `git diff --check` — PASS.

Not executed by design: `/tmp/.../request-test`, any browser/request/live
socket run, build, install, or project TypeScript check.
