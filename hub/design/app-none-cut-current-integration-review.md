# D01 App transition-None current integration retirement review

## Decision

**APPROVE the qualified None/Remove cut for merge-forward.** The manager still
needs to apply the reviewed cut to current App integration `308ac52ad` (tree
`0725ccd2`) and perform the normal post-merge checks. This review does not
claim a browser pass on that current integration head, and it does not edit
the deletion ledger.

The qualified source is App commit `b14bfda0db43e1225394b3e6a7f60ab0dd48cd58`
(tree `c6e0d13cd7631b714a069790de9a930a554f8c03`), with Agent
`8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and the public13 Composition
tuple. Its central result is the exact committed TestID
`app-m2-none-wave2-committed-browser-gate-e2e-native-none-wave2-committed-b14bfda0-treec6e0d13c-agent8130-runtime2c4-public13-e2e-integration-1020172044-22648`:
**2/2 passed**. That result is evidence for `b14`/`c6e0d13c`, not for the
current integration head.

## Precise cut

- Single None/Remove captures through the scalar command session and submits
  `clip.set` v1 with `{ values: {}, clear: ['transition'] }`.
- Bulk None/Remove captures every selected target, finishes one atomic batch,
  and submits no partial batch.
- `PropertiesPanel` and `PropertiesPanelBody` provide the scalar capture
  ports. `ClipTransitionSection` and `BulkClipPanelBody` visibly refuse when
  those ports are absent; they do not call the old `onChange`/
  `onChangeDeep` transition-clear callbacks.
- Authored transition absence is preserved as absence. The qualified browser
  cases also prove opaque/unknown transition data, reload, inverse, lost-ACK
  restart retry, real 409 draft retention, and zero legacy traffic.
- Transition SET/type-change, duration, parameter, and reset handlers remain
  existing unsupported/legacy paths. They are not part of this bounded cut
  and remain open.

The source check found no overlap between the 35-path None delta
(`git diff 0d5009e18 b14bfda0d`) and the seven current-root paths introduced by
f301 label reconciliation plus reviewed42e carrier (`git diff 0d5009e18
308ac52ad`). The private composition of current HEAD plus the b14 delta
applied cleanly. The current changes are confined to the label projection /
save neighbors and `dataProvider.ts` / `mediaImport.test.ts`; no hunk needs a
semantic conflict decision.

## Focused verification on the reviewed current-root composition

Using a private13 source overlay (current HEAD plus the reviewed b14 delta),
the focused scalar/transition/generic/element/session/projection/label and
Inspector neighbors passed:

- Vitest: **32 files, 955 passed, 0 failed**.
- Native transition-clear contract plus launcher controls, with
  `node --experimental-vm-modules`: **2/2 passed**.
- `git diff --check 0d5009e18 b14bfda0d`: passed.

The overlay used the shared node_modules only through a read-only symlink and
redirected TMP/cache writes into the private overlay. No product source or
test was changed. No full suite, TSC, build, install, browser, localhost,
socket, or live service run was performed here.

## Exact ledger proposal (manager applies after merge-forward)

Replace the D01 row's status/evidence with the following wording:

```text
status: DELETED
commit: merge-forward of b14bfda0db43e1225394b3e6a7f60ab0dd48cd58
        (feat(app): merge qualified native None onto wave2 root) onto
        current App integration 308ac52ad; record the resulting integration
        commit SHA after the manager merge.
replacement tests: src/tools/video-editor/commands/clipScalarCapture.test.ts;
  src/tools/video-editor/commands/clipScalarGesture.test.ts;
  src/tools/video-editor/commands/commitSession.clipScalar.test.ts;
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx;
  src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx;
  tests/e2e/local/support/native-transition-clear.contract.test.mjs; and the
  two real `M2 native None` cases in
  tests/e2e/local/three-products.spec.ts (single and atomic bulk).
evidence: b14/tree c6e0d13c central committed browser gate 2/2 PASS
  (TestID 1020172044-22648), plus current-root merge-forward review with
  32 files/955 Vitest passes. This row covers only explicit None/Remove
  clear branches; transition SET/type/duration/parameter/reset remains open
  under the separate transition-writer retirement work.
```

Do not mark the row DELETED from the older `4054ea8f`/public13 candidate or
any older public12/root browser result. The cited `b14` gate is the required
qualified proof; the manager must carry that exact cut into current
integration before recording the status.

## Owner correction

The original None bug is **App-owned**, not Viewing/Composition-owned: the
loss occurred in App inspector callbacks and App `rowsToConfig`/partial
publication. Viewing and Composition consume the accepted authored result and
are not part of this deletion. Keep D01 transition-None under the App
manager; App2's bootstrap handoff does not change this ownership. The separate
transition SET/type/duration/parameter/reset writers remain open and must not
be folded into this row.
