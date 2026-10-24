# P2/P3 corrected-pair terminal handoff

- No product/test changes; worktree clean.
- Commit message written; `DONE` marker created.
- No direct suite execution.

## Requests

Both exact retained requests were waited on with `wait-test <id> 15`; both terminated immediately:

| Request | Request/start/end | Status | Exit | Result |
|---|---|---|---:|---|
| `app-P2-P3-source-rebind-0623-full-e2e-three-products-1024063415-20674` | requested `06:34:15Z`; first log `06:34:20.724Z`; terminal `06:34:25.198Z`; reported duration 6s | FAIL | 2 | D21 preflight `App-source-head`, `App-snapshot-tree`; journey NOTRUN |
| `app-P2-P3-source-rebind-0623-ap2-P3-gate5-h6-0348-1024063415-10144` | requested `06:34:15Z`; first log `06:34:20.845Z`; terminal `06:34:25.417Z`; reported duration 6s | FAIL | 2 | D21 preflight `App-selected-source-tree`; journey NOTRUN |

Safe terminal tails:

- P2: `P2 D21 PREFLIGHT NOTREADY: App-source-head App-snapshot-tree global-setup-NOTRUN hosted-build-NOTRUN actual-beforeAll-NOTRUN trivialboot-NOTRUN native-seed-NOTRUN selector-collection-NOTRUN original-body-NOTRUN`
- P3: `P3 D21 PREFLIGHT NOTREADY: App-selected-source-tree global-setup-NOTRUN actual-beforeAll-NOTRUN trivialboot-NOTRUN selector-collection-NOTRUN original-body-NOTRUN`

Native21/history, mounted readiness, Gate 5 body, original counts, and port/bodyguard observations are all NOTRUN. No PASS or journeyGO verdict.

## Identity qualification

- Requested selected App source: `66354161950d1e747965c095ea97b881d2592708`; tree `9a37265f0286128df7e6240a9df9877d959474af`; parent `b2380539c5545661954d2794976631312ee1d939`.
- Actual service caller snapshot: `d54582a08c6ad0453742523a3ec374dd321ce477`; tree `97b87a5bea5f8c9cbc699320260a3413e0f68701`; parent `66354161950d1e747965c095ea97b881d2592708`.
- Integrated synthetic identity: `9b810408ccf8aadbca708dd0bc461afc19576427`; tree `9a37265f0286128df7e6240a9df9877d959474af`; parents `b2380539c5545661954d2794976631312ee1d939`, `66354161950d1e747965c095ea97b881d2592708`.
- External metadata listed Agent `0b4255…`, Runtime `1d9dd…`, Composition `635f4d…`; these are metadata pins only, not actual daemon/provider identity.
- Retained custody remained exact: Agent `079580…`, tree `2deab1…`; Runtime `37eb6c…`, tree `be4114…`; child `0256`; Remotion `0258`.

The failure is correctly attributed to the actual caller snapshot being `d54582…`/tree `97b87a…`, not the selected `663541…`/tree `9a3726…`.

## Evidence inventory

P2 output root exists but is empty:

`/tmp/.../tests/app-P2-P3-source-rebind-0623-full-e2e-three-products-1024063415-20674/playwright-output/`

P2 retained `preflight/status`: 92 bytes, SHA256 `5b52b2c4a52335b6…`.

P3 produced no `playwright-output`, preflight, attachments, or worker subfolders.

Retained request/snapshot/log/summary files remain immutable. Full paths and hashes are in the service result directories above; no raw environment, auth, URL, wire body, or private trace data was exported.