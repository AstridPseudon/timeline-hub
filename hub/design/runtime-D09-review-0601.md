## Verdict: PASS — exact-original mapping only

Reviewed `tl/rt-F-D09-remainder-0557` against Agent `2007cf7…`.

- Receipt `agent-F-D09-invocation-return-2255.md`: `3 passed in 510.58s`.
- Exact selectors verified and collected:
  - `...test_public_checkout_check_uses_retained_managed_scene_result`
  - `...test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[candidate]`
  - `...test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[saved]`
- Test blob SHA-256 is identical across current `HEAD`, reviewed `6562cde…`, and integrated `bf40ca…`: `03d79f9e…`.
- Both test bodies are AST-identical to the original `ce1d1cca8` bodies; saved/candidate parameterization and all predicates/assertions remain intact.
- Production path verified statically: `Checkout.open()` binds client/project/timeline → `Checkout.check()` → `_managed_scene_spans()` → managed `rendering.timeline_visualize` Scene invocation.
- Relevant managed-path source files are byte-identical to integrated `bf40ca…` (`check.py`, filmstrip dispatch, scene-only invocation, invocation plumbing). `Checkout.open()` has only later additive publication plumbing in this path.

Evidence run:

```text
pytest --collect-only tests/integrations/test_d09_managed_scene_only.py
3 tests collected

source import-origin probe
PASS: Agent modules resolved to this worktree; runtime_protocol resolved to Runtime 1d9ddba…

git diff --check
PASS

git status
clean
```

No duplicate three-case body run, full suite, browser, HTTP/C0, installed-profile, or provider run was performed.

Scope caveat: retained behavior ran with Runtime `8ea0766f`; Runtime `1d9ddba…` was import-probed only. I make no current-`1d9ddba` behavior claim. C0 v2 request/reply qualification remains unclaimed. Raw 2255 evidence files were not available in this sandbox beyond the durable receipt summary.

No product or test files changed. Commit message and `DONE` marker created.