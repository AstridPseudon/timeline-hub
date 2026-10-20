# AP2 M2 selected fallback assertion conversion

## Result

Converted the one selected-pack fallback `it.fails` from source commit
`251f3a5b6f83b0d12b0863d3e602b10fc1d12d2e` into active behavior coverage.
Only `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx`
changed.

The selected-pack path now has two active outcomes covered by the existing
tests:

1. Missing native carrier: the authored edit `selectedSegmentIndex: 2 -> 1`
   visibly refuses, keeps the dirty input at `"1"`, reports the retained-read
   requirement, and calls neither the legacy `onChange` fallback nor the
   element capture/finish/submit path.
2. Existing native carrier: the same `selectedSegmentIndex: 2 -> 1` edit,
   with opaque `futureParam: "keep-me"` retained, finishes and submits the
   native `clip.set-params` command with the exact values, empty clear list,
   original schema pin, and no legacy `onChange` call.

The mounted production-carrier tests were left unchanged. They continue to
cover the P1/P2 selected authority provenance, opaque retained source/object
inputs, authority/basis guards, async retained-read disposal, and no-commit
after unmount. No shared ports or Viewing files were touched.

## Deletion-ledger proposed conversion map

This is a test-expectation conversion under D01 (App fallback writers); the
manager-owned ledger was not edited by this code-only worker.

| Old source assertion in `251f3a5b6` | Active replacement | Preserved meaning |
|---|---|---|
| `expect(capture).not.toHaveBeenCalled();` in `it.fails('keeps selected-pack edits on the existing producer without native capture')` | `it('refuses selected-pack edits without a native carrier while preserving the dirty draft')`: same assertion, plus `finish`/`submit`/`onChange` zero-call checks, retained input value, and visible carrier error | No selected-pack edit falls through to a writer when the native carrier is absent |
| `expect(onChange).toHaveBeenLastCalledWith({ params: { selectedSegmentIndex: 1 } });` | `it('preserves existing params and writes through the selected native producer')`: `port.finish` receives `{ values: { selectedSegmentIndex: 1, futureParam: 'keep-me' }, clear: [], schema_source }`, and `port.submit` receives the exact command with `preview: null`; `onChange` remains unused | The authored intent/parameter change succeeds through the existing native carrier while opaque data survives |

No assertion was skipped, deleted, weakened, xfailed, or converted to a new
expected failure. The App-wide `it.fails` inventory remains exactly the three
original drag exceptions in `useClipDrag.test.tsx`.

## Verification

All commands ran in
`/home/user/work/wt/ap2-m2-selected-fallback-assertion-conversion`:

```sh
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/clipParamsCapture.test.ts \
  src/tools/video-editor/commands/selectedParamPort.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

PASS — 6 files, 71 tests passed, 0 expected failures.

```sh
./node_modules/.bin/eslint --no-cache --max-warnings 0 \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx
```

PASS.

```sh
./node_modules/.bin/tsc --noEmit --pretty false
```

PASS.

```sh
git diff --check
```

PASS.

No browser, localhost/live socket, `request-test`, full suite, pin/adoption,
or build gate was run, per task limits. The central selected P1 DEV journey
therefore remains unverified here.

## Next step

Independent review can inspect the one-file diff and the conversion map above;
the selected P1 DEV journey can be run by the orchestrator when its central
gate is authorized.
