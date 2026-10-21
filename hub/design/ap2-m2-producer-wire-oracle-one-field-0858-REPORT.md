# Producer native-wire oracle correction — 0858

## Result

Changed exactly one observed command-wire assertion in
`tests/e2e/local/producer-ownership-current-pin.spec.ts:163`:

```diff
- args: { at: 1 }
+ args: { on: 1 }
```

This is the one-to-one correction from the old incorrect native-wire spelling
`clip.move.args.at` to the exact native wire field `clip.move.args.on`. No
assertion was deleted, broadened, or replaced with a looser object match. The
command set (`clip.move`, `clip.set`), exact selector, `values: { hold: 5 }`,
`clear: []`, marker count `2`, protected foreign/user records, lost-ACK exact
body/key retry, reload, authored readback, and undo assertions remain
untouched. The existing spec/support pair contains no separate zero-legacy
assertion; no such coverage was added or removed.

## Source and hashes

- Base App HEAD: `3c2dac2a75ad9790bd9a85c82d20b149ec21fc8c`; base test blob:
  `9b1ce700eb6bcd6212aac246365781ef1b1beaf9`.
- Resulting test blob: `76495a3132cf4763609125a5eb25e35f0f1dd6da`.
- App lowering source: `src/tools/video-editor/dev/scene-phase-markers/extension.ts`
  blob `947dd512269974f0114eaa406c7345902326b8d6`, lines `722–731`.
- Frozen Agent pin `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`, schema
  `astrid/core/timeline/schema/edit-command.schema.json`, blob
  `11ff4399dfa4830f3f6177a5124475d970600da5`.
- Frozen Runtime pin `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`, schema
  `contract/schemas/edit-command.json`, the same blob
  `11ff4399dfa4830f3f6177a5124475d970600da5`.

## Frozen proof

Both frozen schemas define `ClipMoveArgs` at lines `399–411`: the only
property is numeric `on`, it is required, and additional properties are
forbidden. The same schemas identify `clip.move` at line `998`. The static
wire-fit0812 report records the same pinned result: App scene intent is
`{at: 1}`, native capture is `clip.move` with `{on: 1}`, followed by the
native hold `clip.set` with `{values: {hold: 5}, clear: []}`.

The App operation builder at
`src/tools/video-editor/dev/scene-phase-markers/extension.ts:722–731` emits
the authored same-track patch payload `{ at: alignment.time }` as `clip.move`.
That is the intentional App intent/readback spelling; the observed POST
oracle must assert the provider/native lowering spelling `{ on: 1 }`.

## Verification

- `./node_modules/.bin/eslint tests/e2e/local/producer-ownership-current-pin.spec.ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `git diff --check` — PASS.
- Diff is one file, one line changed (`1 insertion, 1 deletion`).
- Browser, build, actual producer run, full suite, install, socket/service, and
  central test service were not run, per the task boundary.

Direct-neighbour review found no other deterministic oracle mismatch requiring
an edit. The authored row readback remains `{at: 1, hold: 5}` at line 179;
the exact retry body/key remains asserted at lines 170–171; protected-row and
undo assertions remain unchanged.
