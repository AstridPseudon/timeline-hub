# Runtime private6537 generator source support

This source-only change adds the reviewed C3d optional Agent schema input to
the current Runtime b92 generator. `--agent-command-schema` is explicit and
guarded by the reciprocal Agent `10226a7f` raw SHA-256
`9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`; malformed
or unpinned input is refused. The ordinary path remains bound to the current
checked-in `6ba7b51e…` schema and its existing compatibility floors.

The package-root template now has generator markers. The renderer adds every
new top-level schema definition ending in `Args` (including the expected
`TranscriptAssociateArgs` and arbitrary `NewArgs`) and excludes internal
`*Variant` aliases. For the current ordinary schema, the marker renders away
and the generated root remains byte-identical.

Only `generators/generate.py`,
`generators/python_client_init_template.py`, and the focused generator test
changed. No schema, generated artifact, metadata, manifest, package/version,
pin/config-source file, or private generation was performed. Focused generator,
schema compatibility, public API, union guard, artifact check, and generator
check evidence is recorded in the worker DetailedReport.

