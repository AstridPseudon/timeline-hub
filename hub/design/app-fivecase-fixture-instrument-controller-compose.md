# App five-case fixture, Player instrument, and controller composition

## Result

Composed the three reviewed Viewing test/support units onto current App
integration `dcb9f9c70`:

- Native current-root fixture donor `f084855eff0c40a464a166297d43536458ee4ca4`
  from `app-m3-native-fixture-current-root-small-port`.
- Player tab-audio instrument donor `379c19509ddb4f100d192c0e52d1307abc3c7a00`
  from `tl/vw-m3-player-instrument-current-owner-port`.
- Two-file controller donor `c217fbd0731620285412dbb33a4996c8f909ae8a`
  from `tl/vw-m3-fivecase-final-twofile-owner-unit`.

The controller literals were reconciled to the actual landing facts: complete
cap is integrated at `a8283307a7a5537a95988031b385ef28df7524ea`, App13 is
adopted at `ea38656fe62950440b36cafee780698cff2c3f9c`, and Agent public13 is
verified at `6f0cdc7df95fe3c9b2d491d6fcb39b754fa212bd` with tree
`6e3d8589537d581e65e1da21be3e6a7d83022a01`. The old Agent `04f...` proof is
not used.

## Exact unified source/file list

1. `tests/e2e/local/support/harness.ts`
2. `tests/e2e/timeline/viewing-parity/cases.ts`
3. `tests/e2e/timeline/viewing-parity/canvas.test.ts` — five-case count and
   fifth-before-negative ordering guard.
4. `tests/e2e/timeline/viewing-parity/fixture.ts`
5. `tests/e2e/timeline/viewing-parity/harness.ts`
6. `tests/e2e/timeline/viewing-parity/native-fixture-helper.py`
7. `tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts`
8. `tests/e2e/timeline/viewing-parity/tab-audio.ts`
9. `tests/e2e/timeline/viewing-parity/tab-audio.test.ts`
10. `tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs`
11. `tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs`

The five donor fixture files match `f084855ef` byte-for-byte. The three Player
files match `379c19509` byte-for-byte. Native fixture and Player instrument
code each occur once in this source tree; no old broad ancestry, product,
package, AudioTrack, render-admission, or capture-authority changes were
joined. Existing M1 default-15s behavior and guards remain unchanged.

The controller's flat port state is now:

| Owner | Port | Status | Source |
| --- | --- | --- | --- |
| App | complete-cap-current-join | integrated | `a8283307a7a5537a95988031b385ef28df7524ea` |
| App | track-inspector-preservation | integrated | `a04f90cf60eac69a5079f0ab03188abcbd1571fc6` |
| App | native-frame-fixture | integrated | `f084855eff0c40a464a166297d43536458ee4ca4` |
| App | player-tab-audio-instrument | integrated | `379c19509ddb4f100d192c0e52d1307abc3c7a00` |
| Agent | public13-normal-pin | verified | `6f0cdc7df95fe3c9b2d491d6fcb39b754fa212bd` |

`MISSING_OWNER_PORTS` is empty. The real Playwright discovery sees all five
cases, in order, including the Player tab stream before the planted negative.
Discovery of four cases is not accepted, skipped, xfailed, or relabelled.

## Verification

- Donor/player byte comparison: PASS for all eight directly copied files.
- `git diff --check`: PASS.
- Scoped ESLint with `--no-cache` over all ten controller/fixture/Player
  TypeScript and JavaScript files plus `canvas.test.ts`: PASS.
- Python AST parse of `native-fixture-helper.py`: PASS.
- Direct neighboring Node tests (harness, media, canvas, authority, admission):
  **5 passed, 0 failed**.
- Direct `tab-audio.test.ts`: **1 file passed**.
- Actual Playwright discovery using
  `playwright.viewing-parity.native-codec.config.ts`: **5 tests in 1 file**.
- Full controller test: 8 of 9 subtests passed; the one unverified subtest is
  the retained Node identity acceptance, because its frozen private executable
  path `/tmp/.../workers/vw-m3-current-root-cap-three-stills-prep/node` is absent
  in this environment. No replacement path was fabricated.

No browser, recording, render, PCM/frame capture, build, typecheck, install, or
full suite was run. The native fixture integration test was not run because it
requires the absent production `dist/index.html` and would cross the explicit
no-build boundary.

## Remaining launch prerequisites

- D10 installed-host fix remains pending; no D10 completion or parity claim is
  made here.
- Real viewing launch remains gated on a safe qualified root and the manager's
  exact fresh launch grant. No Runtime fresh normal-render grant was created.
- No physical Player PCM/frame evidence, mux evidence, or parity result was
  created or marked passed. The controller keeps `physicalMixClaim: false`.
- Restore the explicitly pinned Node20 executable/private graph and rerun the
  controller's full environment lane before any `--ready` launch. The existing
  historical Viewing qualification is retained as provenance, not as a new
  capture grant.
