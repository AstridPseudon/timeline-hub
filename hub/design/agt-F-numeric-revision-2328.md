PASS_SOURCE — added the existing `selected_runtime_env` fixture import to register the genuine retained-pack bootstrap dependency. No production files, helpers, or test bodies changed.

Source hashes:

- Before: `20f350633c5522437c657b86e0ccc434b6cf486ee94248401d072acd771f7297`
- After: `d715740334878c67d39af14263bc9e14e67c3124fb8d71706616ddac180f41c6`
- Agent base: `5d4ae93c833c`
- Runtime source: `732c48c6f5a9`

AST conservation:

- Six numeric parameter rows: body/decorator/args unchanged; 12 asserts, 3 raises.
- Three guard parameter rows: body/decorator/args unchanged; 5 asserts, 1 raise.
- All nine assigned selectors preserved.

Evidence:

- `py_compile`: pass
- Ruff baseline and candidate: pass
- Mypy baseline and candidate: pass
- `git diff --check`: pass
- No pytest, test-service, build, render, or functional rerun performed.

The nine nodes remain scheduled for the single later batched rerun. Protected review is pending. Commit message written and `DONE` created.