**FULLFINALREADY for the exact P1 caller.** Updated only `app/ap2-P1-chain-h6` in `tests/suites.conf`. Worktree remains clean; commit message and `DONE` written. No service request submitted.

| Binding | Value |
|---|---|
| Source | `f8b15af0a66ed14e7711a4bb7f1ed5b62b4988b5` |
| Tree | `dde63bed393f716033baaa3512cd5be379a095c1` |
| Parents | `d698c28ae0aad93d0213c12677f737521f8d2e65 756caeaa8d40443b87baf745585361153e8e49e0` |
| Published row SHA256 | `cda895d6568f02e6a24093b24439caab86e15c408f903d079e8f6661dc0fe731` |
| Outside-row SHA256 | `1c29219345caf5d0e555fe11056889b18ad89e407f63fbcbe958be989561ef74` |
| P1 spec blob | `5a2029d5f61a5cb665e1fb59c9fe13c9fff0bfde` |
| Spec SHA256 | `50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17` |
| First leaf SHA256 | `eecdb2b41f66ecfe16a3d564f701c3138e39dd214b473c98635c6f7da51cbd72` |
| Second leaf SHA256 | `4d614d4c8f01e5a53abfa34ff3dd4b59f7dd63908c5d62028158834fcf3eb075` |
| Unchanged Gate-5 blob | `37caf28577d42fbe98afd2320dffa3c72e6e74b1` |

Added exact guards for the six reviewed projection blobs and four bootstrap blobs, a 40-hex snapshot-ID check, and exported `REAL_ID` before stages/body. Preserved all original guards, receipts, private graph, stage commands and complete final invocation tail.

Reviewed blob guards:

```text
preparedImageRequestProducer.test.ts  0e585667a85c170494f958c5d36fed9c4ce700b9
preparedImageRequestProducer.ts       8f686e3e3be448995eae1c43a9e86d1dee217aeb
timelineLocalSaveHandoff.ts           e069b23b3a2f678d13f78a3733a0a40783ca762d
useTimelineSave.test.tsx              90ddf77ee519b8dea4c1be3b024ea6e2b49dae16
timeline-data.ts                      597ae62e1151f8bfc6fede3009ea27f960baebaf
timeline-domain.ts                    e42c3bcc836ba7b2ebe6baed3f0789c85c6820d6
mounted-readiness-safety.test.ts       286b693c6f69ac835d493d5c43b34f225ae29cc1
mounted-readiness-safety.ts            c1ba1c00045f7530299f91cc14301c98ca2d298f
support/app.ts                       1099534016d4951389ff00238399f21870670df0
three-products.mounted-readiness.spec.ts
                                     ba85a25085b61bd2e8e3960ab0260a91c6f9650a
```

Validation commands and results:

```bash
bash -n "$TMPDIR/inner.sh"
bash -n "$TMPDIR/outer.sh"
python "$TMPDIR/qualify.py"
python "$TMPDIR/audit.py"
python "$TMPDIR/publish.py"
git diff --check
```

**PASS:** 22 actual caller controls; real argc2/`-c`/payload identity; full real static prefix; exact-source and synthetic single-parent positives; genuine export/eval and all carriers. Wrong source/tree/parent/multiparent/source-parent/dirty/body/receipt/graph/39-hex controls stopped before stages. Capture17 and parse failures executed zero stages. Success stubs executed seven boundaries once, in order, with five durable logs; stage failures stopped subsequent execution. Native21 and diagnostic38/2/32 preserved.

```bash
NODE_OPTIONS="--require=$TMPDIR/vitest-dirname.cjs" node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mjs" --configLoader runner --no-cache --maxWorkers 1 \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/video-editor/commands/localSaveSession.test.ts \
  src/tools/video-editor/commands/localSaveSession.v2.test.ts
```

**PASS: 188 tests, nine files**, private cache and runner configuration.

```bash
node --import tsx tests/e2e/local/mounted-readiness-safety.test.ts
node --import tsx tests/e2e/local/d21-environment.test.ts
```

**PASS: 12/12 and 7/7.**

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c 'node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json'

node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/lib/timeline-data.ts \
  src/tools/video-editor/lib/timeline-domain.ts \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.ts \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts \
  --max-warnings 0
```

**PASS:** Root/App/Node types and scoped lint. Original `npm run test:e2e:three-products -- --list tests/e2e/local/three-products.p1-chain.spec.ts` collected exactly **two selectors**, using the pinned Node20 toolchain.

**Separate integration finding:** `node --import tsx tests/e2e/local/p1-diagnostic-safety.test.ts` produced **19 passed, 2 failed**. Both failures are `unexpected module: ../mounted-readiness-safety.ts` in existing controlled module loaders. Left unchanged under the row-only scope; this is not an all-green integrated-test claim.

Atomic publication preserved every outside-row byte, including P2 and P3/37340. Their SHA256s remain:

```text
P2 full-e2e-three-products:
ada633470c9204e6e1f1d9318d557a41bc05a070541f934f0f0cff7c5ffbc731
P3 ap2-P3-gate5-h6-0348:
0d73e0f6f88db6010dcdbd06b0567f6ac40539e1a1c4087ba0d26946ebe641ba
```

**NOTRUN:** actual build/native/setup/readiness/browser/backend/HTTP/full/service/provision/dispatcher; no product-recovery or provider-acceptance credit claimed.

Manager next: submit **one** `request-test app-P1-reviewed-leaves-caller-sol-0013 ap2-P1-chain-h6 --no-cache`, then wait on that same returned ID. Track the two diagnostic loader failures separately.