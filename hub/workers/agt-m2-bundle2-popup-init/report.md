I added a guarded `timeline.init` v1 op on top of `tl/integration`. The targeted run passed after my last edit: 797 passed, 4 skipped, 29 deselected, 173 subtests. I wrote the commit message and created `DONE`.

**What the op does**
- **Args:** `select` is exactly `"parent"` and args are closed: `name`, `slug`, and `output` with exactly `resolution`, `fps`, `file`, `background` and `background_scale`. `background` and `background_scale` may be `null`, but every output key is required, so absence is never accepted in place of `null`.
- **Writes, in order:** `config.output`, `name`, `slug`, then `registry` set to `{assets:{}}`. The empty asset container is not an arg.
- **Pristine-init guard:** it raises `not_pristine` unless the parent is exactly the bootstrap bytes and there are no placements or shots. Extra or opaque keys, a second init, and any established timeline are all refused.
- **Guard recording:** `output`, `name` and `slug` are recorded as absent before the write, and `registry` as `{}`, so `{}` and `{assets:{}}` stay distinct. A write to any of those addresses by someone else is refused as `intervening_write`.
- **Inverse, redo and replay:** these are exact.
- **Tracks:** init followed by V1 then A1 in one batch keeps command order. Undoing init leaves the tracks alone, because their addresses don't overlap.

**Changes**
- **Op:** `astrid/sdk/timeline/_init_commands.py` is new, with a small edit to `commands.py`.
- **Schema:** `TimelineInitArgs` and an `allOf` branch in `edit-command.schema.json`.
- **Tests:** `tests/editing_conformance/test_timeline_init.py`, with the golden at `fixtures/recipe_m2_timeline_init.json`. The suite covers the golden, exact round trip, non-pristine refusals, closed args, envelope checks and intervening writes.
- **Design doc:** `docs/design/m2-empty-bootstrap-init.md`. I put it under `docs/design/` rather than a top-level `design/` because the repo has no top-level `design/` directory.

**Tests**
Targeted run via the test service:
`pytest -q tests/editing_conformance tests/sdk/test_timeline_commit_provider.py tests/timeline`. I did not request a full suite, and I did not run lint or format checks.

**Decisions and caveats**
- **No history-wide guard:** I didn't use a whole-timeline revision read as the pristine guard. After init is accepted the head moves, so that pin would break inverse. The guard is therefore exact-state reads plus the pristine check. State alone can't tell "never initialized" from "initialized, then fully undone", so the caller must resume only from proven bootstrap history. That is Runtime's job, and it's in the doc.
- **Branch overlap:** the M2 branches (scalar, track label, popup-media) aren't merged into `tl/integration`. My `commands.py` edit adds one dict entry and one whitelist entry, so it may need a trivial merge against `tl/agt-m2-scalar-commands` and `tl/agt-m2-root-schema-clean`. I reused their `Operation` pattern but nothing from them.
- **Unchanged:** `occurrences` is not a key on the opened bundle's parent. The pristine check uses the actual shape (`config`, `registry`, `clips`, plus empty placements and shots).
- **Sandbox:** direct pytest needed approval, so I used the test service. I also moved a throwaway generator test out of the worktree; `rm` was denied, so it sits at `/tmp/claude-0/-home-user-work-wt-agt-m2-bundle2-popup-init/88700939-3bc7-4d95-8833-330592b114bf/scratchpad/zz_gen.py.bak`.

**Not done (other owners)**
- **Runtime:** same-ID headless repair and the create→init crash resume.
- **App:** the `createDefaultTimeline` replacement and its outbox wiring.
- **Real-Runtime integration test:** none yet for `timeline.init`. A real-Runtime acceptance run should be the next step once Runtime ships the repair.
