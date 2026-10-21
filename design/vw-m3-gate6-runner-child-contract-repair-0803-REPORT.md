# Gate 6 runner child contract repair — 0803

**Blocked after the sole physical request: 5 setup failures, 0 passes, 0 comparison bodies.** The lock-marker repair worked: issue completed, controller READY passed, and all five cases were attempted. Chrome then refused its actual Unix socket path. No retry or alternative request was made.

Packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803`. Frozen App d00/a8bf, Agent d0a, Runtime SERVER8f versus PRODUCER2c4/client013, Composition source5a4/public13/9412/all77, helperb70/bc75, App8bdc/32393 and Runtime4913/21455 graphs, Node20.19.4/43d6 and Chrome155 remain unchanged.

## Changes and decisions

- Copied only the six tiny operational scripts into this owned packet. The old 0739 scripts/evidence and its historical empty physical namespace are untouched. New physical namespace is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/gate6-20261021T0803`; it now contains real authority and must never be reused.
- Added the existing `VIEWING_BROWSER_FLOCK_HELD=1` fact to the clean issue child. Actual `issue.mjs:27` directly calls frozen `harness.ts:110`; 0748's contrary classification was wrong. The original parent fd9 lifetime, actual competing-lock guard and wx issuance remain intact.
- Found a second missing normal-child fact before central: `_host_render_environment` returned no schema path under the actual normal environment. Full production validation already selected `/home/user/work/venv-agent/lib/python3.11/site-packages`; supplied that same `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` to the four clean Node invocations so the normal helper receives its validated input. The frozen Agent has no remotion/node_modules fallback. `schema-path-negative.log` preserves the actual missing-path witness.
- Retained 0739 diagnostic/physical separation and all guards, including clean-env refusals, source/tool/graph/77+75-byte/inode/ancestry/dist/GET/collection/floor checks. Retained 0753's `result.tuple.appSource` correction. No product, package, dependency, API, controller, fixture, assertion, tolerance, dispatcher or Git changes.

## Exact tests and results

One central preflight:

`vw-m3-gate6-runner-child-contract-repair-0803-e2e-viewing-gate6-child-contract-preflight-0803-1021081033-19977`

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/run.sh --preflight
```

**PASS, exit 0, 41 seconds.** Actual complete production validation passed; PYTHONNOUSERSITE and GIT_CONFIG overrides were refused; exactly five normal cases collected; exact GET200 and private server closure; tokenIssued/browserLaunched/runtimeStarted all false. Evidence: `evidence/preflight-uHiB51/preflight.json`. Final preflight free bytes 11,460,988,928 exceeded threshold 11,320,247,244 and floor 10,737,418,240. Both central snapshots used unchanged Composition tree71d8e95edb1bb2d187c3193ef3462d4cfde277fa; measured allocation880640 bytes fits the retained2290636-byte snapshot reserve, additional delta0. No App/graph snapshot was duplicated.

Only after that actual PASS, one physical request using the same immutable packet:

`vw-m3-gate6-runner-child-contract-repair-0803-e2e-viewing-gate6-child-contract-physical-0803-1021081154-29863`

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/run.sh
```

**FAIL, exit 1, 363 seconds.** Repeated full preflight/production validation passed under fd9, fresh tuple/grant/marker were exclusively issued, controller READY passed, then normal Playwright ran five cases with retries=0 and one worker. Runtime and reviewed helper fixtures reached readiness before browser launch.

All five failed in Player browser setup (`harness.ts:292`, surfaced by aggregate at305), before their case bodies:

| cases.ts line | Exact case name | Result |
| --- | --- | --- |
| 229 | normal App Render action downloads a valid native-size MP4 without a parity comparison | setup FAIL |
| 246 | fixture readiness seeks actual managed Player video and captures native frames without export | setup FAIL |
| 267 | compares native-size actual Player frames with decoded real CPU Remotion task output | setup FAIL |
| 277 | captures the actual Player page as one native-PTS VP8/Opus tab stream without a physical-mix claim | setup FAIL |
| 317 | picture-only one-host patch is reported as a mismatch after the full passing baseline | setup FAIL |

