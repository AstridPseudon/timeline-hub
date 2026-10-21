# Original parent-split local preflight — r54

Status: **HELD / not executed**.

This packet prepares the existing original parent-split runner only. It does
not run a Runtime, browser, Vite, or original split test. The required serial
gate remains unresolved: r51 records Trim as terminal-fail before admissible
action evidence, and r53 proves only the wrapper's intentional negative
propagation (`child 7 -> wrapper 7 -> service FAIL`). Historical Trim8788 is
still `UNKNOWN`; it is not replayed.

## Inputs carried forward

- r51: App `92c30b570cf8105dc021a64874c258e6c950b841`, tree
  `c34d65b66481fd0015279451b175c53b7b5e8f4f`; no split list or actual was
  submitted.
- r53: wrapper custody/negative control passed; no Trim retry, browser, graph,
  credential, or full-suite run.
- Existing split packet files remain byte-identical:
  - `tests/e2e/local/parent-split-command.spec.ts`:
    `48938cfeffed2f3d6180206a4e7744c00979b31a14021f61c66ff98638f1f574`
  - `playwright.parent-split.config.ts`:
    `7eb1bff0269a554f1b9bfd5d750c622cec07b3472827f68290874fc4b690bad4`
  - `scripts/testing/current013-parent-split.mjs`:
    `93c0a21a35ca9a6d254aa12ad7150994ff870e1f7eeac4ecf78172d4a05c86b7`
  - `scripts/testing/current013-parent-split.test.mjs`:
    `0cd2e7cbbef272e5ac8d8f6ea5e515498fa6dc78c4815c6658a835937b046449`
- Dependency tuple: Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`,
  Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, Agent vendor
  `091aa23ec83ea05ffd3b0115a640230d51c8c429`, public13 archive
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  Runtime all76 digest
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

## Executable preflight

The preflight is [app-original-split-local-preflight-r54.sh](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-original-split-local-preflight-r54.sh>). It is pure and fail-closed: it creates no directories and never sets
`TIMELINE_CURRENT013_RUN=1`. It requires the caller to provide existing
manager-owned paths, so missing private13/source/credential/lease inputs are
reported together by the first failing guard rather than materialized here.

Required inventory:

```text
MAIN APP AGENT AGENT_VENDOR RUNTIME GRAPH PRIVATE READY LEASE EVIDENCE
NODE CHROME TMP SOCKET SHORT CREDENTIAL PORT
```

The script verifies:

- exact App source/tree, clean source keepers, Agent 6ef, Agent vendor 091,
  Runtime 95bd, and all four original split packet hashes;
- public13 archive digest and exactly 77 safe regular members;
- private13 graph ownership, no symlinks in the graph, App-to-graph overlay
  identity, peer versions, Runtime all76 manifest, READY/LEASE binding,
  mode-0600 App Runtime product credential, and forbidden credential actors;
- Node `v20.19.4`, executable Chromium, physical mode-0700 private/evidence/
  temp/socket directories, short temp/socket paths, disk floor, and a clear
  native port observed with `ss`;
- `ASTRID_PACK_HOST_PYTHON` and `ASTRID_PACK_HOST_HELPER_CHECKOUT` unset;
- the existing source/vendor-lock checks, the existing cache identity, the
  exact list argv, and exactly one selected test in one file; and
- source and overlay postflight equality after the pure checks.

The preflight's list command is exactly:

```text
npm ["run", "test:e2e:three-products", "--", "--config", "playwright.parent-split.config.ts", "--list"]
```

No `--grep`, selector, timeout, retry, FPS, tolerance, or alternate config is
introduced. The TimeRuler and split assertions are untouched.

If an exact source-descendant keeper is absent, request that keeper through the
orchestrator's existing checkout mechanism and stop. Do not clone, install,
build, extract, or replace the graph. Reuse an existing validated list record
only when its source/tree/runner/cache identity is byte-identical; otherwise
the pure preflight may perform one list1 collection and must retain its output.

## Later actual, explicitly not authorized here

After Trim reaches a terminal result and the r53 wrapper negative proof is
accepted, the same private environment may invoke the existing runner once.
The runner's exact actual child argv is:

```text
npm ["run", "test:e2e:three-products", "--", "--config", "playwright.parent-split.config.ts"]
```

The invocation must be the existing `scripts/testing/current013-parent-split.mjs`
with the preflight-produced `TIMELINE_CURRENT013_CACHE_ID`, `TIMELINE_CURRENT013_RUN=1`,
the same absolute paths and bundle heads, `env -i`, and
`PLAYWRIGHT_OUTPUT_DIR="$EVIDENCE"`. It must be one actual only; any non-zero,
extra, skipped, flaky, legacy, renderer, source-drift, or unexpected retained
failure is terminal failure. The shell command is deliberately not run or
registered by this worker.

## Bounded missing prerequisite

The worker cannot return an execution READY marker because the Trim serial
gate is not terminal and the private13 source/graph/credential keepers are
manager-owned external inputs. The packet is ready for the executor to run
the pure preflight once those inputs exist; the original split actual remains
separate and unauthorized.
