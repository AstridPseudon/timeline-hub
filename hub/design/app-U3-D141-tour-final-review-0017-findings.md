# U3/U4p D141 final source review findings

## Verdict

SOURCEPASS for the protected source review. This is not a whole-cut readiness
verdict.

## Finding

- `U3-U4P-D141-EVIDENCE-LABEL` — nonblocking evidence defect. The inherited
  U4p `source-custody.json` records `contract/artifacts.json.version` as a
  required hash path, but the path is absent in the actual Runtime checkout.
  Runtime's canonical `contract/artifacts.json` contains the matching `version`
  field, its file hash matches the recorded value, the producer checkout is
  clean at `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, and the read-only
  `vendor-lock.mjs check` passes. This label defect does not change the
  tool-only adoption result.

## Source result

The one prior blocking regression is repaired in the sole allowed file:
`AgentChat.tsx` imports `useEditorTourRunning` and `TourChatPanel`, evaluates
the predicate after the bridge hook, and returns the scripted panel before the
availability door and live session hooks. The current voice-aware engagement,
unified `AgentChatMenu`, v2 outbox/reply/dependency/undo path, and non-tour
availability behavior remain in the tree. The exact test/mock/input/predicate
blobs are unchanged.

The mandated two-file run passed 89/89 tests: 13/13 `TourChatPanel.test.tsx`
and 76/76 `AgentChat.test.tsx`. Scoped ESLint and both TypeScript checks passed.

## Deferred inputs

`public/install-manifest.json` still carries the historical Runtime source
pointer `ab1e4f6141987706132916e2da16477f5a019464`, and Agent browser vendor
provenance remains pending final Agent qualification for
`vendor/astrid-browser/astrid/packs/astrid_motion/rendering/elements/effects/am-footage/component.tsx`
and `vendor/astrid-browser/astrid/packs/rendering/elements/catalog.ts`. These
are generated qualification inputs, not source-review failures; no pins were
invented.
