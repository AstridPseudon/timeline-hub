# App normal014 central harness report

## Result

Private harness preparation and execution-dependency audit **passed**. Central
execution is **pending manager registration** of the two new exact-source App
suites. I did not submit an existing lane that would run the 0.2.13 App lock,
moving integration checkouts, or historical 013 proof.

## Prepared files

- `normal014-source-common.sh`
- `normal014-parent-media-central.sh`
- `normal014-app-central.sh`
- `app-normal014-central-harness-proposal.md`

All are under the requested absolute design directory. The runners create only
private temporary clones/overlays and clean them by default. The App overlay
uses the leased public13 graph through a verified read-only symlink; no install
or shared dependency/cache write is attempted.

The runners now also create a copied-interpreter venv below each run root from
`/home/user/work/venv-app2-native/bin/python`. The only installed requirements
are Runtime/Agent-declared `jsonschema>=4.18`, `referencing>=0.30`,
`PyYAML>=6.0`, and the test requirements `pytest>=8`, `pytest-timeout>=2.4`.
Agent and Runtime source are imported by `PYTHONPATH`; no shared
`venv-agent`/`venv-runtime` path is used.

## Exact source and byte guards

Passed in both runner preflights:

- Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d` / tree
  `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`.
- Runtime `202074110717146fc7f08af2306a8dd7f695b0b1` / tree
  `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` / tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`; Runtime candidate is its
  descendant.
- 75 manifest entries, manifest digest
  `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`, and
  every candidate/producer artifact byte match.
- Shared schema digest
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` and
  Agent/Runtime schema byte equality.
- Private App `vendor-lock.mjs update`, producer-aware `check`, and local
  `check`; generated metadata/client/schema hashes match the normal014 private
  qualification report (`9b3b…`, `c422…`, `f8cb…`, `f52b…`).
- d05e test blob `150a7abb340040e45c34742bc871ef83caab0575`, with both the
  owner-strict refusal test and complete positive test body retained.
- Locked App graph archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`,
  Composition artifact SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, and
  `computeMediaTrim({from: 0.5, to: 1.5}, 30) = {trimBefore: 15, trimAfter: 45}`.

## Commands and results

```text
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-*.sh
PASS (shell syntax)

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh preflight
PASS: source tuple, 75 artifact bytes, schema, producer ancestry, d05e marker,
      locked public13 graph, private Python imports/CLI, parent-test collection,
      ffmpeg, and ffprobe

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh preflight /home/user/work/wt/ap2-m2-normal014-runner-env-fix
PASS: source tuple, 75 artifact bytes, private vendor-lock update/check, 014
      generated hashes, private Python imports/CLI, provider-test collection,
      Chromium executable, and Playwright Gate 5 collection
```

The first private import attempt failed only because the app2 venv did not
provide `yaml`; adding the Agent-declared `PyYAML>=6.0` requirement made the
fresh preflight pass. No unlisted dependency, renderer, or heavy extra was
installed.

The repository worktree remains unchanged and clean. No browser, localhost,
socket, Runtime daemon, parent-media acceptance, Gate 5 journey, full suite,
build, package install into shared paths, or central request was run by this
worker. Those two live runs must be made only after the manager registers the
literal suites in the proposal.

## Marker boundary and blockers

The d05e marker is carried only in a private test-file overlay. Its current-
schema refusal is not claimed as Runtime 202 proof. The Runtime 202 positive is
selected separately and run with `--runxfail`, preserving the complete positive
body and assertions. No 013 result is relabelled.

The central allow-list still needs these App-owned names registered:

```text
app normal014-integration-parent-media-accepted bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh run
app normal014-integration-e2e-gate5 bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh run "$PWD"
```

After registration, request each once through `request-test` and record the
central result IDs/logs here. No release, adoption, activation, pin movement,
or merge is authorized by this report. No local browser, socket, Runtime
daemon, parent-media acceptance, Gate 5 journey, full suite, build, package
install into shared paths, or central request was run by this worker.
