# App approved project-data removal application report

Status: blocked; no product files changed.

## Result

The approved three-path patch was not applied because the current App
baseline (`9ea5b988542ceea4fec769da736ed464009da668`, tree
`b296de1e18167694394e81883c46e39cf1c16a13`) blocks its first
`clipMovePrimitives.ts` hunk. Per the task instruction, I did not hand-adapt
the hunk or use a workaround.

## Exact blocker

Command:

```text
git apply --verbose --check --whitespace=error-all \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-remove-ordered-carrier-UNAPPLIED.patch
```

Result:

```text
Checking patch src/tools/video-editor/commands/clipMovePrimitives.ts...
error: while searching for:
      actual.value === this.isolatedOwner(ref.slice(0, -'/shot'.length), expected.value);
  }

  set(ref: string, path: string[], state: AgentState): void {
    if (!path.length && (ref.includes('/asset:') || ref.includes('/clip:'))) {
      const slash = ref.lastIndexOf('/');
      const owner = ref.slice(0, slash);
error: patch failed: src/tools/video-editor/commands/clipMovePrimitives.ts:219
error: src/tools/video-editor/commands/clipMovePrimitives.ts: patch does not apply
Checking patch src/tools/video-editor/commands/projectDataMember.ts...
Checking patch src/tools/video-editor/commands/projectDataMember.test.ts...
```

The exact minimal conflict is the patch's first hunk at
`clipMovePrimitives.ts:219`. The reviewed patch expects the old asset/clip
special-case body in `AuthoredState.set`; stage9ea has already removed that
body, so the reviewed hunk cannot be applied byte-for-byte. The subsequent
approved insertion-order changes in the same file were not applied either.

`projectDataMember.ts` and `projectDataMember.test.ts` still have the reviewed
base blobs (`5d4dd26be9e5b296c18fab1372a67ebef2d8d78f` and
`704baa3652086b949161638173d8f75bde8b6ada`), but they were intentionally not
partially applied because the requested result is the exact three-path delta.

## Protected files

The stage9ea protected files were unchanged and byte-identical to `HEAD`:

| path | blob |
| --- | --- |
| `runtime.lock.json` | `c2c59acd8ad7a1bc77be82f0348c1023f010b66f` |
| `src/integrations/runtime/generated-contract-metadata.ts` | `06f8a79906763833d6ce037dbd61baf35a554b5d` |
| `src/integrations/runtime/generated.ts` | `f8bcd8287b0f987827e73c44ceaf3ea27c02c925` |
| `src/integrations/runtime/timeline-commit-types.ts` | `b4a6fea6064fb43d10b5395475c999700423e3a5` |

The normal generated `AgentWrite.insertion_order?: Array<string>` field is
present in `timeline-commit-types.ts`; no pin, generated file, API, caller,
store, or activation change was made.

## Verification and evidence

```text
git apply --check --whitespace=error-all <approved patch>
=> failed only at clipMovePrimitives.ts:219; projectDataMember.ts and its direct test were checked

git status --short
=> clean

git diff --check
=> clean (no worktree diff)

git hash-object <protected files>
=> matched each corresponding HEAD blob listed above
```

The requested three-file Vitest controls, lint, and TypeScript no-emit checks
were not run because the exact candidate could not be applied to this source
baseline. Prior approved candidate evidence remains the 33-test, lint, and
strict TypeScript result recorded in
`ap2-m2-remove-exact-patch-safety-review-1127-REPORT.md`; it does not qualify
this blocked stage9ea application.

No full, browser, HTTP/socket, generation, install, integration, pin, or live
caller test was run. No live caller was changed.

## Handoff

The App manager needs an updated approved three-path patch whose
`clipMovePrimitives.ts` delta is based on stage9ea's already-reduced
`AuthoredState.set`, or must explicitly resolve this source-baseline conflict.
The reviewed patch's semantics and protected-file constraints remain
unchanged.
