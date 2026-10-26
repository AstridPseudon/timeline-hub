# Validation

Verdict: `PASS_EVIDENCE`.

Read-only source/path review. No product or test changes; no pytest, collection,
typecheck, lint, install, render, browser, child, request, CAS, service, full
suite, or manual integration was run by this worker.

Exact custody:

- assigned base `445b9c1a7f8d0e7e3405ad01f4475b9af02acfaf`, parent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, tree `6806fec5657f26097d0d0f3da29082907e6faadd`;
- current supported Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`;
- pristine `64197afa297f86f1e738238d5e80aff6d33e303a`, tree `6c0488b3efdfa47479b0ad1b7bd20608383be26e`;
- Runtime `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`.

Read-only checks passed: exact pristine blobs were inspected with `git show`;
the deletion commit `fc33e0e76ca1c29cb64f574acdab6770eb3303d0` was inspected;
production `plan_inverse`/`plan_inverses` caller search found none; current
`timeline.inverse` caller/source map is recorded in `source-manifest.json`.

Evidence JSON checks passed:

```text
python3 -m json.tool evidence/per-id.json
python3 -m json.tool evidence/source-manifest.json
per-id cases=38, unique=38; manifest IDs=38, unique=38; sets equal=true
```

The retained reviewer evidence is supporting context only: source restoration
PASS, targeted behavior FAIL (15 failures and 40 collection errors); no raw
private XML is claimed. No behavior PASS, REG0, ship, or retirement is claimed.

The required disk trace is the absolute `disk-trace.txt` in this evidence root;
it has six fresh samples over five seconds, all above 4,000,000,000 bytes.

No `report.md` was written because D30 requires the final worker message to be
the report and forbids workers from writing `report.md` themselves.
