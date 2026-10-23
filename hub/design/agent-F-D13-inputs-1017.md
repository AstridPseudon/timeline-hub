# Agent F D13 input handoff — 2026-10-23

## Verdict

**PASS for the missing D13 input contract, not a native qualification.**

The exact original failure was missing `ASTRID_D13_SOURCE_PROFILE`,
`ASTRID_D13_EXPECTED_BINDINGS`, and native/browser/tool path/hash inputs. A
private seven-key carrier now exists at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D13-inputs-1017/d13-bindings.json`

It references the existing durable noneditable profile and wheel, not invented
aliases or test authority. The profile is:

`/home/user/work/venv-agent-child-f1012-installed/profile/astrid.json`

The private carrier was materialized from the reviewed existing D13 seven-key
binding producer contract (`d13_bindings.load_inputs`, donor
`806860a046fc4eba467f8b4a80871d62ef2d2e7c`). No producer code, test, product,
launcher, contract, schema, pin, or shared dependency was changed.

## Cross-check

- Current Agent: `ef851b22c506245441b9a630c093b3460e39cbdc`, tree
  `b11eee891208d11e23c55950f8954ddd3377d5a8`.
- Installed Agent wheel SHA-256:
  `fcccab4dc881faa4eead1f971fc655dc96ebfac9efac199015794d7b644007e3`.
- Installed source digest:
  `302834da6581954c2cb070e99fb4021bea6775cdde2ba351057ca832279f2326`.
- Profile SHA-256:
  `8339f65743af469f940dbc5e25780e97204d048e35ebc83a773584fc3ab72352`.
- Installed origins for Agent, Runtime protocol/platform, Runtime, client,
  and shared schema all resolve under the selected private site-packages tree.
- Existing durable audit: 164 dependency pins match; 182 RECORD files are
  unchanged and contained. D13 preflight checked the Agent RECORD and wheel
  source archive parity against current `ef851`.
- Node20 SHA-256:
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Composition14 lock SHA-256:
  `b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`.
- Chromium, FFmpeg, and FFprobe hashes were checked as recorded in the worker
  report. Free disk was 15 GiB, at the required floor.

## Commands/results

- Exact D13 preflight with isolated `env -i`, selected installed Python, the
  private profile/binding carrier, Node20, Composition14, browser and tools:
  **1 passed in 4.04s**.
- Exact original node collected once with the same selected inputs:
  `--collect-only`: **1 test collected in 0.74s**.
- Existing service row script:
  `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-d13-installed-preflighted-one-native-1011/run.sh`:
  **exit 0**. The row was not activated or run.

## Handoff/limits

The available durable installed profile is owned by the separate F-installed
worker and carries Runtime `1365e4b17b31c4a7093d5943674637067fd2bab4` / tree
`6c69c3dc47822fffbaf27cd63815d2895155ffaa`. It is therefore not proof of the
frozen current Runtime 34e/d106 tuple. U2b must select or produce (through the
same normal custody/profile producer) an installed pair for that exact frozen
tuple before native activation. Do not relabel this profile or reuse the
historical f4ed service row.

No daemon, socket, Runtime, HTTP, browser, renderer, native, or full suite was
run. Full-v2 request/reply fields and frozen pins remain untouched.

