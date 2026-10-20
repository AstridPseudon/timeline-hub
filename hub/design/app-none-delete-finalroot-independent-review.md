# App M2 D01 final-root independent review

Review is against `b1ef4b9b910ba72375c34cf319692f90d22edc25`, tree
`8d8a10b057ed31fed69517e18a23b8ec3811447a`.

The integration current root was clean at `41fff23a29f13bd9aede6343592ffba8adebe1a3`.
Neither candidate changes the Main17/cold4 root paths, the original seven
three-products journeys, or the grouped-delete case 261. Both candidate
worktrees were clean. The requested `scratchpad/luna/reports/` directory was
absent; I reviewed the available candidate reports under
`scratchpad/orch/design/`.

## Verdicts

### Native None — APPROVE (source candidate only)

Reviewed commit `b22ab12b6babed85eb41396d5cc5eaa5becad70f`, tree
`61527d4e10e2ffe141de0c9ac2026357935bb9d4`.

The source shape is ready for the real harness. Both production Properties
Panel entry points supply the scalar capture port for single and bulk
transition clearing. The native command uses `clear: ['transition']`, captures
before finish, submits one original-basis batch for bulk, and visibly refuses
on capture/submit failure without a snapshot fallback. The parent golden is
exactly the d874 shape, including read guards and bindings: `parent/clip:*`
has only `scalar.target`; occurrence targets receive the real `scalar.owner`
binding. No made-up parent owner is present.

The source assertions cover raw absence in both parent mirrors, full
source/mirror/registry payload preservation, opaque/null/ordered/prototype-
shaped values, immutable child closure, exact outbox/original request bytes
and retry identity, inverse restoration, and the real same-property guarded
conflict draft. The recorded
worker evidence is 213 core Vitest passes, 485 neighbor passes, 76
preservation-neighbor passes, 12 integration-launcher checks, 6 native-None
launcher checks, 2 strict binding checks, scoped ESLint, vendor-lock, and
known-failure checks all passing.

The candidate report names working-tree tree `26ffc29bce7f147c546530c6728bb61d70691092`,
but the actual clean branch and reviewed commit resolve to `61527d4e10e2ffe141de0c9ac2026357935bb9d4`.
Freeze and pass the actual final harness SHA/tree to the central runner; do not
use `26ffc…` as the identity.

For the eventual row-`DELETED` decision, remove the transition-removal
fallbacks in `ClipTransitionSection` and `BulkClipPanelBody` (`onChange` /
`onChangeDeep`) only after the capture-port invariant is proven at every
production callsite. This retires the None transition writer only. Standalone
controls whose port is omitted still count as remaining legacy writers, and
the ShotTimelinePreview/`shotTimelineDataProvider` popup path plus unrelated
placement/group writers remain outside this row. The safety route is not full
writer retirement.

### Parent delete — APPROVE (source candidate only)

Reviewed commit `4a782eb03caba7e4df1225f054d8091911354848`, tree
`530019d089acc3cdb36f3624bcfa98dcd9726df9`.

The parent-only slice is truthful. Native capture is mounted for one ordinary
parent row and has no fallback after capture/submit failure. Parent and config
mirrors delete only the selected row; source/mirror/registry/opaque payload,
occurrence data, child closure, manifest, and original bytes are retained by
the exact full-payload assertions. The native S2 contract has the complete
whole-row/collection reads, three membership selections, occurrence-only
`collection.owner:collection.clips` binding, and empty `created`; there is no
invented parent-owner binding. The added conflict journey holds the real App
delete, performs a real Agent same-property move, and requires a real 409 with
the original intent/request/guards retained. Group, multi-clip, occurrence,
and prepared-media unsupported paths remain unchanged; case 261 remains.

The recorded worker evidence is 116 narrow Vitest passes, 7 launcher checks,
15 integration-launcher checks, two parent-delete Playwright tests collected,
the original seven tests collected, scoped ESLint, and `git diff --check`
passing. This is source evidence only.

## Read-only checks performed

```sh
git show -s --format='%H %T %P %s' b1ef4b9b910ba72375c34cf319692f90d22edc25 b22ab12b6babed85eb41396d5cc5eaa5becad70f 4a782eb03caba7e4df1225f054d8091911354848
git diff --check b1ef4b9b910ba72375c34cf319692f90d22edc25 b22ab12b6babed85eb41396d5cc5eaa5becad70f
git diff --check b1ef4b9b910ba72375c34cf319692f90d22edc25 4a782eb03caba7e4df1225f054d8091911354848
git diff --name-only b1ef4b9b910ba72375c34cf319692f90d22edc25 b22ab12b6babed85eb41396d5cc5eaa5becad70f
git diff --name-only b1ef4b9b910ba72375c34cf319692f90d22edc25 4a782eb03caba7e4df1225f054d8091911354848
git grep -n -E 'astridAppendService|SupabaseDataProvider|AstridBridgeDataProvider' b22ab12b6babed85eb41396d5cc5eaa5becad70f -- src ':!tests'
git grep -n -E 'astridAppendService|SupabaseDataProvider|AstridBridgeDataProvider' 4a782eb03caba7e4df1225f054d8091911354848 -- src ':!tests'
```

The diff checks passed; the provider searches returned no matches in candidate
production source. I did not run Vitest, browser,
localhost/socket, full-suite, build, TypeScript, install, or central harness
execution, per the review brief. No qualification, publication, ledger
deletion, merge, or writer-retirement claim is made.

## Required next steps / remaining cuts

1. Freeze each exact final App tree and harness SHA, then run the corresponding
   private-dependency central browser lane with Agent d874
   (`d8749a9ce12a699672faf3ad96b4e4cbea9245c2`), Runtime
   `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and Composition 0.0.12.
2. Require the actual browser journeys to prove publication, restart/reload,
   exact retry, inverse, same-property 409 retention, raw-byte preservation,
   and zero legacy traffic before any qualification or row deletion.
3. After the None gate, delete only its identified transition-removal fallback
   branch; separately inventory and migrate the popup/standalone and other
   legacy writers. After the parent-delete gate, do not expand the native
   claim to unsupported group/occurrence/multi-row operations.
