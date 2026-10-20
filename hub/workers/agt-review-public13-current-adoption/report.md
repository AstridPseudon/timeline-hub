## Result

**APPROVE pin-only. HOLD normal-render qualification** until a separate 0.0.13 installed profile exists.

- Agent tree: `30da0a5e`, tree `0dacaabb`.
- Archive: 58,477 bytes, 77 members, SHA256 `9412ae25…d54738`.
- Lock integrity: `sha512-6qgEAcfY…WgLOuQ==`; lockfile SHA256 `c4d7030b…7a4e24`.
- Composition source: `73bd62b1`, tree `13e37553`.
- Existing 0.0.12 artifact remains unchanged: SHA256 `0a7b6152…f0f1a3`.

Verified only metadata plus the existing `encodedEnvelopeSource` evaluation export/type re-export changed. Root behavior, defaults, theme, labels, scene, loop, mouth, and compatibility assertions remain intact. No Runtime changes were made.

Tests:

- Central targeted: **193 passed, 3 deselected**.
- Node 20 isolated consumer: **31 assertions passed**, including public evaluation/theme/type checks and four forged-source negatives.
- 0.0.12 consumer produced the expected red failure for the new named import.
- Direct local non-socket tests: **187 passed**; six socket tests were sandbox-blocked and covered by central testing.

The shared `agent-remotion-current` profile is still 0.0.12, so it was not treated as HostReady. `commit-msg` and `DONE` were written.