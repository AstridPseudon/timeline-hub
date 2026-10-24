# A2/A3 qualification report

Result: **bounded FAIL**. All requested caller evidence passed, but the exact 27-file union had one pre-existing failure.

Integration identity:

- Before: `c0fe88994405fd517b58473c14678a0d1b73056d`
  - tree `8e3ef15ee5f7c08381d8dc9efb38b5c98845466d`
  - parents `bad9a84fea2b1dddfb4f467e4108f28d3eadf2ff`, `19ac2b0ddcef00e1b2627aa1dd1e19c4bafb4b2f`
- After: `b2380539c5545661954d2794976631312ee1d939`
  - tree `eab53458e86b210b050673bdcd039d29b0a511ca`
  - parents `ae7acc1c2e1ae802b15110b9a7b099c77c9186da`, `172033a677472b0435498310babdbf1524b74bfd`

Protected donor final blobs matched the integrated members: **26/26**. Protected original D31/D37 blobs matched: **6/6**. No extra files were integrated.

Targeted Vitest command used Node 20, private preload/cache paths, `--configLoader runner`, `--no-cache`, `--maxWorkers=1` (Vitest requires the equals form), and the exact requested file union.

Result: **26 passed, 1 failed; 685 passed, 1 failed tests**.

Failure:

```text
src/tools/video-editor/commands/media.test.ts
prepared media command >
canonicalizes matching at_ms timing ...
```

The failure is `expect(result).not.toBeNull()`; this test is outside the A2/A3 donor fixes and was not weakened or modified.

Other checks:

- Gate-5 Node20 command: **12/12 passed**
- Serialized TypeScript checks for `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`: **all passed**
- Changed-file ESLint, `--max-warnings 0`: **passed**
- `git diff --check`: **passed**
- Protected schema/client/pin/D31/D37 census: **passed**
- Worktree remains clean.

Transport proof verified:

- Production route: `POST /v1/projects/{project}/timelines/{timeline}/commit`
- Production generated client forwards `Idempotency-Key`.
- C0 v2 request fields and `{data, receipt}` forwarding are retained.
- Parent path preserves original turn, raw opaque data, and closure.
- Popup path uses the mounted carrier and created-claim flow.
- Parameter path enforces strict genuine-owner binding.
- `am-burst` catalog path produces the exact POST and idempotency key through the production client/provider path.

The retained witnesses use fake transport or controlled Runtime replies; no live HTTP/service claim is made.

No product or test files were changed. Commit message and `DONE` marker were written. Recommended next step: isolate and qualify the unrelated `media.test.ts` `at_ms` canonicalization failure, then rerun the union.