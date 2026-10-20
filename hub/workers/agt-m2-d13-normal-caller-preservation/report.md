Implemented a small test-only PR in [test_runtime_publication_chain.py](/home/user/work/wt/agt-m2-d13-normal-caller-preservation/tests/packs/video_editing/test_runtime_publication_chain.py).

- Added parity assertions for durable assembler target, ordered media, replacement intent, settled proposal guards, and pinned render authority.
- Preserved the legacy refusal control; no new API or Runtime tests changed.
- Wrote commit message and `DONE` marker.

Tests:

- SDK targeted: 70 passed.
- Local control lane: 1 passed, 2 deselected.
- Central `registered014-render-integration`: 2 passed, 1 deselected.

No blockers.