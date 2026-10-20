# App parent-delete candidate gate

## Verdict

Candidate `29564148789ef00a8c28ea44d7ba87faf19d1602` / tree
`7b86b7aff415007f679c29ffa71a1d16f8551e24` is **not qualified** by this
execution. The first real UI case failed before the DELETE request was
observed. This is a partial candidate-validation result, not an integration,
retirement, or `DELETED` claim.

This proof does **not** qualify the cold track-rename path. The separate cold
label mismatch remains a distinct release-gate concern, even though this run
shows an analogous initial-basis/readiness symptom.

## Full tuple

- App candidate: `29564148789ef00a8c28ea44d7ba87faf19d1602`
- App tree: `7b86b7aff415007f679c29ffa71a1d16f8551e24`
- Agent: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree
  `75354d38c898729bac09619679f5421faba319ed`
- Runtime/producer: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`
- Runtime package: `0.2.13`; producer SHA-256
  `6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Runtime schema SHA-256:
  `8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`
- Runtime component manifest SHA-256:
  `1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`
- Runtime artifact count: `75`; public Composition artifact count: `77`
- Public Composition 0.0.12 archive: SHA-256
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- Tracked public browser closure: SHA-256
  `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, version
  `141.0.7390.37`, SHA-256
  `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`

## Preparation and discovery

The exact-source/public-closure checks passed locally. The tracked public
browser bundle was used; `ASTRID_PUBLIC_CHECKOUT` and
`ASTRID_APP_DIRECT_DIST` were unset. Runtime metadata and the public12 archive
matched the verified pins. The private12 dependency overlay and cache runner
were worker-owned; shared node_modules, caches, and virtualenvs were not
modified.

Targeted local checks passed:

- `node --experimental-vm-modules scripts/testing/current013-parent-delete.test.mjs` — 7 passed.
- `node scripts/testing/current013-integration.test.mjs` — 15 passed.
- `python3 -B notes/public-source.py` — tracked closure matched.
- `PWTEST_CACHE_DIR=notes/discovery-cache node node_modules/playwright/cli.js test --config playwright.clip-delete.config.ts --list` — exactly 2 tests discovered, both required cases.

The requested literal central suite command was registered as
`e2e-parent-delete-tree7b86b7a-runner61a036d-e2e-integration` in
`tests/suites.conf`, keyed to the candidate tree, dependency tuple, and runner
hashes. The runner hashes were: lane
`61a036da771c898d9a506888a4464eaeec3ed54eb380e314f5a684987341f868`,
overlay `42ab49c61b60c80c50163e9107920e2a312f48b2c7cd0fa6d1e555fa02a429c8`,
audit `d6b3c5ea26cdc6125c6131e012be7de1c3c327cc43b2cadf13848e478ac0e499`,
and public-source guard
`8546b06b602c8917ad2065bda13083958f182b9e816fad74440b0ab654300aad`.

## Central execution

TestID:
`app-m2-parent-delete-actual-candidate-gate-e2e-parent-delete-tree7b86b7a-runner61a036d-e2e-integration-1020150047-3749`

The request was made with `request-test app-m2-parent-delete-actual-candidate-gate
e2e-parent-delete-tree7b86b7a-runner61a036d-e2e-integration`; the central log is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-parent-delete-actual-candidate-gate-e2e-parent-delete-tree7b86b7a-runner61a036d-e2e-integration-1020150047-3749/log.txt`.

The central command built successfully (`built in 1m 8s`) and launched the
real two-case Playwright run. Case 1 failed at
`tests/e2e/local/clip-delete-command.spec.ts:171` after about 1.6 minutes:

```text
Expected: 1
Received: 0
Timeout: 90000ms exceeded while waiting on the predicate
```

The predicate was the captured wire post count immediately after the UI Delete
action. The page was connected, the timeline was loaded, the `f2-app` overlay
was selected, and the Delete inspector was visible, but no commit request was
captured. The real browser error context and trace are under:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-actual-candidate-gate/notes/run/browser-artifacts/`.

I stopped the central runner at the first product failure as required. Case 2
therefore has no result, and the runner's normal postflight did not run after
the intentional stop. No second request was submitted.

## Evidence limits

The failure occurred before native capture, so this run provides no evidence
for raw/mirror/registry/opaque/closure behavior, the real same-property
Agent409/original-draft conflict, lost ACK, Runtime restart, reload, exact
retry/body-key receipt, Runtime inverse, UI inverse restore, draft retention,
or the zero-legacy assertion. The source assertions and two-case capture were
not weakened; no command injection, provider fake, or group261 change was
made. No full suite, TypeScript check, install, or framePCM run was performed.

The zero-request failure is consistent with the initial-basis/readiness seam
seen in the separate cold-label report. I am reporting that link rather than
weakening the capture or treating it as a runner-only correction. Do not merge
or retire this candidate until the root release gate passes and the corrected
two-case run is repeated from a clean tree.

