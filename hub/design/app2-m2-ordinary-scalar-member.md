# App ordinary scalar member integration evidence

Base: `1eb5364d76bb7dac95b085a4aabd7d97f57dd138`

The row-local implementation adds only:

- `src/tools/video-editor/commands/ordinaryScalarMember.ts`
- `src/tools/video-editor/commands/ordinaryScalarMember.test.ts`

The command accepts the existing Agent `clip.set` record shape for positive
finite `hold` values and explicit `hold`, `asset`, or `transition` clears.
Values delegate to the existing generic native recorder. Clears use the same
App `MoveRecording`/`AuthoredState` primitives and preserve opaque siblings,
unchanged writes, exact clear absence, capture claims, and sequential ordinals.
The hold guard matches Agent's current source window, relation, quantization,
mirror, and occurrence-boundary behavior; unsupported transition SET and other
scalar fields remain visible/refused.

Native source used for the actual probe:
`310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`.

Evidence: focused App Vitest passed (16 tests), ESLint and TypeScript passed,
and the actual generated hold-value + transition-clear command pair passed
Agent validation/execution with equal final bundle, inverse, redo, and replay.
Agent scalar conformance passed 168 tests with 3 existing skips.

No shared files, generic capture helper, contracts, pins, dependencies, Git
operations, full/browser/socket suites, or writer retirement were changed.
