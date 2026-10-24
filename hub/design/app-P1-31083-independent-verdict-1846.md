## Verdict: PASS

Independent same-ID verdict for current P1 tuple:

- Preflight `app-pin-83025232-d73-p1-current-1840-preflight-1024183849-11421`: PASS, exit 0, 2s.
- Normal `app-pin-83025232-d73-p1-current-1840-1024183919-31083`: PASS, exit 0, 192s.
- Readiness XML: 1 test, 0 failures/skips/errors.
- Original P1 XML: 2 tests, 0 failures/skips/errors.
- Behaviors covered: accepted split, merged trim after Agent edit, lost ACK/restart/exact retry, and stale Agent move refusal with rollback.
- Historical `26312` remains reference-only; P3 is independent and is not gated by this review.

Pinned source identities and trees matched the retained manifest:

- App `830252327fc37b9c68fb7fa9e3d09ad560624fb8` → `0161cc1662f0b624efdd9ef46f48cbc941297540`
- Agent `263696c832220eebd79804a74f78c57734ad7bd7` → `0168aa36a6e4cb234aa6b1c587e0fcabe99c1014`
- Runtime `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f` → `4feab0185b3750a55b8f0c21c92c6015aaf8e2f7`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` → `5ab5191a296980a0a6bcd1178ab6902d6478a148`

All six protected source hashes matched, and the P1/readiness hashes were unchanged before and after execution. The current caller is the same `scripts/testing/d66-plain-stack.mjs p1` entrypoint and selectors; its current implementation includes D73 pin/preflight additions, so byte-identical caller implementation is not claimed.

Captured versions: Node 20.19.4, npm 10.8.2, Runtime `AstridRuntime/0.1 Python/3.13.16`, protocol `workspace.v1`, schema digest `sha256:867f3553…`, provider `astrid-v1`, compiler `authoring-bundle-1`.

App and Agent homes advanced after capture; Runtime and Composition still match. The pinned manifest/service snapshot remains authoritative, so this does not invalidate the D73 tuple. No transport metadata was used to infer source cause.

Checks:

- Retained manifest JSON and XML parsed successfully.
- Pinned tree/hash verification passed.
- `git diff --check` passed.
- Worktree remains clean.
- No product, test, generated, pin, collector, or private-body changes.
- No full or duplicate suite run.

The final response is the report; the harness should materialize `report.md` and publish the requested `ORCH/design/app-P1-31083-independent-verdict-1846.md` byte-exactly. `DONE` and commit message `test(timeline): certify current P1 control verdict` were created.