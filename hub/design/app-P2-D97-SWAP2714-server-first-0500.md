# SWAP2714 server-first report

- Read-only inspection completed. No product/test files changed; worktree is clean.
- Retained artifacts inspected: manifest, readiness/XML, phase JSONL, runtime stderr/stdout, terminal metadata, and network trace.

Findings:

- Exact route: `POST /api/runtime/v1/projects/{project_id}/timelines/{timeline_id}/commit`.
- Observed response: HTTP 503, `not_ready`, reason `runtime_unavailable`.
- Browser network timing: 3156.725 ms total; 3153.045 ms wait. This is not a server-duration measurement.
- Server phase capture contained 128 events. Two complete 200 phases were retained; the final phase reached provider start and ended after 291.873 ms due to capture truncation, without provider completion, receipt, or HTTP event. Actual failing server duration is UNKNOWN.
- Runtime stderr was empty; terminal metadata had 158 records, including one failed record, but no exception, route, phase, or action correlation. No retained Agent exception/watchdog record was available.
- Source permits generic mapping through `CommitOutcomeUnknown` or `CommitUnavailable`, but the retained evidence cannot distinguish them. No lock, timeout, provider, or busy cause is inferred.
- Native Undo POST presence and shape were established by the prior wholepath report, but no safe server-side correlation to this phase capture or terminal record was retained.

Comparator tuples:

| Case | App | Agent | Runtime | Composition |
|---|---|---|---|---|
| failing SWAP2714 | `3199118d` | `5faeec5b` | `0c62dfa6` | `635f4de0` |
| passing single5678 | `24865fa2` | `6386c700` | `6634a17f` | `635f4de0` |
| passing asset27438 | `5337b439` | `6386c700` | `6634a17f` | `635f4de0` |

Runtime route/error seam files are byte-identical between failing and passing Runtime sources. Tuple differences do not establish a common cause.

Evidence hashes:

- `manifest.json`: `49e8305dd40495f45658b09525bbf18e7eabae5f1492a4351b773731d503216b`
- `p2-commit-phase.jsonl`: `4eb8132666a281baa6758db15e21acf8c6bfb67fe1e816244214d708d8b971c1`
- `trace.zip`: `e36dec151b86d365b2248b6c7393a4df9bd0f081e2fa8b305910c57ac05aa213`
- Runtime `server.py`: `1ca8ec077415e988856e3b7c747a3a123ab6a982344c32293d60fd00931562c0`
- Runtime `service.py`: `5e79c3b9ed3d2ba5efc129d1cc8d7a43075c4ebc9194026fdb641a8eeb7ff19a`

Safe-export sensitive-pattern scan: 0 matches.

Tests: none run; this was explicitly a READONLY evidence task with no test/build/lint/browser requirement.

Commit message was written and `DONE` created. Recommended next step is to consume any separately retained daemon exception record if one exists; current artifacts do not justify a product fix or source owner.