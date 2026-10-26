# U3/U4p D141 final handoff

## Result

SOURCEPASS. The protected source repair is qualified at
`db8cc7655e5ca81a9c0989a5104645b069571e98`.

`AgentChat.tsx` is the only owner-return source path. Its tour predicate now
returns `TourChatPanel` before the availability check and live session hooks;
the exact 89 protected tests, current voice-aware/unified-menu behavior, and
the v2 save/reply/dependency/undo path are preserved. The Runtime adoption is
independently confirmed as tool-only: lock source `6a011d58…`, clean producer
tree `ac5b8627…`, 14 mappings, and generated/schema/config bytes conserved.

## Remaining generated inputs

Do not treat this as whole-cut-ready. Final Agent head and qualified generated
inputs remain required. `public/install-manifest.json` still has Runtime source
`ab1e4f6141987706132916e2da16477f5a019464`; Agent vendor provenance remains
pending its final qualified producer for
`vendor/astrid-browser/astrid/packs/astrid_motion/rendering/elements/effects/am-footage/component.tsx`
and `vendor/astrid-browser/astrid/packs/rendering/elements/catalog.ts`. Do not
invent pins or rewrite those files in this review.

The inherited U4p custody record has a nonblocking path-label typo for
`contract/artifacts.json.version`; use the actual `version` field in
`contract/artifacts.json`.
