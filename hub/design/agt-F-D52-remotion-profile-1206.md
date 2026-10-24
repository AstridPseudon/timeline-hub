## D52/G4 report

Qualified the exact original node:

`tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`

Used existing `agent-remotion-v3-819acf-1110`, Node `v20.19.4`, current `venv-agent`, and source-first `PYTHONPATH`.

Result:

- `1 passed in 0.56s`
- JUnit: `tests=1, failures=0, errors=0`
- Naturally returned stderr: empty
- Corrected profile matches tracked package/lock; old `255b` profile differed and used the `21fde…` archive.
- Production resolver/callers verified in `remotion_runtime.py` and Remotion renderer paths.
- No product, test, registry, install, overlay, or full-suite changes.
- `git diff --check` passed; worktree clean.

Evidence retained under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D52-remotion-profile-1206/evidence/`

Commit message written and `DONE` marker created.