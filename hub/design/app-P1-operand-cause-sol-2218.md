**Verdict: PRODUCTDEFECT reproduced from actual24510’s retained accepted split document.** The rejecting arm is config comparison; registry comparison passes. No product code or tests changed.

At base `e6d72d3d07d2df485e4f3e86c56d1eb2dd5cd91a`, the offline production path produced:

| Comparison | Equal |
|---|---|
| Source config versus loaded config | false |
| Source config versus projected config | false |
| Source registry versus projected registry | true |
| Source versus projected config, excluding output | true |

Exactly two projected-config fields differ: `output.background` and `output.background_scale`. Both are absent from the captured parent output and reconstructed source; both have null defaults in the loaded/projected views. Resolution, fps and file compare equal.

The cause is deterministic:

- [Accepted-response adoption](/home/user/work/wt/app-P1-operand-cause-sol-2218/src/tools/video-editor/hooks/useTimelineSave.ts:231) passes the canonical config directly to `buildTimelineData`.
- [Assembly](/home/user/work/wt/app-P1-operand-cause-sol-2218/src/tools/video-editor/lib/timeline-data.ts:461) applies output defaults only when resolution is missing. This accepted document already has resolution, so the two absent fields remain absent.
- [checkSource](/home/user/work/wt/app-P1-operand-cause-sol-2218/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:68) applies defaults unconditionally before comparison.

The real handoff `flush()` followed by `capture()` reproduced the exact mismatch rejection before append: **append calls = 0**. The reconstructed selected clip matches every retained numeric observation. Source inspection found no intervening config normalization in adoption.

**Custody and limits:** inspected only the authorized case directory in run `app-P1-preflight-inner-return-2147-ap2-P1-chain-h6-1023215343-24510`. Its 4,069,244-byte trace contains two matching network entries with identical accepted canonical documents. Selected provenance: `0-trace.network`, resource `244e06481d456bb90e1128e571f8efaa574adde6.json`; document/head matching passed privately.

Only the canonical document and previously safe diagnostic identifiers entered private scratch. No credentials, request bodies, receipts, raw trace or error-context content were exported; no request-body hash was invented. The safe diagnostic’s SHA-256 remains `faa0df373a0ae84dfd3ba56aab81988a65435c31b339ec91864be1bb299e4b0f`.

Historical in-memory operands remain unrecorded. These operands are **reconstructed through production source**, not directly observed mounted values. The offline runner used a constant asset resolver, config counter 1 and a session boundary stub; it did not exercise React mounting, durable outbox, HTTP or rollback. Actual24510 still never reached the second POST, Agent move or Runtime 409.

Validation commands:

```bash
python /tmp/w-8699780177/select_document.py
TSX_TSCONFIG_PATH=/home/user/work/wt/app-P1-operand-cause-sol-2218/tsconfig.json node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs /tmp/w-8699780177/probe.ts
git diff --exit-code
git status --short
```

Final results: selection passed; all probe assertions passed; diff/status clean. Initial runner setup encountered TSX IPC and child-process `EPERM`; the successful run used direct Python selection and the Node loader. No suite, browser, service, lint or typecheck ran.

Recommended smallest fix: normalize accepted-display config consistently with the existing Runtime load path before building the adopted source, preserving authored document data and the guard. Add regression coverage in `useTimelineSave.test.tsx` for accepted split → trim with resolution present and both optional background fields absent; retain mismatch-refusal coverage.

No implementation authorized or performed. `commit-msg` and empty `DONE` created. Ready for `app-P1-operand-cause-review-2218`.