## F-D09-remainder report

Result: lossless exact-original proof mapping; no product or test changes.

- Required selectors map exactly to the existing three-node PASS receipt in `agent-F-D09-invocation-return-2255.md`: `3 passed in 510.58s`.
- Current test blob is byte-identical to reviewed D09 fixture `6562cde…` and integrated `bf40ca…`.
- Both test bodies are AST-identical to the pre-fixture originals; parameters, predicates, assertions, and custody guards are preserved.
- Current production caller: `Checkout.open()` binds Runtime client/project/timeline; `Checkout.check()` enters `_check()`; `_managed_scene_spans()` invokes managed `rendering.timeline_visualize` Scene output.

Evidence:

- Source import probe using Agent `2007cf7aaf` and Runtime `1d9ddba546` — passed; imports resolved to the assigned Agent tree and `/home/user/work/runtime`.
- `git diff --check` — passed.
- Worktree remains clean.
- No duplicate live pytest run: exact original behavior already has a retained qualified receipt. The retained live receipt used Runtime `8ea0766f`; current Runtime import custody was verified, but current Runtime `1d9ddba546` behavior was not re-executed.
- C0 v2 HTTP/request-reply, installed-profile, and full-suite scope remain unclaimed.

Commit message and `DONE` marker were created; harness will commit no code changes.