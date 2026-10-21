# Producer explicit list/run mode — source0354

## Result

Updated `scripts/testing/run-producer-public13-list.sh` with a required closed
`list|run` mode. The existing list suite remains list-only, and a distinct
actual suite is registered in the shared test-service allow-list:

- `ap2-m2-producer-existing-graph-command-e2e-integration` — `list`
- `ap2-m2-producer-existing-graph-command-actual-e2e-integration` — `run`

The existing public13 runner, protected graph, source commits, body, helper,
config, traps, short paths, and child return-code handling remain unchanged.
No product, journey, pin, or source-guard files changed.

## Exact custody identities

- Wrapper source: `scripts/testing/run-producer-public13-list.sh`
- Wrapper SHA-256 after this change:
  `11080069b40aab7e9fd9798974cc43d9b244de5f17d930ebc74dc0f935136fc2`
- Protected runner:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh`
- Protected runner SHA-256 (unchanged):
  `40c25724b502ce5582caf04c6ebf44ab89a509b5f3d629876d599f57c3e5fa7a`
- Existing source tuple remains Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, App `4ef89267f00d193273441ff6dbb955f30d27d708`, protected graph archive SHA-256 `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30a`, and public13 package source SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Mode proof

The temporary planted Playwright child recorded these exact argv values:

```text
list: test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list
run:  test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts
```

The run branch accepts exactly one summary line of `1 passed` with child RC 0
or `1 failed` with child RC nonzero, then returns that child RC. It rejects
zero/missing output, pass/nonzero and fail/zero mismatches, and multiple
pass/fail outcomes. The list branch still requires RC 0, no zero-test marker,
and `Total: 1 test in 1 file`.

## Verification

- `sh -n scripts/testing/run-producer-public13-list.sh` — PASS.
- `git diff --check` — PASS.
- `node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list` — PASS; `Total: 1 test in 1 file`.
- Planted child argv/RC/output probes — PASS: list RC 0; run pass RC 0; run failure RC 1; zero output rejected; pass/nonzero rejected; multiple outcomes rejected; invalid mode rejected with RC 2. The temporary probe and its own TMPDIR were cleaned up.
- Missing mode and invalid parent mode probes — PASS; both RC 2.

No hosted build, browser, actual journey, or full suite was run, as required.

## Live callers changed

Only the two shared test-service suite entries changed. There are no product
callers of this wrapper in the App repository; the wrapper self-reference is
the only repository match.

## Next step

After review of this source/mode proof, the manager may submit one central
request using the distinct `...-actual-e2e-integration` suite. Its result is
not claimed here.
