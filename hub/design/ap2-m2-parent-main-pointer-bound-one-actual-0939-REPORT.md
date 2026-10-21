# AP2-M2 parent main-pointer bound one actual 0939

## Result

The approved parent template was bound by data-only substitutions to the final
fixture-only App source, and exactly one central `--no-cache` actual was
submitted. The actual reached the browser and collected exactly one test, but
failed before the mounted ADD body began.

Run ID:

`ap2-m2-parent-main-pointer-bound-one-actual-0939-ap2-m2-parent-main-pointer-bound-one-actual-0939-integration-actual-1021094133-32624`

First retained cause:

```text
Error: Timeline file drop at 22.5s is outside the mounted timeline viewport
at tests/e2e/local/support/app.ts:235
called by tests/e2e/local/three-products.spec.ts:1473
```

This is a new viewport boundary after the previously diagnosed centered-pointer
cause. The final source correctly uses `22.5` for Main's centered five-second
drop semantics, but the actual mounted viewport did not contain that pointer.
No retry, fixture normalization, selector change, assertion change, or writer
cut was made.

## Bound source and custody

- App source: `/home/user/work/wt/app-pin-7419eccb`
- HEAD: `7419eccbbbaaed09d520845366255a9a87af5679`
- tree: `971e8ff779a2e6d3df651a30d37bb8bc7e285a83`
- spec blob: `49d406d76608dde1d6b94df2c4038e5d3c8e5ba4`
- source status: clean; KEEP marker and canonical ignored symlink were present
- `node_modules -> /home/user/work/app/node_modules` (identity checked; no install/copy)
- source ancestry from 0930: passed
- public Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`
- public Runtime/producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- locked public13 graph: Node `v22.22.0`, Vite `5.4.21`, Playwright `1.60.0`
- embedded Composition archive member count: `77`; Runtime artifact manifest: `76`

The helper reverse proof required the prior helper hash
`96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109` and
exactly one prior `final95:parent` pair (`8eb4d08e` / `ea317333`). Only those
two helper identity lines changed to the final HEAD/tree. Other profiles,
roles, pins, and guards were reverse-proven unchanged.

Bound artifact hashes:

```text
gate   80f1b52230115134c58f2ae0d7e11394f9628b855f2083b743caccebc9eb39c9
helper e081b0736e5c9341044d24cbda4f727dbf89f85b6300f8ec9e544c11dcd5992c
driver 0c310d9e906dfbfab8202dd0f17edca9509ad8239150c50eb5a48cabfb478a0c
runner 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
```

Registration was generated from file bytes, validated as lowercase 64-hex,
read back byte-for-byte, and registered once in the central suite allow-list.
The fresh packet is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-main-pointer-bound-one-actual-0939/record/evidence-final95-parent-7419eccb/run/`

Packet hashes:

```text
bounded-browser-evidence.json 2327ed635edd4152b120665d18ca08fec10205675e5b676a3d88efced35ac2fb
error-context.md              196f01aaa5fe2596dcc65111e3ab8171135e906e1df3e88ee2cc16ac47aee45c
evidence-presence.json        0ab19165d6ac03ac502930a7e33b5f6cfda679e7b450e33b0f75b477b689374b
playwright-trace.zip          b9f206316dbdb01191c3057fced6c7411bef63809472159d70a1902781ca9a04
result.txt                    6afccb5b43a157a7f5bc8cdb2dce50e3f6c196db3420f6082169f13ce1775ae9
retention.log                c5410c8014ec39b4476d5918a05d6f147fda9a0cba263817dfc21553ab8f6149
runner-tail.log              b8a9ea69c644b1d926307cd7dfbbddca88ebdbf29b225bfc5672280d7b6b3764
source-identity.txt          9e855f05617b395c6eb2331c940c068cc873ba0bba099425769e38e3d4ff1e9c
central-run.log              3433b69343fd06d5bcc30ece0c8d43593be9af24944087aa829b0d164b8e232b
central-summary.txt          20d1520a1a2fe0520d6a453354a3c9e027f4d378849196273137b7afb659cf51
```

The earlier 31285 and 25174 packets remain untouched. The 31285 before/after
hash lists still compare equal.

## Preflight and test evidence

The aggregate cheap preflight passed. It covered source/ancestry/spec and
original assertions, 76/77 artifact counts, actual Node/Vite/Playwright graph,
exact argv/config and one-test list (`three-products.spec.ts:1410`, title
unchanged), zero-test/retention controls, physical short roots, source/helper/
driver hashes, nonblocking browser lock, 10 GiB disk floor, one normal copy,
credentials-file check, and no active selected/parent/producer body.

Commands and results:

- `env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh record/final-keeper-gate.sh preflight` — PASS.
- `sh record/run-parent-manual-drop-evidence.sh probe` — PASS; zero-test refusal and evidence-before-cleanup control.
- Aggregate offline identity/assertion/graph/resource preflight — PASS.
- `request-test ap2-m2-parent-main-pointer-bound-one-actual-0939 ap2-m2-parent-main-pointer-bound-one-actual-0939-integration-actual --no-cache` — exactly one request.
- `wait-test ...32624` — FAIL, exit 1 in 84s; one test collected/executed, first failure at the viewport guard above.

Not reached: strict 404 response-body assertion, valid import/selection/verified
assertions in the mounted drop body, native `clip.add-media` request, lost-ACK
retry, restart/recovery, undo, and zero-legacy assertions. Therefore this is
not a product PASS and the original success/retry/restart/undo/zeroLegacy
qualification remains open.

No local browser, socket, install, build, full suite, or second actual was run.

## Recommended next step

The App manager should diagnose the mounted viewport geometry at the existing
`dropFileOnTimeline` guard and reconcile it with the approved centered-pointer
semantics. Preserve the `22.5`/left-edge-20 requirement and the strict original
assertions; do not retry this packet or relax the viewport guard without a
smallest-cause decision and a fresh bound source.
