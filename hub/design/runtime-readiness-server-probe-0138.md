Ask: server diagnosis / Owner: Runtime / By: 2026-10-24T02:30Z.

**No hang reproduced; historical cause remains UNKNOWN.** The new diagnostic establishes slow history authentication, with actual handler entry/completion and bounded stack/lock captures. No product repair was justified or authored.

Added an explicit-only probe under `tests/`. Original tests, product source, guards, auth, timeouts and readiness semantics remain unchanged.

| Condition | Direct GET | Browser-door GET |
|---|---:|---:|
| Concurrent native21 seed | 0.056s, HTTP 200 | 0.054s, HTTP 200 |
| Completed native21, no writer | 5.598s, HTTP 200 | 6.277s, HTTP 200 |
| Completed P1 seed | 0.972s, HTTP 200 | 1.059s, HTTP 200 |

Concurrent reads overlapped the genuine seed commit and returned its preceding baseline. Health completed in 0.066s; preflight returned 204 in 0.017s. Both completed seeds exercised real cursor pagination through both listeners: stable heads, no duplicate publications. All 18 requests completed, and every observed method entry had a completion.

The named source of measured latency is repeated authentication along `list_timeline_commits → head/history → history_entry → _verify_accepted → _historical_sequential`. Each completed `limit=50` request authenticated the accepted seed three times. For native21, `_historical_sequential` consumed 5.15s direct and 5.78s through the door; sampled stacks show JSON-schema validation while the request thread owns the store mutex. This demonstrates verification work, not deadlock. Timings include diagnostic instrumentation.

These are **new observations**, not recovered historical evidence. Concurrent writing remains comparison-only: the historical fixture awaited seed acceptance before bootstrap.

Exact source selections:

- Native21: App `804134d74782d40855146aa568ff289200b79142`, Agent `079580ca46af77e0292d49dc34386b25c8391f99`.
- P1: App `f8b15af0a66ed14e7711a4bb7f1ed5b62b4988b5`, Agent `78738040d72ce74c42ddf7731221aecb06f9246d`.
- Shared Runtime: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

The tuples differ. Actual authoring daemons used `/home/user/work/venv-agent/bin/python`, imported Runtime from the live service snapshot, and imported Agent from each frozen scratch archive. Import hashes matched the selected sources.

Durable, credential-scanned captures and file hashes are indexed in [diagnostics/readiness/manifest.json](/home/user/work/wt/rt-R-readiness-probe-sol-0138/diagnostics/readiness/manifest.json). They total approximately 1.1 MB.

Validation:

```bash
$ORCH/bin/request-test rt-R-readiness-probe-sol-0138 targeted --files tests/readiness_commits_probe.py
$ORCH/bin/wait-test rt-R-readiness-probe-sol-0138-targeted-1024013715-21238 1
```

**PASS: 2 tests in 65.94s.** Initial request `1024013649-14946` failed before fixture execution because the service omitted `TMPDIR`; the probe’s scratch-path fallback corrected that setup issue.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /tmp/w-a1885cc6b0/qualify_readiness.py
git diff --check
```

**PASS:** 12 Python AST checks, frozen-source/import hashes, capture credential scans, completion checks and final integrity checks for 18 capture files. TypeScript parsing passed for the driver and both extracted seed functions.

No browser journey, original P1/P2/P3 body, full suite or unrelated suite ran. No blocker remains for this diagnostic task. Commit message and `DONE` are written.

Recommended next step: independent review and manager export of these captures. The observed verification cost is concrete; attributing the historical unfinished requests or choosing an optimization requires a separate judgment.