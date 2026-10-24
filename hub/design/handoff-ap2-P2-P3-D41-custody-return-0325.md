## P2/P3 D41 custody correction

- Source/no-weakening: **PASS**. App `804134d…`, tree `8437e476…` unchanged; Agent `079580ca…` and Runtime `37eb6c7b…` match the producer handoff. No tracked edits.
- Primary outcomes remain separate **NO-GO**:
  - P2: exit 1, 501s; readiness passed, then 3 failures and 5 not run.
  - P3: exit 2, 147s; outbox read was `unknown` vs `verified`; Gate5 selected 1, executed 0 (**NOTRUN**).
- Direct custody: **PASS for P3 files only**. Exact sizes/hashes matched:
  - D21: 5,230 bytes, `09c8735d…b94df26`
  - Readiness: 652 bytes, `eea4457b…f84c9ce`
  - Bootstrap: 12,494 bytes, `679cc75e…8cee77b`
  - No P2 artifacts were claimed.

## New production controls

Command:

```sh
AUDIT_DIR=$(mktemp -d "$TMPDIR/d41-audit.XXXXXX"); export AUDIT_DIR
/opt/node20/bin/node --import tsx /tmp/w-d984202315/d41-audit.mjs
```

Exit: **0**

Passed:

- Genuine nested allowlist, enum, type, finite/bound, correlation, array/string, and security checks.
- `projectMountedDiagnosticDetail` idempotence for all 7 authentic mounted records.
- Real writer → file → `readJSON` roundtrips for all 3 applicable artifacts.
- Production paths exercised: mounted projector/bootstrap writer, D21 formatter/writer, and mounted-readiness `persistDiagnostics` writer.
- No raw token/URI/request/reply/header/credential data was emitted.

Additional checks:

- `git diff --check` — exit 0
- `git diff --quiet` — exit 0

This corrects 0320’s unsupported generic-profile claim: nested validation and production projector/writer evidence are now established, but the original P2/P3 failures and **NO-GO** outcomes are unchanged. Daemon/provider import metadata remains unknown; no journey GO is claimed.