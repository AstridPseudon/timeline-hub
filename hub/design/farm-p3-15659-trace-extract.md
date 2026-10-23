# P3 run 15659: trace extract (sanitized)

Worker: tf-p3-trace-extract. Read-only extraction, requested by app2 (INBOX "Preserve/extract existing P3 15659 trace", 19:28Z). No rerun, rebuild, browser, HTTP or new probe was made.

## Headline

- **`trace.zip` is LOST.** `error-context.md` is LOST too. The snapshot folder `.test-app-ap2-P3-gate5-h6-0348-1023190626-15659` no longer exists under `/home/user/work/wt/`.
- Searched: `find /home/user/work` for `trace.zip` and `error-context.md` (no hits); Glob of the orch scratchpad (no hits). Not searched: `/tmp` in full (a ripgrep timed out, and a `find` over `/tmp/claude-0` was not run).
- What survives: the raw log, the summary, the status and exit files, the run metadata, and the preflight native-seed log. The packet is therefore **partial**. It cannot show the in-browser basis GET, identity, or UI traffic for the failing run.

## Case / phase / tuple

| Field | Value |
|---|---|
| Suite | `ap2-P3-gate5-h6-0348` |
| Test | `M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent` (`tests/e2e/local/three-products.spec.ts:1533`) |
| Target / repo | `integration:app` / `app` |
| Requested | 2026-10-23T19:06:26Z |
| Result | `fail`, exit 1, 224 s total; the test itself ran 1.6 min |
| Phase reached | `openCommandTimeline` (spec line 1275, called from line 1537). Failed before the gesture. |
| App tree | `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c` |
| Source tuple (as logged) | `astridHead` 079580ca…, `runtimeHead` 2a9e347f…, `appHead` 43b71a9e… |
| Pinned in preflight | App HEAD `2107e1870e51c650d59315f4cc1ab6af338f198c` (HEAD or its parent, with the tree above) |

## Failure

- Error: `the mounted editor must claim a new durable command owner before the gesture`.
- Assertion: expected `ready: true`, received `ready: false`. Timeout 90000 ms.
- The predicate required a new `ownerId` absent from the previous owners, `pending` false, and an empty `intents` list.

## Mounted provider identity (project / timeline / selected)

**Absent.** No retained file records the mounted project, timeline, or selected identity for run 15659.

## Basis GET (route / status / head pair / error codes)

- Preflight only, not the failing run. The native-seed check in the same run chain (`preflight-trivialboot.log`) passed: `D21 full native seed: original helper assertions + authoritative history PASS`.
- Route in that check: `GET /v1/projects/{projectId}/timelines/{timelineId}/commits?limit=50`. Expected status 200. Expected head pair `{revision_id, publication_id}` equal to the accepted packet's. The assertions passed. No status value or error code was printed.
- In-browser basis GET for run 15659: **unknown**. It would have been in the lost trace.

## Authenticated identity (presence and scope)

**Absent.** No retained file records identity presence or scope. Nothing is inferred.

## Owner-claim / settled-record stage

- Owner-claim: **not satisfied**. The predicate timed out at the 90 s ceiling. No owner ID or claim state was printed.
- Settled-record: **not reached**. No Agent edit, ACK, or gesture ran.

## UI snapshots over time

| Time | Snapshot |
|---|---|
| Start (preflight, same chain) | Native seed and history PASS |
| End of the 90 s wait | `ready: false` (the only snapshot recorded) |

- `timeline-command-recovery` text was collected inside the predicate, but the harness does not print it. Its content is **unknown**.
- `runtime-connection-status` was **not recorded** in any retained file.
- No intermediate snapshots exist.

## Exact absences and unknowns

1. `trace.zip` and `error-context.md`: LOST (see headline). Their hashes cannot be given.
2. Mounted identity, authenticated-identity presence and scope, and the in-browser basis GET: not recorded.
3. Owner-claim and settled-record stages: not reached. No owner ID was logged.
4. `timeline-command-recovery` and `runtime-connection-status`: not captured.
5. **App head mismatch.** The logged tuple shows `appHead` 43b71a9e…, but the preflight pinned `2107e187…`. The preflight accepts HEAD or its parent, with tree `a3ff3584…`. I could not verify this without git access.
6. **Agent head mismatch in the run metadata.** The `ext` file lists `agent=78738040…`. The logged tuple and the pin use `079580ca…`. Unresolved.
7. `runner.log`: `test-run: line 55: …/tests/cache/2d9ab762…: No such file or directory`. Its effect on the run is unknown.

## Raw files retained

Folder: `workers/tf-p3-trace-extract/private-raw-15659/` (private, not published). Only the files below were copied.

| File | sha256 |
|---|---|
| `exit` | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |
| `ext` | `5cba91fd6f9a3b1bbe329b1c11a12b2010d038dbb3b26143ebd08a865852c0ca` |
| `request` | `1ee241dd62def52bd58a6bbda345618b820bfc905163214540773334ed4530d7` |
| `snap` | `82453329aa4006dc107a5932a8e7274ef0b8b6526509256de1329ee28d0be91c` |
| `status` | `2056a28ea38a000f3a3328cb7fabe330638d3258affe1a869e3f92986222d997` |
| `runner.log` | `0105b5a7404b0c7a380331845eea383f2bd46365a89db0293e41260bac4715fd` |
| `log.txt` | `d3d07149d0fc6951cb2befe7d60023487c47f9e341896fbdd45ea21f64248a43` |
| `summary` | `6bd84872519373c253bcfd6b2db7e3cdfdc58db53ea8049a5bf9adf2844777e3` |
| `preflight-trivialboot.log` (copy of `workers/tf-p3-bench2/p3-preflight.D79IrN/trivialboot.log`) | `c969e85b96362e40624007944deb1916810a59d2a8b11cb1b81c03a97704e464` |
| `trace.zip` | LOST, no hash |
| `error-context.md` | LOST, no hash |

Redaction: the raw summary contains a long preflight command with local paths and pinned SHAs. None of it is a credential, and none is repeated here. No URLs, tokens, headers, cookies, or principals appear in this packet.

## Next steps

- Re-run is out of scope here. If the trace is needed, it must come from a fresh run, not from this packet.
- App should resolve discrepancies 5 and 6 before relying on the tuple.
