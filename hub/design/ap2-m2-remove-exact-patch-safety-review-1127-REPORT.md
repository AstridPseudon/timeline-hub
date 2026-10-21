# Exact ordered project-data removal patch review

Date: 2026-10-21 UTC

## Verdict

**APPROVE for the three-path App source delta only.** No correction is
required in the supplied patch. Downstream application remains **HOLD** until
the normal generated binding containing the optional carrier is landed and the
containing public pin/release is refreshed. The current public014 binding must
remain unchanged until then.

## Identity and scope

- App worktree is clean at `92c30b570cf8105dc021a64874c258e6c950b841`.
- The three patch base blobs match the current worktree exactly:
  - `projectDataMember.ts`: `5d4dd26be9e5b296c18fab1372a67ebef2d8d78f`
  - `clipMovePrimitives.ts`: `401c559c179eb4d4f675e5e3eff052abadf4c3ac`
  - `projectDataMember.test.ts`: `704baa3652086b949161638173d8f75bde8b6ada`
- The supplied candidate indices are the reviewed tested blobs
  `a8ce58a4097d1a56bc9806bf47a23ca487defb89`,
  `442c5ba4a497d3147fcccad8948025b5610a0c5b`, and
  `e140a59955753b6113f17f1ff28e45260459c8d0` as independently recorded by
  the exact-diff report.
- The delta is limited to the requested three App paths. It does not alter
  the generated binding, a caller, a pin, a store, a DTO, or an endpoint.

## Safety review

The source lowering matches the approved Agent remove recipe and the Runtime
42a generated-carrier shape:

- Public `project-data.delete` is accepted only with its closed `{key}`
  payload and lowers to the existing `project-data.write` command with
  `mode: "remove"`; no delete alias or new carrier is introduced.
- A missing target namespace records a read-only absent target. A missing leaf
  in a non-empty namespace records the required absent-to-absent guarded write
  and omits `insertion_order`.
- A present non-empty namespace clears only the requested leaf. A null or
  empty namespace is pruned, and the parent namespace write carries the raw
  `Object.keys(config.app)` sibling order. An empty `config.app` is then
  pruned without manufacturing another carrier.
- Null leaves, opaque values, and unrelated siblings remain ordinary JSON and
  are preserved. Existing replace/merge lowering and four-field ordinary
  writes are unchanged.
- Inverse restoration consumes the optional carrier through the existing
  `AuthoredState` path, validates that the current sibling order is compatible,
  and fails with `history_unavailable` on a missing target or incompatible
  order. Captured claims remain leaf/ancestor guards, so disjoint key replay
  remains allowed while same-key changes remain refused.
- The optional field is omitted when unused and is never represented as null.
  The current App public type is still the old four-field `AgentWrite`; this
  source patch therefore must not be activated against the current binding.

The approved Agent source review (`ed5fd33c4a7fa9956178f9b24eb127415eaca9e6`,
tree `f4a632e4f627499e0b15d8477db9aaab78ebb3d2`) confirms the same remove,
recording, state-setter, inverse, rebase, opaque/null, and order semantics.

## Evidence

Commands run in this review:

```text
git apply --check --whitespace=error-all <exact patch>
=> passed

git apply --stat <exact patch>
=> 3 files changed, 171 insertions(+), 33 deletions(-)

git diff --check
=> passed

git status --short
=> clean
```

The exact candidate identity and private candidate behavior were already
proven in the supplied 1118/1123 reports, and were reused after the base/blob
identity check:

```text
vitest: projectDataMember.test.ts visualSeamProjectDataMember.test.ts
  genericPatchCapture.test.ts
=> 3 files passed; 33 tests passed

strict TypeScript proof for optional and omitted AgentWrite shapes
=> passed

eslint on the three changed source/test files
=> passed
```

No product source was changed here. No full, browser, HTTP/socket, install,
live-caller, lifecycle, activation, or pin test was run.

## Required next step

Generate and land the normal AgentWrite binding from the approved schema
successor (`insertion_order?: Array<string>` in TypeScript, optional string
array in the other generated projections), then perform the normal containing
release/public-pin review before applying this exact three-path source delta.

