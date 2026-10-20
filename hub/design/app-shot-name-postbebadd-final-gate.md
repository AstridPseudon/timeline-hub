# App M2 committed shot-name final gate

## Verdict

**APPROVE** the bounded committed embedded shot-name join on the exact assigned
source below. This approves the real embedded shot-name UI gate only. It does
not retire the whole shot-settings row, gallery/settings/fallback writers, or
claim a full App suite.

## Immutable source

- Assigned App commit: `9d9eb4b18c5526d9599131ac8e4fcf6be95707da`
- Assigned App tree: `2d5d7dba66e91f6306aa72a006abcdf4ea4bdd0b`
- Assigned parents: current `mainbebadd` `0d8cb6a46b110686dbd224ea7595ac2d9b76c272`, qualified `c57dcc26162642f503532f143ceb96bb185273aa`
- Central snapshot App tree: `2d5d7dba66e91f6306aa72a006abcdf4ea4bdd0b` (the service assigned synthetic snapshot HEAD `bb0b9650be52e0dce34e960a1bc25252836d28c1`; tree identity is the qualification identity)
- Agent: commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime: commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`
- Runtime producer: 75 artifacts, producer version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Composition public13 archive: SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 regular members
- Public source guard: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`
- Setup guard: `88888d44ddd375caacb7b45b74001b70428bf4404b76fe11c84a83f8b05a6cfa`
- Current013 source guard: `82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901`
- Composition resolver guard: `f49918bcfc3862f2ebad37d74ad0ae80a5535491949b2bfdbc8e4e4f19081881`
- Chromium 141 binary: `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`
- Strict runner SHA-256: `915afe4a5644667ba5fd31761c4ef650652d80f451bbbef4f175c89f79931c65`

The private13 dependency overlay was `/tmp/app-public13-pcm-complete-source-tsc-leaf13.01Xcjn/node_modules`; the runner isolated its temp, Playwright, npm, Vite, and XDG caches and checked shared/private cache identity before and after.

## Central evidence

Test ID:
`app-m2-shot-name-postbebadd-committed-final-gate-e2e-shot-name-postbebadd-committed-tree2d5d7dba-agent8130-runtime2c4-e2e-integration-1020175016-22598`

Result: **PASS**, exit 0, 306 seconds. The named suite was requested through
this worker name with `--no-cache`, never through `integration:app`.

- Source preflight and postflight passed; Runtime lock and producer-manifest checks passed.
- Public-source, package, peer, 75-artifact, 77-member archive, source-tree,
  and cache guards passed before and after.
- Composition resolver: 9 passed, 0 failed.
- Playwright discovery: exactly 1 test.
- Browser: 1 passed, 0 failed, `tests/e2e/local/shot-name-command.spec.ts:138`.
- The real case preserved raw padded Unicode/name and opaque data, verified
  reload and Undo, lost-ACK restart retry, byte-exact request/idempotency key
  and receipt/history dependency metadata, 409-kept-draft behavior, and zero
  legacy save traffic.

The joined source worker previously passed the proportional private13 native
None/scalar/Generic/Element/label/source controls (17 files, 370 tests), and
this worker reran the focused shot-name/session completion neighbors (4 files,
83 tests), all passing. No assertions were weakened or removed.

## Scope and limits

No tracked product edits were made by this qualification worker. No whole
shot-settings row retirement is claimed. No full suite, TypeScript check,
install, or local browser run was performed; the central runner necessarily
built its temporary hosted bundle for the browser gate and removed generated
`dist` during postflight. The prior full `integration:app` job is unrelated
and is not used as evidence for this verdict.
