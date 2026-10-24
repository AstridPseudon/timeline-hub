## Verdict

**PASS for the complete IMAGE0554 actual-witness scope. A4 IMAGE may close for this behavior.** No live body rerun, browser, HTTP, SDK, or full-suite run was performed.

### Predicate matrix

| Predicate | Result |
|---|---|
| Fresh same-alive fixture and custody | PASS — READY 05:32:29Z; output before 05:57:29Z; no old request/realm reuse evidenced |
| Input/output custody | PASS — input 8,957 bytes / `2858a70d…a7dce`; output 1,492 bytes / `7f90b347…9a404c`; published copies byte-identical |
| App path | PASS — prepared-image preview → `createLocalSaveSession` → outbox/handoff capture → request/hash |
| v2 request | PASS under contract — required fields present; semantic reads were provider-captured (15 reads, 13 dependencies). Top-level and step `reads` keys were omitted; they are optional in `commit-v2.md`, so this is not an all-optional-fields-populated request claim |
| Runtime acceptance/retry | PASS — `txn-968aea8ef6b64a3db6a91f1dc3045e7a`; exact retry byte-identical |
| Foreign selection / changed body | PASS — both refused with head/database unchanged |
| Undo preview/undo/retry | PASS — preview had `would_status=accepted`, `receipt=null`; undo `txn-efb5a44036bb475ba3de1edf6700599c`; exact retry byte-identical |
| Canonical restoration | PASS — original parent revision/content digest, raw `visual.opaque=[null,false]`, three child revisions, occurrences, pins, and original registry restored |
| History | PASS during live harness assertion; accepted and undo receipts were found in history. No standalone history JSON was retained |
| Source/assertion preservation | PASS — commit `3d457697…` changes only worker/evidence/output constants relative to qualified `2007cf7…`; reviewed forwarding `0df7…`, foreign helper `a103…`, and post-undo correction `007164…` are ancestors |

Canonical comparison is about document payload/revision content, not literal equality of all transaction metadata. Accepted/undo publication IDs, receipt IDs, event IDs, timestamps, and heads necessarily change.

### Source and custody limits

- App source commit: `1c5cc47bf6841c140587f6e1b9164ffb76d433a7`
- Handoff blob: `f4f6b4f95c430956b1a5c05750ac3e4573286785`
- Producer blob: `8f686e3e3be448995eae1c43a9e86d1dee217aeb`
- Agent: `2007cf7aaf5d304964e68a33e967502a16de1d24`
- Runtime: `8ea0766f5e9fb23cea26c7398770a8aaac06b258`

`results.json` incorrectly labels the handoff blob `f4f6…` as `app_commit`. The actual App commit is `1c5cc…`; this immutable metadata was not rewritten.

The witness used direct `RuntimeService.commit_timeline` with publisher `app-image-witness`. It does not prove HTTP transport, bearer authentication, or an authenticated actor identity.

### Checks

- Offline retained-boundary pytest: `1 passed, 1 warning`
- Ruff: passed
- Private mypy: passed
- Vendor lock: passed
- Artifact manifest: passed
- `git diff --check`: passed
- Retained JSON parse/hash and retry byte-equality checks: passed

No blockers for the A4 IMAGE row. Recommended follow-up: preserve the explicit App-commit/blob mislabel in the final gate record and avoid expanding this witness into broader HTTP/auth or structured-error coverage claims.