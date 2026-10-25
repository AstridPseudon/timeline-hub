# D127 report

- Used D89c’s original admission `5311045632` bytes; stop line remained `4000000000`.
- Exact pinned tuple and Node/tsx dependency resolution verified. No product/source changes.
- Normal D66 submit: preflight PASS, exactly one original P2 body queued.
- Terminal result: **FAIL** after 554s.
  - Readiness: 1/1 PASS.
  - Original P2: 5 PASS, 2 FAIL, 1 NOTRUN.
  - Failures: element status `applied` missing at line 1052; SWAP returned `history_unavailable` (line 495). `registerAsset` was serially blocked.
- Runtime private diagnostics were inspected; exact SWAP namespace binding was unavailable. No private payloads, credentials, URLs, or stacks published.
- JSON evidence, submission/terminal packets, durable plan, commit message, and `DONE` marker are present in the worker directory.

Commands/results:

```text
node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2 --submit
PASS preflight; one normal ID submitted

bin/wait-test app-pin-fe3309db-d73-p2-fe3309db-submit-1025140943-3250
FAIL exit=1
```

Recommended next step: independent `app-D125-P2-Proof-GO-review`; investigate `history_unavailable` and the missing element `applied` status before any retry.