Local checks before central:

```sh
bash -c 'exec 9>>/tmp/timeline-viewing-browser.lock; flock -x 9; python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/check-child-boundaries.py'
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/run.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/preflight.sh
(cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803 && sha256sum -c SHA256SUMS)
```

PASS: eight real frozen `assertRunBoundary` controls (positive and missing-marker refusal under each of the four actual clean environments), plus actual frozen host/worker projection/context guards under the normal helper environment. This was readonly: no issue or fake authority/validation was invoked. Absolute Node20 `--check` passed for prepare.mjs, issue.mjs and dist-availability.mjs; Python AST parse passed for both Python files, all from foreign cwd `/tmp`. The first added Node->Python readonly probe completed its body but returned sandbox wait EPERM; that failed local attempt is retained and the final readonly probe used direct Python under the same environment. No full suite was requested.

## Actual blocker and unverified behavior

All five retained traces contain Chrome's `FATAL ... Socket path too long`. The actual path is188 bytes, exceeding the108-byte AF_UNIX sun_path capacity:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/tmp-5aZG7i/com.google.Chrome.<suffix>/SingletonSocket`

`preflight.sh` supplies its long packet-owned TMPDIR to the normal Playwright child. Controller `assertOwnedShortTemp()` verifies and removes a separate direct-/tmp directory; it never validates the actual propagated TMPDIR. Its PASS and the prior custody approval therefore did not establish this normal browser contract. I missed that downstream socket-path constraint before the sole physical request. This is the concrete next runner issue; no product deviation or retry was made after finding it.

**Unverified:** same-normal-CPU-export versus actual Player frame and PCM positives; picture-only mismatch detection; half-gain PCM rejection. No raw PNG, WAV, MP4 or tab recording was produced. Five raw trace ZIPs, five error-context files, the issued source tuple/grant/marker, both actual service logs, invocation logs and preflight JSON are preserved. Counts and missing artifacts are explicit in `results.json`; all paths/bytes/SHA256 are in `result-map.tsv`.

Cleanup: all five traces report successful worker fixture and harness teardown steps; no owned tmp-/validation-/diagnostic-/context- directories remain. Final observed free11,316,125,696 exceeds the10GiB floor (it is below the larger launch threshold; no new request was made). `cleanup-summary.json` preserves these observations. Independent process-wide absence was not separately probed; no stronger cleanup claim is made. The new authority namespace and all historical failed evidence remain intact.

Next: manager authorization is required for another physical attempt. First make the actual propagated normal TMPDIR an owned short direct-/tmp path, verify its real Chrome socket suffix length before central, and retain the existing lock/clean-env/schema/guard behavior. Do not reuse either issued or historical namespace. Gate6 remains OPEN.

## Packet and evidence map

- `CHILD-CONTRACTS.md`: required/supplied per-child facts and actual import/body chains.
- `CHILD-COMMANDS.txt`: exact clean env/argv blocks, including normal-only branches.
- `PACKET-DIFF.patch`: complete minimal difference from retained0739.
- `source-map.tsv`: absolute packet/source paths and hashes.
- `result-map.tsv`: absolute raw result/log/source/authority paths and hashes.
- `trace-findings.json`, `cleanup-summary.json`, `results.json`: extracted terminal evidence.

Final immutable packet SHA256SUMS:

```text
6b7527d414bc30c0595bea3b93fd182198f2cf30aaf4915930e1e9bacfd58949  run.sh
ad0e93cb725763ac5180aed06f18a880a21564890f727e809ddabefac8bf2078  preflight.sh
7ad93869a27ff241319559881ade5207c65005f1b1bf9cdb7eb5641a713fd074  prepare.mjs
8c6fc14d75c8cd486b08389fc9bdcde1b21ab1ce74f7655d6f9721697fdf854f  issue.mjs
fb7632d2c69da10c65db04052f0b04ede1b6e72064817fdc600098135ea50dfd  dist-availability.mjs
24be3f3479faafb0676e6a7d18b055e7f1079fa5436802ad0cba7a81124b0c59  prepare-validation-diagnostic.py
```
