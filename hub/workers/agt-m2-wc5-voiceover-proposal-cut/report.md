Implemented WC5 voiceover proposal cut.

- Replaced `TargetBoundAuthoringBundle.publish` with digest-bound EditCommand proposals.
- Migrated `draft_voiceover` to proposal/open handling and durable-outbox commit path.
- Removed `_transport_idempotency_key`.
- Preserved existing voiceover assertions; added proposal-gap coverage.
- Generated audio/timing remains explicitly OPEN because current commands cannot express it.

Test:

`23 passed` via targeted voiceover suite.

Design report: [agent-wc5-voiceover-proposal-cut.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc5-voiceover-proposal-cut.md>)

Commit message and `DONE` marker written.