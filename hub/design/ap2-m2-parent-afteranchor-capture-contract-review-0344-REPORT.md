# M2 parent after-anchor capture contract review

Decision: HOLD. Do not merge or activate the candidate.

## Exact candidate reviewed

- App commit: `5ad9f184b70cb22c0b01d3bbf9bb22ba3cc8b4bb`
- App tree: `6fefbe0850d72e0f5facf1c87cf44b1e4e55899e`
- Parent: `c45cc175a62701593af4ec2503467d681ec9c2f7`
- Exact Agent reference: `3b3208c43903b770010de0649691cfa566447822`, tree `84120e176540fbc2281dcff4b7186ec8ae413274`
- Candidate changes are exactly two dormant files: `parentAfterAnchorCapture.ts` and its focused test. No UI, service, session, Provider, generated schema, endpoint, or live-caller change was made. Live callers changed: none.

## What matched

The candidate carries a frozen bundle, command, and verified-media tuple as a basis; uses raw `parent/clip:<id>` selection; preserves source opaque fields; derives the source-window/rate-aware same-track ripple; leaves the other track unchanged; records the anchor and asset reads, after-selection order/boundary, peer timing writes, after-clip/after-track bindings, and the reserved asset/clip IDs. It keeps the current `afterClipId` refusal unchanged.

The candidate source worker reported its focused lane as 2 files / 8 tests passed, ESLint passed, and `git diff --check` passed. Its repository-wide TypeScript check still reports unrelated current-repository diagnostics; it reported no diagnostics in the two new files. The unchanged App neighbor was run directly here:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/parentClipAddCapture.test.ts
1 file passed, 6 tests passed
```

No full, browser, HTTP, socket, pin, activation, or unchanged-source qualification was run.

## Blocking parity findings

1. The recorder is not Agent-exact. The candidate runs the existing append path first, then rewrites the result in `decorate`. At lines 221-227 of `parentAfterAnchorCapture.ts` it replaces the recorder's mirror history with two synthetic `derived_writes` entries. Agent `3b3208c43` calls `compile_mirrors()` once before `create()` (`native_parent_media_commands.py` lines 119-122); `_recording.py` records one mirror derived write. The candidate therefore changes recorder ordering and before/after states, even though its final bundle looks right. This violates the required recorder parity.

2. The `at_ms` workaround is not exact Agent behavior. Lines 262-267 strip `at_ms` before delegating to the append helper and restore it afterward. Exact Agent `3b3208c43` still sends the after row through `_clip(..., raw_window=True)`, whose unsupported-field loop rejects `at_ms` (`native_parent_media_commands.py` lines 82 and 110-114). The candidate's positive test therefore proves an App-only acceptance that the cited Agent commit does not provide.

3. The same delegation forces the wrong timing/opaque contract for valid Agent after rows. The Agent after path uses `raw_window=True`, which permits a preserved source transition and can derive a missing video hold from `from`/`to` (`native_parent_media_commands.py` lines 82 and 127-144). The candidate delegates with `select: parent`, so the existing App validator uses `rawWindow=false`: a cloned source transition is refused and a missing hold is refused. The Agent neighbor explicitly exercises an opaque source with a transition; the candidate test does not.

4. There are smaller raw-value mismatches in `cloneAfter`: `??` treats an explicitly present null effect/track/asset as absent, whereas Agent `_after_row` uses dictionary presence/default semantics; and `sourceDuration` rejects zero hold although the Agent duration helper permits zero and applies the 0.05-second floor. These need focused refusal/acceptance tests before parity can be claimed.

## Smallest concrete correction

Implement the after-anchor operation at the existing capture-engine seam (or add a narrowly scoped raw-window parameter to that helper) so the Agent sequence is preserved: verify media/rate, validate the cloned row with the same `raw_window` rule, read/select the raw anchor and ordered peers, write peer timing, compile the mirror once at the Agent point, then create at the recorded boundary. Do not append and manually repair the recorder afterward. Remove the `at_ms` strip/restore; either refuse it exactly as Agent `3b3208c43` does and add that negative test, or first obtain a new Agent source contract before accepting it. Add the transition/missing-hold, explicit-null, zero-hold, and exact `derived_writes` parity assertions.

## Conclusion

The source carrier is safely dormant and has no live callers, but this exact commit/tree is not approved because its recorder and accepted row-shape behavior diverge from Agent `3b3208c43`. No product edits were made in this review worktree.
