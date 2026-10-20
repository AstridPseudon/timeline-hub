# App public13 environment preflight

## Result

ENVONLY is complete. No product source, target test, dependency install, pin,
DTO, build, browser, native UI, local server, or socket run was performed.

Central result:

- Suite: `public13-integration-preflight`
- Test ID: `ap2-m2-public13-environment-preflight-only-public13-integration-preflight-1020184006-23865`
- Exit: `0` / pass
- App snapshot tree: `05ac0dd35ee11f1ef593ca4b160d4bb3a781d8de`
- Command: `env PRELIGHT_ONLY=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-environment-preflight-only/public13-integration-runner.sh "$PWD" ordinary`
- Output: `v22.22.0`, `10.9.4`, `public13 integration preflight PASS mode=ordinary grep=M2 ordinary extension batch`

The runner is persistent at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-environment-preflight-only/public13-integration-runner.sh`.
It is parameterized for `ordinary` (`M2 ordinary extension batch`) and
`duplicate` (`M2 native occurrence duplicate`), and defaults to
`PRELIGHT_ONLY=1`. Its SHA-256 is
`6aef3cd4683f2c828f7fabb82d5cd9422933ac8526737f0661f082cfa7c88d72`; the
script is not product source.

## Guards performed

- Agent: commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime: valid 40-character commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`,
  tree `7ab412cc4bcbe517efcfa806e092336390312e18`. The malformed `...26a2`
  value is not used.
- Runtime lock source commit: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`;
  `runtime.lock.json` SHA-256:
  `550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2`.
- Locked graph archive SHA-256:
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Composition package: `0.0.13`; tarball SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Python: existing read-only `/home/user/work/venv-app2-native/bin/python`.
  Correct-PYTHONPATH imports passed for `astrid`, `astrid.__main__`,
  `astrid.sdk.timeline`, `astrid.sdk.timeline.commit`,
  `runtime_protocol.server`, `runtime_protocol.timeline_commit_provider`,
  `astrid_runtime`, and `astrid_runtime.cli`; `python -m astrid --help`
  passed.
- Node/npm: `v22.22.0` / `10.9.4`.
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`,
  `Chromium 141.0.7390.37`.
- ffmpeg: `6.1.1-3ubuntu5`.
- Current ordinary source grep was present in
  `tests/e2e/local/three-products.spec.ts`.

## Exact validation commands

```text
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-environment-preflight-only/public13-integration-runner.sh
PRELIGHT_ONLY=1 .../public13-integration-runner.sh "$PWD" ordinary
PRELIGHT_ONLY=1 .../public13-integration-runner.sh "$PWD" duplicate
```

Both local runs exited `0`; each created exactly one private run root under the
App worktree and removed it via the EXIT trap. The central ordinary run also
exited `0`. No shared node_modules or venv was changed; no private dependency
install was needed. Worktree status remained clean and `git diff --check`
passed.

An initial local attempt to list Playwright tests imported the normal config,
which tries to allocate an isolated port and failed before collection after 80
attempts. That socket-based check was removed from the ENVONLY runner. The
final runner is deliberately socket-free and only performs static source grep;
it does not claim Playwright collection, hosted build, or browser readiness.

## Deferred actual gate

Actual browser/native UI remains held exactly as directed because App provider
forwarding and the approved join SHA are absent. Once that committed App
forwarding lands, re-run the same source guards and use the central service with
`PRELIGHT_ONLY=0` and the exact candidate:

```text
env PRELIGHT_ONLY=0 sh .../public13-integration-runner.sh "$PWD" duplicate
env PRELIGHT_ONLY=0 sh .../public13-integration-runner.sh "$PWD" ordinary
```

Those commands alone do not constitute evidence until the central result
passes. No old invalid central run was repeated.
