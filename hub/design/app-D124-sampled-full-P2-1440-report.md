## D124 report

- Ran exactly one D66 `p2 --submit` through the frozen tuple with the reviewed D126 helper.
- Protected activation and source custody: PASS.
- Admission: `5,331,136,512` bytes; 4 GB stop floor preserved.
- Source preflight: PASS.
- Submission: one body, zero duplicates; same actual ID waited to terminal.
- No App source/test/generated changes; worktree is clean.
- Commit message written for harness: `test(app): D124 actual sampled full P2 same ID`.

Tests:

```text
preflight wait-test: PASS
normal wait-test: FAIL, exit 1, 568s
```

Results:

- Readiness: 1 PASS.
- Originals: 5 PASS, 2 FAIL, 1 NOT RUN.
- First unmet: element edit line 1052 — backend outcome UNKNOWN, no response before page close.
- SWAP line 495 — HTTP 409, static reason `history_unavailable`.
- `registerAsset` line 1133 — NOT RUN due serial predecessor.
- No self-GO or independent verdict claimed.

Actual-element profiling retained 20 request records, 6,089 samples, 109 lost samples, and safe top-10 inclusive frames. Browser/helper key join and exact arrival/lock boundaries remain UNKNOWN; frame counts are not treated as CPU time. Raw payloads, credentials, private URLs, and stacks remain private.

Recommended next steps: independent App verdict; Runtime separately handles SWAP history/log correlation; investigate the element request’s missing response before any retry.