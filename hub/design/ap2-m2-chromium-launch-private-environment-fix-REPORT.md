# Chromium launch private-environment fix

## Result

Fixed the central Chromium 141 SIGTRAP by keeping the browser's per-run
temporary/profile and XDG paths short and private under `/tmp`, while retaining
the one private App/Agent/Runtime run root in the worker snapshot. Added a real
Chromium page/DOM launch-close smoke before the ordinary journey and enabled
`pw:browser` diagnostics. No product assertion, browser binary, dependency,
timeout, or alias/source guard was changed.

App worktree remained based on `01230a5657853be85745566542af6546d254c28c`
(`c4965a7f5fe818a1cf2f6cb091ec4ff93fcde64a`). Changed files:

- `scripts/testing/run-central-m2-ordinary.sh`
- `scripts/testing/chromium-launch-smoke.mjs`

Script SHA-256:

```text
run-central-m2-ordinary.sh  4be2e03461b4910b482c2a0283178b3ea078e0687f87ded68c11ef56afc488b7
chromium-launch-smoke.mjs   0a071710ba246b22256ebbafcb22e14f75dbf1e514b33e7074ba7b28d050a64d
```

## Central evidence

The existing central suite was used; no local browser, localhost/socket test,
full suite, install, or browser substitution was run.

1. TestID `ap2-m2-chromium-launch-private-environment-fix-e2e-m2-ordinary-integration-1020191750-14430` — **exit 1**, 87s. The new smoke passed, then the pre-existing runner exposed a separate environment defect: the old `/home/user/work/venv-runtime` path did not exist, so the ordinary test stopped at its explicit Runtime-venv guard before interaction. This was not product evidence.
2. After changing only the runner to use the existing read-only `/home/user/work/venv-app2-native/bin/python` for both Agent and Runtime, TestID `ap2-m2-chromium-launch-private-environment-fix-e2e-m2-ordinary-integration-1020191951-23822` — **exit 1**, 100s.

For the corrected run:

- Chromium smoke: **PASS** page launch, DOM assertions, page close, browser close.
- Browser: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`; SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.
- Smoke environment: `TMPDIR=/tmp/tl-chromium-MzB7JI/tmp`, `XDG_CACHE_HOME=/tmp/tl-chromium-MzB7JI/xdg-cache`, `XDG_CONFIG_HOME=/tmp/tl-chromium-MzB7JI/xdg-config`.
- Actual ordinary Playwright profile: `/tmp/tl-chromium-MzB7JI/tmp/playwright_chromiumdev_profile-1GpcOJ`.
- Actual launch used the installed full Chrome and normal Playwright launch arguments, plus the existing harness's `--no-sandbox`, `--disable-dev-shm-usage`, `--no-proxy-server`, resolver, certificate, and address-space guards. It launched with exit code 0 and closed with exit code 0; **no SIGTRAP**.
- Captured stderr contained only the host's known DBus absence messages and a Google registration `DEPRECATED_ENDPOINT`; no fatal Chromium launch error.
- Hosted build: **PASS**, 5,570 modules, built in 1m 5s.
- Source tuple reached the real journey with Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and the expected schema/vendor-lock digests.
- Ordinary test reached the page and failed at `tests/e2e/local/three-products.spec.ts:1204`, first UI assertion at line 1216: `getByTestId('scene-markers-summary')` did not appear with expected text `2 markers` within 5s. The browser interaction path started; no ordinary command/producer result is claimed from this failure.

Central logs:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-chromium-launch-private-environment-fix-e2e-m2-ordinary-integration-1020191951-23822/log.txt
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-chromium-launch-private-environment-fix-e2e-m2-ordinary-integration-1020191951-23822/summary
```

## Validation

Passed locally without launching a browser:

```sh
sh -n scripts/testing/run-central-m2-ordinary.sh
node --check scripts/testing/chromium-launch-smoke.mjs
git diff --check
```

The central smoke and ordinary rerun were requested with:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-chromium-launch-private-environment-fix e2e-m2-ordinary-integration)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-chromium-launch-private-environment-fix-e2e-m2-ordinary-integration-1020191951-23822 1
```

## Disposition

The Chromium launch blocker is fixed and centrally verified with the actual
installed browser. The ordinary journey remains unqualified because the first
production Scene Phase Markers UI assertion is absent; this is separate from
Chromium and requires the App manager's product/extension investigation. No
further browser rerun was made.
