# Current13 five-case frozen preparation

## Verdict

**HELD_PREPARED.** The test-only descendant is ready for a later owner-frozen
tuple, but no capture grant, browser, render, export, or adoption is authorized.

The prepared source is App base `e26079c440d09d7712588581e369204b3e035db9`
(tree `e523fc0dc76eeff03a68f3cdb59e78a8b6b55798`) with working source hash
`9ada22fb56897767bf05931b1a3a5837962f04cafd971d82b262352ec7f6a4fe` over 5,848
source files. The controller SHA-256 is
`047aae00bfc5b059e86bc441f53eb4a2854df73606c6021da28a0e95ee5b4854`.
The machine-readable manifest is beside this report.

## Change

Only three test guard files changed:

- `harness.ts`: exact Composition public13 hash, version, and artifact paths;
- `source-tuple.ts` and its unit fixture: `timeline.viewing.next-five-case/v1`.

The existing normal Render route, native 1920/original 640 fixtures, modal-close
capture path, themes, compiled incoming vectors, and audio lifecycle were not
changed. No fixture or product source was added.

## Frozen identities and holds

- Current App integration: `0d5009e18…` / `b3236676…`, public13, but the
  `8488` stored-cap port, `e4c7` native-fixture port, and tab controller are
  absent from that integration head.
- Current Agent integration: `c73b1ab1…` / `ddb30a85…`, still public12.
  The held public13 Agent candidate remains explicitly
  `d8749a9c…` / `75354d38…`; it was not silently adopted.
- Held Runtime official source: `2c4ac180…` / `7ab412cc…`, contract 0.2.13,
  official generated client all75.
- Composition public13: source `5a4e9b72…` / `13e37553…`, archive SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77
  regular members.
- Repaired graph evidence is `GRAPH_READY_ONLY` (21,495 entries, 0
  missing/changed/added). The distinct f816 graph with 21,565 entries remains
  `UNQUALIFIED` and is excluded.
- Node v20.19.4 and Chrome 155 identities are recorded in the manifest.

## Commands and results

- `node --check tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs` — pass
  with the admitted Node 20.19.4 executable.
- `node --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs` —
  1 test file passed with Node 20.19.4.
- Targeted Node tests for admission, authority, browser profile, canvas, harness,
  and source tuple — 6 test files passed.
- Controller `--discover` — exactly 5 native-codec-Chrome155 cases.
- Controller `--ready` — exit 1 at the intentional
  `App13 consumer adoption is pending` hold, before graph/browser/grant checks.
- `git diff --check` — pass.

Not run: browser, render, export, live sockets, localhost, install, network,
full suite, capture, grant creation, or marker reuse. Free disk was
`9,857,830,912` bytes at final inspection, below the required
`10,737,418,240`-byte floor; this alone keeps readiness held.

Next step: land and independently review the exact App owner ports, provision a
matching Agent public13 normal pin, refresh the source tuple/manifest, restore
the disk floor, then request a fresh manager grant. Do not merge this test
candidate wholesale or reuse any consumed marker.
