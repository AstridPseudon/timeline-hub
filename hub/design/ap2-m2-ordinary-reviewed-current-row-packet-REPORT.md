# AP2-M2 ordinary reviewed current row packet

## Result

Prepared the smallest reviewed source/test packet for the ordinary Scene Phase
Markers row on the latest HOME App base. The current source did not already
contain either reviewed delta, so this is not a no-op.

The packet ports the approved producer fix from `17655a570` and the approved
five-member membership correction from `9e59cb69`. It preserves the existing
causal retry, restart, undo, opaque-data, zero-legacy, and negative/refusal
assertions. No `useTimelineOps` or other shared-core/App-owned adapter source
was edited.

## Exact base and source hashes

- Current base commit: `ad1b0961a315b1ba4357768f0fe72d427ecdea49`
- Current base tree: `8937b417e948d4c4e3ab67ac089ee4f6055120cd`
- Uncommitted worktree diff SHA-256: `a91c24673aa48e603efeb191bc5ca474746772d00da9ba592a52cc83f7c15a47`
- `src/tools/video-editor/dev/scene-phase-markers/extension.ts`: `477ec52f4da4b5944033959b1a18035972b9c4fbcf58770eb01abcd08f74f087`
- `src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts`: `404e5bcb18aa6f67095c7edac5321d81aa22f38bdbc6c572e3a25a61b0071eb7`
- `src/tools/video-editor/commands/genericPatchCapture.test.ts`: `b77d131d30022480eddece73936773695799908ad2c6e4e7440231c48cf9ec6f`
- `tests/e2e/local/three-products.spec.ts`: `86f5b9f272b5749a0a487897f9180bec6e1b43dd57fd5d5252231a16e417a964`

## Changed paths and decisions

- `extension.ts`: same-track ordinary hold members now emit the exact `{ hold }`
  shape required by generic capture, while cross-track/mixed batches retain the
  existing guarded legacy shape.
- `patch-building.test.ts`: updated same-track expectations and added the
  focused five-member regression covering two parent clips plus three
  occurrence-projected visual clips in order.
- `genericPatchCapture.test.ts`: added the reviewed transition-preservation
  regression for an exact hold member.
- `three-products.spec.ts`: added the ordinary journey with the reviewed ten
  commands (five move/hold pairs), Agent intervention, newer local edit, lost
  ACK, reload, Runtime restart, exact retry, rebase, guarded undo, opaque
  preservation, and zero legacy traffic.

The independent membership review approved the five-member expectation. The
producer review approved the exact hold shape. Legacy ordinary behavior for
unsupported families remains present; this packet is source/test qualification
only, not activation or writer retirement.

## Validation

```text
npm exec vitest run --no-cache --configLoader=runner \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts
PASS — 2 files, 61 tests

npm exec eslint -- --max-warnings 0 \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/extension.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  tests/e2e/local/three-products.spec.ts
PASS — exit 0

git diff --check
PASS
```

No full suite, browser, localhost, live socket, dependency installation, or
actual ordinary gate was run, as required.

## Merge-forward and qualification dependency

Attempted:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward \
  ap2-m2-ordinary-reviewed-current-row-packet tl/integration
```

It was refused by the sandbox Git metadata filesystem:
`Unable to create .../.git/worktrees/ap2-m2-ordinary-reviewed-current-row-packet/ORIG_HEAD.lock: Read-only file system`
(exit 128). The worktree stayed clean of conflict markers and retained only
the four intended modified paths.

The ordinary browser gate is held until the App shared-core owner merges the
proven stale-adapter fix. The required owner artifact is the exact peer-fix
SHA-256 `97fb1c46827199b89f68e81cd912d72f3a6cce9bbe19fcf85d6a3a7bbc743149`
for `useTimelineOps`; this worker deliberately did not edit that path. After
that owner merge and harness commit, run one ordinary gate against the exact
current source.

The intended qualification tuple remains current public013 / Agent
`8130a401bf44a518d5a40ae274d398b8c560be55` (tree
`236c3e57e0265c52b81ba8085de3193026176bff`) / Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree
`7ab412cc4bcbe517efcfa806e092336390312e18`). No private cohort or pin was
introduced.

## Recommended next step

Have the App shared-core owner merge the stale-adapter patch, commit this
four-path candidate, then run the single named central ordinary journey. Do
not claim the browser gate or retire remaining legacy ordinary families from
this source-only packet.
