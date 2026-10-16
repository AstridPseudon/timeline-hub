# SDK transition admission

The normal SDK transaction resolves timing through its existing path, then uses
`motion/element_motion.py` and the renderer project's public
`@banodoco/timeline-composition/evaluation` export before journal append or save.
The existing renderer esbuild loads both the public evaluator and the small
consumer adapter; no native TypeScript fallback or separate planner is used.
The current 0.0.7 export imports TypeScript parameter properties, so Node strip-only
loading is insufficient. Renderer discovery, Node pin and timeout remain owned by
the existing evaluator boundary. A missing export, runtime, invalid configuration,
or malformed response becomes typed `transition/unsupported-host` with a next step.

Changed builtin look transitions are outgoing declarations through public
`declareAppTransition` and `prepareDeclaredTrack`. They require explicit duration;
raw look patch type, duration and params reach admission before codec normalization
can discard them. The existing codec still owns persisted legacy shape. The
transaction also captures raw stored transition values before timing resolution,
and retains its earlier direct-write guard and in-place rollback.

Current DFI revisioned transitions retain destination ownership, elementRef,
registry/resource validation, adjacency rules, precise seconds, params and opaque
payload. Their affected track spans enter the same public `prepareDeclaredTrack`
with no fabricated outgoing declaration. The existing composite predecessor guard
now returns the same typed overlap code and usable next step for immediate overlap;
the shared evaluator also refuses overlaps elsewhere on the track and later timing
edits. No custom contribution is guessed or mapped to a builtin.

Unchanged legacy metadata is opaque on load, unrelated edits and same-frame timing
edits. Removal remains a recovery without a host. Exact captured inverse payloads
restore existing metadata instead of authoring fresh declarations; geometry changes
still enter track admission. Existing DFI/music transaction resolution, direct-write
recording, check admission and persistence paths are preserved.

Focused tests use a disposable package context linked to the receiver's vendored
Composition source and an explicitly supplied existing esbuild. Set
`TRANSITIONS_TEST_NODE`, `TRANSITIONS_TEST_ESBUILD`, and optionally
`TRANSITIONS_TEST_EVALUATION_PACKAGE`; these are test-only inputs, not production
fallbacks. Tests cover real SDK mutations, gaps/touching/overlap, raw patch custody,
retained-view rollback, host refusal, modern DFI payload preservation and later
geometry refusal. Existing composite inverse/shared-source and transaction tests
supply compatibility evidence.

This increment adds source-level SDK admission. Historical unchanged App/Composition
fixture evidence is reused only as such. Named v8 boundaries remain unavailable;
Player/render parity and rendered visibility remain open. No card acceptance or
release claim follows from these tests.
