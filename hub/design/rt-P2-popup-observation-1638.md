## PASS — source cause identified

- Actual tuple: App `1540/treea3b3`, Agent `9502`, Runtime `8b32`, schema `867f`.
- Source report hash: `4d0daffd...a1229`.
- Mounted App emitter: `shotTimelineDataProvider.ts:826–853` emits `occurrence.fork` → `occurrence.add-media`; actual test is `three-products.p2-popup.spec.ts:850`.
- Runtime refusal: `timeline_commit_auth.py:1986`.
- Cause: Runtime’s `_project_created_child` handles created `occurrence:<id>` roots, but popup fork creates `shot:<id>`. That authored root is not projected into authenticated physical shot/internal images; its write falls through to `native_site(...)=timeline`, which is absent, producing `invalid_records`.
- Owner: Runtime commit validation/intermediate projection.
- Smallest correction: extend the existing authenticated intermediate projection for fork-created `shot:<id>` roots, preserving all existing identity, owner, digest, and physical-observation guards. No Agent carrier or guard relaxation is needed.

Tests:

- Runtime comparators: `2 passed, 18 deselected`.
- Agent same-step fork/add positive and negative comparators: `8 passed`.
- Agent integration media tests were unavailable because required Runtime/VibeComfy/Remotion dependencies were absent; not used as proof.

No product, test, generated, contract, or registry files changed. Worktree is clean. Proposed next step: Runtime owner implements the narrowly scoped fork-root projection and runs the offline comparators above plus a focused fork→ADD Runtime acceptance test.