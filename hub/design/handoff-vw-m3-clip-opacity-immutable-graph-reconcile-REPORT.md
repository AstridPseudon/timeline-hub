# App2 build28265 / public13 clipOpacity reconciliation

## Result

No source fix is justified. Public13 artifact SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
(58,477 bytes, version 0.0.13) is internally consistent and exports
`clipOpacity` from `/evaluation` only. Root `clipOpacity` is intentionally
undefined. The available installed graph is byte-identical to the artifact
across all 77 regular members.

App2 build28265 remains an unresolved environment/source-graph finding. Its
report records Rollup resolving an `evaluation.js` without `clipOpacity`, but
does not retain that file's realpath, hash, package version, or selected
artifact identity. The exact App2 source commit
`48576cfa2783331f2c7c8309ff4069162a3afd11` imports from
`@banodoco/timeline-composition/evaluation`, the artifact-defined supported
import. The prior root-import split was not repeated and is not valid.

## Installed graph comparison

Read-only installed package:

```text
package root: /home/user/work/app/node_modules/@banodoco/timeline-composition
package root realpath: /home/user/work/app/node_modules/@banodoco/timeline-composition
installed regular files: 77
artifact regular members: 77
names only installed: 0
names only artifact: 0
member bytes differing: 0
installed and tar manifest digest: fb5678e4db5a0d59589099641ed261739c56aace1cfbb8369ff583b39f4e2ccc
```

Exact hashes and realpaths:

| entry | realpath | SHA-256 |
| --- | --- | --- |
| `/evaluation` JS | `/home/user/work/app/node_modules/@banodoco/timeline-composition/dist/evaluation.js` | `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155` |
| root JS | `/home/user/work/app/node_modules/@banodoco/timeline-composition/dist/index.js` | `364460a558df5b0b9c6633113943f3414fd1c1873cb1357d01ecf7d279a41e52` |
| `/evaluation` declarations | `/home/user/work/app/node_modules/@banodoco/timeline-composition/dist/evaluation.d.ts` | `fb7226d0e817c15931593a1493646248a7de34bda1be3c80b615b6d02912d285` |
| root declarations | `/home/user/work/app/node_modules/@banodoco/timeline-composition/dist/index.d.ts` | `da76faee7226e65a18f91a2fb45e2a260f33aef8768609093872c7eff1a76e03` |
| package metadata | `/home/user/work/app/node_modules/@banodoco/timeline-composition/package.json` | `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61` |

`evaluation.d.ts` contains `export { clipOpacity } from './lib/clip-look.js'`;
`index.d.ts` has no `clipOpacity` export. Node `v22.22.0` probes resolved
the root to `dist/index.js` with `typeof clipOpacity === 'undefined'`, and
`/evaluation` to `dist/evaluation.js` with `typeof clipOpacity === 'function'`.
Direct import of that exact evaluation realpath also returned `function`.

The App2 private graph/source archive referenced by its locked-graph report is
no longer present at its recorded path. Thus this work cannot prove whether
28265 used a stale Composition directory, an alias/attachment bypass, or a
different cache/resolver state. It does not guess. For context only, the
known 0.0.8 evaluation hash is
`0ee058ca8657a6bbdbe8c127359297f856c5a7b1cb68258bd3bdc20846d98b96` and it
lacks `clipOpacity`; this is not attributed to 28265.

## Evidence and limits

```text
node --test config/vite/timelineCompositionPackage.test.mjs — PASS, 1 test
read-only 77-member comparison and export probes — PASS
```

No hosted build, broad test, browser, render, install, lock/pin/fallback/
graph mutation, or unchanged journey rerun was performed. The exact App2
Rollup file remains unverified; `PEERPACKET.md` is the minimal request for
that evidence.

