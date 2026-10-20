# Reviewed fourcase + whole-tab App candidate

Status: TEST-ONLY integration candidate. **NEVER MERGE THIS COMPOSITE WHOLESALE.**

## Resolved source

- App base: `30b8df2895536c471e270faf83ce710acd847065`, tree `0bf9c9f7fb849cb0938bf29fc72eca069014f623`.
- Candidate in-memory tree after the harness commits: `0be6372fcd92744fe72d447e35a78d1dfab49d4d` (no commit or Git object was written by this worker).
- Public13 archive: 77 regular files, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; package/lock/tsconfig remained byte-identical to the base.
- Agent13 remains source-held: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`.
- Runtime13 remains source-held: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Composition13 source resolved to `af98594dce80c0350a1fc21dfc44839b2279edf1`; archive remains public13 above.

The App13 and Composition13 controller literals were rebound only after source freeze to the exact full identities above. `APP13.status` remains `pending-consumer-adoption`; no readiness grant, actor widening, normal Agent13 pin, or normal Render registration was fabricated.

## Exact composed deltas

Applied as immutable Git diffs, in order, with `git apply --check` before application:

1. Stored-occurrence cap unit: `4720a864c81dc7002a9e95dbacf10cec8df5da81^..4720a864c81dc7002a9e95dbacf10cec8df5da81` (22 paths), then the reviewed ES2020 corrections `1fe351b9847d35db66ab294a6edf631447fa78ce` and `93696b62f`.
2. Source-attributed native three-media fixture: `b1ef4b9b910ba72375c34cf319692f90d22edc25..e4c7a3792` (5 paths).
3. Player tab source and corrected guard: `b1ef4b9b910ba72375c34cf319692f90d22edc25..c60cef9470d0e02abc42c4850cdbd4d1112e7c76`, followed by `c60cef9470d0e02abc42c4850cdbd4d1112e7c76..247bfce2721e4fd0804faf8313b394e94157c2ee` (6 paths).

The final working tree has exactly 33 changed/untracked product/test paths: the 22 cap paths, 5 native-fixture paths, 6 tab paths. The only post-source-freeze content adjustment is the two controller tuple literals (`APP13` full App base SHA/tree and full Composition13 source SHA); all reviewed source blobs otherwise match their cited source commits. No old 320 render helper/product clone, other root/M1/writer delta, new fixture/framework, or duplicate DSP was included.

The original four parity cases remain in `cases.ts`, with the fifth capturing-before-warm tab case and the planted picture-only negative discovered separately. Existing MAIN17 Render/download/admission/codec/dimension/contract paths and strict RGB-2, audio-0.001, mute/half/boost, and negative controls were not changed by this composition. The controller still fails closed before capture because App13 adoption is pending.

## Evidence

All local runs used the private public13 leaf overlay `/tmp/vw-m3-reviewed-fourcase-leaf13.jfM2wu`, private cache/temp/output paths, and left the shared App `node_modules` unchanged and restored.

- Combined targeted Vitest: **10 files / 322 tests passed, exit 0**, 44.81s. This covered cap serialization/draft/persistence/projection/popup neighbors and PCM AudioTrack, audio failure, media conformance, contract, and lifetime neighbors.
- `node --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs`: **1 pass, exit 0**.
- `node --import tsx --test tests/e2e/timeline/viewing-parity/tab-audio.test.ts`: **1 pass, exit 0**.
- Native fixture neighbors with `node --import tsx --test`: **5 pass, exit 0** (`harness.test.ts`, `media.test.ts`, `canvas.test.ts`, `authority.test.ts`, `admission.test.ts`).
- Playwright discovery only: **exactly 5 tests in 1 file, exit 0**; no browser/global setup ran.
- Scoped Player TypeScript check: **exit 0**, `tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --types node` over `tab-audio.ts` and `tab-audio.test.ts`.
- Scoped ESLint over all 33 changed TS/TSX/MJS files: **exit 0**; Python AST parse, Node syntax checks, and `git diff --check`: **exit 0**.
- Public13 archive/extracted leaf audit: **77/77 byte-equal**; lock integrity and React 18.3.1 / Remotion peers 4.0.509 match the recorded tuple.
- `--ready` probe with `/home/user/work/agent` and `/home/user/work/runtime`: **exit 1 as required**, `App13 consumer adoption is pending; --ready remains refused`, before capture/grant checks.

## Held or unverified

- The literal Node20.19.4 executable expected by the approved guard is absent in this sandbox: `/tmp/vw-m3-agent-gate-node20.19.4/bin/node` (expected SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`). Do not substitute Node22 or guess a new SHA.
- Chrome155 was only hashed read-only: executable SHA-256 `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`, tree SHA-256 `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`, 255 files. It was not launched.
- No central actual acceptance, browser capture, Render/download execution, frame/audio/PCM parity, live socket, full suite, build, install, network, or owner-film qualification was run or claimed. Compilation of this cohort is not gate evidence.
- The manager must bind a fresh private graph, exact Node20/Chrome155/peer snapshots, matching App-first qualification, then issue a one-shot central request. Agent13 normal pin remains held until App-first qualification and normal Render registration.

## NEVER MERGE

This branch is a reviewed test-only cohort for the manager’s later actual qualification. Merge or promote individual reviewed units only under their separate owner gates; never request wholesale merge of this composed branch.
