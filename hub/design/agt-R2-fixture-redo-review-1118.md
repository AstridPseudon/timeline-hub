Implemented the setup/helper-only review change in [test_recipe_m2_auto_placement.py](/home/user/work/wt/agt-R2-fixture-redo-review-1118/tests/editing_conformance/test_recipe_m2_auto_placement.py). Provider-generated accepted records are now used intact; no caller bindings are spliced or fabricated. Test ASTs remain unchanged.

Evidence:

- Final helper diagnostics: all four M2 cases PASS.
- Native controls: 2 PASS in mandated run.
- Exact six-node run: 2 passed, 4 failed before the final helper correction; final exact pytest rerun was intentionally not performed per “once” instruction.
- Ruff: PASS.
- Qualified mypy: PASS.
- AST parity: PASS.
- `git diff --check`: PASS.
- No full suite or captured nested real-positive rerun.

Refs/blobs:

- Commit: `77dc9677a8ded0758250364535c991748a471e08`
- Tree: `7cef3d77a64f5e0fc5ddd11931b393400c8a1a02`
- Captured blob unchanged: `afd57690be0fd6171cc3335875c476e6e3a814fd`
- M2 working blob: `770aa1094f3a3536a111a768e66e99f7a9eafa4f`

Recommended next step: rerun the exact six controls on the final working tree.