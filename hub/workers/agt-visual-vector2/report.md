## agt-visual-vector2: report

Vector 2 (the overhang closure) is in place, and the targeted compile-contract run is green with 26 passed and 4 strict xfails. The commit message is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-visual-vector2/commit-msg`. `DONE` is created. Nothing was committed or pushed by me.

### What changed (worktree `/home/user/work/wt/agt-visual-vector2`, branch `tl/agt-visual-vector2`)
- **`tests/editing_conformance/fixtures/visual_compile_contract.json`** (schema 2 → 3)
  - Native vector 1 is untouched.
  - New `overhang_closure` block, labelled "OVERHANG VARIANT (not App output)". It is the native parent with only the occurrence list replaced: occ-c on the picture lane at 2 s, 1.5 s long, pinning the native `shot-1` revision. Its `clip-a` child is 2 s, so it runs to 5 s against an occurrence end of 3.5 s.
  - `physical_reference` is `{"status": "pending", "owner": "viewing"}` with no values.
  - Six new vector rows: three clamp-on (90 / 105 / 15 frames) and two clamp-off (end 150, duration 60).
- **`tests/editing_conformance/test_compile_contracts.py`**
  - `_native_projection()` became `_projection(closure)`. The overhang closure replaces only the occurrence list.
  - Vector rows select their closure with `vector.get('closure', 'native')`.
  - New `test_overhang_child_is_clamped_to_its_occurrence_end`. It checks the compiler's visible window: at 3.0 s, 0.5 s visible, ending at 3.5 s.
  - `clip_timeline_duration` added to the imports.
- **`design/visual-compile-contract.md`**: status line updated; the "clamp not exercised" text now points to vector 2; new section 1b; physical-reference note for both closures; vector table, measured results and Open items updated.

### Test commands and results
- Targeted, via the test service: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-visual-vector2 targeted --files "tests/editing_conformance/test_compile_contracts.py"`, then `wait-test agt-visual-vector2-targeted-1020050917-11665`.
  - Result: `pass exit=0`, **26 passed, 4 xfailed**.
  - The 4 xfails are the two existing audio vectors 10–11 and the two new clamp-off rows.
- Compiler values, read from `project_runtime_parent_composition` at `Fraction(30000, 1001)`: native occ-a 270/330/60, occ-b 330/390/60 (both unchanged). Overhang occ-c clamp-on 90/105/15. These agree with the expected values.
- `git diff --check`: clean.
- No full suite was requested.

### Decisions I made
1. **Clamp-off is not a compiler mode.** The Python compiler always clamps to occurrence end, so the clamp-off rows cannot come from it. I put the unclamped values (end 150, duration 60) in the fixture and marked them `xfail(strict=True)`. The reason names the 03:46 decision, which removes the per-call option. The brief asked for "clamp on and off from the actual compiler", and that part is only half true; I could not do better without adding a mode, which the decision rules out.
2. **Vector 1 kept exactly native.** The 8 s overlap stays, pending App's hub confirmation.
3. **Schema bumped to 3** because the fixture structure changed. Nothing else reads this file.

### Finding for the orchestrator (not resolved)
Viewing's MAIN report says MAIN's default clamp cuts the native closure's A children at **10 s**, which is B's start, not A's end at 18 s. Specifically, `occ-a:clip-a` is `to 4` (end 10) where the compiler has `to 6` (end 11), and `reserved-child` is `to 5.75` where the compiler has `to 6`. That is a real divergence between MAIN and the compiler on vector 1. I read that claim from the report and did not verify it against MAIN's source. The doc records it as open, and the orchestrator needs to decide which clamp is intended.

### Unverified / blocked
- The MAIN physical reference for both closures is pending Viewing's analog. Viewing's probe found that MAIN's rational-fps path gives `NaN`, and the fixture media has no playable bytes. No frame values exist yet.
- I did not confirm App's overlapping spans; that is still with App via the hub.

### Notes
- **Commit message attribution:** the system reminder asks for Co-Authored-By trailers, but your brief says "no model names". I followed the brief and left the trailers out. Please check which one you want.
- **Scratch file not cleaned up:** I wrote a probe script at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/agt-visual-vector2-probe.py`. My attempt to delete it was denied, so it is still there. It is outside the worktree and holds no build output.
