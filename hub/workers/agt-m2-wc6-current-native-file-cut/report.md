## WC6 report

Implemented the approved native detached-document adapter on current `3c4f6de4`, including timing/media ordering, strict opaque/source-window/order guards, authenticated media reads, inverse/reload protection, and exact retry identity.

Tests:

- Targeted unit/conformance: `251 passed, 2 deselected`
- Ruff: passed
- `git diff --check`: passed
- Central `native7d-sockets-integration` with only the WC6 node: `1 passed in 9.70s`
- Full suite: not run

Added the required `integration` marker so the named socket suite selected the proof. WC1/WC2/WC7 positives and narration/structural holds remain unchanged; whole WC6 deletion is not claimed.

Commit message written and `DONE` created. Harness commit tree: `d8242e883b799c7d2a9422055d8eca58d1fbbfd2`.