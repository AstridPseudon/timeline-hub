## PCM source carry: design delivered, one cleanup blocker

The design is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-pcm-source-carry.md`. I did not create `DONE`. I wrote `BLOCKED` because a throwaway probe test file is still in the worktree and the harness would commit it on exit.

### The blocker
- **File:** `tests/packs/rendering/test_zz_probe_source_carry_domain.py` in `/home/user/work/wt/agt-m2-pcm-source-carry-design`.
- **Why it's there:** I used it to probe raw versus compiled slicing. It is untracked and fails on purpose.
- **Why it's still there:** deleting it was denied, both alone and inside a compound command. I did not work around the denial.
- **Action needed:** `rm` that file before the worktree is committed. I wrote no `commit-msg`, since no product or test change is meant to land.

### Key finding: the host slices the wrong domain
- The four PCM requirements need originals in the compiled domain, the `Timeline.load().for_render()` output that the renderer consumes.
- Today `_segment_request` (`service.py:1052`) slices the **raw** JSON. The renderer compiles the already-sliced file later (`run.py:1104-1107`). No compiled, unsliced original exists on the host.
- The probe used one fixture with a fade and `at 0.1234`. Slicing raw gives `from` 0.5016, and slicing compiled gives 0.502. That is a 1.6 ms source shift, enough to break a sample-exact comparison.
- This is one fixture, so compile idempotence still needs a real corpus before activation.

### Design in brief
- **Call sites:** `service.py:1076-1093` is where the host slices layered segments, the only place it slices. `run.py:1104-1167` is where the renderer's helper call goes, inside the existing ExitStack.
- **Carried structure:** a `SliceOrigins` value holding the window, tracks, source digest, and a map from windowed clip ID to compiled unsliced original. It is written as a sidecar with its digest recorded in `materialized_hashes`, and passed through an additive optional `RenderRequest` field.
- **Trust:** the renderer is a separate process. The sidecar is host-written and digest-pinned. The check proves the originals and transformed clips are consistent, not that the renderer is honest.
- **Validation:** the helper re-derives each transformed clip with `_window_clip` and compares it exactly, including the stamp. It refuses on digest, missing key, track, asset, fps, duplicate ID, or `None` digest. Refusals happen before any subprocess and never fall back to the frame-step callback.
- **Lifetime bug to fix:** when materializations are reused, `serving_root` is the shared cache. Successful WAVs would persist there, so the attempt directory needs a cleanup callback on the ExitStack.

### Tests
- **Written:** none. The domain and carry tests need the seam, so writing them now would encode the wrong behaviour or invent an API name.
- **Targeted baseline:** `test_normal_audio_source_phase.py` + `test_service.py` gave 54 passed, 4 xfailed (run `...-1020080014-2253`).
- **Four PCM tests:** once Viewing's helper lands, they become positives for the helper's unit-level path. They do not prove the service route, so the design adds service-route positives. Keep the strict markers until the helper is on base.

### Merge order
1. Agent `f29a9475` (Composition 0.0.12 consumer). It is not on base yet.
2. Viewing `ab935f77` (inactive helper), with the validation fixes folded in. Viewing's review approved only the inactive unit.
3. The Agent source-carry change.
4. Viewing activation of the normal route, then the served-HTTP lane.

### Decisions for the orchestrator
- Activating the helper stops non-Player fades from refusing `ENVELOPE_UNRENDERED` and changes export audio. The owner's film-viewing list needs this.
- Compile-before-slice changes every layered render with a fractional `at`, not only fades. The owner list should note it.

### Not verified
- No PCM render, Node decode, Remotion, served HTTP, or full suite was run. No `full*` suite was requested.
- The Runtime schema check for `RenderRequest` keys was not made.
