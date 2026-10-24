# F-ABA attachment review

Verdict: **FAIL for integrated attachment; offline runner controls PASS.**

Finding: commit `546d868…` adds only the runner and offline test. It does not add a candidate `tests/suites.conf.candidate` row or install input. The current managed row `authoring-current-becfe-nodes` invokes pytest directly and contains no runner, plugin, or sink arguments. Therefore the production caller does not use the attachment, and durable service-log retention is unverified.

Checks:

- Targeted existing 19 + new runner test: **20 passed**
- Ruff: **passed**
- Mypy typecheck-v2, Python 3.12, silent imports: **passed**
- `git diff --check`: **passed**
- Pinned Agent/Runtime/module/profile/Node guards: **passed**
- Offline missing, oversize, partial, no-overlay, and child-exit controls: **passed**
- Original test blob and product/Runtime/registry bytes unchanged.
- No original/live/full/service execution performed.

Own XML: `evidence/targeted.xml` (3,234 bytes). Author XML was present at `/tmp/w-09e7c3de01/agt-F-ABA-capture-attach-1004.xml`; not recreated or used as current proof.

No source changes were made. DONE marker and commit message were prepared.