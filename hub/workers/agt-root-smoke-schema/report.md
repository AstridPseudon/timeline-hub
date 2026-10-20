## agt-root-smoke-schema report

**Result:** The patch applied cleanly to this branch. It is a 3-line addition to `remotion/__smoke__/bundle.mjs`. It adds `derivedFrom`, `media_id` and `origin` to `EXPECTED_ALLOWED._ASSET_ENTRY_ALLOWED`. The new list now matches `remotion/src/types.generated.ts` and `astrid/core/timeline/banodoco_schema.py` exactly, in the same order. The worktree's only change is that file.

**Verification (not green):**

1. `request-test agt-root-smoke-schema targeted --files "tests/test_schema_contract.py tests/packs/rendering/test_remotion_render_contract.py"`
   - Result: 1 failed, 25 passed, 3 skipped.
   - Cause: `TextCardVisibleMarkupTest::test_text_card_renders_visible_markup` expected Node v20.19.4 (pinned in `remotion/package.json`). The default environment has Node v22.22.0.
   - All schema-contract tests passed, including `test_generator_arrays_match_frozensets`.

2. `request-test agt-root-smoke-schema consumer-regressions-integration` (named suite, which runs Node 20 via `env -i`)
   - Result: 1 failed, 5 passed.
   - The Node version now matches. The remaining failure is the same test, which compares `/home/user/work/runtimes/agent-remotion/package.json` with the snapshot `remotion/package.json`. The runtime checkout pins `@remotion/*` at 0.0.8 tarballs, while the snapshot has 0.0.10.
   - The patch does not touch either `package.json`, so this mismatch is environmental and unrelated to the patch. I did not run the test on the unpatched base to confirm that directly.

I did not run `remotion/__smoke__/bundle.mjs` itself; it needs a bundled Remotion install. The allowlist match was checked by reading the arrays.

**Decisions:** I used the named `consumer-regressions-integration` suite for the Node-20 check, rather than the whole-repo `remotion-env-nodes` suite, to keep the run narrow. I did not request any full suite. Nothing was pushed, merged or committed by me.

**Blocked?** No. The patch is in place and its own check matches. The failing SSR test is a runtime-checkout version mismatch that needs an orchestrator decision. Either the runtime checkout should be aligned to the snapshot, or the snapshot should move to match it. I did not hand-port any alternative design.

**Files written:**
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-root-smoke-schema/commit-msg`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-root-smoke-schema/DONE`

**Next steps:**
- Confirm that the runtime checkout at `/home/user/work/runtimes/agent-remotion` should pin the same `@remotion` version as the snapshot. Then rerun the consumer named suite.
- Commit the change from `commit-msg` when the harness picks up this worktree.
