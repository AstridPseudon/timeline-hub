# App M2 embedded shot-name MAIN574/public13 real gate

## Result

PASS for the bounded embedded parent-mounted shot-name path. This qualifies one
actual central Chromium case against the committed current-root candidate. It
does not close the whole shot-settings ledger row or claim global name-writer
retirement.

## Exact qualification tuple

| input | identity |
| --- | --- |
| App commit/tree | `0d8cb6a46b110686dbd224ea7595ac2d9b76c272` / `b5096cb688349930456d3ab34600a675100aac17` |
| Agent commit/tree | `8130a401bf44a518d5a40ae274d398b8c560be55` / `236c3e57e0265c52b81ba8085de3193026176bff` |
| Runtime commit/tree | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Runtime producer | `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, 75 artifacts |
| Composition public13 | archive `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular files |
| Public browser source | `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28` |
| Chromium | 141.0.7390.37, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95` |

## Central evidence

- Test ID: `app-m2-shot-name-main574-public13-real-gate-e2e-shot-name-main574-public13-committed-b509-agent8130-runtime2c4-1020172535-16386`
- Result: exit 0; one discovered and one passed browser test; 290 seconds total, 19.4 seconds product case.
- Test: `tests/e2e/local/shot-name-command.spec.ts:139`, selected only through `playwright.shot-name.config.ts`.
- Resolver guard: 9 tests passed. Source, public13 archive/package, peer, 75-artifact, cache, and paired checkout postflight guards passed.

The real case used the MAIN574 embedded `[data-shot-group-key]` shot label for
`F2 canonical shot`, not a Track-name input. It passed raw padded Unicode and
opaque payload preservation, accepted `shot.set` history dependency, reload and
real Undo/inverse, lost-ack Runtime restart/recovery with byte-identical key and
body and the same receipt, and a same-leaf Runtime `409` retaining the exact
draft. It also asserted no legacy composition-revision save traffic.

## Scope and limits

Only the embedded parent-mounted name path is qualified. Gallery/list,
standalone fallback, ordinary legacy, and separate settings writers remain
outside this gate. No global zero-legacy-writer or shot-settings-row deletion
claim is made.

No full suite, local browser/socket run, separate build, install, or project
TypeScript check was run. The central browser harness performed its normal
hosted bundle build as part of the actual case. A local wrapper preflight could
not invoke the frozen Chromium binary under sandbox policy (`EPERM`); this was
not counted as product evidence.
