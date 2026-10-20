## Report: agt-visual-contract-correct

The visual contract now uses App's native ADD fixture instead of the reconstruction. Targeted tests pass, with the two audio strict xfails unchanged. The audio reconciliation is blocked on Viewing's originals, which I could not find.

### What changed (worktree `tl/agt-visual-contract-correct`, uncommitted)
- **`tests/editing_conformance/fixtures/visual_compile_contract.json`** (schema 2): stores App `309cb7a4` `add.output` verbatim as `native_add_output`. Source: `src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json`, blob `22be2059`. Occurrence A (occ-a) is at 8 s and B (occ-b) at 10 s, both 10 s long, on `picture`. Fps is `{numerator: 30000, denominator: 1001}`.
- **`tests/editing_conformance/test_compile_contracts.py`**: the visual half now projects the native closure with `project_runtime_parent_composition`, which is the path for runtime parent closures. The clock is `Fraction(30000, 1001)`. The dict and `[num, den]` forms raise at `_positive_fps`, which I confirmed.
- **`design/visual-compile-contract.md`**: rewritten section 1 and the vector table. Section 2 (clip look) is unchanged.
- **`design/audio-compile-contract.md`**: new subsection listing what could and could not be reconciled, and which vectors need Viewing sign-off.
- **`design/owner-film-differences.md`**: appended section 4 with the compiler and source evidence. Nothing else in the file was altered.
- **commit-msg** written; **DONE** created.

### Rows (main's projection, probed on this branch; `_project_clip` is identical to main e51595c6)
| Row | Frames |
|---|---|
| occ-a source child `clip-a`: start / end / duration | 270 / 330 / 60 |
| occ-b source child `clip-a`: start / end / duration | 330 / 390 / 60 |

### Findings for the orchestrator (not decided here)
1. **The clamp is not exercised by the native closure.** No child extends past its occurrence end: A's largest child ends at 15 s against an end of 18 s, and B's at 17 s against 20 s. The clamp on and off give the same rows. The 03:46 premise that A's child runs into B came from the reconstruction. The "clamp ON" policy is still a policy, not evidence from this closure.
2. **Occurrence spans overlap.** A spans 8–18 s and B 10–20 s, an 8 s overlap on the picture lane. Main accepts this. The source-window children do not overlap: A's child ends at 11 s, where B's begins. Please confirm that overlapping occurrence spans on a shared lane are intended.
3. **Physical reference not produced.** The approved executable analog (generated media, MAIN fed `Fraction(30000, 1001)`) belongs to Viewing. No media was generated here and no frames were rendered.

### Audio (task 2): not reconciled
- Viewing's `vw-m3-audio-projection-goldens2` is not reachable. It is not in the orchestrator's `workers/`, not in any worktree under `/home/user/work/wt`, and not on any branch or path I searched under `/home/user/work`, `/home/user/peteromallet` or `/home/user/banodoco`.
- The closed escalation `viewing-20261020T0309Z` quotes four of Viewing's values. They match this file's vectors 1, 2, 7 and 8.
- **Needs Viewing sign-off:** vectors 1, 2, 7 and 8 against the authored originals; vectors 3, 4, 5, 6, 9, 10 and 11, which the escalation does not quote. Vectors 12–14 are Agent-authored under the 04:24 curve decision.

### Tests (exact commands and results)
- Direct: `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_compile_contracts.py -rxX` → **22 passed, 2 xfailed** (the two strict audio xfails, 10 and 11, each with its reason).
- Central service, targeted: `request-test agt-visual-contract-correct targeted --files "tests/editing_conformance/test_compile_contracts.py"` → **pass, exit 0, 22 passed, 2 xfailed**.
- No full suite was requested.
- **Not run:** ruff. The lint command was refused as requiring approval, so the lint status of the edited file is unknown.

### Decisions I made
- **Rows:** the six rows are the source-window child of each occurrence (`clip-a`), not the occurrence window. The occurrence window is not a projected clip. The two `reserved-child` and `clip-b` children are not in the row set.
- **Overlap test:** the "half-open" test now checks the source-window children only, because occurrence spans overlap by design of the native fixture.
- **Added checks:** two non-row vectors cover the closure placement (A at 8 s, B at 10 s) and that the reserved child keeps `opaque` `[null, false, {}]` and `params: null`.
- **Commit trailer:** I omitted the `Co-Authored-By: Claude Haiku 5.5` line from the commit message because the brief says no model names. I kept the `Claude-Session` line.

### Blocked / unverified
- **`__pycache__` left behind.** My pytest runs created gitignored `__pycache__` directories under `astrid/`, `astrid/core/...` and `tests/`. I was denied permission to delete them, so the worktree still has build output. This breaks the "leave no build output" rule and needs a manual `rm -rf` of those directories.
- Not verified: pixels, frames and PCM; App tests and App's clamp replica; the pinned 0.0.8 artifact.

### Next steps
1. Orchestrator to decide the clamp and the overlapping-span question, with a closure that actually overhangs if the clamp is to be evidenced.
2. Viewing to produce the physical reference against the six rows, and to sign off the audio list above.
3. Remove the `__pycache__` directories in the worktree before commit.
