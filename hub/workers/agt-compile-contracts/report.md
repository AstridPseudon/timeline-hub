## Report: agt-compile-contracts

The docs, vectors and test are written and green on the targeted runs. The worktree holds only the new files, and the commit message and DONE marker are written.

### What I did

- **`design/audio-compile-contract.md`**: gain is multiplicative. Occurrence `source_offset` and occurrence `speed` stay metadata-only because main never plays them. Fades move to one continuous source-time envelope, with an ENVELOPE_UNRENDERED join plan. Main evidence is cited with file:line.
- **`design/visual-compile-contract.md`**: popup closure A (8 s) and B (10 s) on a shared lane. The clamp is ON, matching main's visible result (frames [0,240) and [240,540)). App's `clampToOccurrenceDuration: false` call sites diverge from that. The element clip look is an intended change from 0.0.6 to 0.0.7.
- **`tests/editing_conformance/fixtures/`**: `audio_compile_contract.json` (11 vectors) and `visual_compile_contract.json`.
- **`tests/editing_conformance/test_compile_contracts.py`**: 9 audio vectors pass, 2 fade vectors are strict xfail, the popup vectors and the half-open lane check pass, and the pin test passes.

### Test commands and results

- `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance tests/timeline/test_shot_composition_projection.py` gives **267 passed, 4 skipped, 27 deselected, 2 xfailed**. The 2 xfails are the fade vectors. The skips and deselections are pre-existing.
- `tests/editing_conformance` alone gives 250 passed, 4 skipped, 27 deselected, 2 xfailed.
- Both xfails fail for the intended reason (`render_source` is absent). Verified with `--runxfail`.
- Ruff was **not run**: the permission prompt was denied.
- No full or `full*` suite was requested.

### Decisions and findings

1. **Main's audible behaviour decides the audio items.** On `origin/main`, `shot_composition_projection.py` (lines 353, 359-365) writes the occurrence `source_offset` and `speed` as metadata only. `AudioTrack.tsx` (lines 75-76) reads only the child's `from`/`to` and `speed`. So the compiler keeps them as metadata, and App's adapter application must go.
2. **Fade curves: a question for you.** Main's `clip_fields.py:358` parses `curve=NAME` and then drops it. Audible fades are always linear. The public package does honour `fadeInCurve`. The contract neither honours nor drops it, because the decisions don't say. I recommend honouring it, but that changes audible output for films that use `curve=`, so it needs owner visibility.
3. **Clip look is already in this tree.** `origin/main` pins Composition 0.0.6 (`remotion/package.json:18`). This integration tree pins the 0.0.8 artifact. The 0.0.7 ClipLook is therefore already in the pin. The test asserts the pin is at least 0.0.7 and passes; it is not an xfail, because the premise "main pins 0.0.6" holds only for main.
4. **Viewing's 11 vectors were not reachable.** The worker `vw-m3-audio-projection-goldens2` has no output in any accessible location. The 11 audio vectors are reconstructed from the 03:17 decision and the escalation. **Viewing must reconcile them.** The popup closure's placement and child timings are also my reconstruction. Viewing should confirm them against main's frames.

### Not verified

- No PCM or frames were rendered. The vectors check only compiler output fields.
- The 0.0.8 artifact's `AudioTrack` was not read. `AudioTrack.tsx` is identical between v0.0.6 and v0.0.7.
- I did not run App's tests.

### Left in the worktree

- `tests/__pycache__/` is gitignored and was created by my test runs. I tried to remove it, but the removal was denied, so it remains.

### Commit message

The commit message is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-compile-contracts/commit-msg`. I omitted the model co-author line, following the brief's "no model names" rule, and kept the Claude-Session trailer. The file changed on disk after I wrote it; I left its current contents as they are.

### Next steps

- Viewing reconciles the 11 audio vectors with its authored set, and confirms the popup reference against main's frames.
- Orchestrator decides the `curve=` question.
- App drops its occurrence offset/speed application and its `clampToOccurrenceDuration: false` calls.
