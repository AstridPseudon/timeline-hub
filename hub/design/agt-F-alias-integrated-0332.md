## Result

Ported only the reviewed `d7390a90d4` trusted-seed fixture hunk in [test_authoring_bundle.py](/home/user/work/wt/agt-F-alias-integrated-0332/tests/timeline/test_authoring_bundle.py). No product edits.

AST checks passed:

- Target body matches reviewed `d7390a90d4`.
- 11/11 assertion predicates preserved.
- `_closure` topology unchanged.
- Function/decorator surface unchanged.
- `git diff --check` passed.

Tests:

- Original required integration test: **1 failed**. Single execution only.
  - Failure: `KeyError: 'parent_revision_id'` at line 1293.
  - No Runtime refusal emitted.
  - No retry or neighborhood suite run.
- Registry controls: **6 + 27 + 26 passed**.
- Scoped Ruff, private mypy, vendor lock, artifact manifest: **passed**.

Identities remained stable before/after:

- Worker: `8f5c7329c8`, tree `dd4367f3`
- Runtime: `8ea0766f5e`, tree `6047ac30`
- Home Agent remained `7aa96ae6`; its fixture blob stayed at the pre-change `12c3798d`.

Commit message written to the required path, and `DONE` marker created. The integration remains blocked on the observed response-shape failure; no speculative correction was made.