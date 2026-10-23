# R1-native review: `c79398561` against `9729c07b`

Independent source review: **PASS** for the exact three-file delta
`c79398561e5612d0a393074e6b9a198992d77f5b`.

`RuntimeCommitService.commit` is the production caller. Its legacy stale-head
branch passes the authenticated request and evaluated landing head through
`rebase.replay`; `rebase.replay` passes both into `commands.execute`. The
original-base `steps`/`label`/`merge_mode` overwrite is removed, so landing
steps, dependency union, bindings, and patches are generated from the replay
head. Existing ABI-1 normalization, original-base and head guards, undo and
authentication remain intact. No product, Runtime, schema, client, pin, or
test behavior was weakened.

Evidence on this checkout: focused `2 passed`; native/read `28 passed`; provider
plus native vectors `127 passed`; scoped Ruff, normal Ruff ratchet (`2150 =
2150`), private mypy ratchet (`1915 = 1915`), default vendor lock, artifact,
and diff checks passed. Direct output inspection showed `status=rebased`, the
actual `rebased_onto` landing head, a nonempty landing step patch, 68
dependencies, and replay bindings.

The exact retained-source node was attempted once by the author against Runtime
`ad823e0a...` and stopped in fixture setup when Agent V2 `_fps_values` rejected
mixed numeric/rational FPS values. It did not reach replay, is not replay-failure
evidence, and is owned by the separate V2 FPS audit 0453. This report claims
source qualification only, not actual wire/full54 qualification. The current
home port should carry only this narrow delta after the merge-hold audit; then
rerun that one retained-source node after the V2 ruling.
