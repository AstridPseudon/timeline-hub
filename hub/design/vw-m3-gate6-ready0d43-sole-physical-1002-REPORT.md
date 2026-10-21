# vw-m3-gate6-ready0d43-sole-physical-1002

## Final result

Central preflight passed once. The authorized single physical request then failed in case 1 and was explicitly stopped; cases 2-5 did not execute. No parity result was produced, and no product files were changed.

Failure: the frozen generic pack host reported that it could not resolve ../../astrid/packs/rendering/editor/live-scenes/SceneSurface while executing the real App Render action. This is an infrastructure/source-resolution failure before valid export, not a parity mismatch.

## Tuple and identity

App pin 0d4323913b92c4e0e3830bf14ec7f35d981475ca, tree 5a1e0e85d0f336f642426b91ccf3b3f1984ebd14; App HOME HEAD f60a47389ec71c98526eff0843ee0c0644f9a63a, with pin verified as ancestor.

Agent d0a5072bbe7b7ce9489f43aa0a81027ec400343b, tree 6adb4a1190dfb2874e101565f37eccd392b1ae2f. Runtime 8f105c26e3b62f9c2683f717a9773a12bc775a8e, tree b7f456d5135cba6049980ebc43a91c7a72ab8f7e. Composition 5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8, tree 13e375534fffd704305eced5686699d2c8c9c948.

App source: 5902 files, SHA-256 4fb1e53b2dce325f826b6b071d0782544e5ba2c7b27418b6170f8c947c450435. App graph: 8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b / 32393. Runtime graph: 4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c / 21455. d00 dist: 339 files, index aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b. Public13 archive 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738. Runtime producer 2c4ac180c2220bdad966bc01e95ad230e99ce26a, tree 7ab412cc4bcbe517efcfa806e092336390312e18, 75 artifacts. Node 20.19.4 hash 43d6...99490; Chrome 155; helper b70+bc75.

## Central IDs

- Preflight: vw-m3-gate6-ready0d43-sole-physical-1002-e2e-viewing-gate6-ready0d43-sole-physical-1002-preflight-1021100413-23857 — PASS, exit 0.
- Physical: vw-m3-gate6-ready0d43-sole-physical-1002-e2e-viewing-gate6-ready0d43-sole-physical-1002-physical-1021100528-15923 — cancelled after explicit first-failure stop, final exit 130. No retry.

The physical namespace is /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-ready0d43-sole-physical-1002/packet/gate6-20261021T1002. Raw evidence remains there.

First-case raw hashes: error-context.md dbb49fd6fdcbcb579aff1b664381e182da531d87585cf8188b2e62e03d6173b5; page-diagnostics.json 91e99ec5d0e453832da3bc8323dff9b9781b289cc338ace4c8448e1b97848ecb; trace.zip 60e7302defa6fe012af2ef76efbb2b0fe98af8c43aa80ff62d731a7517ab07dc. Central/invocation log b1249bf75db3aa47a9392139b9aeebd596e6c84d64e3b8868fe41714ad01fa8b. source-tuple.json e5fdb984701b9becd1c1192793075a56a4f3c6fe7aec0e82bcd5b4eeed41df85. Grant 9195360c316eda34f69065cad2b189634d25c441290551ceed232d4a0466c14f. Marker f453036618027b94b92ff15206dd8ddd9beaf12f97a3c9df3f74ebeffb9025fb.

## Case counts

Exactly five names were discovered/listed. Body count: 1 executed, 1 failed, 4 not executed.

1. cases.ts:229 normal App Render action downloads a valid native-size MP4 without a parity comparison — FAIL; expected output path viewing-parity/final-export.mp4, but no valid MP4.
2. cases.ts:246 fixture readiness seeks actual managed Player video and captures native frames without export — NOT EXECUTED.
3. cases.ts:267 compares native-size actual Player frames with decoded real CPU Remotion task output — NOT EXECUTED.
4. cases.ts:277 captures the actual Player page as one native-PTS VP8/Opus tab stream without a physical-mix claim — NOT EXECUTED.
5. cases.ts:317 picture-only one-host patch is reported as a mismatch after the full passing baseline — NOT EXECUTED.

Normal CPU frame, PCM, picture-only, and half-gain outcomes are unverified. The physical run did not reach any comparison body.

## Next step

Investigate the SceneSurface resolution failure and obtain a new explicit immutable grant/tuple before another physical run. The consumed one-shot packet must not be replayed.

