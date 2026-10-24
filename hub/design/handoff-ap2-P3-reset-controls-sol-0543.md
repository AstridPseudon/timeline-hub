Completed the bounded P3 packet in the three authorized paths.

- Ported exact donor files, then added owner/refusal controls using the actual helper and real outbox records in offline IndexedDB.
- Proved the scheduling gap with the actual caller slice and `dragTimelineClip`: the donor had no response listener during `mouse.up()`. Registered the waiter before the exact 0→5 gesture, bound to its request identity.
- Preserved all five existing controls, the original reset, and every downstream assertion.
- No product, guard, fixture, P1/P2, timeout, or shared-dependency changes.

Actual base: `5f43d9e86a11dedf0484b60a111b5bc35b0af186`  
Base tree: `464333ff8be4c67abbb70d20229c0afcc0211e96`  
Donor: `e1b296b24ca1c9fb24f43a4331533c6dbca659e4`  
Donor tree: `d84238b69fa09b8a1c4e108c2365899456908dab`

All final checks exited **0**, using Node **v20.20.0**:

```text
/opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-reset-precondition.test.mjs
/opt/node20/bin/node --import tsx tests/e2e/local/support/gate5-reset-precondition.test.mjs
/opt/node20/bin/node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --list
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json
/opt/node20/bin/node node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.spec.ts tests/e2e/local/support/gate5-reset-precondition.ts tests/e2e/local/support/gate5-reset-precondition.test.mjs --max-warnings 0
git diff --check
```

The required Node test command passed; supplemental direct TAP showed **12/12 passing**. Playwright listed **15 tests**. Before the scheduling fix, the targeted timing control exited **1**, detecting zero registered response listeners during the drop.

Preservation passed: all **4,863 tracked paths outside the packet** match actualbase, including the merged P2 oracle. Reverse-removing only the import/setup reproduces the entire spec at `c0fe88994405fd517b58473c14678a0d1b73056d` byte-for-byte. No files deleted.

Full hashes:

```text
Spec base blob:
37caf28577d42fbe98afd2320dffa3c72e6e74b1
Spec donor blob:
c8b8494cfd148bb00f25725239d575a32aea61d1
Spec final blob:
9091d36fa38e961a9089e668beb456495e9338b8

Spec base SHA256:
0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14
Spec donor SHA256:
cac725a518e83b2bf4c9254dca869c136d6411bec3ac8b3c2e10339c9c58d488
Spec final SHA256:
741bcfb986fe0e80bbf81a40f741418991ed7e59cda59e578060b818e7d7cd94

Helper donor/final blob:
70164519544999cd6b910e62b0964d6d7e788970
Helper donor/final SHA256:
52b14c838ee05acd7d544fde35c5c760dd1d47bf7e38a066af7ead04e2af3d9b

Controls donor blob:
6386adabf57a6f9b9b2131a28ed000fcd3892fcd
Controls final blob:
ce3fcbe67a5f9199df4150c7471cbec8e4291428
Controls donor SHA256:
100aedb89efa0059f7edbc3c2dfd947efd56fb1bccab6da905055f2b1f558518
Controls final SHA256:
456489a94f83eba97e6d72a5d7a8c8d104f2c2116086a02b04c155631441a38f

Gate5 body base SHA256:
d3ead85a96a6fdf7dd76797bc75b24374e39ea640b632697603d16fc286c52ca
Gate5 body donor SHA256:
a555a6d7dd0f9d8518794d81c2ce9707411613cb83615a3df6253a30d6440a12
Gate5 body final SHA256:
c7735569a90ec9acdc2d66feed8747d3480c3b6d0e5acd3e22316ba84f9489e8

Required tail, unchanged across all three:
f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67
```

No blocker remains for this packet. The timing correction was justified by offline source-faithful evidence; no other decision changed. No browser/backend journey or full suite ran. **Actual 4065 remains NO-GO; no new browser success or journey GO is claimed.**

Commit message and `DONE` created. Next: independent final review, then the normal App merge queue; live qualification remains App-owned.